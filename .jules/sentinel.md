## 2024-05-23 - Path Traversal Prevention in ArchiveScanner
**Vulnerability:** The `ArchiveScanner` module previously allowed scanning of any directory, including sensitive system paths like `/etc` or `/root`, if the user provided them as input.
**Learning:** Even local CLI tools should validate file path inputs to prevent accidental or malicious scanning of sensitive system areas. Using simple string prefix matching (`startswith`) is insufficient for path validation as it leads to false positives (e.g., blocking `/development` because of `/dev`).
**Prevention:** Always use path-aware libraries (like `pathlib` in Python) to validate paths. Check if the resolved target path matches or is a child of restricted paths (`path in resolved_path.parents`).
