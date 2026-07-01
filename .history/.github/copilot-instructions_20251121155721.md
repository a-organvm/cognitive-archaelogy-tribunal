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

*   All configuration folders are consolidated in `.config/` directory:
    *   `.config/.venv` - Python virtual environment
    *   `.config/.vscode` - VS Code settings
    *   `.config/.trunk` - Trunk.io configuration
    *   `.config/.history` - Local file history
    *   `.config/.github` - GitHub configuration
    *   `.config/.specstory` - SpecStory configuration
*   Symlinks at workspace root maintain tool compatibility:
    *   `.venv` → `.config/.venv`
    *   `.vscode` → `.config/.vscode`
    *   `.trunk` → `.config/.trunk`
    *   `.github` → `.config/.github`
    *   `.specstory` → `.config/.specstory`
*   Both `.config/` directory and symlinks are gitignored.

## VS CODE SETTINGS

- Disable the Local History extension (`"local-history.enabled": false`) to prevent `.history` from continually repopulating.
- Add `.history` to the explorer exclusion list.

## DEBUGGING

## WORKFLOW & RELEASE RULES
