#!/usr/bin/env bash
set -euo pipefail

# Automated checks for the static site (constitution Principle 2).
#
# The site is dependency-free static HTML/CSS/JS, so these are structural
# assertions run with grep — no runtime or package install required, which
# keeps CI honest on a bare ubuntu runner. Test IDs (T-xxx) are referenced
# from docs/REQUIREMENTS_TRACEABILITY.md.

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
site="$root/site"
index="$site/index.html"

pass=0
fail=0

# Detected up front rather than at the validator: T-095 needs it too.
if command -v python >/dev/null 2>&1; then PY=python
elif command -v python3 >/dev/null 2>&1; then PY=python3
else PY=""; fi

check() {
  # check <test-id> <description> <command...>
  local id="$1" desc="$2"
  shift 2
  if "$@" >/dev/null 2>&1; then
    echo "  PASS  $id  $desc"
    pass=$((pass + 1))
  else
    echo "  FAIL  $id  $desc"
    fail=$((fail + 1))
  fi
}

echo "Site structural tests"
echo "====================="

# --- T-001 .. T-007: required files exist -------------------------------
check T-001 "index.html exists"            test -f "$index"
check T-002 "styles.css exists"            test -f "$site/styles.css"
check T-003 "app.js exists"                test -f "$site/app.js"
check T-004 "404.html exists"              test -f "$site/404.html"
check T-005 "deploy workflow exists"       test -f "$root/.github/workflows/deploy-pages.yml"
check T-006 "robots.txt exists"            test -f "$site/robots.txt"
check T-007 "sitemap.xml exists"           test -f "$site/sitemap.xml"

# --- T-010 .. T-017: page head and structure ----------------------------
check T-010 "has an html5 doctype"         grep -qi '^<!DOCTYPE html>' "$index"
check T-011 "has a <title>"                grep -q '<title>.*PicklesToys.*</title>' "$index"
check T-012 "has viewport meta (mobile)"   grep -q 'name="viewport"' "$index"
check T-013 "has meta description"         grep -q 'name="description"' "$index"
check T-014 "links styles.css"             grep -q 'href="styles.css"' "$index"
check T-015 "links app.js"                 grep -q 'src="app.js"' "$index"
check T-016 "skip-to-content link"         grep -q 'class="skip-link"' "$index"
check T-017 "canonical url is the apex"    grep -q 'rel="canonical" href="https://picklestoys.com/"' "$index"

# --- T-020 .. T-023: every section the nav promises is present ----------
check T-020 "what section present"         grep -q 'id="what"' "$index"
check T-021 "look section present"         grep -q 'id="look"' "$index"
check T-022 "news section present"         grep -q 'id="news"' "$index"
check T-023 "every nav link resolves" bash -c '
  for href in $(grep -o "class=\"nav__links\"" -A 6 "'"$index"'" | grep -o "href=\"#[a-z]*\"" | cut -d\" -f2); do
    id="${href#\#}";
    grep -q "id=\"$id\"" "'"$index"'" || { echo "dangling nav link: $href"; exit 1; };
  done
'

# --- T-030 .. T-034: the page states only what is true today ------------
# The business has no products, prices, or launch date yet. These assertions
# exist so a future edit cannot quietly add invented commerce copy: the site
# must keep saying it is not open until someone deliberately changes a test.
check T-030 "states it is not open yet"    grep -qi 'not open yet' "$index"
check T-031 "describes handmade toys"      grep -qi 'handmade' "$index"
check T-032 "describes small batches"      grep -qi 'small batch' "$index"
check T-033 "no invented prices" bash -c '
  ! grep -qE "\\\$[0-9]" "'"$index"'"
'
check T-034 "no shop or cart claims" bash -c '
  ! grep -qiE "add to cart|buy now|checkout|pre-?order now" "'"$index"'"
'

# --- T-040 .. T-042: intellectual-property guardrails -------------------
# The aesthetic is 90s-cartoon-era inspired. Naming another company's show,
# characters, or marks would turn homage into infringement, so the page must
# never contain them and must carry the non-affiliation line. See docs/BRAND.md.
check T-040 "no third-party franchise or character names" bash -c '
  ! grep -qiE "rugrats|nickelodeon|nicktoon|reptar|tommy pickles|chuckie|paramount|viacom|angelica|spumco|ren & stimpy|hey arnold" "'"$index"'"
'
check T-041 "non-affiliation disclaimer present" bash -c '
  grep -qi "not affiliated" "'"$index"'"
'
check T-042 "brand boundary is documented"  test -f "$root/docs/BRAND.md"

# --- T-050 .. T-053: placeholders are marked, never invented ------------
# Real-world facts (email, socials, prices, dates) are the owner to provide.
# A placeholder must be visibly a placeholder; an invented address that
# bounces is worse than none at all.
# The address landed 2026-09-10. Until then this accepted either a marked
# placeholder or a real mailto, which was right while one was pending — but
# now that a real address is live, that shape would also pass if someone
# deleted it. It asserts the real thing instead.
check T-050 "contact address is a real mailto" bash -c '
  grep -q "href=\"mailto:[^\"@]*@[^\"]*\"" "'"$index"'" &&
  ! grep -q "CONTACT-EMAIL-TBD" "'"$index"'"
'
# The visible text and the href must name the same address. They are written
# twice, so they can drift, and a link that displays one address while mailing
# another is worse than no link.
check T-051 "link text matches the mailto target" "$PY" - "$index" <<'EOF'
import re, sys
html = open(sys.argv[1], encoding="utf-8").read()
links = re.findall(r'href="mailto:([^"]+)"[^>]*>([^<]+)<', html)
assert links, "no mailto link found"
for target, text in links:
    assert target.strip() == text.strip(),         f"mailto target {target!r} does not match link text {text!r}"
EOF
# The .tbd treatment is retained for the next unavailable fact; if one is
# reintroduced it must still be visibly flagged.
check T-052b "any reintroduced TBD is visually flagged" bash -c '
  if grep -q "CONTACT-EMAIL-TBD" "'"$index"'"; then
    grep -q "class=\"tbd\"" "'"$index"'";
  fi
'
check T-052 "no placeholder social handles" bash -c '
  ! grep -qiE "@yourhandle|instagram.com/TBD|example.com" "'"$index"'"
'
check T-053 "no lorem ipsum" bash -c '
  ! grep -qi "lorem ipsum" "'"$index"'" "'"$site"'/404.html"
'

# --- T-060 .. T-063: dependency-free, per constitution Principle 7 ------
# Absolute URLs to picklestoys.com itself are fine and expected (canonical,
# og:url, sitemap). What must never appear is a resource fetched from another
# origin — that is the dependency the constitution forbids.
check T-060 "no external resources" bash -c '
  offenders=$(grep -oE "(src|href)=\"https?://[^\"]*" "'"$index"'" "'"$site"'/404.html" |
    grep -v "picklestoys\.com" || true);
  [ -z "$offenders" ] || { echo "$offenders"; exit 1; }
'
check T-061 "no package.json in site/"     test ! -f "$site/package.json"
check T-062 "no @import of remote css" bash -c '
  ! grep -qE "@import[^;]*https?://" "'"$site"'/styles.css"
'
check T-063 "no external fonts" bash -c '
  ! grep -qiE "fonts.googleapis|fonts.gstatic|@font-face" "'"$site"'/styles.css"
'

# --- T-070 .. T-074: theming and accessibility --------------------------
check T-070 "theme toggle button present"  grep -q 'id="themeToggle"' "$index"
check T-071 "pre-paint theme script"       grep -q 'pickles-theme' "$index"
check T-072 "dark mode tokens defined"     grep -q 'prefers-color-scheme: dark' "$site/styles.css"
check T-073 "reduced motion respected"     grep -q 'prefers-reduced-motion' "$site/styles.css"
check T-074 "landmarks and skip target" bash -c '
  grep -q "<main id=\"main\">" "'"$index"'" &&
  grep -q "href=\"#main\"" "'"$index"'"
'
# Without JS the reveal animation must not hide content: the opacity rule is
# scoped to .js, which only the inline head script adds.
check T-075 "reveal degrades without JS" bash -c '
  grep -q "^\.js \.reveal {" "'"$site"'/styles.css" &&
  grep -q "classList.add(\"js\")" "'"$index"'"
'
# Contrast regression guard. The vivid --orange is 4.05:1 on the tinted band,
# under the AA floor for 14px bold overlines, so small orange text must use
# the darker --orange-text. Measured contrast lives in the browser suite; this
# is the cheap structural proxy that runs on a bare CI runner.
check T-076 "small orange text uses the AA-safe token" bash -c '
  grep -q -- "--orange-text:" "'"$site"'/styles.css" &&
  grep -A 8 "^\.overline {" "'"$site"'/styles.css" | grep -q "color: var(--orange-text)"
'

# The badge on the first card sits on --sun, which is a bright yellow in BOTH
# themes, so it needs an explicit dark colour. Without one it inherits
# .card__num's var(--ink), which flips to cream in dark mode and measures
# 1.25:1 — shipped in 0.1.0 and caught by tests/test_layout.sh L-020-2. That
# suite skips on CI runners, so this is the guard that runs everywhere.
check T-077 "sun-filled badge sets an explicit dark colour" bash -c '
  grep -q -- "--on-sun:" "'"$site"'/styles.css" &&
  grep -q "\.card--orange \.card__num {[^}]*color: var(--on-sun)" "'"$site"'/styles.css"
'

# The doodle field and burst polygons are machine-generated into styles.css
# between markers. --check re-derives them and compares, so a hand-edit of
# that region fails here instead of drifting silently from its source.
if [ -z "$PY" ]; then
  echo "  SKIP  T-078  generated CSS freshness (no python available)"
else
check T-078 "generated CSS block matches its generator"   "$PY" "$root/tools/make_pattern.py" --check
fi
check T-079 "pattern generator is committed"  test -f "$root/tools/make_pattern.py"

# The title card's shape must come from a clipped background on an ANCESTOR of
# the heading, not an SVG sibling behind it. With a sibling the text is
# technically on the page colour — it measured 1.00:1 — and would be invisible
# if the shape failed to paint. tests/test_layout.sh measures the real ratio;
# this is the structural guard that runs where no browser does.
check T-080 "title card paints a real background behind its text" bash -c '
  grep -A 6 "^\.titlecard {" "'"$site"'/styles.css" | grep -q "background: var(" &&
  grep -A 6 "^\.titlecard {" "'"$site"'/styles.css" | grep -q "clip-path: var(--burst" &&
  grep -A 6 "^\.titlecard__fill {" "'"$site"'/styles.css" | grep -q "background: var(" &&
  ! grep -q "titlecard__burst" "'"$index"'"
'

# --- T-081 .. T-083: publishing configuration ---------------------------
check T-081 "CNAME names the apex domain" bash -c '
  [ "$(tr -d "[:space:]" < "'"$site"'/CNAME")" = "picklestoys.com" ]
'
check T-082 "sitemap points at the live domain" bash -c '
  grep -q "https://picklestoys.com/" "'"$site"'/sitemap.xml"
'
check T-083 "robots allows indexing"       grep -q 'Allow: /' "$site/robots.txt"

# --- T-090 .. T-091: weight budget --------------------------------------
# There are no images yet, so the whole page is the three core files. Keeping
# the cap tight now means a future photo drop has to be a deliberate decision.
check T-090 "core files under 100KB" bash -c '
  total=$(cat "'"$index"'" "'"$site"'/styles.css" "'"$site"'/app.js" | wc -c);
  [ "$total" -lt 102400 ] || { echo "core=$total bytes"; exit 1; }
'
check T-091 "no committed binaries over 400KB" bash -c '
  find "'"$site"'" -type f -size +400k | grep . && exit 1 || exit 0
'

# --- T-092 .. T-096: favicon -------------------------------------------
check T-092 "favicon files exist" bash -c '
  test -f "'"$site"'/favicon.svg" &&
  test -f "'"$site"'/favicon.ico" &&
  test -f "'"$site"'/apple-touch-icon.png"
'
check T-093 "index links all three icons" bash -c '
  grep -q "rel=\"icon\" href=\"favicon.ico\"" "'"$index"'" &&
  grep -q "rel=\"icon\" href=\"favicon.svg\"" "'"$index"'" &&
  grep -q "rel=\"apple-touch-icon\" href=\"apple-touch-icon.png\"" "'"$index"'"
'
# A 404 is served for an arbitrary request path, so its asset hrefs must be
# root-absolute or they resolve against whatever the visitor mistyped.
check T-094 "404 icon links are root-absolute" bash -c '
  grep -q "rel=\"icon\" href=\"/favicon.ico\"" "'"$site"'/404.html" &&
  grep -q "rel=\"icon\" href=\"/favicon.svg\"" "'"$site"'/404.html"
'
if [ -z "$PY" ]; then
  echo "  SKIP  T-095  raster validation (no python available)"
else
check T-095 "rasters are real, well-formed images" bash -c '
  "'"$PY"'" - "'"$site"'" <<'"'"'EOF'"'"'
import struct, sys
from pathlib import Path
site = Path(sys.argv[1])
png = (site / "apple-touch-icon.png").read_bytes()
assert png[:8] == b"\x89PNG\r\n\x1a\n", "apple-touch-icon is not a PNG"
w, h = struct.unpack(">II", png[16:24])
assert (w, h) == (180, 180), f"apple-touch-icon is {w}x{h}, expected 180x180"
ico = (site / "favicon.ico").read_bytes()
reserved, kind, count = struct.unpack("<HHH", ico[:6])
assert (reserved, kind) == (0, 1) and count >= 1, "favicon.ico header is malformed"
bw, bh, _, _, _, _, size, off = struct.unpack("<BBBBHHII", ico[6:22])
assert (bw or 256, bh or 256) == (32, 32), f"favicon.ico is {bw}x{bh}, expected 32x32"
assert off + size == len(ico), "favicon.ico length does not match its directory entry"
EOF
'
fi
# The rasters are generated, not drawn by hand. Losing the generator would
# make the icons unreproducible on a machine with no image toolchain, which
# is every machine here — the repo is deliberately dependency-free.
check T-096 "favicon generator is committed"  test -f "$root/tools/make_favicon.py"

# --- T-097 .. T-100: social sharing card --------------------------------
check T-097 "og-image source and raster exist" bash -c '
  test -f "'"$site"'/og-image.svg" && test -f "'"$site"'/og-image.png"
'
# og:image is spec-required to be an absolute URL, and must agree with the
# canonical host or the unfurl attributes to the wrong site.
check T-098 "og:image is absolute and on the canonical host" bash -c '
  grep -q "property=\"og:image\" content=\"https://picklestoys.com/og-image.png\"" "'"$index"'" &&
  grep -q "name=\"twitter:image\" content=\"https://picklestoys.com/og-image.png\"" "'"$index"'"
'
# Declared dimensions must match the file, or previews letterbox and crop
# wrongly on the platforms that trust the tags over the bytes.
check T-099 "declared og dimensions match the PNG" bash -c '
  grep -q "og:image:width\" content=\"1200\"" "'"$index"'" &&
  grep -q "og:image:height\" content=\"630\"" "'"$index"'" &&
  grep -q "twitter:card\" content=\"summary_large_image\"" "'"$index"'"
'
if [ -z "$PY" ]; then
  echo "  SKIP  T-100  og-image raster validation (no python available)"
else
check T-100 "og-image.png is 1200x630 and within platform limits" bash -c '
  "'"$PY"'" - "'"$site"'" <<'"'"'EOF'"'"'
import struct, sys
from pathlib import Path
png = (Path(sys.argv[1]) / "og-image.png").read_bytes()
assert png[:8] == b"\x89PNG\r\n\x1a\n", "og-image.png is not a PNG"
w, h = struct.unpack(">II", png[16:24])
assert (w, h) == (1200, 630), f"og-image.png is {w}x{h}, expected 1200x630"
# WhatsApp is the tightest mainstream consumer at ~300KB; stay well under.
assert len(png) < 300_000, f"og-image.png is {len(png)} bytes, over the 300KB budget"
EOF
'
fi
check T-101 "og-image generator is committed"  test -f "$root/tools/make_og_image.py"

# --- T-102 .. T-104: the torn-card layering -----------------------------
# clip-path clips absolutely positioned descendants too. While the number
# badge was a child of the clipped panel it was sliced in half by the card's
# own torn edge and rendered as a pennant. The badge must stay a sibling of
# the clipped layer, not a descendant of it.
check T-102 "card badge sits outside the clipped panel" "$PY" - "$index" <<'EOF'
import re, sys
html = open(sys.argv[1], encoding="utf-8").read()
for card in re.findall(r'<li class="card [^"]*">(.*?)</li>', html, re.S):
    panel = re.search(r'<div class="card__panel">(.*?)</div>\s*</div>', card, re.S)
    assert panel, "card has no card__panel wrapper"
    assert "card__num" not in panel.group(1),         "card__num is inside card__panel; clip-path will slice it"
    assert "card__num" in card, "card lost its badge"
EOF
# The fill colour must be a real background on an ANCESTOR of the copy, not a
# pseudo-element behind it, or the contrast pass measures the text against the
# rim colour instead. Same lesson as T-080.
check T-103 "card copy sits on a real background layer" bash -c '
  grep -q "\.card__fill {" "'"$site"'/styles.css" &&
  grep -A 4 "^\.card__fill {" "'"$site"'/styles.css" | grep -q "background: var(--surface)" &&
  [ "$(grep -c "class=\"card__fill\"" "'"$index"'")" = 3 ]
'
check T-104 "swatch chips and card panels use generated shapes" bash -c '
  grep -q -- "--burst-badge:" "'"$site"'/styles.css" &&
  grep -q -- "--panel-1:" "'"$site"'/styles.css" &&
  grep -q "clip-path: var(--burst-badge)" "'"$site"'/styles.css" &&
  grep -q "clip-path: var(--panel-1)" "'"$site"'/styles.css"
'

echo
echo "HTML + accessibility validation"
echo "==============================="
if [ -n "$PY" ]; then
  # Self-test first: a validator that cannot fail proves nothing.
  "$PY" "$root/tests/validate_html.py" --selftest || fail=$((fail + 1))
  "$PY" "$root/tests/validate_html.py" || fail=$((fail + 1))
else
  echo "  SKIP  python not available"
fi

echo "---------------------"
echo "Passed: $pass  Failed: $fail"
[ "$fail" -eq 0 ] || exit 1

# Browser-based suites. Each SKIPs cleanly where its tooling is absent (CI
# runners have no browser), so the structural checks above remain the gate
# that protects production. Locally they measure what grep cannot see.
for suite in test_layout; do
  if [ -f "$root/tests/$suite.sh" ]; then
    echo
    bash "$root/tests/$suite.sh"
  fi
done
