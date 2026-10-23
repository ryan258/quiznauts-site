# Quiznauts site

The local Hugo companion to Quiznauts, with the cut-paper space-poster Mr. Big, a playable quick mission, field notes, profile copy and a reusable social/media asset kit.

From this folder, start the site with:

```sh
./qn
```

Open the printed loopback URL. Control-C stops the preview. Requirements: Hugo extended and Python 3.9 or later; the initial build was checked with Hugo 0.166.0 extended and the existing macOS Python. No account or backend is needed.

| Command | Result |
| --- | --- |
| `./qn` or `./qn serve` | Start the local Hugo preview |
| `./qn build` | Build into `public/` using the current preview/public configuration; noindex by default |
| `./qn check` | Build and run focused source/generated-site checks |
| `./qn browser` | Explicitly run the owner browser checks using the existing quiz Playwright environment |
| `./qn kit` | Refresh deterministic social and brand ZIPs; identical content keeps the existing files |
| `./qn images` | Refresh all lossless WebP copies and both ZIPs; authoring requires local `cwebp` |
| `./qn art` | Back up sources, render SVG/PNG artwork safely, then refresh WebPs and ZIPs; macOS authoring tools required |
| `./qn backup` | Save and verify a local source ZIP in `backups/`, including original PNGs; no Git changes |
| `./qn status` | Read the current state and show site configuration |
| `./qn readiness` | Report the remaining public-link/domain decisions |

The site is a local, single-user authoring tool for public-facing output. There are no credentials, signups, provider calls, analytics or publication actions in these commands.

## Where to work

- `content/`: site pages, missions and field notes.
- `data/quick_mission.json`: the three-question sample and its primary sources.
- `assets/scss/_tokens.scss`: approved brand colors, fonts, type sizes, spacing and shape variables.
- `assets/scss/site.scss`: shared site rules; `_poster.scss` adapts the current player look. Hugo compiles Sass into CSS during preview and build.
- `data/properties.json`: verified channel/social URLs. Empty values stay out of visitor links.
- `hugo.toml`: base URL, site metadata and indexing flag. Preview defaults are deliberate.
- `static/brand/`: preserved v1.4 SVG/PNG/WebP production library (`docs/brand-source.json`), plus the current player’s four public WebPs under `player/bass/` (`docs/site-style-source.json`).
- `static/marketing/`: property-specific SVG masters, PNG upload exports, WebP gallery images and downloadable ZIPs.
- `data/marketing.json`: export inventory, dimensions, descriptions and crop guides.
- `marketing/`: profile copy, post drafts, launch sequence and an operator workflow.

The media kit is available at `/media/`; connected destinations live at `/links/`. A social profile is shown only after its real URL is entered. This scaffold does not claim a channel, handle, audience size or publishing schedule already exists.

All 22 source PNGs have optimized lossless WebP copies. Existing transparency stays intact; composed poster/banner backgrounds stay intact too. PNG originals and SVG masters remain available for uploads and recovery. Ordinary builds use the saved files without an image encoder. After changing PNGs, run `./qn images`; `./qn check` detects missing or stale WebP copies. See `docs/image-optimization.json` for hashes and `docs/visual-assets.md` for the workflow.

## Shared brand variables

Edit `assets/scss/_tokens.scss` to adjust the site palette and design tokens. The current player palette is paper `#F3E6C8`, navy ink `#071D2B`, night sky `#031522`, gold `#EFB23F`, vermilion `#DC4027` and blue `#2B5E9E`. System Avenir/Futura stacks echo the player; prose keeps an uncondensed body font. The legacy `--teal` property now aliases navy for existing shared rules. `site.scss` exposes the Sass values as CSS custom properties so responsive, motion and contrast preferences still work at runtime. The homepage uses the matching starfield, wordmark and printed Mr. Big; missions use paper banners and colored answer coins. Artwork stays static, controls keep their minimum sizes, and the quiz remains untimed. Darker red/green variants support small text. Static marketing SVG/PNG artwork and downloadable v1.4 kits retain their recorded production colors; changing a site token does not recolor exported artwork automatically.

This project uses the Sass compiler bundled in the installed Hugo extended release. Hugo currently emits a LibSass deprecation notice; the build succeeds. Before upgrading to a Hugo version that removes it, migrate the single Sass pipeline to Dart Sass. No npm packages or separate compiler are required for the verified local version. See `docs/site-operations.md`.

## Browser review

Ryan runs browser verification locally. The sibling quiz project already has Python Playwright; from this folder use:

```sh
./qn browser
```

It writes a compact JSON report and screenshots under `reports/`. It is a focused regression check, not a full accessibility evaluation. Actual 200%/400% zoom, screen-reader use and human visual review remain separate. Browser tooling is optional and does not become a dependency for building or using the site.

The first owner run on October 22 found reflow failures, while quiz scoring/reset and no-JavaScript explanations passed. The local repair and its verification status are recorded in `docs/reflow-repair.md`. The original run is preserved separately; source checks do not establish a successful browser rerun.

## Return and launch

Read `docs/handoff.md` for the saved state and the next concrete actions. `docs/site-operations.md` describes the local/public boundary. `docs/visual-assets.md` records platform export choices and crop limits; `docs/editorial-sources.md` records factual sources.

The October 22 full project review and issue-resolution table are in `docs/project-review.md`. `docs/status.json` owns the current return state; `docs/verification/latest-local.json` records the latest `./qn check` with a source fingerprint. Earlier evidence files remain historical receipts.

The short command is the recovery path: `./qn status`, then `./qn` to continue.

## GitHub Pages hosting

The repository includes a GitHub Actions workflow in `.github/workflows/deploy.yml` configured to build and deploy to GitHub Pages on pushes to `main` (or via manual `workflow_dispatch`).

To activate on GitHub:
1. In the repository on GitHub, go to **Settings → Pages**.
2. Under **Build and deployment → Source**, select **GitHub Actions**.
3. When `main` is pushed, the workflow runs contract tests, packages download kits, builds with Hugo extended 0.166.0 using the detected GitHub Pages base URL (`https://ryan258.github.io/quiznauts-site/` or custom domain), and publishes the artifact with `.nojekyll` protection.

## Content contracts and recovery

`data/missions.json` maps public mission IDs to JSON data names. Each mission page must declare its `missionId`; missing or mismatched identities fail the build. Add a separate reviewed data file before registering another mission. `quick_mission.json` remains the independent three-question sample. Native source checks compare every rendered prompt, choice, answer, explanation and source with the selected data, verify section feeds, brand hashes, ZIP contents and WebP freshness.

`data/url_policy.json` supplies the shared public-host rules for readiness, destination checks and Hugo metadata. Invalid configured destinations fail local checks; empty destinations stay hidden. Syntactically valid URLs do not establish account ownership or a live page. The current preview configuration intentionally remains incomplete for publication.

For a recoverable local checkpoint use `./qn backup`. It includes source content, documentation, tools, SVG/PNG/WebP assets and kits, with verified SHA-256 hashes. It excludes Git internals, runtime caches, browser reports and root credential files. Restore into a separate folder, then run `python3 qn check` there. Backups on the same disk do not protect against disk loss; copy a checkpoint to a separate disk when wanted. Nothing stages or commits the files.

Focused regression checks for these corrections, when needed:

```sh
python3 -m unittest discover -s scripts -p test_contracts.py
```

This is the targeted URL/content/archive test file, not a browser or full-suite command.
