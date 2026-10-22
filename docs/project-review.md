# Quiznauts project review

Reviewed October 22, 2026. Scope: the entire initial working tree, public content, operator documentation, architecture, native asset pipeline, saved browser evidence and current Git state. The WebP migration and one related verification correction were implemented during this review. The original findings below record the audit state. The current resolution table immediately below supersedes their original status; historical evidence has been retained.


## Harmony repair status — October 22

Current state is owned by `status.json`; the latest native check is `verification/latest-local.json`, and targeted repair evidence is `verification/harmony-repair.json`. Original findings and owner-run browser evidence remain historical. No staging, commit or publication is part of this repair.

| Findings | Current disposition |
| --- | --- |
| R01, R10 | Browser execution and human zoom, keyboard, print, screen-reader and visual acceptance remain with Ryan. The owner helper now includes mixed-score and completion-status assertions; it has not been run by the agent. |
| R02 | `./qn backup` supplies a verified local source checkpoint without a Git commit. Git still has no checkpoint; separate-disk recovery remains an owner choice. |
| R03, R13 | Previously implemented empty-output rejection and lossless WebP migration are retained and checked. All original PNGs/SVGs are preserved. |
| R04 | A shared offline URL policy rejects malformed/non-HTTP public URLs, credentials, local/reserved hosts and invalid destinations. Readiness and the Hugo indexing policy use that policy. Empty profile destinations remain valid local preparation. |
| R05 | Each section feed selects its own content; home intentionally remains a field-notes feed. The gate verifies entry identity, title and self URL. |
| R06, R07 | Mission pages resolve a registered `missionId` with matching data identity. Missing/mismatched data fails locally. The gate compares rendered IDs, prompts, choices, correct answers, reveals, explanations and sources. |
| R08, R09 | Required ZIPs, exact members, source bytes and manifest content are verified; recorded brand hashes are checked locally without the sibling project. Only recorded public brand assets enter the kit. |
| R11 | Final-score feedback updates a persistent polite live status without forcing focus. Changing an answer or resetting clears stale completion. Actual screen-reader acceptance remains open. |
| R12 | `status.json` is the current return record, `latest-local.json` is the latest source-bound check, marketing status owns only draft/publication decisions, and older evidence is historical. |
| R14 | `./qn art` backs up sources and completes SVG/PNG → WebP → kits. The generator has a main guard and stages/validates a whole native render batch before replacing saved artwork. No artwork regeneration was needed for this repair. |
| R15 | ZIP timestamps/permissions/order are deterministic; unchanged archives retain their bytes and modification time. |
| R16 | Hugo fingerprints CSS and quiz JS and emits integrity metadata. |
| R17 | The header reads the three configured Hugo menu entries. Mission question counts come from data. Curated homepage copy deliberately remains about First Contact. |
| R18 | The Mr. Big note renders its chosen WebP illustration with explicit dimensions and alt text. |
| R19 | Public metadata distinguishes field-note articles from other pages and supports a page-specific OG image; PNG defaults include dimensions and alt text. Preview metadata remains noindex. |
| R20 | Optional browser and artwork tools have explicit preflight errors. Builds keep using saved exports without those tools. |
| R21 | About-page copy now distinguishes the one current sample from planned subjects/channel formats. Account/domain/contact choices remain with Ryan; no destinations were invented. |
| R22 | The ocean-card alt starter now describes the actual card. Final platform crop/upload acceptance remains human work. |
| R23 | Bundled LibSass still builds on the installed Hugo version and reports its deprecation. A future Dart Sass migration remains documented maintenance; no extra compiler was installed. |
| R24 | Optional new content, responsive-size derivatives and larger reuse tooling remain deferred. These are enhancements, not correctness defects. |
| R25 | Removed the blanket PNG ignore and retained scoped browser/cache ignores. Original PNGs are visible to normal Git status and included in local source backups. |

## Overall assessment

This is a concrete local authoring project with a coherent first visitor journey. It has a Hugo website, one playable mission, three field notes, a recorded brand library and fourteen marketing compositions. The work is substantially beyond a placeholder. Its appropriate next milestone is a reviewed first edition with a reliable return point, rather than more infrastructure.

Public launch acceptance is incomplete. The only saved browser run failed before the documented reflow repair; no successful rerun is present. Real channel URLs and domain remain blank, intentionally. There is no Git recovery checkpoint because the repository has no commits. None of those facts prevents further local authoring.

## Git and index identity

- Checkout: `/Users/ryanjohnson/Projects/quiznauts-site`, branch `main`.
- At review start: 142 untracked, nonignored files; zero tracked or staged files; no commits; no configured remote. A conventional historical diff is unavailable. This review therefore inspected the full initial file set rather than treating empty `git diff` output as no changes.
- Initial inventory: six root files, six generated local GitNexus skill files, three site assets, eleven content files, three data files, ten documentation files, fourteen layouts, eight marketing workflow files, seven helper scripts and seventy-four static assets/archives.
- During the review, a concurrent edit added a blanket `*.png` rule to `.gitignore`. It was preserved. All twenty-two original PNGs remain on disk but are now ignored; current untracked status lists 146 files rather than the 168 that would appear with those sources included. The project still depends on those PNGs for kits, image regeneration and the PNG Open Graph image. See R25.
- GitNexus 1.6.12 registry identifies this exact checkout. Index timestamp: `2026-10-22T18:14:44.693Z`, or 1:14:44 p.m. Central. Index statistics: 59 files, 245 nodes, 305 edges, eleven communities and four processes. It has no commit identity because there is no HEAD.
- Before edits, indexed source hashes matched disk except `AGENTS.md`, which contains generated index instructions. The index predates this review's changes and new optimizer.
- Query results exposed browser-check flows and located packaging, artwork, quiz and source-validation symbols. Impact was LOW for `page`, packaging `main`/`write_zip`, and source `check`. The source checker result is explicitly a lower bound with five unresolved receiver call sites. `qn` and the Hugo media template returned UNKNOWN; direct tracing confirmed CLI dispatch, subprocess calls, content type selection and data/template paths.
- `detect-changes --scope all --repo .` fails because HEAD does not exist. That is unavailable diff evidence, not a clean graph-change check. A first commit remains Ryan's decision. No stage, commit, push, remote setup or publication occurred during this review.

## Architecture and ownership

| Layer | Source of truth | Behavior and boundary |
| --- | --- | --- |
| Operator commands | `qn` | Python CLI for status, preview, build, check, images, kits, readiness and explicit owner browser checks. No deployment command. |
| Site configuration | `hugo.toml`, `scripts/site_config.py` | Hugo parses its own effective configuration. Loopback/noindex is the current default. |
| Content | `content/` | Eleven Markdown content files generate the home/interior pages, two collections, mission, field notes, links and media kit. |
| Quiz | `data/quick_mission.json`, `layouts/mission/single.html`, `assets/js/mission.js` | Hugo emits all questions, native radios, answer details and sources. JavaScript adds checking, progress, completion and reset. No network request, timer or answer storage. |
| Layout | `layouts/`, `assets/scss/` | Small native Hugo templates, system fonts, one Sass pipeline and shared palette/control tokens. No theme/framework dependency. |
| Destinations | `data/properties.json` | Six platform entries with empty URLs and handles. Empty URLs do not become public buttons. |
| Brand masters | `static/brand/`, `docs/brand-source.json` | Forty-four source-recorded v1.4 SVG/PNG files copied from the sibling compiler project. All matched both their receipt and current sibling sources during this review. |
| Campaign artwork | `scripts/generate-art.py`, two Swift helpers, `data/marketing.json` | Fourteen local SVG/PNG compositions; text outlined using macOS CoreText and rendered through AppKit. Swift and named fonts are authoring requirements, separate from site builds. |
| Web derivatives | `scripts/optimize_images.py`, `docs/image-optimization.json` | Twenty-two lossless WebPs, regenerated by optional local cwebp. Saved derivatives build without an encoder. |
| Downloads | `scripts/package_kits.py` | Social ZIP contains fourteen SVG/PNG/WebP sets; brand ZIP contains the brand library plus WebPs. CRC and manifest checks establish file integrity, not rights or platform acceptance. |
| Publication preparation | `marketing/` | Bios, twelve draft posts, paired reveals, a fourteen-slot proposed sequence and one-mission reuse workflow. No automation or live account mutation. |
| Evidence | `docs/verification.json`, `docs/verification/`, ignored `reports/` | Original owner browser evidence is preserved separately from local/source success and this review's results. |

The key separation is sound: private compiler banks stay in the sibling project; the website owns three freshly authored sample questions. Runtime behavior stays static and local to the visitor's browser. Brand sources, WebP derivatives, downloadable archives and human acceptance are different records.

## Content and editorial review

The first visitor journey is complete in source: home → First Contact → explanation/source → field notes; the links page offers useful local destinations while external properties are empty. The voice is friendly without fake urgency, invented engagement claims or a fixed posting promise.

The three factual answers were checked against their linked primary sources during this review. NOAA supports the Pacific's largest/deepest basin status and the Atlantic's second-place size. NASA Space Place supports the rounded Venus rotation/orbit values and distinguishes its 117-day sunrise cycle. Monterey Bay Aquarium explicitly supports the red octopus's three hearts and their roles. Sources: [NOAA](https://oceanservice.noaa.gov/facts/biggestocean.html), [NASA](https://spaceplace.nasa.gov/all-about-venus/en/), [Monterey Bay Aquarium](https://www.montereybayaquarium.org/animals-the-ocean/animals-a-to-z/red-octopus).

The Venus question and note are particularly careful about the definition of “day.” Answer positions are B/C/A, explanations are short, and sources appear beside the explanations. The ocean marketing pair is bound to an exact question ID; the generator fails if its expected prompt/explanation changes. The Venus/octopus post pairs correctly disclose that adapted artwork is still needed.

Content limitations are mainly scale and presentation: only one playable mission exists; present-tense descriptions of a broad subject range or channel formats describe the editorial direction rather than evidence of a published catalogue. Keep new claims aligned with actual material as it is added. No new batch of content is needed to validate the existing first edition.

## Functionality and accessibility review

The mission code handles no selection, repeated checking, incorrect-to-correct changes, invalidating a checked answer after selection changes, all-correct completion and reset. The original owner browser run passed those states and the no-JavaScript explanation/source path. The implementation uses native radios, fieldsets/legends, details controls, live text feedback and a visible reset action.

Sass includes default 44px controls, visible focus, wrapping/shrinking layouts, reduced-motion and forced-colors rules, and print styling. These are useful implementation choices. They do not establish current rendered reflow or accessibility acceptance. The preserved initial browser run failed twelve of twenty-four layout cases and its keyboard visibility probe. A source repair and revised settling probe exist; a browser rerun is still pending.

No browser was launched during this review. The existing contact sheet was inspected as a local image; all PNG/WebP pairs were decoded and compared separately. Neither action is a browser or platform-upload test.

## Corrections and opportunities, in priority order

Priority here reflects this personal project's recovery, correctness and review needs; it is not a claim of a security incident or commercial-release obligation.

| ID / priority | Finding and evidence | Concrete next action |
| --- | --- | --- |
| R01 / high | No successful browser rerun exists after the reflow repair. The only saved report is the failed first owner run. | Ryan runs `./qn browser`, then reviews its remaining failures and actual page reading/crops. Preserve owner attribution. |
| R02 / high | No commits or tracked files exist. Git currently cannot recover any of the 142 initial files, and graph diff analysis cannot resolve HEAD. | When Ryan chooses, make a first reviewed recovery checkpoint or separate backup. No commit was authorized here. |
| R25 / high, concurrent change | A blanket `*.png` rule appeared in `.gitignore` during the review and hides all twenty-two required original PNG sources from a normal first Git checkpoint. A restored checkout without them cannot build kits or regenerate WebPs. The files remain intact locally. | Narrow the ignore rule to derived evidence or explicitly unignore `static/brand/png/` and `static/marketing/png/` before the recovery checkpoint. The concurrent edit was preserved, not silently reversed. |
| R03 / medium, fixed | `check_site.py` accepted an output directory containing only `robots.txt`: exit 0, pages 0, no failures. | Added required visitor-route checks; the same focused negative probe must now fail. Continue treating build success and generated-page coverage as separate evidence. |
| R04 / medium | `qn readiness` accepts an invalid public configuration. A read-only injected configuration with an FTP origin and `youtube.url = "not a URL"` returned `configuration_complete: true`. | Share an HTTP(S), real-host and nonempty-value validator across readiness, destination checks and metadata policy. Validate locally; ownership stays a human fact. |
| R05 / medium | `layouts/_default/rss.xml` always selects field notes. Consequently `/missions/index.xml` advertises “Quiznauts Field Notes” and contains three field notes instead of a mission feed. | Scope section feeds to the section or disable missions RSS deliberately. Add an XML assertion for title/entry identity. The main/footer field-notes feed is otherwise useful. |
| R06 / medium | `layouts/mission/single.html` always reads `hugo.Data.quick_mission`; `missionId` is unused and headings/CTAs contain fixed counts and routes. A second mission page would repeat First Contact's questions. | Before adding a second mission, resolve a page's explicit data ID and fail the build on missing/mismatched IDs. Keep the current one-mission scope until then. |
| R07 / medium | The source gate checks question data separately from rendered HTML, not that prompts, choices, answers and sources actually agree in the output. The browser helper covers some of this, but it is optional and slower. | Add a small static data-to-render assertion and mission identity check; keep malformed data diagnostics readable. |
| R08 / medium | ZIP checks verify CRC, not that required archives/members exist or match current source/manifest hashes. CRC-valid stale content can pass a direct checker invocation. The normal build does rebuild kits. | Add required archive/member and SHA-256 checks, including WebPs; keep checks deterministic and offline. |
| R09 / medium | Copied brand identity matches today, but the normal gate does not compare the forty-four files with `docs/brand-source.json`. | Add local receipt verification without requiring the sibling project. Review intentional brand changes and derivatives together. |
| R10 / medium | Browser coverage is three routes, twelve home Tab stops, Chromium only, and a document-width threshold. It does not prove all controls/routes, mixed-score outcomes, clipping, actual zoom, printed answers or screen-reader announcements. | Expand only where a real failure or decision warrants it. First review actual 200%/400% zoom, the full quiz by keyboard, final score announcement and print output. |
| R11 / medium | Completion score is inserted into a newly unhidden block without its own live status or focus change. Progress announces the checked count, not explicitly the final score. | During screen-reader review, verify whether completion and score are discoverable; if needed, add a concise completion status without forcing focus or scrolling. This is a source-based risk, not a demonstrated assistive-technology failure. |
| R12 / medium | `docs/verification.json`, handoff, reflow notes and `marketing/status.json` repeat state. Current operator docs also had contradictory “no GitNexus index” and not-yet-initialized Git wording. | Index/Git wording corrected here. Keep historical receipts immutable; designate one current status record and derive concise summaries when practical. |
| R13 / medium, implemented | Media gallery loaded full PNGs; PNG-only derivatives had no ongoing freshness receipt. | Added 22 exact lossless WebPs, WebP previews/downloads, kit inclusion, `./qn images` and hash/header freshness checks. All originals preserved. |
| R14 / medium | The artwork generator is a top-level script with dense composition strings, exact hardcoded question wording and macOS/font dependencies. Regeneration can replace many artifacts, while `qn kit` alone cannot refresh artwork. | Keep the documented source → SVG/PNG → WebP → kits → gate sequence explicit. Later add a short artwork command/main guard and staged generation if real editing makes this burdensome; do not add a new framework. |
| R15 / low | `write_zip` stores filesystem/current member timestamps. Rebuilding identical source can change ZIP bytes, producing noisy future diffs. | Use stable ZIP member metadata and only replace changed archives when reproducibility becomes useful. |
| R16 / low | CSS and quiz JS use stable unversioned resource URLs. A future hosted cache can retain older behavior while HTML changes. | Use Hugo fingerprinting for generated assets before a hosted release; verify paths in a subdirectory build. |
| R17 / low | `hugo.toml` declares a menu that the header/footer templates do not use; some copy and question counts also appear in multiple layers. | Either use the declared menu data or remove unused declarations intentionally. Derive counts/titles from mission data while retaining curated visitor copy. |
| R18 / low | `meet-mr-big.md` has image/imageAlt frontmatter that the single-page template does not render. It records an image choice without an actual illustrated field note. | Either display that editorial image accessibly or remove misleading unused metadata. Its path now points to the saved WebP. |
| R19 / low | All public pages share one OG image; the head lacks explicit image dimensions/alt and uses `article` for every regular page. | Refine metadata types and optional per-page images when a real domain is configured. Retain a PNG/JPEG share image until chosen consumers are checked. |
| R20 / low | The runtime is dependency-light, but owner browser tooling uses a hardcoded sibling venv; image authoring needs cwebp; vector authoring needs macOS Swift and two specific fonts. | Document those separate requirements and provide clear missing-tool messages. Preserve saved exports so optional tooling cannot block normal authoring. |
| R21 / low | Empty official links and lack of contact are intentional now; there is no usable public correction destination yet. Some broad mission/channel copy can read like a larger live catalogue. | Before publication, connect verified URLs and reread the copy against actual available content. Add only a real chosen correction route, without inventing a contact backend. |
| R22 / low | Alt-text starters and crop rectangles are aids rather than per-upload truth. For example, the accessible-publishing question-card starter describes a mascot/orbit diagram absent from the supplied ocean card. | Use the actual `data/marketing.json` description and final image for each post; correct the starter when preparing that post. Check smallest reading size, real crops and upload acceptance. |
| R23 / maintenance | Current Sass builds on Hugo 0.166.0 extended but uses deprecated bundled LibSass. | Plan a bounded migration to standalone Dart Sass when needed; do not suppress the warning or introduce npm solely for this. [Official Hugo guidance](https://gohugo.io/functions/css/sass/). |
| R24 / optional | More missions, richer field-note art, responsive-size gallery derivatives, improved mixed-score messaging and a one-command mission package could improve reuse. | Choose one only after completing and returning successfully to the current mission/package workflow. No account system, backend, analytics, service container or platform expansion is required. |

## WebP result and preservation

Twenty-two full-size images were encoded with cwebp 1.6.0 using lossless `-z 9 -exact -metadata none`. Source PNGs total 3,200,449 bytes; WebPs total 992,174 bytes, saving 69.0%. The fourteen gallery PNGs total 2,270,085 bytes versus 682,548 bytes for WebP, saving 69.9%. These are asset-byte comparisons, not measured browser timings.

Decoded 8-bit RGBA bytes matched for every one of the twenty-two PNG/WebP pairs, including hidden RGB and alpha. Eight mascot images and the video watermark retain transparency; the other thirteen retain their deliberate backgrounds. All original SVG/PNG hashes remain unchanged. PNGs remain in the kits and as individual download choices; the OG image stays PNG. The SVG-based homepage does not acquire an additional WebP performance claim.

YouTube's current official [profile guidance](https://support.google.com/youtube/answer/10456525?hl=en) lists PNG among accepted formats, and its [thumbnail guidance](https://support.google.com/youtube/answer/72431?hl=en) gives JPG/PNG examples and the same 3840 × 2160 video recommendation recorded here. Keeping upload PNGs is therefore useful. No live upload or crop acceptance was performed.

## Verification and next return

The current local results are recorded in `verification/current-review.json`. Checks are intentionally limited to the changed image/build boundary, source identity, archive contents, URL generation and focused negative probes. No full suite, browser, assistive-technology session, provider request, account mutation or publication was performed.

Ryan's next concrete command is:

```sh
./qn browser
```

Expected helper success is `passed: true`, twenty-four layout cases, no failed case names, zero blocked external requests and zero page errors. Inspect `reports/browser/results.json` and screenshots if it fails. Actual zoom, keyboard reading, screen-reader use, platform crop/upload acceptance and final content/visual acceptance remain separate even if that helper passes.

The readiness and feed findings are now repaired. After the owner browser review, resolve any observed rendered failures and decide whether a Git checkpoint or separate-disk copy is wanted. The current project can remain a finished local first edition while account/domain/publication decisions stay open.
