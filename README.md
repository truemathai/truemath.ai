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
│   ├── vertical.html        Renders a vertical landing page from its front matter.
│   └── redirect.html        Renders a /go/ campaign redirect (see below).
├── _includes/
│   └── tmv-blocks.html      Renders the demo result blocks (table / callout / chart).
├── _verticals/              One file per industry vertical → /for/<name>/ (see below).
├── _data/campaign_codes.yml Source of truth for /go/ campaign codes (see below).
├── _go/                     GENERATED /go/<CODE> redirect files. Don't hand-edit.
├── scripts/                 Campaign code tooling (new_code, build_go, set_post_id). Not published.
├── campaign_batches/        Batch CSVs for new_code.py --batch. Not published.
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
`truemath.ai/go/<CODE>`, where `<CODE>` is a six-character Crockford Base32 code
(`0-9` and `A-Z` minus `I L O U`, always uppercase). Each link forwards
(client-side, since the site is static) to a destination with Google Analytics
UTM parameters attached, so GA attributes the visit natively in Traffic
Acquisition. The `/go` hop itself is invisible to GA (no analytics on the
redirect page, `noindex`).

### Where the data lives

- **[`_data/campaign_codes.yml`](_data/campaign_codes.yml) is the source of
  truth.** Every code is one entry there; it is the only place campaign code
  data is edited. The schema is documented at the top of the file.
- **`_go/<CODE>.md` files are generated** by `scripts/build_go.py`, one per
  entry, and rendered by [`_layouts/redirect.html`](_layouts/redirect.html).
  Never hand-edit them: the next build overwrites them and `--check` fails.
- `scripts/` and `campaign_batches/` are excluded from the published site.

The scripts need Python 3.8+ and PyYAML (`python3 -m pip install --user pyyaml`).

### Create one code

```bash
python3 scripts/new_code.py \
  --campaign exactly \
  --series cleared-for-exactness \
  --episode ep1-weight-and-balance \
  --platform youtube \
  --placement description \
  --to /series/cleared-for-exactness#weight-and-balance \
  --note "CfE Ep1 YouTube description link"
python3 scripts/build_go.py
```

`new_code.py` picks a random unused code, derives the UTM values, appends the
entry to the YAML (comments and layout are kept), and prints the URL.
`--campaign` is the launch campaign the code belongs to (`exactly` for the
"Exactly!" MCP launch, later `live-numbers`). Other options: `--paid` (a paid ad
or boosted post), `--post-id` (the platform's ID for the post, if already
known), `--video-uid` (Cloudflare Stream clip, added as `?v=`), `--description`,
`--abbr` (override the series abbreviation), `--utm-term`, `--owner` (default
`bill`), `--destination-type` (default `landing-page`), `--qr [PATH]`,
`--expires YYYY-MM-DD`, and `--dry-run` to validate and print without writing.

UTM values are derived, never typed by hand:

| Field | Value |
| --- | --- |
| `utm_source` | the platform (`youtube`, `linkedin`, `qr`, ...) |
| `utm_medium` | youtube/tiktok/instagram = `video`; linkedin/facebook = `social`; qr = `qr`; email = `email`; podcast = `podcast`; trade-media = `referral`. With `--paid` it gets a `paid-` prefix (`paid-video`, `paid-social`, ...), which GA4's default channel grouping files under the paid channels |
| `utm_campaign` | `<campaign>-<series>`, e.g. `exactly-cleared-for-exactness` |
| `utm_content` | series abbreviation + episode + platform + placement, e.g. `cfe-ep1-youtube-description`; series-level links use `series` (`cfe-series-qr-print`) |
| `utm_id` | the code itself (added to the generated file) |

The abbreviation is the first letter of each word of the series slug
(`cleared-for-exactness` = `cfe`), or the whole word for one-word slugs (`dana`).
For paid placements use placement `ad`, so ads and organic posts get different
`utm_content` (`cfe-ep1-linkedin-ad` vs `cfe-ep1-linkedin-post`).

### Record the post ID once it's live

Codes are created before posting, so `post_id` starts empty. When the video,
post or ad is live, record the platform's ID for it (YouTube video ID, TikTok
video ID, LinkedIn post URN, Meta ad ID, ...):

```bash
python3 scripts/set_post_id.py R7K9XM dQw4w9WgXcQ
```

It edits the YAML in place (comments kept) and refuses to replace an existing
ID unless you pass `--force`. `post_id` never goes into URLs or UTMs, so there's
nothing to rebuild; it lets the campaign dashboard join platform views to codes.

### Launch a series (batch)

1. Put a CSV in `campaign_batches/` with one row per code. Required columns:
   `campaign, series, episode, platform, placement, to, video_uid, note`
   (episode and video_uid may be blank). Optional: `description, abbr,
   utm_term, owner, destination_type, expires, qr_generated, paid, post_id`
   (`paid` is true/false; blank means false).
2. `python3 scripts/new_code.py --batch campaign_batches/launch_codes.csv`.
   If any row is invalid nothing is written. On success it also writes
   `campaign_batches/launch_codes.codes.csv` listing every new code and URL.
3. `python3 scripts/build_go.py`
4. `python3 scripts/build_go.py --check`, commit to a branch, open a pull
   request. Codes go live within minutes of the merge.
5. Paste the URLs from the `.codes.csv` into the YouTube descriptions,
   LinkedIn posts, etc.

### Build and check

```bash
python3 scripts/build_go.py           # validate the YAML, regenerate every _go/*.md
python3 scripts/build_go.py --check   # write nothing; fail if invalid or _go/ is stale
python3 -m unittest discover -s scripts -p "test_*.py"   # tests for the scripts
```

`build_go.py` refuses to write anything if an entry is invalid. Warnings don't
fail the build: expired codes (they still redirect), two codes sharing a
`utm_content` (GA shows them as one row), and values that look like an email
address or phone number.

### Validation rules

- `code`: exactly six uppercase Crockford Base32 characters, unique.
- `to`: a site path starting with `/` (optionally ending in `#section`) or a full
  `http(s)` URL. UTM params are inserted before any `#section`, since browsers
  never send the fragment.
- `campaign`, `series`, `platform`, `placement` and all of `utm_source`,
  `utm_medium`, `utm_campaign`, `utm_content` are required; `campaign` and
  `series` are lowercase slugs; UTM values are lowercase with no spaces, and
  `utm_campaign` equals `<campaign>-<series>`. `platform`, `placement`
  and `destination_type` must come from the lists in the YAML header.
- `created` is a valid date; `expires`, if set, is on or after `created`.
- `video_uid`, if set, is a 32-character lowercase hex Cloudflare Stream UID, and
  `to` must not also carry `?v=`.
- `owner` is a lowercase slug (who asked for the code; never in URLs).
- `paid` is `true` or `false`.
- `post_id`, if set, has no whitespace; on YouTube codes it must be an
  11-character video ID (`A-Z a-z 0-9 _ -`).
- `qr_generated` is `false`, `true`, or a path to an existing file under
  `campaign_assets/`.
- Unknown fields are rejected, so a typo like `utm_souce` can't slip through.

### Legacy codes

The eight codes that predate this system (`099AWD`, `09G3SA`, `0BBF19`,
`8ZP2QR`, `HR67H3`, `J4K7WM`, `Q3XR9T`, `R7K9XM`) are entries with
`legacy: true`. They were migrated by `scripts/migrate_existing_codes.py` with
every field copied exactly and `created` taken from git history. Their files are
generated with exactly their original fields, and they have no `campaign`,
`paid` or `post_id` (no `utm_id`; fields they left out
fall back to the layout defaults `utm_source=go`, `utm_medium=referral`,
`utm_campaign=<CODE>`), so their redirects and GA history are unchanged. They
are exempt from the UTM naming rules.

### Notes

- **Casing matters.** Static URLs are case-sensitive; distribute codes exactly as
  written (uppercase). The generated `permalink` keeps that casing.
- `note` and `description` are internal-only: they never appear in the URL, the
  redirect, or GA. But **this repo is public**, so they are readable on GitHub.
  Keep personal or private details out of every field.
- **`utm_*` values are visible** in GA reports and briefly in the address bar.
- **The landing URL self-cleans.** Once GA has recorded the visit, the `utm_*`
  params are stripped from the address bar. The strip fires from GA's page-view
  `event_callback` (wired in [`_layouts/default.html`](_layouts/default.html)),
  only after the analytics beacon has gone out, so attribution is never lost.
- **Reading it in GA4:** the Campaign report has one row per campaign and
  series (`exactly-cleared-for-exactness`, `exactly-dana`, ...);
  Source/medium shows platform and format (paid placements show as
  `paid-*`); drill into `utm_content` for the exact placement. To trace a visit to its exact code, use the **Session campaign ID**
  dimension, which carries `utm_id`.
- `/go/` links are kept out of `sitemap.xml` and marked `noindex` automatically.
- If you ever need true server-side 302s or case-insensitive codes, move this to
  a Cloudflare Worker on `truemath.ai/go/*` reading the same YAML; the data
  model and scripts stay the same.
