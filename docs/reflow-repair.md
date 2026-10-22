# Reflow repair after the first owner browser run

October 22, 2026. Ryan ran `scripts/check_browser.py` against the local Hugo site with Chromium 156.0.8078.4. The original report is preserved in `verification/browser-before-reflow.json`; its hash and owner attribution are in `verification.json`.

## What the original run established

- 24 layout cases ran. Twelve failed the existing document-width overflow check.
- The complete quiz state check passed: empty selection, incorrect-to-correct change, repeated checking, all-correct score, changing a completed answer, and reset. Choice accessible names included their letters.
- The no-JavaScript details and source-link check passed.
- No external requests or page script errors were observed.
- Keyboard focus remained on the expected ninth Tab target with `:focus-visible`, but the immediate visibility sample was outside the viewport. The original report cannot establish whether native smooth scrolling had finished.

These are results from the owner's initial run, not evidence about the repaired build.

## Layout changes

The repair keeps content visible and lets layout shrink and wrap. It does not hide horizontal overflow on the page or weaken the browser width gate.

- Bound header and footer wordmarks to their available width. The original footer's 15rem width becomes 480px at 200% root text; adding its 35px left gutter explains the reported 515px extent.
- Give grid tracks and flex children a zero automatic minimum where content must reflow. Let answer labels, headings, buttons and navigation wrap within the available width.
- Keep raw source URLs inside media cards readable by allowing breaks inside an otherwise unbroken URL.
- Keep rotated decorative shapes inside their available space. Their connection to the original homepage's small overflow is a source-based diagnosis, supported by the forced-colors case passing when the shapes were absent.
- Keep fixed-size mascot and decorative elements responsive when text is enlarged. Brand tokens and default comfortable control sizes remain in place.

## Checker changes

The keyboard probe waits for the browser's actual native Tab focus and scrolling to settle, with a 2.5-second bound. It records scroll position, element rectangle and settling time. It does not focus or scroll the target itself, disable smooth scrolling, or relax the viewport assertion. A settled target outside the viewport still fails. Keyboard screenshots preserve the observed scroll position.

Overflow hints now include header, main, footer and body content, plus bounded overflow-container and generated pseudo-element details. The original `scrollWidth > clientWidth + 1` failure threshold is unchanged.

`./qn browser` is a shorter explicit owner command that uses the sibling quiz project's existing Playwright environment. Local `./qn check` and build commands never invoke it or launch a browser.

## Verification and next step

The repair was reviewed against the supplied report, screenshots, templates and Sass. Local `./qn check` passed after applying the repair: 12 HTML pages and 295 local references, with valid artwork/downloads. Python helper syntax passed and the updated CLI help lists the explicit browser command. These local checks are separate from browser evidence. The post-repair browser result is pending; no browser has been launched by the agent.

From the sibling quiz project, run:

```sh
../quiznauts-site/qn browser
```

From this site folder, use `./qn browser`. The helper writes `reports/browser/results.json` and screenshots. Expected success is `passed: true`, 24 layout cases, an empty failed-case list, zero external requests and zero page errors. If it fails, the report contains the remaining case and focus diagnostics. Actual zoom, assistive technology, platform crops and final human visual acceptance remain separate.
