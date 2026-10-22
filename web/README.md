# JSON Formatters Pro: static site (Astro → Cloudflare Pages)

The frontend that replaces the Django templates. Every page is pre-built HTML; the
database lives in Supabase.

## Layout

| Path | What it is |
|---|---|
| `src/layouts/base.html` | The old `base.html`, with `<!--@block:NAME-->default<!--@end:NAME-->` slots |
| `src/pages-html/<page>.html` | One file per page, holding only the blocks it overrides (like a Django child template) |
| `src/data/routes.json` | URL → page file. Add a line here when you add a page |
| `src/pages/[...slug].astro` | Builds every route in `routes.json` |
| `public/static/` | CSS/JS/images, served at the same `/static/...` URLs as before |
| `public/_headers`, `public/_redirects` | Security headers and redirects (were Django middleware) |

| `src/templates/*.njk` | Blog, tutorials and careers templates (Django templates translated to Nunjucks) |
| `src/lib/views.ts` | Builds each page's data from Supabase, the way the Django views did |
| `src/lib/django.ts` | Django-compatible filters and escaping for the `.njk` templates |
| `src/pages/sitemap.xml.ts` | `sitemap.xml`; static list comes from `src/data/sitemap-static.json` |

`src/pages-html`, `src/templates` and `src/layouts/base.html` are now the source of truth. Edit them directly.
`npm run convert` regenerates them from `../templates` and **overwrites** your edits, so only
use it while the Django templates are still the ones being edited.

## Commands

```bash
npm install
npm run dev      # http://localhost:4321
npm run build    # writes dist/
```

## Cloudflare Pages settings

- Framework preset: **Astro**
- Root directory: `web`
- Build command: `npm run build`
- Output directory: `dist`
- Environment variables:
  - `NODE_VERSION` = `22`
  - `SUPABASE_URL` = `https://<project-ref>.supabase.co` (Supabase → Project Settings → API)
  - `SUPABASE_ANON_KEY` = the project's **anon / publishable** key. It is safe to use here: Row Level
    Security only lets it read published content. Never use the `service_role` key.

Without the Supabase variables the build still succeeds, but skips the blog, tutorials and careers pages.

### Blog posts in the repo (Markdown)

Add a file to `src/content/blog/<slug>.md`; the file name is the URL (`/blog/<slug>/`). The frontmatter
fields are listed at the top of `src/lib/static-posts.ts`. Start the body with `##` headings (the
title is the page's `<h1>`), and tag code blocks with a language (`json`, `javascript`, `python`,
`bash`, `yaml`) for highlighting. Repo posts and Supabase posts are listed together, newest first.

### Adding content (Supabase Table Editor)

Supabase → **Table Editor**. Fill in only the fields below; everything else (slug, timestamps,
`published_at`, `reading_time`, view counts, meta titles/descriptions) is filled in automatically
by the defaults and triggers in `supabase/migrations/20261022010000_content_defaults.sql`.

| Table | Required fields |
|---|---|
| `formatter_blogcategory` | `name` |
| `formatter_blogpost` | `title`, `category_id`, `excerpt`, `content` (HTML), tick `published` to make it live |
| `formatter_programminglanguage` | `name` (optional: `icon`, `syntax_highlight`, `order`) |
| `formatter_tutorialcategory` | `name` (optional: `icon`, `order`) |
| `formatter_tutorial` | `title`, `category_id`, `description`, `content` (HTML), tick `is_published` |
| `formatter_codeexample` | `tutorial_id`, `language_id`, `title`, `code` |
| `formatter_mcqquestion` / `formatter_mcqoption` | `tutorial_id`, `question` / `question_id`, `option_text`, `is_correct` |
| `formatter_jobposting` | `title`, `description`, `requirements`, `responsibilities` (HTML) |

Only published posts/tutorials and active jobs are visible to the site. Changes show up after the
next build (see below).

### Rebuild when content changes

Blog posts, tutorials and jobs are baked into the HTML at build time, so publishing one needs a rebuild:

1. Cloudflare Pages → your project → **Settings** → **Builds** → **Deploy hooks** → add a hook for the
   production branch and copy its URL.
2. Supabase → **Database** → **Webhooks** → **Create a new hook** on `formatter_blogpost`,
   `formatter_tutorial` and `formatter_jobposting` (insert, update, delete), type **HTTP Request**,
   method **POST**, URL = the deploy hook.

### Offline builds

`DATA_FIXTURE=/path/to/fixture.json npm run build` builds from a JSON export instead of Supabase.
Create one from the Django database with `env=development python manage.py shell < scripts/export_fixture.py`.

After adding your domain, create a Redirect Rule for `www.jsonformatterspro.com/*` →
`https://jsonformatterspro.com/${1}` (301). Django's WWWRedirectMiddleware used to do this.

## Not working yet on the static site

Server endpoints live in `functions/` (Cloudflare Pages Functions, same domain, free plan), with shared
code in `server/`. No page calls the old Django server any more:

| Endpoint | Notes |
|---|---|
| `/api/dns-lookup/` | Cloudflare DNS-over-HTTPS + ip-api.com locations |
| `/api/dummy-json/<resource>/`, `/api/dummy/*` | public fake-data API, no quota |
| `/api/contact/`, `/api/careers/apply/` | Supabase, honeypot spam check |
| `/api/typing-test/{submit,leaderboard}/` | Supabase, `tt_sid` cookie for "your best" |
| `/api/ip-lookup/`, `/api/my-ip/` | own IP from Cloudflare data; other IPs via ip-api.com (free tier is non-commercial) |
| `/api/cors-checker/` | OPTIONS + GET with the test Origin |
| `/api/ssl-checker/` | live HTTPS check + Certificate Transparency logs (Cert Spotter); no serial number |
| `/api/domain-age/`, `/api/top-domains/` | RDAP (IANA bootstrap) instead of port-43 WHOIS, cached 24 h |
| `/api/ai/generate-json/` | OpenRouter; `mode: "explain"` returns plain text (Log Analyzer) |
| `/api/webhook/*`, `/hook/<id>/` | Webhook Tester; owner = browser cookie `wh_sid` |
| `/api/mock/*`, `/api/<path>/<id>/` | Mock API; mocks are always served under `/api/` |

The homepage formatter (`static/js/app.js`) and the QR generator run entirely in the browser; tool-usage
tracking is a Google Analytics `tool_use` event.

**Cloudflare variables** (Settings → Variables and Secrets; encrypt the secrets):

| Variable | Needed for |
|---|---|
| `SUPABASE_URL`, `SUPABASE_ANON_KEY` | building blog/tutorials/careers |
| `SUPABASE_SECRET_KEY` | forms, typing test, webhooks, mocks, top domains |
| `OPENROUTER_API_KEY` | AI JSON generator / Log Analyzer explanations |
| `OPENROUTER_MODEL` | optional; comma-separated fallback list. Default: `nvidia/nemotron-3.5-lightning:free,poolside/laguna-s-2.1:free,google/gemma-4-31b-it:free` |
| `CERTSPOTTER_API_KEY` | optional; raises the SSL checker's 100 lookups/hour limit |

For local testing put the same values in `web/.dev.vars` (git-ignored), then run
`npm run build && npx wrangler pages dev dist`:

```
SUPABASE_URL=https://<project-ref>.supabase.co
SUPABASE_SECRET_KEY=sb_secret_...
OPENROUTER_API_KEY=sk-or-...
```

Also not working without a server yet: the job application form (Phase 3), and the domain-age result
pages `/domain-age/<domain>/`, which need live WHOIS data (Phase 4; also left out of sitemap.xml until then).

Differences from the Django site, because a static host can't read query strings:
- Blog pagination is `/blog/page/2/` instead of `/blog/?page=2`.
- Careers department/type filters and the tutorials `?lang=` switch show the default (unfiltered) view.
- View counters show the value at build time.
