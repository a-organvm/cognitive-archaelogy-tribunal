## 2024-05-24 - Empty State Pattern for CLIs
**Learning:** Users often run a CLI without arguments to see what happens. Showing a harsh "error: missing arguments" is a missed opportunity. A "Welcome Panel" (Empty State) that explains the tool and provides quick-start examples significantly improves perceived quality and approachability.
**Action:** For all CLI entry points, check for empty `sys.argv` and display a styled `rich` panel with usage examples instead of an error trace.
