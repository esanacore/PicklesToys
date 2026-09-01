# Test Plan

This document defines how this repository is tested, what coverage it targets, and where coverage gaps currently exist.

It is a living document. Update it whenever the test strategy, targets, or known gaps change.

## Test Strategy

This repository publishes a static, dependency-free website. There is no
application runtime, no state, and no build step, so the conventional test
pyramid does not map cleanly onto it. What is worth testing is different:
whether the published artifact has the structure, the honesty, and the
accessibility properties it claims.

- **Structural tests**: assertions over the published HTML/CSS/JS, run with
  `grep` so they need no runtime or package install. Location / command:
  `bash tests/test_site.sh` (`T-xxx` IDs).
- **Document validation**: HTML well-formedness and accessibility structure —
  nesting, duplicate ids, alt text, heading order, landmarks, ARIA references.
  Standard library only, so it runs on a bare CI runner. Location / command:
  `python tests/validate_html.py` (`V-xxx` IDs), invoked by the suite above.
- **Browser-backed tests**: none yet. Measured layout geometry and computed
  contrast currently require a browser, which CI runners do not have. See
  GAP-001.

### A note on what these tests are for

Several checks do not verify code behavior at all — they verify that the site
keeps telling the truth. `T-030`–`T-034` fail the build if commerce copy or a
price appears while the business has nothing to sell. `T-040` fails if a
third-party franchise name appears anywhere in the HTML. `T-050`–`T-053` fail
if a placeholder is quietly replaced with an invented value.

These are the most valuable tests in the repository. The markup will be
rewritten many times; the constraints are what must survive that.

## How to Run Tests

- Full suite: `bash tests/test_site.sh`
- Validator alone: `python tests/validate_html.py`
- Validator self-test (proves the validator can fail): `python tests/validate_html.py --selftest`

There is no coverage instrumentation: with no application code to execute,
line coverage has no meaning here. The equivalent question — "is every
requirement verified?" — is answered by `docs/REQUIREMENTS_TRACEABILITY.md`.

## Coverage Targets

Targets are a floor, not a ceiling. Changes that drop measured coverage below a floor require explicit, documented justification.

| Scope | Metric | Floor |
| --- | --- | --- |
| Product requirements | Requirements with a verifying test | 100% |
| Published HTML documents | Documents passing the structural validator | 100% |
| Accessibility | Text/background pairs meeting WCAG AA | 100% |

New or modified code should meet the floor on its own, not lean on untouched legacy code.

## Continuous Coverage Evaluation

Coverage is measured on every change (locally and, where possible, in CI). Record the latest figures here so trends stay visible.

| Date | Overall coverage | Notes |
| --- | --- | --- |
| 2026-08-31 | 15/15 requirements covered; 47/47 structural checks passing | Baseline at 0.1.0. Contrast measured by hand in a real browser: every text pair clears AA in both themes, lowest is 5.38:1 (overline on the tinted band, light mode). |

A downward trend is a signal to investigate, even when the number stays above the floor.

## Coverage Gap Log

Track known untested behavior here. A percentage alone hides gaps; this log makes them explicit. Each entry should have a follow-up item in `TODO.md` under Testing.

| Gap ID | Area / behavior | Risk | Related requirement | Status | TODO ref |
| --- | --- | --- | --- | --- | --- |
| GAP-001 | Measured contrast ratios are computed by hand in a browser and recorded in `docs/BRAND.md`. `T-076` only asserts that `.overline` is wired to the AA-safe `--orange-text` token, so changing a token *value* to something failing would not be caught. | med | NFR-003 | Open | TODO.md, "Site work" |
| GAP-002 | No browser-backed layout suite. Horizontal overflow, element containment, and mobile stacking were verified manually at 375px and 1280px, but nothing re-checks them on change. `702_with_the_view/tests/test_layout.sh` is the pattern to copy — it skips cleanly where no browser exists. | low | NFR-006 | Open | TODO.md, "Site work" |
