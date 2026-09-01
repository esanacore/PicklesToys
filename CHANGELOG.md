# Changelog

All notable user-facing changes to this project should be documented in this file.

This project follows semantic versioning.

## 0.3.0 — 2026-08-31

### Added

- **Social sharing card.** `site/og-image.svg` is the source artwork;
  `site/og-image.png` (1200x630, 140KB) is rendered from it. Wired up as
  `og:image` and `twitter:image` with declared type, dimensions, and alt text,
  and the Twitter card upgraded from `summary` to `summary_large_image`.
- **`tools/make_og_image.py`** renders the PNG. Unlike the favicon, this card
  contains real text, and there is no font rasteriser in the standard library —
  so the script serves the SVG plus a small page that draws it to a canvas and
  POSTs the PNG straight back to disk. The browser is the one renderer
  guaranteed to be present, and the bytes never pass through a clipboard or a
  copy-paste step, which is the part that actually goes wrong.
- Five new checks (`T-097`–`T-101`): source and raster exist, the URLs are
  absolute and on the canonical host, the declared dimensions match the file,
  the PNG really is 1200x630 and under a 300KB budget, and the generator stays
  committed.

### Notes

- **The `og:image` URLs will not resolve until DNS is pointed at the site.**
  They are absolute and on `picklestoys.com`, because og:image requires an
  absolute URL and it must agree with the canonical host. Pointing them at the
  temporary `github.io` URL instead would bake the wrong host into every
  cached unfurl, and crawlers cache aggressively. A link shared before DNS
  lands simply unfurls without an image.
- The card's layout was corrected against measured text metrics rather than
  estimated ones: the status pill was 470px wide for a label that measures
  467px starting at x=140, so the text was overflowing its own pill, and the
  highlight stroke ended mid-word instead of under the phrase it emphasises.
- The 140KB weight is mostly the halftone dot pattern, which is
  high-frequency noise that PNG cannot compress. It is well within every
  platform limit and is fetched by crawlers, not by readers of the page.

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
