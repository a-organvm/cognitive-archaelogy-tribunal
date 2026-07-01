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

- **DO NOT** consolidate hidden folders (`.history`, `.trunk`, `.venv`, `.vscode`, `.github`, `.specstory`) into a `.config` directory.
- These folders must remain at workspace root because tools expect them at their default paths.
- Moving them causes continuous regeneration as tools recreate them at expected locations.

## VS CODE SETTINGS

- Disable the Local History extension (`"local-history.enabled": false`) to prevent `.history` from continually repopulating.
- Add `.history` to the explorer exclusion list.

## DEBUGGING

## WORKFLOW & RELEASE RULES
