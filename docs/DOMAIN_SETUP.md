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

**If the DNS is on Cloudflare** (as `gentletable.com` is), set every one of
these records to **DNS only / grey cloud**, not proxied. An orange-cloud
proxied record in front of GitHub Pages breaks Pages' own certificate
provisioning and produces a redirect loop. This is the single most common way
this setup fails.

## 2. Set the custom domain in GitHub

**Settings → Pages → Custom domain** → `picklestoys.com` → Save.

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
