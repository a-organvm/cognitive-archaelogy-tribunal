## 2026-01-10 - [Archive Scanner Path Traversal Protection]
**Vulnerability:** The `ArchiveScanner` could be instructed to scan critical system directories (e.g., `/etc`, `/var`, `C:\Windows`) by passing a root path, potentially exposing sensitive system information or causing performance issues.
**Learning:** Even utility tools designed for scanning user archives should have boundaries to prevent accidental or malicious scanning of the host operating system's critical areas. Path normalization (`resolve()`) alone is not enough; explicit blocking of known unsafe prefixes is required.
**Prevention:** Implemented an `is_unsafe_path` check with a blocklist of POSIX and NT system paths that runs before any scanning operation.
