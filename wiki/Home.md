# Home

**PicklesToys** is a hand-finished, small-batch toy workshop in the making, and this
repository is its website. The business has not launched — there are no
products, no prices, and nothing for sale — so the site is a deliberately
honest placeholder that says exactly that, built so the real thing can grow
into it later.

The site is live-published from this repository to GitHub Pages at
`picklestoys.com` on every push to `main`.

## What this project does

Serves one page. It states the name, the intent (toys made by hand, a few at a
time, built to be played with rather than displayed), and the fact that the
workshop is not open yet. It carries a real visual identity so the domain is
not parked on a blank page, and it carries a test suite that keeps the page
honest as it is edited.

The audience is whoever types the domain in early: a friend, a potential
stockist, someone who saw the name somewhere.

## Getting started

No build step, no packages, no toolchain. Clone recursively (the constitution
is a submodule), serve `site/`, and run the suite. See `docs/SETUP.md` for the
full instructions and for why verifying a fresh clone matters more than reading
`git status`.

## How it works

Static HTML, CSS, and JavaScript served straight from `site/`. What is
committed is byte-for-byte what is served — no server, no database, no build.
`app.js` is progressive enhancement only: theme toggle, scroll reveal,
scrollspy, footer year. The page reads fine with JavaScript disabled.

Publishing is a single GitHub Actions workflow that runs the test suite and
then deploys. The gate runs *before* the deploy, so a failing push leaves the
previous deployment live.

See `docs/ARCHITECTURE.md` for the detailed version, including why this
repository is shaped like `702_with_the_view` rather than like `gentle-table`.

## Where things live

| Directory | What is in it |
| --- | --- |
| `site/` | The website — everything GitHub Pages publishes |
| `tests/` | The structural suite and the HTML/accessibility validator |
| `docs/` | Governance and project documentation |
| `constitution/` | Submodule: Eric's Engineering Constitution |
| `.github/workflows/` | The deploy workflow plus eight constitution CI gates |

## The two rules to read before changing anything

1. **The site must not overstate what exists.** No invented products, prices,
   dates, or contact details. Placeholders stay visibly marked.
2. **The aesthetic is an era, not a franchise.** The look draws on early-90s
   cartoon art direction. Naming a specific show, studio, or character is
   infringement territory and fails the build.

Both are enforced by tests, not just documented. `docs/BRAND.md` explains the
second one and where exactly the line sits.

## See also

- `docs/HELP.md` — common questions and troubleshooting
- `docs/BRAND.md` — design language and the intellectual-property boundary
- `docs/DOMAIN_SETUP.md` — pointing picklestoys.com at GitHub Pages
- `docs/OPERATIONS.md` — running and operating the project
- `docs/AGENT_HANDOFF.md` — context for an agent picking this up cold
