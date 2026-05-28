## 2026-01-14 - [Path Traversal in Archive Scanner]
**Vulnerability:** The `ArchiveScanner.scan_directory` method blindly accepted any directory path, including filesystem root (`/`) and critical system directories (`/etc`, `C:\Windows`), allowing potential exposure of sensitive system files.
**Learning:** Documented security controls (in memory/docs) were not actually implemented in the code. Trust but verify - always check the implementation, not just the description.
**Prevention:** Implemented `is_unsafe_path` validation using `pathlib.Path.resolve()` and platform-specific blocklists (`UNSAFE_PATHS_POSIX`, `UNSAFE_PATHS_NT`) to enforce boundaries at the scanning entry point.
