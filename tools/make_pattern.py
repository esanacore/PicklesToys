#!/usr/bin/env python3
"""Generate the doodle-field and burst-shape tokens in site/styles.css.

The page background is a dense scatter of hand-drawn marks — squiggles,
chevrons, rings, crosses, dots — in the manner of early-90s kids-TV title
cards, where the card sat on a busy patterned field rather than flat colour.

Why generated rather than hand-written: the field is three layers of scattered
SVG, each with its own seed, and the whole thing is ~25KB of data URI. Nobody
should be editing that by hand, and nobody should have to trust that it is
still what the parameters below describe. Run:

    python tools/make_pattern.py            # rewrite the generated block
    python tools/make_pattern.py --check    # verify the block is current

`--check` is wired into the test suite, so a hand-edit of the generated region
fails the build instead of silently drifting from its source.

Three implementation notes worth keeping:

* Marks are emitted once, plus an extra copy only when they fall within one
  mark-radius of a tile edge, so a mark crossing the boundary reappears on the
  opposite side and the tile is seamless. Emitting all nine 3x3 offsets
  unconditionally also works, and costs ~7x the bytes for identical output.
* The three layers use coprime tile sizes (180 / 127 / 151). A single tile
  repeats visibly at any realistic viewport width; layers whose sizes share no
  factor only realign after their least common multiple, which is far past the
  size of any screen.
* Each theme's field is emitted exactly once into its own custom property,
  and the dark-mode selectors reference it. Setting --doodle-field directly in
  each selector is the obvious shape and writes the dark layers twice, because
  a media-query rule and a bare [data-theme] rule cannot share a block.
"""
from __future__ import annotations

import argparse
import math
import re
import sys
from pathlib import Path
from urllib.parse import quote

STYLES = Path(__file__).resolve().parent.parent / "site" / "styles.css"

BEGIN = "/* BEGIN GENERATED doodle field — tools/make_pattern.py, do not edit by hand */"
END = "/* END GENERATED doodle field */"

# seed, tile size, mark count, stroke width
LAYERS = [
    (7, 180, 24, 1.7),
    (31, 127, 16, 1.7),
    (53, 151, 12, 1.7),
]

# Per theme: the ink for each layer, and that layer's opacity. Dark mode is
# not the light inks inverted — it is the theme's own accent values, at lower
# opacity, because light marks on near-black read louder than dark marks on
# cream at the same alpha.
THEMES = {
    "light": [("#1e1a17", 0.15), ("#66399b", 0.22), ("#0e6f6b", 0.20)],
    "dark": [("#fbf3e4", 0.10), ("#c39bf5", 0.16), ("#4fd1ca", 0.14)],
}


def rng(seed: int):
    """The same linear congruential generator the design lab used.

    Values stay below 2^53 (seed < 2^32, times 1664525), so this produces
    bit-identical output in Python and in JavaScript — which is what let the
    shapes be tuned in a browser and then frozen here.
    """
    state = seed

    def nxt() -> float:
        nonlocal state
        state = (state * 1664525 + 1013904223) % 4294967296
        return state / 4294967296

    return nxt


def mark(kind: int) -> str:
    """One doodle, centred on the origin."""
    return [
        '<path d="M-9 0c3-5 6 5 9 0s6-5 9 0" fill="none"/>',    # squiggle
        '<path d="M-5 -6l5 6-5 6" fill="none"/>',                # chevron
        '<circle cx="0" cy="0" r="4.5" fill="none"/>',           # ring
        '<path d="M0 -5v10M-5 0h10" fill="none"/>',              # cross
        '<circle cx="0" cy="0" r="2.2" stroke="none"/>',         # dot
        '<path d="M-6 4c4-9 8 5 12-4" fill="none"/>',            # wave
        '<path d="M-5 -5l10 10M5 -5l-10 10" fill="none"/>',      # saltire
        '<path d="M-7 -3q7 -6 14 0q-7 6 -14 0z" fill="none"/>',  # lens
    ][kind]


def tile(seed: int, size: int, count: int, ink: str, width: float, opacity: float) -> str:
    r = rng(seed)
    body: list[str] = []
    for _ in range(count):
        x, y = r() * size, r() * size
        rot = r() * 360
        scale = 0.75 + r() * 0.75
        kind = math.floor(r() * 8)
        glyph = mark(kind)

        reach = 11 * scale                      # widest mark half-extent
        xs = [0.0]
        ys = [0.0]
        if x < reach:
            xs.append(float(size))
        elif x > size - reach:
            xs.append(-float(size))
        if y < reach:
            ys.append(float(size))
        elif y > size - reach:
            ys.append(-float(size))

        for dx in xs:
            for dy in ys:
                body.append(
                    f'<g transform="translate({x + dx:.1f},{y + dy:.1f}) '
                    f'rotate({rot:.0f}) scale({scale:.2f})">{glyph}</g>'
                )

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 {size} {size}">'
        f'<g stroke="{ink}" stroke-width="{width}" stroke-linecap="round" '
        f'fill="{ink}" opacity="{opacity}">{"".join(body)}</g></svg>'
    )


def data_uri(svg: str) -> str:
    # Single-quoted: the value lands inside a double-quoted context often
    # enough that the opposite choice bites. safe="" so every reserved
    # character is escaped rather than trusted to survive the CSS parser.
    return "url('data:image/svg+xml," + quote(svg, safe="") + "')"


def layers_for(theme: str) -> str:
    parts = []
    for (seed, size, count, width), (ink, opacity) in zip(LAYERS, THEMES[theme]):
        parts.append(data_uri(tile(seed, size, count, ink, width, opacity)))
    return ",\n    ".join(parts)


def sizes() -> str:
    return ", ".join(f"{size}px {size}px" for _, size, _, _ in LAYERS)


BURSTS = {
    # name: (seed, points, outer radius, inner radius, jitter, width ratio)
    "hero": (7, 9, 42, 26, 0.16, 1.55),
    "tag": (21, 11, 44, 24, 0.20, 1.55),
    # Round rather than elongated, and more points: at badge size a nine-point
    # burst reads as a blob, because each spike is only a few pixels.
    "badge": (13, 12, 45, 31, 0.15, 1.0),
}

# Ragged panels for the three content cards. Unlike a burst, a card has to
# hold body copy, so the edge only wobbles — the usable interior is the whole
# box minus a couple of percent. Three seeds so the cards differ from each
# other the way their rotations already do.
PANELS = {"1": 5, "2": 23, "3": 61}


def burst_points(seed: int, points: int, outer: float, inner: float,
                 jitter: float, wide: float):
    """An irregular starburst: alternating outer/inner radii, jittered.

    Wider than tall, like a title card, and deliberately not a regular star —
    the per-point jitter is what makes it read as torn rather than geometric.
    """
    r = rng(seed)
    pts = []
    n = points * 2
    for i in range(n):
        base = outer if i % 2 == 0 else inner
        rad = base * (1 + (r() - 0.5) * jitter * 2)
        ang = (i / n) * math.pi * 2 + (r() - 0.5) * (math.pi / n) * jitter * 3
        pts.append((50 + math.cos(ang) * rad * wide, 50 + math.sin(ang) * rad))
    return pts


def ragged_rect(seed: int, per_side: int = 11, wobble: float = 1.5):
    """A rectangle whose edges wobble, like a torn paper card.

    Amplitude and frequency have to be read together. Few points with a large
    wobble gives long diagonal segments and deep pointed bites — it reads as
    damage, not as a torn edge. Many points with a small wobble reads as
    paper. The first attempt here used 7 points at 2.4%, which on a 344px card
    put a 16px excursion across 29px of travel; 11 at 1.5% is the fix.

    Each edge is nominally inset by `wobble` and then wobbles by +/-`wobble`,
    so every point stays inside the 0-100 box. That matters: these are clipped
    onto real content, and an edge that strayed outside would be cropped flat
    by the element bounds — turning a torn edge back into a straight one.
    """
    r = rng(seed)
    pts: list[tuple[float, float]] = []

    def edge(x0: float, y0: float, x1: float, y1: float,
             nx: float, ny: float) -> None:
        for i in range(per_side):
            t = i / per_side
            d = wobble + (r() - 0.5) * 2 * wobble
            pts.append((x0 + (x1 - x0) * t + nx * d,
                        y0 + (y1 - y0) * t + ny * d))

    edge(0, 0, 100, 0, 0, 1)        # top, normal points down (inward)
    edge(100, 0, 100, 100, -1, 0)   # right
    edge(100, 100, 0, 100, 0, -1)   # bottom
    edge(0, 100, 0, 0, 1, 0)        # left
    return pts


def polygon(pts) -> str:
    return "polygon(" + ", ".join(f"{x:.2f}% {y:.2f}%" for x, y in pts) + ")"


def panel_path(seed: int) -> str:
    return polygon(ragged_rect(seed))


def clip_path(name: str) -> str:
    """A CSS clip-path polygon, normalised so the shape fills its element.

    clip-path rather than an inline <svg> on purpose. The shape has to be a
    real painted background on an *ancestor* of the heading: an SVG sibling
    leaves the text technically sitting on the page colour, which measured
    1.00:1 in tests/test_layout.sh — and would genuinely be invisible if the
    SVG failed to paint. Clipping a background-color keeps the jagged edge and
    keeps the contrast real.
    """
    pts = burst_points(*BURSTS[name])
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    x0, x1 = min(xs), max(xs)
    y0, y1 = min(ys), max(ys)
    return polygon([((x - x0) / (x1 - x0) * 100, (y - y0) / (y1 - y0) * 100)
                    for x, y in pts])


def block() -> str:
    """The generated CSS region."""
    lines = [
        BEGIN,
        "",
        "/* Layer sizes are coprime so the field's visual repeat lands far past",
        "   any real viewport width. See tools/make_pattern.py. */",
        ":root {",
        "  --doodle-size: " + sizes() + ";",
        "  --doodle-light:\n    " + layers_for("light") + ";",
        "  --doodle-dark:\n    " + layers_for("dark") + ";",
        "  --doodle-field: var(--doodle-light);",
        "",
        "  /* Burst shapes for the title cards. See clip_path() for why these",
        "     are clip-paths and not inline SVG. */",
        "  --burst-hero: " + clip_path("hero") + ";",
        "  --burst-tag: " + clip_path("tag") + ";",
        "  --burst-badge: " + clip_path("badge") + ";",
        "",
        "  /* Ragged card panels: an edge that wobbles rather than a burst,",
        "     because these hold body copy. See ragged_rect(). */",
        "  --panel-1: " + panel_path(PANELS["1"]) + ";",
        "  --panel-2: " + panel_path(PANELS["2"]) + ";",
        "  --panel-3: " + panel_path(PANELS["3"]) + ";",
        "}",
        "",
        "@media (prefers-color-scheme: dark) {",
        '  :root:not([data-theme="light"]) { --doodle-field: var(--doodle-dark); }',
        "}",
        "",
        ':root[data-theme="dark"] { --doodle-field: var(--doodle-dark); }',
        "",
        END,
    ]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="exit non-zero if the committed block is not current")
    args = ap.parse_args()

    css = STYLES.read_text(encoding="utf-8")
    if BEGIN not in css or END not in css:
        print(f"markers not found in {STYLES.name}", file=sys.stderr)
        return 2

    pattern = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END), re.S)
    fresh = block()
    current = pattern.search(css).group(0)

    if args.check:
        if current == fresh:
            print(f"  doodle field is current ({len(fresh)} chars)")
            return 0
        print("  doodle field in styles.css does NOT match tools/make_pattern.py.",
              file=sys.stderr)
        print("  Re-run: python tools/make_pattern.py", file=sys.stderr)
        return 1

    STYLES.write_text(pattern.sub(lambda _: fresh, css), encoding="utf-8")
    print(f"  wrote doodle field into styles.css ({len(fresh)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
