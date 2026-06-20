
# Bolt's Journal

## 2024-05-22 - Hashing Performance in Python 3.12
**Learning:** `hashlib.file_digest` (introduced in Python 3.11) provides a measurable speedup (approx 1.1x) over manual chunk reading for file hashing, likely by moving the loop to C level.
**Action:** Use `hashlib.file_digest` for hashing files when on Python 3.11+.
