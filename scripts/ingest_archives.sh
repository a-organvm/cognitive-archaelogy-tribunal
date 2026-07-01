#!/usr/bin/env bash
#
# Archives Ingestion Script
# Processes archive locations from the ingestion chamber
#

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Directories
INGESTION_DIR="$PROJECT_ROOT/ingestion/archives"
OUTPUT_DIR="$PROJECT_ROOT/output/archives"
LOCATIONS_FILE="$INGESTION_DIR/locations.txt"

echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}Archives Ingestion${NC}"
echo -e "${GREEN}================================${NC}"
echo ""

# Check if locations file exists
if [ ! -f "$LOCATIONS_FILE" ]; then
    echo -e "${RED}Error: locations.txt not found${NC}"
    echo ""
    echo "Please create: $LOCATIONS_FILE"
    echo ""
    echo "Example:"
    echo "  cat > $LOCATIONS_FILE <<EOF"
    echo "  ~/iCloud Drive"
    echo "  ~/Dropbox"
    echo "  ~/Documents/Archives"
    echo "  EOF"
    echo ""
    echo "See: ingestion/archives/README.md for details"
    exit 1
fi

# Read and validate locations
echo "📂 Reading locations from: $LOCATIONS_FILE"
echo ""

# Filter out comments and empty lines
LOCATIONS=$(grep -v '^#' "$LOCATIONS_FILE" | grep -v '^$' | tr '\n' ',' | sed 's/,$//')

if [ -z "$LOCATIONS" ]; then
    echo -e "${RED}Error: No valid locations found in $LOCATIONS_FILE${NC}"
    echo ""
    echo "Add at least one directory path to scan"
    exit 1
fi

# Show locations
echo "Locations to scan:"
echo "$LOCATIONS" | tr ',' '\n' | while read -r loc; do
    if [ -d "$loc" ]; then
        echo -e "  ${GREEN}✓${NC} $loc"
    else
        echo -e "  ${RED}✗${NC} $loc (not found or not accessible)"
    fi
done
echo ""

# Confirm before proceeding
echo -e "${YELLOW}Note: Large archives may take 10-30+ minutes to scan${NC}"
read -p "Continue? [y/N] " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled"
    exit 0
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Run the main script
echo ""
echo -e "${GREEN}Running archive scanner...${NC}"
echo ""

cd "$PROJECT_ROOT"
python main.py \
    --scan-archives "$LOCATIONS" \
    --output-dir "$OUTPUT_DIR" \
    --no-graph

# Check results
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}================================${NC}"
    echo -e "${GREEN}✓ Ingestion Complete${NC}"
    echo -e "${GREEN}================================${NC}"
    echo ""
    echo "Results saved to: $OUTPUT_DIR"
    echo ""

    if [ -f "$OUTPUT_DIR/triage_report.txt" ]; then
        echo "📋 Triage Report Preview:"
        echo "----------------------------------------"
        head -n 30 "$OUTPUT_DIR/triage_report.txt"
        echo "----------------------------------------"
        echo ""
        echo "Full report: $OUTPUT_DIR/triage_report.txt"
    fi

    echo ""
    echo "Generated files:"
    ls -lh "$OUTPUT_DIR" | grep -v "^d" | awk '{print "  - " $9 " (" $5 ")"}'
else
    echo ""
    echo -e "${RED}✗ Ingestion failed${NC}"
    echo "Check error messages above for details"
    exit 1
fi
