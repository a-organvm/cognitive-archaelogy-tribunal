## 2024-05-23 - Path Traversal Protection
**Vulnerability:** The `ArchiveScanner` allowed scanning of any directory the user had permissions for, including sensitive system roots like `/`, `/etc`, and `/proc`. This could lead to sensitive data exposure or denial of service (infinite recursion in `/proc` or `/sys`).
**Learning:** Even local CLI tools running with user permissions should implement boundaries to prevent accidental or malicious scanning of sensitive system areas. Users might mistype a path or use `*` inappropriately.
**Prevention:** Implemented an `is_unsafe_path` check that resolves the path and verifies it against a blocklist of critical system directories (`/`, `/etc`, `/var`, etc.) before allowing the scan to proceed. This adheres to "Defense in Depth".
