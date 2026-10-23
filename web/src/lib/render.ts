// Renders a translated Django template (src/templates/<name>.njk) with a context and
// puts its blocks into layouts/base.html.
import nunjucks from 'nunjucks';
import layout from '../layouts/base.html?raw';
import { createEnvironment } from './django';
import { parseBlocks, renderPage, withSeoDefaults } from './blocks';

const SITE = { SITE_URL: 'https://jsonformatterspro.com', SITE_NAME: 'JSON Formatters Pro' };

const sources = import.meta.glob<string>('../templates/*.njk', { query: '?raw', import: 'default', eager: true });
const env = createEnvironment();
const compiled = new Map<string, nunjucks.Template>();

/** `path` is the page's URL path, used for its default canonical and og:url. */
export function renderTemplate(name: string, context: Record<string, unknown>, path: string): string {
  if (!compiled.has(name)) {
    const src = sources[`../templates/${name}.njk`];
    if (!src) throw new Error(`template ${name}.njk not found`);
    compiled.set(name, nunjucks.compile(src, env, name));
  }
  const html = compiled.get(name)!.render({ ...SITE, messages: [], ...context });
  return renderPage(layout, withSeoDefaults(parseBlocks(html), path));
}
