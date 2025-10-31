#!/bin/bash
# CV Format Validation Script
# Validates CV PDF formatting against master CV standards
# Usage: ./validate-cv-format.sh <path-to-cv.pdf> [<path-to-markdown.md>]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
MAX_PAGES=2
MIN_FILE_SIZE_KB=40
MAX_FILE_SIZE_KB=100
TARGET_MIN_SIZE_KB=60
TARGET_MAX_SIZE_KB=80
EXPECTED_WIDTH=595
EXPECTED_HEIGHT=842

# Counters
PASS_COUNT=0
FAIL_COUNT=0
WARN_COUNT=0

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}   CV FORMAT VALIDATION TOOL${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if PDF path provided
if [ -z "$1" ]; then
    echo -e "${RED}❌ ERROR: No PDF file specified${NC}"
    echo "Usage: $0 <path-to-cv.pdf> [<path-to-markdown.md>]"
    exit 1
fi

PDF_PATH="$1"
MD_PATH="$2"

# Check if PDF exists
if [ ! -f "$PDF_PATH" ]; then
    echo -e "${RED}❌ ERROR: PDF file not found: $PDF_PATH${NC}"
    exit 1
fi

echo -e "${BLUE}Validating:${NC} $PDF_PATH"
echo ""

# Check if pdfinfo is available
if ! command -v pdfinfo &> /dev/null; then
    echo -e "${YELLOW}⚠️  WARNING: pdfinfo not installed. Install poppler-utils for full validation.${NC}"
    echo "   On Windows: choco install xpdf-utils"
    echo "   On Mac: brew install poppler"
    echo "   On Linux: apt-get install poppler-utils"
    echo ""
fi

echo -e "${BLUE}Running validation checks...${NC}"
echo ""

# ============================================
# CHECK 1: File Existence and Basic Info
# ============================================
echo -e "${BLUE}[1/7]${NC} Checking file existence..."
if [ -f "$PDF_PATH" ]; then
    echo -e "${GREEN}✅ PASS:${NC} PDF file exists"
    ((PASS_COUNT++))
else
    echo -e "${RED}❌ FAIL:${NC} PDF file not found"
    ((FAIL_COUNT++))
    exit 1
fi
echo ""

# ============================================
# CHECK 2: File Size
# ============================================
echo -e "${BLUE}[2/7]${NC} Checking file size..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows (Git Bash)
    FILE_SIZE_BYTES=$(stat -c%s "$PDF_PATH" 2>/dev/null || echo "0")
else
    # Unix/Mac
    FILE_SIZE_BYTES=$(stat -f%z "$PDF_PATH" 2>/dev/null || stat -c%s "$PDF_PATH" 2>/dev/null || echo "0")
fi
FILE_SIZE_KB=$((FILE_SIZE_BYTES / 1024))

echo "   File size: ${FILE_SIZE_KB}KB"

if [ "$FILE_SIZE_KB" -lt "$MIN_FILE_SIZE_KB" ]; then
    echo -e "${RED}❌ FAIL:${NC} File too small (${FILE_SIZE_KB}KB < ${MIN_FILE_SIZE_KB}KB)"
    echo "   This suggests wrong template was used (not Eisvogel)"
    ((FAIL_COUNT++))
elif [ "$FILE_SIZE_KB" -gt "$MAX_FILE_SIZE_KB" ]; then
    echo -e "${YELLOW}⚠️  WARN:${NC} File larger than expected (${FILE_SIZE_KB}KB > ${MAX_FILE_SIZE_KB}KB)"
    echo "   This might indicate embedded fonts or images"
    ((WARN_COUNT++))
elif [ "$FILE_SIZE_KB" -ge "$TARGET_MIN_SIZE_KB" ] && [ "$FILE_SIZE_KB" -le "$TARGET_MAX_SIZE_KB" ]; then
    echo -e "${GREEN}✅ PASS:${NC} File size in optimal range (${TARGET_MIN_SIZE_KB}-${TARGET_MAX_SIZE_KB}KB)"
    ((PASS_COUNT++))
else
    echo -e "${GREEN}✅ PASS:${NC} File size acceptable (within ${MIN_FILE_SIZE_KB}-${MAX_FILE_SIZE_KB}KB range)"
    ((PASS_COUNT++))
fi
echo ""

# ============================================
# CHECK 3: Page Count (CRITICAL)
# ============================================
echo -e "${BLUE}[3/7]${NC} Checking page count..."
if command -v pdfinfo &> /dev/null; then
    PAGE_COUNT=$(pdfinfo "$PDF_PATH" 2>/dev/null | grep -i "Pages:" | awk '{print $2}')

    if [ -z "$PAGE_COUNT" ]; then
        echo -e "${YELLOW}⚠️  WARN:${NC} Could not determine page count"
        ((WARN_COUNT++))
    else
        echo "   Pages: $PAGE_COUNT"

        if [ "$PAGE_COUNT" -gt "$MAX_PAGES" ]; then
            echo -e "${RED}❌ FAIL:${NC} Too many pages ($PAGE_COUNT > $MAX_PAGES)"
            echo "   ${RED}CRITICAL: CV must be $MAX_PAGES pages maximum${NC}"
            echo "   This indicates BROKEN formatting (wrong YAML or missing Eisvogel)"
            ((FAIL_COUNT++))
        elif [ "$PAGE_COUNT" -eq "$MAX_PAGES" ]; then
            echo -e "${GREEN}✅ PASS:${NC} Perfect page count ($MAX_PAGES pages)"
            ((PASS_COUNT++))
        else
            echo -e "${GREEN}✅ PASS:${NC} Page count acceptable ($PAGE_COUNT pages)"
            ((PASS_COUNT++))
        fi
    fi
else
    echo -e "${YELLOW}⚠️  SKIP:${NC} pdfinfo not available - cannot check page count"
    ((WARN_COUNT++))
fi
echo ""

# ============================================
# CHECK 4: Paper Size (CRITICAL)
# ============================================
echo -e "${BLUE}[4/7]${NC} Checking paper size..."
if command -v pdfinfo &> /dev/null; then
    PAGE_SIZE=$(pdfinfo "$PDF_PATH" 2>/dev/null | grep -i "Page size:")

    if [ -z "$PAGE_SIZE" ]; then
        echo -e "${YELLOW}⚠️  WARN:${NC} Could not determine page size"
        ((WARN_COUNT++))
    else
        echo "   $PAGE_SIZE"

        # Extract width and height
        WIDTH=$(echo "$PAGE_SIZE" | grep -oP '\d+\.?\d*(?= x)' | head -1)
        HEIGHT=$(echo "$PAGE_SIZE" | grep -oP '(?<=x )\d+\.?\d*' | head -1)

        # Convert to integers for comparison (remove decimal)
        WIDTH_INT=$(printf "%.0f" "$WIDTH" 2>/dev/null || echo "0")
        HEIGHT_INT=$(printf "%.0f" "$HEIGHT" 2>/dev/null || echo "0")

        # Allow small tolerance (±5 pts)
        if [ "$WIDTH_INT" -ge $((EXPECTED_WIDTH - 5)) ] && [ "$WIDTH_INT" -le $((EXPECTED_WIDTH + 5)) ] && \
           [ "$HEIGHT_INT" -ge $((EXPECTED_HEIGHT - 5)) ] && [ "$HEIGHT_INT" -le $((EXPECTED_HEIGHT + 5)) ]; then
            echo -e "${GREEN}✅ PASS:${NC} A4 paper size confirmed (${WIDTH_INT} x ${HEIGHT_INT} pts)"
            ((PASS_COUNT++))
        else
            echo -e "${RED}❌ FAIL:${NC} Wrong paper size (expected ${EXPECTED_WIDTH} x ${EXPECTED_HEIGHT} pts)"
            echo "   This indicates missing Eisvogel template or wrong configuration"
            ((FAIL_COUNT++))
        fi
    fi
else
    echo -e "${YELLOW}⚠️  SKIP:${NC} pdfinfo not available - cannot check paper size"
    ((WARN_COUNT++))
fi
echo ""

# ============================================
# CHECK 5: Markdown YAML Validation (if provided)
# ============================================
echo -e "${BLUE}[5/7]${NC} Checking markdown YAML..."
if [ -n "$MD_PATH" ] && [ -f "$MD_PATH" ]; then
    echo "   Analyzing: $MD_PATH"

    # Extract first 30 lines (YAML should be at top)
    YAML_CONTENT=$(head -30 "$MD_PATH")

    # Check for problematic YAML
    YAML_ISSUES=0

    if echo "$YAML_CONTENT" | grep -q "documentclass:"; then
        echo -e "${RED}   ❌ Found 'documentclass:' - DO NOT USE${NC}"
        ((YAML_ISSUES++))
    fi

    if echo "$YAML_CONTENT" | grep -q "header-includes:"; then
        echo -e "${RED}   ❌ Found 'header-includes:' - DO NOT USE${NC}"
        ((YAML_ISSUES++))
    fi

    if echo "$YAML_CONTENT" | grep -q "geometry:.*margin"; then
        echo -e "${RED}   ❌ Found 'geometry: margin' - DO NOT USE${NC}"
        ((YAML_ISSUES++))
    fi

    if echo "$YAML_CONTENT" | grep -q "\\\\usepackage"; then
        echo -e "${RED}   ❌ Found '\\usepackage' commands - DO NOT USE${NC}"
        ((YAML_ISSUES++))
    fi

    if echo "$YAML_CONTENT" | grep -q "\\\\titleformat"; then
        echo -e "${RED}   ❌ Found '\\titleformat' commands - DO NOT USE${NC}"
        ((YAML_ISSUES++))
    fi

    if [ "$YAML_ISSUES" -gt 0 ]; then
        echo -e "${RED}❌ FAIL:${NC} Markdown contains problematic YAML ($YAML_ISSUES issues)"
        echo "   These YAML elements break Eisvogel template formatting"
        echo "   ${YELLOW}FIX: Remove all custom YAML, use minimal or NO YAML${NC}"
        ((FAIL_COUNT++))
    else
        echo -e "${GREEN}✅ PASS:${NC} Markdown YAML looks clean (no problematic elements)"
        ((PASS_COUNT++))
    fi
else
    echo -e "${YELLOW}⚠️  SKIP:${NC} Markdown file not provided or not found"
    if [ -n "$MD_PATH" ]; then
        echo "   Looked for: $MD_PATH"
    fi
    ((WARN_COUNT++))
fi
echo ""

# ============================================
# CHECK 6: PDF Metadata
# ============================================
echo -e "${BLUE}[6/7]${NC} Checking PDF metadata..."
if command -v pdfinfo &> /dev/null; then
    CREATOR=$(pdfinfo "$PDF_PATH" 2>/dev/null | grep -i "Creator:" | sed 's/Creator:[ ]*//')
    PRODUCER=$(pdfinfo "$PDF_PATH" 2>/dev/null | grep -i "Producer:" | sed 's/Producer:[ ]*//')

    echo "   Creator: ${CREATOR:-Unknown}"
    echo "   Producer: ${PRODUCER:-Unknown}"

    # Check if created with XeLaTeX (good sign for Eisvogel)
    if echo "$PRODUCER" | grep -qi "xelatex\|xetex"; then
        echo -e "${GREEN}✅ PASS:${NC} Generated with XeLaTeX (expected for Eisvogel)"
        ((PASS_COUNT++))
    else
        echo -e "${YELLOW}⚠️  WARN:${NC} Not generated with XeLaTeX (might not be Eisvogel template)"
        ((WARN_COUNT++))
    fi
else
    echo -e "${YELLOW}⚠️  SKIP:${NC} pdfinfo not available - cannot check metadata"
    ((WARN_COUNT++))
fi
echo ""

# ============================================
# CHECK 7: Comparison with Master CV (if available)
# ============================================
echo -e "${BLUE}[7/7]${NC} Comparing with master CV..."
MASTER_CV="master/ArturSwadzba_MasterCV.pdf"

if [ -f "$MASTER_CV" ]; then
    echo "   Found master CV: $MASTER_CV"

    if command -v pdfinfo &> /dev/null; then
        MASTER_PAGES=$(pdfinfo "$MASTER_CV" 2>/dev/null | grep -i "Pages:" | awk '{print $2}')

        if [ -n "$MASTER_PAGES" ] && [ -n "$PAGE_COUNT" ]; then
            if [ "$PAGE_COUNT" -eq "$MASTER_PAGES" ]; then
                echo -e "${GREEN}✅ PASS:${NC} Same page count as master CV ($MASTER_PAGES pages)"
                ((PASS_COUNT++))
            else
                echo -e "${YELLOW}⚠️  INFO:${NC} Different page count than master (CV: $PAGE_COUNT, Master: $MASTER_PAGES)"
                echo "   This may be acceptable if CV is tailored/condensed"
            fi
        fi
    fi
else
    echo -e "${YELLOW}⚠️  SKIP:${NC} Master CV not found at: $MASTER_CV"
    ((WARN_COUNT++))
fi
echo ""

# ============================================
# SUMMARY
# ============================================
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}   VALIDATION SUMMARY${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${GREEN}Passed:  ${PASS_COUNT}${NC}"
echo -e "${RED}Failed:  ${FAIL_COUNT}${NC}"
echo -e "${YELLOW}Warnings: ${WARN_COUNT}${NC}"
echo ""

# Overall result
if [ "$FAIL_COUNT" -eq 0 ]; then
    if [ "$WARN_COUNT" -eq 0 ]; then
        echo -e "${GREEN}✅ OVERALL: EXCELLENT - CV formatting is perfect!${NC}"
        exit 0
    else
        echo -e "${YELLOW}⚠️  OVERALL: GOOD - CV passed with warnings${NC}"
        echo "Review warnings above for potential improvements"
        exit 0
    fi
else
    echo -e "${RED}❌ OVERALL: FAILED - CV has critical formatting issues${NC}"
    echo ""
    echo -e "${YELLOW}REMEDIATION STEPS:${NC}"
    echo "1. Check markdown YAML - remove documentclass, header-includes, geometry"
    echo "2. Ensure pandoc command uses: --template eisvogel"
    echo "3. Regenerate PDF with correct settings"
    echo "4. Run this validator again"
    echo ""
    echo -e "Reference working example: ${BLUE}applications/2025-11-VirginAtlantic-DigitalProductLead/ArturSwadzba_CV_VirginAtlantic.pdf${NC}"
    exit 1
fi
