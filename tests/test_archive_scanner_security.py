"""
Tests for Archive Scanner Security enhancements.
"""

import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cognitive_tribunal.modules.archive_scanner import ArchiveScanner, UNSAFE_PATHS

class TestArchiveScannerSecurity(unittest.TestCase):

    def setUp(self):
        self.scanner = ArchiveScanner()

    def test_unsafe_paths_blocked(self):
        """Test that all defined unsafe paths are blocked."""

        for unsafe_path in UNSAFE_PATHS:
            with patch('pathlib.Path.resolve') as mock_resolve, \
                 patch('pathlib.Path.exists', return_value=True), \
                 patch('pathlib.Path.is_dir', return_value=True), \
                 patch.object(self.scanner, '_scan_recursive') as mock_scan:

                # Mock path behavior
                mock_path = MagicMock(spec=Path)
                mock_path.__str__.return_value = unsafe_path
                mock_path.resolve.return_value = mock_path
                mock_resolve.return_value = mock_path

                result = self.scanner.scan_directory(unsafe_path)

                self.assertFalse(mock_scan.called, f"Scanner should have blocked {unsafe_path}")
                self.assertIn('error', result)
                self.assertIn('Security risk', result['error'])

    def test_unsafe_subdirectories_blocked(self):
        """Test that subdirectories of unsafe paths are blocked."""

        # Test /etc/passwd (conceptual)
        unsafe_subdir = "/etc/passwd_dir"

        with patch('pathlib.Path.resolve') as mock_resolve, \
             patch('pathlib.Path.exists', return_value=True), \
             patch('pathlib.Path.is_dir', return_value=True), \
             patch.object(self.scanner, '_scan_recursive') as mock_scan:

            mock_path = MagicMock(spec=Path)
            mock_path.__str__.return_value = unsafe_subdir
            mock_path.resolve.return_value = mock_path
            mock_resolve.return_value = mock_path

            result = self.scanner.scan_directory(unsafe_subdir)

            self.assertFalse(mock_scan.called, f"Scanner should have blocked {unsafe_subdir}")
            self.assertIn('error', result)
            self.assertIn('Security risk', result['error'])

    def test_safe_paths_allowed(self):
        """Test that safe paths are allowed."""

        safe_path = "/home/user/documents"

        with patch('pathlib.Path.resolve') as mock_resolve, \
             patch('pathlib.Path.exists', return_value=True), \
             patch('pathlib.Path.is_dir', return_value=True), \
             patch.object(self.scanner, '_scan_recursive') as mock_scan:

            mock_path = MagicMock(spec=Path)
            mock_path.__str__.return_value = safe_path
            mock_path.resolve.return_value = mock_path
            mock_resolve.return_value = mock_path

            result = self.scanner.scan_directory(safe_path)

            self.assertTrue(mock_scan.called, f"Scanner should have allowed {safe_path}")
            self.assertNotIn('error', result)

if __name__ == '__main__':
    unittest.main()
