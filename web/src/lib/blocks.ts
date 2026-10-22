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

export function renderPage(layout: string, blocks: Blocks): string {
  const fill = (text: string): string =>
    text.replace(BLOCK, (_, name: string, fallback: string) => {
      const defaultHtml = fill(fallback);
      return name in blocks ? blocks[name].replaceAll('<!--@super-->', defaultHtml) : defaultHtml;
    });
  return fill(layout).replace(/^\s+/, '');
}
