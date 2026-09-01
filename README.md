# PicklesToys

<!-- CONSTITUTION_START -->
[![Eric's Engineering Constitution](https://img.shields.io/badge/Eric's%20Engineering%20Constitution-Adopted-blue)](https://github.com/esanacore/engineering-constitution)
<!-- CONSTITUTION_END -->

Current version: **0.1.0** · Domain: **picklestoys.com** (registered, not yet
pointed at this site — see `docs/DOMAIN_SETUP.md`)

The website for **PicklesToys** — a handmade, small-batch toy workshop in the
making. The business has not launched: there are no products, no prices, and
nothing for sale. This site is an honest placeholder that says exactly that,
built so the real thing can grow into it.

The site is dependency-free static HTML/CSS/JS, published straight from this
repository: **every push to `main` deploys automatically to GitHub Pages.**

## Getting Started

No build step, no packages. Clone with the constitution submodule:

```bash
git clone --recurse-submodules https://github.com/esanacore/PicklesToys.git
```

## Run

Open `site/index.html` in a browser, or serve the directory:

```bash
python -m http.server 8123 --directory site
```

## Test

```bash
bash tests/test_site.sh
```

47 structural checks (`T-xxx`) plus a dependency-free HTML/accessibility
validator (`V-xxx`) that runs on the standard library alone, so it works on a
bare CI runner. The suite gates every deploy — if it fails, the previous
deployment stays up.

The checks are not only "does the markup parse." Several encode decisions that
would otherwise quietly rot:

| Group | What it protects |
| --- | --- |
| `T-030`–`T-034` | The page keeps saying it is **not open yet**. No invented prices, no cart or checkout copy. |
| `T-040`–`T-042` | No third-party franchise, studio, or character names anywhere in the HTML — comments included — and the non-affiliation line stays in the footer. See `docs/BRAND.md`. |
| `T-050`–`T-053` | Placeholders stay visibly marked. No invented email, no fake social handles, no lorem ipsum. |
| `T-060`–`T-063` | `site/` stays dependency-free: no CDN, no external font, no package.json. |
| `T-070`–`T-076` | Theme toggle, reduced-motion support, no-JS degradation, and the AA-safe color token for small orange text. |
| `T-080`–`T-091` | Publishing config (CNAME, sitemap, robots) and the page-weight budget. |

## Project Structure

```text
PicklesToys/
├── site/                  ← The website (what GitHub Pages publishes)
│   ├── index.html         ← Single-page placeholder
│   ├── 404.html           ← Themed not-found page
│   ├── styles.css         ← Design system (color tokens, layout)
│   ├── app.js             ← Theme toggle, scroll reveal, scrollspy
│   ├── CNAME              ← Custom domain, kept in version control
│   ├── robots.txt
│   └── sitemap.xml
├── tests/
│   ├── test_site.sh       ← Structural suite (T-xxx) — the CI gate
│   └── validate_html.py   ← HTML + a11y validator (V-xxx), stdlib only
├── docs/                  ← Governance and project documentation
│   ├── BRAND.md           ← Design language and the IP boundary
│   ├── DOMAIN_SETUP.md    ← Pointing picklestoys.com at GitHub Pages
│   └── ...
├── constitution/          ← Submodule: Eric's Engineering Constitution
└── .github/workflows/     ← Deploy + eight constitution CI gates
```

## Deploying

Push to `main`. That is the whole process.

`.github/workflows/deploy-pages.yml` runs `tests/test_site.sh`, then publishes
`site/` to GitHub Pages. Nothing else needs to be run by hand.

## Status

Early. The domain is registered and this placeholder is what lives at it. What
is deliberately **not** here yet, because it is the owner's to provide:

- A contact email (marked `CONTACT-EMAIL-TBD` in `site/index.html`)
- Product photos, names, prices, or a shop
- Social links
- Any launch date

`TODO.md` tracks what comes next.
