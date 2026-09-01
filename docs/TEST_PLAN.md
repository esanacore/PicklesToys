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
- **Browser-backed tests**: real geometry and computed contrast, measured in
  headless Chromium. Location / command: `bash tests/test_layout.sh` (`L-xxx`
  IDs), chained from the structural suite. Runs four passes — desktop and
  mobile widths against light and dark themes. **Skips cleanly with exit 0
  when the browser is unavailable**, so a bare CI runner still gets the
  structural suite as its gate.

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
- Browser suite alone: `bash tests/test_layout.sh`

`tests/test_site.sh` chains the browser suite after its own checks, so the
single command above runs everything available on the machine.

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
| 2026-08-31 | 15/15 requirements covered; 47/47 structural checks passing | Baseline at 0.1.0. Contrast measured by hand: every text pair clears AA in both themes, lowest 5.38:1. **This hand-audit was incomplete — see the 0.4.0 row.** |
| 2026-08-31 | 17/17 requirements covered; 57/57 structural checks passing | 0.3.0. Favicon and social card added, each with generator and validation checks. |
| 2026-08-31 | 17/17 requirements covered; 58/58 structural + 20/20 browser checks passing | 0.4.0. Browser suite added, closing GAP-001 and GAP-002. **It found a real defect on its first run**: `.card__num` on the first card measured 1.25:1 in dark mode, shipped since 0.1.0 and missed by the hand-audit, because the audit checked a hand-picked list of pairs and that element was not on it. Now every text node on the page is measured. |

A downward trend is a signal to investigate, even when the number stays above the floor.

## Coverage Gap Log

Track known untested behavior here. A percentage alone hides gaps; this log makes them explicit. Each entry should have a follow-up item in `TODO.md` under Testing.

| Gap ID | Area / behavior | Risk | Related requirement | Status | TODO ref |
| --- | --- | --- | --- | --- | --- |
| GAP-001 | Measured contrast ratios were computed by hand and nothing recomputed them. **Closed in 0.4.0** by `tests/test_layout.sh` L-0x0-2, which walks every text node and checks each against its own WCAG floor (3:1 for large text, 4.5:1 otherwise). Deliberately not a list of selectors — a list only covers what someone remembered to add, which is the exact failure that let the `.card__num` defect through. | med | NFR-003 | Closed | — |
| GAP-002 | No browser-backed layout suite. **Closed in 0.4.0** by `tests/test_layout.sh` L-0x0-3/4/5: horizontal overflow, content escaping the viewport, and text below 12px, each measured at two widths in both themes. | low | NFR-006 | Closed | — |
| GAP-003 | The browser suite skips where no browser exists, which includes CI. Defects it alone can see would reach production if a change were pushed from such a machine. Mitigated per-defect by a structural guard: `T-076` and `T-077` pin the two contrast decisions the suite has actually caught. That mitigation is per-defect, not general. | low | NFR-003 | Open | TODO.md, "Site work" |
