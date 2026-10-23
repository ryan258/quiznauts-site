# Local operation and eventual launch

The site is authored locally with Hugo. A GitHub Pages deployment pipeline is configured via `.github/workflows/deploy.yml` to build with Hugo extended 0.166.0, run contract tests, package kits, and publish the site using the configured GitHub Pages origin (`https://ryan258.github.io/quiznauts-site/` or custom domain). No Cloudflare project, database, form, email sender or provider binding is configured. The static site does not need those services to run.

Run `./qn` for a loopback preview and stop it with Control-C. `./qn build` creates `public/`; `./qn check` builds and checks generated pages, local links, source attribution and downloadable assets. `./qn kit` rebuilds the two download ZIPs. No helper publishes, pushes, sends messages or changes accounts.

To connect an existing account, enter its verified URL and handle in `data/properties.json`. Empty destinations are hidden from public navigation. Handle candidates in the marketing kit are proposals only. Keep confirmed ownership separate from availability assumptions.

The preview config is `baseURL = "http://localhost:1313/"` and `params.indexable = false`. When deploying through GitHub Pages, the workflow configures the public base URL dynamically via `actions/configure-pages`. Canonical/social metadata is conditional on a real public base URL and indexing being enabled. Template asset and route links use Hugo URL helpers (`relURL`, `RelPermalink`) which automatically adapt to root or subdirectory paths.

Hugo was built locally with version 0.166.0 extended on macOS. Shared authoring variables live in `assets/scss/_tokens.scss`, with styles in `assets/scss/site.scss`; `layouts/partials/head.html` compiles them through `css.Sass`. The initial site uses core Hugo templates and resource processing, without a downloaded theme or package installation. A different Hugo version should be checked with `./qn check` before relying on its output.

The installed extended release includes LibSass and emits its explicit deprecation warning while compiling successfully. Hugo documents future removal and recommends Dart Sass. The current project intentionally runs with the installed compiler; a future migration would install standalone Dart Sass, change the pipeline's `transpiler` to `dartsass`, and move the token import to `@use`. This is a known maintenance boundary, not a hidden clean-warning claim. [Hugo Sass documentation](https://gohugo.io/functions/css/sass/).

Keep `content/`, `data/`, `layouts/`, `assets/`, `static/`, `marketing/` and `docs/` together for recovery. `public/`, Hugo caches and browser reports are derived and ignored. Git is initialized on `main`, but the October 22 review found no commits or tracked files. Until Ryan authorizes a first commit or makes a separate backup, this checkout has no Git recovery checkpoint. Source distribution terms and public release remain owner decisions.


WebP copies are saved static artifacts; Hugo and ordinary checks do not need an encoder. After editing or regenerating PNG artwork, `./qn images` uses local `cwebp` to refresh lossless WebPs, the source/export receipt and both download kits. It preserves PNG originals, transparent mascot/watermark backgrounds and deliberate poster/banner backgrounds. See `visual-assets.md`.


## Current integrity and recovery contract

Use `docs/status.json` for current state and `docs/verification/latest-local.json` for the latest source-bound local check. Historical reports remain separate; no source check grants browser acceptance. `./qn status` shows the current return record. `./qn check` saves its result with an input fingerprint and never launches a browser.

`./qn backup` writes a verified source ZIP under `backups/`, including the original PNG inputs even if Git has no commits. Extract to a separate folder for recovery and run `./qn check` there. Keep another copy elsewhere for disk-loss recovery. `./qn art` creates that checkpoint before using optional macOS/Swift/font/cwebp tooling, renders the whole batch before replacing SVG/PNG outputs, then refreshes WebPs and kits. Saved exports remain sufficient for normal site builds.

Download kits use fixed ZIP metadata and replace an archive only when its bytes change. Only assets listed in the marketing inventory, brand-source receipt and derived-image receipt enter them. Normal checks compare every required archive member, manifest and content byte with its current source. Extra files placed beside brand assets are not swept into a download automatically.

The mission registry and shared URL policy are described in README.md. Invalid public origins or destinations must be corrected locally; verification never probes an account or infers its ownership. The home feed intentionally offers field notes; each section feed contains its own entries. Styles and quiz scripts use content fingerprints, and shared PNG Open Graph metadata now includes dimensions and descriptive text.
