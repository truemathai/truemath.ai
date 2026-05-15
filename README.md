# truemath.ai

Public-facing marketing site for [TrueMath](https://truemath.ai). Static HTML served via GitHub Pages from the apex domain.

## Structure

```
/                            Static HTML pages
├── index.html, developers.html, teams.html, saas-fintech.html,
│   faq.html, privacy.html, terms.html
├── CNAME                    GitHub Pages custom domain (truemath.ai)
├── robots.txt
├── sitemap.xml
├── css/site.css             Consolidated stylesheet (page-scoped via body class)
├── js/site.js               Consolidated behaviors (hamburger, carousel, FAQ search)
└── images/                  Photos + logos
    └── logos/
```

The blog lives at [blog.truemath.ai](https://blog.truemath.ai/) (WordPress.com).
The product app is at [app.truemath.ai](https://app.truemath.ai/) (separate repo).

## Local preview

```sh
python3 -m http.server 8000
```

Then open [http://localhost:8000](http://localhost:8000).

## Deploy

`main` auto-deploys to GitHub Pages. The custom domain (`truemath.ai`) is configured in repo Settings → Pages, backed by the `CNAME` file at the repo root.

## Analytics

Google Analytics 4 (`G-J6QKEF8PLS`) is wired into every page via `gtag.js`.
