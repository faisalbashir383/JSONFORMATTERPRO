#!/usr/bin/env python3
"""
Convert the Django templates into plain-HTML block files for the Astro site in web/.

Runs without Django (plain python3, standard library only):

    python3 scripts/convert_templates.py

Output:
    web/src/layouts/base.html     base.html with <!--@block:NAME-->default<!--@end:NAME--> slots
    web/src/pages-html/<name>.html one file per page, holding only the blocks that page overrides
    web/src/data/routes.json      URL path -> page file, for [...slug].astro

Tags are resolved the same way Django renders them with an empty request context:
{% static %} and {% url %} become real paths, {{ SITE_URL }} / {{ SITE_NAME }} become the
site constants, {% if %} with no data takes its else branch, {% for %} renders nothing,
{% verbatim %} content is copied untouched.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / 'templates'
WEB = ROOT / 'web'

SITE_URL = 'https://jsonformatterspro.com'
SITE_NAME = 'JSON Formatters Pro'

# Pages rendered from database rows; they are built from Supabase in Phase 2.
DYNAMIC_TEMPLATES = {
    'blog_list.html', 'blog_detail.html', 'careers.html', 'job-detail.html',
    'tutorials-list.html', 'tutorial-detail.html', 'domain-age-result.html',
}
SKIP_TEMPLATES = {'base.html', '500.html', 'test.html'}
# Translated to Nunjucks (web/src/templates/*.njk) and rendered from Supabase data.
# domain-age-result.html needs live WHOIS data, so it waits for Phase 4.
NUNJUCKS_TEMPLATES = [
    'blog_list.html', 'blog_detail.html', 'careers.html', 'job-detail.html',
    'tutorials-list.html', 'tutorial-detail.html',
]

TAG_RE = re.compile(r'\{%\s*(.*?)\s*%\}', re.S)
VAR_RE = re.compile(r'\{\{\s*(.*?)\s*\}\}', re.S)
COMMENT_RE = re.compile(r'\{#.*?#\}', re.S)

warnings = []


# ---------------------------------------------------------------- URL names

def load_url_names():
    """Map Django URL names to paths by reading the urls.py files."""
    names = {'index': '/'}
    for f in ('formatter/urls.py', 'apiutils/urls.py'):
        src = (ROOT / f).read_text()
        for m in re.finditer(r"path\(\s*'([^']*)'\s*,\s*[\w.]+(?:\.as_view\([^)]*\))?\s*,\s*name='([^']+)'", src):
            route, name = m.groups()
            if '<' not in route:
                names[name] = '/' + route
    return names


def load_view_templates():
    """Map URL path -> template file, by pairing urls.py view names with render() calls."""
    view_tpl = {}
    for f in ('formatter/views.py', 'apiutils/views.py'):
        src = (ROOT / f).read_text()
        for chunk in re.split(r'\n(?=def )', src):
            m = re.match(r'def (\w+)\(request\)', chunk)
            t = re.search(r"render\(\s*request\s*,\s*['\"]([^'\"]+)['\"]", chunk)
            if m and t:
                view_tpl[m.group(1)] = t.group(1)
    routes = {'/': 'index.html'}
    for f in ('formatter/urls.py', 'apiutils/urls.py'):
        src = (ROOT / f).read_text()
        for m in re.finditer(r"path\(\s*'([^'<]*)'\s*,\s*views\.(\w+)\s*,", src):
            route, view = m.groups()
            if view in view_tpl:
                routes['/' + route] = view_tpl[view]
    return routes


def load_url_routes():
    """Map Django URL names to routes, keeping parameters (e.g. 'blog/<slug:slug>/')."""
    routes = {}
    for f in ('formatter/urls.py', 'apiutils/urls.py'):
        src = (ROOT / f).read_text()
        for m in re.finditer(r"path\(\s*'([^']*)'\s*,\s*[\w.]+\s*,\s*name='([^']+)'", src):
            routes[m.group(2)] = '/' + m.group(1)
    return routes


URL_NAMES = load_url_names()
URL_ROUTES = load_url_routes()


# ---------------------------------------------------------------- rendering

def split_verbatim(text):
    """Yield (is_verbatim, chunk) pieces."""
    pos = 0
    for m in re.finditer(r'\{%\s*verbatim\s*%\}(.*?)\{%\s*endverbatim\s*%\}', text, re.S):
        yield False, text[pos:m.start()]
        yield True, m.group(1)
        pos = m.end()
    yield False, text[pos:]


def render_var(expr, where):
    name = expr.split('|')[0].strip()
    if name == 'SITE_URL':
        return SITE_URL
    if name == 'SITE_NAME':
        return SITE_NAME
    if name == 'block.super':
        return '<!--@super-->'
    # Django renders unknown variables as an empty string.
    warnings.append(f'{where}: {{{{ {expr} }}}} rendered as empty')
    return ''


def render_tag(tag, where):
    parts = tag.split()
    kind = parts[0]
    if kind in ('load', 'csrf_token'):
        return ''
    if kind == 'static':
        return '/static/' + parts[1].strip('\'"')
    if kind == 'url':
        name = parts[1].strip('\'"')
        if name not in URL_NAMES:
            warnings.append(f'{where}: unknown url name {name!r}')
            return '#'
        return URL_NAMES[name]
    warnings.append(f'{where}: unsupported tag {{% {tag} %}} removed')
    return ''


def resolve_control(text, where):
    """Resolve {% if %} (always false: there is no request data) and drop {% for %} loops."""
    tokens = re.split(r'(\{%\s*(?:if|elif|else|endif|for|empty|endfor)\b.*?%\})', text, flags=re.S)
    out, stack = [], []  # stack of (kind, emitting_before, branch_taken)

    def emitting():
        return all(s[1] for s in stack)

    for tok in tokens:
        m = re.match(r'\{%\s*(\w+)(.*?)%\}$', tok, re.S)
        kind = m.group(1) if m else None
        if kind == 'if':
            stack.append(['if', False, False])
        elif kind == 'elif':
            stack[-1][1] = False
        elif kind == 'else':
            top = stack[-1]
            top[1] = not top[2]  # take else when no earlier branch matched
        elif kind == 'endif':
            stack.pop()
        elif kind == 'for':
            stack.append(['for', False, False])
        elif kind == 'empty':
            stack[-1][1] = True  # loops are empty, so {% empty %} renders
        elif kind == 'endfor':
            stack.pop()
        elif emitting():
            out.append(tok)
    if stack:
        warnings.append(f'{where}: unbalanced if/for')
    return ''.join(out)


def render(text, where):
    text = COMMENT_RE.sub('', text)
    out = []
    for verbatim, chunk in split_verbatim(text):
        if verbatim:
            out.append(chunk)
            continue
        chunk = resolve_control(chunk, where)
        chunk = TAG_RE.sub(lambda m: render_tag(m.group(1), where), chunk)
        chunk = VAR_RE.sub(lambda m: render_var(m.group(1), where), chunk)
        out.append(chunk)
    return ''.join(out)


# ---------------------------------------------------------------- blocks

def parse_blocks(text):
    """Return {name: raw_content} for the outermost blocks, and the text with block bodies marked."""
    blocks, marked, stack, pos = {}, [], [], 0
    for m in re.finditer(r'\{%\s*(block\s+(\w+)|endblock(?:\s+\w+)?)\s*%\}', text):
        if m.group(1).startswith('block'):
            if not stack:
                marked.append(text[pos:m.start()])
            stack.append((m.group(2), m.end()))
        else:
            name, start = stack.pop()
            if not stack:
                blocks[name] = text[start:m.start()]
                marked.append(f'\x00{name}\x00')
                pos = m.end()
    marked.append(text[pos:])
    return blocks, ''.join(marked)


def convert_base():
    raw = (TEMPLATES / 'base.html').read_text()

    def mark(text):
        blocks, marked = parse_blocks(text)
        for name, body in blocks.items():
            inner = mark(body)  # nested blocks keep their own slots
            marked = marked.replace(f'\x00{name}\x00', f'<!--@block:{name}-->{inner}<!--@end:{name}-->')
        return marked

    return render(mark(raw), 'base.html')


def convert_page(path):
    raw = path.read_text()
    where = str(path.relative_to(TEMPLATES))
    if not re.search(r'\{%\s*extends', raw):
        return render(raw, where)  # standalone document, used as-is
    blocks, _ = parse_blocks(raw)
    parts = []
    for name, body in blocks.items():
        parts.append(f'<!--@block:{name}-->{render(body, where)}<!--@end:{name}-->')
    return '\n'.join(parts) + '\n'


# ---------------------------------------------------------------- Nunjucks

COMPARISON_OPS = {'==', '!=', '<', '>', '<=', '>=', 'in'}
PATH_RE = re.compile(r'^[A-Za-z_][\w.]*$')

# Pagination links: ?page=N only works with a server, so the static site uses /page/N/ URLs.
PAGINATION_LINKS = {
    '?page={{ page_obj.previous_page_number }}{% if current_category %}&category={{ current_category }}{% endif %}':
        '{{ page_obj.previous_page_url }}',
    '?page={{ page_obj.next_page_number }}{% if current_category %}&category={{ current_category }}{% endif %}':
        '{{ page_obj.next_page_url }}',
}


def nj_filters(expr):
    """Django 'a|f:arg|g' -> Nunjucks 'a|f(arg)|g', with Django's output rules applied."""
    parts = [p.strip() for p in re.split(r'\|(?=(?:[^"\']|"[^"]*"|\'[^\']*\')*$)', expr)]
    head = re.sub(r'^(.*)\.count$', r'\1|length', parts[0])
    head = re.sub(r'\.all$', '', head)
    out = [head]
    for f in parts[1:]:
        name, _, arg = f.partition(':')
        out.append(f'{name}({arg})' if arg else name)
    return out


def nj_var(expr):
    """{{ expr }}: Django prints True/False/None, so finish with the |py filter (before |safe)."""
    parts = nj_filters(expr)
    if parts[-1] == 'safe':
        parts.insert(len(parts) - 1, 'py')
    else:
        parts.append('py')
    return '{{ ' + '|'.join(parts) + ' }}'


def nj_condition(cond):
    """Wrap bare operands in |pytruth: empty lists are falsy in Django but truthy in JS."""
    tokens = cond.split()
    out = []
    for i, tok in enumerate(tokens):
        prev = tokens[i - 1] if i else None
        nxt = tokens[i + 1] if i + 1 < len(tokens) else None
        if (PATH_RE.match(tok) and tok not in ('and', 'or', 'not', 'True', 'False', 'None')
                and prev not in COMPARISON_OPS and nxt not in COMPARISON_OPS):
            out.append(f'({"|".join(nj_filters(tok))}|pytruth)')
        else:
            out.append({'True': 'true', 'False': 'false', 'None': 'none'}.get(tok, tok))
    return ' '.join(out)


def nj_url(args):
    name, *params = args.split()
    route = URL_ROUTES.get(name.strip('\'"'))
    if route is None:
        warnings.append(f'nunjucks: unknown url name {name}')
        return '#'
    values = [p.split('=', 1)[-1] for p in params]
    for v in values:
        route = re.sub(r'<[^>]+>', '{{ ' + v + ' }}', route, count=1)
    return route


def nj_tag(tag, where):
    kind, _, rest = tag.partition(' ')
    rest = rest.strip()
    if kind in ('load', 'csrf_token'):
        return ''
    if kind == 'static':
        return '/static/' + rest.strip('\'"')
    if kind == 'url':
        return nj_url(rest)
    if kind in ('if', 'elif'):
        return '{% ' + kind + ' ' + nj_condition(rest) + ' %}'
    if kind == 'for':
        target, _, iterable = rest.partition(' in ')
        iterable = '|'.join(nj_filters(iterable.strip()))
        if iterable == 'page_obj':
            iterable = 'page_obj.object_list'
        return '{% for ' + target.strip() + ' in ' + iterable + ' %}'
    if kind == 'empty':
        return '{% else %}'
    if kind in ('else', 'endif', 'endfor'):
        return '{% ' + kind + ' %}'
    warnings.append(f'{where}: unsupported tag {{% {tag} %}} removed')
    return ''


def to_nunjucks(text, where):
    for old, new in PAGINATION_LINKS.items():
        text = text.replace(old, new)
    text = COMMENT_RE.sub('', text)
    text = text.replace('forloop.counter', 'loop.index').replace('forloop.last', 'loop.last')
    text = text.replace('forloop.first', 'loop.first')

    def var(m):
        expr = m.group(1)
        if expr in ('SITE_URL', 'SITE_NAME'):
            return {'SITE_URL': SITE_URL, 'SITE_NAME': SITE_NAME}[expr]
        if expr == 'csrf_token':
            return ''
        return nj_var(expr)

    # Variables first: the tag pass emits Nunjucks {{ }} (e.g. url slugs) that must stay as-is.
    text = VAR_RE.sub(var, text)
    return TAG_RE.sub(lambda m: nj_tag(m.group(1), where), text)


def convert_nunjucks(path):
    raw = path.read_text()
    blocks, _ = parse_blocks(raw)
    where = path.name
    parts = []
    for name, body in blocks.items():
        parts.append(f'<!--@block:{name}-->{to_nunjucks(body, where)}<!--@end:{name}-->')
    return '\n'.join(parts) + '\n'


def main():
    (WEB / 'src/layouts').mkdir(parents=True, exist_ok=True)
    (WEB / 'src/pages-html').mkdir(parents=True, exist_ok=True)
    (WEB / 'src/data').mkdir(parents=True, exist_ok=True)

    (WEB / 'src/layouts/base.html').write_text(convert_base())

    url_for_template = load_view_templates()
    routes = []
    for url, tpl in sorted(url_for_template.items()):
        # robots.txt / llms.txt are plain files in web/public.
        if tpl in DYNAMIC_TEMPLATES or tpl in SKIP_TEMPLATES or not tpl.endswith('.html'):
            continue
        src = TEMPLATES / tpl
        if not src.exists():
            warnings.append(f'{url}: template {tpl} not found')
            continue
        name = tpl.removesuffix('.html').replace('/', '__')
        (WEB / f'src/pages-html/{name}.html').write_text(convert_page(src))
        routes.append({'path': url, 'page': name})

    # 404 page is served by Cloudflare Pages from /404.html.
    (WEB / 'src/pages-html/404.html').write_text(convert_page(TEMPLATES / '404.html'))

    (WEB / 'src/data/routes.json').write_text(json.dumps(routes, indent=2) + '\n')

    # Static part of sitemap.xml, in the order of StaticViewSitemap.items() in formatter/sitemaps.py.
    sitemap_src = (ROOT / 'formatter/sitemaps.py').read_text()
    items = re.search(r'class StaticViewSitemap.*?return \[(.*?)\]', sitemap_src, re.S).group(1)
    names = [n.split(':')[-1] for n in re.findall(r"'([^']+)'", items)]
    missing = [n for n in names if n not in URL_NAMES]
    if missing:
        warnings.append(f'sitemap: unknown url names {missing}')
    sitemap_paths = [URL_NAMES[n] for n in names if n in URL_NAMES]
    (WEB / 'src/data/sitemap-static.json').write_text(json.dumps(sitemap_paths, indent=2) + '\n')

    (WEB / 'src/templates').mkdir(parents=True, exist_ok=True)
    for tpl in NUNJUCKS_TEMPLATES:
        out = WEB / 'src/templates' / tpl.replace('.html', '.njk')
        out.write_text(convert_nunjucks(TEMPLATES / tpl))

    print(f'converted {len(routes)} pages + 404, {len(NUNJUCKS_TEMPLATES)} Nunjucks templates')
    for w in warnings:
        print('warning:', w, file=sys.stderr)


if __name__ == '__main__':
    main()
