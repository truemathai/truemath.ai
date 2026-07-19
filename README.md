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
│   └── default.html         The ONE shared shell: <head>, nav, mobile menu, footer.
│                            Edit this to change the header/footer on every page.
├── index.html, developers.html, teams.html, saas-fintech.html,
│   faq.html, privacy.html, terms.html, 404.html
│                            Each page is just front matter (title, description,
│                            social tags) + its own body content. No more copy-
│                            pasted headers and footers.
├── CNAME                    GitHub Pages custom domain (truemath.ai)
├── robots.txt, sitemap.xml
├── css/site.css             Consolidated stylesheet (page-scoped via body class)
├── js/site.js               Consolidated behaviors (hamburger, carousel, FAQ search)
├── images/                  Photos + logos
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
