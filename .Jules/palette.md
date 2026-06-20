## 2024-05-22 - Empty State for CLI Tools
**Learning:** Users often run CLI tools without arguments to "test" them or see what happens. The default `argparse` error "error: the following arguments are required" is technically correct but feels like a slap on the wrist. A rich, welcoming "empty state" that acts as a landing page is much friendlier and guides the user to success.
**Action:** When detecting no arguments in CLI tools, intercept the error and display a styled "Welcome" screen with common examples and a clear description of what the tool does, rather than just an error message.
