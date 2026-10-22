import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://jsonformatterspro.com',
  output: 'static',
  // Keep every URL exactly as the Django site served it: /json-diff/ -> dist/json-diff/index.html
  trailingSlash: 'always',
  build: { format: 'directory' },
  // Pages are pre-built HTML; leave their whitespace alone.
  compressHTML: false,
});
