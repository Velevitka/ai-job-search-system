# Eisvogel Template Assessment for CV Generation

**Date:** 2025-10-31
**Question:** Should we use Eisvogel template as specified in generate-cv.md?

---

## Eisvogel Template Analysis

### What is Eisvogel?
- **Purpose:** Designed for lecture notes, technical documentation, computer science papers
- **Style:** Academic/technical document formatting
- **Features:**
  - Title pages
  - Table of contents
  - Code syntax highlighting
  - Academic formatting
  - Headers/footers for long documents

### Eisvogel's Default Output
- Title page with centered title/author/date
- Academic document structure
- Larger margins (suitable for printing/binding)
- Headers with section names
- Designed for multi-page documents (10+ pages)
- Focus on readability for long-form content

### Why Eisvogel Failed for Our CV

**Error encountered:**
```
! LaTeX Error: Command \chead already defined.
```

**Reason:** My YAML front matter conflicted with Eisvogel's built-in header/footer system.

**Even if fixed:** Eisvogel would produce:
- ❌ Title page (we need header on page 1)
- ❌ Academic formatting (we need compact professional CV)
- ❌ Large margins (we need 15mm tight margins)
- ❌ Document structure for long content (we need 2-page CV)

---

## Master CV Requirements vs Eisvogel

| Requirement | Master CV | Eisvogel Output |
|------------|-----------|-----------------|
| **Page count** | 2 pages | 3-4+ pages (adds title page) |
| **First page** | Name + contact at top | Title page with centered text |
| **Margins** | Tight ~15mm | Academic ~25-30mm |
| **Font** | Calibri 10-11pt | Can be configured |
| **Headers** | None on page 1 | Headers on all pages |
| **Style** | Compact professional CV | Academic document |
| **Sections** | Blue headers with underline | Standard LaTeX sections |
| **Purpose** | Quick scan by recruiters | Long-form reading |

---

## Verdict: Eisvogel is NOT the Right Tool

### Why Eisvogel is Wrong:
1. ❌ **Design Philosophy Mismatch:** Academic docs ≠ Professional CV
2. ❌ **Page Count:** Adds title page, increases length
3. ❌ **Formatting:** Academic style vs compact CV style
4. ❌ **Customization Effort:** Would require heavy modification to match master
5. ❌ **Complexity:** Harder to control exact formatting

### Why generate-cv.md Specified Eisvogel:
The instructions in `.claude/commands/generate-cv.md` were written with the assumption that Eisvogel would produce professional formatting. This was **incorrect** - Eisvogel is for academic documents, not CVs.

**The instruction should be updated.**

---

## Recommended Approaches (Ranked)

### Option 1: Simple LaTeX Article Class (BEST FOR CV)
**Pros:**
- ✅ Full control over formatting
- ✅ Can match master CV exactly
- ✅ Compact 2-page output
- ✅ No unwanted features (title pages, TOC, etc.)
- ✅ Direct font control
- ✅ Exact margin specifications

**Cons:**
- Requires LaTeX knowledge (but simple)
- No markdown → we need conversion layer

**Implementation:**
```yaml
---
documentclass: article
fontsize: 10pt
geometry:
  - a4paper
  - top=15mm
  - bottom=15mm
  - left=15mm
  - right=15mm
mainfont: Calibri
header-includes:
  - \usepackage{titlesec}
  - \titleformat{\section}{\Large\bfseries\color{blue}}{}{0em}{}[\titlerule]
  - \setlength{\parindent}{0pt}
  - \usepackage{enumitem}
  - \setlist{noitemsep,topsep=2pt}
---
```

**Pandoc command:**
```bash
pandoc CV.md -o CV.pdf --pdf-engine=xelatex
```

---

### Option 2: ModernCV LaTeX Package
**Pros:**
- ✅ Specifically designed for CVs
- ✅ Professional CV templates
- ✅ Compact formatting
- ✅ Multiple style options

**Cons:**
- ❌ Harder to integrate with pandoc
- ❌ May not match master CV exactly
- ❌ Requires learning ModernCV syntax
- ❌ Less direct control

**Verdict:** Good for starting from scratch, but harder to match existing master CV design.

---

### Option 3: Pandoc-ModernCV (Pandoc + ModernCV)
Repository: https://github.com/barraq/pandoc-moderncv

**Pros:**
- ✅ Markdown → CV workflow
- ✅ CV-specific design
- ✅ Pandoc integration

**Cons:**
- ❌ Still requires matching master CV design
- ❌ Additional dependency
- ❌ May need template customization

**Verdict:** Potential future option, but adds complexity.

---

### Option 4: Keep Eisvogel But Heavily Customize
**Pros:**
- Follows current generate-cv.md instruction

**Cons:**
- ❌ Wrong tool for the job
- ❌ Requires extensive customization
- ❌ Still produces academic-style output
- ❌ Harder to maintain
- ❌ Title page difficult to disable properly

**Verdict:** Not recommended - fighting the template's design philosophy.

---

## Decision: Use Article Class (Option 1)

### Rationale:
1. **Simplest solution** for matching master CV exactly
2. **Full control** over every formatting aspect
3. **No unnecessary features** (title pages, TOC, fancy headers)
4. **Works with pandoc** directly via YAML front matter
5. **Easy to validate** and maintain

### What We Need to Do:

1. **Update .claude/commands/generate-cv.md**
   - Remove Eisvogel template reference
   - Replace with article class + custom YAML
   - Add validation requirements

2. **Create YAML Template**
   ```yaml
   # templates/cv-yaml-template.yaml
   ---
   documentclass: article
   fontsize: 10pt
   geometry:
     - a4paper
     - margin=15mm
   mainfont: Calibri
   colorlinks: true
   urlcolor: blue
   header-includes:
     - \usepackage{titlesec}
     - \usepackage{xcolor}
     - \definecolor{cvblue}{RGB}{0,102,204}
     - \titleformat{\section}{\Large\bfseries\color{cvblue}}{}{0em}{}[\titlerule]
     - \setlength{\parindent}{0pt}
     - \usepackage{enumitem}
     - \setlist{noitemsep,topsep=2pt,leftmargin=*}
     - \pagestyle{plain}
   ---
   ```

3. **Updated Pandoc Command**
   ```bash
   cd applications/YYYY-MM-CompanyName-Role
   pandoc ArturSwadzba_CV_CompanyName.md \
     -o ArturSwadzba_CV_CompanyName.pdf \
     --pdf-engine=xelatex \
     --no-highlight
   ```

4. **Validation Script**
   - Check page count ≤ 2
   - Verify A4 dimensions
   - Confirm no title page
   - Check file size reasonable

---

## Implementation Plan

### Phase 1: Fix Angi CV (Immediate)
1. ✅ Remove broken Eisvogel YAML
2. ✅ Add corrected article class YAML
3. ✅ Regenerate with simple pandoc command
4. ✅ Verify 2 pages, correct formatting

### Phase 2: Update Documentation (Today)
1. Update `.claude/commands/generate-cv.md`:
   - Remove Eisvogel references
   - Add correct YAML template
   - Update pandoc command
   - Add validation requirements

2. Create `templates/cv-yaml-template.yaml` as source of truth

3. Document rationale in `docs/cv-template-decision.md`

### Phase 3: Testing & Validation (This Week)
1. Test CV generation with multiple applications
2. Create `scripts/validate-cv-pdf.py`
3. Verify consistent 2-page output
4. Check Calibri font rendering

---

## Key Corrections to generate-cv.md

### BEFORE (Incorrect):
```markdown
Generate PDF using pandoc:
```bash
pandoc CV.md -o CV.pdf --template eisvogel --pdf-engine=xelatex
```

PDF Requirements:
- Uses Eisvogel template for professional appearance
```

### AFTER (Correct):
```markdown
Generate PDF using pandoc:
```bash
pandoc CV.md -o CV.pdf --pdf-engine=xelatex --no-highlight
```

PDF Requirements:
- Uses article class with custom YAML for professional CV appearance
- NO Eisvogel template (designed for academic documents, not CVs)
- Calibri font, tight margins, 2-page limit
```

---

## Testing Checklist

After implementing article class approach:
- [ ] Generate CV produces exactly 2 pages
- [ ] Uses Calibri font throughout
- [ ] A4 paper size (210×297mm)
- [ ] Margins are ~15mm all sides
- [ ] No title page
- [ ] Blue section headers with underline
- [ ] Dates right-aligned properly
- [ ] Bullet points compact (not spread out)
- [ ] Visually matches master CV style
- [ ] File size < 100KB (no bloat)

---

## Conclusion

**Eisvogel is the wrong tool.** It was incorrectly specified in generate-cv.md because:
1. Eisvogel is designed for academic documents (lecture notes, technical papers)
2. It produces 3-4+ page documents with title pages
3. It has academic formatting unsuitable for professional CVs
4. It would require extensive customization to match master CV

**Article class is the right tool** because:
1. Simple, minimal, gives full control
2. Can match master CV exactly
3. Produces compact 2-page output
4. No unnecessary features
5. Easy to maintain and validate

**Action:** Update generate-cv.md to use article class instead of Eisvogel.

---

**Status:** Analysis complete - ready to implement article class approach
**Priority:** HIGH - Fix Angi CV + update generate-cv.md
