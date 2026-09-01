# Changelog

All notable user-facing changes to this project should be documented in this file.

This project follows semantic versioning.

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
