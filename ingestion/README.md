# Ingestion Chambers

This directory contains ingestion chambers for loading data into the Cognitive Archaeology Tribunal for processing.

## Directory Structure

```
ingestion/
├── ai-exports/         # AI conversation exports (ChatGPT, Claude)
├── archives/           # Links to archive locations (iCloud, Dropbox, drives)
├── bookmarks/          # Browser bookmark export files
└── browser-tabs/       # Browser tab/session exports
```

## Usage

### Quick Start

1. **Place your data files in the appropriate chamber:**
   - AI exports → `ai-exports/`
   - Bookmark HTML files → `bookmarks/`
   - Browser tab exports → `browser-tabs/`

2. **For archives, create location file:**
   - Create `archives/locations.txt` with paths to scan

3. **Run ingestion:**
   ```bash
   # Process all chambers
   ./scripts/ingest_all.sh

   # Or process individually
   ./scripts/ingest_ai.sh
   ./scripts/ingest_bookmarks.sh
   ./scripts/ingest_archives.sh
   ```

## Chamber Details

### 🤖 AI Exports (`ai-exports/`)
Drop your AI conversation exports here:
- **ChatGPT**: Export from Settings → Data Controls → Export Data
- **Claude**: Export conversation JSON files
- **Format**: JSON files or directories containing JSON files

**What happens:**
- Conversations are parsed and indexed
- Topics are extracted
- Timeline analysis performed
- Output: `output/ai-context/*.json`

See: [AI Exports README](ai-exports/README.md)

---

### 📦 Archives (`archives/`)
Configure archive locations to scan:
- **Create**: `archives/locations.txt` with one path per line
- **Supported**: iCloud, Dropbox, local drives, network mounts
- **Format**: Absolute paths to directories

**What happens:**
- File classification by type
- Deduplication analysis
- Large/old file identification
- Output: `output/archives/*.json`

See: [Archives README](archives/README.md)

---

### 🔖 Bookmarks (`bookmarks/`)
Drop browser bookmark export files here:
- **Chrome**: Export from Bookmark Manager → ⋮ → Export bookmarks
- **Firefox**: Bookmarks → Show All Bookmarks → Import and Backup → Export
- **Format**: HTML (Netscape Bookmark File Format)

**What happens:**
- URLs and titles extracted
- Creation dates parsed
- Statistics generated
- Output: `output/bookmarks/*.json`

See: [Bookmarks README](bookmarks/README.md)

---

### 🌐 Browser Tabs (`browser-tabs/`)
Drop browser tab/session exports here:
- **OneTab**: Export to text/URL list
- **Session Buddy**: Export to JSON
- **Tab Session Manager**: Export to JSON
- **Format**: JSON, TXT, or URL lists

**What happens:**
- Active tabs cataloged
- Tab groups analyzed
- Domain frequency tracked
- Output: `output/browser-tabs/*.json`

See: [Browser Tabs README](browser-tabs/README.md)

---

## Helper Scripts

Located in `scripts/`:

- `ingest_all.sh` - Process all chambers at once
- `ingest_ai.sh` - Process AI exports only
- `ingest_archives.sh` - Process archives only
- `ingest_bookmarks.sh` - Process bookmarks only
- `ingest_tabs.sh` - Process browser tabs only

## Output Location

All processed results are saved to:
```
output/
├── ai-context/
├── archives/
├── bookmarks/
└── browser-tabs/
```

The `output/` directory is gitignored to keep large data files out of version control.

## Examples

### Example 1: ChatGPT Export
```bash
# 1. Export from ChatGPT (you'll get a ZIP file)
# 2. Extract the ZIP
# 3. Move/copy conversations.json to ingestion chamber:
cp ~/Downloads/chatgpt-export/conversations.json ingestion/ai-exports/

# 4. Run ingestion
./scripts/ingest_ai.sh
```

### Example 2: Chrome Bookmarks
```bash
# 1. Export from Chrome (creates bookmarks_*.html)
# 2. Move to ingestion chamber:
cp ~/Downloads/bookmarks_11_18_2025.html ingestion/bookmarks/

# 3. Run ingestion
./scripts/ingest_bookmarks.sh
```

### Example 3: Archive Scan
```bash
# 1. Create locations file
cat > ingestion/archives/locations.txt <<EOF
~/iCloud Drive
~/Dropbox
/Volumes/ExternalDrive
EOF

# 2. Run ingestion
./scripts/ingest_archives.sh
```

### Example 4: Process Everything
```bash
# After placing all files in their chambers:
./scripts/ingest_all.sh
```

## Tips

1. **Large Archives**: Archive scanning can be slow. Start with a small test directory first.
2. **File Organization**: Keep original exports organized by date: `ai-exports/2025-11-18/`
3. **Incremental**: You can run ingestion multiple times. Results will be regenerated.
4. **Backup**: Always keep original export files. Ingestion is read-only.

## Troubleshooting

### "Permission denied" on archive scanning
- Ensure you have read access to the directories in `locations.txt`
- On macOS, grant Terminal "Full Disk Access" in System Preferences

### "No JSON files found" for AI exports
- Verify the file is actually JSON (open in text editor)
- Check file extension is `.json`
- Ensure file isn't corrupted

### Script not executable
```bash
chmod +x scripts/ingest_*.sh
```

## Next Steps

After ingestion completes:
1. Review triage reports in `output/*/triage_report.txt`
2. Explore knowledge graphs in `output/*/knowledge_graph.json`
3. Check unified inventory in `output/*/inventory.json`

See [USAGE.md](../USAGE.md) for detailed usage instructions.
