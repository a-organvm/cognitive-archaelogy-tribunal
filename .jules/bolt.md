## 2024-05-23 - [File I/O and Redundant Hashing]
**Learning:** Default file read buffers (8KB) in Python are often too small for modern I/O. 64KB is a sweet spot. Also, eager hashing in deduplication logic can lead to 2x or more work if not carefully managed against the final verification pass.
**Action:** Always check buffer sizes in I/O loops. For deduplication, ensure work isn't done twice (once on ingestion, once on verification).
