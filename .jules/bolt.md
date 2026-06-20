# Bolt's Journal

## 2024-05-22 - File Hashing Optimization
**Learning:** File hashing was reading the entire file into memory, causing memory spikes for large files. Switching to a buffered read (64KB chunks) significantly reduces memory usage without impacting speed.
**Action:** Always check file I/O operations for potential memory issues, especially when dealing with unknown file sizes. Use buffered reading by default.

## 2024-05-22 - Lazy Hashing in Deduplication
**Learning:** Calculating hashes for all files during the initial scan is wasteful if the file sizes don't match.
**Action:** Implement lazy hashing where we only hash files that have potential duplicates based on file size. This drastically reduces CPU and I/O during the initial scanning phase.
