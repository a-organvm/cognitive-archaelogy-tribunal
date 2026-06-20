## 2024-12-20 - [Command Injection/Information Disclosure]
**Vulnerability:** The `main.py` script accepted a GitHub token as a command-line argument (`--github-token`). Command-line arguments are visible to other users on the system via process listing tools (e.g., `ps aux`).
**Learning:** Sensitive credentials (API keys, tokens, passwords) should never be passed as command-line arguments. This is a common but dangerous pattern.
**Prevention:** Force the use of environment variables for sensitive data. In this case, we removed the argument and rely on `GITHUB_TOKEN` environment variable, which is already supported by the underlying modules.
