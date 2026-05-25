## 2026-01-14 - Small Buffer Size Anti-Pattern
**Learning:** The legacy file hashing implementation used a small 8KB buffer, which is suboptimal for modern I/O. Additionally, Python 3.11+ offers `hashlib.file_digest` which pushes the loop to C-level, releasing GIL.
**Action:** Always check for `hashlib.file_digest` availability when implementing file hashing and default to larger buffers (e.g., 64KB) for fallbacks.
