# TODO

Tracked work for PicklesToys. Items are grouped by what unblocks them.

## Blocked on the owner (real-world facts nobody else can supply)

- [x] **Contact email.** Done 2026-09-10 — `pureheartmakerstuff@gmail.com`.
      `T-050` now asserts the real address and `T-051` guards against the
      visible text drifting from the `mailto:` target.
- [x] **DNS host identified: GoDaddy** (2026-09-10, from the live
      nameservers `ns37/ns38.domaincontrol.com`). `docs/DOMAIN_SETUP.md` now
      carries GoDaddy-specific steps. Still worth recording the **expiry
      date** there, and confirming the registrar is GoDaddy too — the
      nameservers only prove where DNS is hosted.
- [x] **Product line decided 2026-09-10: adult collector pieces**, mixed media
      with a large 3D-printed component. The site describes that intent but
      names no products, because none exist yet.

## Launch the site at the domain

- [x] Enable GitHub Pages (Source: **GitHub Actions**). Done 2026-08-31; the
      site is live at https://esanacore.github.io/PicklesToys/.
- [ ] Create the four A records and the `www` CNAME (`docs/DOMAIN_SETUP.md`).
      On Cloudflare these must be **grey-cloud / DNS-only**.
- [ ] Set the custom domain in Settings → Pages, then enable **Enforce HTTPS**
      once the certificate is issued. Required even though `site/CNAME` exists:
      with an Actions-based deploy the artifact's CNAME file does not register
      the domain on its own (confirmed — the API still reports `cname: null`).
- [ ] Verify with `dig` and `curl` per `docs/DOMAIN_SETUP.md` step 3.

## Site work

- [x] **`og:image`.** Done 2026-08-31. `site/og-image.svg` is the source;
      `og-image.png` (1200x630) is rendered from it by `tools/make_og_image.py`.
      **Note the URLs only resolve once DNS is pointed** — they are absolute and
      on picklestoys.com, as og:image requires. Re-check the unfurl then.
- [x] **Favicon.** Done 2026-08-31. `site/favicon.svg` is a redraw of the
      header jar simplified for 16px; `favicon.ico` and `apple-touch-icon.png`
      are generated from it by `tools/make_favicon.py` (stdlib only, no image
      toolchain). Re-run that script after editing the SVG.
- [x] **Browser-based layout/contrast suite.** Done 2026-08-31 —
      `tests/test_layout.sh`. Closed GAP-001 and GAP-002, and found a real
      1.25:1 contrast defect on its first run.
- [ ] **GAP-003: the browser suite skips in CI.** Contrast defects are only
      caught on a machine with a browser. Options: run it in CI with a
      Playwright-enabled job (adds a CI dependency this repo has so far avoided),
      or keep adding structural guards per defect as `T-076`/`T-077` do. Low
      risk while the page is this small; revisit if the site grows.

## Business questions

- [x] **Who it is for: adult collectors, not children** (2026-09-10). This is
      the decision that removes the CPSIA children's-product regime — no
      third-party lab testing, no Children's Product Certificate, no tracking
      labels, no ASTM F963. It is also why the page now talks about shelves
      rather than being wrecked.
- [x] **Materials: mixed, with a lot of 3D printing** (2026-09-10). Hence
      "hand-finished" rather than "handmade" — the page should not claim more
      handwork than the process involves.
- [ ] **The adult framing has to be genuine, not a label.** "Not for children"
      on something that plainly reads as a kids' toy does not hold up: design,
      marketing, and price all have to point the same way. Worth a real check
      with someone qualified before money changes hands — this is the one
      remaining regulatory question, and it is a judgement call, not a form.
- [ ] **Age marking at point of sale.** Not needed on the site while nothing is
      for sale, but the listings and packaging will need it. Decide 14+ or 18+.
- [ ] **Resin safety, if resin printing is in the mix.** Uncured photopolymer
      is a skin sensitiser; pieces must be fully cured before they go out, and
      the workspace needs ventilation. This is a maker-safety issue rather than
      a product-compliance one, but it is real.
- [ ] Where does selling happen — this site, or an existing marketplace? A
      static GitHub Pages site cannot take payments; that would mean either an
      embedded third-party checkout (breaking the dependency-free rule) or a
      move to the Next.js/Vercel shape `gentle-table` uses. Marketplaces
      (Etsy, a designer-toy shop) sidestep both and are the usual first step.
- [ ] **First actual piece.** Nothing on the site can name a product until one
      exists. That is the next real milestone.
