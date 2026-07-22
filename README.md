# truemath.ai

Public-facing marketing site for [TrueMath](https://truemath.ai). Built with
[Jekyll](https://jekyllrb.com/) and served as static HTML via GitHub Pages from
the apex domain. GitHub Pages runs the Jekyll build automatically on every push
to `main` — there is no separate build step or CI to manage.

## Structure

```
/
├── _config.yml              Site-wide settings (URL, analytics ID, theme disabled)
├── _layouts/
│   ├── default.html         The ONE shared shell: <head>, nav, mobile menu, footer.
│   │                        Edit this to change the header/footer on every page.
│   └── vertical.html        Renders a vertical landing page from its front matter.
├── _includes/
│   └── tmv-blocks.html      Renders the demo result blocks (table / callout / chart).
├── _verticals/              One file per industry vertical → /for/<name>/ (see below).
├── index.html, developers.html, teams.html, saas-fintech.html,
│   faq.html, privacy.html, terms.html, 404.html
│                            Each page is just front matter (title, description,
│                            social tags) + its own body content. No more copy-
│                            pasted headers and footers.
├── CNAME                    GitHub Pages custom domain (truemath.ai)
├── robots.txt, sitemap.xml  (sitemap auto-includes verticals)
├── css/site.css             Consolidated stylesheet (page-scoped via body class)
├── js/site.js               Consolidated behaviors (hamburger, carousel, FAQ search)
├── js/vertical-demo.js      Interactive demo + auto-scaling chart for verticals
├── images/                  Photos + logos
├── icons/                   Favicons and app icons (favicon.ico stays at root)
├── Gemfile                  Pins the same Jekyll version GitHub Pages runs
└── _site/                   Local build output (git-ignored; do not edit)
```

## How each page works

Every page starts with a small "front matter" block that fills in the shared
layout. To change a page's title, description, or social-share text, edit these
lines — you never touch the header, nav, or footer:

```yaml
---
layout: default
title: "TrueMath for Developers: Stop Hardcoding Math. Start Shipping It."
description: "A single API that gives your app deterministic, auditable calculation logic."
og_title: "TrueMath for Developers"          # optional; falls back to title
og_description: "..."                          # optional; falls back to description
body_class: page-developers                   # selects page-scoped CSS
---
```

The canonical URL and the Open Graph / Twitter `url` tags are generated
automatically from the site URL, so they never drift.

## Editing content

- **Change a nav link, the footer, analytics, or anything in `<head>`:** edit
  [`_layouts/default.html`](_layouts/default.html) once — it applies to all pages.
- **Change the words on a page:** edit that page's `.html` file below the front
  matter. This can be done entirely through the GitHub web UI (Edit → Commit),
  no local setup required.

## Vertical landing pages

Industry-specific demo pages (e.g. mortgage brokers) live in
[`_verticals/`](_verticals/). Each file is one vertical and becomes a page at
`/for/<filename>/`. They all share one design and one interactive demo — only
the words and numbers differ — so **adding a vertical means copying one file and
editing its content. No HTML, CSS, or JavaScript.**

### To add a vertical

1. In `_verticals/`, copy an existing file (e.g.
   `residential-mortgage-broker.md`) and rename it — the new filename is the URL
   (`_verticals/estate-planning.md` → `/for/estate-planning/`). This can be done
   in the GitHub web UI (Add file → Create new file, then paste).
2. Edit the front matter:
   - `title` / `description` — SEO and the browser tab.
   - `name` — the industry label shown on the pill inside each demo.
   - `hero_line` — the vertical-specific noun (e.g. "Loan decisions").
   - `demos` — the three prompts. Each has a `prompt`, a `parse` list (how the
     engine reads it), and `blocks` (the results). A block is one of:
     - `type: kv` — a heading, a description, and `lines` of label/value pairs.
     - `type: pmi` — a one-line callout (`k` label + `v` text).
     - `type: chart` — a bar chart. Put the numbers in the demo's `chart:` list;
       the chart scales its own axes automatically.
   - `proof` — the "raw LLM vs TrueMath" comparison.
   - `resolve` — the closing headline and line.
3. Commit. The page, and its entry in the sitemap, appear automatically.

The existing file is thoroughly commented as a working example. Everything a
visitor sees comes from that one file; the shared machinery lives in
[`_layouts/vertical.html`](_layouts/vertical.html),
[`_includes/tmv-blocks.html`](_includes/tmv-blocks.html),
the `.tmv-*` styles in `css/site.css`, and `js/vertical-demo.js` — none of which
need to change to add a vertical.

## Local preview

Requires Ruby (already standard on macOS). First time only:

```sh
bundle install
```

Then, to preview with live reload at <http://localhost:4000>:

```sh
bundle exec jekyll serve
```

## Deploy

Push to `main`. GitHub Pages builds the Jekyll site and publishes it to the
custom domain (`truemath.ai`, configured in repo Settings → Pages and backed by
the `CNAME` file). Nothing else to run.

## Related sites

- Blog: [blog.truemath.ai](https://blog.truemath.ai/) (WordPress.com)
- Product app: [app.truemath.ai](https://app.truemath.ai/) (separate repo)

## Analytics

Google Analytics 4 (`G-J6QKEF8PLS`) is wired into every page via the shared
layout (`gtag.js`).

## Campaign redirect links (`/go/`)

Inbound lead sources are tracked with short vanity links of the form
`truemath.ai/go/<CODE>`, where `<CODE>` is one of the pre-generated six-character
Crockford Base32 codes. Each link **302-style forwards** (client-side, since the
site is static) to a destination with Google Analytics UTM parameters attached,
so GA attributes the visit natively in Traffic Acquisition — the `/go` hop
itself is invisible to GA (no analytics on the redirect page, `noindex`).

Like verticals, these are **data, not pages.** Each assigned code is one file in
`_go/` rendered by [`_layouts/redirect.html`](_layouts/redirect.html). To put a
code into service, add `_go/<CODE>.md`:

```yaml
---
permalink: /go/<CODE>/          # REQUIRED — must match the code's exact casing
note: "Human label — where this code is being used"
to: /for/residential-mortgage-broker/   # site-relative path or absolute URL
utm_source: newsletter
utm_medium: email
utm_campaign: broker-spring
# utm_content / utm_term are optional
---
```

Notes:

- **Casing matters.** Static URLs are case-sensitive, so the `permalink` must
  match the casing of the code you actually distribute (we use canonical
  uppercase). The explicit `permalink` is required because Jekyll would
  otherwise lowercase the URL. Distribute the code exactly as written.
- `to:` accepts a site path (`/for/foo/`) or a full URL (e.g.
  `https://app.truemath.ai/signup`); UTM params are appended with the correct
  `?`/`&` separator either way.
- `/go/` links are kept out of `sitemap.xml` and marked `noindex` automatically.
- If you ever need true server-side 302s or case-insensitive codes, move this to
  a Cloudflare Worker on `truemath.ai/go/*` — the data model stays the same.
