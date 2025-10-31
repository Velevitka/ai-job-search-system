# CV Formatting Fix Plan

**Date:** 2025-10-31
**Issue:** Generated CV is 4 pages (should be 2), wrong font (serif vs Calibri), huge margins, title page added
**Root Cause:** YAML front matter incompatible with xelatex default template

---

## Problem Analysis

### Master CV Specifications (Correct Format)
✅ **Page Count:** 2 pages
✅ **Paper Size:** A4 (210mm × 297mm)
✅ **Font:** Calibri, ~11pt body text
✅ **Margins:** Small/tight (approx 15-20mm all sides)
✅ **Header:**
  - Name as large heading with horizontal rule
  - Contact info on same line as name
  - No title page
✅ **Section Headers:** Blue, bold (e.g., "Professional Experience")
✅ **Job Titles:** Bold black
✅ **Dates:** Right-aligned, same line as job title
✅ **Bullets:** Compact spacing, no huge gaps
✅ **Footer:** "Page X of 2" bottom right on page 2

### Generated CV Issues (Broken Format)
❌ **Page Count:** 4 pages (2x too long)
❌ **Font:** Computer Modern (LaTeX default serif font, not Calibri)
❌ **Title Page:** Added unwanted title page with centered text
❌ **Margins:** Very large/academic style
❌ **Headers:** Added page headers with italic section names
❌ **Spacing:** Too much whitespace between sections
❌ **Date Format:** Different style than master
❌ **Overall:** Looks like academic paper, not professional CV

---

## Root Cause

The YAML front matter I used was designed for Eisvogel template, but pandoc ran with **default LaTeX template** using **xelatex**. This caused:

1. **Titlepage: true** → Created unwanted title page
2. **No Calibri font loading** → Fell back to Computer Modern
3. **Academic formatting** → Large margins, headers, formal styling
4. **Wrong geometry** → Didn't respect margin specs

The command executed was:
```bash
pandoc ArturSwadzba_CV_Angi.md -o ArturSwadzba_CV_Angi.pdf --pdf-engine=xelatex
```

This **ignored the Eisvogel template** that was specified in generate-cv.md instructions.

---

## Solution Strategy

### Option 1: Direct LaTeX with Minimal Template (RECOMMENDED)
Write CV directly in LaTeX with minimal preamble, giving complete control over formatting.

**Pros:**
- Full control over every aspect of formatting
- Can match master CV exactly
- No dependency on pandoc templates
- Easier to debug and maintain

**Cons:**
- Requires writing LaTeX directly
- Slightly more complex syntax

### Option 2: Pandoc with Custom Template
Create custom pandoc template that matches master CV format.

**Pros:**
- Keep markdown workflow
- Reusable template

**Cons:**
- Template syntax complex
- Still dependent on pandoc behavior
- Harder to debug

### Option 3: Use Word/DOCX Instead of PDF
Generate DOCX from markdown, then convert to PDF.

**Pros:**
- Better font handling
- More familiar format

**Cons:**
- Loses some formatting control
- Requires Word or LibreOffice installed
- Extra conversion step

---

## RECOMMENDED APPROACH: Direct LaTeX Generation

### Step 1: Create LaTeX Template
Create `templates/cv-template.tex` that matches master CV exactly:

```latex
\documentclass[10pt,a4paper,sans]{moderncv}
\moderncvstyle{banking}
\moderncvcolor{blue}
\usepackage[utf8]{inputenc}
\usepackage[scale=0.85]{geometry} % Adjust margins

% Font
\usepackage{fontspec}
\setmainfont{Calibri}

% Personal info
\name{Artur}{Swadzba}
\address{Bromley, UK}{}{}
\phone[mobile]{+44~7383~431055}
\email{artur@swadzba.info}
\social[linkedin]{arturswadzba}

\begin{document}
\makecvtitle

% Content will be inserted here via script

\end{document}
```

**Issue:** moderncv might not match master exactly. **Better approach: Simple article class.**

### Step 2: Simpler LaTeX Approach

Use basic `article` class with manual formatting to match master:

```latex
\documentclass[10pt,a4paper]{article}
\usepackage[top=15mm,bottom=15mm,left=15mm,right=15mm]{geometry}
\usepackage{fontspec}
\setmainfont{Calibri}
\usepackage{xcolor}
\definecolor{headingblue}{RGB}{0,102,204}
\usepackage{hyperref}
\hypersetup{colorlinks=true, urlcolor=blue}

\pagestyle{plain}
\setlength{\parindent}{0pt}
\usepackage{titlesec}

% Section formatting (blue headers like master)
\titleformat{\section}{\Large\bfseries\color{headingblue}}{}{0em}{}[\titlerule]
\titleformat{\subsection}{\large\bfseries}{}{0em}{}

% Compact lists
\usepackage{enumitem}
\setlist{noitemsep,topsep=2pt,leftmargin=*}

\begin{document}

% Header
{\LARGE\bfseries Artur Swadzba}
\vspace{2mm}

\noindent Bromley, UK | +44 7383 431055 | \href{mailto:artur@swadzba.info}{artur@swadzba.info} | \href{https://www.linkedin.com/in/arturswadzba/}{linkedin.com/in/arturswadzba}

\vspace{4mm}
\section*{Data Platform Product Leader}
\vspace{-4mm}

[Content goes here...]

\end{document}
```

### Step 3: Python Script to Generate LaTeX from Plan

Create `scripts/generate-cv-latex.py`:

```python
#!/usr/bin/env python3
"""
Generate LaTeX CV from markdown content and tailoring plan
"""
import sys
import re
from pathlib import Path

def markdown_to_latex(md_content):
    """Convert markdown bullets to LaTeX"""
    # Convert bullets
    content = re.sub(r'^\- ', r'\\item ', md_content, flags=re.MULTILINE)
    # Escape special chars
    content = content.replace('$', '\\$')
    content = content.replace('&', '\\&')
    content = content.replace('%', '\\%')
    # Bold
    content = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', content)
    return content

def generate_cv_latex(application_folder):
    """Generate complete LaTeX CV"""
    # Read markdown CV
    md_file = application_folder / "ArturSwadzba_CV_Angi.md"
    # Parse and convert
    # Write LaTeX
    tex_file = application_folder / "ArturSwadzba_CV_Angi.tex"
    # Return tex_file path

# [Full implementation...]
```

### Step 4: Compile LaTeX to PDF

```bash
cd applications/2025-10-Angi-DirectorProductDataPlatform
xelatex ArturSwadzba_CV_Angi.tex
```

---

## ALTERNATIVE: Fix Pandoc Approach (Simpler Short-term)

Since we already have markdown, let's fix the pandoc command:

### Issues with Current YAML:
```yaml
titlepage: true  # ❌ Creates title page
mainfont: "Calibri"  # ❌ Not loaded correctly
geometry:  # ❌ Not applied
  - top=15mm
```

### Fixed YAML for Direct LaTeX Output:

```yaml
---
# NO title, author, date fields (causes title page)
documentclass: article
fontsize: 10pt
geometry:
  - a4paper
  - margin=15mm
mainfont: Calibri
mainfontoptions:
  - Ligatures=TeX
header-includes:
  - \usepackage{titlesec}
  - \usepackage{xcolor}
  - \definecolor{cvblue}{RGB}{0,102,204}
  - \titleformat{\section}{\Large\bfseries\color{cvblue}}{}{0em}{}[\titlerule]
  - \titleformat{\subsection}{\large\bfseries}{}{0em}{}
  - \setlength{\parindent}{0pt}
  - \pagenumbering{arabic}
  - \usepackage{enumitem}
  - \setlist{noitemsep,topsep=2pt,leftmargin=*}
  - \pagestyle{plain}
colorlinks: true
urlcolor: blue
linkcolor: blue
---
```

### Correct Pandoc Command:

```bash
pandoc ArturSwadzba_CV_Angi.md \
  -o ArturSwadzba_CV_Angi.pdf \
  --pdf-engine=xelatex \
  -V geometry:a4paper \
  -V geometry:margin=15mm \
  --no-highlight
```

---

## Implementation Plan

### Phase 1: Quick Fix (Generate Correct PDF Now)
1. ✅ Strip bad YAML from ArturSwadzba_CV_Angi.md
2. ✅ Add corrected YAML front matter
3. ✅ Regenerate with correct pandoc command
4. ✅ Verify: 2 pages, Calibri font, correct margins

### Phase 2: Update generate-cv.md Command
1. Fix YAML template in `.claude/commands/generate-cv.md`
2. Fix pandoc command in generate-cv.md
3. Add validation checks before generation

### Phase 3: Create Validation Script
Create `scripts/validate-cv-pdf.py`:

```python
#!/usr/bin/env python3
"""
Validate generated CV meets requirements
"""
import PyPDF2
import sys

def validate_cv(pdf_path):
    """Check CV formatting"""
    with open(pdf_path, 'rb') as f:
        pdf = PyPDF2.PdfReader(f)

        # Check page count
        num_pages = len(pdf.pages)
        if num_pages > 2:
            print(f"❌ FAIL: {num_pages} pages (should be 2 max)")
            return False

        # Check page size
        page = pdf.pages[0]
        width = float(page.mediabox.width) * 0.352778  # Convert to mm
        height = float(page.mediabox.height) * 0.352778
        if not (abs(width - 210) < 5 and abs(height - 297) < 5):
            print(f"❌ FAIL: Page size {width}x{height}mm (should be A4: 210x297mm)")
            return False

        # Check fonts (requires pdf parsing libraries)
        # TODO: Verify Calibri font is used

        print(f"✅ PASS: {num_pages} pages, A4 size")
        return True

if __name__ == "__main__":
    validate_cv(sys.argv[1])
```

### Phase 4: Integration into generate-cv Command
Add automatic validation after PDF generation:

```python
# In generate-cv.md instructions:
# After generating PDF, run validation:
python scripts/validate-cv-pdf.py applications/.../CV.pdf

# If validation fails:
# - Display errors
# - Do NOT proceed
# - Ask user to check formatting
```

---

## Guardrails to Implement

### 1. Pre-Generation Checks
```markdown
Before generating PDF:
- [ ] Verify YAML front matter has correct structure
- [ ] Verify mainfont is "Calibri"
- [ ] Verify geometry is a4paper with 15mm margins
- [ ] Verify no titlepage: true
- [ ] Verify documentclass is article
```

### 2. Post-Generation Validation
```markdown
After generating PDF:
- [ ] Run validate-cv-pdf.py script
- [ ] Check page count ≤ 2
- [ ] Check file size < 200KB (indicates images/bad formatting)
- [ ] Verify A4 dimensions (210×297mm)
- [ ] Display sample for human verification
```

### 3. Template Lock File
Create `templates/cv-yaml-template.yaml` as source of truth:

```yaml
# CV YAML Front Matter Template
# DO NOT MODIFY without updating validation
---
documentclass: article
fontsize: 10pt
geometry:
  - a4paper
  - margin=15mm
mainfont: Calibri
mainfontoptions:
  - Ligatures=TeX
colorlinks: true
urlcolor: blue
linkcolor: blue
header-includes:
  - \usepackage{titlesec}
  - \usepackage{xcolor}
  - \definecolor{cvblue}{RGB}{0,102,204}
  - \titleformat{\section}{\Large\bfseries\color{cvblue}}{}{0em}{}[\titlerule]
  - \setlength{\parindent}{0pt}
  - \usepackage{enumitem}
  - \setlist{noitemsep,topsep=2pt,leftmargin=*}
---
```

### 4. Update .claude/commands/generate-cv.md

Add section:
```markdown
## CRITICAL: PDF Formatting Requirements

**YAML Front Matter MUST use this exact structure:**
[Include template above]

**Pandoc Command MUST be:**
```bash
pandoc CV.md -o CV.pdf --pdf-engine=xelatex --no-highlight
```

**Validation MUST pass before delivering to user:**
```bash
python scripts/validate-cv-pdf.py CV.pdf
```
```

---

## Immediate Action Items

### NOW (Fix Current Angi CV):
1. Create corrected markdown with proper YAML
2. Regenerate PDF with correct pandoc command
3. Verify 2 pages, Calibri, proper formatting

### TODAY (Prevent Future Issues):
1. Update `.claude/commands/generate-cv.md` with correct YAML template
2. Add validation requirements to generate-cv.md
3. Create `templates/cv-yaml-template.yaml` lock file

### THIS WEEK (Robust Solution):
1. Create `scripts/validate-cv-pdf.py` validation script
2. Test with multiple CV generations
3. Document in `docs/cv-generation-workflow.md`

---

## Testing Plan

### Test Cases:
1. **Master CV Match Test**
   - Generate CV from master content with no modifications
   - Compare formatting to master PDF
   - Should be visually identical

2. **2-Page Limit Test**
   - Generate CV with maximum content
   - Verify stays within 2 pages
   - Check no content cut off

3. **Font Test**
   - Extract font info from generated PDF
   - Verify Calibri is used throughout
   - No fallback to Computer Modern

4. **Margin Test**
   - Measure margins from PDF
   - Verify 15mm all sides
   - Check text doesn't overflow

5. **Cross-Platform Test**
   - Generate on Windows (current environment)
   - Verify Calibri font available
   - Check xelatex can access system fonts

---

## Success Criteria

✅ Generated CV is 2 pages (max)
✅ Uses Calibri font throughout
✅ A4 paper size (210×297mm)
✅ Margins ~15mm all sides
✅ No title page
✅ Blue section headers with underline
✅ Professional CV appearance (not academic paper)
✅ Matches master CV visual style
✅ Validation script passes all checks
✅ generate-cv.md updated with guardrails
✅ Documented for future use

---

## Next Steps

**Immediate:**
```bash
# 1. Fix the Angi CV now
cd applications/2025-10-Angi-DirectorProductDataPlatform

# 2. Update markdown with correct YAML
# 3. Regenerate with correct command
# 4. Verify output
```

**Prevention:**
- Update generate-cv.md
- Create validation script
- Add to CI/CD workflow (if applicable)

---

**Status:** Ready to implement
**Priority:** HIGH - Angi CV needs to be fixed before application
**Owner:** Claude Code Agent
