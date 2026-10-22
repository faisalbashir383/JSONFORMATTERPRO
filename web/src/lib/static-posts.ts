// Blog posts kept in the repo as Markdown: src/content/blog/<slug>.md
//
// ---
// title: "How to Fix Unexpected Token Errors in JSON"
// category: "JSON Guides"
// excerpt: "One or two sentences for the listing page and search results."
// meta_description: "Up to ~155 characters for Google."      (optional, defaults to excerpt)
// meta_keywords: "json error, unexpected token"
// tags: "JSON, Debugging"
// published_at: "2026-10-20T09:00:00+00:00"
// updated_at: "2026-10-20T09:00:00+00:00"                   (optional, defaults to published_at)
// author_name: "Faisal Ahmad"                                (optional)
// author_profile_url: "https://github.com/..."               (optional)
// ---
// Markdown body...
//
// They render through the same templates as Supabase posts and are merged with them.
import { marked } from 'marked';
import type { Row } from './db';

const files = import.meta.glob<string>('../content/blog/*.md', { query: '?raw', import: 'default', eager: true });

const slugify = (s: string) =>
  s.normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase()
    .replace(/[^\w\s-]/g, '').replace(/[-\s]+/g, '-').replace(/^[-_]+|[-_]+$/g, '');

function parseFrontmatter(raw: string, file: string) {
  const m = raw.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!m) throw new Error(`${file}: missing --- frontmatter ---`);
  const data: Record<string, string> = {};
  for (const line of m[1].split('\n')) {
    const kv = line.match(/^(\w+):\s*(.*)$/);
    if (!kv) continue;
    let value = kv[2].trim();
    if (value.startsWith('"') && value.endsWith('"')) value = JSON.parse(value);
    data[kv[1]] = value;
  }
  for (const key of ['title', 'category', 'excerpt', 'published_at']) {
    if (!data[key]) throw new Error(`${file}: frontmatter needs "${key}"`);
  }
  return { data, body: m[2] };
}

export function staticPosts(): Row[] {
  return Object.entries(files).map(([path, raw]) => {
    const slug = path.split('/').pop()!.replace(/\.md$/, '');
    const { data, body } = parseFrontmatter(raw, path);
    const content = marked.parse(body, { async: false }) as string;
    const words = content.split(/\s+/).filter(Boolean).length;
    return {
      id: `static:${slug}`,
      slug,
      title: data.title,
      category_slug: slugify(data.category),
      category_name: data.category,
      excerpt: data.excerpt,
      content,
      tags: data.tags ?? '',
      meta_description: data.meta_description || data.excerpt,
      meta_keywords: data.meta_keywords ?? '',
      published: true,
      published_at: data.published_at,
      created_at: data.published_at,
      updated_at: data.updated_at || data.published_at,
      views: 0,
      reading_time: Math.max(1, Math.floor(words / 200)),
      author_name: data.author_name || 'JSON Formatters Pro',
      author_profile_url: data.author_profile_url ?? '',
    };
  });
}
