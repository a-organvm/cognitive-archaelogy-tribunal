## 2024-05-23 - [ArchiveScanner Path Traversal Protection]
**Vulnerability:** The `ArchiveScanner` previously allowed scanning any directory, including sensitive system paths like `/` or `/etc`.
**Learning:** Recursively blocking subdirectories of sensitive paths using `Path.is_relative_to` is effective but requires careful handling of root paths (like `C:\`) to avoid blocking legitimate user directories (e.g., `C:\Users`).
**Prevention:** Always validate user-supplied file paths against a blocklist of sensitive system directories before performing file operations. Use `resolve()` to handle symlinks and `..`.
