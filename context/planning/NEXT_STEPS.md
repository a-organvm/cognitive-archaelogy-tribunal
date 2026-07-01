# Next Steps - Quick Reference

**Generated:** 2025-11-16
**Status:** Ready for Execution

---

## Immediate Actions (Priority Order)

### 1. Run Self-Analysis ⚡ DO NOW
```bash
cd ~/cognitive-archaelogy-tribunal

python main.py \
  --scan-archives ~/cognitive-archaelogy-tribunal \
  --output-dir ./output/self-analysis
```

**Why:** Validate tool functionality and create baseline inventory

**Expected Output:**
- `output/self-analysis/inventory.json`
- `output/self-analysis/archives.json`
- `output/self-analysis/triage_report.txt`

**Review Command:**
```bash
cat ./output/self-analysis/triage_report.txt
```

---

### 2. Obtain GitHub Token 🔑 DO TODAY
1. Visit: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo` (Full control of private repositories)
4. Generate and copy token
5. Set environment variable:
   ```bash
   export GITHUB_TOKEN="ghp_your_token_here"
   ```
6. Verify:
   ```bash
   echo "Token set: ${GITHUB_TOKEN:0:10}..."
   ```

**Why:** Required for all GitHub repository analysis (Phases 2-5)

---

### 3. Analyze Personal Repositories 📊 DO TODAY
```bash
python main.py \
  --personal-repos 4444JPP \
  --github-token $GITHUB_TOKEN \
  --output-dir ./output/personal-repos
```

**Why:** Map all 35+ personal repos, identify cleanup opportunities

**Expected Insights:**
- Unmodified forks to delete
- Inactive repos to archive
- Active projects to maintain
- Graduation candidates for org

**Review Command:**
```bash
cat ./output/personal-repos/triage_report.txt
head -50 ./output/personal-repos/personal_repos.json
```

---

### 4. Analyze Organization Repositories 🏢 DO THIS WEEK
```bash
python main.py \
  --org-repos ivi374forivi \
  --github-token $GITHUB_TOKEN \
  --output-dir ./output/org-repos
```

**Why:** Health check all 23 org repos, identify maintenance needs

**Expected Insights:**
- Active vs. stale vs. abandoned repos
- Health scores
- Dependency tracking
- Open issues requiring attention

**Review Command:**
```bash
cat ./output/org-repos/triage_report.txt
```

---

### 5. Combined Repository Analysis 🔗 DO THIS WEEK
```bash
python main.py \
  --personal-repos 4444JPP \
  --org-repos ivi374forivi \
  --github-token $GITHUB_TOKEN \
  --output-dir ./output/complete-repo-audit
```

**Why:** Map cross-layer integration and relationships

**Expected Insights:**
- Personal → Org graduation candidates
- Cross-repository dependencies
- Complete ecosystem knowledge graph
- Unified triage recommendations

**Review Commands:**
```bash
cat ./output/complete-repo-audit/triage_report.txt
cat ./output/complete-repo-audit/inventory.json | jq '.summary'
```

---

## Short-Term Actions (Next 1-2 Weeks)

### 6. Export AI Conversations 💬
**ChatGPT:**
1. Go to ChatGPT settings
2. Navigate to "Data Controls"
3. Click "Export data"
4. Wait for email (can take 24-48 hours)
5. Download and extract ZIP
6. Locate `conversations.json`

**Claude:**
- Check Claude settings for export option
- Alternative: Save important conversations manually

---

### 7. Process AI Context
```bash
python main.py \
  --ai-conversations /path/to/chatgpt/export \
  --output-dir ./output/ai-context
```

**Why:** Index conversation history, extract topics, map idea evolution

---

### 8. Map Archive Locations 📁
Document all storage:
- [ ] iCloud Drive path: `___________________`
- [ ] Dropbox path: `___________________`
- [ ] External drives: `___________________`
- [ ] Network storage: `___________________`
- [ ] Old backups: `___________________`

---

## Medium-Term Actions (Next 2-4 Weeks)

### 9. Scan Archives
```bash
# Adjust paths to your actual locations
python main.py \
  --scan-archives "/path/to/iCloud,/path/to/Dropbox,/path/to/drives" \
  --output-dir ./output/archive-excavation
```

**Why:** Complete Layer 0 inventory, find duplicates, optimize storage

---

### 10. Complete Four-Layer Synthesis 🎯
```bash
python main.py \
  --scan-archives "/path/to/archives" \
  --ai-conversations "/path/to/ai/exports" \
  --personal-repos 4444JPP \
  --org-repos ivi374forivi \
  --github-token $GITHUB_TOKEN \
  --output-dir ./output/COMPLETE-COGNITIVE-ARCHAEOLOGY
```

**Why:** Master knowledge graph, unified triage, complete system view

---

## Action Tracking Checklist

### Phase 1: Self-Analysis
- [ ] Run self-analysis scan
- [ ] Review inventory output
- [ ] Validate tool functionality
- [ ] Document baseline

### Phase 2: Repository Analysis
- [ ] Obtain GitHub token
- [ ] Scan personal repos (4444JPP)
- [ ] Scan org repos (ivi374forivi)
- [ ] Run combined analysis
- [ ] Review triage recommendations
- [ ] Identify quick wins (forks to delete, etc.)

### Phase 3: AI Context
- [ ] Request ChatGPT export
- [ ] Collect Claude conversations
- [ ] Process AI context
- [ ] Review topic extraction
- [ ] Map conversation timeline

### Phase 4: Archive Excavation
- [ ] Map all storage locations
- [ ] Plan scan strategy
- [ ] Run archive scans
- [ ] Review duplicate report
- [ ] Calculate space savings

### Phase 5: Synthesis
- [ ] Run complete 4-layer analysis
- [ ] Generate master knowledge graph
- [ ] Review unified triage report
- [ ] Create action plan from recommendations

---

## Success Indicators

**You'll know you're succeeding when:**

1. ✅ Self-analysis completes without errors
2. ✅ Personal repo audit reveals actionable cleanup items
3. ✅ Org repo audit shows health metrics for all repos
4. ✅ Triage reports provide clear, prioritized actions
5. ✅ Knowledge graphs visualize cross-layer relationships
6. ✅ You can answer questions like:
   - How many unmodified forks can I delete?
   - Which repos haven't been touched in 6+ months?
   - What are the health scores of our org repos?
   - Where are the duplicates in my archives?
   - How much space can I save?
   - Which personal repos should graduate to org?

---

## Common Issues & Solutions

### "No module named 'cognitive_tribunal'"
```bash
cd ~/cognitive-archaelogy-tribunal
pip install -r requirements.txt
```

### "GitHub API rate limit exceeded"
- Use GitHub token for authentication
- Wait for rate limit reset (check headers)
- Run in smaller batches

### "Permission denied" on archive scan
- Check file/directory permissions
- Run with appropriate user privileges
- Add problematic paths to exclusion patterns

### Large output files
```bash
# Compress old outputs
gzip ./output/*/archives.json

# Use --no-graph to skip graph generation if needed
python main.py --scan-archives /path --no-graph --output-dir ./output
```

---

## Quick Command Reference

### Scan this repo
```bash
python main.py --scan-archives . --output-dir ./output/self
```

### Personal repos only
```bash
python main.py --personal-repos 4444JPP --output-dir ./output/personal
```

### Org repos only
```bash
python main.py --org-repos ivi374forivi --output-dir ./output/org
```

### Both repos
```bash
python main.py --personal-repos 4444JPP --org-repos ivi374forivi --output-dir ./output/repos
```

### Everything (when ready)
```bash
python main.py \
  --scan-archives "/archives" \
  --ai-conversations "/ai" \
  --personal-repos 4444JPP \
  --org-repos ivi374forivi \
  --output-dir ./output/complete
```

### View outputs
```bash
# Triage report (human-readable)
cat ./output/*/triage_report.txt

# Inventory summary
cat ./output/*/inventory.json | jq '.summary'

# Knowledge graph
cat ./output/*/knowledge_graph.json | jq '.nodes | length'
```

---

## Questions to Answer Through Ingestion

As you run each phase, you'll be able to answer:

**Personal Repos:**
- How many repos are unmodified forks? → Delete candidates
- Which repos have no commits in 6+ months? → Archive candidates
- What languages dominate my projects? → Skill map
- Which repos have dependencies? → Integration map

**Org Repos:**
- Which repos are abandoned (180+ days)? → Revival or archive
- What's the average health score? → Ecosystem health
- Which repos have open issues? → Maintenance queue
- What are the dependency chains? → Risk assessment

**Archives:**
- How many duplicate files exist? → Space savings
- What's the oldest content? → Historical timeline
- Where are the largest files? → Storage optimization
- What file types dominate? → Content classification

**AI Conversations:**
- What topics appear most frequently? → Interest map
- Which ideas led to repos? → Provenance tracking
- What remains unimplemented? → Future roadmap
- How have concepts evolved? → Intellectual timeline

---

**Status:** ✅ Plan Ready
**Next Action:** Run Step 1 (Self-Analysis)
**Command:**
```bash
cd ~/cognitive-archaelogy-tribunal && \
python main.py --scan-archives . --output-dir ./output/self-analysis
```
