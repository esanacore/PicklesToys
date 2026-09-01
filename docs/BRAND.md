# Brand and Influence Boundary

This document exists to keep one decision from drifting: **PicklesToys draws
on the *era* of early-90s kids-television art direction, and never on any
specific show, character, or company's marks.**

It is enforced, not just written down. `tests/test_site.sh` T-040 fails the
build if a third-party franchise or character name appears anywhere in the
published HTML — comments included — and T-041 requires the non-affiliation
line in the footer.

## Why the line is where it is

The original prompt for this project was "toys inspired by Rugrats." That
phrase covers two very different things, and only one of them is safe to
build a business on:

| | Status |
| --- | --- |
| The visual **language** of that era — lumpy silhouettes, uneven line weights, clashing saturated colors, halftone dots, paper grain, a deliberately un-tidy look | **Fine.** A style is not protectable. Many studios worked in it. |
| Specific **characters**, their names, their designs, their catchphrases, logos, and show titles | **Not fine.** These are trademarks and copyrighted works owned by Paramount/Nickelodeon. Making and selling toys that use them is infringement, regardless of scale, and "small batch" or "handmade" is not a defense. |

Fan art sold at small volume is still infringement — it is simply infringement
that often goes unpursued. That is a risk position, not a legal permission, and
it is a bad foundation for a brand with a domain and a real storefront. A
cease-and-desist would land on the whole business, not just one product.

None of this is legal advice. If PicklesToys ever wants to go near licensed
territory, that is a conversation with an IP attorney, not a judgment call to
make in a commit.

## What this means in practice

**Do:**

- Design original characters and original toy forms.
- Use the era's palette, textures, geometry, and attitude.
- Describe the influence in general terms: "early-90s cartoon art direction,"
  "Saturday-morning-cartoon spirit," "the era when kids' TV stopped looking
  tidy."

**Do not:**

- Name a show, studio, network, or character — in copy, alt text, file names,
  product names, commit messages, or HTML comments.
- Recreate a recognizable character's silhouette, color scheme, or signature
  feature, even "stylized" or "our version of."
- Use a typeface that is a known franchise's custom logo lettering.
- Lean on search terms that trade on someone else's audience (page titles,
  meta descriptions, alt text, social tags).

## The palette

Named so the colors have their own identity rather than borrowing one. Defined
as CSS custom properties at the top of `site/styles.css`.

| Token | Name | Light | Dark |
| --- | --- | --- | --- |
| `--orange` | Brine Orange | `#c8431b` | `#ff8a5c` |
| `--teal` | Jar Teal | `#0e6f6b` | `#4fd1ca` |
| `--grape` | Grape Soda | `#66399b` | `#c39bf5` |
| `--sun` | Lunchbox Yellow | `#f5c518` | `#ffd84d` |
| `--lime` | Dill Green | `#4e7615` | `#a6d65e` |
| `--on-sun` | ink for sun fills | `#1e1a17` | `#1e1a17` (same) |

Light-mode accents are tuned for contrast against the cream paper background
(`--paper`) and go muddy on near-black, which is why dark mode lifts each one
rather than reusing the same hex. Accents used as text clear 4.5:1 against
their own background. `--sun` is decorative only — it is a fill behind dark
ink, never text.

**`--on-sun` is the one token that does not change between themes**, and the
reason is worth understanding before touching it. `--teal` and `--grape` invert
with the theme — dark in light mode, light in dark mode — so text on them uses
`--on-accent`, which inverts too. `--sun` does *not* invert: it is a bright
yellow in both. Text on it must therefore be dark in both, which no inverting
token can deliver.

Getting this wrong is not hypothetical. The numbered badge on the first card
set a `--sun` background and no colour, inheriting `var(--ink)`, which flips to
cream in dark mode. Cream on bright yellow is **1.25:1**. It shipped in 0.1.0
and survived three releases and a careful hand-audit before
`tests/test_layout.sh` measured it. `T-077` now guards it structurally.

## The mark

A pickle jar. It appears twice, drawn differently for each job:

- **Header** (`site/index.html`, inline SVG): lid, glass body, two pickles,
  1.6–2px ink strokes. Sits at ~30px, where that detail reads.
- **Favicon** (`site/favicon.svg`): a redraw, not an export. Three flat shapes
  on a filled Brine Orange badge, no strokes at all. The header version turns
  to mush at 16px, which is the size that actually decides whether anyone
  recognises the tab.

The badge is filled rather than transparent so the mark holds contrast against
both light and dark browser chrome.

`favicon.ico` (32x32) and `apple-touch-icon.png` (180x180) are generated from
the SVG's geometry by `tools/make_favicon.py`, which uses the standard library
alone — there is no image toolchain in this repo and adding one would break
`NFR-001`. **Edit the SVG, then re-run the script**; do not hand-edit the
rasters, they will be overwritten.

Note the jar is a generic object, deliberately. It is a visual pun on the name
and owes nothing to anyone else's character design — which is the whole point
of the boundary above.

## The social card

`site/og-image.svg` is the 1200x630 card a link unfurls into — the size
Facebook, LinkedIn, Slack, iMessage, and X all crop from. It reuses the page's
own vocabulary: cream paper, halftone, the jar badge, the two-line headline
with a hand-drawn highlight under the phrase that carries the meaning, and the
status pill. It says the business is not open, for the same reason the page
does.

`site/og-image.png` is rendered from it by `tools/make_og_image.py`. **Edit
the SVG, then re-run the script** — the PNG exists only because og:image is
not accepted as SVG by most platforms.

Two layout rules worth keeping if the card is redesigned: keep everything
inside a 72px margin, since several platforms crop to 1.91:1 and some chat
clients round the corners; and check text metrics rather than estimating them.
The first draft here had a status pill narrower than its own label, which is
invisible in source and obvious the moment it renders.

## Typography

System fonts only. The constitution forbids external dependencies
(Principle 7) and `tests/test_site.sh` T-063 enforces no `@font-face` and no
Google Fonts. If a display face is ever wanted for the wordmark, the way to do
it without breaking that rule is to draw the wordmark as inline SVG paths —
which also sidesteps the trademark question, since custom lettering cannot be
mistaken for someone else's logo font.
