# Requirements Traceability Matrix

This matrix links each requirement to its acceptance criteria, the tests that verify it, and its current verification status. It provides a single, auditable view from product intent to evidence of completion.

It is a living document. Update it in the same change that adds, modifies, or verifies a requirement.

Related documents:

- `docs/PRODUCT_REQUIREMENTS.md` — the source of requirement definitions and IDs.
- `docs/TEST_PLAN.md` — coverage targets, continuous evaluation, and the gap log.

## Conventions

- **Requirement ID**: matches the ID in `docs/PRODUCT_REQUIREMENTS.md` (for example, `FR-001`, `NFR-001`).
- **Level**: `MUST`, `SHOULD`, `COULD`, or `WON'T`.
- **Acceptance criteria**: the verifiable conditions for the requirement (may be referenced as `FR-001-AC-1`).
- **Verifying tests**: the test names, files, or IDs that exercise the requirement (`T-xxx` IDs live in `tests/test_site.sh`; `V-xxx` IDs live in `tests/validate_html.py`).
- **Status**: `Not Started`, `In Progress`, `Verified`, or `Deferred`.

A requirement with no verifying test is a coverage gap. Record it in `docs/TEST_PLAN.md` (gap log) and in `TODO.md` under Testing.

## Functional Requirements

| Requirement ID | Level | Description | Acceptance Criteria | Verifying Tests | Status |
| --- | --- | --- | --- | --- | --- |
| FR-001 | MUST | Every promised section is present and nav links resolve | FR-001-AC-1 | T-020, T-021, T-022, T-023 | Verified |
| FR-002 | MUST | Page states it is not open; describes handmade small-batch intent | FR-002-AC-1 | T-030, T-031, T-032 | Verified |
| FR-003 | MUST | No commerce that does not exist | FR-003-AC-1, FR-003-AC-2 | T-033, T-034 | Verified |
| FR-004 | MUST | Unavailable facts are marked placeholders, never invented | FR-004-AC-1, FR-004-AC-2, FR-004-AC-3 | T-050, T-051, T-052, T-053 | Verified |
| FR-005 | MUST | Era-inspired only; no third-party franchise or character names | FR-005-AC-1, FR-005-AC-2, FR-005-AC-3 | T-040, T-041, T-042 | Verified |
| FR-006 | MUST | Push to `main` publishes, gated on tests | FR-006-AC-1 | T-005 (workflow present); the gate itself is exercised by every CI run | Verified |
| FR-007 | MUST | Publishing config targets the apex domain consistently | FR-007-AC-1 | T-017, T-080, T-081, T-082 | Verified |
| FR-008 | SHOULD | Themed, non-indexed 404 page | FR-008-AC-1 | T-004, V-001..V-010 (404.html validated) | Verified |
| FR-010 | SHOULD | The site presents a recognisable icon in browser chrome | FR-010-AC-1, FR-010-AC-2 | T-092, T-093, T-094, T-095, T-096 | Verified |
| FR-011 | SHOULD | A shared link unfurls with a branded preview card | FR-011-AC-1, FR-011-AC-2 | T-097, T-098, T-099, T-100, T-101 | Verified |
| FR-009 | WON'T | Online sales are out of scope this release | FR-009-AC-1 | T-034 (asserts no cart or checkout copy exists) | Verified |

## Non-Functional Requirements

| Requirement ID | Level | Description | Acceptance Criteria | Verifying Tests | Status |
| --- | --- | --- | --- | --- | --- |
| NFR-001 | MUST | No runtime dependencies | NFR-001-AC-1 | T-060, T-061, T-062, T-063 | Verified |
| NFR-002 | MUST | Light/dark theming, OS-following, persisted, no flash | NFR-002-AC-1, NFR-002-AC-2 | T-070, T-071, T-072 | Verified |
| NFR-003 | MUST | WCAG AA text contrast in both themes | NFR-003-AC-1, NFR-003-AC-2 | T-076, T-077 (token wiring, structural); L-010-2, L-020-2, L-030-2, L-040-2 (measured in-browser, both themes, both widths) | Verified |
| NFR-004 | MUST | Keyboard and screen-reader navigable | NFR-004-AC-1, NFR-004-AC-2 | T-016, T-074, V-002, V-003, V-005, V-006, V-007, V-008, V-009, V-010 | Verified |
| NFR-005 | MUST | Respects reduced motion; works without JavaScript | NFR-005-AC-1, NFR-005-AC-2 | T-073, T-075 | Verified |
| NFR-006 | SHOULD | Page weight budget | NFR-006-AC-1 | T-090, T-091 | Verified |
| NFR-007 | SHOULD | Layout holds at desktop and mobile widths in both themes | NFR-007-AC-1, NFR-007-AC-2 | L-0x0-3 (no horizontal scroll), L-0x0-4 (nothing escapes the viewport), L-0x0-5 (no text under 12px) | Verified |

## Coverage Gaps

| Gap ID | Requirement | What is not verified automatically | Tracked in |
| --- | --- | --- | --- |
| GAP-003 | NFR-003-AC-1 | `tests/test_layout.sh` measures the real ratios, but skips where no browser exists — including CI. A change pushed from such a machine would not be checked. Mitigated per-defect by structural guards (`T-076`, `T-077`) that run everywhere; that mitigation covers known decisions, not new ones. | `docs/TEST_PLAN.md` |
