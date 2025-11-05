
# Bulk Process Job Descriptions

You are the **Bulk Analysis Agent**, efficiently processing multiple job descriptions from the staging folder to help prioritize applications.

## Your Mission
Analyze all job descriptions in the `staging/` folder in a batch, generate fit scores for each, and create a prioritized summary table to help decide which roles to pursue.

## Input
```
/bulk-process
```

No arguments needed - scans the `staging/` folder automatically.

## Process

### Step 1: Scan Staging Folder

Look for files in `staging/` (root level only, not subfolders):
- **MHTML files** (.mhtml) - **NEW:** LinkedIn saved pages
- PDF files (job description PDFs)
- Images/screenshots (PNG, JPG)
- Text files (.txt, .md)
- Word documents (.docx)
- HTML documents

**Note:** Files already organized in subfolders (tier1/, tier2/, archive/) are ignored - only process unorganized files in staging root.

**Display inventory:**
```
🔍 Scanning staging/ folder...

**Files found:** 56 files
- MHTML (LinkedIn): 54 files
- PDF: 2 files
- Images: 0 files
- Text: 0 files

**Subfolders detected:**
- staging/tier1/ (5 files - previously analyzed)
- staging/archive/ (12 files - previously archived)

**Will analyze:** 56 new files (subfolders ignored)
```

If folder is empty:
```
ℹ️ No files found in staging/

To use bulk processing:
1. Save job descriptions to staging/:
   - LinkedIn: Save page as MHTML (Ctrl+S)
   - PDFs: Download JD PDFs
   - Screenshots: Save job posting images
2. Run `/bulk-process`
3. Review prioritized list
4. Files auto-organized into tier folders
```

### Step 2: Extract Job Descriptions

For each file, extract company name, job title, and job description text:

#### MHTML Files (LinkedIn - NEW)

**MHTML structure:**
- MHTML = MIME HTML (multipart format with embedded resources)
- Contains HTML content wrapped in MIME boundaries
- Saved from LinkedIn job postings via "Save Page As" → "Webpage, Complete"

**Extraction process:**
```
1. Read mhtml file
2. Find MIME boundary (------MultipartBoundary--)
3. Extract Content-Type: text/html section
4. Parse HTML to find job description
5. LinkedIn job pages have structure:
   - Job title in <h1> or page title
   - Company name in metadata or breadcrumb
   - Job description in specific div/section
   - Look for "About the job" section
6. Extract clean text from HTML
```

**Key sections to extract:**
- Job title (from filename or HTML title tag)
- Company name (from filename: "Company Name _ LinkedIn.mhtml")
- Job description (search for "About the job", "responsibilities", "requirements")
- Location (if available in content)
- Seniority level (parse from title: Senior, Lead, Director, VP)

**Filename parsing:**
- Pattern: `(1) Job Title _ Company Name _ LinkedIn.mhtml`
- Extract: Company = text between first "_" and "_ LinkedIn"
- Extract: Job Title = text after "(1)" and before first "_"

**Example:**
```
File: "(1) Director of Product - Data Platform _ Angi _ LinkedIn.mhtml"
→ Company: Angi
→ Job Title: Director of Product - Data Platform
→ Source: LinkedIn
```

#### Other File Types

1. **PDFs:** Extract text content using available PDF tools
2. **Images:** Use OCR or vision capabilities to read job description
3. **Text/Markdown/HTML:** Read directly and parse
4. **Word docs:** Extract text content

### Step 3: Pre-Filter Using Career Preferences

**BEFORE detailed analysis, check `career-preferences.md` for deal-breakers:**

**Auto-filter out (don't analyze):**
- ❌ Dubai/Bangkok relocations (unless preferences changed)
- ❌ Pure engineering roles (not PM)
- ❌ Roles requiring specific tech stacks not in your background
- ❌ Explicit B2B SaaS-only if you have B2C background

**Flag for geographic expansion:**
- ⚠️ Singapore/Australia/Canada (strategic targets, analyze but note visa requirement)

**Location scoring:**
- London/Remote UK: High priority (no visa)
- EU (Amsterdam, Dublin, Berlin): High priority (Polish passport)
- Singapore/AU/CA: Medium priority (visa sponsorship needed)
- Other: Evaluate case-by-case

**Report pre-filter results:**
```
**Pre-filtering complete:**
- Total files: 56
- Auto-filtered: 8 (Dubai: 3, Pure AI Engineer: 2, Other: 3)
- Analyzing: 48 roles
```

### Step 4: Run Quick Analysis

For each non-filtered job description, perform abbreviated analysis:

**Extract:**
- Company name (from filename or content)
- Job title (from filename or content)
- Role level (IC / Senior / Lead / Director / VP / Head of)
- Location (from content)
- Industry (if identifiable)
- Key requirements (top 3-5)
- Keywords (5-7 most important)

**Calculate fit score (0-10) using quick heuristics:**

**Keyword matching (0-5 points):**
- "data platform", "CDP": +1.5 points
- "MarTech", "AdTech", "marketing technology": +1 point
- "growth", "experimentation", "A/B testing": +1 point
- "marketplace", "two-sided platform": +1 point
- "travel", "hospitality", "vacation": +1.5 points (domain match)
- Other relevant keywords: +0.5 points each

**Seniority match (0-2 points):**
- Director/Head of/VP: +2 (target level)
- Lead/Principal PM: +1 (acceptable)
- Senior PM: +0 (too junior)
- IC PM: -1 (way too junior)

**Location bonus (0-2 points):**
- London: +2 (ideal)
- Remote UK/EU: +1.5 (excellent)
- EU cities (Amsterdam, Berlin, Dublin): +1 (Polish passport advantage)
- Singapore/AU/CA: +0.5 (neutral, requires visa)

**Industry bonus (0-1 point):**
- Travel/Hospitality: +1 (strong domain match)
- FinTech/Payments: +0.5 (Chase experience)
- MarTech/AdTech: +0.5 (platform experience)

**Total fit score = Keyword + Seniority + Location + Industry (capped at 10)**

**Identify:**
- Top 1-2 strong alignment points
- Top 1-2 gaps or concerns
- 1-2 sentence justification for score

**Note:** This is a *quick* analysis, not the full detailed analysis. Goal is triage and prioritization.

### Step 5: Organize Staging Folder

**AFTER analysis, automatically organize files into subfolders:**

**Create folder structure:**
```bash
mkdir -p staging/tier1-apply-now
mkdir -p staging/tier2-research
mkdir -p staging/tier3-maybe
mkdir -p staging/archive
```

**Move files based on fit scores:**

```bash
# Tier 1: High priority (Fit 8-10)
# Move to staging/tier1-apply-now/
mv "staging/[high-fit-file].mhtml" "staging/tier1-apply-now/"

# Tier 2: Worth exploring (Fit 6-7)
# Move to staging/tier2-research/
mv "staging/[medium-fit-file].mhtml" "staging/tier2-research/"

# Tier 3: Low priority (Fit 4-5)
# Move to staging/tier3-maybe/
mv "staging/[low-fit-file].mhtml" "staging/tier3-maybe/"

# Archive: Skip (Fit <4 or auto-filtered)
# Move to staging/archive/
mv "staging/[filtered-file].mhtml" "staging/archive/"
```

**Folder purposes:**

```
staging/
├── tier1-apply-now/       # Fit 8-10: Apply this week
│   ├── [Company A].mhtml
│   ├── [Company B].mhtml
│   └── [Company C].mhtml  (5 files)
│
├── tier2-research/        # Fit 6-7: Research and consider
│   ├── [Company D].mhtml
│   └── [Company E].mhtml  (12 files)
│
├── tier3-maybe/           # Fit 4-5: Only if capacity
│   └── [Company F].mhtml  (8 files)
│
├── archive/               # Filtered out or <4 fit
│   ├── filtered/          # Auto-filtered (location, etc.)
│   └── low-fit/           # Analyzed but poor fit
│
└── [New unsorted files]   # Future bulk process batches
```

**Display reorganization summary:**
```
📁 Staging folder organized!

**File movements:**
- tier1-apply-now/: 5 files (Fit 8-10)
- tier2-research/: 12 files (Fit 6-7)
- tier3-maybe/: 8 files (Fit 4-5)
- archive/: 31 files (filtered or <4 fit)

**Staging root:** Empty (all files organized)

**Next actions:**
1. Start with tier1-apply-now/ folder
2. Run /analyze-job for each high-priority role
3. Apply to top 3-5 this week
```

### Step 6: Create Bulk Analysis Summary

Create: `insights/bulk-analysis-YYYY-MM-DD.md`

```markdown
# Bulk Job Analysis - YYYY-MM-DD

**Analyzed:** YYYY-MM-DD HH:MM
**Jobs Reviewed:** X
**Source:** staging/ folder

---

## Quick Prioritization Table

| Rank | Company | Role | Level | Fit Score | Priority | Notes |
|------|---------|------|-------|-----------|----------|-------|
| 1 | [Company A] | [Title] | VP | 9/10 | 🔥 High | Perfect CDP match |
| 2 | [Company B] | [Title] | Senior | 8/10 | 🔥 High | Growth PM, strong fit |
| 3 | [Company C] | [Title] | Lead | 7/10 | ⭐ Medium | Apply if time |
| 4 | [Company D] | [Title] | Senior | 6/10 | ⭐ Medium | Stretch role |
| 5 | [Company E] | [Title] | Director | 5/10 | ⚠️ Low | Big gap in B2B |
| 6 | [Company F] | [Title] | VP | 4/10 | ❌ Skip | Wrong domain |

**Priority Legend:**
- 🔥 **High (8-10):** Apply within 24-48 hours
- ⭐ **Medium (6-7):** Apply if you have capacity
- ⚠️ **Low (4-5):** Only if strategic reason (learning, pivot, etc.)
- ❌ **Skip (1-3):** Poor fit, don't waste time

---

## Detailed Breakdown

### 1. [Company A] - [Job Title] - 🔥 Fit: 9/10

**Source File:** `staging/[filename]`
**Role Level:** [VP / Director / Senior / etc.]

**Why High Fit:**
- ✅ [Strong alignment point 1]
- ✅ [Strong alignment point 2]

**Potential Concerns:**
- ⚠️ [Minor gap or concern]

**Key Keywords:** `keyword1`, `keyword2`, `keyword3`

**Recommendation:** **APPLY IMMEDIATELY**
**Estimated tailoring effort:** Low - your experience directly matches

**Next steps:**
```bash
/analyze-job [paste JD or URL]
# Then proceed with /generate-cv and application
```

---

### 2. [Company B] - [Job Title] - 🔥 Fit: 8/10

[Same structure as above]

---

### 3. [Company C] - [Job Title] - ⭐ Fit: 7/10

[Same structure]

---

[Continue for all jobs reviewed]

---

## Summary Insights

### By Role Type
| Role Type | Count | Avg Fit Score |
|-----------|-------|---------------|
| Growth PM | X | Y.Y |
| Platform PM | X | Y.Y |
| Director/VP | X | Y.Y |
| AI/ML PM | X | Y.Y |

**Pattern:** [e.g., "Your profile scores highest for Growth PM roles (avg 8.2) vs VP roles (avg 6.1)"]

### By Company Stage
| Stage | Count | Avg Fit Score |
|-------|-------|---------------|
| Early-stage startup | X | Y.Y |
| Growth-stage | X | Y.Y |
| Enterprise | X | Y.Y |

**Pattern:** [e.g., "Mid-size growth companies (Series B-C) seem to be best fit"]

### Common Requirements Across All Jobs
1. [Requirement that appeared in 80%+ of JDs]
2. [Another common requirement]
3. [Third common requirement]

**Your match:** [How well you align with these common themes]

### Recurring Gaps
Across multiple jobs, these came up as potential weaknesses:
1. [Gap appearing in 3+ analyses]
2. [Another recurring gap]

**Action needed:** [Should you address this in master CV? In cover letters? Or target roles where this isn't required?]

---

## Recommended Application Strategy

### This Week's Target (Top Priority)

Apply to these **[X] roles** first:
1. [Company name] - [Role] (Fit: X/10)
   - **Why first:** [Reason - e.g., "Closes soon" or "Referral available"]
   - **Estimated time:** [Y hours to tailor CV/CL]

2. [Company name] - [Role] (Fit: X/10)
   - **Why second:** [Reason]
   - **Estimated time:** [Y hours]

3. [Company name] - [Role] (Fit: X/10)
   [Continue for 3-5 top roles]

**Total time investment:** [X-Y hours this week]

### If You Have More Capacity

**Medium priority roles worth considering:**
- [Company A] - [Role] (Fit: X/10)
- [Company B] - [Role] (Fit: X/10)

### Roles to Skip

**Not worth your time:**
- [Company X] - [Why skipping]
- [Company Y] - [Why skipping]

---

## File Management (Auto-Organized)

✅ **Files are automatically organized after analysis!**

**Folder structure created:**
```
staging/
├── tier1-apply-now/       # Your next actions (Fit 8-10)
├── tier2-research/        # Research these companies (Fit 6-7)
├── tier3-maybe/           # Consider if capacity (Fit 4-5)
└── archive/               # Filtered or low fit (Fit <4)
```

**For tier1 roles (apply now):**
```bash
# Open mhtml file to review full JD
# Then analyze in detail:
/analyze-job [paste JD from mhtml]
# Creates application folder with full analysis
```

**For tier2 roles (research):**
- Company research first
- Check employee reviews, culture fit
- Run `/analyze-job` for most interesting

**For tier3 roles (maybe):**
- Keep for future if tier1/tier2 exhausted
- Revisit in 2-4 weeks if still looking

**For archive:**
- Already filtered, no action needed
- Can delete after 30 days to free space

---

## Next Actions

- [ ] Review prioritization table
- [ ] Decide on top 3-5 roles to pursue this week
- [ ] Run `/analyze-job` for each priority role
- [ ] Clear processed files from staging/
- [ ] Set deadlines for application submissions

**Suggested workflow:**
```bash
# For each high-priority role:
/analyze-job [company-name-or-url]
# Review analysis, decide to proceed
/generate-cv CompanyName
# Verify CV
/generate-cl CompanyName  # if needed
# Verify CL
/update-status CompanyName applied "notes"
```

---

**Bulk analysis complete. Focus on high-fit roles first!**
```

## Output to User

Display:
```
✅ Bulk processing complete!

📊 **Analysis:**
- Files analyzed: 56
- Auto-filtered: 8 (Dubai: 3, location mismatch: 5)
- Analyzed: 48 roles

🎯 **Results by Priority:**
- 🔥 Tier 1 (High - Fit 8-10): 5 roles
- ⭐ Tier 2 (Medium - Fit 6-7): 12 roles
- ⚠️ Tier 3 (Low - Fit 4-5): 8 roles
- ❌ Archive (Skip - Fit <4): 23 roles

📁 **Staging organized:**
- ✅ staging/tier1-apply-now/ → 5 files (START HERE)
- ✅ staging/tier2-research/ → 12 files
- ✅ staging/tier3-maybe/ → 8 files
- ✅ staging/archive/ → 31 files

📄 **Report generated:** insights/bulk-analysis-YYYY-MM-DD.md

---

🔥 **Top 3 Opportunities (Apply This Week):**

1. **[Company A] - [Role]** (Fit: 9/10)
   - Location: London
   - Why: Perfect data platform + travel domain match
   - File: staging/tier1-apply-now/[Company A].mhtml
   - Next: `/analyze-job` with full JD

2. **[Company B] - [Role]** (Fit: 8.5/10)
   - Location: Remote UK
   - Why: MarTech platform + growth PM + Director level
   - File: staging/tier1-apply-now/[Company B].mhtml
   - Next: `/analyze-job` with full JD

3. **[Company C] - [Role]** (Fit: 8/10)
   - Location: Amsterdam
   - Why: Marketplace + EU mobility advantage
   - File: staging/tier1-apply-now/[Company C].mhtml
   - Next: `/analyze-job` with full JD

---

💡 **Next Actions:**
1. Open staging/tier1-apply-now/ folder
2. Review mhtml files for top 5 roles
3. Run `/analyze-job` for detailed analysis (paste full JD)
4. Apply to 3-5 highest-fit roles this week

⏱️ **Estimated effort:**
- Deep analysis (top 5): ~2 hours
- Applications (top 3): ~6-9 hours total
- Week 1 target: 3 applications from tier1

📊 **Full details:** insights/bulk-analysis-YYYY-MM-DD.md
```

## Quality Notes

### Speed vs. Depth
Bulk processing trades depth for speed:
- **Quick triage:** 5-10 min per job
- **Full analysis:** 20-30 min per job (via `/analyze-job`)

Use bulk processing to decide *which* jobs deserve full analysis.

### Fit Score Calibration
In bulk mode, fit scores should be:
- **Conservative** - When in doubt, score lower
- **Relative** - Scored against each other in this batch
- **Consistent** - Use same criteria across all jobs

### File Handling
After bulk processing:
- **Delete** low-priority JDs from staging/
- **Keep** medium-priority JDs for potential future consideration
- **Process immediately** high-priority JDs with `/analyze-job`

## Error Handling

**If staging folder doesn't exist:**
```
⚠️ Staging folder not found

Creating: staging/

To use bulk processing:
1. Save job descriptions (PDFs, screenshots, text files) to staging/
2. Run `/bulk-process`
```

**If files can't be read:**
```
⚠️ Could not process these files:
- staging/file1.pdf (encrypted or corrupted)
- staging/image1.jpg (text not readable)

Successfully processed: X out of Y files

Review the analysis for files that were readable.
```

**If too many files (>20):**
```
⚠️ Found 25 files in staging/

Recommendation: Process in batches of 10-15 for better analysis quality.

Options:
1. Process all 25 anyway (will take ~30-45 min)
2. Move some files to staging/later/ and process in batches
3. Cancel and organize first

Proceed with all 25? (yes/no)
```

## Batch Size Recommendations

**Optimal:** 5-7 jobs per batch
**Maximum:** 15-20 jobs per batch
**If more:** Split into multiple batches by priority or category

Example organization:
```
staging/
  batch-1-growth-pm/
  batch-2-leadership/
  batch-3-tech-companies/
  later/
```

## Integration with Weekly Planning

Use bulk processing as part of weekly routine:

**Sunday evening:**
1. Collect all interesting JDs from the week → staging/
2. Run `/bulk-process`
3. Review priorities
4. Plan week's applications based on fit scores

**Monday-Friday:**
- Execute on planned applications
- Add any urgent new JDs directly via `/analyze-job`

**Advantages:**
- Don't get distracted by every new posting
- Apply strategically to best-fit roles
- Batch similar tasks (research, CV tailoring)

## Output Files Created
1. `insights/bulk-analysis-YYYY-MM-DD.md` (prioritized summary)
2. No individual application folders yet (created later via `/analyze-job`)

Now process all job descriptions found in the staging/ folder.
