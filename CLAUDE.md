# CLAUDE.md — working guidelines for this repo

This is the **TrueMath marketing site**: a static site built with **Jekyll**,
deployed by **GitHub Pages** on every push to `main`, served through Cloudflare.
The human-facing docs are in [README.md](README.md); this file is the guardrail
layer for anyone (including Claude) making changes. When in doubt, match what the
repo already does rather than introducing something new.

## Branching and merging — read this first

`main` is protected: direct pushes are rejected, and every change reaches `main`
through a reviewed pull request. **Never commit to `main`.** For any change:

1. Create a branch — `git checkout -b short-description`.
2. Commit your changes to that branch.
3. Push it and open a pull request against `main` (`gh pr create`, or the GitHub
   web UI).
4. Wait for review. A PR needs approval from **someone other than its author**
   before it can merge — you cannot approve or merge your own PR.

If a push to `main` is rejected, that is this rule working as intended — make a
branch and open a PR instead.

## Hard rules — do not break these

1. **Never paste the header, nav, mobile menu, footer, or `<head>` into a page.**
   They live once in [`_layouts/default.html`](_layouts/default.html). Every page
   uses a layout (`layout: default` or `layout: vertical`) and provides only its
   own content.
2. **One stylesheet, one design system.** All CSS is in `css/site.css` and uses
   the design tokens defined at the top (`--purple`, `--ink`, `--bg`, the
   `--font-serif/sans/mono` trio, etc.). Do **not** add new fonts, a second color
   palette, inline `<style>` blocks, or CDN/`<link>` assets. Reuse tokens.
3. **Dark mode is automatic** via `@media (prefers-color-scheme: dark)` flipping
   the `:root` tokens in `css/site.css`. Do **not** add a manual light/dark toggle
   or hardcode theme colors that won't flip. Style with the tokens and dark mode
   comes for free.
4. **Keep URLs stable.** Existing pages are `*.html` at the root; verticals are
   `/for/<name>/`. Don't rename or move files that already have a public URL
   without a redirect plan.
5. **GitHub Pages plugins only.** The build must work on stock GitHub Pages — no
   custom Jekyll plugins, no `gems` outside what `github-pages` provides.
6. **Always build before committing:** `bundle exec jekyll build` must succeed
   with no errors. Prefer `bundle exec jekyll serve` to eyeball changes.

## CTA conventions

- **"Talk to us" / contact-style CTAs** → `https://app.truemath.ai/contact`
- **"Start free" / "Get invited" / signup-style CTAs** → `https://app.truemath.ai/signup`

## Adding or editing a vertical landing page

Verticals are **data, not new pages.** Each file in `_verticals/` becomes
`/for/<filename>/` using [`_layouts/vertical.html`](_layouts/vertical.html).
To add one, copy an existing file in `_verticals/` and edit its front matter —
see the "Vertical landing pages" section of [README.md](README.md) for the full
field reference. Do **not** hand-author a new standalone vertical page.

## Translating a Claude-app mockup into this repo

Bill (and others) will prototype pages in the Claude app and hand you a
**self-contained HTML file** — its own `<head>`, its own header/footer, its own
fonts, its own color variables, often its own dark-mode toggle and inline JS.
**Do not drop that file into the repo as-is.** It would create a second design
system and duplicate the site chrome — exactly what this structure exists to
prevent. Instead, translate it:

1. **Discard the mockup's chrome:** its `<!DOCTYPE>`, `<head>`, header/nav,
   footer, and any theme-toggle button + its JS. The site provides all of that.
2. **Separate content from presentation.** Pull the actual copy, numbers, and
   any structured data out of the mockup. If it's a vertical-style page, that
   content becomes a `_verticals/*.md` file; otherwise it becomes a page body
   under a layout.
3. **Map the mockup's design to the site's system.** Replace its fonts and color
   variables with the tokens in `css/site.css`. If a component genuinely needs
   bespoke styling (e.g. the product-style demo frame), add it to `css/site.css`
   under a namespaced class prefix (the vertical demo uses `.tmv-*`) so it can't
   collide with the marketing styles — never inline it into the page.
4. **Reuse the shared behavior.** Interaction JS goes in a file under `js/`,
   written as progressive enhancement (the page should still render server-side
   without JS). Don't inline `<script>` blocks into pages.
5. **Verify:** build, then check light mode, dark mode, and a narrow viewport
   before committing.

The residential-mortgage-broker vertical is a worked example of exactly this
translation — reference it when in doubt.

## Repo-specific gotchas

- The demo's API responses are **stubbed** with captured JSON in the vertical's
  front matter; there is no live API call. Keep it that way unless explicitly
  wiring up the real endpoint.
- `sitemap.xml` is a Jekyll template that auto-includes verticals — you don't
  edit it when adding a vertical.
- `favicon.ico` stays at the repo root (browsers probe `/favicon.ico`); the other
  icons live in `icons/`.
