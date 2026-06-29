## 2024-05-24 - Empty State for CLI
**Learning:** CLI tools often lack an "Empty State". When run without args, they just show a dry error.
**Action:** Always intercept `len(sys.argv) == 1` and show a friendly "Welcome Panel" using `rich` or similar, guiding the user on what to do next. This transforms an error into an invitation.
