# Palette's Journal - Critical UX/Accessibility Learnings

## 2024-05-22 - [CLI Accessibility]
**Learning:** Screen readers for terminal (like JAWS or NVDA) rely heavily on plain text structure. Over-use of complex ASCII art or purely color-based information can be inaccessible.
**Action:** Ensure that critical information delivered via `rich` or colored output is also understandable via text content alone, or offer a `--plain` mode if color usage becomes structural.
