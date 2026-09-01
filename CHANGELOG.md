# Changelog

All notable user-facing changes to this project should be documented in this file.

This project follows semantic versioning.

## 0.2.0 — 2026-08-31

### Added

- **Favicon.** `site/favicon.svg` plus a 32x32 `favicon.ico` and a 180x180
  `apple-touch-icon.png`, linked from both `index.html` and `404.html`.
- **`tools/make_favicon.py`** generates the rasters from the SVG's geometry
  using the standard library alone — no Pillow, no cairosvg, no image
  toolchain, because the repo is deliberately dependency-free. It draws the
  three shapes with 4x4 supersampled coverage and writes the PNG and ICO
  containers by hand. Re-run it after editing the SVG.
- Five new checks (`T-092`–`T-096`): the icon files exist, both pages link
  them, the 404's hrefs are root-absolute, the rasters are structurally valid
  images of the right dimensions, and the generator stays committed.

### Notes

- The favicon is a **redraw** of the header jar, not an export of it. The
  header mark has a lid, a glass body, two pickles, and 1.6–2px strokes, which
  reads at 30px and turns to mush at 16px — the size that actually matters in
  a browser tab. The favicon drops to three flat shapes with no strokes on a
  filled badge, so it holds contrast on both light and dark tab bars.
- `index.html` uses relative icon hrefs so they resolve both at the apex domain
  and at the `github.io/PicklesToys/` project URL. `404.html` uses
  root-absolute hrefs because a 404 is served for an arbitrary request path,
  where a relative href would resolve against whatever the visitor mistyped.
- `apple-touch-icon.png` is written opaque: iOS discards alpha and composites
  on black, so transparent edges would fringe.

## 0.1.0 — 2026-08-31

First commit of the site. The business has not launched, so this release is a
deliberately honest placeholder rather than a preview of a shop.

### Added

- **Placeholder landing page** (`site/index.html`). States what is true today:
  the name, the intent (handmade toys in small batches), and that nothing is
  for sale. No products, prices, launch dates, or invented contact details.
- **Design system** (`site/styles.css`). Early-90s cartoon art direction —
  chunky ink outlines, hard offset shadows, lumpy asymmetric radii, halftone
  page texture, warm paper palette. Light and dark themes, both contrast-checked
  to WCAG AA for every text pair.
- **Progressive enhancement** (`site/app.js`). Theme toggle that follows the OS
  until the reader chooses and then remembers, scroll reveal, and scrollspy.
  The page reads fine with JavaScript disabled.
- **Themed 404 page**, `robots.txt`, and `sitemap.xml`.
- **Test suite** (`tests/test_site.sh`): 47 structural checks plus a
  standard-library HTML/accessibility validator. Gates every deploy.
- **`docs/BRAND.md`** — the design language and, more importantly, the
  intellectual-property boundary: the influence is the *era*, never a specific
  show, studio, or character. Enforced by `T-040`, which fails the build if a
  franchise name appears anywhere in the HTML, comments included.
- **`docs/DOMAIN_SETUP.md`** — the checklist for pointing picklestoys.com at
  GitHub Pages, including the Cloudflare grey-cloud requirement that is the
  usual way this setup fails.
- **Push-to-deploy** via `.github/workflows/deploy-pages.yml`. Tests run before
  publishing, so a failing push leaves the previous deployment up.
- Adopted Eric's Engineering Constitution v1.44.1 as a submodule, with its
  eight CI gates.

### Notes

- `--orange-text` exists as a separate token from `--orange` because the vivid
  brand orange measures 4.05:1 on the tinted band — under the AA floor for the
  14px bold overlines. Fills and large display type keep the vivid value.
- No `og:image` or favicon yet; a meta tag pointing at a missing file unfurls
  worse than no tag at all. Tracked in `TODO.md`.
