# Setup

There is nothing to install. The site has no build step and no dependencies —
the only tools involved are `git`, a browser, and (for the test suite) `bash`
and `python`.

## Clone

The constitution is a submodule, so clone recursively:

```bash
git clone --recurse-submodules https://github.com/esanacore/PicklesToys.git
```

If you already cloned without `--recurse-submodules`:

```bash
git submodule update --init --recursive
```

Without this, `constitution/` is an empty directory and every governance
check fails with a message about the submodule being missing.

## Run the site locally

Open `site/index.html` directly in a browser, or serve the directory:

```bash
python -m http.server 8123 --directory site
```

Serving is preferable to opening the file directly: `site/404.html` links its
stylesheet with a root-absolute path (`/styles.css`), which resolves correctly
over HTTP and not over `file://`. `localStorage` also behaves more
consistently over HTTP, which matters when testing the theme toggle.

## Run the tests

```bash
bash tests/test_site.sh
```

Expect 47 passing structural checks plus the validator's self-test and two
validated documents. The suite needs `bash`, `grep`, and `python` — all
present on a bare CI runner, which is the point.

## Requirements

| Tool | Why | Notes |
| --- | --- | --- |
| `git` | Clone, submodule, and the push-to-deploy workflow | 2.13+ for recursive submodules |
| A browser | Viewing the site | Any modern one |
| `bash` | Test suite | Git Bash on Windows works |
| `python` | HTML/accessibility validator | 3.8+, standard library only |

No Node, no package manager, no toolchain. Adding one would break `T-061`.

## Verify a fresh clone actually works

Reading `git status` is not proof that a repository is complete. A file can be
silently excluded by a global gitignore and never appear as untracked. The
only reliable check is to clone into a scratch directory and run the suite
there:

```bash
git clone --recurse-submodules https://github.com/esanacore/PicklesToys.git /tmp/pt-check
bash /tmp/pt-check/tests/test_site.sh
```

This matters more than it sounds. A global gitignore on the maintainer's
machine excludes `lib/`, `build/`, `dist/`, `bin/`, and `packages/` as Python
packaging conventions. This repository does not currently use any of those
directory names, so it is unaffected — but if one is ever introduced, it will
vanish from commits without warning, and only a clean clone will reveal it.
