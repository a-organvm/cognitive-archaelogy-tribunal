
import unittest
import tempfile
import os
import hashlib
from pathlib import Path
from cognitive_tribunal.utils.file_utils import FileHasher, Deduplicator, HAS_XXHASH

class TestFileUtilsPerformance(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.file_path = Path(self.test_dir) / "test_file.bin"
        self.content = os.urandom(1024 * 1024) # 1MB
        with open(self.file_path, 'wb') as f:
            f.write(self.content)

    def tearDown(self):
        os.unlink(self.file_path)
        os.rmdir(self.test_dir)

    def test_compute_hash_sha256(self):
        # Verify sha256 still works and is correct
        expected = hashlib.sha256(self.content).hexdigest()
        actual = FileHasher.compute_hash(self.file_path, 'sha256')
        self.assertEqual(actual, expected)

    def test_compute_hash_xxhash(self):
        if not HAS_XXHASH:
            print("Skipping xxhash test as library not available")
            return

        import xxhash
        expected = xxhash.xxh64(self.content).hexdigest()
        actual = FileHasher.compute_hash(self.file_path, 'xxhash')
        self.assertEqual(actual, expected)

    def test_deduplicator_uses_xxhash(self):
        if not HAS_XXHASH:
            return

        dedup = Deduplicator()
        # Add file twice
        dedup.add_file(self.file_path)
        dedup.add_file(self.file_path) # Should trigger hash computation because size matches

        # Check if hash in hash_to_files is xxhash (length 16 for xxh64 hex) vs 64 for sha256
        # xxh64 hexdigest is 16 chars (64 bits = 8 bytes = 16 hex chars)
        # sha256 hexdigest is 64 chars

        hashes = list(dedup.hash_to_files.keys())
        # We need to force hash computation. add_file only computes hash if collision or requested.
        # But we added the same file twice, so size collision occurred.
        # However, add_file checks `if compute_full_hash or len(self.size_to_files[file_size]) > 1:`
        # First add: size_to_files has 1. No hash.
        # Second add: size_to_files has 2. Hash computed.

        # But wait, logic is:
        # if compute_full_hash or len(self.size_to_files[file_size]) > 1:
        #    full_hash = ...
        #    ...

        # So on second add, it computes hash for the *current* file_path being added.
        # But what about the *first* file? It is in size_to_files but not hash_to_files yet?
        # The code for `add_file` doesn't go back and hash the previous files in size_to_files?

        # Let's check `add_file` logic again.
        # It adds to size_to_files first.
        # Then checks len > 1.
        # Then hashes *current* file_path.
        # It does NOT hash the previous file if it wasn't hashed.

        # `find_duplicates` iterates size_to_files and hashes ALL of them if len > 1.

        # So to test `add_file` behavior regarding `compute_full_hash=True`:
        dedup2 = Deduplicator()
        dedup2.add_file(self.file_path, compute_full_hash=True)
        hashes = list(dedup2.hash_to_files.keys())
        self.assertEqual(len(hashes), 1)
        self.assertEqual(len(hashes[0]), 16, f"Hash length should be 16 for xxhash, got {len(hashes[0])}: {hashes[0]}")

if __name__ == '__main__':
    unittest.main()
