## 2024-05-23 - Path Traversal Prevention in Scanners
**Vulnerability:** The `ArchiveScanner` module allowed scanning of any directory, including system roots (`/`, `C:\`) and sensitive system directories (`/etc`, `/proc`).
**Learning:** File scanning tools must explicitly validate input paths against a blocklist of system directories to prevent accidental or malicious scanning of sensitive system areas, which could lead to DoS (infinite virtual files) or information disclosure.
**Prevention:** Implemented `is_unsafe_path` using `pathlib.Path.resolve()` to normalize paths and check against `UNSAFE_PATHS_POSIX` and `UNSAFE_PATHS_NT` blocklists before allowing a scan.
