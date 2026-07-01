# Usage Guide

## Table of Contents
1. [Installation](#installation)
2. [Basic Usage](#basic-usage)
3. [Module Details](#module-details)
4. [Configuration](#configuration)
5. [Output Formats](#output-formats)
6. [Examples](#examples)

## Installation

### Using pip (recommended)
```bash
pip install -e .
```

### Manual installation
```bash
pip install -r requirements.txt
```

### Setting up GitHub Token
For GitHub repository analysis, you'll need a personal access token:

1. Go to https://github.com/settings/tokens
2. Generate a new token with `repo` scope
3. Set the environment variable:
   ```bash
   export GITHUB_TOKEN="your_token_here"
   ```

## Basic Usage

### Command Line Interface

Run the main script with desired modules:

```bash
python main.py [OPTIONS]
```

#### Options:
- `--scan-archives PATH` - Scan archive directories
- `--ai-conversations PATH` - Load AI conversations
- `--personal-repos USERNAME` - Analyze personal GitHub repos
- `--org-repos ORGNAME` - Analyze organization repos
- `--web-bookmarks PATH` - Analyze web bookmarks from an export file
- `--github-token TOKEN` - GitHub token (or use GITHUB_TOKEN env var)
- `--output-dir DIR` - Output directory (default: ./output)
- `--no-inventory` - Skip inventory generation
- `--no-graph` - Skip knowledge graph generation
- `--no-triage` - Skip triage report generation

### Programmatic Usage

```python
from cognitive_tribunal import (
    ArchiveScanner,
    AIContextAggregator,
    PersonalRepoAnalyzer,
    OrgRepoAnalyzer,
    WebBookmarkAnalyzer
)

# Archive scanning
scanner = ArchiveScanner()
results = scanner.scan_directory('/path/to/archives')
duplicates = scanner.deduplicator.find_duplicates()

# AI conversations
aggregator = AIContextAggregator()
aggregator.load_chatgpt_export('/path/to/export')
conversations = aggregator.get_results()

# Personal repos
analyzer = PersonalRepoAnalyzer(github_token='your_token')
repos = analyzer.analyze_user_repos('username')
triage = analyzer.generate_triage_report()

# Organization repos
org_analyzer = OrgRepoAnalyzer(github_token='your_token')
org_repos = org_analyzer.analyze_org_repos('org-name')
health = org_analyzer.generate_health_report()
```

## Module Details

### Module 1: Archive Scanner

Scans file systems and identifies:
- File types and categories
- Duplicate files (content-based)
- Large files
- Old/unused files

**Supported Storage:**
- Local directories
- Network drives
- iCloud Drive mounts
- Dropbox folders
- Any accessible file system

**Example:**
```bash
python main.py --scan-archives "~/Documents,~/Dropbox" --output-dir ./output
```

### Module 2: AI Context Aggregator

Processes AI conversation exports:
- ChatGPT conversation exports
- Generic JSON conversation formats
- Message extraction and parsing
- Topic identification

**ChatGPT Export Format:**
The tool expects ChatGPT's native export format with `mapping` structure. To export:
1. Go to ChatGPT settings
2. Data Controls → Export data
3. Wait for email with download link
4. Extract and point tool to `conversations.json`

**Example:**
```bash
python main.py --ai-conversations "/path/to/chatgpt/export" --output-dir ./output
```

### Module 3: Personal Repo Analyzer

Analyzes personal GitHub repositories:
- Fork detection
- Modification tracking in forks
- Repository activity metrics
- Language statistics
- Triage recommendations

**Example:**
```bash
export GITHUB_TOKEN="your_token"
python main.py --personal-repos your-username --output-dir ./output
```

### Module 4: Org Repo Analyzer

Analyzes organization repositories:
- Status tracking (active/stale/abandoned/archived)
- Health scoring
- Dependency detection
- Migration planning
- Issue tracking

**Example:**
```bash
export GITHUB_TOKEN="your_token"
python main.py --org-repos your-org --output-dir ./output
```

### Module 5: Web Bookmark Analyzer

Analyzes web bookmark export files:
- Parses Netscape Bookmark File Format
- Extracts URLs, titles, and creation dates
- Provides statistics on bookmark collections

**Example:**
```bash
python main.py --web-bookmarks /path/to/bookmarks.html --output-dir ./output
```

## Configuration

### Using config.yaml

Create a `config.yaml` from the example:

```bash
cp config.example.yaml config.yaml
```

Edit the file with your settings:

```yaml
github:
  token: "${GITHUB_TOKEN}"

archives:
  locations:
    - "/path/to/iCloud/Drive"
    - "/path/to/Dropbox"
  exclude_patterns:
    - "__pycache__"
    - ".git"
    - "node_modules"

personal_repos:
  username: "your-github-username"
  
org_repos:
  organizations:
    - "org-name-1"

output:
  directory: "./output"
  generate:
    inventory: true
    knowledge_graph: true
    triage_report: true
```

## Output Formats

### 1. Unified Inventory (inventory.json)

Complete catalog of all discovered assets:
- File statistics and metadata
- Conversation summaries
- Repository information
- Cross-module statistics

### 2. Knowledge Graph

Two formats:
- `knowledge_graph.json` - Native format
- `knowledge_graph_cytoscape.json` - Cytoscape.js compatible

Visualizes relationships between:
- File categories
- Conversation sources
- Repository dependencies
- Project connections

### 3. Triage Report

Two formats:
- `triage_report.json` - Structured data
- `triage_report.txt` - Human-readable

Prioritized action items:
- **High Priority**: Duplicates, abandoned repos with issues
- **Medium Priority**: Unmodified forks, stale repos
- **Low Priority**: Inactive projects, archiving suggestions

### 4. Module-Specific Outputs

Each module generates detailed JSON:
- `archives.json` - Complete file inventory with deduplication
- `ai_conversations.json` - Conversation catalog with messages
- `personal_repos.json` - Repository analysis with metrics
- `org_repos.json` - Organization health and dependencies
- `web_bookmarks.json` - Web bookmark analysis

## Examples

### Example 1: Local Archive Audit
```bash
python main.py \
  --scan-archives "~/Documents,~/Downloads" \
  --output-dir ./archive-audit
```

### Example 2: AI Conversation Analysis
```bash
python main.py \
  --ai-conversations "~/Downloads/chatgpt-export" \
  --output-dir ./ai-analysis
```

### Example 3: Personal GitHub Cleanup
```bash
export GITHUB_TOKEN="ghp_yourtoken"
python main.py \
  --personal-repos your-username \
  --output-dir ./github-cleanup
```

### Example 4: Organization Health Check
```bash
export GITHUB_TOKEN="ghp_yourtoken"
python main.py \
  --org-repos your-org \
  --output-dir ./org-health
```

### Example 5: Complete Digital Archaeology
```bash
export GITHUB_TOKEN="ghp_yourtoken"
python main.py \
  --scan-archives "~/Documents" \
  --ai-conversations "~/Downloads/chatgpt-export" \
  --personal-repos your-username \
  --org-repos your-org \
  --output-dir ./complete-audit
```

### Example 6: Skip Specific Outputs
```bash
python main.py \
  --scan-archives "/path/to/archives" \
  --no-graph \
  --no-triage \
  --output-dir ./inventory-only
```

## Advanced Usage

### Custom Exclude Patterns

When using programmatically:

```python
from cognitive_tribunal.modules.archive_scanner import ArchiveScanner

scanner = ArchiveScanner(exclude_patterns=[
    '__pycache__',
    '.git',
    'node_modules',
    '*.tmp',
    '*.swp',
    '.DS_Store',
    'Thumbs.db',
    'venv',
    '.venv',
])

results = scanner.scan_directory('/path/to/scan')
```

### Filtering Results

```python
# Get specific file categories
code_files = scanner.get_files_by_category('code')
documents = scanner.get_files_by_category('document')

# Get large files
large_files = scanner.get_large_files(min_size_mb=10.0)

# Get old files
old_files = scanner.get_old_files(days_old=365)

# Get duplicates
duplicates = scanner.deduplicator.find_duplicates()
```

### Search Conversations

```python
from cognitive_tribunal.modules.ai_context_aggregator import AIContextAggregator

aggregator = AIContextAggregator()
aggregator.load_chatgpt_export('/path/to/export')

# Search by keyword
python_convs = aggregator.search_conversations('python')

# Filter by date
from datetime import datetime
recent = aggregator.get_conversations_by_date_range(
    start_date=datetime(2023, 1, 1),
    end_date=datetime(2023, 12, 31)
)

# Extract topics
topics = aggregator.extract_topics(min_conversations=2)
```

### Repository Filtering

```python
from cognitive_tribunal.modules.personal_repo_analyzer import PersonalRepoAnalyzer

analyzer = PersonalRepoAnalyzer(github_token='token')
analyzer.analyze_user_repos('username')

# Get specific repo types
forks = analyzer.get_forks()
originals = analyzer.get_originals()
modified_forks = analyzer.get_modified_forks()
unmodified_forks = analyzer.get_unmodified_forks()
archived = analyzer.get_archived_repos()
active = analyzer.get_active_repos()

# Filter by language
python_repos = analyzer.get_repos_by_language('Python')
```

## Troubleshooting

### GitHub API Rate Limits

If you see rate limit errors:
1. Use a GitHub token (authenticated requests have higher limits)
2. Wait for the rate limit to reset
3. Reduce the number of repos being analyzed

### File Permission Errors

If you get permission denied errors:
1. Check file/directory permissions
2. Run with appropriate user privileges
3. Add paths to exclude patterns if needed

### Large Archive Scans

For very large archives:
1. Limit scan depth with `max_depth` parameter
2. Use exclude patterns to skip large directories
3. Run scans on smaller subsets

### Memory Usage

For large datasets:
1. Process modules separately instead of all at once
2. Use `--no-graph` to skip graph generation
3. Clear output directory between runs

## Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/ivi374forivi/cognitive-archaelogy-tribunal/issues
- See CONTRIBUTING.md for contribution guidelines
