---
description: AI rules derived by SpecStory from the project AI interaction history
globs: *
---

## <headers/>

## TECH STACK

## PROJECT DOCUMENTATION & CONTEXT SYSTEM

## CODING STANDARDS

## GIT & VERSION CONTROL

- `.history` and `.trunk` should follow the same `.venv` and `.vscode` rules.
- `.history` (local VS Code file history) must be added to `.gitignore`.
- `.trunk` (trunk.io tool cache/config) must be added to `.gitignore`.
- `.trunk/*` subdirectories must be excluded from VS Code explorer (in `settings.json`).

## DIRECTORY STRUCTURE

- Configuration folders are kept in `.config/` for archival purposes but tools regenerate them at workspace root
- All config folders (`.venv`, `.vscode`, `.trunk`, `.history`, `.github`, `.specstory`) are:
  - Gitignored (not committed to repository)
  - Hidden from VS Code explorer via `files.exclude` setting
  - Allowed to regenerate at workspace root as needed by tools
- This approach keeps the workspace clean while maintaining full tool compatibility

## VS CODE SETTINGS

- Disable the Local History extension (`"local-history.enabled": false`) to prevent `.history` from continually repopulating.
- Add `.history` to the explorer exclusion list.

## DEBUGGING

## WORKFLOW & RELEASE RULES
