# Changelog

All notable user-facing changes to this project should be documented in this file.

This project follows semantic versioning.

## 0.7.1 — 2026-09-10

### Fixed

- **A stale comment in `index.html` was shipping to the live page**, still
  describing the contact address as a deliberate placeholder — and crediting
  `T-070` (the theme-toggle check) for accepting it, which was never that
  test's job. Rewritten to describe what is actually there and cite `T-050`
  and `T-051`.

### Added

- **`T-105`: every `T-xxx` cited in `site/` or `tools/` must exist in the
  suite.** A comment naming a test ID reads as a guarantee; one naming an ID
  that does not exist is worse than no comment, and nothing was checking. The
  five other citations in the source all resolved correctly — this was the
  only wrong one, and now it cannot recur. Verified against a bogus id.

## 0.7.0 — 2026-09-10

### Added

- **A real contact address.** `pureheartmakerstuff@gmail.com`, as a `mailto:`
  link in the sticker treatment used elsewhere on the page. This was the last
  marked placeholder on the site; `CONTACT-EMAIL-TBD` and its loud `.tbd`
  callout are gone.
- Copy inviting the mail, so the address is not just sitting there unexplained
  under a heading that says there is nothing to buy.

### Changed

- **`T-050` now asserts the real address rather than accepting either state.**
  It previously passed if *either* a marked placeholder or a `mailto:` was
  present, which was correct while one was pending — but with a real address
  live, that shape would also have passed if someone deleted it.
- **`T-051` is now a drift guard**: the visible link text and the `mailto:`
  target must name the same address. They are written twice and can diverge,
  and a link that displays one address while mailing another is worse than no
  link at all. Verified against a deliberately drifted copy.
- The old placeholder check moves to `T-052b`, so a future TBD still has to be
  visibly flagged.

### Notes

- The `.tbd` CSS is retained although nothing uses it today. `CLAUDE.md`
  instructs that unavailable facts ship as visibly-marked placeholders in that
  treatment; deleting the style would mean reinventing it for the next one.
- The address is a plain `mailto:` on a public page, so it will be scraped by
  address harvesters in time. That is the normal trade for being reachable.
  If the spam becomes a nuisance, the fix is a forwarding alias rather than
  obfuscating the link — obfuscation mostly defeats screen readers and
  keyboard users while barely inconveniencing scrapers.

## 0.6.0 — 2026-09-10

### Changed

- **The content cards and palette swatches now speak the title-card language.**
  The redesign in 0.5.0 converted the hero and section labels to jagged burst
  cards but left everything below in the older rounded vocabulary, so the page
  read as a hybrid. Both are converted:
  - Cards are **torn-paper panels** — a ragged polygon whose edges wobble,
    generated per card from its own seed so no two are alike, over an ink rim.
  - The numbered badges are **small bursts** rather than discs.
  - Swatch chips are bursts with an ink rim instead of organic blobs.
- `tools/make_pattern.py` gained `ragged_rect()` and a round `badge` burst, so
  every shape on the page still comes from one generator and one seeded RNG.

### Fixed

- **Card badges were being sliced in half by their own card.** `clip-path`
  clips absolutely positioned descendants, so while the badge was a child of
  the clipped panel the card's torn edge cut straight through it and it
  rendered as a pennant. The clipped rim/fill pair now lives in its own
  `.card__panel`, with the badge a sibling of it. Guarded by `T-102`.
- **Card fill overflowed its panel by twice its margin.** `height: 100%` plus
  `margin: 4px` makes a 212px-tall fill inside a 204px card; the clip then
  carved wedges out of the edges. Flex sizing accounts for margins correctly.

### Notes

- The first ragged edge used 7 points per side at 2.4% wobble, which on a
  344px card is a 16px excursion across 29px of travel — it read as bite marks
  rather than a tear. Amplitude and frequency have to be read together: 11
  points at 1.5% reads as paper. The reasoning is recorded in
  `ragged_rect()`'s docstring rather than left as bare constants.
- Three new checks (`T-102`–`T-104`) pin the layering, the real-background
  rule, and the use of generated shapes. `T-102` was verified against a
  deliberately reintroduced defect — a guard that cannot fail proves nothing.

## 0.5.0 — 2026-09-10

### Changed

- **The site now uses a title-card visual language**, developed from a 90s
  cartoon title card supplied as a reference: a torn angular burst holding the
  words, sitting on a densely scribbled field.
  - The page background is a **doodle field** — three seeded layers of
    scattered marks at coprime tile sizes, so the repeat is not perceptible.
    It replaces the halftone dots.
  - The hero headline sits inside a **burst title card**; the three section
    labels sit in smaller burst tags.
  - The smooth blobs and the squiggle underline are gone. They were a rounder
    vocabulary and reading both at once just muddled the page.
- The social card was rebuilt in the same language, reusing the *same* burst
  polygon and doodle marks the page uses, so the two cannot drift apart.

### Added

- **`tools/make_pattern.py`** generates the doodle field and the burst
  polygons into a marked region of `styles.css`. `--check` re-derives them and
  compares, wired up as `T-078`, so hand-editing that region fails the build
  instead of silently drifting from its source.
- `T-079` (generator committed) and `T-080` (the title card paints a real
  background behind its text).

### Notes

- **The burst is a `clip-path` on a real background, not an SVG behind the
  text.** The first implementation used an inline `<svg>` sibling, and the
  browser suite immediately measured the heading at **1.00:1** — because the
  text's actual CSS background was the cream page, not the purple shape. That
  is not a false positive: had the SVG failed to paint, the cream text would
  have been invisible on cream. Clipping a background-color keeps the jagged
  edge *and* keeps the contrast real and measurable.
- The field is ~27KB of generated CSS. Emitting each mark only where it
  actually crosses a tile edge, rather than all nine 3x3 offsets, produced
  byte-identical output at ~15% of the size. Core files are 59KB of the
  100KB budget.
- All 61 structural and 20 browser checks pass, in both themes at both widths.

## 0.4.1 — 2026-09-01

### Changed

- Updated the `constitution` submodule from 1.44.1 to **1.45.0**. Caught by the
  daily `Constitution Version Check` drift gate, not by anything in this repo.
  All eight governance checkers pass unchanged under the new version — 1.45.0
  adds no newly-required files — and all nine shipped workflow templates are
  byte-identical to the copies here, so no re-sync was needed.

## 0.4.0 — 2026-08-31

### Fixed

- **The numbered badge on the first card was unreadable in dark mode.** It sets
  a `--sun` background but no colour, so it inherited `.card__num`'s
  `var(--ink)` — near-black in light, cream in dark. Cream on bright yellow
  measures **1.25:1**, against a 4.5:1 floor. Shipped in 0.1.0 and present in
  every release since.

  The fix is a new `--on-sun` token, deliberately **not** redefined per theme:
  `--sun` is a bright yellow in both themes, so text on it must be dark in
  both. `--on-accent` inverts with the theme, which is correct for `--teal` and
  `--grape` (they invert too) and wrong here.

### Added

- **`tests/test_layout.sh` + `tests/layout_assertions.js`** — browser-backed
  layout and contrast tests (`L-xxx`), run in headless Chromium across desktop
  and mobile widths in both themes. Chained from `tests/test_site.sh`, and
  **skips cleanly with exit 0 where no browser exists**, so a bare CI runner
  still has the structural suite as its gate.
- `T-077`, a structural guard for the badge defect above, so the specific
  regression is caught even where the browser suite skips.
- `NFR-007`, covering layout integrity at both widths in both themes.

### Notes

- **The contrast suite does not take a list of selectors to check.** It walks
  every text node on the page and measures each against its own WCAG floor
  (3:1 for large text, 4.5:1 otherwise), compositing translucent backgrounds up
  the ancestor chain to find the colour actually painted behind the text.

  This is the whole point. The previous hand-audit checked a hand-picked list
  of pairs, and `.card__num` was not on it — which is exactly why a 1.25:1
  defect survived three releases. A list only ever covers what someone
  remembered to add.
- The suite found that defect on its first run.
- GAP-001 and GAP-002 are closed. GAP-003 is opened in their place and is
  honest about what remains: the browser suite skips in CI, so defects only it
  can see are guarded per-defect by `T-076`/`T-077` rather than in general.

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
- Adopted Eric's Engineering Constitution as a submodule, with its
  eight CI gates.

### Notes

- `--orange-text` exists as a separate token from `--orange` because the vivid
  brand orange measures 4.05:1 on the tinted band — under the AA floor for the
  14px bold overlines. Fills and large display type keep the vivid value.
- No `og:image` or favicon yet; a meta tag pointing at a missing file unfurls
  worse than no tag at all. Tracked in `TODO.md`.
