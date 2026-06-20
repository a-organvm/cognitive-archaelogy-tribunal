def show_welcome_message():
    """Displays a styled welcome message when no arguments are provided."""
    try:
        from rich.console import Console
        from rich.panel import Panel
        from rich.markdown import Markdown

        console = Console()

        title = "[bold cyan]Cognitive Archaeology Tribunal[/bold cyan]"
        subtitle = "[italic]Digital Preservation & Analysis Suite[/italic]"

        content = """
Welcome to the Cognitive Archaeology Tribunal!

This tool helps you analyze, preserve, and understand your digital footprint across:
• 📁 **Local Archives** (File systems, backups)
• 🧠 **AI Context** (ChatGPT exports)
• 💻 **Code Repositories** (GitHub Personal & Org)
• 🔖 **Web Bookmarks** (Browser exports)

**Quick Start Examples:**

1. **Scan a local archive:**
   `python main.py --scan-archives ./my_archive`

2. **Analyze personal GitHub repos:**
   `python main.py --personal-repos myusername`

3. **Run full suite:**
   `python main.py --all --output-dir ./report`

Run `python main.py --help` for full documentation.
"""

        panel = Panel(
            Markdown(content),
            title=title,
            subtitle=subtitle,
            border_style="blue",
            padding=(1, 2)
        )

        console.print(panel)
        sys.exit(0)

    except ImportError:
        # Fallback for when rich is not installed
        print("=" * 70)
        print("COGNITIVE ARCHAEOLOGY TRIBUNAL")
        print("Comprehensive Archaeological Dig Tool")
        print("=" * 70)
        print("\nNo modules specified.")
        print("Run 'python main.py --help' for usage information.")
        sys.exit(0)
