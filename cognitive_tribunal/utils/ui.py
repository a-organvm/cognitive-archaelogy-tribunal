"""
UI utilities for the Cognitive Tribunal project.
Handles terminal output with graceful fallback for rich text.
"""

import sys
import re

# Try to import rich, otherwise define fallbacks
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.theme import Theme

    custom_theme = Theme({
        "info": "dim cyan",
        "warning": "magenta",
        "error": "bold red",
        "success": "bold green",
        "header": "bold blue",
    })
    console = Console(theme=custom_theme)

except ImportError:
    # Fallback for environments without rich
    def strip_rich_tags(text):
        # Strip rich markup tags but preserve [1/4]
        return re.sub(r'\[(?!\d+/\d+)[^\]]+\]', '', str(text))

    class MockStatus:
        def __init__(self, message, **kwargs):
            self.message = strip_rich_tags(message)
        def __enter__(self):
            print(f"{self.message}...")
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

    class MockPanel:
        def __init__(self, renderable, **kwargs):
            self.renderable = renderable

        def __str__(self):
            return strip_rich_tags(self.renderable)

        @classmethod
        def fit(cls, renderable, **kwargs):
            return cls(renderable)

    class MockConsole:
        def print(self, *args, **kwargs):
            text = " ".join(str(a) for a in args)
            print(strip_rich_tags(text))

        def status(self, message, **kwargs):
            return MockStatus(message)

    console = MockConsole()
    Panel = MockPanel
