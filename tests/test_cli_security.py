import unittest
import subprocess
import sys
import os

class TestCLISecurity(unittest.TestCase):
    def test_no_token_arg(self):
        """Test that --github-token argument is not accepted."""
        result = subprocess.run(
            [sys.executable, "main.py", "--personal-repos", "testuser", "--github-token", "fake-token"],
            capture_output=True,
            text=True
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unrecognized arguments: --github-token", result.stderr)

    def test_env_var_usage(self):
        """Test that application still runs (attempts to run) without the arg, implying env var usage."""
        # We don't need to actually succeed in analysis, just not fail on args
        # We provide a fake token via env var so it doesn't complain about missing auth immediately (if it checks)
        env = os.environ.copy()
        env['GITHUB_TOKEN'] = 'fake-token'

        result = subprocess.run(
            [sys.executable, "main.py", "--personal-repos", "testuser", "--output-dir", "test_output_sec"],
            capture_output=True,
            text=True,
            env=env
        )

        # It shouldn't fail with argument parsing error.
        # It might fail with "Bad credentials" or similar from the API, or just print errors.
        # But return code logic in main.py catches exceptions for modules, so it might exit 0.

        # Check that it didn't fail due to missing arguments or similar
        self.assertNotIn("unrecognized arguments", result.stderr)

        # Check that it tried to run the analyzer
        self.assertIn("Running Personal Repo Analyzer", result.stdout)

if __name__ == '__main__':
    unittest.main()
