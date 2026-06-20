#!/usr/bin/env python3
"""
Cognitive Archaeology Tribunal - Main CLI
Command-line interface for running the complete audit suite.
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Optional

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from cognitive_tribunal.modules.archive_scanner import ArchiveScanner
from cognitive_tribunal.modules.ai_context_aggregator import AIContextAggregator
from cognitive_tribunal.modules.personal_repo_analyzer import PersonalRepoAnalyzer
from cognitive_tribunal.modules.org_repo_analyzer import OrgRepoAnalyzer
from cognitive_tribunal.modules.web_bookmark_analyzer import WebBookmarkAnalyzer
from cognitive_tribunal.outputs.inventory import InventoryGenerator
from cognitive_tribunal.outputs.knowledge_graph import KnowledgeGraphGenerator
from cognitive_tribunal.outputs.triage_report import TriageReportGenerator


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description='Cognitive Archaeology Tribunal - Comprehensive digital archaeology tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run all modules
  python main.py --all --output-dir ./output
  
  # Scan archives only
  python main.py --scan-archives /path/to/archives --output-dir ./output
  
  # Analyze personal repos
  python main.py --personal-repos username --output-dir ./output
  
  # Analyze org repos
  python main.py --org-repos orgname --output-dir ./output
  
  # Load AI conversations
  python main.py --ai-conversations /path/to/chatgpt/export --output-dir ./output
        """
    )
    
    # Module selection
    parser.add_argument('--all', action='store_true', help='Run all modules (requires other arguments)')
    parser.add_argument('--scan-archives', metavar='PATH', help='Scan archive directories (comma-separated paths)')
    parser.add_argument('--ai-conversations', metavar='PATH', help='Load AI conversations from path')
    parser.add_argument('--personal-repos', metavar='USERNAME', help='Analyze personal GitHub repos')
    parser.add_argument('--org-repos', metavar='ORGNAME', help='Analyze organization GitHub repos')
    parser.add_argument('--web-bookmarks', metavar='PATH', help='Analyze web bookmarks from an export file')
    
    # Configuration
    parser.add_argument('--github-token', help='GitHub personal access token (or use GITHUB_TOKEN env var)')
    parser.add_argument('--output-dir', default='./output', help='Output directory (default: ./output)')
    parser.add_argument('--no-inventory', action='store_true', help='Skip inventory generation')
    parser.add_argument('--no-graph', action='store_true', help='Skip knowledge graph generation')
    parser.add_argument('--no-triage', action='store_true', help='Skip triage report generation')
    
    args = parser.parse_args()
    
    # Validate arguments
    if not (args.all or args.scan_archives or args.ai_conversations or args.personal_repos or args.org_repos or args.web_bookmarks):
        # Empty State: Try to show a rich welcome panel if no args provided
        try:
            from rich.console import Console
            from rich.panel import Panel
            from rich.markdown import Markdown

            console = Console()

            welcome_md = """
# Welcome to Cognitive Archaeology Tribunal

Your digital preservation and audit companion. This tool helps you:

* 🔍 **Scan Archives**: Analyze file structures and duplicates
* 🤖 **AI Context**: Aggregate conversations from AI exports
* 💻 **GitHub Analysis**: Audit personal and organizational repositories
* 🔖 **Bookmarks**: Analyze web bookmarks

## Quick Start

Run with specific modules:

```bash
python main.py --scan-archives ./my-data --output-dir ./report
python main.py --personal-repos myusername
```

For full help, run: `python main.py --help`
            """

            console.print(Panel(
                Markdown(welcome_md),
                title="🎨 [bold magenta]Cognitive Archaeology Tribunal[/bold magenta]",
                border_style="cyan",
                expand=False
            ))
            sys.exit(0)

        except ImportError:
            # Fallback for when rich is not available
            parser.error('At least one module must be specified')
    
    print("=" * 70)
    print("COGNITIVE ARCHAEOLOGY TRIBUNAL")
    print("Comprehensive Archaeological Dig Tool")
    print("=" * 70)
    print()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize results storage
    results = {}
    
    # Module 1: Archive Scanner
    if args.scan_archives:
        print("\n[1/4] Running Archive Scanner...")
        print("-" * 70)
        
        scanner = ArchiveScanner()
        paths = [p.strip() for p in args.scan_archives.split(',')]
        
        if len(paths) == 1:
            archive_results = scanner.scan_directory(paths[0])
        else:
            archive_results = scanner.scan_multiple_locations(paths)
        
        results['archives'] = archive_results
        
        # Save module results
        import json
        with open(output_dir / 'archives.json', 'w') as f:
            json.dump(archive_results, f, indent=2)
        
        print(f"✓ Archive scan complete. Found {archive_results.get('stats', {}).get('total_files', 0)} files")
    
    # Module 2: AI Context Aggregator
    if args.ai_conversations:
        print("\n[2/4] Running AI Context Aggregator...")
        print("-" * 70)
        
        aggregator = AIContextAggregator()
        ai_results = aggregator.load_chatgpt_export(args.ai_conversations)
        results['ai_conversations'] = aggregator.get_results()
        
        # Save module results
        import json
        with open(output_dir / 'ai_conversations.json', 'w') as f:
            json.dump(results['ai_conversations'], f, indent=2)
        
        print(f"✓ AI context aggregation complete. Loaded {ai_results.get('loaded_count', 0)} conversations")
    
    # Module 3: Personal Repo Analyzer
    if args.personal_repos:
        print("\n[3/4] Running Personal Repo Analyzer...")
        print("-" * 70)
        
        try:
            analyzer = PersonalRepoAnalyzer(args.github_token)
            repo_results = analyzer.analyze_user_repos(args.personal_repos)
            results['personal_repos'] = repo_results
            
            # Save module results
            import json
            with open(output_dir / 'personal_repos.json', 'w') as f:
                json.dump(repo_results, f, indent=2)
            
            print(f"✓ Personal repo analysis complete. Analyzed {repo_results.get('stats', {}).get('total_repos', 0)} repositories")
        except Exception as e:
            print(f"✗ Error analyzing personal repos: {e}")
    
    # Module 4: Org Repo Analyzer
    if args.org_repos:
        print("\n[4/4] Running Org Repo Analyzer...")
        print("-" * 70)
        
        try:
            analyzer = OrgRepoAnalyzer(args.github_token)
            org_results = analyzer.analyze_org_repos(args.org_repos)
            results['org_repos'] = org_results
            
            # Save module results
            import json
            with open(output_dir / 'org_repos.json', 'w') as f:
                json.dump(org_results, f, indent=2)
            
            print(f"✓ Org repo analysis complete. Analyzed {org_results.get('stats', {}).get('total_repos', 0)} repositories")
        except Exception as e:
            print(f"✗ Error analyzing org repos: {e}")
    
    # Module 5: Web Bookmark Analyzer
    if args.web_bookmarks:
        print("\n[5/5] Running Web Bookmark Analyzer...")
        print("-" * 70)

        analyzer = WebBookmarkAnalyzer()
        bookmark_results = analyzer.analyze_bookmarks(args.web_bookmarks)
        results['web_bookmarks'] = bookmark_results

        # Save module results
        import json
        with open(output_dir / 'web_bookmarks.json', 'w') as f:
            json.dump(bookmark_results, f, indent=2)

        print(f"✓ Web bookmark analysis complete. Found {bookmark_results.get('stats', {}).get('total_bookmarks', 0)} bookmarks")

    # Generate unified outputs
    print("\n" + "=" * 70)
    print("GENERATING OUTPUTS")
    print("=" * 70)
    
    # Unified Inventory
    if not args.no_inventory:
        print("\nGenerating unified inventory...")
        inventory = InventoryGenerator()
        
        if 'archives' in results:
            inventory.add_archive_results(results['archives'])
        if 'ai_conversations' in results:
            inventory.add_ai_context_results(results['ai_conversations'])
        if 'personal_repos' in results:
            inventory.add_personal_repo_results(results['personal_repos'])
        if 'org_repos' in results:
            inventory.add_org_repo_results(results['org_repos'])
        if 'web_bookmarks' in results:
            # This method needs to be added to the InventoryGenerator class
            # For now, we'll just conceptually add it.
            # inventory.add_web_bookmark_results(results['web_bookmarks'])
            pass
        
        inventory.save_to_file(str(output_dir / 'inventory.json'))
        print("✓ Inventory saved")
    
    # Knowledge Graph
    if not args.no_graph:
        print("\nGenerating knowledge graph...")
        graph = KnowledgeGraphGenerator()
        
        if not args.no_inventory:
            graph.build_from_inventory(inventory.get_inventory())
            graph.save_to_file(str(output_dir / 'knowledge_graph.json'))
            graph.export_to_cytoscape(str(output_dir / 'knowledge_graph_cytoscape.json'))
            print("✓ Knowledge graph saved")
    
    # Triage Report
    if not args.no_triage:
        print("\nGenerating triage report...")
        triage = TriageReportGenerator()
        
        if 'archives' in results:
            triage.add_archive_triage(results['archives'])
        if 'ai_conversations' in results:
            triage.add_ai_context_triage(results['ai_conversations'])
        if 'personal_repos' in results:
            triage.add_personal_repo_triage(results['personal_repos'])
        if 'org_repos' in results:
            triage.add_org_repo_triage(results['org_repos'])
        if 'web_bookmarks' in results:
            # This method needs to be added to the TriageReportGenerator class
            # For now, we'll just conceptually add it.
            # triage.add_web_bookmark_triage(results['web_bookmarks'])
            pass
        
        triage.save_to_file(str(output_dir / 'triage_report.json'))
        
        # Also save as text
        with open(output_dir / 'triage_report.txt', 'w') as f:
            f.write(triage.generate_text_report())
        
        print("✓ Triage report saved")
    
    # Final summary
    print("\n" + "=" * 70)
    print("COMPLETE!")
    print("=" * 70)
    print(f"\nAll outputs saved to: {output_dir.absolute()}")
    print("\nGenerated files:")
    for file in sorted(output_dir.glob('*')):
        print(f"  - {file.name}")
    print()


if __name__ == '__main__':
    main()
