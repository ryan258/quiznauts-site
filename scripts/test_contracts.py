"""Targeted regressions for URL, mission and download-integrity corrections."""
from copy import deepcopy
from pathlib import Path
import json
import os
import runpy
import tempfile
import unittest
from unittest.mock import patch
import zipfile
import hashlib
import stat
import subprocess

from content_contract import http_url_error, destination_errors, mission_catalog, validate_mission
from check_site import Page, check_mission, check_archives
import package_kits
from backup_project import backup, FILES

ROOT = Path(__file__).resolve().parents[1]


class ContentContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy = json.loads((ROOT / "data/url_policy.json").read_text())
        cls.sample = json.loads((ROOT / "data/quick_mission.json").read_text())

    def test_public_urls_reject_local_malformed_and_credential_values(self):
        invalid = ["not a URL", "ftp://quiznauts.org/", "https://user:secret@quiznauts.org/", "https://quiznauts.org:99999/",
                   "https://127.0.0.1/", "https://[::1]/", "https://192.168.1.1/", "https://example.test/",
                   "https://example.org/", "https://host.local/", "https://localhost./", "https://quiznauts.org/ bad", None, 3]
        for value in invalid:
            with self.subTest(value=value): self.assertTrue(http_url_error(value, self.policy))
        for value in ("https://www.youtube.com/@quiznauts", "https://Quiznauts.org/site/", "http://quiznauts.org:8080/"):
            with self.subTest(value=value): self.assertEqual(http_url_error(value, self.policy), "")
        self.assertTrue(http_url_error("https://quiznauts.org/?draft=1", self.policy, base=True))

    def test_destinations_keep_empty_values_but_reject_whitespace_and_duplicates(self):
        self.assertFalse(destination_errors([{"id": "youtube", "url": ""}], self.policy))
        self.assertTrue(destination_errors([{"id": "youtube", "url": " "}], self.policy))
        self.assertTrue(destination_errors([{"id": "x", "url": ""}, {"id": "x", "url": ""}], self.policy))

    def test_malformed_mission_data_is_rejected(self):
        self.assertEqual(validate_mission(self.sample, self.policy), [])
        for change in (lambda d: d["questions"].append(deepcopy(d["questions"][0])),
                       lambda d: d["questions"][0].update(answer="D"),
                       lambda d: d["questions"][0].update(source=None),
                       lambda d: d["questions"][0]["choices"][1].update(text="Atlantic"),
                       lambda d: d["questions"][0].update(choices=[None]),
                       lambda d: d.update(questions=[])):
            data = deepcopy(self.sample); change(data)
            self.assertTrue(validate_mission(data, self.policy))

    def test_registry_rejects_identity_mismatch_and_path_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); (root / "data").mkdir()
            (root / "data/missions.json").write_text(json.dumps({"different-mission": "quick_mission"}))
            (root / "data/quick_mission.json").write_text(json.dumps(self.sample))
            with self.assertRaisesRegex(ValueError, "identity"): mission_catalog(root)
            (root / "data/missions.json").write_text(json.dumps({"first-contact": "../private"}))
            with self.assertRaisesRegex(ValueError, "simple names"): mission_catalog(root)

    def test_render_contract_detects_wrong_prompt_choices_answer_and_source(self):
        # Deliberately independent one-question HTML fixture, not the Hugo template.
        mission = {"id": "fixture", "questions": [{"id": "q-one", "prompt": "Pick a letter?", "choices": [{"id": c, "text": t} for c, t in zip("ABC", ["Alpha", "Beta", "Gamma"])], "answer": "B", "explanation": "Beta is correct.", "source": {"title": "Source", "url": "https://nasa.gov/"}}]}
        html = '<div data-quiz data-mission-id="fixture"><section data-question data-question-id="q-one" data-answer="B"><h2>Pick a letter?</h2>'
        html += ''.join(f'<label><input type="radio" name="q-one" value="{c}"><span>{c}</span><span>{t}</span></label>' for c,t in zip("ABC",["Alpha","Beta","Gamma"]))
        html += '<p class="answer-line">Answer B: Beta</p><p data-explanation>Beta is correct.</p><a href="https://nasa.gov/">Source ↗</a></section><p data-completion role="status" aria-live="polite"></p></div>'
        for text, expected in [(html, False), (html.replace('data-answer="B"', 'data-answer="A"'), True),
                               (html.replace('Pick a letter?', 'Wrong prompt'), True), (html.replace('>Gamma<', '>Delta<'), True),
                               (html.replace('https://nasa.gov/', 'https://noaa.gov/'), True), (html.replace('Beta is correct.', 'Wrong explanation.'), True)]:
            page=Page();page.feed(text);failures=[]
            check_mission(page, mission, lambda valid, message: failures.append(message) if not valid else None)
            self.assertEqual(bool(failures), expected, failures)

    def test_artwork_import_has_no_render_or_write_side_effects(self):
        with patch("subprocess.run") as run, patch("pathlib.Path.write_text") as write:
            runpy.run_path(str(ROOT / "scripts/generate-art.py"), run_name="import_probe")
            run.assert_not_called();write.assert_not_called()

    def test_failed_native_render_retains_saved_artwork(self):
        paths = [p for p in (ROOT / "static/marketing").rglob("*") if p.suffix in {".png", ".svg"}]
        before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
        namespace = runpy.run_path(str(ROOT / "scripts/generate-art.py"), run_name="failure_probe")
        with patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "swift")):
            with self.assertRaises(subprocess.CalledProcessError): namespace["main"]()
        self.assertEqual(before, {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})


class BackupContracts(unittest.TestCase):
    def test_source_checkpoint_preserves_pngs_modes_and_excludes_runtime_and_credentials(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in FILES: (root / name).write_text("source")
            (root / "qn").chmod(0o755)
            (root / "static/brand/png").mkdir(parents=True)
            (root / "static/brand/png/original.png").write_bytes(b"preserved")
            (root / ".env").write_text("private")
            (root / "reports").mkdir(); (root / "reports/browser.png").write_bytes(b"derived")
            result = backup(root)
            with zipfile.ZipFile(result["backup"]) as archive:
                self.assertEqual(archive.read("static/brand/png/original.png"), b"preserved")
                self.assertNotIn(".env", archive.namelist())
                self.assertNotIn("reports/browser.png", archive.namelist())
                self.assertTrue((archive.getinfo("qn").external_attr >> 16) & stat.S_IXUSR)
                manifest = json.loads(archive.read("backup-manifest.json"))
                self.assertTrue(all(hashlib.sha256(archive.read(name)).hexdigest() == digest for name,digest in manifest.items()))


class ArchiveContracts(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for folder in ("data", "docs", "static/marketing/svg", "static/marketing/png", "static/marketing/webp", "static/brand/svg", "static/brand/webp", "static/marketing/downloads"):
            (self.root / folder).mkdir(parents=True, exist_ok=True)
        for kind in ("svg", "png", "webp"):
            (self.root / f"static/marketing/{kind}/asset.{kind}").write_bytes(kind.encode())
        (self.root / "static/brand/svg/mascot.svg").write_bytes(b"original")
        (self.root / "static/brand/webp/mascot.webp").write_bytes(b"webcopy")
        (self.root / "data/marketing.json").write_text(json.dumps({"assets": [{k: f"/marketing/{k}/asset.{k}" for k in ("svg", "png", "webp")}]}))
        (self.root / "docs/brand-source.json").write_text(json.dumps({"library_version": "1.4", "files": [{"path": "static/brand/svg/mascot.svg"}]}))
        (self.root / "docs/image-optimization.json").write_text(json.dumps({"files": [{"source": "static/brand/png/mascot.png", "webp": "static/brand/webp/mascot.webp"}]}))
        self.dest = self.root / "static/marketing/downloads"
        with patch.object(package_kits, "DEST", self.dest):
            for args in package_kits.kit_specs(self.root): package_kits.write_zip(*args)

    def failures(self):
        failures=[]
        check_archives(self.root, lambda valid, message: failures.append(message) if not valid else None)
        return failures

    def test_archives_are_current_and_do_not_sweep_unrecorded_files(self):
        (self.root / "static/brand/private-reference.jpg").write_bytes(b"not public")
        self.assertFalse(self.failures())
        brand = package_kits.kit_specs(self.root)[1]
        self.assertNotIn("private-reference.jpg", [member for _, member in brand[1]])

    def test_rebuild_is_stable_when_source_timestamps_change(self):
        target = self.dest / "quiznauts-social-kit.zip"
        original, mtime = target.read_bytes(), target.stat().st_mtime_ns
        source = self.root / "static/marketing/svg/asset.svg"
        os.utime(source, (1_000_000_000, 1_000_000_000))
        with patch.object(package_kits, "DEST", self.dest): package_kits.write_zip(*package_kits.kit_specs(self.root)[0])
        self.assertEqual(target.read_bytes(), original)
        self.assertEqual(target.stat().st_mtime_ns, mtime)

    def test_missing_archive_and_crc_valid_stale_member_are_rejected(self):
        target = self.dest / "quiznauts-social-kit.zip"
        with zipfile.ZipFile(target) as archive: members = {n:archive.read(n) for n in archive.namelist()}
        members['quiznauts-social-kit/png/asset.png'] = b'stale but valid CRC'
        with zipfile.ZipFile(target, 'w') as archive:
            for name, content in members.items(): archive.writestr(name,content)
        self.assertTrue(any('Stale ZIP asset' in f for f in self.failures()))
        target.unlink()
        self.assertTrue(any('Missing required ZIP' in f for f in self.failures()))

    def test_missing_member_and_stale_manifest_are_rejected(self):
        target = self.dest / "quiznauts-social-kit.zip"
        with zipfile.ZipFile(target) as archive: members = {n:archive.read(n) for n in archive.namelist()}
        del members['quiznauts-social-kit/png/asset.png']
        members['quiznauts-social-kit/manifest.json'] = b'{}'
        with zipfile.ZipFile(target, 'w') as archive:
            for name, content in members.items(): archive.writestr(name,content)
        failures=self.failures()
        self.assertTrue(any('Wrong ZIP members' in f for f in failures))
        self.assertTrue(any('Stale ZIP manifest' in f for f in failures))


if __name__ == "__main__":
    unittest.main()
