# Quiznauts site: return here

Saved October 22, 2026. The local Hugo companion and marketing scaffold are built. Start with `./qn status`, then `./qn` for the preview. Control-C stops the server. No account setup or publication is needed to keep working locally.

## What is here

- A complete atomic-era homepage with the approved adorable Mr. Big; missions, field notes, about, official links, media kit, site notes and a custom 404 page.
- One playable, untimed three-question mission. Correct answers and explanations remain available through native details controls without JavaScript. Each factual answer has a primary source.
- Three opening field notes, including the difference between Venus's rotation and solar day.
- Shared Sass colors, typography, spacing, control sizes and shape tokens in `assets/scss/_tokens.scss`. Hugo compiles `assets/scss/site.scss`; no npm or separate build process is involved.
- Fourteen distinct marketing designs, each as a standalone outlined SVG and PNG. These cover avatar, YouTube banner/thumbnail/end card, Open Graph, square and portrait posts, vertical invitation, question/reveal pair, wide profile header, Facebook cover, Pinterest and watermark.
- Downloadable social and brand ZIPs, asset descriptions and alt text, crop guides, and recorded brand-source hashes. The two download buttons live at `/media/`.
- Profile bios and YouTube About copy, twelve post drafts, a proposed fourteen-slot launch sequence, a property matrix, accessible publishing notes, and a one-mission reuse workflow in `marketing/`.

View `marketing-contact.jpg` beside this file for the asset contact sheet. Static artwork keeps its recorded production colors; changing Sass variables affects site styles rather than recoloring exported graphics.

## Evidence and limits

`./qn check` passed with 12 HTML pages, 295 local references, 14 marketing designs and 3 sample questions. Local checks cover document structure, alt attributes and dimensions, internal links and anchors, preview indexing defaults, SVG parsing/resources, PNG dimensions and ZIP integrity. All 44 copied production brand files match their recorded source hashes. A separate subdirectory build and link check passed at `https://example.test/quiznauts/`.

The approved reading-color pairs have calculated contrast ratios from 5.37:1 to 12.02:1. This verifies those color pairs, not every rendered state. Native inspection covered the exported marketing contact sheet; individual platform crops and compressed readability remain open.

The installed Hugo 0.166.0 extended release compiles Sass successfully with its bundled LibSass. It emits a known deprecation warning; future Hugo releases may require standalone Dart Sass. See `site-operations.md` for the exact maintenance boundary and official source. No warnings are globally suppressed.

The agent has not launched a browser. Ryan ran the first browser check: quiz scoring/reset and no-JavaScript checks passed; 12 of 24 layout cases and the keyboard visibility probe failed. That original report is preserved in `verification/browser-before-reflow.json`. Reflow and checker timing repairs are recorded in `reflow-repair.md`; their browser rerun is pending. Actual zoom, assistive technology and human content/visual acceptance remain separate. Run from this folder:

```sh
./qn browser
```

It builds locally, uses a temporary loopback server, blocks external page requests, and writes `reports/browser/results.json` plus bounded screenshots. It covers home/mission/media layouts, narrow reflow, text enlargement and spacing, reduced motion, forced colors, keyboard focus, scoring/reset, accessible choice names and the no-JavaScript reveal path. This is a focused regression check; actual browser zoom and screen-reader acceptance remain separate.

## Next concrete actions

1. Run `./qn`, open the printed URL, and review the homepage, mission and `/media/` artwork.
2. Run the browser command above and keep its report for follow-up fixes.
3. When ready to connect real properties, put only verified owned URLs in `data/properties.json`. Empty destinations stay hidden from visitors. Start with the intended YouTube channel to avoid duplicates.
4. Choose a public domain and hosting when launch is wanted. Set the real `baseURL`, complete review, then deliberately enable `params.indexable`. `./qn readiness` reports these configuration gaps; it does not authorize publication.
5. Use `marketing/one-session-workflow.md` to turn one reviewed mission into a video/upload draft, a supporting post and a field note. Save the exact live URLs only after publication.

The site remains in preview mode with noindex and a disallow-all robots policy. Channel ownership, handles, upload URLs, public domain and hosting are unverified. No accounts, credentials, remote repository, analytics, signups, scheduled automation, staging, commit, push, deployment or publication were created by this work. The sibling quiz project and its private banks remain separate.


## Current review and image update — October 22

The complete project/initial Git review is in `project-review.md`; current native-check evidence is in `verification/current-review.json`. Earlier counts above describe the original build. Current `./qn check` passes with 12 HTML pages, 309 local references, 14 marketing designs and 22 lossless WebP copies. The subdirectory build and focused checks also pass. The gate now rejects empty generated sites and stale image receipts.

All 22 PNG assets now have optimized WebPs, with exact decoded RGBA equality and a 69.0% total byte reduction. The gallery uses WebP; downloads retain PNG/SVG and add WebP. The eight mascots and watermark retain transparency; the thirteen composed backgrounds stay intact. All 72 original SVG/PNG files are unchanged, including the 44 brand files covered by the source receipt. After PNG edits, use `./qn images`, then `./qn check`. Ordinary builds need no encoder.

Git is initialized on `main`, but there are still no commits, tracked files or remote. There is no Git recovery checkpoint. Nothing was staged or committed in this review. The fresh GitNexus index was used for navigation/impact, with unresolved CLI/template edges traced directly; it now predates these edits. Its diff command cannot work without HEAD.

The next owner command remains `./qn browser`. No new browser has been launched, and the preserved first run is still the only saved browser evidence. After that result, the most useful bounded correction pass is local URL/readiness validation and the incorrect missions RSS feed. See the review's prioritized findings for details. More infrastructure or accounts are unnecessary for continuing locally.


Final Git inspection also found a concurrent blanket `*.png` addition in `.gitignore`. It was preserved. This hides the 22 required original PNGs from normal Git status even though they remain intact locally. Before a first checkpoint, narrow the ignore or add exceptions for `static/brand/png/` and `static/marketing/png/`; a restored copy still needs those inputs. This is review finding R25.
