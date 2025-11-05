# Automation Scripts

Automated scripts for job discovery, document validation, and workflow optimization.

## Job Discovery & Scraping

### `job_discovery.py` - LinkedIn Job Search Automation

**NEW:** Automates job discovery by searching LinkedIn Jobs and scraping full descriptions.

**Requirements:**
- Python 3.x
- Playwright: `pip install playwright && python -m playwright install chromium`

**Usage:**

```bash
# Interactive mode (uses defaults)
python scripts/job_discovery.py

# Specific search
python scripts/job_discovery.py --keywords "Director Product Data Platform" --location "London, United Kingdom"

# With date filter
python scripts/job_discovery.py --keywords "VP Product" --location "Remote, UK" --date past_week

# Headless mode (no browser window)
python scripts/job_discovery.py --headless

# Future: Auto mode (uses career-preferences.md)
python scripts/job_discovery.py --auto
```

**Features:**
- ✅ Searches LinkedIn Jobs with customizable filters
- ✅ Handles infinite scroll/pagination
- ✅ Deduplicates against existing `applications/*` folders
- ✅ Scrapes full job descriptions
- ✅ Saves to `staging/YYYY-MM-DD-discovery-batch/`
- ✅ Generates JSON summary report

**Output:**
```
staging/2025-11-05-discovery-batch/
├── DISCOVERY-SUMMARY.json          # Metadata and job list
├── CompanyName-RoleTitle/
│   └── job-description.md
└── ...
```

**Next Steps After Discovery:**
```bash
# 1. Bulk analyze discovered jobs
python scripts/bulk_analyze.py staging/2025-11-05-discovery-batch

# 2. Review summary
cat staging/2025-11-05-discovery-batch/BULK-ANALYSIS-SUMMARY.md

# 3. Apply to 8+ fit scores
/generate-cv CompanyName
/generate-cover-letter CompanyName
```

**Time Saved:** 2-3 hours/week on manual job searching

**Roadmap:**
- Phase 1 ✅: LinkedIn search scraper
- Phase 2 (Week 2): Scheduled monitoring with email alerts
- Phase 3 (Week 3): Multi-platform support (Greenhouse, Lever, Indeed)

---

## Document Validation Scripts

Automated scripts to validate CV and Cover Letter PDF formatting and ensure compliance with professional standards.

## Purpose

These scripts prevent formatting issues by validating:

### CV Validation
- ✅ Page count (must be ≤ 2 pages)
- ✅ File size (should be 60-80KB for Eisvogel template)
- ✅ Paper size (A4: 595 x 842 pts)
- ✅ Markdown YAML (no problematic custom YAML)
- ✅ PDF metadata (XeLaTeX generation)

### Cover Letter Validation
- ✅ Page count (MUST be exactly 1 page - 2 pages is unprofessional)
- ✅ Word count (300-400 words optimal for Eisvogel)
- ✅ File size (should be 10-20KB)
- ✅ Paper size (A4: 595 x 842 pts)
- ✅ Markdown YAML (clean, minimal formatting)

## Scripts

## CV Validation Scripts

### 1. `validate-cv.py` (Python - Primary, Cross-platform)

**Requirements:**
- Python 3.x
- `pdfinfo` (optional but recommended)
  - Windows: `choco install xpdf-utils`
  - Mac: `brew install poppler`
  - Linux: `apt-get install poppler-utils`

**Usage:**
```bash
# Full validation (PDF + Markdown)
python scripts/validate-cv.py applications/2025-10-Angi-DirectorProductDataPlatform/ArturSwadzba_CV_Angi.pdf applications/2025-10-Angi-DirectorProductDataPlatform/ArturSwadzba_CV_Angi.md
```

**Features:**
- 7 comprehensive validation checks
- Color-coded output (Pass/Fail/Warn)
- Detailed remediation steps if validation fails
- Compares with master CV
- Works on Windows, Mac, Linux (cross-platform)

### 2. `validate-cv-format.sh` (Bash - Full Featured)

**Requirements:**
- Bash (Git Bash on Windows, native on Mac/Linux)
- `pdfinfo` (optional but recommended)
  - Windows: `choco install xpdf-utils`
  - Mac: `brew install poppler`
  - Linux: `apt-get install poppler-utils`

**Usage:**
```bash
# Basic validation (PDF only)
./scripts/validate-cv-format.sh applications/2025-10-Angi-DirectorProductDataPlatform/ArturSwadzba_CV_Angi.pdf

# Full validation (PDF + Markdown)
./scripts/validate-cv-format.sh applications/2025-10-Angi-DirectorProductDataPlatform/ArturSwadzba_CV_Angi.pdf applications/2025-10-Angi-DirectorProductDataPlatform/ArturSwadzba_CV_Angi.md
```

**Features:**
- 7 comprehensive validation checks
- Color-coded output (Pass/Fail/Warn)
- Detailed remediation steps if validation fails
- Compares with master CV
- Works on Windows (Git Bash), Mac, Linux

### 3. `validate-cv-format.bat` (Windows Batch - Basic)

**Requirements:**
- Windows Command Prompt or PowerShell

**Usage:**
```cmd
scripts\validate-cv-format.bat applications\2025-10-Angi-DirectorProductDataPlatform\ArturSwadzba_CV_Angi.pdf
```

**Features:**
- Basic validation checks
- No external dependencies
- Automatic markdown file detection
- Windows-native

---

## Cover Letter Validation Scripts

### 1. `validate-cover-letter.py` (Python - Primary, Cross-platform)

**Requirements:**
- Python 3.x
- `pdfinfo` (optional but recommended)

**Usage:**
```bash
# Full validation (PDF + Markdown)
python scripts/validate-cover-letter.py applications/2025-10-Angi-DirectorProductDataPlatform/ArturSwadzba_CoverLetter_Angi.pdf applications/2025-10-Angi-DirectorProductDataPlatform/ArturSwadzba_CoverLetter_Angi.md
```

**Features:**
- 6 comprehensive validation checks
- **CRITICAL: Detects 2-page cover letters** (unprofessional)
- Word count validation (300-400 words optimal)
- Color-coded output with remediation steps
- Cross-platform (Windows, Mac, Linux)

**Validation Checks:**
1. ✅ File existence
2. ✅ File size (10-20KB optimal)
3. ✅ **Page count = 1 (CRITICAL)** - 2-page cover letters are unprofessional
4. ✅ Paper size (A4)
5. ✅ **Word count (300-400 words)** - Optimized for Eisvogel spacing
6. ✅ Clean YAML (no problematic formatting)

**Why This Matters:**
- **2-page cover letters look unprofessional** and hurt applications
- Eisvogel template has generous spacing: 400-500 words = 2 pages
- **300-400 words = 1 page** (sweet spot)
- Hiring managers expect 1-page cover letters

---

## Validation Checks Summary

### CV Validation Checks

| Check | Description | Critical? |
|-------|-------------|-----------|
| **File Existence** | Verifies PDF file exists | ✅ Yes |
| **File Size** | 60-80KB optimal, 40-100KB acceptable | ⚠️ Important |
| **Page Count** | Must be ≤ 2 pages | ✅ Critical |
| **Paper Size** | Must be A4 (595 x 842 pts) | ✅ Critical |
| **Markdown YAML** | No documentclass, header-includes, geometry | ✅ Critical |
| **PDF Metadata** | Should show XeLaTeX generation | ⚠️ Informational |
| **Master CV Compare** | Same page count as master | ℹ️ Reference |

### Cover Letter Validation Checks

| Check | Description | Critical? |
|-------|-------------|-----------|
| **File Existence** | Verifies PDF file exists | ✅ Yes |
| **File Size** | 10-20KB optimal, 10-25KB acceptable | ⚠️ Important |
| **Page Count** | **MUST be exactly 1 page** | ✅ CRITICAL |
| **Paper Size** | Must be A4 (595 x 842 pts) | ✅ Critical |
| **Word Count** | 300-400 words optimal, 250-400 acceptable | ✅ CRITICAL |
| **Markdown YAML** | Clean, minimal formatting only | ✅ Critical |

## Common Issues and Fixes

### ❌ Issue: CV is 4+ pages instead of 2

**Cause:** Wrong YAML or missing Eisvogel template

**Fix:**
```bash
# 1. Check markdown YAML
head -20 ArturSwadzba_CV_Company.md

# 2. Remove problematic YAML (documentclass, header-includes, geometry)

# 3. Regenerate with Eisvogel
cd applications/YYYY-MM-Company-Role
pandoc ArturSwadzba_CV_Company.md -o ArturSwadzba_CV_Company.pdf --from markdown --template eisvogel --pdf-engine=xelatex --listings

# 4. Validate again
../../scripts/validate-cv-format.sh ArturSwadzba_CV_Company.pdf ArturSwadzba_CV_Company.md
```

### ❌ Issue: File size too small (<40KB)

**Cause:** Wrong template used (not Eisvogel)

**Fix:**
Ensure pandoc command includes `--template eisvogel`

### ❌ Issue: Wrong paper size

**Cause:** Missing Eisvogel template

**Fix:**
Use `--template eisvogel` in pandoc command

---

### Cover Letter Issues

### ❌ Issue: Cover letter is 2 pages instead of 1

**Cause:** Word count too high (>400 words) + Eisvogel spacing

**Fix:**
```bash
# 1. Check current word count
python scripts/validate-cover-letter.py CoverLetter.pdf CoverLetter.md

# 2. Open markdown file and count words in body (should be 300-400)

# 3. Reduce word count:
#    - Opening: 60-80 words (2-3 sentences)
#    - Body paragraphs: 80-100 words each (3-4 sentences)
#    - Closing: 40-50 words (2 sentences)

# 4. Remove excessive \vspace commands (max 2 total)

# 5. Regenerate PDF
cd applications/YYYY-MM-Company-Role
pandoc CoverLetter.md -o CoverLetter.pdf --from markdown --template eisvogel --pdf-engine=xelatex

# 6. Validate again
python ../../scripts/validate-cover-letter.py CoverLetter.pdf CoverLetter.md
```

**Word Count Target Distribution (350 words total):**
- Opening paragraph: 60-80 words
- Body paragraph 1: 80-100 words
- Body paragraph 2: 80-100 words
- Closing paragraph: 40-50 words

### ❌ Issue: Word count too high (450-500 words)

**Cause:** Following standard "400-500 word" advice (doesn't work with Eisvogel)

**Fix:**
- Target 300-400 words (not 400-500)
- Eisvogel has generous spacing
- 400-500 words = 2 pages (WRONG)
- 300-400 words = 1 page (CORRECT)

## Integration with Workflow

### Manual Validation
```bash
# After generating CV, validate immediately
/generate-cv CompanyName
./scripts/validate-cv-format.sh applications/.../ArturSwadzba_CV_CompanyName.pdf
```

### Automated Validation
The `/generate-cv` command now includes automatic validation (see `.claude/commands/generate-cv.md` Step 5)

## Exit Codes

- `0` - Validation passed
- `1` - Validation failed (critical issues found)

## Examples

### ✅ Good CV (VirginAtlantic)
```bash
$ ./scripts/validate-cv-format.sh applications/2025-11-VirginAtlantic-DigitalProductLead/ArturSwadzba_CV_VirginAtlantic.pdf

✅ PASS: PDF file exists
✅ PASS: File size in optimal range (60-80KB)
✅ PASS: Perfect page count (2 pages)
✅ PASS: A4 paper size confirmed
✅ PASS: Generated with XeLaTeX

✅ OVERALL: EXCELLENT - CV formatting is perfect!
```

### ❌ Bad CV (Angi - Before Fix)
```bash
$ ./scripts/validate-cv-format.sh applications/2025-10-Angi-DirectorProductDataPlatform/ArturSwadzba_CV_Angi.pdf applications/2025-10-Angi-DirectorProductDataPlatform/ArturSwadzba_CV_Angi.md

✅ PASS: PDF file exists
⚠️  WARN: File size too small (39KB < 40KB)
❌ FAIL: Too many pages (4 > 2) - CRITICAL
❌ FAIL: Markdown contains problematic YAML (3 issues)
   ❌ Found 'documentclass:' - DO NOT USE
   ❌ Found 'header-includes:' - DO NOT USE
   ❌ Found 'geometry: margin' - DO NOT USE

❌ OVERALL: FAILED - CV has critical formatting issues

REMEDIATION STEPS:
1. Check markdown YAML - remove documentclass, header-includes, geometry
2. Ensure pandoc command uses: --template eisvogel
3. Regenerate PDF with correct settings
4. Run this validator again
```

### ✅ Good Cover Letter (Angi - After Fix)
```bash
$ python scripts/validate-cover-letter.py applications/2025-10-Angi-DirectorProductDataPlatform/ArturSwadzba_CoverLetter_Angi.pdf applications/2025-10-Angi-DirectorProductDataPlatform/ArturSwadzba_CoverLetter_Angi.md

✅ PASS: File exists
✅ PASS: File size in optimal range (12KB)
✅ PASS: Perfect page count (1 page)
✅ PASS: A4 paper size confirmed
✅ PASS: Word count acceptable (284 words)
✅ PASS: Markdown YAML looks clean

✅ OVERALL: PERFECT - Cover letter formatting is correct!
```

### ❌ Bad Cover Letter (Angi - Before Fix)
```bash
$ python scripts/validate-cover-letter.py applications/2025-10-Angi-DirectorProductDataPlatform/ArturSwadzba_CoverLetter_Angi.pdf applications/2025-10-Angi-DirectorProductDataPlatform/ArturSwadzba_CoverLetter_Angi.md

✅ PASS: File exists
✅ PASS: File size in optimal range (14KB)
❌ FAIL: TOO MANY PAGES (2 pages)
   CRITICAL: Cover letters MUST be 1 page
   This is UNPROFESSIONAL and will hurt your application

   FIX:
   1. Reduce word count to 300-400 words (currently likely 450-500)
   2. Shorten paragraphs (max 3-4 sentences each)
   3. Remove excessive spacing
   4. Regenerate PDF

✅ PASS: A4 paper size confirmed
❌ FAIL: Word count too high (472 > 400)
   This will create a 2-page cover letter!
   FIX: Reduce to 300-400 words

✅ PASS: Markdown YAML looks clean

❌ OVERALL: FAILED - Cover letter has critical formatting issues

REMEDIATION STEPS:
1. Check markdown word count - reduce to 300-400 words
2. Shorten paragraphs (3-4 sentences max each)
3. Remove excessive \vspace commands
4. Ensure YAML has only geometry + fontsize
5. Regenerate PDF with Eisvogel template
6. Run this validator again
```

## Reference

**Good Examples:**
- CV: `applications/2025-11-VirginAtlantic-DigitalProductLead/ArturSwadzba_CV_VirginAtlantic.pdf`
- Cover Letter: `applications/2025-10-Angi-DirectorProductDataPlatform/ArturSwadzba_CoverLetter_Angi.pdf` (after fix)

**Master Templates:**
- Master CV: `master/ArturSwadzba_MasterCV.pdf`

**Documentation:**
- CV Guardrails: `docs/cv-formatting-guardrails.md`
- Cover Letter Guardrails: `docs/cover-letter-formatting-guardrails.md`

## Troubleshooting

### pdfinfo not found
Install poppler-utils:
- Windows: `choco install xpdf-utils`
- Mac: `brew install poppler`
- Linux: `apt-get install poppler-utils`

### Permission denied (bash script)
```bash
chmod +x scripts/validate-cv-format.sh
```

### Git Bash path issues on Windows
Use forward slashes or quote paths with spaces:
```bash
./scripts/validate-cv-format.sh "applications/2025-10-Company Name/CV.pdf"
```
