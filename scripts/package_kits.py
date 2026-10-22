#!/usr/bin/env python3
"""Create deterministic local download kits from recorded public assets."""
from pathlib import Path
import hashlib
import json
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "static/marketing/downloads"


def recorded_file(root, relative):
    path = (root / relative).resolve()
    if not path.is_relative_to((root / "static").resolve()) or not path.is_file():
        raise ValueError("Missing or unsafe public asset: " + relative)
    return path


def kit_specs(root=ROOT):
    data = json.loads((root / "data/marketing.json").read_text())
    files, receipts = [], []
    for asset in data["assets"]:
        for key in ("svg", "png", "webp"):
            relative = asset[key].lstrip("/")
            if not relative.startswith("marketing/" + key + "/"):
                raise ValueError("Wrong marketing export path: " + relative)
            path = recorded_file(root, "static/" + relative)
            member = key + "/" + path.name
            files.append((path, member))
            receipts.append({"file": member, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    social_manifest = {"brand": "Quiznauts", "direction": "Mr. Big / Atomic Advertising",
                       "assets": data["assets"], "files": receipts,
                       "scope": "Local artwork and templates; profile ownership, publication and platform crop acceptance are separate."}
    brand_receipt = json.loads((root / "docs/brand-source.json").read_text())
    webp_receipt = json.loads((root / "docs/image-optimization.json").read_text())
    # Only recorded public files enter the brand kit, never an arbitrary new file.
    brand_paths = [row["path"] for row in brand_receipt["files"]]
    brand_paths += [row["webp"] for row in webp_receipt["files"] if row["source"].startswith("static/brand/")]
    brand_files = []
    for relative in sorted(brand_paths):
        path = recorded_file(root, relative)
        member = path.relative_to((root / "static/brand").resolve()).as_posix()
        brand_files.append((path, member))
    brand_manifest = {"brand": "Quiznauts", "source_library": brand_receipt["library_version"],
                      "files": [{"file": member, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()} for path, member in brand_files]}
    return [
        ("quiznauts-social-kit", files,
         "Quiznauts social kit. SVG masters, full-size PNG exports and lossless WebP copies. See manifest.json for dimensions, intended properties and safe-area guides.\n"
         "Question/answer cards must stay tied to their recorded factual source. Template art does not establish that a matching video is published.\n"
         "Crop guides are production guides; inspect the actual upload on the chosen platform before publishing. No blanket reuse license is asserted here.", social_manifest),
        ("quiznauts-brand-kit", brand_files,
         "Quiznauts brand kit / production library v1.4. Clean SVG artwork, mascot PNG exports and lossless WebP copies.\n"
         "Preserve Mr. Big's round paws and feet, compact proportions and asymmetric temple patch. Never mirror his head. Keep essential text high contrast.\n"
         "The actual toy reference photo, private source records and question banks are not included. Distribution terms remain an owner decision.", brand_manifest),
    ]


def write_zip(name, files, note, manifest):
    DEST.mkdir(parents=True, exist_ok=True)
    target = DEST / (name + ".zip")
    members = [(member, path.read_bytes()) for path, member in files]
    members += [("README.txt", (note + "\n").encode()),
                ("manifest.json", (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode())]
    if len({member for member, _ in members}) != len(members):
        raise ValueError("Duplicate ZIP member: " + name)
    with tempfile.NamedTemporaryFile(dir=DEST, suffix=".tmp", delete=False) as stream:
        temporary = Path(stream.name)
    try:
        with zipfile.ZipFile(temporary, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for member, content in sorted(members):
                info = zipfile.ZipInfo(name + "/" + member, date_time=(1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                archive.writestr(info, content, compresslevel=9)
        with zipfile.ZipFile(temporary) as archive:
            if archive.testzip() is not None:
                raise ValueError("ZIP integrity check failed: " + name)
        if not target.exists() or target.read_bytes() != temporary.read_bytes():
            temporary.replace(target)
        return target.stat().st_size
    finally:
        temporary.unlink(missing_ok=True)


def main():
    try:
        sizes = {name: write_zip(name, files, note, manifest) for name, files, note, manifest in kit_specs()}
    except (OSError, ValueError, KeyError) as error:
        raise SystemExit("Cannot build download kits: " + str(error)) from error
    print(json.dumps({"social_kit_bytes": sizes["quiznauts-social-kit"],
                      "brand_kit_bytes": sizes["quiznauts-brand-kit"], "zip_integrity": "pass"}, indent=2))


if __name__ == "__main__":
    main()
