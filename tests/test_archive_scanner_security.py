import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
import sys

from cognitive_tribunal.modules.archive_scanner import ArchiveScanner

class TestArchiveScannerSecurity(unittest.TestCase):
    def setUp(self):
        self.scanner = ArchiveScanner()

    @patch('cognitive_tribunal.modules.archive_scanner.ArchiveScanner._scan_recursive')
    @patch('pathlib.Path.resolve')
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.is_dir')
    def test_rejects_unsafe_paths_posix(self, mock_is_dir, mock_exists, mock_resolve, mock_scan_recursive):
        # Setup mocks
        mock_exists.return_value = True
        mock_is_dir.return_value = True

        # Test root path
        root_path = Path('/')
        mock_resolve.return_value = root_path

        # This should fail currently because the check is missing
        result = self.scanner.scan_directory('/')

        # If the check was present, it would return an error
        self.assertIn('error', result, "Should return error for root path")
        self.assertIn('Unsafe path', result.get('error', ''), "Error should mention unsafe path")

        # Verify scan recursive was NOT called if we expect security check to fail
        # But currently it IS called, so this assertion would also fail if we were checking for it to NOT be called
        # mock_scan_recursive.assert_not_called()

    @patch('cognitive_tribunal.modules.archive_scanner.ArchiveScanner._scan_recursive')
    @patch('pathlib.Path.resolve')
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.is_dir')
    def test_rejects_unsafe_paths_etc(self, mock_is_dir, mock_exists, mock_resolve, mock_scan_recursive):
        # Setup mocks
        mock_exists.return_value = True
        mock_is_dir.return_value = True

        # Test /etc path
        etc_path = Path('/etc')
        mock_resolve.return_value = etc_path

        result = self.scanner.scan_directory('/etc')

        self.assertIn('error', result, "Should return error for /etc path")
        self.assertIn('Unsafe path', result.get('error', ''), "Error should mention unsafe path")

if __name__ == '__main__':
    unittest.main()
