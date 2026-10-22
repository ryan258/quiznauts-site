# Quiznauts: return here

Saved October 22, 2026. The local site, content contracts, download integrity, PNG preservation and WebP workflow have been reconciled. `status.json` owns current state. Historical checks remain in `verification.json` and `verification/`; they do not establish acceptance of this repaired build.

The site now follows the sibling player’s cut-paper space-poster style. Four byte-identical public WebPs supply the starfield, wordmark and two Mr. Big poses; `site-style-source.json` records hashes and origins. Tokens and `_poster.scss` supply the navy/cream/gold palette, paper banners and colored answer coins. Earlier marketing exports and v1.4 download kits remain preserved. A verified pre-style backup is `backups/quiznauts-source-20261022-180044-839420.zip`.

## Next action

Ryan runs:

```sh
./qn browser
```

The helper should report `passed: true`, 24 layout cases, no failed layout cases, zero blocked external requests and zero page errors. It now also checks mixed scores and completion status. Actual 200%/400% zoom, full keyboard reading, screen-reader use, printed answers, final visual/content acceptance and platform crops remain separate owner checks. The agent has not launched a browser. The only preserved browser run is still the failed first run from before the reflow repair.

## What is ready locally

- One three-question First Contact mission, three field notes, fourteen marketing designs, sourced explanations and no-JavaScript answer reveals.
- Explicit mission IDs; section-specific RSS; validated public URL syntax; fingerprinted CSS/JS; final-score status feedback; illustrated Mr. Big note; complete public OG image metadata.
- All original PNG/SVG artwork retained. Twenty-two full-size lossless WebPs stay linked to their source hashes; kits contain PNG/SVG/WebP and are deterministic.
- Local checks verify rendered quiz/data agreement, internal links, feeds, preview metadata, brand identity, WebP freshness and exact required ZIP contents. Read `verification/latest-local.json` for the latest result and source fingerprint.
- A local source checkpoint in `backups/`, verified with per-file hashes. Use `./qn backup` for another; restore into a separate folder and run `python3 qn check`. A same-disk backup does not cover disk loss.

## Short commands

| Command | Use |
| --- | --- |
| `./qn status` | Read configuration and current return state |
| `./qn` | Preview locally; Control-C stops it |
| `./qn check` | Build and save focused local contract results |
| `./qn images` | Refresh WebPs and kits after PNG edits |
| `./qn art` | Back up, render the SVG/PNG batch, refresh WebPs and kits; optional macOS tools/fonts required |
| `./qn backup` | Save a local source checkpoint without Git changes |
| `./qn readiness` | Report publication configuration gaps without probing accounts |

## Decisions and limits

The repository is organized into five logically grouped initial commits on `main`. PNG originals remain versioned alongside SVGs and WebPs. No remote push, deployment, account change or publication was performed. Actual public domain, account ownership and contact destination remain unchosen; keep empty property URLs hidden. Current preview mode stays noindex.

Hugo's installed LibSass compiler builds but emits its known deprecation warning; future Dart Sass migration remains maintenance. Optional new content and tooling are deferred. The issue-by-issue resolution table is in `project-review.md`; native repair evidence is in `verification/harmony-repair.json`. The previous return note is preserved in `verification/handoff-before-harmony.md`.
