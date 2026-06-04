[![ORGAN-I: Theory](https://img.shields.io/badge/ORGAN--I-Theory-1a237e?style=flat-square)](https://github.com/organvm-i-theoria) [![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](./LICENSE)

# Cognitive Archaeology Tribunal

[![CI](https://github.com/organvm-i-theoria/cognitive-archaelogy-tribunal/actions/workflows/ci.yml/badge.svg)](https://github.com/organvm-i-theoria/cognitive-archaelogy-tribunal/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-pending-lightgrey)](https://github.com/organvm-i-theoria/cognitive-archaelogy-tribunal)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/organvm-i-theoria/cognitive-archaelogy-tribunal/blob/main/LICENSE)
[![Organ I](https://img.shields.io/badge/Organ-I%20Theoria-8B5CF6)](https://github.com/organvm-i-theoria)
[![Status](https://img.shields.io/badge/status-active-brightgreen)](https://github.com/organvm-i-theoria/cognitive-archaelogy-tribunal)
[![Python](https://img.shields.io/badge/lang-Python-informational)](https://github.com/organvm-i-theoria/cognitive-archaelogy-tribunal)


**A systematic excavation engine that audits every layer of a creator's digital footprint — archives, AI conversations, personal repositories, organisation repositories, and web bookmarks — and produces a unified inventory, a knowledge graph of relationships, and a prioritised triage report that transforms scattered creative history into an organised system foundation.**

---

## Name Explanation

**Cognitive Archaeology** refers to the practice of excavating layers of thought. Just as physical archaeology digs through strata of soil to reconstruct civilisations, cognitive archaeology digs through strata of digital artefacts — conversation logs, code repositories, cloud archives, browser bookmarks — to reconstruct the intellectual history of a creative practice. Each layer carries its own temporal signature, its own logic, and its own relationship to the layers above and below it.

**Tribunal** carries the dual meaning of judgment and adjudication. The tool does not merely inventory what it finds; it renders verdicts. Every artefact passes through triage: what survives into the organised system, what gets archived, what gets merged, and what gets discarded. The tribunal metaphor reflects the epistemological seriousness of the task — deciding what knowledge is worth preserving is itself an act of knowledge-making.

Together, the name describes a system that excavates cognitive strata and adjudicates what survives the transition from chaos to order.

---

## Table of Contents

- [Problem Statement](#problem-statement)
- [Core Concepts](#core-concepts)
- [Architecture](#architecture)
- [Module Reference](#module-reference)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Output Formats](#output-formats)
- [Downstream Implementation](#downstream-implementation)
- [Validation](#validation)
- [Roadmap](#roadmap)
- [Cross-References](#cross-references)
- [Contributing](#contributing)
- [License](#license)
- [Author & Contact](#author--contact)

---

## Problem Statement

Any sufficiently long creative practice accumulates entropy. Years of work produce scattered artefacts across incompatible systems: hundreds of AI conversation threads (ChatGPT, Claude, Gemini) containing architectural decisions that were never extracted; personal GitHub repositories that are really evaluation forks of external tools, not original work, but mixed indistinguishably with originals; cloud storage directories (iCloud, Dropbox, network drives) containing duplicated files across multiple locations with no canonical version; browser bookmark collections numbering in the thousands with no topical organisation; and organisation repositories that may be active, stale, or silently abandoned.

The fundamental problem is not storage — storage is cheap. The problem is **epistemic**: you cannot govern what you cannot see. Before the eight-organ system could be designed, before repositories could be assigned to organisations, before any architectural decision could be made, someone had to answer the question: *what do we actually have?*

Manual inventory is not viable at scale. A human scanning 85 repositories, thousands of archived files, and hundreds of AI conversations would take weeks and produce an incomplete, error-prone result. The Cognitive Archaeology Tribunal exists to answer this question programmatically, comprehensively, and repeatedly. It scans every layer of a creator's digital footprint — from local filesystem archives through GitHub API endpoints — and produces machine-readable outputs (JSON inventories, knowledge graphs, triage reports) that downstream tools and human reviewers can act on.

This is not a backup tool or a file manager. It is a **pre-governance audit system** — the epistemological foundation that makes governance possible. Within ORGAN-I (Theoria), it embodies the principle that theory begins with accurate observation. You cannot theorise about a system you have not first measured.

---

## Core Concepts

### Multi-Layer Auditing

The tribunal models a creator's digital footprint as four discrete layers, each with its own scanning module, data model, and triage logic:

| Layer | Domain | Scanner Module | Key Metric |
|-------|--------|---------------|------------|
| **Layer 0** | Filesystem archives (iCloud, Dropbox, local/network drives) | `ArchiveScanner` | Files counted, duplicates found, space savings |
| **Layer 1** | AI conversation history (ChatGPT, Claude, generic JSON) | `AIContextAggregator` | Conversations loaded, messages parsed, topics extracted |
| **Layer 2** | Personal GitHub repositories | `PersonalRepoAnalyzer` | Repos classified (fork vs. original), modification detection |
| **Layer 3** | Organisation GitHub repositories | `OrgRepoAnalyzer` | Repos by status (active/stale/abandoned), health scoring |
| **Layer 4** | Web bookmarks (Netscape format exports) | `WebBookmarkAnalyzer` | Bookmarks parsed, URLs and timestamps extracted |

Each layer is independently scannable. You can run the archive scanner without touching GitHub, or analyse organisation repos without providing bookmark exports. The unified inventory and knowledge graph only gain cross-layer power when multiple layers are combined, but each layer stands alone as a useful audit.

### Knowledge Graph Generation

Raw inventories are useful but flat. The `KnowledgeGraphGenerator` transforms audit results into a directed graph of nodes (entities) and edges (relationships). Nodes carry type metadata — `repository`, `file_category`, `conversation_source`, `repo_status` — and edges encode relationships like `contains`, `forked_from`, and `has_status`. The graph exports in two formats: a native JSON structure for programmatic consumption and a Cytoscape.js-compatible format for interactive visualisation.

The knowledge graph enables queries that no single module can answer alone: "Which AI conversations relate to repositories that are currently stale?" or "Which archive categories overlap with active org repositories?" These cross-layer queries are the tribunal's primary analytical value.

### Triage and Prioritisation

The `TriageReportGenerator` converts raw audit data into prioritised action items across three tiers — high, medium, and low priority. Triage logic is domain-specific per layer:

- **Archives:** Duplicate files flagged as high priority (quantified by wasted disk space); large or old files flagged for review.
- **AI Conversations:** Collections exceeding 100 conversations flagged for topical organisation.
- **Personal Repos:** Unmodified forks flagged for deletion (they can be re-forked); inactive originals flagged for archival.
- **Org Repos:** Abandoned repositories (no updates in 180+ days) flagged as high priority; stale repositories (30-180 days) flagged as medium.

The triage report generates both JSON (for downstream automation) and plain-text (for human review) output formats. The text report is structured as an executive summary suitable for reading in a terminal or including in planning documents.

### Deduplication Engine

The `Deduplicator` class within `file_utils.py` implements a two-pass deduplication strategy. The first pass groups files by size — an O(1) lookup that eliminates most non-duplicates without reading file contents. The second pass computes SHA-256 content hashes only for files that share a size, avoiding expensive hashing for unique files. This approach scales to large archives (the roadmap targets 1M+ files) while remaining accurate. The deduplicator reports both the number of duplicate groups and the total space savings achievable by removing redundant copies.

### Fork Classification and Modification Detection

The `PersonalRepoAnalyzer` does not treat all repositories equally. It classifies each repository as `fork`, `template`, `archived`, `private-original`, or `public-original` using the `classify_repo_type` utility. For forks specifically, the `detect_modifications` function compares creation timestamps against push timestamps and checks for the presence of commits beyond the fork point, answering the critical question: *is this fork actively modified, or is it an untouched copy?*

This distinction matters operationally. During the initial audit of 42 personal repositories, 38 were identified as forks — but the reframing that emerged was that these forks were not clutter but an *integration staging area*. The Tribunal's classification data made that reframing possible by quantifying the difference between evaluated forks (with modifications) and untouched forks (candidates for deletion).

---

## Architecture

```
main.py                          # CLI entry point (argparse)
  |
  +-- cognitive_tribunal/
  |     +-- modules/
  |     |     +-- archive_scanner.py        # Layer 0: Filesystem scanning + deduplication
  |     |     +-- ai_context_aggregator.py  # Layer 1: ChatGPT/generic JSON parsing
  |     |     +-- personal_repo_analyzer.py # Layer 2: Personal GitHub repo analysis
  |     |     +-- org_repo_analyzer.py      # Layer 3: Org GitHub repo analysis
  |     |     +-- web_bookmark_analyzer.py  # Layer 4: Netscape bookmark parsing
  |     |
  |     +-- outputs/
  |     |     +-- inventory.py              # Unified inventory generator
  |     |     +-- knowledge_graph.py        # Knowledge graph + Cytoscape export
  |     |     +-- triage_report.py          # Prioritised triage (JSON + text)
  |     |
  |     +-- utils/
  |           +-- file_utils.py             # FileClassifier, FileHasher, Deduplicator
  |           +-- github_utils.py           # GitHubClient wrapper (PyGithub)
  |           +-- metadata.py               # Dublin Core / DataCite metadata
  |
  +-- ingestion/                  # Ingestion chambers (input staging)
  |     +-- ai-exports/           # ChatGPT/Claude export JSON files
  |     +-- archives/             # Filesystem archive path references
  |     +-- bookmarks/            # Netscape-format bookmark HTML exports
  |     +-- browser-tabs/         # Browser session JSON exports
  |
  +-- data/
  |     +-- genesis-conversations/ # 16 indexed genesis conversation JSONs
  |
  +-- scripts/                    # Shell utilities
  |     +-- ingest_all.sh         # Run full ingestion pipeline
  |     +-- sanitize_for_public.sh # Privacy sanitisation for publishing
  |     +-- publish_dataset.sh    # Dataset publication workflow
  |     +-- generate_snapshot.sh  # Point-in-time snapshot generation
  |     +-- convert_genesis_chat.py # Genesis chat format conversion
  |
  +-- context/                    # Historical and planning context
  |     +-- history/              # Genesis transcripts, cognitive OS master plan
  |     +-- planning/             # Ingestion plans, integration queue, task hierarchy
  |
  +-- docs/                       # Documentation
  |     +-- analysis/             # Phase 2 analysis summaries
  |     +-- guides/               # Integration quick start, usage guides
  |     +-- setup/                # GitHub token setup, configuration guides
  |
  +-- output/                     # Generated outputs (.gitignored)
        +-- *.json                # Inventory, knowledge graph, triage report
```

### Data Flow

```
     Sources                    Modules                    Outputs
  +--------------+        +--------------------+    +---------------------+
  | iCloud       |---+    | ArchiveScanner     |-+  |                     |
  | Dropbox      |   +--->| (classify, dedup)  | |  | inventory.json      |
  | Local dirs   |---+    +--------------------+ |  | (unified catalog)   |
  +--------------+        +--------------------+ |  |                     |
  | ChatGPT      |---+    | AIContext          | +->| knowledge_graph     |
  | exports      |   +--->| Aggregator         |-+  | .json + cytoscape   |
  | Claude       |---+    +--------------------+ |  |                     |
  +--------------+        +--------------------+ |  | triage_report       |
  | Personal     |------->| PersonalRepo       |-+  | .json + .txt        |
  | GitHub       |        | Analyzer           | |  |                     |
  +--------------+        +--------------------+ |  | per-module          |
  | Org          |------->+--------------------+ |  | .json files         |
  | GitHub       |        | OrgRepo            |-+  |                     |
  +--------------+        | Analyzer           | |  +---------------------+
  | Bookmark     |------->+--------------------+ |
  | HTML files   |        +--------------------+ |
  +--------------+------->| WebBookmark        |-+
                          | Analyzer           |
                          +--------------------+
```

Each module writes its own per-module JSON output (`archives.json`, `personal_repos.json`, etc.) to the output directory. The three output generators — `InventoryGenerator`, `KnowledgeGraphGenerator`, and `TriageReportGenerator` — then consume these per-module results and produce the unified cross-layer outputs.

---

## Module Reference

### ArchiveScanner

Scans local filesystem directories recursively with configurable depth limits and exclusion patterns. Default exclusions include `.git`, `node_modules`, `__pycache__`, and OS metadata files (`.DS_Store`, `Thumbs.db`). Classifies files into 12 categories (code, document, spreadsheet, image, video, audio, archive, data, database, notebook, config, other) using extension-based matching. Runs the two-pass deduplication engine on all discovered files. Exposes convenience methods for filtering results: `get_files_by_category()`, `get_large_files(min_size_mb)`, `get_old_files(days_old)`.

### AIContextAggregator

Parses ChatGPT conversation exports (JSON with nested `mapping` tree structure) and generic JSON conversation formats. Extracts message content, author roles, and timestamps. Sorts messages chronologically within each conversation. Provides search (`search_conversations(keyword)`), date-range filtering (`get_conversations_by_date_range()`), and topic extraction (`extract_topics()`) using word-frequency analysis across conversation titles.

### PersonalRepoAnalyzer

Uses the `GitHubClient` wrapper around PyGithub to enumerate all repositories for a GitHub username. Classifies each repo by type (fork, template, archived, private-original, public-original). For forks, retrieves parent repository information and runs modification detection. Analyses commit history, dependency files, and activity metrics. Generates a triage report separating unmodified forks (deletion candidates), inactive repos (archival candidates), and active projects.

### OrgRepoAnalyzer

Mirrors the personal analyser but targets GitHub organisation repositories. Adds status determination (active/stale/abandoned/archived) based on time since last update. Generates an organisation health report with a 0-100 health score weighted by the ratio of active to stale/abandoned repos. Produces migration plans with prioritised recommendations. Provides a dependency summary across all organisation repositories.

### WebBookmarkAnalyzer

Parses Netscape Bookmark File Format (the standard export format for Chrome, Firefox, and most browsers). Extracts URLs, titles, and addition timestamps using regex pattern matching. Reports total bookmark counts. Designed as the simplest module — a foundation for future enrichment with domain categorisation and link-rot detection.

---

## Installation

### Prerequisites

- Python 3.8 or later
- A GitHub personal access token with `repo` scope (for GitHub analysis modules)

### Setup

```bash
git clone https://github.com/organvm-i-theoria/cognitive-archaelogy-tribunal.git
cd cognitive-archaelogy-tribunal
pip install -r requirements.txt
```

### Configuration

Copy and edit the example configuration:

```bash
cp config.example.yaml config.yaml
```

The configuration file specifies archive paths, AI export locations, GitHub usernames/organisations, output directory, and exclusion patterns. Alternatively, all parameters can be passed as CLI arguments.

Set your GitHub token as an environment variable:

```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

For token creation instructions, see `docs/setup/GITHUB_TOKEN_SETUP.md`.

---

## Usage

### Full Audit (All Modules)

```bash
python main.py \
  --scan-archives "/path/to/iCloud,/path/to/Dropbox" \
  --ai-conversations /path/to/chatgpt/export \
  --personal-repos your-username \
  --org-repos your-org \
  --web-bookmarks /path/to/bookmarks.html \
  --output-dir ./output
```

### Individual Modules

```bash
# Archive scanning only
python main.py --scan-archives /path/to/archives --output-dir ./output

# AI conversation analysis only
python main.py --ai-conversations /path/to/exports --output-dir ./output

# Personal GitHub repos only
python main.py --personal-repos your-username --output-dir ./output

# Organisation repos only
python main.py --org-repos your-org-name --output-dir ./output

# Web bookmarks only
python main.py --web-bookmarks /path/to/bookmarks.html --output-dir ./output
```

### Selective Output

```bash
# Skip knowledge graph generation
python main.py --personal-repos username --no-graph --output-dir ./output

# Skip triage report
python main.py --org-repos orgname --no-triage --output-dir ./output

# Inventory only (skip graph and triage)
python main.py --scan-archives /path --no-graph --no-triage --output-dir ./output
```

---

## Examples

### Scenario 1: Pre-Governance Audit

Before designing the eight-organ system, we needed a complete picture of what existed. Running the tribunal against both personal and organisation accounts:

```bash
python main.py \
  --personal-repos 4444J99 \
  --org-repos organvm-i-theoria \
  --output-dir ./output/pre-governance-audit
```

This produced a 793KB output set revealing 85 total repositories (42 personal, 43 organisational). The critical insight: 38 of 42 personal repos were forks functioning as an evaluation staging area, not clutter. The triage report quantified this, enabling the reframing that shaped the entire migration strategy.

### Scenario 2: Duplicate Detection Across Cloud Storage

Scanning multiple cloud storage mounts to find wasted space:

```bash
python main.py \
  --scan-archives "/Users/me/Library/Mobile Documents/com~apple~CloudDocs,/Users/me/Dropbox" \
  --output-dir ./output/cloud-dedup
```

The deduplication engine groups files by size first, then computes SHA-256 hashes only for size-colliding files, reporting both the number of duplicate groups and the total recoverable disk space.

### Scenario 3: AI Conversation Mining

After exporting ChatGPT conversations (Settings > Data Controls > Export Data):

```bash
python main.py \
  --ai-conversations ~/Downloads/chatgpt-export/ \
  --output-dir ./output/ai-archaeology
```

The aggregator parses the nested `mapping` tree structure, extracts all messages chronologically, and runs topic extraction to surface recurring themes across hundreds of conversations.

---

## Output Formats

| Output | Format | Description |
|--------|--------|-------------|
| `inventory.json` | JSON | Unified catalog of all discovered assets across all scanned layers |
| `knowledge_graph.json` | JSON | Node-edge graph with typed entities and relationships |
| `knowledge_graph_cytoscape.json` | Cytoscape.js JSON | Import-ready format for interactive graph visualisation |
| `triage_report.json` | JSON | Structured priority tiers (high/medium/low) with action items |
| `triage_report.txt` | Plain text | Human-readable executive summary for terminal or document inclusion |
| `archives.json` | JSON | Per-module archive scan results with deduplication data |
| `personal_repos.json` | JSON | Per-module personal repository analysis |
| `org_repos.json` | JSON | Per-module organisation repository analysis |
| `ai_conversations.json` | JSON | Per-module AI conversation aggregation |
| `web_bookmarks.json` | JSON | Per-module bookmark analysis |

All output files are written to the `--output-dir` directory. The `output/` directory in the repository root is `.gitignored` — generated data stays local.

---

## Downstream Implementation

The Cognitive Archaeology Tribunal sits at the very top of the dependency chain within the eight-organ system. Its outputs were the empirical basis for the organ-system design itself:

- **Registry Foundation:** The repo audit in `00-d-organ-system-audit.md` and the `registry-v2.json` source of truth in the ingesting-organ-document-structure (planning corpus) planning corpus both trace their lineage to data this tool produced.

- **ORGAN-IV (Taxis) Orchestration:** The tribunal's triage reports feed directly into [agentic-titan](https://github.com/organvm-iv-taxis/agentic-titan), the orchestration layer that governs cross-organ routing and governance. Health scores, status classifications, and migration plans from `OrgRepoAnalyzer.generate_health_report()` provide the quantitative inputs that ORGAN-IV needs to make routing decisions.

- **ORGAN-V (Logos) Public Process:** The narrative of "pre-synthesis chaos to organised system" — documented through the tribunal's outputs — forms one of the flagship essay themes in ORGAN-V's public process content strategy.

- **Integration Queue:** The fork classification data from `PersonalRepoAnalyzer` generated the 42-fork integration queue (`context/planning/INTEGRATION_QUEUE.md`) that drove the personal-to-org migration strategy, tiered into high/medium/low priority integrations.

The tribunal is designed to be re-runnable. As the eight-organ system evolves, periodic re-audits produce updated inventories that track drift, validate governance assumptions, and surface new triage recommendations.

---

## Validation

### Current State

The tribunal has been validated through two complete audit runs:

1. **Self-analysis** (Phase 1): The tool scanned its own repository — 32 files, 1.69 MB — establishing baseline functionality.
2. **Full repository audit** (Phase 2): 85 repositories analysed (42 personal + 43 organisational), producing 793 KB of structured output including inventory, knowledge graph, and triage report.

### Test Suite

Unit tests exist for `ArchiveScanner` and `WebBookmarkAnalyzer` in the `tests/` directory. The roadmap targets 80%+ test coverage by v0.5.0. Run existing tests with:

```bash
pytest tests/
```

### Governance Agent

The repository includes a [Nervous Archaeologist](/.github/agents/nervous-archaeologist.agent.md) agent definition — a GitHub Copilot agent configured for exhaustive data excavation with security-first governance. The agent operates under the tribunal's scanning philosophy: zero stones unturned, every finding documented.

---

## Roadmap

The tribunal follows a four-sprint development plan toward v1.0.0:

| Sprint | Focus | Key Deliverables | Status |
|--------|-------|------------------|--------|
| **Sprint 1** | Foundation and Governance | Metadata standards, privacy enhancement, browser tab module, data validation | In progress |
| **Sprint 2** | Cross-Layer Synthesis | Synthesis engine, entity extraction, cross-layer knowledge graph, pattern detection | Planned |
| **Sprint 3** | Visualisation and Testing | Cytoscape.js/D3.js visualisations, CI/CD pipeline, 80%+ test coverage, performance optimisation | Planned |
| **Sprint 4** | Temporal Analysis | Concept drift detection, interest trajectory mapping, evolution visualisations | Planned |

**Future backlog** includes: plugin architecture, REST API (FastAPI), collaborative features, export bridges (Obsidian, Notion, Zotero, Anki), interactive web UI, and semantic search with RAG.

The full roadmap is maintained in [ROADMAP.md](./docs/ROADMAP.md).

---

## Cross-References

### Within ORGAN-I (Theoria)

- [recursive-engine--generative-entity](https://github.com/organvm-i-theoria/recursive-engine--generative-entity) — Recursive systems theory; the tribunal embodies recursive self-examination (it audits itself as part of its validation suite)
- ingesting-organ-document-structure (planning corpus) — Planning corpus that consumes the tribunal's audit outputs as empirical foundation

### Across Organs

- [agentic-titan](https://github.com/organvm-iv-taxis/agentic-titan) (ORGAN-IV) — Orchestration layer that consumes tribunal health scores and migration plans
- [public-process](https://github.com/organvm-v-logos/public-process) (ORGAN-V) — Public essays documenting the chaos-to-order transformation the tribunal enables

### Within This Repository

- `CONTEXTUAL_RELAY.md` — Session handoff document with current state, priorities, and quick commands
- `ROADMAP.md` — Full development roadmap with sprint breakdowns
- `context/planning/INTEGRATION_QUEUE.md` — 42-fork integration tracker generated from tribunal output
- `docs/analysis/PHASE2_REVISED_INTEGRATION_ANALYSIS.md` — The critical reframing that forks are integration staging, not clutter

---

## Contributing

Contributions are welcome. The project uses Trunk-based linting (configuration in `.trunk/trunk.yaml`) with Ruff for Python, markdownlint for Markdown, and yamllint for YAML.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Run linting: `trunk check`
4. Run tests: `pytest tests/`
5. Commit with descriptive messages in imperative mood
6. Open a pull request

For significant changes, open an issue first to discuss the approach. See [CONTRIBUTING.md](./CONTRIBUTING.md) for detailed guidelines and [docs/GOVERNANCE.md](./docs/GOVERNANCE.md) for the project's governance framework.

---

## License

This project is licensed under the MIT License. See [LICENSE](./LICENSE) for the full text.

---

## Author & Contact

**[@4444J99](https://github.com/4444J99)**

Part of [ORGAN-I: Theoria](https://github.com/organvm-i-theoria) within the eight-organ creative-institutional system coordinated by [meta-organvm](https://github.com/meta-organvm).

<!-- SYSTEM-NAV-START -->

---

<sub>[Portfolio](https://4444j99.github.io/portfolio/) · [System Directory](https://4444j99.github.io/portfolio/directory/) · [ORGAN I · Theoria](https://organvm-i-theoria.github.io/) · Part of the <a href="https://4444j99.github.io/portfolio/directory/">ORGANVM eight-organ system</a></sub>

<!-- SYSTEM-NAV-END -->
