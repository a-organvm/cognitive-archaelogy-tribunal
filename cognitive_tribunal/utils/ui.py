"""
UI helper module for Cognitive Tribunal.
Provides rich output capabilities with fallback to standard print.
"""

import sys
from typing import Optional, Any
from contextlib import contextmanager

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.status import Status
    from rich.tree import Tree
    from rich.text import Text
    from rich.table import Table
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


class UI:
    """User Interface helper."""

    def __init__(self):
        if RICH_AVAILABLE:
            self.console = Console()
        else:
            self.console = None

    def print(self, *args, **kwargs):
        """Print message to console."""
        if RICH_AVAILABLE and self.console:
            self.console.print(*args, **kwargs)
        else:
            # Strip styles for plain text fallback if passed as separate args
            # Simple fallback for now
            print(*args)

    def print_header(self, title: str, subtitle: str = ""):
        """Print a styled header."""
        if RICH_AVAILABLE and self.console:
            content = Text(title, style="bold cyan")
            if subtitle:
                content.append("\n" + subtitle, style="italic white")
            self.console.print(Panel(content, border_style="cyan"))
        else:
            print("=" * 70)
            print(title)
            if subtitle:
                print(subtitle)
            print("=" * 70)
            print()

    def print_step(self, step_num: int, total_steps: int, title: str):
        """Print a step header."""
        if RICH_AVAILABLE and self.console:
            self.console.print(f"\n[bold yellow][{step_num}/{total_steps}] {title}...[/bold yellow]")
            self.console.rule(style="yellow")
        else:
            print(f"\n[{step_num}/{total_steps}] {title}...")
            print("-" * 70)

    def print_success(self, message: str):
        """Print a success message."""
        if RICH_AVAILABLE and self.console:
            self.console.print(f"[bold green]✓ {message}[/bold green]")
        else:
            print(f"✓ {message}")

    def print_error(self, message: str):
        """Print an error message."""
        if RICH_AVAILABLE and self.console:
            self.console.print(f"[bold red]✗ {message}[/bold red]")
        else:
            print(f"✗ {message}")

    def print_section(self, title: str):
        """Print a section header."""
        if RICH_AVAILABLE and self.console:
            self.console.print(f"\n[bold cyan]{title}[/bold cyan]")
            self.console.rule(style="cyan")
        else:
            print(f"\n{title}")
            print("-" * 70)

    @contextmanager
    def status(self, message: str):
        """Show a status spinner during an operation."""
        if RICH_AVAILABLE and self.console:
            with self.console.status(message, spinner="dots"):
                yield
        else:
            print(f"  {message}...", end="", flush=True)
            try:
                yield
                print(" Done.")
            except Exception:
                print(" Failed.")
                raise

    def print_list(self, items: list, title: str = ""):
        """Print a list of items."""
        if RICH_AVAILABLE and self.console:
            if title:
                self.console.print(f"\n[bold]{title}[/bold]")
            for item in items:
                self.console.print(f"  • {item}")
        else:
            if title:
                print(f"\n{title}")
            for item in items:
                print(f"  - {item}")
