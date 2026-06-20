import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from cognitive_tribunal.modules.archive_scanner import ArchiveScanner

class TestArchiveScannerSecurity(unittest.TestCase):

    @patch('pathlib.Path.resolve')
    @patch('pathlib.Path.is_dir')
    @patch('pathlib.Path.exists')
    @patch('cognitive_tribunal.modules.archive_scanner.ArchiveScanner._scan_recursive')
    def test_unsafe_path_rejection_root(self, mock_scan, mock_exists, mock_is_dir, mock_resolve):
        """Test that scanning root directory is rejected."""
        mock_exists.return_value = True
        mock_is_dir.return_value = True
        # Mock resolve to return the path as is (or as absolute path)
        mock_resolve.return_value = Path('/')

        scanner = ArchiveScanner()
        result = scanner.scan_directory('/')

        if mock_scan.called:
             self.fail("Security vulnerability: Scanner attempted to scan root directory '/'")

        self.assertIn('error', result)
        self.assertIn('Unsafe path', result['error'])

    @patch('pathlib.Path.resolve')
    @patch('pathlib.Path.is_dir')
    @patch('pathlib.Path.exists')
    @patch('cognitive_tribunal.modules.archive_scanner.ArchiveScanner._scan_recursive')
    def test_unsafe_path_rejection_etc(self, mock_scan, mock_exists, mock_is_dir, mock_resolve):
        """Test that scanning /etc is rejected."""
        mock_exists.return_value = True
        mock_is_dir.return_value = True
        mock_resolve.return_value = Path('/etc')

        scanner = ArchiveScanner()
        result = scanner.scan_directory('/etc')

        if mock_scan.called:
             self.fail("Security vulnerability: Scanner attempted to scan sensitive directory '/etc'")

        self.assertIn('error', result)
        self.assertIn('Unsafe path', result['error'])

    @patch('pathlib.Path.resolve')
    @patch('pathlib.Path.is_dir')
    @patch('pathlib.Path.exists')
    @patch('cognitive_tribunal.modules.archive_scanner.ArchiveScanner._scan_recursive')
    def test_unsafe_path_rejection_subdir(self, mock_scan, mock_exists, mock_is_dir, mock_resolve):
        """Test that scanning a subdirectory of a sensitive directory is rejected."""
        mock_exists.return_value = True
        mock_is_dir.return_value = True
        # Mock resolve to return a subdirectory of /etc
        mock_resolve.return_value = Path('/etc/ssh')

        scanner = ArchiveScanner()
        result = scanner.scan_directory('/etc/ssh')

        if mock_scan.called:
             self.fail("Security vulnerability: Scanner attempted to scan sensitive subdirectory '/etc/ssh'")

        self.assertIn('error', result)
        self.assertIn('Unsafe path', result['error'])

    @patch('pathlib.Path.resolve')
    @patch('pathlib.Path.is_dir')
    @patch('pathlib.Path.exists')
    @patch('cognitive_tribunal.modules.archive_scanner.ArchiveScanner._scan_recursive')
    def test_safe_path_allowed(self, mock_scan, mock_exists, mock_is_dir, mock_resolve):
        """Test that scanning a safe directory is allowed."""
        mock_exists.return_value = True
        mock_is_dir.return_value = True
        mock_resolve.return_value = Path('/home/user/documents')

        scanner = ArchiveScanner()
        result = scanner.scan_directory('/home/user/documents')

        # Should call _scan_recursive
        self.assertTrue(mock_scan.called, "Scanner should have proceeded with scanning safe path")
        self.assertNotIn('error', result)

    @patch('pathlib.Path.resolve')
    @patch('pathlib.Path.is_dir')
    @patch('pathlib.Path.exists')
    @patch('cognitive_tribunal.modules.archive_scanner.ArchiveScanner._scan_recursive')
    def test_windows_sensitive_path(self, mock_scan, mock_exists, mock_is_dir, mock_resolve):
        """Test blocking of Windows sensitive paths even on Linux environment (via mocking)."""
        mock_exists.return_value = True
        mock_is_dir.return_value = True
        mock_resolve.return_value = Path('C:\\Windows')

        scanner = ArchiveScanner()
        result = scanner.scan_directory('C:\\Windows')

        if mock_scan.called:
             self.fail("Security vulnerability: Scanner attempted to scan C:\\Windows")

        self.assertIn('error', result)
        self.assertIn('Unsafe path', result['error'])

    @patch('pathlib.Path.resolve')
    @patch('pathlib.Path.is_dir')
    @patch('pathlib.Path.exists')
    @patch('cognitive_tribunal.modules.archive_scanner.ArchiveScanner._scan_recursive')
    def test_windows_root_path_blocked(self, mock_scan, mock_exists, mock_is_dir, mock_resolve):
        """Test blocking of Windows root C:\\."""
        mock_exists.return_value = True
        mock_is_dir.return_value = True
        mock_resolve.return_value = Path('C:\\')

        scanner = ArchiveScanner()
        result = scanner.scan_directory('C:\\')

        if mock_scan.called:
             self.fail("Security vulnerability: Scanner attempted to scan C:\\")

        self.assertIn('error', result)
        self.assertIn('Unsafe path', result['error'])

    @patch('pathlib.Path.resolve')
    @patch('pathlib.Path.is_dir')
    @patch('pathlib.Path.exists')
    @patch('cognitive_tribunal.modules.archive_scanner.ArchiveScanner._scan_recursive')
    def test_windows_user_path_allowed(self, mock_scan, mock_exists, mock_is_dir, mock_resolve):
        """Test that a normal Windows user path is allowed."""
        mock_exists.return_value = True
        mock_is_dir.return_value = True
        mock_resolve.return_value = Path('C:\\Users\\User\\Documents')

        scanner = ArchiveScanner()
        result = scanner.scan_directory('C:\\Users\\User\\Documents')

        # Should call _scan_recursive
        self.assertTrue(mock_scan.called, "Scanner should have proceeded with scanning safe windows path")
        self.assertNotIn('error', result)
