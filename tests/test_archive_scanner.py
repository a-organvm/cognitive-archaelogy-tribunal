"""
Tests for Archive Scanner module.
"""

import tempfile
from pathlib import Path

from cognitive_tribunal.modules.archive_scanner import ArchiveScanner


def create_test_file(directory: Path, filename: str, content: str):
    """Helper function to create test files."""
    file_path = directory / filename
    file_path.write_text(content)
    return file_path


def test_deduplicator_reset_between_locations():
    """
    Test that the deduplicator is reset between different location scans.
    
    This test verifies that when scanning multiple locations with the same
    ArchiveScanner instance, the deduplicator statistics for each location
    are independent and don't include data from previous locations.
    """
    # Create two temporary directories with identical files
    with tempfile.TemporaryDirectory() as temp_dir1:
        with tempfile.TemporaryDirectory() as temp_dir2:
            dir1 = Path(temp_dir1)
            dir2 = Path(temp_dir2)
            
            # Create identical files in both directories
            content = "This is test content for duplicate detection"
            create_test_file(dir1, "file1.txt", content)
            create_test_file(dir2, "file1.txt", content)
            
            # Scan locations one by one
            scanner = ArchiveScanner()
            
            # Scan first location
            result1 = scanner.scan_directory(str(dir1))
            dedup_stats1 = result1['deduplication']['stats']
            
            # Scan second location - should not include duplicates from first location
            result2 = scanner.scan_directory(str(dir2))
            dedup_stats2 = result2['deduplication']['stats']
            
            # Each location should report only 1 file (no duplicates within location)
            assert dedup_stats1['total_files'] == 1, \
                f"Expected 1 file in location 1, got {dedup_stats1['total_files']}"
            assert dedup_stats1['duplicate_files'] == 0, \
                f"Expected 0 duplicates in location 1, got {dedup_stats1['duplicate_files']}"
            
            assert dedup_stats2['total_files'] == 1, \
                f"Expected 1 file in location 2, got {dedup_stats2['total_files']}"
            assert dedup_stats2['duplicate_files'] == 0, \
                f"Expected 0 duplicates in location 2, got {dedup_stats2['duplicate_files']}"
            
            # If deduplicator is not reset, location 2 would show 2 total_files
            # (1 from current location + 1 from previous location)


def test_scan_multiple_locations_independent():
    """
    Test that scan_multiple_locations produces correct per-location stats.
    
    This test verifies that each location's results are independent and
    don't get contaminated by files from other locations.
    """
    with tempfile.TemporaryDirectory() as temp_dir1:
        with tempfile.TemporaryDirectory() as temp_dir2:
            dir1 = Path(temp_dir1)
            dir2 = Path(temp_dir2)
            
            # Create different files in each directory
            create_test_file(dir1, "file1.txt", "Content for location 1")
            create_test_file(dir1, "file2.txt", "More content for location 1")
            
            create_test_file(dir2, "file3.txt", "Content for location 2")
            
            # Use scan_multiple_locations
            scanner = ArchiveScanner()
            results = scanner.scan_multiple_locations([str(dir1), str(dir2)])
            
            # Check per-location results
            loc1_results = results['locations'][str(dir1)]
            loc2_results = results['locations'][str(dir2)]
            
            # Location 1 should have 2 files
            assert loc1_results['stats']['total_files'] == 2, \
                f"Expected 2 files in location 1, got {loc1_results['stats']['total_files']}"
            
            # Location 2 should have 1 file (not 3 from accumulated state)
            assert loc2_results['stats']['total_files'] == 1, \
                f"Expected 1 file in location 2, got {loc2_results['stats']['total_files']}"
            
            # Deduplication stats for location 2 should only count its own file
            loc2_dedup = loc2_results['deduplication']['stats']
            assert loc2_dedup['total_files'] == 1, \
                f"Expected 1 file in location 2 dedup stats, got {loc2_dedup['total_files']}"


def test_duplicate_detection_within_single_location():
    """
    Test that duplicates within a single location are correctly detected.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        directory = Path(temp_dir)
        
        # Create duplicate files within the same location
        content = "Duplicate content"
        create_test_file(directory, "dup1.txt", content)
        create_test_file(directory, "dup2.txt", content)
        create_test_file(directory, "unique.txt", "Unique content")
        
        scanner = ArchiveScanner()
        result = scanner.scan_directory(str(directory))
        
        # Should have 3 total files
        assert result['stats']['total_files'] == 3
        
        # Should detect 1 duplicate group with 2 files
        dedup_stats = result['deduplication']['stats']
        assert dedup_stats['total_files'] == 3
        assert dedup_stats['duplicate_groups'] == 1
        assert dedup_stats['duplicate_files'] == 1  # 2 files - 1 = 1 duplicate


def test_unsafe_path_blocking():
    """
    Test that scanning sensitive system paths is blocked.
    """
    scanner = ArchiveScanner()
    # Mocking unsafe_paths for the test environment to ensure we can trigger it
    # regardless of the actual OS we are running on.
    scanner.unsafe_paths = {'/unsafe_test_dir'}

    # We need a path that resolves to /unsafe_test_dir or starts with it.
    with tempfile.TemporaryDirectory() as temp_dir:
        unsafe_dir = Path(temp_dir).resolve()
        # Mocking the set of unsafe paths to include our temp dir
        scanner.unsafe_paths = {str(unsafe_dir)}

        result = scanner.scan_directory(str(unsafe_dir))

        assert 'error' in result, "Expected error when scanning unsafe path"
        assert 'Security: Scanning of system directory' in result['error']

        # Also verify that a subpath is blocked
        sub_dir = unsafe_dir / "subdir"
        # We don't create it, but the check happens before existence check if we implemented it right
        # But our implementation checks resolve() which requires existence for symlinks usually,
        # but resolve() works on non-existent paths in modern python if only the last part is missing?
        # Actually, let's just make the directory to be sure
        sub_dir.mkdir()
        result_sub = scanner.scan_directory(str(sub_dir))
        assert 'error' in result_sub, "Expected error when scanning subpath of unsafe path"
        assert 'Security: Scanning of system directory' in result_sub['error']

    # Test false positive avoidance (prefix match but not directory match)
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a directory that starts with the unsafe name but is different
        # e.g. /tmp/unsafe_test_dir_suffix
        safe_dir = Path(temp_dir) / "unsafe_test_dir_suffix"
        safe_dir.mkdir()

        # Reset unsafe paths to just the base name (virtual)
        # We need to simulate: unsafe=/foo, scanning=/foo_bar

        # Let's use a concrete example. Unsafe: /tmp/mock_unsafe
        # Safe: /tmp/mock_unsafe_suffix

        base_dir = Path(temp_dir).resolve()
        unsafe_path = base_dir / "mock_unsafe"
        safe_path = base_dir / "mock_unsafe_suffix"
        safe_path.mkdir()

        scanner.unsafe_paths = {str(unsafe_path)}

        # Should NOT return security error (might return empty stats as dir is empty)
        result = scanner.scan_directory(str(safe_path))

        if 'error' in result:
             assert 'Security' not in result['error'], \
                 f"False positive detection: {safe_path} matches unsafe {unsafe_path}"
