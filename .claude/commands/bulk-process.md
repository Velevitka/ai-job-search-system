
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

Look for files in `staging/`:
- PDF files (job description PDFs)
- Images/screenshots (PNG, JPG)
- Text files (.txt, .md)
- Word documents (.docx)

If folder is empty:
```
ℹ️ No files found in staging/

To use bulk processing:
1. Save job description PDFs, screenshots, or text files to staging/
2. Run `/bulk-process`
3. Review prioritized list and decide which to pursue
```

### Step 2: Extract Job Descriptions

For each file:
1. **PDFs:** Extract text content
2. **Images:** Use OCR or vision capabilities to read job description
3. **Text/Markdown:** Read directly
4. **Word docs:** Extract text content

### Step 3: Run Quick Analysis

For each job description, perform abbreviated analysis:

**Extract:**
- Company name
- Job title
- Role level (IC / Senior / Lead / Director / VP)
- Key requirements (top 3-5)
- Keywords (5-7 most important)

**Calculate:**
- Fit score (X/10) based on master CV
- 1-2 sentence justification for score

**Identify:**
- Top 1-2 strong alignment points
- Top 1-2 gaps or concerns

**Note:** This is a *quick* analysis, not the full detailed analysis. Goal is triage and prioritization.

### Step 4: Create Bulk Analysis Summary

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

## File Management

After reviewing this analysis:

**For roles you'll pursue:**
```bash
# Move JD from staging to create full analysis
/analyze-job [URL or paste JD]
# This will create proper application folder
```

**For roles you're skipping:**
- Move staging files to `staging/archive/`
- Keep staging/ clean for next batch

**For roles you're unsure about:**
- Leave in staging/ for now
- Revisit after applying to top priorities
- Run `/analyze-job` if you decide to pursue

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
📊 Bulk processing complete!

📁 Generated: insights/bulk-analysis-YYYY-MM-DD.md

### Summary
- **Jobs analyzed:** X
- **High priority (8-10):** Y jobs 🔥
- **Medium priority (6-7):** Z jobs ⭐
- **Low/Skip (1-5):** W jobs

### Top 3 Recommendations
1. [Company A] - [Role] - Fit: X/10
2. [Company B] - [Role] - Fit: Y/10
3. [Company C] - [Role] - Fit: Z/10

### Next Steps
1. Review full analysis in insights/bulk-analysis-YYYY-MM-DD.md
2. Run `/analyze-job` for top priority roles
3. Clear processed files from staging/

⏱️ **Estimated application time for top 3:** [X-Y hours]
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
