## 2026-01-20 - [CLI Empty State]
**Learning:** Users often run a CLI tool without arguments to see what happens. Showing an error message "At least one module must be specified" is hostile. A styled "Empty State" with examples and a welcome message invites exploration and reduces initial friction.
**Action:** Always intercept `len(argv) == 1` in CLI tools to provide a "Welcome Panel" or "Interactive Mode" instead of a raw argument parser error.
