# Command Reference

Every command this repository needs. There is no build step, so the list is short.

## Daily

| Command | What it does |
| --- | --- |
| `python -m http.server 8123 --directory site` | Serve the site locally at `http://localhost:8123` |
| `bash tests/test_site.sh` | Run the full suite — 58 structural checks, the HTML/accessibility validator, then the browser suite |
| `git push origin main` | Publish. Tests run first; a failure leaves the previous deployment live |

## Testing

| Command | What it does |
| --- | --- |
| `bash tests/test_site.sh` | Full suite — structural checks, then the browser suite |
| `bash tests/test_layout.sh` | Browser suite alone (`L-xxx`): measured contrast and geometry |
| `python tests/validate_html.py` | Validator alone, over every `site/*.html` |
| `python tests/validate_html.py --selftest` | Prove the validator can actually fail |
| `GSTACK_BROWSE=/nonexistent bash tests/test_layout.sh` | Prove the suite still skips cleanly where no browser exists |

The browser suite needs the gstack browse daemon. Without it the suite prints
SKIP and exits 0 — which means **a green `test_site.sh` does not by itself mean
contrast was checked**. After any colour or layout change, confirm the `L-xxx`
checks actually ran rather than skipped.

## Governance

These ship in the `constitution/` submodule and run in CI. Running them locally
before pushing avoids a red build.

| Command | What it checks |
| --- | --- |
| `bash constitution/scripts/check_compliance.sh .` | Required governance files are present |
| `bash constitution/scripts/check_traceability.sh docs/PRODUCT_REQUIREMENTS.md docs/REQUIREMENTS_TRACEABILITY.md` | Every requirement has a verifying test |
| `bash constitution/scripts/check_secrets.sh .` | No credentials committed |
| `bash constitution/scripts/check_ots_inventory.sh .` | Dependencies match `docs/OTS_SOFTWARE.md` |
| `bash constitution/scripts/check_env_vars.sh .` | Environment variables are documented |
| `bash constitution/scripts/check_version_alignment.sh .` | `VERSION`, changelog, and tags agree |

## Submodule

| Command | What it does |
| --- | --- |
| `git submodule update --init --recursive` | Populate `constitution/` after a non-recursive clone |
| `git submodule update --remote constitution` | Pull the latest constitution release |

After updating the submodule, commit the new pointer:

```bash
git add constitution && git commit -m "Update constitution to <version>"
```

The `constitution-version` workflow fails the build when the pinned submodule
is behind the latest tagged release, so this is not optional maintenance.

## Deployment

There is no deploy command. Pushing to `main` is the deploy.

To re-run a deployment without a code change, use the workflow's
`workflow_dispatch` trigger from the Actions tab, or:

```bash
gh workflow run deploy-pages.yml
```

## Domain

| Command | What it does |
| --- | --- |
| `dig +short picklestoys.com` | Should return GitHub's four Pages IPs |
| `curl -sI https://picklestoys.com \| head -n 1` | Should return `HTTP/2 200` |
| `curl -sI http://picklestoys.com \| grep -i location` | Should show the redirect to HTTPS |

See `docs/DOMAIN_SETUP.md` for what to do when these do not return the expected values.
