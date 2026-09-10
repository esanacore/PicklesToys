# TODO

Tracked work for PicklesToys. Items are grouped by what unblocks them.

## Blocked on the owner (real-world facts nobody else can supply)

- [ ] **Contact email.** Replace `CONTACT-EMAIL-TBD` in `site/index.html` with
      a real `mailto:` link. `T-050` accepts either the marked placeholder or a
      real address, so the site stays honest until this lands.
- [x] **DNS host identified: GoDaddy** (2026-09-10, from the live
      nameservers `ns37/ns38.domaincontrol.com`). `docs/DOMAIN_SETUP.md` now
      carries GoDaddy-specific steps. Still worth recording the **expiry
      date** there, and confirming the registrar is GoDaddy too — the
      nameservers only prove where DNS is hosted.
- [ ] **Decide the actual product line.** The site describes an intent
      (handmade, small batch, built to be played with) but names no products,
      because none exist yet.

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

## Business questions worth answering before building more

- [ ] What is actually being made first — plush, wood, resin, something else?
      Materials change photography, shipping, safety labelling, and price.
- [ ] **Toy safety.** Anything sold as a children's toy in the US falls under
      CPSIA: third-party testing, tracking labels, and a Children's Product
      Certificate. If the intended buyer is adult collectors, the rules differ
      substantially. This decision shapes the product, not just the paperwork.
- [ ] Where does selling happen — this site, or an existing marketplace? A
      static GitHub Pages site cannot take payments; that would mean either an
      embedded third-party checkout (breaking the dependency-free rule) or a
      move to the Next.js/Vercel shape `gentle-table` uses.
