# Palette's Journal

## 2025-02-18 - [CLI Empty State Enhancement]
**Learning:** Users often run CLI tools without arguments to see what happens. Providing a friendly, styled "empty state" instead of a raw error creates a much more welcoming and professional first impression.
**Action:** When designing CLIs, always intercept the "no args" case to show a helpful welcome screen with examples, rather than letting the argument parser throw a generic error.
