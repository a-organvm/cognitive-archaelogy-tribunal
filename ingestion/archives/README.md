# Archives Ingestion Chamber

Configure archive locations to scan for comprehensive file analysis.

## How It Works

Unlike other chambers where you copy files IN, this chamber is where you configure PATHS to scan.

## Setup

### Create `locations.txt`

Create a file listing archive directories to scan:

```bash
# Create locations.txt with paths to scan
cat > ingestion/archives/locations.txt <<EOF
~/iCloud Drive
~/Dropbox
~/Documents/Archives
/Volumes/ExternalDrive
EOF
```

**Format:**
- One absolute path per line
- Comments supported with `#`
- Empty lines ignored
- Paths can include spaces (no quotes needed)

### Example `locations.txt`
```
# Cloud storage
~/Library/Mobile Documents/com~apple~CloudDocs
~/Dropbox

# Local archives
~/Documents/Old Projects
~/Pictures/Archive

# External drives
/Volumes/Backup Drive
/Volumes/TimeMachine

# Network storage (if mounted)
/Volumes/NAS/archive
```

## What Gets Scanned

The archive scanner will:
- ✅ Recursively scan all subdirectories
- ✅ Classify files by type (documents, code, media, etc.)
- ✅ Calculate sizes and modification dates
- ✅ Detect duplicate files (hash-based)
- ✅ Identify large files (>10MB)
- ✅ Find old files (>1 year untouched)
- ❌ Never modify or delete files (read-only)

### Excluded Automatically
- System files (`.DS_Store`, `Thumbs.db`)
- Cache directories (`__pycache__`, `.cache`)
- Version control (`.git`, `.svn`)
- Dependencies (`node_modules`)
- Temporary files (`*.tmp`, `*.swp`)

## Processing

### Manual
```bash
# Read locations from file
python main.py --scan-archives "$(cat ingestion/archives/locations.txt | grep -v '^#' | grep -v '^$' | tr '\n' ',')" --output-dir ./output/archives
```

### Using Script
```bash
# From project root
./scripts/ingest_archives.sh
```

## Output

Results saved to `output/archives/`:
- `archives.json` - Complete scan results
- `inventory.json` - Unified inventory
- `knowledge_graph.json` - File relationships
- `triage_report.json` - Cleanup recommendations
- `triage_report.txt` - Human-readable report

## What Gets Analyzed

### File Classification
- Documents (PDF, DOC, TXT, MD)
- Code (PY, JS, TS, GO, JAVA)
- Media (JPG, PNG, MP4, MOV)
- Archives (ZIP, TAR, DMG)
- Data (CSV, JSON, XML, DB)
- Other

### Deduplication
- Hash-based duplicate detection
- Potential space savings calculation
- Duplicate file groups

### Recommendations
- Large files to review
- Old files to archive/delete
- Duplicate removal suggestions
- Organization opportunities

## Performance Tips

### Start Small
For initial testing, start with a small directory:
```
# Test with one directory first
~/Documents/TestFolder
```

### Exclude More Patterns
Edit `cognitive_tribunal/modules/archive_scanner.py` to add exclusions if needed.

### Large Archives
- First scan may take 10-30+ minutes depending on size
- ~1-5 seconds per 1000 files (rough estimate)
- External drives will be slower than local SSDs

## Example Workflow

### 1. Create Configuration
```bash
cat > ingestion/archives/locations.txt <<EOF
~/iCloud Drive
~/Dropbox
EOF
```

### 2. Run Scan
```bash
./scripts/ingest_archives.sh
```

### 3. Review Results
```bash
# Human-readable report
cat output/archives/triage_report.txt

# Full JSON data
jq '.stats' output/archives/archives.json
```

### 4. Act on Recommendations
Based on triage report:
- Delete duplicates
- Archive old files
- Organize by type
- Free up space

## Supported Locations

### macOS
- iCloud Drive: `~/Library/Mobile Documents/com~apple~CloudDocs`
- Dropbox: `~/Dropbox`
- Google Drive: `~/Google Drive`
- OneDrive: `~/OneDrive`
- External drives: `/Volumes/*`

### Linux
- Home: `/home/username`
- Mounted drives: `/mnt/*`, `/media/*`
- Network shares: `/mnt/nas/*`

### Windows (WSL)
- Windows drives: `/mnt/c/Users/username`
- Network drives: `/mnt/n/*`

## Permissions

### macOS: Full Disk Access Required

If scanning iCloud, Documents, or other protected folders:

1. Open "System Preferences" → "Security & Privacy"
2. Go to "Privacy" tab → "Full Disk Access"
3. Click 🔒 to unlock
4. Add Terminal or your Python executable
5. Restart terminal

### Linux: Permission Errors
```bash
# Check permissions
ls -la /path/to/scan

# Fix if needed (be careful!)
sudo chmod -R +r /path/to/scan
```

## Troubleshooting

**"Permission denied"**
- Grant Full Disk Access (macOS)
- Check directory permissions
- Run with appropriate privileges

**"Path does not exist"**
- Verify paths are absolute (start with `/`)
- Check for typos
- Ensure drives are mounted

**Scan is very slow**
- This is normal for large archives (millions of files)
- Consider scanning smaller subsets first
- Exclude `node_modules`, `Library`, etc. if needed

**Out of memory**
- Scan locations separately
- Reduce scan depth
- Process in batches

## Privacy & Safety

- ✅ **Read-only**: Never modifies files
- ✅ **Local**: All processing happens on your machine
- ✅ **Gitignored**: Results stay local
- ❌ **No deletion**: Recommendations only, you decide

## Next Steps

After scanning:
1. Review deduplication recommendations
2. Identify large files for cleanup
3. Find old files to archive
4. Plan organization strategy

See [USAGE.md](../../USAGE.md) for advanced features.
