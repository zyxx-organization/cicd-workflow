"""Execute the workflow shell against isolated repositories, never a service."""
import os
from pathlib import Path
import subprocess
import tempfile
import textwrap
import unittest


@unittest.skipIf(os.name == "nt", "Release shell runs on Linux")
class DeploymentTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.origin = self.root / "origin"
        self.checkout = self.root / "checkout"
        self.git("init", "-b", "main", str(self.origin))
        self.git("-C", str(self.origin), "config", "user.email", "test@example.invalid")
        self.git("-C", str(self.origin), "config", "user.name", "test")
        self.old = self.commit("old")
        self.git("clone", str(self.origin), str(self.checkout))
        self.checked = self.commit("checked")
        self.newest = self.commit("untested-newer")
        workflow = (Path(__file__).resolve().parents[1] / ".github/workflows/deploy.yml").read_text()
        self.script = self.root / "deploy.sh"
        self.script.write_text(textwrap.dedent(workflow.split("        run: |\n", 1)[1]))

    def git(self, *args):
        return subprocess.check_output(["git", *args], text=True, stderr=subprocess.DEVNULL).strip()

    def commit(self, value):
        (self.origin / "version.txt").write_text(value)
        self.git("-C", str(self.origin), "add", "version.txt")
        self.git("-C", str(self.origin), "commit", "-m", value)
        return self.git("-C", str(self.origin), "rev-parse", "HEAD")

    def run_release(self, **changes):
        env = dict(os.environ, PROJECT_NAME="test", PROJECT_PATH=str(self.checkout),
                   BRANCH="main", REVISION=self.checked, SERVICE_NAME="test",
                   DEPLOY_COMMAND='test "$(cat version.txt)" = checked',
                   ROLLBACK_COMMAND='test "$(cat version.txt)" = old; touch restored',
                   SMOKE_COMMAND="", HEALTHCHECK_URL="")
        env.update(changes)
        return subprocess.run(["bash", str(self.script)], env=env, capture_output=True, text=True)

    def test_deploys_checked_commit_even_when_branch_has_advanced(self):
        result = self.run_release()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.git("-C", str(self.checkout), "rev-parse", "HEAD"), self.checked)

    def test_deploy_failure_restores_old_code_but_keeps_data(self):
        (self.checkout / "personal.db").write_bytes(b"do-not-change")
        result = self.run_release(DEPLOY_COMMAND="exit 7")
        self.assertEqual(result.returncode, 7)
        self.assertEqual(self.git("-C", str(self.checkout), "rev-parse", "HEAD"), self.old)
        self.assertTrue((self.checkout / "restored").exists())
        self.assertEqual((self.checkout / "personal.db").read_bytes(), b"do-not-change")

    def test_smoke_failure_also_restores_previous_code(self):
        result = self.run_release(SMOKE_COMMAND="exit 9")
        self.assertEqual(result.returncode, 9)
        self.assertTrue((self.checkout / "restored").exists())

    def test_local_changes_are_preserved_and_deployment_refused(self):
        (self.checkout / "version.txt").write_text("user-edit")
        self.assertNotEqual(self.run_release().returncode, 0)
        self.assertEqual((self.checkout / "version.txt").read_text(), "user-edit")

    def test_mutable_revision_is_rejected(self):
        self.assertNotEqual(self.run_release(REVISION="main").returncode, 0)
        self.assertEqual(self.git("-C", str(self.checkout), "rev-parse", "HEAD"), self.old)


if __name__ == "__main__":
    unittest.main()
