# Pointing picklestoys.com at this site

The site is published by GitHub Pages from the `site/` directory on every push
to `main`. Until DNS is configured, it is reachable only at the
`esanacore.github.io/PicklesToys` URL. This document is the checklist for
making `picklestoys.com` serve it.

Nothing here needs to happen for the repository to be correct — the site is
already building and testing. This is the last mile.

## Prerequisite: enable Pages once

In the repository: **Settings → Pages → Build and deployment → Source:
GitHub Actions**. The `deploy-pages.yml` workflow does the rest. Without this
one-time setting, the workflow will fail at the deploy step with a message
about Pages not being enabled.

## 1. DNS records at the registrar

`site/CNAME` already contains `picklestoys.com`, so the apex is the canonical
host and `www` redirects to it. The records to create:

| Type | Name | Value |
| --- | --- | --- |
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| CNAME | `www` | `esanacore.github.io.` |

All four A records are required — they are GitHub's anycast set, not
alternatives to pick from.

**The `www` CNAME must target `esanacore.github.io`, not the apex.** This
looks like it should not matter: `www` → `picklestoys.com` → the GitHub
addresses routes a request to GitHub perfectly well. It was tried here, on
the reasoning that one fewer record is one fewer thing to get wrong. It is
wrong.

GitHub only provisions a certificate for a hostname it can verify points at
it in the shape it expects. With `www` aliased to the apex, the issued
certificate covered the apex alone:

```
X509v3 Subject Alternative Name:
    DNS:picklestoys.com
```

and the API agreed — `"domains": ["picklestoys.com"]`. The result is that
`https://www.picklestoys.com` fails TLS outright, which presents to a visitor
as a browser security warning: worse than a 404, because it looks like the
site is compromised rather than absent. Point `www` at
`esanacore.github.io` and GitHub extends the certificate to cover it and
redirects `www` to the apex.

After changing the record, GitHub does not re-check immediately, and
re-saving the same custom-domain value is a no-op. It re-verifies on its own
schedule; if it has not picked the change up, removing the custom domain and
re-adding it in Settings forces re-provisioning at the cost of a brief window
where the domain serves nothing.

**If the DNS is on Cloudflare** (as `gentletable.com` is), set every one of
these records to **DNS only / grey cloud**, not proxied. An orange-cloud
proxied record in front of GitHub Pages breaks Pages' own certificate
provisioning and produces a redirect loop. This is the single most common way
this setup fails.

## 2. Set the custom domain in GitHub

**Settings → Pages → Custom domain** → `picklestoys.com` → Save.

Doing this over the API takes two calls, not one. Setting the domain and
`https_enforced` together fails with `The certificate does not exist yet`
(HTTP 404), because there is no certificate to enforce against until the
domain is verified:

```bash
gh api repos/esanacore/PicklesToys/pages -X PUT -f 'cname=picklestoys.com'
# wait for .https_certificate.state to become "approved"
gh api repos/esanacore/PicklesToys/pages -X PUT   -f 'cname=picklestoys.com' -F 'https_enforced=true'
```

GitHub verifies the DNS, then provisions a Let's Encrypt certificate. This
usually takes a few minutes but can take up to 24 hours. Once the certificate
is issued, tick **Enforce HTTPS**.

**This step is required, not optional.** With an Actions-based deploy (as
opposed to the older publish-from-a-branch mode), the `CNAME` file inside the
uploaded artifact does **not** register the custom domain by itself. Verified
on this repository: after the first successful deploy with `site/CNAME`
present and containing `picklestoys.com`, the API still reported
`"cname": null`. The Settings value is the authoritative one.

`site/CNAME` is still kept in version control deliberately — it travels with
the artifact, documents the intended domain in the source rather than only in
a settings page, and is asserted by `T-080`. Keep the two in agreement: if the
domain ever changes, change `site/CNAME` too or the test fails.

Check which state you are in with:

```bash
gh api repos/esanacore/PicklesToys/pages --jq '{cname: .cname, status: .status}'
```

## 3. Verify

```bash
dig +short picklestoys.com
curl -sI https://picklestoys.com | head -n 1
curl -sI http://picklestoys.com | grep -i location
```

Expected: the four GitHub IPs, `HTTP/2 200`, and an http→https redirect.

**If the http→https redirect does not appear on `/` but does on a subpath,
it is a cache, not a fault.** GitHub's CDN serves Pages HTML with
`Cache-Control: max-age=600`, so any plain-http request made before Enforce
HTTPS was switched on stays cached as a `200` for up to ten minutes. The
give-away is in the response headers:

```bash
curl -sI http://picklestoys.com/ | grep -iE 'age|x-cache|cache-control'
# X-Cache: HIT      Age: 490      Cache-Control: max-age=600
```

`curl http://picklestoys.com/favicon.svg` redirecting while `/` does not is
the same signal — the asset was never cached over http. Wait out the TTL
rather than changing anything. Note that verifying the domain over http
*before* enabling HTTPS is what plants this cache entry in the first place.

Then confirm the deploy is actually current — that the live page is this
repository's `site/index.html` and not a cached placeholder from the
registrar's parking page.

## Registrar and DNS host

- **DNS host: GoDaddy** — confirmed 2026-09-10 from the live nameservers:

  ```bash
  nslookup -type=NS picklestoys.com
  # picklestoys.com  nameserver = ns37.domaincontrol.com
  # picklestoys.com  nameserver = ns38.domaincontrol.com
  ```

  `domaincontrol.com` is GoDaddy's nameserver domain, so step 1 happens in
  the GoDaddy DNS panel, **not** Cloudflare — unlike gentletable.com.
- **Registrar: almost certainly GoDaddy**, but strictly speaking the
  nameservers only prove where DNS is *hosted*. It is possible (though
  unusual) to register elsewhere and point at GoDaddy's nameservers. Confirm
  in the account before relying on it for renewal.
- **Expiry: TBD** — visible on the GoDaddy domain page; worth recording here,
  since a lapsed domain is the one failure no amount of repository hygiene
  protects against.

**Live at https://picklestoys.com since 2026-09-10.** The apex was serving
GoDaddy's parking lander (`15.197.148.33`, `3.33.130.190`) until the four
GitHub addresses replaced it; the certificate was approved about twenty
seconds after the custom domain was set.

### The Cloudflare warning does not apply here

The grey-cloud/orange-cloud proxying caveat elsewhere in this document is a
Cloudflare concern. GoDaddy's DNS does not proxy, so there is no equivalent
setting to get wrong. Keep the warning in place in case the domain is ever
moved to Cloudflare to match gentletable.com.

### Where the records go in GoDaddy

**Domain portfolio → picklestoys.com → DNS → DNS Records.**

GoDaddy pre-populates a parked `A` record on `@` pointing at its own parking
IP, and often a `CNAME` on `www` pointing to `@`. Edit the existing `@` record
to the first GitHub address and **Add** the other three — GoDaddy allows
multiple `A` records on the same name, which is what GitHub's anycast set
needs. Delete any leftover parking record that does not point at one of the
four addresses, or the domain will intermittently serve GoDaddy's parking
page instead of the site.

GoDaddy's TTL default of 1 hour is fine. Propagation is usually minutes, but
allow up to the TTL before concluding something is wrong.
