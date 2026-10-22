#!/usr/bin/env python3
"""Regenerate lossless WebP copies locally. Requires cwebp only for authoring."""
from pathlib import Path
import hashlib
import json
import shutil
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "docs/image-optimization.json"
OPTIONS = ["-lossless", "-z", "9", "-exact", "-metadata", "none"]


def png_sources(root):
    return sorted(path for folder in ("brand/png", "marketing/png")
                  for path in (root / "static" / folder).rglob("*.png"))


def webp_path(source):
    # Only replace the format directory; keep nested mascot paths intact.
    parts = list(source.parts)
    parts[parts.index("png")] = "webp"
    return Path(*parts).with_suffix(".webp")


def lossless_dimensions(raw):
    """Read the VP8L dimensions, including files with an extended RIFF header."""
    if raw[:4] != b"RIFF" or raw[8:12] != b"WEBP" or len(raw) != int.from_bytes(raw[4:8], "little") + 8:
        raise ValueError("Invalid WebP RIFF container")
    offset = 12
    while offset + 8 <= len(raw):
        size = int.from_bytes(raw[offset + 4:offset + 8], "little")
        payload = raw[offset + 8:offset + 8 + size]
        if len(payload) != size:
            raise ValueError("Truncated WebP chunk")
        if raw[offset:offset + 4] == b"VP8L" and len(payload) >= 5 and payload[0] == 0x2f:
            bits = int.from_bytes(payload[1:5], "little")
            return ((bits & 0x3fff) + 1, ((bits >> 14) & 0x3fff) + 1)
        offset += 8 + size + (size & 1)
    raise ValueError("Expected lossless VP8L image")


def main():
    encoder = shutil.which("cwebp")
    if not encoder:
        raise SystemExit("Image authoring needs cwebp (libwebp). Existing exports still build without it. See docs/visual-assets.md.")
    sources = png_sources(ROOT)
    if not sources:
        raise SystemExit("No source PNGs found; existing exports were retained.")
    records, pending = [], []
    with tempfile.TemporaryDirectory(prefix="quiznauts-webp-") as directory:
        for index, source in enumerate(sources):
            raw = source.read_bytes()
            if raw[:8] != b"\x89PNG\r\n\x1a\n" or len(raw) < 24:
                raise SystemExit("Invalid source PNG: " + str(source))
            dimensions = struct.unpack(">II", raw[16:24])
            target = webp_path(source)
            temporary = Path(directory) / f"{index}.webp"
            subprocess.run([encoder, "-quiet", *OPTIONS, str(source), "-o", str(temporary)], check=True)
            encoded = temporary.read_bytes()
            if lossless_dimensions(encoded) != dimensions:
                raise SystemExit("WebP dimensions differ from source: " + str(source))
            records.append({"source": source.relative_to(ROOT).as_posix(),
                            "webp": target.relative_to(ROOT).as_posix(),
                            "width": dimensions[0], "height": dimensions[1],
                            "source_bytes": len(raw), "webp_bytes": len(encoded),
                            "source_sha256": hashlib.sha256(raw).hexdigest(),
                            "webp_sha256": hashlib.sha256(encoded).hexdigest()})
            pending.append((temporary, target))
        # Encode every file successfully before replacing any project exports.
        for temporary, target in pending:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(temporary, target)
    receipt = {"encoding": "lossless WebP; exact RGBA; original backgrounds and alpha retained",
               "encoder": "cwebp", "encoder_version": subprocess.check_output([encoder, "-version"], text=True).strip(),
               "options": OPTIONS, "files": records}
    RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
    original = sum(row["source_bytes"] for row in records)
    optimized = sum(row["webp_bytes"] for row in records)
    print(json.dumps({"webp_images": len(records), "png_bytes": original, "webp_bytes": optimized,
                      "saved_percent": round(100 * (1 - optimized / original), 1),
                      "receipt": "docs/image-optimization.json"}, indent=2))


if __name__ == "__main__":
    main()
