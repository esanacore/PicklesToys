# Operations

## Runtime footprint

None. The site is static files served by GitHub Pages. There is no server to
patch, no database to back up, no process to restart, and no bill to pay.

This is worth stating explicitly because it is the main operational property
worth protecting. Most proposed additions to this site — analytics, a checkout,
a contact form backend, a CMS — would replace "nothing to operate" with
something to operate. That trade may be worth making later; it should be made
deliberately.

## Deploying

Push to `main`. `.github/workflows/deploy-pages.yml` runs the test suite, then
publishes `site/` to GitHub Pages.

To redeploy without a code change, trigger the workflow manually from the
Actions tab or with `gh workflow run deploy-pages.yml`.

## Rollback

Revert the commit and push:

```bash
git revert <sha>
git push origin main
```

The workflow republishes the previous content. There is no separate rollback
mechanism and none is needed — the deployed artifact is exactly the contents
of `site/` at that commit.

Note that a failing test suite is itself a rollback safety net: a bad push that
fails the gate never reaches the CDN, and the prior deployment stays live.

## Monitoring

There is no uptime monitoring, error tracking, or analytics, by choice. For a
placeholder page with no users and no transactions, the instrumentation would
outweigh what it observes.

When the site starts mattering commercially, the first thing worth adding is an
external uptime check on `https://picklestoys.com` — not analytics. Knowing the
site is down is operationally useful; knowing how many people visited is a
business question that can wait.

Any analytics added later must not break `NFR-001` (no external resources).
That rules out the usual hosted snippets and points toward either server-side
log analysis, which GitHub Pages does not expose, or accepting the dependency
deliberately with an ADR recording the trade.

## Secrets

There are none. The site has no API keys, no tokens, and no environment
variables — see `docs/ENV_VARS.md`. The `constitution-secrets` workflow scans
every push, and `.gitignore` blocks the common credential file shapes even
though none should ever exist here.

If a secret is ever needed, that is a signal the architecture has changed
(see `docs/ARCHITECTURE.md`), not a routine configuration step.

## Domain and certificate

`picklestoys.com` is registered and renewed by the owner. TLS is provisioned
and renewed automatically by GitHub Pages via Let's Encrypt once the custom
domain is verified — there is no certificate to rotate by hand.

The failure mode to watch for is the domain lapsing, which no amount of
repository hygiene protects against. Registrar, DNS host, and expiry date are
recorded in `docs/DOMAIN_SETUP.md` and currently marked TBD; filling them in
is tracked in `TODO.md`.

## Routine maintenance

| Cadence | Task |
| --- | --- |
| On every change | Run `bash tests/test_site.sh` before pushing |
| When CI flags it | Update the `constitution` submodule to the latest release |
| Weekly, automatic | Dependabot checks GitHub Actions versions (`.github/dependabot.yml`) |
| Per release | Re-review `docs/OTS_SOFTWARE.md` and the coverage log in `docs/TEST_PLAN.md` |
| Annually | Confirm the domain renewal actually processed |
