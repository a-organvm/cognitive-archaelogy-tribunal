"""
UI utilities for Console output using Rich.
"""
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def print_header(title: str, subtitle: str = ""):
    """Print a styled header."""
    content = Text(title, justify="center", style="bold blue")
    if subtitle:
        content.append("\n" + subtitle, style="italic cyan")
    console.print(Panel.fit(content, border_style="blue"))
    console.print()

def print_step(message: str):
    """Print a step message."""
    console.print(f"\n[bold cyan]{message}[/bold cyan]")
    console.rule(style="cyan")

def print_success(message: str):
    """Print a success message."""
    console.print(f"[green]✓ {message}[/green]")

def print_error(message: str):
    """Print an error message."""
    console.print(f"[bold red]✗ {message}[/bold red]")

def print_warning(message: str):
    """Print a warning message."""
    console.print(f"[bold yellow]! {message}[/bold yellow]")
