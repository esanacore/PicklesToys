# OTS Software Inventory

This inventory tracks every off-the-shelf (OTS) software component this project depends on: third-party libraries, frameworks, runtimes, databases, and any other software the project uses but did not develop. It answers, for each component: what it is, why we use it, how risky it is, how we verified it is fit for use, and how it stays current.

The structure follows the intent of the FDA's OTS software guidance and IEC 62304's SOUP (Software of Unknown Provenance) requirements, generalized for any repository — regulated or not. For most projects it is simply the auditable answer to "what third-party software are we shipping, and is anyone watching it?"

It is a living document. Update it in the same change that adds, removes, or upgrades a dependency.

Related documents:

- `SECURITY.md` (constitution) — dependency risk review expectations and threat-modeling triggers.
- `docs/TEST_PLAN.md` — where verification evidence (test suites exercising a component) is declared.

## Conventions

- **Component ID**: a stable identifier, `OTS-001`, `OTS-002`, ... Once assigned, an ID is never reused, even after the component is removed. When a component is removed, set its Status to `Removed` rather than deleting the row.
- **Name**: the component's name **exactly as it is declared in the dependency manifest** (`package.json`, `requirements.txt`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `Gemfile`, ...). The automated checker (`constitution/scripts/check_ots_inventory.sh`) matches manifest entries against this cell by exact value (case-insensitive), so a paraphrased or prettified name counts as undocumented.
- **Risk**: `Low`, `Medium`, or `High`. A component is at least `Medium` when it sits in a trust-sensitive position — handling credentials, parsing untrusted input, or running with elevated privileges (see `SECURITY.md`'s "Threat Modeling Triggers").
- **Verification**: how fitness for use was established — for example, the project's own integration tests that exercise it, upstream test-suite maturity, vendor certification, or a manual validation record.
- **Anomaly Review**: known-issue posture — where known defects/CVEs for this component are tracked, and the date they were last reviewed.
- **Update Policy**: how the version moves — pinned exactly, pinned to a range, Dependabot/Renovate-managed, vendored, etc.
- **Status**: `Active`, `Evaluating`, or `Removed`.

## Managed Dependencies

Components declared in a dependency manifest in this repository. `constitution/scripts/check_ots_inventory.sh` cross-checks the manifests against this table, so a dependency added without a row here is flagged.

**None.** The site is deliberately dependency-free — there is no
`package.json` or any other dependency manifest, no CDN, no external font, and
no third-party script. This is enforced by `tests/test_site.sh` `T-060`
through `T-063`, and recorded as `NFR-001` in `docs/PRODUCT_REQUIREMENTS.md`.

Adding a first managed dependency is an architectural decision, not a routine
change: it introduces a build step, a lockfile, a supply-chain surface, and an
upgrade obligation to a repository that currently has none of those. It
warrants an ADR in `docs/adr/`.

## System-Level OTS

Software the project depends on that is **not** declared in a dependency manifest: operating systems, language runtimes, databases, message brokers, container base images, and similar. The checker cannot discover these automatically — keep this section honest by hand.

None of the components below ship to the reader. They are development and
publishing infrastructure only; the artifact served to a visitor is plain
HTML, CSS, and JavaScript written in this repository.

| Component ID | Name | Version | Supplier / Maintainer | Purpose | Risk | Verification | Anomaly Review | Update Policy | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OTS-101 | GitHub Pages | Hosted service | GitHub | Serves the static site and provisions TLS | Low | Site verified live over HTTPS after each deploy | GitHub status page and changelog — last reviewed 2026-08-31 | Vendor-managed; no version to pin | Active |
| OTS-102 | GitHub Actions | Hosted service | GitHub | Runs the test gate and publishes the site | Low | Every deploy exercises the workflow end to end | GitHub status page and changelog — last reviewed 2026-08-31 | Action versions pinned to majors, bumped by Dependabot | Active |
| OTS-103 | actions/checkout | v4 | GitHub | Checks the repository out in CI | Low | Exercised by every workflow run | GitHub advisories — last reviewed 2026-08-31 | Dependabot-managed | Active |
| OTS-104 | actions/configure-pages | v5 | GitHub | Configures the Pages deployment | Low | Exercised by every deploy | GitHub advisories — last reviewed 2026-08-31 | Dependabot-managed | Active |
| OTS-105 | actions/upload-pages-artifact | v3 | GitHub | Packages `site/` for publication | Low | Exercised by every deploy | GitHub advisories — last reviewed 2026-08-31 | Dependabot-managed | Active |
| OTS-106 | actions/deploy-pages | v4 | GitHub | Publishes the artifact | Low | Exercised by every deploy | GitHub advisories — last reviewed 2026-08-31 | Dependabot-managed | Active |
| OTS-107 | Python (standard library only) | 3.8+ | Python Software Foundation | Runs `tests/validate_html.py`; not shipped to readers | Low | Validator carries a self-test proving it can fail | CPython security releases — last reviewed 2026-08-31 | Whatever the runner or developer provides | Active |
| OTS-108 | Bash + coreutils | Any modern | GNU / distro | Runs `tests/test_site.sh`; not shipped to readers | Low | Suite runs clean on the CI runner and on Git Bash for Windows | Distro advisories — last reviewed 2026-08-31 | Whatever the runner or developer provides | Active |
| OTS-110 | gstack browse (headless Chromium via Playwright) | Local install | garrytan/gstack + Playwright | Runs `tests/test_layout.sh`; developer machines only, never shipped to readers and not required by CI | Low | The suite it drives caught a real 1.25:1 contrast defect on first run | Upstream repo and Playwright advisories — last reviewed 2026-08-31 | Developer-installed; the suite skips cleanly when absent | Active |
| OTS-109 | Eric's Engineering Constitution | v1.46.0 | esanacore | Governance rules and CI checkers, pinned as a Git submodule | Low | Its own checkers run against this repository in CI | Upstream repository releases — last reviewed 2026-09-01 | Pinned by submodule SHA; `constitution-version` fails the build when behind | Active |

## Review Cadence

- Review this inventory whenever a dependency is added, removed, or upgraded — in the **same change**, not a later documentation pass.
- Periodically (at least once per release), re-review the Anomaly Review column: check each `Medium`/`High` component's tracker for newly reported defects and CVEs, and refresh the last-reviewed dates.
- A dependency the checker reports as undocumented is a gap: add its row (or remove the dependency) before the change merges.
