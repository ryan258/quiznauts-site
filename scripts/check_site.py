#!/usr/bin/env python3
"""Focused source/generated-site contracts; no browser or network requests."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urljoin, urlsplit
import argparse
import hashlib
import json
import struct
import xml.etree.ElementTree as ET
import zipfile
from site_config import load_config
from content_contract import content_errors, http_url_error, mission_catalog, read_json
from optimize_images import lossless_dimensions, png_sources, webp_path
from package_kits import kit_specs, recorded_file

ROOT = Path(__file__).resolve().parents[1]
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


def normalized(text):
    return " ".join(text.split())


class Node:
    def __init__(self, tag, attrs, parent):
        self.tag, self.attrs, self.parent = tag, attrs, parent
        self.parts = []

    @property
    def text(self):
        return normalized("".join(self.parts))

    def inside(self, ancestor):
        parent = self.parent
        while parent is not None:
            if parent is ancestor:
                return True
            parent = parent.parent
        return False


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.refs, self.images, self.robots = [], [], [], []
        self.h1 = self.main = self.title = 0
        self.lang = ""
        self.nodes, self.stack = [], []

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        node = Node(tag, data, self.stack[-1] if self.stack else None)
        self.nodes.append(node)
        if tag not in VOID_TAGS:
            self.stack.append(node)
        if tag == "html": self.lang = data.get("lang", "")
        if tag == "h1": self.h1 += 1
        if tag == "main": self.main += 1
        if tag == "title": self.title += 1
        if "id" in data: self.ids.append(data["id"])
        if tag == "img": self.images.append(data)
        if tag == "meta" and data.get("name") == "robots": self.robots.append(data.get("content", ""))
        for key in ("href", "src", "poster"):
            if key in data: self.refs.append(data[key])

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        for node in self.stack:
            node.parts.append(data)

    def select(self, tag=None, attribute=None, within=None):
        return [node for node in self.nodes if (tag is None or node.tag == tag)
                and (attribute is None or attribute in node.attrs)
                and (within is None or node.inside(within))]


def check_mission(page, mission, require):
    quizzes = page.select(attribute="data-quiz")
    identity = mission["id"]
    require(len(quizzes) == 1 and quizzes[0].attrs.get("data-mission-id") == identity,
            "Rendered mission identity mismatch: " + identity)
    questions = page.select(attribute="data-question")
    require(len(questions) == len(mission["questions"]), "Rendered question count mismatch: " + identity)
    for node, row in zip(questions, mission["questions"]):
        label = identity + "/" + row["id"]
        require(node.attrs.get("data-question-id") == row["id"] and node.attrs.get("data-answer") == row["answer"], "Rendered answer/identity mismatch: " + label)
        headings = page.select("h2", within=node)
        require(len(headings) == 1 and headings[0].text == normalized(row["prompt"]), "Rendered prompt mismatch: " + label)
        inputs = page.select("input", within=node)
        require([(n.attrs.get("type"), n.attrs.get("name"), n.attrs.get("value")) for n in inputs] ==
                [("radio", row["id"], c["id"]) for c in row["choices"]], "Rendered radio identity mismatch: " + label)
        require([[n.text for n in page.select("span", within=choice)] for choice in page.select("label", within=node)] ==
                [[c["id"], normalized(c["text"])] for c in row["choices"]], "Rendered choices mismatch: " + label)
        explanations = page.select(attribute="data-explanation", within=node)
        require(len(explanations) == 1 and explanations[0].text == normalized(row["explanation"]), "Rendered explanation mismatch: " + label)
        answers = [n for n in page.select("p", within=node) if "answer-line" in n.attrs.get("class", "").split()]
        correct = next(c["text"] for c in row["choices"] if c["id"] == row["answer"])
        require(len(answers) == 1 and answers[0].text == normalized(f"Answer {row['answer']}: {correct}"), "Rendered reveal mismatch: " + label)
        sources = page.select("a", within=node)
        require(len(sources) == 1 and sources[0].attrs.get("href") == row["source"]["url"] and
                sources[0].text.removesuffix(" ↗") == normalized(row["source"]["title"]), "Rendered source mismatch: " + label)
    completion = page.select(attribute="data-completion")
    require(len(completion) == 1 and completion[0].attrs.get("role") == "status" and completion[0].attrs.get("aria-live") == "polite", "Missing completion status: " + identity)


def check_archives(root, require):
    for name, files, note, expected in kit_specs(root):
        path = root / "static/marketing/downloads" / (name + ".zip")
        require(path.is_file(), "Missing required ZIP: " + name)
        if not path.is_file(): continue
        try:
            with zipfile.ZipFile(path) as archive:
                prefix = name + "/"
                expected_names = {prefix + member for _, member in files} | {prefix + "manifest.json", prefix + "README.txt"}
                require(len(archive.namelist()) == len(expected_names) and set(archive.namelist()) == expected_names, "Wrong ZIP members: " + name)
                require(archive.testzip() is None, "Corrupt ZIP: " + name)
                require(json.loads(archive.read(prefix + "manifest.json")) == expected, "Stale ZIP manifest: " + name)
                require(archive.read(prefix + "README.txt").decode() == note + "\n", "Stale ZIP note: " + name)
                for source, member in files:
                    require(archive.read(prefix + member) == source.read_bytes(), "Stale ZIP asset: " + name + "/" + member)
        except (OSError, ValueError, KeyError, zipfile.BadZipFile) as error:
            require(False, "Cannot verify ZIP " + name + ": " + str(error))


def check_feeds(public, pages, base_url, require):
    for route, section in (("index.xml", "field-notes"), ("field-notes/index.xml", "field-notes"), ("missions/index.xml", "missions")):
        path = public / route
        require(path.is_file(), "Missing RSS feed: " + route)
        if not path.is_file(): continue
        try:
            feed = ET.parse(path).getroot()
            candidates = [(p, page) for p, page in pages.items() if p.relative_to(public).parts[0] == section and p != public / section / "index.html"]
            expected = {(page.select("h1")[0].text, urljoin(base_url, p.relative_to(public).as_posix().removesuffix("index.html"))) for p, page in candidates}
            items = feed.findall("channel/item")
            require(len(items) == len(expected) and {(i.findtext("title"), i.findtext("link")) for i in items} == expected, "Wrong RSS entries: " + route)
            title = "Quiznauts Field Notes" if route == "index.xml" else pages[public / section / "index.html"].select("h1")[0].text + " · Quiznauts"
            require(feed.findtext("channel/title") == title, "Wrong RSS title: " + route)
            require(feed.find("channel/{http://www.w3.org/2005/Atom}link").get("href") == urljoin(base_url, route), "Wrong RSS self link: " + route)
        except (OSError, ET.ParseError, AttributeError, KeyError, IndexError) as error:
            require(False, "Invalid RSS feed " + route + ": " + str(error))


def source_fingerprint(root):
    paths = [root / "qn", root / "hugo.toml", root / "docs/brand-source.json", root / "docs/image-optimization.json"]
    paths += [p for folder in ("assets", "content", "data", "layouts", "scripts", "static") for p in (root / folder).rglob("*")
              if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"]
    digest = hashlib.sha256()
    for path in sorted(paths):
        digest.update(path.relative_to(root).as_posix().encode() + b"\0" + hashlib.sha256(path.read_bytes()).digest())
    return {"sha256": digest.hexdigest(), "input_files": len(paths)}


def check(public, base_url, config=None, report_path=None):
    public = public.resolve()
    failures = []
    def require(value, message):
        if not value: failures.append(message)
    policy = read_json(ROOT / "data/url_policy.json")
    problems = content_errors(ROOT)
    if problems:
        raise ValueError("Invalid source content: " + "; ".join(problems))
    base = urlsplit(base_url)
    prefix = base.path.rstrip("/")
    pages = {}
    for path in sorted(public.rglob("*.html")):
        parsed = Page(); parsed.feed(path.read_text())
        pages[path.resolve()] = parsed
        require(parsed.lang, str(path) + ": missing document language")
        require(parsed.h1 == 1 and parsed.main == 1 and parsed.title == 1, str(path) + ": expected one h1/main/title")
        require(len(parsed.ids) == len(set(parsed.ids)), str(path) + ": duplicate ids")
        for image in parsed.images:
            require("alt" in image and image.get("width") and image.get("height"), str(path) + ": image lacks alt/dimensions")
    for route in ("index.html", "missions/first-contact/index.html", "media/index.html", "links/index.html", "field-notes/index.html", "site-notes/index.html"):
        require((public / route) in pages, "Missing required generated page: " + route)
    count = 0
    cfg = config or load_config(ROOT)
    indexable = cfg["params"].get("indexable") is True
    public_mode = indexable and not http_url_error(base_url, policy, base=True)
    require(not indexable or public_mode, "Indexable configuration needs a valid public HTTP(S) base URL")
    for path, page in pages.items():
        route = path.relative_to(public).as_posix()
        current = urljoin(base_url, route.removesuffix("index.html"))
        for reference in page.refs:
            require(reference not in {"", "#"}, str(path) + ": empty/dead link")
            url = urlsplit(urljoin(current, reference))
            if url.scheme in {"mailto", "tel", "data"}: continue
            require(url.scheme in {"http", "https", ""}, str(path) + ": unsupported URL scheme")
            if url.netloc and url.netloc != base.netloc: continue
            target_path = unquote(url.path)
            if prefix:
                require(target_path == prefix or target_path.startswith(prefix + "/"), str(path) + ": link escapes configured base path: " + reference)
                if target_path.startswith(prefix): target_path = target_path[len(prefix):]
            target = (public / target_path.lstrip("/")).resolve()
            require(target.is_relative_to(public), str(path) + ": link escapes output directory")
            if target.is_dir(): target /= "index.html"
            require(target.is_file(), str(path) + ": missing local target " + reference)
            if target in pages and url.fragment:
                require(unquote(url.fragment) in pages[target].ids, str(path) + ": missing fragment " + reference)
            count += 1
        canonical = [n for n in page.select("link") if n.attrs.get("rel") == "canonical"]
        social = [n for n in page.select("meta") if n.attrs.get("property", "").startswith("og:")]
        if public_mode:
            require(len(canonical) == 1 and canonical[0].attrs.get("href") == current, str(path) + ": canonical mismatch")
            require(not any("noindex" in value for value in page.robots), str(path) + ": public page has noindex")
            properties = {n.attrs["property"]: n.attrs.get("content", "") for n in social}
            require(all(properties.get(k) for k in ("og:image", "og:image:alt", "og:image:width", "og:image:height")), str(path) + ": incomplete image metadata")
        else:
            require(any("noindex" in value for value in page.robots) and not canonical and not social, str(path) + ": preview indexing metadata is unsafe")
        for node in page.nodes:
            if node.tag == "script" and node.attrs.get("src") or node.tag == "link" and node.attrs.get("rel") == "stylesheet":
                require(bool(node.attrs.get("integrity")), str(path) + ": generated asset lacks fingerprint integrity")
    robots = public / "robots.txt"
    require(robots.is_file(), "Missing robots.txt")
    if robots.is_file():
        require(("Allow: /" in robots.read_text() and "Disallow: /" not in robots.read_text()) if public_mode else "Disallow: /" in robots.read_text(), "Robots policy does not match indexing mode")
    catalog = mission_catalog(ROOT)
    rendered = []
    for page in pages.values():
        for quiz in page.select(attribute="data-quiz"):
            identity = quiz.attrs.get("data-mission-id")
            rendered.append(identity)
            require(identity in catalog, "Unregistered rendered mission: " + str(identity))
            if identity in catalog: check_mission(page, catalog[identity], require)
    require(len(rendered) == len(catalog) and set(rendered) == set(catalog), "Registered missions must each have exactly one rendered page")
    check_feeds(public, pages, base_url, require)
    data = read_json(ROOT / "data/marketing.json")
    for item in data["assets"]:
        png = recorded_file(ROOT, "static/" + item["png"].lstrip("/"))
        raw = png.read_bytes()
        require(raw[:8] == b"\x89PNG\r\n\x1a\n" and len(raw) >= 24 and struct.unpack(">II", raw[16:24]) == (item["width"], item["height"]), "Wrong export dimensions: " + item["id"])
        require(item.get("webp") == "/" + webp_path(png).relative_to(ROOT / "static").as_posix(), "Wrong WebP path: " + item["id"])
    receipt = read_json(ROOT / "docs/image-optimization.json")
    sources = {p.relative_to(ROOT).as_posix() for p in png_sources(ROOT)}
    require(len(receipt["files"]) == len(sources) and {r["source"] for r in receipt["files"]} == sources, "WebP receipt must cover every source PNG; run ./qn images")
    for row in receipt["files"]:
        source = recorded_file(ROOT, row["source"])
        target = ROOT / row["webp"]
        require(target == webp_path(source), "Wrong WebP destination: " + row["webp"])
        require(target.is_file(), "Missing WebP: " + row["webp"] + "; run ./qn images")
        if not target.is_file(): continue
        raw, encoded = source.read_bytes(), target.read_bytes()
        require(hashlib.sha256(raw).hexdigest() == row["source_sha256"], "PNG changed; run ./qn images: " + row["source"])
        require(hashlib.sha256(encoded).hexdigest() == row["webp_sha256"], "WebP differs from receipt: " + row["webp"])
        try:
            require(lossless_dimensions(encoded) == struct.unpack(">II", raw[16:24]) == (row["width"], row["height"]), "Wrong WebP dimensions: " + row["webp"])
        except ValueError as error:
            require(False, row["webp"] + ": " + str(error))
    brand = read_json(ROOT / "docs/brand-source.json")
    for row in brand["files"]:
        require(hashlib.sha256(recorded_file(ROOT, row["path"]).read_bytes()).hexdigest() == row["sha256"], "Brand source hash mismatch: " + row["path"])
    actual_brand = {p.relative_to(ROOT).as_posix() for p in (ROOT / "static/brand").rglob("*") if p.suffix in {".png", ".svg"}}
    require(actual_brand == {r["path"] for r in brand["files"]}, "Unrecorded/missing original brand asset")
    for path in (ROOT / "static").rglob("*.svg"):
        doc = ET.parse(path).getroot()
        ids = [e.get("id") for e in doc.iter() if e.get("id")]
        require(len(ids) == len(set(ids)), "Duplicate SVG ids: " + str(path))
        require(not {e.tag.split("}")[-1] for e in doc.iter()} & {"script", "foreignObject", "image"}, "Unexpected active/raster SVG content: " + str(path))
        for element in doc.iter():
            require(not any(("href" in key and not value.startswith("#")) or key.lower().startswith("on") for key, value in element.attrib.items()), "Active/external SVG resource: " + str(path))
    check_archives(ROOT, require)
    report = {"scope": "Local source/generated-site contracts; no browser/AT/human acceptance", "passed": not failures,
              "base_url": base_url, "indexable": public_mode, "pages": len(pages), "local_references": count,
              "marketing_assets": len(data["assets"]), "webp_images": len(receipt["files"]), "brand_files": len(brand["files"]),
              "missions": len(catalog), "sample_questions": 3, "failures": failures, "browser_run": False, "source_snapshot": source_fingerprint(ROOT)}
    if report_path:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--public", type=Path, default=ROOT / "public")
    parser.add_argument("--base-url")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        raise SystemExit(check(args.public, args.base_url or load_config(ROOT)["baseURL"], report_path=args.report))
    except (OSError, ValueError, KeyError, TypeError, ET.ParseError, struct.error) as error:
        report = {"passed": False, "failures": [str(error)], "browser_run": False}
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(report, indent=2) + "\n")
        print(json.dumps(report, indent=2))
        raise SystemExit(1)
