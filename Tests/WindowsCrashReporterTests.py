import json
import os
from pathlib import Path
import subprocess
import sys
import unittest


class WindowsCrashReporterTests(unittest.TestCase):
    def test_exception_report_uses_artifact_override_and_preserves_code(self):
        root = Path(os.environ["HP2_ARTIFACT_DIR"])
        explicit = root / "explicit"
        artifact = root / "artifact-\u03a9"
        working = root / "working"
        for path in (explicit, artifact, working):
            path.mkdir(parents=True, exist_ok=True)
        report = artifact / "crash-report.json"
        if report.exists():
            report.unlink()
        env = os.environ.copy()
        env["HP2_ARTIFACT_DIR"] = str(artifact)
        child = subprocess.run([sys.argv[1], str(explicit)], env=env, cwd=working,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               timeout=20)
        self.assertNotEqual(child.returncode, 0)
        self.assertTrue(report.is_file(), child.stderr.decode(errors="replace"))
        result = json.loads(report.read_text(encoding="utf-8"))
        self.assertEqual(result["reason_code"], "crash.exception")
        self.assertEqual(result["exception_code"], "0xe0424242")
        self.assertNotEqual(result["exception_address"], "0x0")
        self.assertTrue(result["module"])
        self.assertNotIn("\\", result["module"])
        self.assertIn("module_offset", result)
        self.assertEqual(result["frames"], [])
        self.assertFalse((working / "crash-report.json").exists())
        self.assertFalse((explicit / "crash-report.json").exists())

    def test_explicit_directory_without_override(self):
        root = Path(os.environ["HP2_ARTIFACT_DIR"])
        destination = root / "configured"
        working = root / "other-working-directory"
        destination.mkdir(parents=True, exist_ok=True)
        working.mkdir(parents=True, exist_ok=True)
        report = destination / "crash-report.json"
        if report.exists():
            report.unlink()
        env = os.environ.copy()
        env.pop("HP2_ARTIFACT_DIR", None)
        child = subprocess.run([sys.argv[1], str(destination)], env=env, cwd=working,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               timeout=20)
        self.assertNotEqual(child.returncode, 0)
        self.assertTrue(report.is_file(), child.stderr.decode(errors="replace"))
        self.assertEqual(json.loads(report.read_text(encoding="utf-8"))["exception_code"],
                         "0xe0424242")
        self.assertFalse((working / "crash-report.json").exists())

    def test_stack_overflow_writes_exception_report(self):
        root = Path(os.environ["HP2_ARTIFACT_DIR"])
        artifact = root / "stack-overflow"
        artifact.mkdir(parents=True, exist_ok=True)
        report = artifact / "crash-report.json"
        if report.exists():
            report.unlink()
        env = os.environ.copy()
        env["HP2_ARTIFACT_DIR"] = str(artifact)
        child = subprocess.run([sys.argv[1], str(root), "overflow"], env=env,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               timeout=20)
        self.assertNotEqual(child.returncode, 0)
        self.assertTrue(report.is_file(), child.stderr.decode(errors="replace"))
        self.assertEqual(json.loads(report.read_text(encoding="utf-8"))["exception_code"],
                         "0xc00000fd")


if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]])
