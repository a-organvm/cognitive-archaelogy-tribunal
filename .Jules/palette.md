## 2024-05-23 - Progressive Enhancement for CLI Tools
**Learning:** When enhancing CLI tools with rich text libraries like `rich`, it's critical to implement a robust fallback mechanism for environments where the library might be missing or the terminal is non-interactive (e.g., CI/CD pipelines, dumb terminals).
**Action:** Use a `try/except ImportError` block to conditionally import `rich`. If the import fails, define a local `MockConsole` class that mimics the essential methods (e.g., `print`, `status`) using standard `print` statements or no-ops, ensuring the application remains functional without the dependency.

## 2024-05-23 - Data Safety in Rich Text Output
**Learning:** When printing user-generated content (like filenames) using libraries that parse markup (like `rich`), there is a risk of accidental markup injection if the content contains characters like `[` or `]`.
**Action:** Always escape dynamic content using `rich.markup.escape` before printing it within a markup string, or use `Text` objects which handle content literally. Similarly, when implementing fallbacks that strip tags, ensure the regex is specific enough to avoid stripping valid content that resembles tags.
