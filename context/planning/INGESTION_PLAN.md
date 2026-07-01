# Cognitive Archaeology Tribunal - Ingestion & Execution Plan

**Generated:** 2025-11-16
**Branch:** claude/ingest-and-process-01MwVhAeqXSqxU5vZaVfvkVY

---

## Executive Summary

This document outlines the comprehensive ingestion and execution strategy for the **Cognitive Archaeology Tribunal** project. The tool is designed to audit and organize the four-layer cognitive ecosystem described in the project documentation.

### Current State Analysis

**What We Have:**
- ✅ Fully functional Cognitive Archaeology Tribunal tool with 4 modules
- ✅ Archive Scanner module (scans files, detects duplicates, classifies content)
- ✅ AI Context Aggregator module (processes ChatGPT/Claude conversation exports)
- ✅ Personal Repo Analyzer module (analyzes GitHub personal repos via API)
- ✅ Org Repo Analyzer module (analyzes GitHub organization repos)
- ✅ Unified output system (inventory, knowledge graph, triage report)
- ✅ Comprehensive documentation (README, USAGE, PROJECT_SUMMARY)
- ✅ Context documents defining the 4-layer architecture

**What We Need:**
- 🔑 GitHub Personal Access Token (for repo analysis)
- 📁 Access to archive locations (iCloud, Dropbox, local drives)
- 💬 AI conversation export files (ChatGPT/Claude)
- 🎯 Prioritized execution strategy

---

## The Four-Layer Architecture

Based on the Cognitive Operating System documentation, the system consists of:

### Layer 0: ARCHIVES (Primordial Chaos)
**Description:** Raw creative materials stored across multiple locations
- iCloud Drive
- Dropbox
- Local hard drives
- Network storage
- Old backups

**Content Types:**
- Writing (notes, drafts, brainstorms)
- Music (compositions, recordings)
- Video (footage, projects)
- Code snippets
- Documentation
- Media files

**Status:** ⚠️ Unmapped, needs full inventory

---

### Layer 1: AI KNOWLEDGE BASES (Seeds)
**Description:** AI conversation threads containing ideas, plans, and explorations
- ChatGPT conversations
- Claude conversations
- Other LLM interactions

**Content:**
- Conceptual explorations
- Technical planning
- Problem-solving sessions
- Code generation experiments
- Architecture discussions

**Status:** ⚠️ Needs export and aggregation

---

### Layer 2: PERSONAL REPOSITORIES (Staging)
**Description:** 35+ experimental GitHub repositories
**Account:** 4444JPP

**Categories:**
- Multi-model AI orchestration
- Automation & workflow tools
- Creative computing experiments
- Agent-based systems
- Knowledge management
- Forks and references
- Unfinished prototypes

**Status:** ⚠️ Needs comprehensive audit and classification

---

### Layer 3: ORGANIZATION REPOSITORIES (Production)
**Description:** 23 repositories forming the production OS
**Organization:** ivi374forivi

**Categories:**
- Core systems (auto-revision-epistemic-engine, solve-et-coagula, a-recursive-root)
- Governance (civic-assembly, census-api)
- Tools (public-record-data-scrapper, tab-bookmark-manager)
- Web (lmaoWebPage, css-js-webdev-skeletons)
- Data (legal-precedent-database, case-law-repository)
- Apps (various applications)

**Status:** ⚠️ Needs health audit and integration mapping

---

## Ingestion Strategy: Phased Approach

### PHASE 1: Self-Analysis & Local Inventory
**Goal:** Use the tool to analyze itself and local resources

#### 1.1 Scan This Repository
```bash
python main.py \
  --scan-archives ~/cognitive-archaelogy-tribunal \
  --output-dir ./output/self-analysis
```

**What This Reveals:**
- Current codebase structure
- Documentation inventory
- File organization patterns
- Baseline for the tool itself

**Deliverables:**
- `inventory.json` - Complete file catalog
- `archives.json` - Detailed scan results
- `triage_report.txt` - Self-assessment

---

### PHASE 2: GitHub Repository Analysis
**Goal:** Map all personal and organization repositories

#### 2.1 Prerequisites
- Obtain GitHub Personal Access Token
  - Go to: https://github.com/settings/tokens
  - Create token with `repo` scope (read access to repos)
  - Set as environment variable: `export GITHUB_TOKEN="ghp_xxx"`

#### 2.2 Analyze Personal Repositories
```bash
python main.py \
  --personal-repos 4444JPP \
  --github-token $GITHUB_TOKEN \
  --output-dir ./output/personal-repos-audit
```

**What This Reveals:**
- Fork vs. original classification
- Modified vs. unmodified forks
- Activity levels and staleness
- Language distribution
- Archival candidates
- Consolidation opportunities

**Deliverables:**
- `personal_repos.json` - Complete repo inventory
- `triage_report.json` - Recommendations (delete unmodified forks, archive inactive, etc.)
- `knowledge_graph.json` - Repo relationship map

#### 2.3 Analyze Organization Repositories
```bash
python main.py \
  --org-repos ivi374forivi \
  --github-token $GITHUB_TOKEN \
  --output-dir ./output/org-repos-audit
```

**What This Reveals:**
- Active vs. stale vs. abandoned status
- Health scores
- Dependency tracking
- Open issues
- Migration planning needs

**Deliverables:**
- `org_repos.json` - Organization health report
- `triage_report.json` - Priority actions
- `knowledge_graph.json` - Org ecosystem map

#### 2.4 Combined Repository Analysis
```bash
python main.py \
  --personal-repos 4444JPP \
  --org-repos ivi374forivi \
  --github-token $GITHUB_TOKEN \
  --output-dir ./output/complete-repo-audit
```

**What This Reveals:**
- Personal → Org graduation candidates
- Cross-layer integration patterns
- Dependency flows
- Complete ecosystem map

**Deliverables:**
- `inventory.json` - Unified catalog
- `knowledge_graph_cytoscape.json` - Visual ecosystem
- `triage_report.txt` - Prioritized actions across both layers

---

### PHASE 3: AI Conversation Ingestion
**Goal:** Extract and index all AI conversation history

#### 3.1 Export AI Conversations

**ChatGPT Export:**
1. Go to ChatGPT settings
2. Data Controls → Export data
3. Wait for email with download link
4. Extract ZIP file to get `conversations.json`

**Claude Export:**
- Check if export is available via Claude settings
- Alternative: Use API if available
- Manual export if needed

#### 3.2 Process AI Conversations
```bash
python main.py \
  --ai-conversations /path/to/chatgpt/export \
  --output-dir ./output/ai-context-audit
```

**What This Reveals:**
- Conversation timeline
- Topic distribution
- Idea evolution
- Unimplemented concepts
- Links to code/repos

**Deliverables:**
- `ai_conversations.json` - Conversation catalog
- Topic summaries
- Timeline analysis

#### 3.3 Combined Analysis (Repos + AI)
```bash
python main.py \
  --personal-repos 4444JPP \
  --org-repos ivi374forivi \
  --ai-conversations /path/to/exports \
  --github-token $GITHUB_TOKEN \
  --output-dir ./output/3-layer-audit
```

**What This Reveals:**
- AI conversations → Repo implementation tracking
- Unimplemented ideas
- Provenance trails
- Conceptual lineage

---

### PHASE 4: Archive Excavation
**Goal:** Inventory and index all archive materials (Layer 0)

#### 4.1 Identify Archive Locations
- [ ] Map iCloud Drive mount point
- [ ] Map Dropbox folder
- [ ] Identify external drives
- [ ] List network storage
- [ ] Locate old backups

#### 4.2 Scan Archives
```bash
# Example for multiple locations
python main.py \
  --scan-archives "/path/to/iCloud,/path/to/Dropbox,/path/to/drives" \
  --output-dir ./output/archive-excavation
```

**What This Reveals:**
- Complete file inventory
- Duplicate detection (content-based)
- Large files
- Old/unused files
- File type distribution
- Storage optimization opportunities

**Deliverables:**
- `archives.json` - Complete catalog with metadata
- Deduplication report with space savings
- File classification by type and age
- Triage recommendations

---

### PHASE 5: Complete Four-Layer Synthesis
**Goal:** Run full audit across all layers simultaneously

```bash
python main.py \
  --scan-archives "/path/to/archives" \
  --ai-conversations "/path/to/ai/exports" \
  --personal-repos 4444JPP \
  --org-repos ivi374forivi \
  --github-token $GITHUB_TOKEN \
  --output-dir ./output/COMPLETE-COGNITIVE-ARCHAEOLOGY
```

**What This Reveals:**
- Complete cross-layer knowledge graph
- Archive → AI → Personal → Org flow mapping
- Concept evolution across all layers
- Gap analysis (missing links)
- Complete system inventory
- Master triage report

**Deliverables:**
- `inventory.json` - Unified 4-layer catalog
- `knowledge_graph_cytoscape.json` - Complete visual map
- `triage_report.txt` - Master action plan
- Individual layer JSONs for detailed analysis

---

## Priority Action Items

### IMMEDIATE (Next 24-48 hours)

1. **Run Self-Analysis**
   ```bash
   python main.py \
     --scan-archives ~/cognitive-archaelogy-tribunal \
     --output-dir ./output/self-analysis
   ```
   - Understand tool's current state
   - Validate functionality
   - Generate baseline

2. **Obtain GitHub Token**
   - Create Personal Access Token
   - Set environment variable
   - Test access

3. **Run Personal Repo Audit**
   ```bash
   python main.py \
     --personal-repos 4444JPP \
     --github-token $GITHUB_TOKEN \
     --output-dir ./output/personal-repos
   ```
   - Map all 35+ personal repos
   - Identify cleanup candidates
   - Find consolidation opportunities

### SHORT-TERM (Next Week)

4. **Run Organization Audit**
   ```bash
   python main.py \
     --org-repos ivi374forivi \
     --github-token $GITHUB_TOKEN \
     --output-dir ./output/org-repos
   ```
   - Health check all 23 org repos
   - Identify stale projects
   - Map dependencies

5. **Export AI Conversations**
   - Request ChatGPT export
   - Collect Claude conversations
   - Organize export files

6. **Process AI Context**
   ```bash
   python main.py \
     --ai-conversations /path/to/exports \
     --output-dir ./output/ai-context
   ```

### MEDIUM-TERM (Next 2-4 Weeks)

7. **Map Archive Locations**
   - Document all storage locations
   - Mount necessary drives
   - Plan scan strategy

8. **Run Archive Scan**
   - Scan archives in batches
   - Generate inventories
   - Identify duplicates

9. **Run Complete 4-Layer Analysis**
   - Combined audit across all layers
   - Generate master knowledge graph
   - Create comprehensive triage report

### LONG-TERM (Next Month+)

10. **Act on Triage Recommendations**
    - Delete unmodified forks
    - Archive inactive repos
    - Consolidate duplicates
    - Graduate personal → org repos

11. **Build Integration Pipeline**
    - Automate lineage tracking
    - Create provenance links
    - Implement recursive refinement

12. **Establish Maintenance Workflow**
    - Regular audits
    - Automated monitoring
    - Continuous consolidation

---

## Success Metrics

### Phase 1 (Self-Analysis)
- ✅ Tool successfully scans itself
- ✅ Inventory generated
- ✅ Baseline established

### Phase 2 (Repository Analysis)
- ✅ All 35+ personal repos cataloged
- ✅ All 23 org repos health-checked
- ✅ Triage recommendations generated
- ✅ Fork cleanup list created
- ✅ Graduation candidates identified

### Phase 3 (AI Context)
- ✅ All AI conversations exported
- ✅ Conversations indexed and searchable
- ✅ Topics extracted
- ✅ Timeline mapped

### Phase 4 (Archive Excavation)
- ✅ All storage locations scanned
- ✅ Complete file inventory created
- ✅ Duplicates identified
- ✅ Space savings calculated

### Phase 5 (Four-Layer Synthesis)
- ✅ Unified knowledge graph generated
- ✅ Cross-layer connections mapped
- ✅ Master triage report created
- ✅ System constitution defined

---

## Technical Requirements Checklist

### Environment Setup
- [x] Python 3.8+ installed
- [x] Dependencies installed (`pip install -r requirements.txt`)
- [ ] GitHub token obtained and set
- [ ] Archive locations identified and accessible
- [ ] AI conversation exports prepared
- [ ] Output directory structure planned

### Data Sources
- [ ] GitHub personal repos (4444JPP) - requires token
- [ ] GitHub org repos (ivi374forivi) - requires token
- [ ] AI conversations (ChatGPT/Claude) - requires export
- [ ] Archive locations (iCloud/Dropbox/drives) - requires access

### Execution Environment
- [x] Main tool (`main.py`) functional
- [x] All 4 modules operational
- [x] Output generators working
- [ ] Sufficient disk space for outputs
- [ ] Network access for GitHub API

---

## Risk Mitigation

### GitHub API Rate Limits
- **Issue:** Unauthenticated: 60 req/hr, Authenticated: 5000 req/hr
- **Solution:** Use GitHub token, pace requests if needed
- **Backup:** Run in smaller batches if limits hit

### Large Archive Scans
- **Issue:** Scanning TBs of data may take hours
- **Solution:** Use exclusion patterns, scan in batches
- **Backup:** Run overnight or in background

### Missing Data Sources
- **Issue:** Some archives or conversations may be inaccessible
- **Solution:** Document gaps, proceed with available data
- **Backup:** Plan incremental ingestion as data becomes available

### Storage Space
- **Issue:** Output files may be large
- **Solution:** Monitor disk usage, compress old outputs
- **Backup:** Use external storage if needed

---

## Next Commands to Run

### Step 1: Self-Analysis (DO NOW)
```bash
cd ~/cognitive-archaelogy-tribunal

python main.py \
  --scan-archives ~/cognitive-archaelogy-tribunal \
  --output-dir ./output/self-analysis

# Review outputs
ls -lh ./output/self-analysis/
cat ./output/self-analysis/triage_report.txt
```

### Step 2: Get GitHub Token (DO TODAY)
```bash
# Visit: https://github.com/settings/tokens
# Create token with 'repo' scope
# Then set:
export GITHUB_TOKEN="ghp_your_token_here"

# Verify:
echo $GITHUB_TOKEN
```

### Step 3: Personal Repo Audit (DO TODAY)
```bash
python main.py \
  --personal-repos 4444JPP \
  --github-token $GITHUB_TOKEN \
  --output-dir ./output/personal-repos

# Review
cat ./output/personal-repos/triage_report.txt
```

### Step 4: Org Repo Audit (DO THIS WEEK)
```bash
python main.py \
  --org-repos ivi374forivi \
  --github-token $GITHUB_TOKEN \
  --output-dir ./output/org-repos

cat ./output/org-repos/triage_report.txt
```

### Step 5: Combined Analysis (DO THIS WEEK)
```bash
python main.py \
  --personal-repos 4444JPP \
  --org-repos ivi374forivi \
  --github-token $GITHUB_TOKEN \
  --output-dir ./output/complete-repos

# Explore knowledge graph
cat ./output/complete-repos/knowledge_graph.json
```

---

## Appendix: Task Mapping to Existing Plans

### From CHAOS>LOGOS-PATH_STEPXSTEP.MD

This ingestion plan addresses:

**Phase 0 (Preparation):**
- ✅ T004: Audit existing repositories → PHASE 2
- ✅ T005: Design intake system → Tool already built
- ✅ T006: Define taxonomy → Built into modules

**Phase 1 (Personal Repos):**
- ✅ T016: Perform first-pass audit → PHASE 2.2
- ✅ T017: Classify repos → Personal Repo Analyzer
- ✅ T018-T020: Identify patterns/reuse/duplicates → Automated

**Phase 2 (Org Repos):**
- ✅ T029: Review org repos → PHASE 2.3
- ✅ T030-T031: Map integration → Knowledge graph
- ✅ T032: Identify patterns → Org Repo Analyzer

**Phase 4 (Tools):**
- ✅ T039-T043: Meta-repo-analyzer → Personal/Org analyzers
- ✅ T047: AI context extractor → AI Context Aggregator

**Phase 5 (Archives):**
- ✅ T054-T066: Archive ingestion → PHASE 4
- ✅ T055: Archive aggregator → Archive Scanner

---

## Conclusion

This ingestion plan provides a clear, executable roadmap to transform the "pre-synthesis chaos" into an organized, audited, and actionable system. By following the phased approach, we systematically inventory and analyze all four layers of the cognitive ecosystem, generating comprehensive outputs that enable informed decision-making about consolidation, archival, and systematization.

**The tool is ready. The plan is clear. Execution begins now.**

---

**Document Status:** ✅ Complete
**Ready for Execution:** ✅ Yes
**Next Action:** Run Step 1 (Self-Analysis)
