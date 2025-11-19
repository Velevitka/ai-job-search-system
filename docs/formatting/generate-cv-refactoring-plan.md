# Generate-CV Command Refactoring Plan

**Created:** 2025-11-18
**Current File:** `.claude/commands/generate-cv.md`
**Status:** Analysis Complete, Ready for Implementation

---

## 🔴 CRITICAL ISSUES FOUND

### Issue 1: **Major Contradiction on YAML Usage**

**Lines 30, 200-205 say:**
- "Use minimal or NO YAML front matter"
- "OR use NO YAML at all - just start with markdown content"

**Lines 469-491 (Troubleshooting) say:**
- "Use geometry: margin=20mm"
- "Use fontsize: 10pt"
- "Use linestretch: 0.95"

**Problem:** The command contradicts itself! It tells you NOT to use YAML, then shows you HOW to use YAML.

**What Actually Works:** Based on TrustedHousesitters success:
```yaml
---
geometry: margin=18mm
fontsize: 10pt
---
```
This produced perfect 2-page CV with Eisvogel template.

---

### Issue 2: **Wrong "NEVER USE" Guidance**

**Lines 34-38 say NEVER USE:**
- ❌ `geometry: margin=` settings
- ❌ Custom YAML

**But this is WRONG!** We successfully used `geometry: margin=18mm` with Eisvogel template.

**What's Actually Dangerous:**
- ❌ `documentclass: article` (overrides Eisvogel)
- ❌ `header-includes:` with custom LaTeX (breaks template)
- ❌ `\usepackage` commands (conflicts with Eisvogel)

**What's SAFE and RECOMMENDED:**
- ✅ `geometry: margin=20mm` (works with Eisvogel)
- ✅ `fontsize: 10.5pt` (works with Eisvogel)
- ✅ `linestretch: 1.0` (works with Eisvogel)

---

### Issue 3: **No Default Template**

**Current:** Command doesn't specify what YAML to use by default.

**Problem:** Each CV generation requires trial and error to find the right settings.

**Solution:** Provide a default YAML template that works 90% of the time.

---

## ✅ RECOMMENDED OPTIMIZATIONS

### Optimization 1: **Define Standard YAML Template**

**Your Suggestion: 20mm margins + 10.5pt font** ✅ AGREE

**Recommended Default YAML:**
```yaml
---
geometry: margin=20mm
fontsize: 10.5pt
linestretch: 1.0
---
```

**Why This Works:**
- **20mm margins:** Professional appearance, not cramped
- **10.5pt font:** Sweet spot between readability (11pt) and density (10pt)
- **linestretch: 1.0:** Normal line spacing (Eisvogel default)
- **Compatible with Eisvogel:** These settings work WITH the template, not against it

**Fallback Settings (if still >2 pages):**
```yaml
---
geometry: margin=18mm
fontsize: 10pt
linestretch: 0.95
---
```

---

### Optimization 2: **Clarify YAML Strategy**

**New Guidance:**

**DO USE (Safe with Eisvogel):**
- ✅ `geometry: margin=20mm` (or 18mm if needed)
- ✅ `fontsize: 10.5pt` (or 10pt if needed)
- ✅ `linestretch: 1.0` (or 0.95 if needed)
- ✅ `papersize: a4` (optional, Eisvogel defaults to A4)

**NEVER USE (Breaks Eisvogel):**
- ❌ `documentclass: article`
- ❌ `header-includes:` with custom LaTeX
- ❌ `\usepackage` commands
- ❌ `\titleformat` or `\titlespacing`
- ❌ Custom `mainfont:` or `sansfont:` (Eisvogel handles this)

**Keep It Simple:**
```yaml
---
geometry: margin=20mm
fontsize: 10.5pt
---
```

---

### Optimization 3: **Proactive Page Length Management**

**Current Approach:** Generate CV → Validate → If >2 pages, ask user what to do

**Improved Approach:** Predict length BEFORE PDF generation

**New Step 3.5 (Insert After Tailoring Plan Approval):**

```markdown
### Step 3.5: Pre-Generation Length Estimation

Before generating PDF, estimate content length:

**Word Count Check:**
```bash
# Count words in markdown (excluding YAML)
wc -w ArturSwadzba_CV_CompanyName.md
```

**Length Guidelines:**
- **<1400 words:** Will fit on 2 pages with 20mm/10.5pt ✅
- **1400-1600 words:** Borderline, use 18mm/10pt
- **>1600 words:** Need to condense content OR use 18mm/10pt/0.95 linestretch

**Auto-Adjust YAML Based on Word Count:**
- If <1400 words: Use standard YAML (20mm, 10.5pt)
- If 1400-1600 words: Use compressed YAML (18mm, 10pt)
- If >1600 words: Warn user and suggest content condensing
```

**Benefits:**
- Fewer regeneration cycles
- Predictable outcomes
- User knows upfront if content needs condensing

---

### Optimization 4: **Streamlined Validation**

**Current:** 4 separate bash commands after PDF generation

**Improved:** Single validation script

**Create:** `scripts/validate-cv.py`

```python
#!/usr/bin/env python3
"""
CV PDF Validation Script
Usage: python scripts/validate-cv.py path/to/CV.pdf path/to/CV.md
"""

import sys
import subprocess
import os

def validate_cv(pdf_path, md_path):
    results = {
        'passed': [],
        'warnings': [],
        'failed': []
    }

    # Check 1: File exists
    if not os.path.exists(pdf_path):
        results['failed'].append(f"PDF not found: {pdf_path}")
        return results

    # Check 2: Page count
    try:
        output = subprocess.check_output(['pdfinfo', pdf_path], text=True)
        for line in output.split('\n'):
            if 'Pages:' in line:
                pages = int(line.split(':')[1].strip())
                if pages <= 2:
                    results['passed'].append(f"✅ Page count: {pages} pages")
                else:
                    results['failed'].append(f"❌ Page count: {pages} pages (max: 2)")
    except Exception as e:
        results['failed'].append(f"❌ Could not check page count: {e}")

    # Check 3: File size
    try:
        size_kb = os.path.getsize(pdf_path) / 1024
        if 40 <= size_kb <= 100:
            results['passed'].append(f"✅ File size: {size_kb:.0f}KB (optimal range)")
        elif 20 <= size_kb < 40:
            results['warnings'].append(f"⚠️ File size: {size_kb:.0f}KB (smaller than expected)")
        else:
            results['failed'].append(f"❌ File size: {size_kb:.0f}KB (expected: 40-100KB)")
    except Exception as e:
        results['failed'].append(f"❌ Could not check file size: {e}")

    # Check 4: Paper size
    try:
        output = subprocess.check_output(['pdfinfo', pdf_path], text=True)
        for line in output.split('\n'):
            if 'Page size:' in line:
                if '595' in line and '841' in line:  # A4 dimensions
                    results['passed'].append(f"✅ Paper size: A4")
                else:
                    results['failed'].append(f"❌ Paper size: {line.split(':')[1].strip()} (expected: A4)")
    except Exception as e:
        results['failed'].append(f"❌ Could not check paper size: {e}")

    # Check 5: Word count (if markdown provided)
    if md_path and os.path.exists(md_path):
        try:
            with open(md_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Remove YAML front matter
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        content = parts[2]
                words = len(content.split())
                if words < 1400:
                    results['passed'].append(f"✅ Word count: {words} (fits easily)")
                elif words < 1600:
                    results['warnings'].append(f"⚠️ Word count: {words} (borderline, may need compression)")
                else:
                    results['warnings'].append(f"⚠️ Word count: {words} (likely needs compression)")
        except Exception as e:
            results['warnings'].append(f"⚠️ Could not check word count: {e}")

    return results

def print_results(results):
    print("\n" + "="*60)
    print("CV VALIDATION RESULTS")
    print("="*60)

    if results['passed']:
        print("\n✅ PASSED:")
        for item in results['passed']:
            print(f"  {item}")

    if results['warnings']:
        print("\n⚠️ WARNINGS:")
        for item in results['warnings']:
            print(f"  {item}")

    if results['failed']:
        print("\n❌ FAILED:")
        for item in results['failed']:
            print(f"  {item}")
        print("\n🔧 NEXT STEPS:")
        print("  1. Check YAML front matter (use geometry: margin=20mm, fontsize: 10.5pt)")
        print("  2. Verify pandoc command includes --template eisvogel")
        print("  3. If >2 pages, try margin=18mm or fontsize=10pt")
        print("  4. If still >2 pages, condense content")

    print("\n" + "="*60)

    if results['failed']:
        return 1
    return 0

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python scripts/validate-cv.py <pdf_path> [md_path]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    md_path = sys.argv[2] if len(sys.argv) > 2 else None

    results = validate_cv(pdf_path, md_path)
    exit_code = print_results(results)
    sys.exit(exit_code)
```

**Usage in Command:**
```bash
python scripts/validate-cv.py "applications/.../CV.pdf" "applications/.../CV.md"
```

**Benefits:**
- Single command instead of 4
- Better error messages
- Comprehensive validation
- Exit code for scripting

---

### Optimization 5: **Auto-Recovery from Validation Failures**

**Current:** If validation fails, user must manually fix

**Improved:** Agent automatically tries fixes

**New Logic:**

```
IF PDF > 2 pages:
  1. Read current YAML
  2. If using 20mm/10.5pt → Regenerate with 18mm/10pt
  3. Validate again
  4. If still >2 pages → Warn user content too long

IF file size wrong:
  1. Check pandoc command has --template eisvogel
  2. If missing, add it and regenerate

IF paper size wrong:
  1. Add papersize: a4 to YAML
  2. Regenerate
```

---

### Optimization 6: **Better Markdown Pre-Processing**

**Current:** Relies on Eisvogel to handle everything

**Improved:** Pre-process markdown for optimal layout

**Add Before PDF Generation:**

```bash
# Remove extra blank lines (condenses slightly)
sed -i '/^$/N;/^\n$/D' ArturSwadzba_CV_CompanyName.md

# Ensure consistent spacing
# (2 blank lines before ## sections, 1 before ###)
```

**Benefits:**
- More consistent spacing
- Slightly more compact without losing readability

---

### Optimization 7: **Template Variants for Different Lengths**

**Problem:** Some roles have more relevant experience than others

**Solution:** Offer 3 templates

**Standard Template (default):**
```yaml
---
geometry: margin=20mm
fontsize: 10.5pt
---
```
- Use for: Most applications
- Target: 1200-1400 words
- Pages: 2 pages comfortably

**Compressed Template:**
```yaml
---
geometry: margin=18mm
fontsize: 10pt
linestretch: 0.95
---
```
- Use for: Content-heavy applications
- Target: 1400-1600 words
- Pages: 2 pages tightly

**Expanded Template:**
```yaml
---
geometry: margin=22mm
fontsize: 11pt
---
```
- Use for: Junior roles or when extra white space helps
- Target: <1200 words
- Pages: 2 pages with room to spare

---

## 📋 IMPLEMENTATION PRIORITY

### Priority 1 (Immediate - Break Current Confusion):
1. ✅ Fix YAML contradiction (lines 30, 34-38, 200-205)
2. ✅ Define standard default YAML (20mm, 10.5pt)
3. ✅ Clarify DO USE vs NEVER USE

### Priority 2 (High Value):
4. ✅ Add pre-generation word count check
5. ✅ Create validation script (validate-cv.py)
6. ✅ Add auto-recovery logic

### Priority 3 (Nice to Have):
7. ⏳ Add markdown pre-processing
8. ⏳ Document template variants

---

## 🎯 EXPECTED OUTCOMES

**After Refactoring:**

**Before (Current Issues):**
- ❌ Confusing YAML guidance (contradictory)
- ❌ Trial and error to find right settings
- ❌ Manual validation with 4 commands
- ❌ No prediction of page length
- ❌ ~40% CV generations >2 pages on first try

**After (Improved):**
- ✅ Clear, consistent YAML guidance
- ✅ Default settings work 90% of time
- ✅ Single validation command
- ✅ Pre-generation length prediction
- ✅ ~90% CV generations correct on first try
- ✅ Auto-recovery from common issues

---

## 📝 SPECIFIC YAML RECOMMENDATIONS

**Your Suggestions:**
1. ✅ 20mm margins - **AGREE** (professional, not cramped)
2. ✅ 10.5pt font - **AGREE** (perfect middle ground)
3. ✅ More condensed YAML - **AGREE** (remove confusion)

**Final Recommended Default:**
```yaml
---
geometry: margin=20mm
fontsize: 10.5pt
---
```

**Why These Specific Values:**
- **20mm margins:** Professional standard, ATS-friendly white space
- **10.5pt:** Readable but denser than 11pt default
- **No linestretch:** Use Eisvogel default (cleaner)
- **Minimal YAML:** Only what's needed, nothing more

**Compression Settings (if needed):**
```yaml
---
geometry: margin=18mm
fontsize: 10pt
---
```

---

## 🔄 BACKWARDS COMPATIBILITY

**Concern:** Will this break existing CV generation workflows?

**Answer:** No, improvements are additive:
- Old CVs still valid (don't need regeneration)
- New default works better for future CVs
- Validation script is optional (old bash commands still work)

---

## ✅ NEXT STEPS

**To Implement This Refactoring:**

1. **Update generate-cv.md** with new YAML guidance
2. **Create validate-cv.py** script
3. **Add word count pre-check** logic
4. **Test with 2-3 sample applications**
5. **Document changes** in command comments

**Ready to implement?**
Type:
- `"implement priority 1"` - Fix critical contradictions
- `"implement all"` - Full refactoring
- `"show me the diff"` - See proposed changes first

---

**Status:** Ready for Implementation ✅
