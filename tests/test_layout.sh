#!/usr/bin/env bash
set -euo pipefail

# Browser-based layout and contrast tests (L-xxx checks).
#
# Renders the real page in headless Chromium (gstack browse) and asserts what
# the grep-based suite cannot see: the colours a reader actually gets, measured
# from computed style, and geometry measured from real boxes.
#
# This is what closes GAP-001 and GAP-002 in docs/TEST_PLAN.md. tests/
# test_site.sh T-076 only checks that .overline references the AA-safe token;
# it cannot tell whether that token's *value* still passes. This can.
#
# The browse daemon is a local dev tool, not a CI dependency: when it is not
# installed this suite SKIPs with exit 0, so the structural suite remains the
# gate on a bare runner. That is the same arrangement 702_with_the_view uses.

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

B="${GSTACK_BROWSE:-$HOME/.claude/skills/gstack/browse/dist/browse}"
if [ ! -x "$B" ]; then
  echo "Layout + contrast tests (headless Chromium)"
  echo "==========================================="
  echo "  SKIP  gstack browse not installed — structural checks in test_site.sh still apply"
  exit 0
fi

# file:// URL for the local page. On Git Bash, /c/... must become
# file:///C:/... — keep the leading slash (or "c:" parses as a hostname) and
# uppercase the drive letter (the daemon's path allowlist is case-sensitive).
# On macOS/Linux the sed is a no-op.
site_url="file://$(printf '%s' "$root/site/index.html" | sed -E 's#^/([a-zA-Z])/#/\U\1:/#')"

pass=0
fail=0

assert() {
  local id="$1" desc="$2" ok="$3"
  if [ "$ok" = "true" ]; then
    echo "  PASS  $id  $desc"
    pass=$((pass + 1))
  else
    echo "  FAIL  $id  $desc"
    fail=$((fail + 1))
  fi
}

run_checks() {
  # run_checks <id-prefix> <viewport> <theme>
  local prefix="$1" viewport="$2" theme="$3"
  local label="$viewport $theme"

  "$B" viewport "$viewport" >/dev/null
  "$B" goto "$site_url" >/dev/null 2>&1
  "$B" js "document.documentElement.dataset.theme='$theme'" >/dev/null
  # Force-finish the reveal animation so geometry and opacity are final
  # before measuring; otherwise every .reveal reads as transparent.
  "$B" js "document.querySelectorAll('.reveal').forEach(function(e){e.classList.add('is-visible')}); 'ok'" >/dev/null
  sleep 1

  local out
  out=$("$B" eval "$root/tests/layout_assertions.js" 2>/dev/null | grep -v "UNTRUSTED" || true)

  local checked contrast pagex offscreen tiny
  checked=$(printf '%s' "$out"  | sed -n 's/.*"textNodesChecked":\([0-9]*\).*/\1/p')
  contrast=$(printf '%s' "$out" | sed -n 's/.*"lowContrast":\[\([^]]*\)\].*/\1/p')
  pagex=$(printf '%s' "$out"    | sed -n 's/.*"pageOverflowX":\(true\|false\).*/\1/p')
  offscreen=$(printf '%s' "$out"| sed -n 's/.*"outOfViewport":\[\([^]]*\)\].*/\1/p')
  tiny=$(printf '%s' "$out"     | sed -n 's/.*"unreadableSize":\[\([^]]*\)\].*/\1/p')

  # A run that measured nothing is a broken harness, not a passing page.
  assert "$prefix-1" "page measurable ($label: ${checked:-0} text nodes)" \
    "$([ -n "$checked" ] && [ "$checked" -gt 20 ] && echo true || echo false)"

  assert "$prefix-2" "all text meets its WCAG AA floor ($label)" \
    "$([ -z "$contrast" ] && echo true || echo false)"
  [ -n "$contrast" ] && echo "          low contrast: $contrast"

  assert "$prefix-3" "no horizontal page scroll ($label)" \
    "$([ "$pagex" = "false" ] && echo true || echo false)"

  assert "$prefix-4" "no content escapes the viewport ($label)" \
    "$([ -z "$offscreen" ] && echo true || echo false)"
  [ -n "$offscreen" ] && echo "          off-viewport: $offscreen"

  assert "$prefix-5" "no text below 12px ($label)" \
    "$([ -z "$tiny" ] && echo true || echo false)"
  [ -n "$tiny" ] && echo "          too small: $tiny"

  # run_checks must not end on a failed test: under `set -e` a non-zero
  # return from the last command aborts the whole suite mid-run.
  return 0
}

echo "Layout + contrast tests (headless Chromium)"
echo "==========================================="
run_checks L-010 1280x900 light
run_checks L-020 1280x900 dark
run_checks L-030 375x812  light
run_checks L-040 375x812  dark

echo "-------------------------------------------"
echo "Passed: $pass  Failed: $fail"
[ "$fail" -eq 0 ]
