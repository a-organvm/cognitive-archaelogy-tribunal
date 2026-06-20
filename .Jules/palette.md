## 2024-05-23 - [Rich CLI Output]
**Learning:** Python CLI tools often claim to have rich output but fall back to print. Implementing a centralized `UI` helper class that handles `rich` import and fallback allows for consistent styling and graceful degradation without cluttering the main logic.
**Action:** Use a `UI` helper wrapper pattern in future CLI tools to manage `rich` dependency optionality cleanly.
