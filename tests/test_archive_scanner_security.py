import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
import os
import sys

from cognitive_tribunal.modules.archive_scanner import ArchiveScanner

class TestArchiveScannerSecurity(unittest.TestCase):
    """Security tests for ArchiveScanner."""

    def setUp(self):
        self.scanner = ArchiveScanner()

    @patch('cognitive_tribunal.modules.archive_scanner.Path')
    def test_scan_directory_unsafe_posix(self, mock_path):
        """Test that scanning unsafe POSIX paths returns a security error."""
        # Setup mock to simulate a resolved path that is unsafe
        mock_path_obj = MagicMock()
        # Mock resolve to return itself
        mock_path_obj.resolve.return_value = mock_path_obj
        mock_path_obj.exists.return_value = True
        mock_path_obj.is_dir.return_value = True

        # Determine strictness. Let's assume we implement a check against string paths or parts
        # For the test, we can mock the behavior of 'parts' or string representation

        # Case 1: Root directory
        mock_path_obj.__str__.return_value = "/"
        # For pathlib checks, usually we check .parts
        mock_path_obj.parts = ("/",)

        mock_path.return_value = mock_path_obj

        # We need to ensure os.name doesn't interfere if we want to test cross-platform logic
        # But assuming the code uses pathlib, we can mock parts.

        # To robustly test logic that might depend on os.name, we might need to patch os.name too
        # But let's start with a simple check.

        # Note: We need to implement the check in the code first to know exactly what to mock.
        # But TDD says write test first. I expect the code will check against a set of unsafe paths.

        result = self.scanner.scan_directory("/")

        self.assertIn('error', result)
        self.assertIn('Security risk', result['error'])
        self.assertIn('unsafe', result['error'])

    @patch('cognitive_tribunal.modules.archive_scanner.Path')
    def test_scan_directory_unsafe_windows(self, mock_path):
        """Test that scanning unsafe Windows paths returns a security error."""
        mock_path_obj = MagicMock()
        mock_path_obj.resolve.return_value = mock_path_obj
        mock_path_obj.exists.return_value = True
        mock_path_obj.is_dir.return_value = True

        # Case: Windows directory
        mock_path_obj.__str__.return_value = "C:\\Windows"
        # On Windows, parts would be ('C:\\', 'Windows')
        mock_path_obj.parts = ("C:\\", "Windows")

        mock_path.return_value = mock_path_obj

        # We simulate the scanner running on Windows for this test?
        # Or we implement a check that handles both if possible.
        # Ideally the scanner detects the OS it is running on.
        # But to be safe, we might blacklist common unsafe paths for both.

        result = self.scanner.scan_directory("C:\\Windows")

        self.assertIn('error', result)
        self.assertIn('Security risk', result['error'])

    @patch('cognitive_tribunal.modules.archive_scanner.Path')
    def test_scan_directory_safe_path(self, mock_path):
        """Test that scanning a safe path proceeds (or fails with mocked later steps)."""
        mock_path_obj = MagicMock()
        mock_path_obj.resolve.return_value = mock_path_obj
        mock_path_obj.exists.return_value = True
        mock_path_obj.is_dir.return_value = True

        mock_path_obj.__str__.return_value = "/Users/jules/Documents"
        mock_path_obj.parts = ("/", "Users", "jules", "Documents")

        mock_path.return_value = mock_path_obj

        # We expect it to NOT fail with security error.
        # It might fail later because we haven't mocked _scan_recursive fully,
        # but the return value shouldn't be the security error.

        # We mock _scan_recursive to avoid actual work
        with patch.object(self.scanner, '_scan_recursive') as mock_scan:
            with patch.object(self.scanner, 'get_results') as mock_results:
                mock_results.return_value = {'stats': 'ok'}

                result = self.scanner.scan_directory("/Users/jules/Documents")

                self.assertEqual(result, {'stats': 'ok'})
                mock_scan.assert_called_once()
