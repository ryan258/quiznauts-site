#!/usr/bin/env python3
"""Save a local, verified source checkpoint without changing Git."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import hashlib
import json
import stat
import zipfile

ROOT = Path(__file__).resolve().parents[1]
FOLDERS = ("assets", "content", "data", "docs", "layouts", "marketing", "scripts", "static")
FILES = ("qn", "hugo.toml", "README.md", "AGENTS.md", "CLAUDE.md", ".gitignore")


def backup(root=ROOT):
    paths = [root / name for name in FILES]
    paths += [path for folder in FOLDERS for path in (root / folder).rglob("*")
              if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
              and not path.name.startswith(".env")]
    paths = sorted(paths)
    if any(path.is_symlink() or not path.resolve().is_relative_to(root.resolve()) for path in paths):
        raise ValueError("Backup source contains a symlink or path outside this project.")
    directory = root / "backups"
    directory.mkdir(exist_ok=True)
    stamp = datetime.now(ZoneInfo("America/Chicago")).strftime("%Y%m%d-%H%M%S-%f")
    target = directory / ("quiznauts-source-" + stamp + ".zip")
    temporary = target.with_suffix(".tmp")
    manifest = {}
    try:
        with zipfile.ZipFile(temporary, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
            for path in paths:
                content = path.read_bytes()
                member = path.relative_to(root).as_posix()
                manifest[member] = hashlib.sha256(content).hexdigest()
                info = zipfile.ZipInfo(member, date_time=(1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = (stat.S_IFREG | stat.S_IMODE(path.stat().st_mode)) << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, content)
            archive.writestr("backup-manifest.json", json.dumps(manifest, indent=2) + "\n")
        with zipfile.ZipFile(temporary) as archive:
            if archive.testzip() or any(hashlib.sha256(archive.read(name)).hexdigest() != digest for name, digest in manifest.items()):
                raise ValueError("Backup verification failed; previous checkpoints were retained.")
        temporary.replace(target)
    finally:
        temporary.unlink(missing_ok=True)
    return {"backup": str(target), "files": len(manifest), "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
            "restore": "Extract into a separate folder, then run python3 qn check there (works even if the extractor drops executable bits). Keep another copy on a separate disk for disk-loss recovery.",
            "git_changed": False}


if __name__ == "__main__":
    print(json.dumps(backup(), indent=2))
