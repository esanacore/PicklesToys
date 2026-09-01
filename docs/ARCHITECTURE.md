# Architecture

## Shape

A static website. Three files in `site/` are the entire application:

```text
Reader ──HTTPS──> GitHub Pages CDN ──serves──> site/
                                                ├── index.html   structure + content
                                                ├── styles.css   design system
                                                └── app.js       progressive enhancement
```

There is no server, no database, no build step, no package manager, and no
runtime dependency. What is committed is byte-for-byte what is served.

## Why this shape

The business has not launched. The site's job right now is to exist, be
honest, and cost nothing to run. Every capability not needed for that is a
liability: a build step that can break, a dependency that can be abandoned, a
server that can be billed for or breached.

The comparison worth making is with `gentle-table`, which is Next.js on Vercel
with Neon Postgres — because it genuinely needs to accept orders and persist
them. PicklesToys needs none of that yet. Choosing the same stack "so it is
ready later" would buy an operational burden years before the feature it
supports.

`702_with_the_view` is the closer sibling and the model this repo follows: a
static listing page on GitHub Pages, tested by a bash suite, deployed on push.

## Publishing

```text
git push origin main
        │
        ▼
.github/workflows/deploy-pages.yml
        │
        ├── bash tests/test_site.sh      ← gate: a failure stops here
        │
        ├── actions/upload-pages-artifact (path: site)
        │
        └── actions/deploy-pages          → live at picklestoys.com
```

The test suite runs **before** the deploy step. A push that breaks the site
fails the workflow and the previous deployment stays live — the site cannot be
taken down by a bad commit, only by a deliberate one that passes the tests.

## Client-side behavior

`app.js` is progressive enhancement only. With JavaScript disabled the page is
fully readable; this is enforced by `T-075`, which requires that the reveal
animation's `opacity: 0` rule be scoped to a `.js` class that only the inline
head script adds.

Four behaviors, in order:

1. **Theme.** Follows `prefers-color-scheme` until the reader clicks the
   toggle, then persists the choice in `localStorage` under `pickles-theme`.
   The apply-saved-theme half runs inline in `<head>` before first paint, so
   the page never flashes the wrong mode; the toggle wiring runs from `app.js`.
   Same approach as `702withtheview.com` and `gentletable.com`.
2. **Scroll reveal.** `IntersectionObserver` adds `.is-visible`. Skipped
   entirely under `prefers-reduced-motion` or where the observer is missing —
   in both cases everything is shown immediately rather than never.
3. **Scrollspy.** Marks the nav link for the section in view, setting
   `aria-current` as well as a visual underline.
4. **Footer year.** Set from `Date`, so the copyright line cannot go stale.

## Design system

Color lives entirely in CSS custom properties defined in three blocks at the
top of `styles.css`: light (`:root`), system-dark
(`@media (prefers-color-scheme: dark)` guarded by `:root:not([data-theme="light"])`),
and explicit dark (`:root[data-theme="dark"]`). The third block is what makes
the toggle win over the OS in both directions.

Dark mode redefines each accent rather than reusing the light value, because
the light accents are tuned for contrast against cream paper and go muddy on
near-black. `--orange-text` is deliberately separate from `--orange`: the
vivid brand orange is 4.05:1 on the tinted band, under the AA floor for the
14px bold overlines, so fills and small text need different values. See
`docs/BRAND.md`.

## Constraints that shape future changes

- **`site/` stays dependency-free.** No CDN, no external font, no
  `package.json`. Enforced by `T-060`–`T-063`. This is the constraint most
  likely to be challenged — an embedded checkout, an analytics snippet, and a
  webfont all violate it.
- **Selling requires a different architecture.** GitHub Pages cannot process
  payments. Adding commerce means either an embedded third-party checkout
  (breaking the rule above) or moving to the `gentle-table` shape. That is an
  ADR-worthy decision, not an incremental edit.
- **The domain is in version control.** `site/CNAME` holds `picklestoys.com`
  so it survives a rebuild and is visible in source rather than only in a
  settings page. `T-080` fails if it drifts.
