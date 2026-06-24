
from cognitive_tribunal.modules.archive_scanner import ArchiveScanner
import unittest
from unittest.mock import MagicMock, patch, PropertyMock
from pathlib import Path
import os
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestArchiveScannerSecurity(unittest.TestCase):

    def setUp(self):
        self.scanner = ArchiveScanner()

    def test_unsafe_root_detection(self):
        """Test that the filesystem root is considered unsafe."""
        # Create a mock path that behaves like root
        mock_path = MagicMock(spec=Path)
        mock_path.resolve.return_value = mock_path
        # Anchor being same as string representation implies root
        type(mock_path).anchor = PropertyMock(return_value="/")
        mock_path.__str__.return_value = "/"

        self.assertTrue(self.scanner.is_unsafe_path(mock_path))

    def test_unsafe_system_dir_detection_posix(self):
        """Test that system directories on POSIX are blocked."""
        with patch('os.name', 'posix'):
            unsafe_paths = ['/etc', '/bin', '/sys', '/proc']

            for p in unsafe_paths:
                mock_path = MagicMock(spec=Path)
                mock_path.resolve.return_value = mock_path
                type(mock_path).anchor = PropertyMock(
                    return_value="/")  # Root anchor
                mock_path.__str__.return_value = p

                self.assertTrue(self.scanner.is_unsafe_path(
                    mock_path), f"Should block {p}")

    def test_safe_user_dir_posix(self):
        """Test that user directories are allowed."""
        with patch('os.name', 'posix'):
            safe_paths = ['/home/user/docs', '/tmp/scan_target', '/var/www']

            for p in safe_paths:
                mock_path = MagicMock(spec=Path)
                mock_path.resolve.return_value = mock_path
                type(mock_path).anchor = PropertyMock(return_value="/")
                mock_path.__str__.return_value = p

                self.assertFalse(self.scanner.is_unsafe_path(
                    mock_path), f"Should allow {p}")

    def test_scan_directory_blocks_unsafe(self):
        """Test that scan_directory actually uses the check."""
        with patch('pathlib.Path.resolve') as mock_resolve, \
                patch('pathlib.Path.exists', return_value=True), \
                patch('pathlib.Path.is_dir', return_value=True):

            # Simulate /etc
            mock_path = MagicMock(spec=Path)
            mock_path.resolve.return_value = mock_path
            type(mock_path).anchor = PropertyMock(return_value="/")
            mock_path.__str__.return_value = "/etc"
            mock_resolve.return_value = mock_path

            # Force os.name to posix for this test
            with patch('os.name', 'posix'):
                result = self.scanner.scan_directory("/etc")

            self.assertIn('error', result)
            self.assertIn('Security', result['error'])


if __name__ == '__main__':
    unittest.main()
