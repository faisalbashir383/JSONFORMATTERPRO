// Fills the slots in layouts/base.html with a page's blocks, the way Django's
// {% extends "base.html" %} / {% block %} did.
//
//   layout: <!--@block:title-->Default title<!--@end:title-->
//   page:   <!--@block:title-->JSON Diff<!--@end:title-->
//
// A page block may contain <!--@super-->, which is replaced by the layout's default
// (Django's {{ block.super }}). Blocks the page does not define keep the default.

const BLOCK = /<!--@block:(\w+)-->([\s\S]*?)<!--@end:\1-->/g;

export type Blocks = Record<string, string>;

export function parseBlocks(page: string): Blocks {
  const blocks: Blocks = {};
  for (const [, name, body] of page.matchAll(BLOCK)) blocks[name] = body;
  return blocks;
}

const SITE_URL = 'https://jsonformatterspro.com';

/**
 * Per-page SEO defaults. Without these, a page that doesn't set a block inherits the layout's
 * homepage values: canonical = homepage (Google treats the page as a duplicate) and og:url =
 * homepage (shares link to the wrong page). Social tags fall back to the page's own text.
 */
export function withSeoDefaults(blocks: Blocks, path: string): Blocks {
  const b = { ...blocks };
  const text = (k: string) => (b[k] ?? '').replace(/\s+/g, ' ').trim();
  b.canonical_url = text('canonical_url') || SITE_URL + path;
  for (const k of ['og_url', 'twitter_url']) if (!text(k)) b[k] = b.canonical_url;
  for (const k of ['og_description', 'twitter_description']) if (!text(k) && text('meta_description')) b[k] = text('meta_description');
  for (const k of ['og_title', 'twitter_title']) if (!text(k) && text('title')) b[k] = text('title');
  return b;
}

export function renderPage(layout: string, blocks: Blocks): string {
  const fill = (text: string): string =>
    text.replace(BLOCK, (_, name: string, fallback: string) => {
      const defaultHtml = fill(fallback);
      return name in blocks ? blocks[name].replaceAll('<!--@super-->', defaultHtml) : defaultHtml;
    });
  return fill(layout).replace(/^\s+/, '');
}
