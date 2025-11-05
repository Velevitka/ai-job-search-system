# Claude Code Project Guide

> **Quick Start:** Read this + ARCHITECTURE.md before making changes

**Purpose:** This guide helps Claude Code understand project conventions, tech stack decisions, and patterns to maintain consistency across sessions.

---

## Technology Stack

### Document Generation (LOCKED - Don't Change)

**PDF Generation Pipeline:**
- **Pandoc** - Document conversion engine
- **XeLaTeX** - LaTeX backend for professional typesetting
- **Eisvogel template** - Professional CV/CL formatting
- **Why:** Consistent 2-page CVs, professional formatting, version-controlled source

**Source Format:**
- **Markdown** with YAML front matter
- **Why:** Human-readable, AI-friendly, version controllable, pandoc-compatible

**Alternative Considered & Rejected:**
- ❌ Direct LaTeX - Too complex, hard to maintain
- ❌ docx2pdf - Inconsistent formatting, hard to version control
- ❌ HTML→PDF - Poor print formatting, no professional templates

### Validation Tools (REQUIRED)

**Before Every Commit with PDF Changes:**
```bash
# Validate CV
python scripts/validation/validate-cv.py path/to/cv.pdf [path/to/cv.md]

# Validate Cover Letter
python scripts/validation/validate-cover-letter.py path/to/cl.pdf [path/to/cl.md]
```

**What Gets Validated:**
- CV: Exactly 2 pages, A4 size (595x842 pts), file size 60-80KB
- Cover Letter: Exactly 1 page, 300-400 words, file size 10-20KB
- YAML front matter: Clean, no formatting issues
- Markdown: Proper structure, no problematic characters

### System Requirements
- Python 3.7+
- Pandoc 2.x+
- XeLaTeX (TeX Live or MiKTeX)
- pdfinfo (poppler-utils)

---

## Python Code Standards

### Required UTF-8 Fix for Windows

**Always include at start of scripts:**
```python
import sys

# Fix Windows console encoding for emojis and unicode
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

**Why:** Windows defaults to cp1252, can't display emoji in output

### Type Hints (Preferred)

```python
from typing import Dict, List, Optional
from pathlib import Path

def calculate_fit_score(
    job_description: str,
    preferences: Dict[str, float]
) -> float:
    """Calculate job fit score from 0-10.

    Args:
        job_description: Full text of job posting
        preferences: Scoring weights by category

    Returns:
        Float between 0-10 indicating fit
    """
    pass
```

### File Operations

**Prefer pathlib over os:**
```python
from pathlib import Path

# ✅ Good
app_dir = Path("applications/2025-11-Company-Role")
cv_path = app_dir / "ArturSwadzba_CV_Company.md"
if cv_path.exists():
    content = cv_path.read_text(encoding='utf-8')

# ❌ Avoid
import os
cv_path = os.path.join("applications", "2025-11-Company-Role", "cv.md")
if os.path.exists(cv_path):
    with open(cv_path, 'r') as f:
        content = f.read()
```

### Error Handling

```python
# Graceful degradation with specific errors
try:
    result = parse_job_description(url)
except requests.RequestException as e:
    logging.error(f"Failed to fetch job: {e}")
    return fallback_manual_paste_instructions()
except ValueError as e:
    logging.error(f"Invalid job format: {e}")
    return None
```

---

## Slash Command Writing Standards

### Command Structure (Pattern from Existing Commands)

Every command should follow this structure:

```markdown
# Command Name

You are the **[Role] Agent**, responsible for [specific task].

## ⚡ Purpose

[1-2 sentence description of what this command does]

**What this means:**
- [Key point about behavior]
- [Important constraint]

**When to use this:**
- [Scenario 1]
- [Scenario 2]

---

## Your Task

[Step-by-step instructions with clear numbering]

### 1. [First Major Step]

**[Substep category]:**
- Action item
- Action item

### 2. [Second Major Step]

**[Substep category]:**
- Action item

### 3. Generate [Output File]

**IMPORTANT:** After generating, **WRITE IT TO [path]**

Use the Write tool to create/overwrite the file.

**Format exactly as follows:**

```markdown
[Exact template with placeholders]
```

---

## Rules & Best Practices

**CRITICAL:**
1. **[Key rule]** - Explanation
2. **[Key rule]** - Explanation

**Verification checklist:**
- [ ] Check 1
- [ ] Check 2

---

## Display to User

After writing the file, show:

```
[User-friendly summary with emoji]
[Key metrics]
[Next actions]
```
```

### Required Elements in Every Command

✅ **Role definition** - "You are the X Agent"
✅ **Clear purpose** - What and why
✅ **Task breakdown** - Numbered steps
✅ **Output format** - Exact template or example
✅ **WRITE instruction** - Explicitly use Write tool
✅ **Validation** - Check output was created
✅ **User display** - Summary of what happened
✅ **Rules section** - Critical constraints

### Command Output Best Practices

**Always show to user:**
- What files were created/updated (with paths)
- Key metrics (word count, fit score, etc.)
- Validation status (passed/failed checks)
- Next recommended actions

**Example:**
```
✅ CV Generated Successfully!

📁 Files Created:
- applications/2025-11-Company-Role/ArturSwadzba_CV_Company.md
- applications/2025-11-Company-Role/ArturSwadzba_CV_Company.pdf

📊 Stats:
- Pages: 2 (validated ✅)
- Keywords matched: 12/12
- Fit score: 8.5/10

🎯 Next Steps:
1. Review CV for accuracy
2. Generate cover letter with /generate-cl Company
3. Update status with /update-status
```

---

## Architecture Principles

See ARCHITECTURE.md for full structure. Key rules:

### Source of Truth vs. Derived Views

**Source of Truth (NEVER auto-regenerate):**
- `applications/*/status.md` - Application tracking
- `master/YourName_MasterCV.docx` - Master CV
- `applications/*/job-description.md` - Saved job postings
- `career-preferences.md` - User preferences

**Derived Views (AUTO-REGENERATE on every run):**
- `STATUS.md` - Regenerated by `/status` command
- `insights/metrics-dashboard.md` - Regenerated by `/update-metrics`
- Manual edits to derived views WILL BE OVERWRITTEN

### Data Immutability Rules

1. **Master CV**
   - Never modify without explicit user approval
   - All CV tailoring is REFRAMING, not fabrication
   - Changes must be documented in cv-changes-log.md

2. **Job Descriptions**
   - Save original, never edit
   - If analysis is wrong, re-analyze, don't modify source

3. **Status Files**
   - Update, don't replace
   - Preserve history with timestamps
   - Status changes are append-only

### Privacy & Git

**NEVER commit:**
- `master/` - Master CV (personal data)
- `applications/` - Job applications (except _example-application/)
- `insights/` - Analytics with personal info
- `staging/` - Temporary job saves
- `archive/` - Old CVs

**Safe to commit:**
- `.claude/commands/` - Command definitions
- `docs/` - Documentation
- `scripts/` - Automation scripts
- `README.md`, ARCHITECTURE.md, etc.

---

## Validation Requirements

### CV Validation (2-Page Rule)

**Critical:** CVs MUST be exactly 2 pages. This is non-negotiable.

```bash
python scripts/validation/validate-cv.py applications/2025-11-Company-Role/ArturSwadzba_CV_Company.pdf
```

**Checks performed:**
- ✅ Exactly 2 pages (not 1, not 3, not 4)
- ✅ A4 paper size (595 x 842 points)
- ✅ File size 60-80KB (typical for Eisvogel)
- ✅ PDF metadata correct

**If validation fails:**
1. Check YAML front matter for extra spacing
2. Review markdown content length
3. Check for problematic characters (`, ", etc.)
4. See docs/formatting/cv-formatting-guardrails.md

### Cover Letter Validation (1-Page Rule)

**Critical:** Cover letters MUST be exactly 1 page. 2 pages is unprofessional.

```bash
python scripts/validation/validate-cover-letter.py applications/2025-11-Company-Role/ArturSwadzba_CoverLetter_Company.pdf
```

**Checks performed:**
- ✅ Exactly 1 page
- ✅ Word count 300-400 (optimal for Eisvogel spacing)
- ✅ A4 paper size
- ✅ File size 10-20KB

**If validation fails:**
1. Reduce word count (aim for 350 words)
2. Check for extra spacing in YAML
3. Remove unnecessary paragraphs
4. See docs/formatting/cover-letter-formatting-guardrails.md

### When to Validate

- ✅ After generating CV/CL PDFs
- ✅ Before committing changes
- ✅ After modifying templates
- ✅ When troubleshooting formatting issues

---

## Testing Framework

### Current State

**✅ Implemented:**
- Pytest framework installed and configured
- Test directory structure (`tests/`, `tests/fixtures/`)
- Validation script tests (`test_validation.py`)
- Pytest fixtures for module imports
- Configuration (`pytest.ini`, `tests/README.md`)
- Requirements updated with pytest dependencies

**What works:**
- Validation scripts: `scripts/validation/validate-cv.py`, `validate-cover-letter.py`
- Automated tests for file size, page count, paper size validation
- Test coverage tracking with pytest-cov
- Fixtures handle import of scripts with hyphens in filenames

**Still manual:**
- Slash command testing
- Visual inspection of PDFs
- Real-world usage testing (applying to jobs)

**Gaps to address:**
- Fit score calculation tests
- File operations tests
- Bookmarklet extraction tests
- Integration tests for full workflows

### Planned Testing Framework (pytest)

**Phase 1: Setup** ✅ COMPLETE

```bash
# Installed
pip install pytest pytest-cov

# Added to requirements.txt
pytest==8.4.2
pytest-cov==7.0.0

# Created test structure
tests/
├── __init__.py               ✅ Created
├── conftest.py               ✅ Created (fixtures)
├── test_validation.py        ✅ Created (18 tests)
├── README.md                 ✅ Created (documentation)
└── fixtures/                 ✅ Created (empty, ready for test data)

# Additional files
pytest.ini                     ✅ Created (configuration)
```

**Phase 2: Write Tests**

```python
# tests/test_validation.py
import pytest
from pathlib import Path
from scripts.validation.validate_cv import validate_cv_format

def test_valid_2_page_cv():
    """Test that valid 2-page CV passes validation."""
    result = validate_cv_format("tests/fixtures/valid_2page_cv.pdf")
    assert result['valid'] == True
    assert result['page_count'] == 2

def test_invalid_3_page_cv():
    """Test that 3-page CV fails validation."""
    result = validate_cv_format("tests/fixtures/invalid_3page_cv.pdf")
    assert result['valid'] == False
    assert 'must be exactly 2 pages' in result['errors'][0]

def test_cv_file_size_range():
    """Test that CV file size is within expected range."""
    result = validate_cv_format("tests/fixtures/valid_2page_cv.pdf")
    assert 60000 <= result['file_size'] <= 80000
```

**Phase 3: Run Tests** ✅ IMPLEMENTED

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=scripts --cov-report=html

# Run specific test file
pytest tests/test_validation.py

# Run specific test
pytest tests/test_validation.py::TestFileSizeCheck::test_optimal_size_range

# See tests/README.md for full documentation
```

### Test Coverage Goals

**Priority 1 (Essential):**
- ✅ Validation scripts (validate-cv.py, validate-cover-letter.py)
- ✅ Fit score calculation logic
- ✅ File operations (path handling, encoding)

**Priority 2 (Important):**
- ✅ Bookmarklet data extraction
- ✅ Markdown to PDF conversion validation
- ✅ YAML front matter parsing

**Priority 3 (Nice to Have):**
- ✅ Command workflow integration tests
- ✅ End-to-end application generation
- ✅ Performance benchmarks

### Evaluation Criteria

**What to measure:**
1. **Fit Score Accuracy**
   - Compare AI-calculated scores vs. manual scores
   - Track score consistency over time
   - Target: ±0.5 points accuracy

2. **Formatting Compliance**
   - 100% validation pass rate for generated CVs/CLs
   - Zero formatting regressions
   - Track: pages, file size, paper size

3. **Command Reliability**
   - Zero errors on standard workflows
   - Graceful handling of edge cases
   - Track: success rate per command

**How to evaluate:**
```bash
# After implementing pytest
pytest tests/ --cov=scripts --cov-report=term-missing

# Target coverage: 80%+ for validation scripts
# Target coverage: 60%+ for utility scripts
```

---

## Common Patterns

### Reading Application Data

```python
from pathlib import Path

def get_application_data(company_name: str) -> dict:
    """Read application folder data safely.

    Returns dict with keys: status, analysis, cv_path, cl_path
    """
    # Find application folder
    apps_dir = Path("applications")
    folders = list(apps_dir.glob(f"*{company_name}*"))

    if not folders:
        raise FileNotFoundError(f"No application found for {company_name}")

    app_dir = folders[0]

    # Read status if exists
    status_path = app_dir / "status.md"
    status = status_path.read_text(encoding='utf-8') if status_path.exists() else None

    return {
        'folder': app_dir,
        'status': status,
        'cv_path': app_dir / f"ArturSwadzba_CV_{company_name}.pdf",
        'analysis_path': app_dir / "analysis.md"
    }
```

### Fit Score Calculation Pattern

```python
def calculate_fit_score(job_description: str, analysis: dict) -> float:
    """Calculate fit score based on career-preferences.md criteria.

    Scoring (max 10 points):
    - Data platform/CDP keywords: +1.5
    - MarTech/AdTech/Growth: +1.0
    - Seniority (Director/Head/VP): +2.0
    - Location (UK/Remote): +2.0, EU: +1.0
    - Travel/hospitality domain: +1.5
    - Other strong signals: +0.5 each
    """
    score = 0.0

    # Check keywords
    if any(kw in job_description.lower() for kw in ['cdp', 'customer data platform', 'data platform']):
        score += 1.5

    # Check location
    if 'london' in job_description.lower() or 'remote' in job_description.lower():
        score += 2.0

    # ... etc

    return min(score, 10.0)  # Cap at 10
```

### Command Output Template

```python
def display_completion_message(files_created: list, metrics: dict):
    """Standard completion message for commands."""
    print("✅ Task Completed Successfully!\n")

    print("📁 Files Created:")
    for file_path in files_created:
        print(f"- {file_path}")

    print("\n📊 Stats:")
    for key, value in metrics.items():
        print(f"- {key}: {value}")

    print("\n🎯 Next Steps:")
    print("1. Review generated files")
    print("2. Run validation if PDFs were created")
    print("3. Update status or proceed to next command")
```

---

## Dependencies

### Current Dependencies (requirements.txt)

```
# None - using Python standard library only
```

**Philosophy:** Prefer standard library when possible, only add external deps when they save significant complexity.

### When to Add a Dependency

**✅ Good reasons to add:**
- Saves 100+ lines of complex code
- Industry standard for the task (e.g., requests for HTTP)
- Significantly improves reliability
- Well-maintained, popular library

**❌ Avoid adding for:**
- Simple tasks (file I/O, string manipulation)
- One-off use cases
- Unmaintained libraries
- Features you can implement in <50 lines

**Process:**
1. Check if standard library can do it
2. Evaluate library (stars, maintenance, size)
3. Add to requirements.txt with comment
4. Document in commit message why it's needed
5. Update docs/setup/SETUP.md installation instructions

### System Dependencies (Required)

These must be installed manually:
- Pandoc 2.x+
- XeLaTeX (TeX Live or MiKTeX)
- pdfinfo (poppler-utils)

See docs/setup/SETUP.md for installation instructions.

---

## Anti-Patterns to Avoid

### ❌ Don't Fabricate Data

**Never:**
- Invent achievements not in master CV
- Make up metrics or numbers
- Fabricate company names or dates
- Create fake experiences

**Always:**
- Reframe existing achievements
- Use exact numbers from master CV
- Document all changes in cv-changes-log.md

### ❌ Don't Modify Source of Truth

**Never:**
- Auto-regenerate status.md files in applications/
- Modify master CV without approval
- Edit saved job descriptions
- Change user preferences without permission

**Always:**
- Ask before modifying source of truth
- Document changes
- Preserve history

### ❌ Don't Skip Validation

**Never:**
- Generate PDF without running validation
- Assume formatting is correct
- Commit PDFs without validation pass
- Ignore validation warnings

**Always:**
- Run validation scripts after PDF generation
- Fix validation errors before proceeding
- Include validation status in output

### ❌ Don't Hardcode Paths

**Never:**
```python
cv_path = "C:\\Users\\ArturSwadzba\\OneDrive\\4. CV\\applications\\..."
```

**Always:**
```python
from pathlib import Path
cv_path = Path("applications") / company_folder / f"{name}_CV_{company}.pdf"
```

---

## Quick Reference

### Key Files to Read First
- `ARCHITECTURE.md` - Project structure
- `career-preferences.md` - Fit scoring criteria
- `docs/formatting/cv-formatting-guardrails.md` - CV rules
- `docs/formatting/cover-letter-formatting-guardrails.md` - CL rules

### Key Commands
- `/analyze-job` - Analyze job posting, calculate fit
- `/generate-cv` - Create tailored CV (requires analysis)
- `/generate-cl` - Create cover letter (requires analysis)
- `/status` - Check current application status
- `/update-metrics` - Refresh metrics dashboard
- `/bulk-process` - Analyze multiple job postings

### Key Directories
- `.claude/commands/` - Slash command definitions
- `applications/` - Job applications (gitignored)
- `master/` - Master CV (gitignored)
- `scripts/validation/` - Validation scripts
- `docs/` - All documentation

### Emergency Contacts
- Validation fails: See docs/formatting/
- Command broken: Check .claude/commands/
- Architecture unclear: Read ARCHITECTURE.md
- Git issues: See docs/setup/GIT-SETUP-GUIDE.md

---

**Last Updated:** 2025-11-05
**Maintained By:** Auto-updated as patterns emerge
**Questions?** Update this file with new patterns as you discover them
