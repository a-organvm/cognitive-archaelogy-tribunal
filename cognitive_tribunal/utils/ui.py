"""
UI Utilities for Cognitive Archaeology Tribunal.
Handles CLI output with rich formatting if available.
"""
import sys
import re
from contextlib import contextmanager

class MockConsole:
    def _strip_tags(self, text):
        # Strip rich tags like [bold], [/bold], [cyan], etc.
        return re.sub(r'\[/?[a-z0-9\s]+\]', '', str(text))

    def print(self, *args, **kwargs):
        # Basic print, stripping tags
        print(*[self._strip_tags(a) for a in args])

    def rule(self, title="", **kwargs):
        width = 70
        title = self._strip_tags(title)
        if title:
            print(f"{title:-^{width}}")
        else:
            print("-" * width)

    @contextmanager
    def status(self, label, **kwargs):
        print(f"Working: {self._strip_tags(label)}...")
        yield
        print("Done.")

try:
    from rich.console import Console
    from rich.theme import Theme
    from rich.panel import Panel

    custom_theme = Theme({
        "info": "dim cyan",
        "warning": "magenta",
        "error": "bold red",
        "success": "bold green",
    })

    console = Console(theme=custom_theme)

except ImportError:
    console = MockConsole()
    Panel = None
