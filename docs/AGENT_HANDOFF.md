# Agent Handoff

Context an agent picking this repository up needs before making changes.

## What this is

The website for PicklesToys, a hand-finished small-batch toy workshop that
**has not launched**. Pieces are for **adult collectors**, not children —
mixed media with a lot of 3D printing. Static HTML/CSS/JS in `site/`, no build step, no dependencies,
published to GitHub Pages on every push to `main`.

Start with `README.md`, then `docs/BRAND.md`. The second one is not optional —
it holds the constraint most likely to be violated by an agent working from a
one-line prompt.

## The two constraints that matter most

**1. The site must not overstate what exists.**

There are no products, prices, launch dates, or contact details. The page says
so plainly. If asked to "make it look more like a real store," the correct
response is to ask what actually exists yet — not to invent a catalog. Tests
`T-030` through `T-034` and `T-050` through `T-053` fail the build on invented
commerce copy, prices, fake handles, or lorem ipsum.

**2. The aesthetic is an era, never a franchise.**

The project brief was "toys inspired by Rugrats." The *look* of early-90s kids
television is fair to draw on; the characters, names, and marks are Paramount's
and using them is infringement. `T-040` greps the entire HTML — comments
included — for franchise and character names and fails the build if one
appears. It has already caught this once, during the initial build, when the
word appeared in a source comment.

Do not weaken that test to make a change pass. If a change genuinely needs to
reference a franchise, that is a business and legal decision for the owner, not
a test edit.

## Where things live

| Path | What |
| --- | --- |
| `site/index.html` | The whole page. Single file, commented by section. |
| `site/styles.css` | Design system. Color tokens in three blocks at the top. |
| `site/app.js` | Theme toggle, scroll reveal, scrollspy, footer year. Progressive enhancement only. |
| `tests/test_site.sh` | 66 structural checks. The CI gate. Chains the browser suite. |
| `tests/test_layout.sh` | Browser suite (`L-xxx`): measured contrast + geometry. Skips without a browser. |
| `tests/layout_assertions.js` | What the browser suite evaluates in-page. |
| `tests/validate_html.py` | HTML + accessibility validator, standard library only. |
| `tools/make_pattern.py` | Generates the doodle field + burst clip-paths into styles.css. |
| `docs/BRAND.md` | Design language and the IP boundary. |
| `docs/DOMAIN_SETUP.md` | Pointing picklestoys.com at Pages. |

## Non-obvious things that will bite you

- **`.js` scoping.** The reveal animation's `opacity: 0` is scoped to a `.js`
  class added by the inline `<head>` script. Unscope it and the page goes blank
  for anyone without JavaScript. `T-075` guards both halves.
- **`--orange-text` vs `--orange`.** The vivid brand orange is 4.05:1 on the
  tinted band — below AA for the 14px bold overlines. Small orange text uses
  the darker token (`T-076`).
- **`--on-sun` does not change between themes, on purpose.** `--teal` and
  `--grape` invert with the theme so text on them uses `--on-accent`, which
  inverts too. `--sun` stays bright yellow in both, so its text must stay dark
  in both. Using `--ink` or `--on-accent` there produced a 1.25:1 badge that
  shipped for three releases (`T-077`).
- **`clip-path` also clips absolutely positioned descendants.** The card
  badges overhang the torn edge, so they must be siblings of `.card__panel`,
  never children of it (`T-102`).
- **A shape drawn behind text is not that text's background.** The burst is a
  clip-path on a real background-color of an ancestor. The first version used
  an SVG sibling and measured 1.00:1, because the heading's actual background
  was the cream page (`T-080`).
- **`styles.css` contains a generated region** between `BEGIN GENERATED` and
  `END GENERATED`. Change `tools/make_pattern.py`, re-run it, never edit the
  block (`T-078`).
- **A green `test_site.sh` does not mean contrast was checked.** The browser
  suite skips silently where no browser is installed. Run
  `bash tests/test_layout.sh` after any colour or layout change and confirm the
  `L-xxx` checks ran rather than skipped.
- **The theme script must stay before first paint.** It lives inline in
  `<head>`, before the stylesheet. Moving it into `app.js` reintroduces a
  flash of the wrong theme. `T-071` cannot detect position.
- **`T-060` allows `picklestoys.com` URLs** but rejects any other origin. The
  canonical and `og:url` tags are absolute on purpose.
- **The maintainer's global gitignore excludes `lib/`, `build/`, `dist/`,
  `bin/`, `packages/`.** This repo uses none of those names today. If you
  introduce one, the files will be silently omitted from commits — verify with
  a fresh clone, not `git status`. See `docs/SETUP.md`.

## Current state

Version 0.8.0. The site builds, all 66 structural and 20 browser checks pass,
and all 19 requirements have verifying tests.

**Live at https://picklestoys.com since 2026-09-10**, over HTTPS with a valid
certificate and an http->https redirect. DNS is GoDaddy. `og:image` resolves
at the apex, so link previews work.

One known wrinkle: the certificate covers the apex only, so
`https://www.picklestoys.com` fails TLS. `www` CNAMEs to `esanacore.github.io`
correctly and redirects over http; GitHub had not extended the certificate to
it as of the last check. See `docs/DOMAIN_SETUP.md`.

What is outstanding is in `TODO.md`. The largest item still blocked on the
owner is deciding what is actually being made first — including whether it is
aimed at children, which decides whether CPSIA applies.
