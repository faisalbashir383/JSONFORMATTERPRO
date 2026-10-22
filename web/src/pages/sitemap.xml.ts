// sitemap.xml in the same format and order as Django's (formatter/sitemaps.py):
// static pages, then blog posts, tutorials and job postings.
// Approved domain-age pages are added back once those pages exist again (Phase 4).
import staticPaths from '../data/sitemap-static.json';
import { hasData } from '../lib/db';
import { blogDetailPages, jobDetailPages, tutorialDetailPages } from '../lib/views';

const SITE_URL = 'https://jsonformatterspro.com';

type Entry = { path: string; lastmod?: string; changefreq: string; priority: string };

const entry = ({ path, lastmod, changefreq, priority }: Entry) =>
  `<url><loc>${SITE_URL}${path}</loc>${lastmod ? `<lastmod>${lastmod.slice(0, 10)}</lastmod>` : ''}` +
  `<changefreq>${changefreq}</changefreq><priority>${priority}</priority></url>`;

export async function GET() {
  const entries: Entry[] = staticPaths.map((path) => ({ path, changefreq: 'weekly', priority: '0.8' }));
  if (hasData) {
    for (const { url, context } of await blogDetailPages()) {
      entries.push({ path: url, lastmod: context.post.updated_at, changefreq: 'weekly', priority: '0.9' });
    }
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
