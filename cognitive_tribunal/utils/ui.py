"""
UI Utility Module for Cognitive Archaeology Tribunal.
Provides rich text output capabilities for the CLI.
"""
import sys
from typing import Optional, Any

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.theme import Theme
    from rich.status import Status
except ImportError:
    # Fallback if rich is not installed, though it is a requirement
    class Console:
        def print(self, *args, **kwargs):
            print(*[str(a) for a in args])

        def rule(self, title="", **kwargs):
            print("-" * 70)
            if title:
                print(title.center(70))
                print("-" * 70)

        def status(self, status: str):
            print(f"status: {status}")
            return self

        def __enter__(self): return self
        def __exit__(self, exc_type, exc_val, exc_tb): pass

    Panel = str
    Text = str
    Theme = lambda x: None
    Status = None

# custom theme
try:
    custom_theme = Theme({
        "info": "cyan",
        "warning": "yellow",
        "error": "bold red",
        "success": "bold green",
        "header": "bold magenta",
        "section": "bold blue",
    })
    console = Console(theme=custom_theme)
except Exception:
    # Fallback if Theme is mocked or fails
    console = Console()

def print_header(title: str, subtitle: str = ""):
    """Prints a styled header."""
    console.print()
    console.rule(f"[header]{title}[/header]")
    if subtitle:
        console.print(f"[dim]{subtitle}[/dim]", justify="center")
    console.print()

def print_section(title: str):
    """Prints a section divider."""
    console.print()
    console.rule(f"[section]{title}[/section]", align="left")
    console.print()

def print_success(message: str):
    """Prints a success message."""
    console.print(f"[success]✓[/success] {message}")

def print_error(message: str):
    """Prints an error message."""
    console.print(f"[error]✗ {message}[/error]")

def print_info(message: str):
    """Prints an info message."""
    console.print(f"[info]ℹ[/info] {message}")

def print_step(current: int, total: int, message: str):
    """Prints a step indicator."""
    console.print(f"[bold cyan][{current}/{total}][/bold cyan] {message}")
