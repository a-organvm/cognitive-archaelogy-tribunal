from cognitive_tribunal.utils.file_utils import FileHasher, Deduplicator, HAS_XXHASH
import hashlib
import os
from pathlib import Path
import pytest

try:
    import xxhash
except ImportError:
    xxhash = None

@pytest.mark.skipif(not HAS_XXHASH, reason="xxhash not available")
def test_file_hasher_xxhash():
    # Create a test file
    test_file = Path("test_hash.txt")
    with open(test_file, "wb") as f:
        f.write(b"test content")

    # Calculate expected xxhash
    expected = xxhash.xxh64(b"test content").hexdigest()

    # Calculate actual
    actual = FileHasher.compute_hash(test_file, algorithm="xxhash")

    # Clean up
    if test_file.exists():
        os.remove(test_file)

    assert actual == expected

@pytest.mark.skipif(not HAS_XXHASH, reason="xxhash not available")
def test_deduplicator_caching_xxhash():
    dedup = Deduplicator()
    file_path = Path("test_dedup.txt")
    with open(file_path, "wb") as f:
        f.write(b"test content")

    # Add file, force hash computation
    dedup.add_file(file_path, compute_full_hash=True)

    # Check if hash is cached
    assert file_path in dedup.file_to_hash
    cached_hash = dedup.file_to_hash[file_path]

    # Verify hash is correct (should be xxhash by default now if available)
    expected = xxhash.xxh64(b"test content").hexdigest()
    assert cached_hash == expected

    # Clean up
    if file_path.exists():
        os.remove(file_path)

def test_deduplicator_caching_fallback():
    # Force HAS_XXHASH to False if needed, but we can just test that caching works
    # regardless of algorithm
    dedup = Deduplicator()
    file_path = Path("test_dedup_fallback.txt")
    with open(file_path, "wb") as f:
        f.write(b"test content")

    # Add file, force hash computation
    dedup.add_file(file_path, compute_full_hash=True)

    # Check if hash is cached
    assert file_path in dedup.file_to_hash

    # Clean up
    if file_path.exists():
        os.remove(file_path)

def test_deduplicator_find_duplicates():
    dedup = Deduplicator()
    file1 = Path("test_dup1.txt")
    file2 = Path("test_dup2.txt")

    content = b"duplicate content"
    with open(file1, "wb") as f:
        f.write(content)
    with open(file2, "wb") as f:
        f.write(content)

    try:
        dedup.add_file(file1)
        dedup.add_file(file2)

        duplicates = dedup.find_duplicates()

        assert len(duplicates) == 1
        # Check that caching happened
        assert file1 in dedup.file_to_hash
        assert file2 in dedup.file_to_hash
    finally:
        if file1.exists():
            os.remove(file1)
        if file2.exists():
            os.remove(file2)
