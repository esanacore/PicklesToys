# Troubleshooting

## The deploy workflow fails at "Configure GitHub Pages"

Pages has not been enabled for the repository. Go to **Settings → Pages →
Build and deployment → Source** and select **GitHub Actions**. This is a
one-time setting; the workflow cannot create it.

## The deploy workflow fails at "Run site tests before publishing"

Working as designed — the gate caught something. Run the same command locally
to see which check failed:

```bash
bash tests/test_site.sh
```

The previous deployment is still live. Nothing is broken in production.

## `T-040` fails and I did not add any franchise name

Check HTML comments. `T-040` greps the whole file, comments included, on
purpose — a name in a comment is still shipped to every visitor in the page
source. This check has already caught exactly that once, during the initial
build. See `docs/BRAND.md` for why the rule exists.

## `T-060` fails after adding a link

`T-060` allows absolute URLs to `picklestoys.com` (canonical, `og:url`) but
rejects any `src`/`href` pointing at another origin, because that would make
the page depend on a third party at load time. A link a reader clicks is fine;
a resource the browser fetches is not.

If you need to link out to something, it belongs in prose as an ordinary
anchor — which does not match the pattern, since the check looks at whether
the page *loads* from elsewhere.

## The page flashes white before going dark

The inline `<head>` script that applies the saved theme was moved, removed, or
placed after the stylesheet link. It must run before first paint. `T-071`
checks the script exists but cannot check its position — verify by hard-
reloading with dark mode active.

## Content is invisible with JavaScript disabled

The reveal animation's `opacity: 0` rule escaped its `.js` scope. The rule
must be `.js .reveal`, never bare `.reveal`, and the `js` class is added by the
inline head script. `T-075` guards both halves.

## Contrast looks wrong after a palette change

Small orange text must use `--orange-text`, not `--orange`. The vivid brand
orange measures 4.05:1 on the tinted band — under the AA floor for the 14px
bold overlines. `T-076` guards the wiring but not the token *values*, so if
you change a hex, re-measure. The recorded values are in `docs/BRAND.md`.

## `constitution/` is empty and every governance check fails

The submodule was not initialized:

```bash
git submodule update --init --recursive
```

## The `constitution-version` workflow fails

The pinned submodule is behind the latest tagged release:

```bash
git submodule update --remote constitution
git add constitution && git commit -m "Update constitution to <version>"
```

## picklestoys.com does not resolve, or shows a certificate error

Work through `docs/DOMAIN_SETUP.md` in order. The most common cause by far, if
the DNS is on Cloudflare, is a **proxied (orange-cloud) record**. GitHub Pages
must receive the traffic directly to provision its certificate; proxying
produces certificate failures and redirect loops. Set every Pages record to
DNS-only.

Second most common: fewer than all four A records. GitHub publishes four
anycast addresses and expects all of them, not one.

## The live site is stale after a successful deploy

Check that the deploy actually targeted the custom domain and not just the
`github.io` URL, and that `site/CNAME` still contains `picklestoys.com` — a
missing or changed CNAME file in the published artifact will unset the custom
domain. `T-080` catches this before it ships.
