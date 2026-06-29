import os
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch, call
from cognitive_tribunal.modules.archive_scanner import ArchiveScanner

def test_scan_directory_unsafe_paths_linux():
    """Verify that unsafe paths are blocked on Linux using mocked resolution."""
    # This test runs on the actual OS (Linux), so we don't mock os.name
    # We rely on the fact that we are on Posix.
    if os.name == 'posix':
        scanner = ArchiveScanner()

        # Define unsafe paths to test (subset of actual blacklist)
        unsafe_paths = ['/', '/etc', '/dev']

        for unsafe_path_str in unsafe_paths:
            if Path(unsafe_path_str).exists():
                 # Test real logic integration
                 result = scanner.scan_directory(unsafe_path_str, recursive=False)
                 assert 'error' in result, f"Should return error for {unsafe_path_str}"
                 assert "Unsafe path detected" in result['error']

def test_is_unsafe_path_posix():
    """Test is_unsafe_path logic for POSIX systems."""
    scanner = ArchiveScanner()

    with patch('os.name', 'posix'):
        # Test Root
        p_root = MagicMock(spec=Path)
        p_root.resolve.return_value = Path('/')
        assert scanner.is_unsafe_path(p_root) is True

        # Test /etc (Unsafe)
        p_etc = MagicMock(spec=Path)
        p_etc.resolve.return_value = Path('/etc')
        assert scanner.is_unsafe_path(p_etc) is True

        # Test /sys/kernel (Unsafe subdir)
        p_sys = MagicMock(spec=Path)
        p_sys.resolve.return_value = Path('/sys/kernel')
        assert scanner.is_unsafe_path(p_sys) is True

        # Test Safe Path (/opt and /var should be safe now)
        p_opt = MagicMock(spec=Path)
        p_opt.resolve.return_value = Path('/opt/myapp')
        assert scanner.is_unsafe_path(p_opt) is False

        p_home = MagicMock(spec=Path)
        p_home.resolve.return_value = Path('/home/user')
        assert scanner.is_unsafe_path(p_home) is False

def test_is_unsafe_path_windows_logic():
    """Test is_unsafe_path logic uses correct list for Windows systems."""
    scanner = ArchiveScanner()

    # We cannot instantiate WindowsPath on Linux, so we mock Path inside the module
    # to verify it iterates over the NT list when os.name is nt.

    with patch('os.name', 'nt'):
        with patch('cognitive_tribunal.modules.archive_scanner.Path') as MockPath:
            # Setup MockPath to return a mock that compares nicely
            mock_u_path = MagicMock()
            MockPath.return_value = mock_u_path

            # Setup resolved path
            p_input = MagicMock()
            # If resolved_path == u_path returns True
            p_input.resolve.return_value.__eq__.return_value = False
            p_input.resolve.return_value.parents = []
            p_input.resolve.return_value.anchor = 'D:\\'

            # Run method
            scanner.is_unsafe_path(p_input)

            # Verify Path was instantiated with Windows unsafe paths
            expected_calls = [call(p) for p in ArchiveScanner.UNSAFE_PATHS_NT]
            MockPath.assert_has_calls(expected_calls, any_order=True)

def test_scan_directory_blocks_unsafe():
    """Integration test: scan_directory returns error for unsafe path."""
    scanner = ArchiveScanner()

    # We mock is_unsafe_path to return True to verify scan_directory behavior
    with patch.object(scanner, 'is_unsafe_path', return_value=True):
        # We can pass any string, it will be resolved but blocked
        result = scanner.scan_directory('.', recursive=False)
        assert 'error' in result
        assert "Unsafe path detected" in result['error']

def test_scan_directory_allows_safe():
    """Integration test: scan_directory proceeds for safe path."""
    scanner = ArchiveScanner()

    # We mock is_unsafe_path to return False
    with patch.object(scanner, 'is_unsafe_path', return_value=False):
        # We also need to mock exists and is_dir to pass
        with patch('pathlib.Path.exists', return_value=True):
            with patch('pathlib.Path.is_dir', return_value=True):
                # We need to mock _scan_recursive or it will fail on invalid path
                with patch.object(scanner, '_scan_recursive'):
                    result = scanner.scan_directory('/some/path', recursive=False)
                    # If it proceeds, it returns get_results()
                    assert 'stats' in result
