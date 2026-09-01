# Agent Handoff

Context an agent picking this repository up needs before making changes.

## What this is

The website for PicklesToys, a handmade small-batch toy workshop that **has not
launched**. Static HTML/CSS/JS in `site/`, no build step, no dependencies,
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
| `tests/test_site.sh` | 47 structural checks. The CI gate. |
| `tests/validate_html.py` | HTML + accessibility validator, standard library only. |
| `docs/BRAND.md` | Design language and the IP boundary. |
| `docs/DOMAIN_SETUP.md` | Pointing picklestoys.com at Pages. |

## Non-obvious things that will bite you

- **`.js` scoping.** The reveal animation's `opacity: 0` is scoped to a `.js`
  class added by the inline `<head>` script. Unscope it and the page goes blank
  for anyone without JavaScript. `T-075` guards both halves.
- **`--orange-text` vs `--orange`.** The vivid brand orange is 4.05:1 on the
  tinted band — below AA for the 14px bold overlines. Small orange text uses
  the darker token. `T-076` guards the wiring; token *values* are not
  automatically re-measured, so re-check contrast if you change a hex.
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

Version 0.1.0. The site builds, all 47 checks pass, and all 15 requirements
have verifying tests. What is outstanding is in `TODO.md`, and the largest
items are blocked on the owner: a real contact email, the registrar/DNS
details, and a decision about what is actually being made first.

The site is not yet live at picklestoys.com — Pages needs enabling and DNS
needs creating. Neither can be done from inside the repository.
