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

`src/pages-html` and `src/layouts/base.html` are now the source of truth. Edit them directly.
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
- Environment variable: `NODE_VERSION=22`

After adding your domain, create a Redirect Rule for `www.jsonformatterspro.com/*` →
`https://jsonformatterspro.com/${1}` (301). Django's WWWRedirectMiddleware used to do this.

## Not working yet on the static site

These pages call Django `/api/...` endpoints and need Phase 3/4 (Supabase tables or Edge Functions):
webhook-tester, domain-age-checker, dns-lookup, cors-checker, ssl-checker, ip-info,
dummy-json-api-playground, mock-api-generator, qr-generator, typing-test (score submit/leaderboard),
contact (form POST), and the tool-usage tracking calls in json-viewer, log-analyzer and swagger-viewer.

Not built yet (Phase 2, from Supabase): blog, tutorials, careers, domain-age result pages, sitemap.xml.
