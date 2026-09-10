# CLAUDE.md

This repository follows Eric's Engineering Constitution.

## What This Repo Is

The website for PicklesToys — a hand-finished, small-batch toy workshop that
has not launched yet. The pieces are made for **adult collectors**, not
children (decided 2026-09-10), across mixed media with a lot of 3D printing. Static HTML/CSS/JS in `site/`, no build step, no runtime
dependencies. Publishing is push-to-deploy: every push to `main` triggers
`.github/workflows/deploy-pages.yml`, which runs `tests/test_site.sh` and
deploys `site/` to GitHub Pages.

## Project-Specific Rules

- **The site must keep saying it is not open yet.** There are no products,
  prices, or launch dates. Do not invent any. `T-030`-`T-034` fail the build if
  commerce copy or a dollar figure appears. The contact address is the one
  real-world detail on the page — it was supplied by the owner, not invented,
  which is the only reason it is there.
- **The IP boundary is not negotiable.** The aesthetic is early-90s cartoon
  art direction. Naming a show, studio, network, or character — anywhere in
  the HTML, comments included — is infringement territory and fails `T-040`.
  Read `docs/BRAND.md` before touching page copy or design.
- **Real-world facts are the owner's to provide.** Leave clearly-marked TBD
  placeholders in the `.tbd` treatment rather than inventing values — an
  address that bounces is worse than no address. The contact address was the
  last outstanding one and landed 2026-09-10, so nothing on the page carries a
  placeholder today; `.tbd` is retained for the next one (`T-052b`).
- `site/` must stay dependency-free: no CDNs, no external fonts, no
  package.json. `T-060`-`T-063` enforce this.
- Small orange text uses `--orange-text`, not `--orange` — the vivid brand
  orange is 4.05:1 on the tinted band, under the AA floor (`T-076`).
- **Text on a `--sun` fill uses `--on-sun`, never `--ink` or `--on-accent`.**
  `--sun` is bright yellow in *both* themes, so its text must be dark in both;
  `--ink` and `--on-accent` invert with the theme. Getting this wrong shipped a
  1.25:1 badge for three releases (`T-077`).
- **The doodle field and burst polygons in `styles.css` are generated.** They
  live between `BEGIN GENERATED` / `END GENERATED` markers. Edit
  `tools/make_pattern.py` and re-run it; never hand-edit the block (`T-078`).
- **A shape behind text is not a background.** The title card's burst is a
  `clip-path` on a real `background-color` of an *ancestor* of the heading. An
  SVG sibling leaves the text on the page colour — it measured 1.00:1 — and
  would be invisible if the shape failed to paint (`T-080`).
- **`clip-path` clips absolutely positioned descendants.** Anything meant to
  overhang a clipped shape — the card number badges — must be a *sibling* of
  the clipped element, not a child. Getting this wrong sliced the badges in
  half along the card's torn edge (`T-102`).
- **Run `bash tests/test_layout.sh` after any colour or layout change.** The
  structural suite cannot see computed colour. The browser suite measures every
  text node; it skips silently where no browser is installed, so a green
  `test_site.sh` alone does not mean contrast was checked.

## Branching

The owner pushes directly to `main` — this is a single-maintainer repo and
push-to-publish is the intended workflow. The deploy workflow runs the test
suite before publishing, so a broken push does not take the live site down.

## Required Reading

Before making changes, read:

- `constitution/CONSTITUTION.md`
- `constitution/AI_WORKFLOW.md`
- `constitution/TESTING.md`
- `constitution/DOCUMENTATION.md`
- `constitution/SECURITY.md`
- `constitution/CODE_STYLE.md`
- `README.md`
- `TODO.md`
- `CHANGELOG.md`
- `docs/MEMORY.md`
- `docs/BRAND.md`

## gstack (Optional — delete this section if unused)

This section applies only if this project has adopted
[gstack](https://github.com/garrytan/gstack) for AI-assisted workflows.
gstack is a third-party skill suite, not a constitution requirement — if
this project doesn't use it, delete this entire section (through "Available
gstack skills" below).

If this project *does* use gstack, verify it's installed before relying on
any skill below:

```bash
test -d ~/.claude/skills/gstack/bin && echo "GSTACK_OK" || echo "GSTACK_MISSING"
```

If `GSTACK_MISSING`, the one-shot fix is `bash constitution/scripts/setup-machine.sh`
(installs Bun, gstack, goose, and goosetown together, idempotently, run
once per machine — see `constitution/INTEGRATION.md` "Provisioning a
Machine in One Step"). Or install gstack alone (requires [Bun](https://bun.sh)
v1.0+ — install with `curl -fsSL https://bun.sh/install | bash` first if
`bun --version` fails):

```bash
git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/.claude/skills/gstack
cd ~/.claude/skills/gstack && ./setup
```

On a Linux distro Playwright doesn't officially recognize yet (its browser
install fails with `Playwright does not support chromium on <distro>-x64`),
`/browse` and other browser-driving skills need one more step — a same-family
fallback build still works:

```bash
cd ~/.claude/skills/gstack/browse
PLAYWRIGHT_HOST_PLATFORM_OVERRIDE=ubuntu24.04-x64 bunx playwright install chromium chromium-headless-shell
```

(Swap `ubuntu24.04-x64` for the newest Ubuntu Playwright's installer actually
lists as supported at the time — check the error message it prints.)

- Use the `/browse` skill from gstack for **all** web browsing.
- **Never** use `mcp__claude-in-chrome__*` tools.
- Run `/setup-gbrain` once in this repository to initialize the project brain.

Available gstack skills:

- `/office-hours`
- `/plan-ceo-review`
- `/plan-eng-review`
- `/plan-design-review`
- `/design-consultation`
- `/design-shotgun`
- `/design-html`
- `/review`
- `/ship`
- `/land-and-deploy`
- `/canary`
- `/benchmark`
- `/browse`
- `/connect-chrome`
- `/qa`
- `/qa-only`
- `/design-review`
- `/setup-browser-cookies`
- `/setup-deploy`
- `/setup-gbrain`
- `/retro`
- `/investigate`
- `/document-release`
- `/document-generate`
- `/codex`
- `/cso`
- `/autoplan`
- `/plan-devex-review`
- `/devex-review`
- `/careful`
- `/freeze`
- `/guard`
- `/unfreeze`
- `/gstack-upgrade`
- `/learn`

## Completion Checklist

Before completing work:

- Confirm the requested change is implemented.
- Run `bash tests/test_site.sh` and keep it green; add tests for new behavior.
- Evaluate coverage against targets and record any gaps.
- Update requirements traceability for product-facing repositories.
- Update the OTS software inventory (`docs/OTS_SOFTWARE.md`) when third-party dependencies changed.
- Update documentation when needed.
- Update TODO.md with discovered or completed work.
- Update CHANGELOG.md for user-facing changes.
- Consider security impact.
- Propose new codebase learnings, user preferences, or major decisions to the user and (upon approval) record them in `docs/MEMORY.md`.
- Identify useful follow-up work.
- Clear or archive `docs/SESSION_PLAN.md`.
- Summarize changes and verification.