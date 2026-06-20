## 2024-05-23 - [Rich CLI Output]
**Learning:** CLI tools can greatly benefit from semantic coloring and progress spinners to reduce perceived latency. However, handling environments without these capabilities requires robust fallback logic that strips formatting without losing content (e.g. preserving `[1/4]` step indicators while stripping `[bold]`).
**Action:** Always implement a `MockConsole` or similar abstraction when introducing UI libraries like `rich` to ensure scripts remain scriptable and pipe-friendly.
