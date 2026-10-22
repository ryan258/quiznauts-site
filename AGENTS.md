# Quiznauts site operator capsule

This is Ryan's local, single-user authoring project for the Quiznauts channel website and reusable marketing materials. Public output is the purpose; a hosted application, multi-user platform, billing, logins and provider services are not required to author it. Preserve work, make return paths clear, and keep commands short and voice-friendly.

- Ryan has MS and relies on voice input, aliases and short commands. Minimize required typing and repeated setup. Ask one concise lettered choice only when a material decision cannot be inferred.
- Keep owner authority over account creation, credentials, staging, commits, pushes, deployment, domain/DNS changes, publishing and external messages. None is implied by a local build.
- Stack: Hugo extended with native Sass, vanilla JavaScript and Python standard-library tooling. Brand variables live in `assets/scss/_tokens.scss`; `assets/scss/site.scss` exposes them as CSS custom properties. No Node/npm, JS framework, CSS framework, Docker, tracking, third-party fonts, contact backend or newsletter service without a concrete authorized need.
- Read `README.md`, `docs/project-brief.md`, `data/properties.json` and the relevant source before changes. This project has a GitNexus index; bind it to this checkout and use it as described below. Confirm unresolved Hugo/template/CLI edges with native source searches.
- Source content is in `content/`; the three-question sample is `data/quick_mission.json`. Do not copy private quiz banks from the sibling compiler project. Keep each factual explanation linked to its primary source.
- Mr. Big follows the selected Atomic Advertising direction. Preserve round paws/feet, compact toy proportions, button eyes, closed smiles, one collar, white forehead and eye areas, and the large viewer-right temple patch. Never mirror the asymmetric head.
- `static/brand/` is a recorded copy of the sibling Quiznauts v1.4 production library. `docs/brand-source.json` records its origins and hashes. Update source and derived graphics together when intentional. Do not copy the private reference photo into public assets.
- Keep original PNGs/SVGs and derived WebP copies together. `./qn images` refreshes lossless WebPs and kits after PNG edits; it requires local `cwebp` only for artwork authoring. Preserve existing alpha and intentional composed backgrounds. `docs/image-optimization.json` records source/export hashes.
- `data/properties.json` owns real external destinations. Empty values stay out of public links. Do not claim reserved handles, live accounts, episodes, followers or an upload cadence without evidence.
- Normal text uses ink/teal on cream or cream on teal. Keep accents and print texture away from essential text. Preserve 44px default controls, visible focus, keyboard access, text-based quiz feedback, reduced-motion support, no timers and static-first imagery.
- `./qn check` is the focused local gate. Run only checks needed for changed behavior. Ryan runs browser verification himself; provide the command rather than launching a browser. Do not describe source/native checks as browser, assistive-technology or human acceptance.

Shared default operating intent: `/Users/ryanjohnson/Projects/cyborg/MANUAL.md`, “Default project operating intent.”

<!-- gitnexus:start -->
# GitNexus — Code Intelligence

This project is indexed by GitNexus as **quiznauts-site** (245 symbols, 305 relationships, 4 execution flows).

> Index stale? Run `node .gitnexus/run.cjs analyze --index-only` from the project root — it auto-selects an available runner. No `.gitnexus/run.cjs` yet? Bootstrap with `npx`, `bunx`, or `pnpm dlx` — e.g. `bunx gitnexus@latest analyze` (npm 11 npx crash; #1939).

## Always Do

- **MUST run impact before editing.** Use `impact({target: "symbolName", direction: "upstream"})` or `node .gitnexus/run.cjs impact "symbolName" --direction upstream --repo .`; report callers, processes, and risk. Never substitute grep for graph analysis.
- **MUST analyze graph changes before committing.** Use `detect_changes({scope: "all"})` (MCP) or `node .gitnexus/run.cjs detect-changes --scope all --repo .` (CLI fallback). `partial: true` or `truncated: true` is not a clean check — a zero means unseen, not unaffected; re-run it. For regression review: `detect_changes({scope: "compare", base_ref: "main"})` or `node .gitnexus/run.cjs detect-changes --scope compare --base-ref "main" --repo .`.
- MUST warn on HIGH/CRITICAL `risk` pre-edit; never use `riskSharedAxes` to waive a HIGH/CRITICAL `risk` warning. Compare File/symbol: MCP File omits axes; Graph-RAG expands File.
- **MUST treat `risk: UNKNOWN` as unresolved, not as low.** An empty caller set is not evidence the symbol is unused — it can also mean the callers are not resolvable by the index (plain-object property access, dynamic dispatch, cross-language calls). `impact` pairs `UNKNOWN` with a `riskNote` saying so. Confirm with a text search before treating the symbol as safe to change or delete; do not proceed on the strength of a zero.
- **MUST use `query({search_query: "concept"})` for concepts/flows, `context({name: "symbolName"})` for a named symbol, or `impact` for blast radius, on read-only callers, dependencies, imports, or execution flow.** Graph first; text search only for empty/`UNKNOWN`/literals.
- For security review, `explain({target: "fileOrSymbol"})` lists taint findings (source→sink flows; needs `analyze --pdg`).

## Never Do

- NEVER edit a function, class, or method before MCP/CLI impact analysis.
- NEVER ignore HIGH or CRITICAL risk warnings from impact analysis, and never read `UNKNOWN` as an all-clear — it means the walk could not answer, which is the one verdict that requires confirming by other means.
- NEVER rename symbols with find-and-replace — use `rename` which understands the call graph.
- NEVER commit before MCP/CLI graph change analysis.

## Resources

| Resource | Use for |
| --- | --- |
| `gitnexus://repo/quiznauts-site/context` | Codebase overview, check index freshness |
| `gitnexus://repo/quiznauts-site/clusters` | All functional areas |
| `gitnexus://repo/quiznauts-site/processes` | All execution flows |
| `gitnexus://repo/quiznauts-site/process/{name}` | Step-by-step execution trace |

## CLI

| Task | Read this skill file |
| --- | --- |
| Understand architecture / "How does X work?" | `.claude/skills/gitnexus-exploring/SKILL.md` |
| Blast radius / "What breaks if I change X?" | `.claude/skills/gitnexus-impact-analysis/SKILL.md` |
| Trace bugs / "Why is X failing?" | `.claude/skills/gitnexus-debugging/SKILL.md` |
| Rename / extract / split / refactor | `.claude/skills/gitnexus-refactoring/SKILL.md` |
| Tools, resources, schema reference | `.claude/skills/gitnexus-guide/SKILL.md` |
| Index, status, clean, wiki CLI commands | `.claude/skills/gitnexus-cli/SKILL.md` |

<!-- gitnexus:end -->
