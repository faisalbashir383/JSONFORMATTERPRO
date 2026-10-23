// sitemap.xml in the same format and order as Django's (formatter/sitemaps.py):
// static pages, then blog posts, tutorials and job postings.
// Django's hand-written static list missed some pages, so every built tool page that isn't
// noindex is added after it, plus the blog category pages.
import staticPaths from '../data/sitemap-static.json';
import routes from '../data/routes.json';
import { hasData } from '../lib/db';
import { blogDetailPages, blogListPages, jobDetailPages, tutorialDetailPages } from '../lib/views';

const pageSources = import.meta.glob<string>('../pages-html/*.html', { query: '?raw', import: 'default', eager: true });
const isNoindex = (page: string) =>
  /<!--@block:meta_robots-->[^<]*noindex/.test(pageSources[`../pages-html/${page}.html`] ?? '');

const SITE_URL = 'https://jsonformatterspro.com';

type Entry = { path: string; lastmod?: string; changefreq: string; priority: string };

const entry = ({ path, lastmod, changefreq, priority }: Entry) =>
  `<url><loc>${SITE_URL}${path}</loc>${lastmod ? `<lastmod>${lastmod.slice(0, 10)}</lastmod>` : ''}` +
  `<changefreq>${changefreq}</changefreq><priority>${priority}</priority></url>`;

export async function GET() {
  // Django's list can name pages that were since removed or merged (e.g. /json-formatter/), so keep
  // only paths that are built here; the data-driven sections are built from Supabase.
  const built = new Set([...routes.map((r) => r.path), '/blog/', '/tutorials/', '/careers/']);
  const live = staticPaths.filter((path) => built.has(path));
  const entries: Entry[] = live.map((path) => ({ path, changefreq: 'weekly', priority: '0.8' }));
  const listed = new Set(live);
  for (const { path, page } of routes) {
    if (!listed.has(path) && !isNoindex(page)) entries.push({ path, changefreq: 'weekly', priority: '0.8' });
  }
  for (const { url } of await blogListPages()) {
    if (url.startsWith('/blog/category/') && !url.includes('/page/')) entries.push({ path: url, changefreq: 'weekly', priority: '0.6' });
  }
  for (const { url, context } of await blogDetailPages()) {
    entries.push({ path: url, lastmod: context.post.updated_at, changefreq: 'weekly', priority: '0.9' });
  }
  if (hasData) {
    for (const { url, context } of await tutorialDetailPages()) {
      entries.push({ path: url, lastmod: context.tutorial.updated_at, changefreq: 'weekly', priority: '0.9' });
    }
    for (const { url, context } of await jobDetailPages()) {
      entries.push({ path: url, lastmod: context.job.updated_at, changefreq: 'weekly', priority: '0.8' });
    }
  }
  const xml = '<?xml version="1.0" encoding="UTF-8"?>\n' +
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' +
    entries.map(entry).join('') + '\n</urlset>\n';
  return new Response(xml, { headers: { 'Content-Type': 'application/xml' } });
}
