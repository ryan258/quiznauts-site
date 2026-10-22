#!/usr/bin/env python3
"""Owner-run, local-only browser checks. Does not publish or contact sources.

Run from the site folder with the existing source project's Python environment:
    ../quiznauts/venv/bin/python scripts/check_browser.py

Builds public/, serves it on a temporary loopback port, checks Chromium, and
writes reports/browser/results.json plus viewport-sized screenshots. It never
installs a package/browser. This file was authored without launching a browser.
"""

from __future__ import annotations

import functools
import json
from pathlib import Path
import subprocess
import sys
import threading
import traceback
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports" / "browser"
PAGES = {"home": "/", "mission": "/missions/first-contact/", "media": "/media/"}
SCENARIOS = [
    {"name": "desktop", "width": 1280},
    {"name": "narrow", "width": 320},
    {"name": "desktop-text-200", "width": 1280, "text200": True},
    {"name": "narrow-text-200", "width": 320, "text200": True},
    {"name": "desktop-text-spacing", "width": 1280, "spacing": True},
    {"name": "narrow-text-spacing", "width": 320, "spacing": True},
    {"name": "reduced-motion", "width": 1280, "reduced_motion": "reduce"},
    {"name": "forced-colors", "width": 320, "forced_colors": "active"},
]

LAYOUT_PROBE = """() => {
  const width = document.documentElement.clientWidth;
  const visible = el => {
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden'
      && s.display !== 'none' && !el.closest('.sr-only,[hidden]');
  };
  const region = el => el.closest('header') ? 'header' : el.closest('footer')
    ? 'footer' : el.closest('main') ? 'main' : 'body';
  const describe = el => {
    const r=el.getBoundingClientRect(),s=getComputedStyle(el);
    return {tag:el.tagName,id:el.id,region:region(el),
      class: typeof el.className === 'string' ? el.className : '',
      text: el.textContent.trim().slice(0,80),
      left:Math.round(r.left),right:Math.round(r.right),
      top:Math.round(r.top),bottom:Math.round(r.bottom),
      clientWidth:el.clientWidth,scrollWidth:el.scrollWidth,
      overflowX:s.overflowX,position:s.position,transform:s.transform};
  };
  const elements=[...document.querySelectorAll('body,body *')].filter(visible);
  const outside=elements.filter(el => {
    const r=el.getBoundingClientRect();
    return r.left < -1 || r.right > width + 1;
  });
  const regions=['header','main','footer','body'];
  const outsideCounts=Object.fromEntries(regions.map(name =>
    [name,outside.filter(el => region(el)===name).length]));
  // Bound each region separately so a large main section cannot hide footer hints.
  const outsideHints=regions.flatMap(name => outside
    .filter(el => region(el)===name).slice(0,6).map(describe));
  const containers=elements.filter(el => el.clientWidth>0
    && el.scrollWidth>el.clientWidth+1)
    .sort((a,b) => (b.scrollWidth-b.clientWidth)-(a.scrollWidth-a.clientWidth))
    .slice(0,16).map(describe);
  const pseudos=[];
  for (const el of elements) {
    for (const pseudo of ['::before','::after']) {
      const s=getComputedStyle(el,pseudo);
      if (s.content==='none'||s.content==='normal'||s.display==='none') continue;
      pseudos.push({owner:describe(el),pseudo,content:s.content.slice(0,80),
        position:s.position,width:s.width,height:s.height,left:s.left,right:s.right,
        top:s.top,bottom:s.bottom,transform:s.transform,boxShadow:s.boxShadow,
        overflowX:s.overflowX});
    }
  }
  return {viewportWidth:width, scrollWidth:document.documentElement.scrollWidth,
    horizontalOverflow:document.documentElement.scrollWidth > width + 1,
    possibleOutsideElements:outsideHints,outsideElementCounts:outsideCounts,
    overflowContainers:containers,generatedPseudoStyles:pseudos.slice(0,16),
    generatedPseudoCount:pseudos.length,
    bodyClientWidth:document.body.clientWidth,bodyScrollWidth:document.body.scrollWidth,
    rootFontSize:getComputedStyle(document.documentElement).fontSize,
    reducedMotion:matchMedia('(prefers-reduced-motion: reduce)').matches,
    forcedColors:matchMedia('(forced-colors: active)').matches,
    scrollBehavior:getComputedStyle(document.documentElement).scrollBehavior,
    autoplayElements:document.querySelectorAll('video[autoplay],audio[autoplay]').length,
    bodyFont:getComputedStyle(document.body).fontFamily};
}"""

FOCUS_PROBE = """async () => {
  const target=document.activeElement,started=performance.now(),limitMs=2500;
  let previous=null,stationarySince=started,settled=false;
  while (performance.now()-started<limitMs) {
    await new Promise(resolve => requestAnimationFrame(resolve));
    const r=target.getBoundingClientRect();
    const current=[scrollX,scrollY,r.left,r.top,r.right,r.bottom,innerWidth,innerHeight];
    // Only the settling measurement uses a subpixel threshold; visibility below
    // retains its original exact viewport intersection assertion.
    const stationary=previous && current.every((value,index) =>
      Math.abs(value-previous[index])<0.01);
    if (!stationary) stationarySince=performance.now();
    previous=current;
    if (performance.now()-started>=200 && performance.now()-stationarySince>=150) {
      settled=true;
      break;
    }
  }
  const el=document.activeElement,r=el.getBoundingClientRect(),s=getComputedStyle(el);
  return {tag:el.tagName,text:el.textContent.trim().slice(0,100),
    href:el.getAttribute('href'),focusVisible:el.matches(':focus-visible'),
    outlineStyle:s.outlineStyle,outlineWidth:s.outlineWidth,boxShadow:s.boxShadow,
    inViewport:r.bottom>0&&r.top<innerHeight&&r.right>0&&r.left<innerWidth,
    settled,settleDurationMs:Math.round(performance.now()-started),
    focusChangedWhileWaiting:el!==target,scrollX,scrollY,
    viewportWidth:innerWidth,viewportHeight:innerHeight,
    rect:{left:r.left,right:r.right,top:r.top,bottom:r.bottom},
    scrollBehavior:getComputedStyle(document.documentElement).scrollBehavior};
}"""


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def wait_visible_images(page):
    page.wait_for_function("""() => [...document.images].filter(i => {
      const r=i.getBoundingClientRect();
      return i.getClientRects().length && r.bottom>0 && r.top<innerHeight
        && r.right>0 && r.left<innerWidth;
    }).every(i => i.complete && i.naturalWidth>0)""", timeout=10000)


def screenshot(page, name, selector=None, preserve_scroll=False):
    if selector:
        page.locator(selector).first.scroll_into_view_if_needed()
    elif not preserve_scroll:
        page.evaluate("window.scrollTo(0,0)")
    wait_visible_images(page)
    target = REPORT_DIR / f"{name}.png"
    page.screenshot(path=str(target), full_page=False, animations="disabled")
    return str(target.relative_to(ROOT))


def configure_context(browser, base, report, **kwargs):
    context = browser.new_context(service_workers="block", **kwargs)
    local = urlsplit(base)

    def local_only(route):
        target = urlsplit(route.request.url)
        if target.scheme in {"data", "blob", "about"}:
            route.continue_()
        elif (target.scheme, target.netloc) == (local.scheme, local.netloc):
            route.continue_()
        else:
            report["blocked_external_requests"].append(route.request.url)
            route.abort()

    context.route("**/*", local_only)
    context.on("page", lambda page: page.on(
        "pageerror", lambda error: report["page_errors"].append(str(error))))
    return context


def run_layout_checks(browser, base, report):
    for scenario in SCENARIOS:
        context = configure_context(
            browser, base, report,
            viewport={"width": scenario["width"], "height": 900},
            reduced_motion=scenario.get("reduced_motion", "no-preference"),
            forced_colors=scenario.get("forced_colors", "none"),
        )
        try:
            page = context.new_page()
            for label, path in PAGES.items():
                entry = {"scenario": scenario["name"], "page": path}
                try:
                    response = page.goto(base + path, wait_until="networkidle")
                    require(response and response.ok, f"Page did not load: {path}")
                    if scenario.get("text200"):
                        page.add_style_tag(content="html{font-size:200%!important}")
                    if scenario.get("spacing"):
                        page.add_style_tag(content="""
                          *{line-height:1.5!important;letter-spacing:.12em!important;
                            word-spacing:.16em!important}
                          p{margin-block-end:2em!important}
                        """)
                    entry["layout"] = page.evaluate(LAYOUT_PROBE)
                    require(not entry["layout"]["horizontalOverflow"],
                            "Document has horizontal overflow; inspect screenshot and outside-element hints.")
                    require(entry["layout"]["autoplayElements"] == 0,
                            "Unexpected autoplay media in page.")
                    if scenario.get("text200"):
                        require(float(entry["layout"]["rootFontSize"].removesuffix("px")) >= 32,
                                "Root text enlargement was not applied.")
                    if scenario.get("reduced_motion"):
                        require(entry["layout"]["reducedMotion"], "Reduced-motion emulation not active.")
                        require(entry["layout"]["scrollBehavior"] == "auto",
                                "Smooth scrolling remains enabled under reduced motion.")
                    if scenario.get("forced_colors"):
                        require(entry["layout"]["forcedColors"], "Forced-colors emulation not active.")
                    entry["passed"] = True
                except Exception as error:
                    entry["passed"] = False
                    entry["error"] = str(error)
                try:
                    entry["screenshot"] = screenshot(
                        page, f"{scenario['name']}-{label}",
                        "[data-question]" if label == "mission" else None)
                except Exception as error:
                    entry["screenshot_error"] = str(error)
                    entry["passed"] = False
                report["layout_checks"].append(entry)
        finally:
            context.close()


def run_keyboard_check(browser, base, report):
    context = configure_context(browser, base, report,
                                viewport={"width": 1280, "height": 900})
    entry = {"page": "/", "steps": []}
    try:
        page = context.new_page()
        page.goto(base + "/", wait_until="networkidle")
        for _ in range(12):
            page.keyboard.press("Tab")
            # Observe the native Tab result after any native smooth scrolling.
            # Do not focus/scroll a target or change scroll-behavior for this gate.
            focused = page.evaluate(FOCUS_PROBE)
            entry["steps"].append(focused)
            require(focused["settled"] and not focused["focusChangedWhileWaiting"],
                    "Native Tab focus/scroll did not settle on the original control within 2.5 seconds.")
            require(focused["tag"] in {"A", "BUTTON", "INPUT", "SUMMARY"},
                    "Tab did not reach an expected native control.")
            require(focused["focusVisible"] and focused["inViewport"],
                    "Keyboard focus is not focus-visible and in the viewport.")
            require(focused["outlineStyle"] != "none" or focused["boxShadow"] != "none",
                    "Focused control has no computed outline or shadow.")
        entry["passed"] = True
        entry["screenshot"] = screenshot(page, "keyboard-focus", preserve_scroll=True)
    except Exception as error:
        entry["passed"] = False
        entry["error"] = str(error)
        try:
            entry["screenshot"] = screenshot(page, "keyboard-focus-failure", preserve_scroll=True)
        except Exception as screenshot_error:
            entry["screenshot_error"] = str(screenshot_error)
    finally:
        context.close()
    report["keyboard_check"] = entry


def run_quiz_check(browser, base, report):
    data = json.loads((ROOT / "data" / "quick_mission.json").read_text())
    rows = data["questions"]
    context = configure_context(browser, base, report,
                                viewport={"width": 1280, "height": 900})
    entry = {"question_ids": [row["id"] for row in rows], "steps": []}
    try:
        page = context.new_page()
        page.goto(base + "/missions/first-contact/", wait_until="networkidle")
        questions = page.locator("[data-question]")
        require(questions.count() == len(rows), "Rendered question count differs from JSON.")
        progress = page.locator("#quiz-progress")
        first = questions.nth(0)
        first.locator("[data-check]").click()
        require("Choose an answer first" in first.locator("[data-feedback]").inner_text(),
                "Empty selection did not produce guidance.")
        require(first.locator("input").first.evaluate("el => el === document.activeElement"),
                "Empty selection did not focus the first answer.")
        require(progress.inner_text() == f"0 of {len(rows)} questions checked.",
                "Empty selection changed progress.")
        entry["steps"].append("No selection gives guidance and focuses an answer without scoring.")

        wrong = next(choice["id"] for choice in rows[0]["choices"]
                     if choice["id"] != rows[0]["answer"])
        first.locator(f"input[value='{wrong}']").check()
        first.locator("[data-check]").click()
        require(f"The answer is {rows[0]['answer']}" in first.locator("[data-feedback]").inner_text(),
                "Incorrect-answer feedback does not identify the expected answer.")
        require(first.locator("details").evaluate("el => el.open"),
                "Incorrect answer did not reveal the explanation.")
        require(progress.inner_text() == f"1 of {len(rows)} questions checked.",
                "First checked answer did not count exactly once.")
        first.locator(f"input[value='{rows[0]['answer']}']").check()
        require(progress.inner_text() == f"0 of {len(rows)} questions checked.",
                "Changing a checked answer did not invalidate that result.")
        first.locator("[data-check]").click()
        require(first.locator("[data-feedback]").inner_text().startswith("Correct."),
                "Correct replacement did not receive correct feedback.")
        first.locator("[data-check]").click()
        require(progress.inner_text() == f"1 of {len(rows)} questions checked.",
                "Repeated check double-counted a question.")
        entry["steps"].append("Incorrect-to-correct change invalidates and recounts once; repeated checks do not inflate progress.")

        for index, row in enumerate(rows):
            question = questions.nth(index)
            require(question.get_attribute("data-answer") == row["answer"],
                    f"Rendered answer does not match data for {row['id']}.")
            for choice in row["choices"]:
                # The letter must be in the actual accessible name, not aria-hidden.
                require(question.get_by_role("radio", name=f"{choice['id']} {choice['text']}", exact=True).count() == 1,
                        f"Radio name lacks letter and answer for {row['id']}:{choice['id']}.")
            question.locator(f"input[value='{row['answer']}']").check()
            question.locator("[data-check]").click()
        require(page.locator("[data-finish]").is_visible(), "Completion is hidden after all answers.")
        require(page.locator("[data-score]").inner_text() ==
                f"You answered {len(rows)} of {len(rows)} correctly.", "Final all-correct score is wrong.")
        entry["steps"].append("All data-bound answers score correctly; radio accessible names include letters.")
        entry["completion_screenshot"] = screenshot(page, "mission-complete", "[data-finish]")
        completion = page.locator("[data-completion]")
        require(completion.get_attribute("role") == "status" and
                completion.inner_text() == f"Mission complete. You answered {len(rows)} of {len(rows)} correctly.",
                "Completion status does not expose the final score.")

        first.locator(f"input[value='{wrong}']").check()
        require(page.locator("[data-finish]").is_hidden(),
                "Changing a completed answer did not hide completion.")
        require(page.locator("[data-score]").inner_text() == "",
                "Changing a completed answer retained the old score.")
        require(progress.inner_text() == f"{len(rows) - 1} of {len(rows)} questions checked.",
                "Changing a completed answer did not remove exactly one result.")
        require(completion.inner_text() == "", "Changed answer retained the old completion announcement.")
        first.locator("[data-check]").click()
        require(page.locator("[data-score]").inner_text() ==
                f"You answered {len(rows) - 1} of {len(rows)} correctly.", "Mixed-answer score is wrong.")
        require(completion.inner_text() ==
                f"Mission complete. You answered {len(rows) - 1} of {len(rows)} correctly.",
                "Mixed-answer completion status is wrong.")
        entry["steps"].append("Mixed answers produce an accurate score and completion status without moving focus.")
        first.locator(f"input[value='{rows[0]['answer']}']").check()
        first.locator("[data-check]").click()
        require(page.locator("[data-score]").inner_text() ==
                f"You answered {len(rows)} of {len(rows)} correctly.",
                "Rechecking the changed answer did not restore the correct score.")
        entry["steps"].append("Changing a completed answer hides and clears the old score until rechecked.")

        page.locator("[data-reset]").click()
        require(page.locator("[data-question] input:checked").count() == 0, "Reset kept checked answers.")
        require(page.locator("[data-question] details[open]").count() == 0, "Reset left explanations open.")
        require(all(not value.strip() for value in page.locator("[data-feedback]").all_text_contents()),
                "Reset retained feedback.")
        require(page.locator("[data-score]").inner_text() == "", "Reset retained score text.")
        require(completion.inner_text() == "", "Reset retained completion status.")
        require(page.locator("[data-finish]").is_hidden(), "Reset did not hide completion.")
        require(progress.inner_text() == f"0 of {len(rows)} questions checked.", "Reset progress is wrong.")
        require(first.locator("input").first.evaluate("el => el === document.activeElement"),
                "Reset did not return focus to the first answer.")
        entry["steps"].append("Reset clears answers, explanations, feedback, score and progress, then restores focus.")
        entry["passed"] = True
    except Exception as error:
        entry["passed"] = False
        entry["error"] = str(error)
    finally:
        context.close()
    report["quiz_check"] = entry


def run_no_js_check(browser, base, report):
    data = json.loads((ROOT / "data" / "quick_mission.json").read_text())
    context = configure_context(browser, base, report, java_script_enabled=False,
                                viewport={"width": 320, "height": 900})
    entry = {"steps": []}
    try:
        page = context.new_page()
        page.goto(base + "/missions/first-contact/", wait_until="networkidle")
        require(page.locator("[data-check]").first.is_hidden(), "No-JS check controls should stay hidden.")
        for index, row in enumerate(data["questions"]):
            question = page.locator("[data-question]").nth(index)
            summary = question.locator("summary")
            summary.focus()
            summary.press("Enter")
            answer = question.locator(".answer-line")
            require(answer.is_visible(), f"Native details did not open by keyboard for {row['id']}.")
            require(f"Answer {row['answer']}:" in answer.inner_text(), "No-JS answer differs from data.")
            source = question.locator(".source-link a")
            require(source.is_visible() and source.get_attribute("href") == row["source"]["url"],
                    f"No-JS source is absent or incorrect for {row['id']}.")
        entry["steps"].append("All three native details open with Enter and expose the expected answers/sources without JavaScript.")
        entry["screenshot"] = screenshot(page, "mission-no-js", "[data-question]")
        entry["passed"] = True
    except Exception as error:
        entry["passed"] = False
        entry["error"] = str(error)
    finally:
        context.close()
    report["no_js_check"] = entry


def main():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report = {
        "checked_at": datetime.now(ZoneInfo("America/Chicago")).isoformat(),
        "scope": "Owner-run Chromium checks of the built local site; no publishing or source-page requests.",
        "limitations": [
            "Not a full accessibility audit or WCAG conformance claim.",
            "320 CSS pixels simulates narrow reflow; root text enlargement is not actual browser zoom.",
            "Screenshots are bounded viewport samples; inspect them for clipping, reading size and crop quality.",
            "Computed focus styles do not establish human-visible focus quality or screen-reader usability.",
            "Forced colors and reduced motion are browser emulations, not device or operating-system acceptance.",
            "Actual 200/400% zoom, assistive technology, final human visual/content acceptance and real upload previews remain manual.",
        ],
        "blocked_external_requests": [],
        "page_errors": [],
        "layout_checks": [],
    }
    server = None
    server_thread = None
    try:
        # Use this invocation's existing Python environment rather than the qn shebang.
        subprocess.run([sys.executable, str(ROOT / "qn"), "build"], cwd=ROOT, check=True)
        from playwright.sync_api import sync_playwright

        handler = functools.partial(QuietHandler, directory=str(ROOT / "public"))
        server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        server.daemon_threads = True
        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()
        base = f"http://127.0.0.1:{server.server_address[1]}"
        report["origin"] = base
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            try:
                report["browser_version"] = browser.version
                run_layout_checks(browser, base, report)
                run_keyboard_check(browser, base, report)
                run_quiz_check(browser, base, report)
                run_no_js_check(browser, base, report)
            finally:
                browser.close()
        gates = [entry["passed"] for entry in report["layout_checks"]]
        gates.extend(report[name]["passed"] for name in ("keyboard_check", "quiz_check", "no_js_check"))
        report["passed"] = (all(gates) and not report["blocked_external_requests"]
                            and not report["page_errors"])
    except Exception as error:
        report["passed"] = False
        report["operational_error"] = str(error)
        report["traceback"] = traceback.format_exc()
    finally:
        if server is not None:
            server.shutdown()
            server.server_close()
        if server_thread is not None:
            server_thread.join(timeout=5)
        path = REPORT_DIR / "results.json"
        path.write_text(json.dumps(report, indent=2) + "\n")
        print(json.dumps({
            "passed": report["passed"],
            "report": str(path),
            "screenshots": str(REPORT_DIR),
            "layout_cases": len(report["layout_checks"]),
            "failed_layout_cases": [f"{r['scenario']}:{r['page']}"
                                    for r in report["layout_checks"] if not r["passed"]],
            "blocked_external_requests": len(report["blocked_external_requests"]),
            "page_errors": len(report["page_errors"]),
            "operational_error": report.get("operational_error"),
            "scope": "Focused local checks; human accessibility and final visual acceptance remain open.",
        }, indent=2))
    return 0 if report["passed"] else (2 if "operational_error" in report else 1)


if __name__ == "__main__":
    raise SystemExit(main())
