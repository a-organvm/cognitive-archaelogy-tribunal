## 2024-05-23 - Prevent Sensitive Directory Scanning
**Vulnerability:** The `ArchiveScanner` allowed scanning of arbitrary directories, including sensitive system paths like `/etc` or `/root`.
**Learning:** CLI tools that operate on file systems should default to safe boundaries, especially when they might be used by users with elevated privileges or in automated scripts.
**Prevention:** Implemented an `is_unsafe_path` check with a blocklist of system directories (`UNSAFE_PATHS`) in `ArchiveScanner`.
