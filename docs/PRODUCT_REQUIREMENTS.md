# Product Requirements

This document translates product intent into concrete implementation requirements.

Each requirement carries a stable ID and explicit acceptance criteria. The mapping from requirement to verifying test is tracked in `docs/REQUIREMENTS_TRACEABILITY.md`.

## Requirement Levels

- `MUST`: Required for the current release or MVP.
- `SHOULD`: Important, but can be deferred if needed.
- `COULD`: Useful future enhancement.
- `WON'T`: Explicitly out of scope for the current release or MVP.

## Requirement Identifiers

- Functional requirements use the prefix `FR-` (for example, `FR-001`).
- Non-functional requirements use the prefix `NFR-` (for example, `NFR-001`).
- Acceptance criteria may carry sub-identifiers (for example, `FR-001-AC-1`).
- IDs are stable and never reused for a different requirement, even after one is removed or superseded.

## Product Summary

A single-page placeholder website for **PicklesToys**, a handmade small-batch
toy workshop that has not launched. Published via GitHub Pages at
`picklestoys.com`. The target reader is anyone who types the domain in early —
a friend, a potential stockist, a curious visitor. The release goal is a page
that is honest about the stage the business is at, has real visual identity,
and can absorb products later without being rebuilt.

The defining constraint: **the site must not overstate what exists.** No
products, prices, launch dates, or contact details are invented. Several
requirements below exist specifically to keep that true as the site is edited.

## Functional Requirements

### Page content

**FR-001** The page presents every section the navigation promises.

- Level: `MUST`
- Acceptance criteria:
  - `FR-001-AC-1`: the `what`, `look`, and `news` sections are present, and every in-page nav link resolves to a real element id.

**FR-002** The page states the business is not open and describes the intent accurately.

- Level: `MUST`
- Acceptance criteria:
  - `FR-002-AC-1`: the page says it is not open yet, and describes handmade production and small batches.

**FR-003** The page never advertises commerce that does not exist.

- Level: `MUST`
- Acceptance criteria:
  - `FR-003-AC-1`: no price figures appear on the page.
  - `FR-003-AC-2`: no cart, checkout, buy-now, or pre-order copy appears.

**FR-004** Unavailable real-world facts are shown as marked placeholders, never invented.

- Level: `MUST`
- Acceptance criteria:
  - `FR-004-AC-1`: contact is either a real `mailto:` link or the marked `CONTACT-EMAIL-TBD` placeholder.
  - `FR-004-AC-2`: a placeholder, when present, is visually flagged by the `.tbd` treatment.
  - `FR-004-AC-3`: no fabricated social handles, example.com addresses, or lorem ipsum.

### Brand and intellectual property

**FR-005** The site draws on the early-90s cartoon *era* and never on a specific franchise.

- Level: `MUST`
- Acceptance criteria:
  - `FR-005-AC-1`: no third-party show, studio, network, or character name appears anywhere in the published HTML, comments included.
  - `FR-005-AC-2`: the footer carries a non-affiliation statement.
  - `FR-005-AC-3`: the boundary is documented in `docs/BRAND.md`.

### Publishing

**FR-006** Pushing to `main` publishes the site, gated on the test suite.

- Level: `MUST`
- Acceptance criteria:
  - `FR-006-AC-1`: a deploy workflow exists that runs `tests/test_site.sh` before the deploy step.

**FR-007** Publishing configuration targets the registered apex domain.

- Level: `MUST`
- Acceptance criteria:
  - `FR-007-AC-1`: `site/CNAME` names `picklestoys.com`, and the canonical URL, sitemap, and robots directives agree with it.

**FR-008** A reader who requests a missing page gets a themed, non-indexed 404.

- Level: `SHOULD`
- Acceptance criteria:
  - `FR-008-AC-1`: `site/404.html` exists and shares the site styling.

**FR-010** The site presents a recognisable icon in browser chrome.

- Level: `SHOULD`
- Acceptance criteria:
  - `FR-010-AC-1`: an SVG icon, an ICO fallback, and an apple-touch icon exist and are linked from both published pages.
  - `FR-010-AC-2`: the rasters are generated from the SVG by a committed, dependency-free script rather than hand-produced, so they can be regenerated after a design change.

**FR-011** A shared link unfurls with a branded preview card.

- Level: `SHOULD`
- Acceptance criteria:
  - `FR-011-AC-1`: a 1200x630 PNG card exists, generated from a committed SVG source by a committed script.
  - `FR-011-AC-2`: `og:image` and `twitter:image` are absolute URLs on the canonical host, and the declared dimensions match the actual file.

**FR-012** The site's generated design assets stay reproducible from committed sources.

- Level: `SHOULD`
- Acceptance criteria:
  - `FR-012-AC-1`: the doodle field and burst polygons in `site/styles.css` are produced by a committed generator, and a check re-derives them so hand-edits fail the build.
  - `FR-012-AC-2`: decorative shapes behind text are painted as real backgrounds on an ancestor of that text, so the contrast a reader gets is the contrast the suite measures.

## Non-Functional Requirements

**NFR-001** The site has no runtime dependencies.

- Level: `MUST`
- Acceptance criteria:
  - `NFR-001-AC-1`: no external resource is fetched from another origin, no remote `@import`, no web font, and no `package.json` in `site/`.

**NFR-002** The site is usable in both light and dark themes, following the operating system until the reader chooses otherwise.

- Level: `MUST`
- Acceptance criteria:
  - `NFR-002-AC-1`: a theme toggle exists, the choice persists, and the theme is applied before first paint.
  - `NFR-002-AC-2`: dark-mode tokens are defined.

**NFR-003** The site meets WCAG 2.1 AA for text contrast.

- Level: `MUST`
- Acceptance criteria:
  - `NFR-003-AC-1`: every text/background pair measures at least 4.5:1 in both themes.
  - `NFR-003-AC-2`: small orange text uses the AA-safe `--orange-text` token rather than the vivid brand `--orange`.

**NFR-004** The page is navigable by keyboard and screen reader.

- Level: `MUST`
- Acceptance criteria:
  - `NFR-004-AC-1`: a skip link targets a `<main>` landmark.
  - `NFR-004-AC-2`: the document passes the structural accessibility validator (single `h1`, no skipped heading levels, no duplicate ids, every image has alt text, every button has a discernible name).

**NFR-005** The page respects a reader's reduced-motion preference and works without JavaScript.

- Level: `MUST`
- Acceptance criteria:
  - `NFR-005-AC-1`: animations are disabled under `prefers-reduced-motion`.
  - `NFR-005-AC-2`: content is not hidden when JavaScript is unavailable.

**NFR-006** The page stays light enough to load quickly on a phone.

- Level: `SHOULD`
- Acceptance criteria:
  - `NFR-006-AC-1`: the three core files total under 100KB, and no committed asset exceeds 400KB.

**NFR-007** The layout holds at both phone and desktop widths, in both themes.

- Level: `SHOULD`
- Acceptance criteria:
  - `NFR-007-AC-1`: the page never scrolls horizontally, and no content box extends past the viewport, at 375px and 1280px in light and dark.
  - `NFR-007-AC-2`: no rendered text is smaller than 12px.

## Out of Scope for This Release

**FR-009** Online sales, cart, checkout, or payment processing.

- Level: `WON'T`
- Rationale: there is no product yet, and a static GitHub Pages site cannot
  take payments without either an embedded third-party checkout (which would
  break `NFR-001`) or a move to the Next.js/Vercel architecture used by
  `gentle-table`. Revisit when there is something to sell.
- Acceptance criteria:
  - `FR-009-AC-1`: no cart, checkout, or payment affordance exists on the site.
