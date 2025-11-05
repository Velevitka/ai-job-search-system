# Complete Job Search Workflow Guide

**Last Updated:** 2025-11-05
**System Version:** Pipeline v2 (Auto-move workflow)

---

## Overview

This document describes the complete end-to-end workflow for the AI-powered job search system, from job discovery to offer acceptance.

**System Philosophy:**
- **Persistent priority queue** - No lost opportunities across batches
- **Career preferences weighting** - Travel > AdTech > FinTech prioritization
- **Visual pipeline** - Clear folder-based workflow stages
- **Automation-first** - Minimize manual file management

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Complete Lifecycle](#complete-lifecycle)
3. [Stage 1: Discovery](#stage-1-discovery)
4. [Stage 2: Bulk Analysis](#stage-2-bulk-analysis)
5. [Stage 3: Shortlisting](#stage-3-shortlisting)
6. [Stage 4: Application Creation](#stage-4-application-creation)
7. [Stage 5: Submission & Tracking](#stage-5-submission--tracking)
8. [Special Workflows](#special-workflows)
9. [Commands Reference](#commands-reference)
10. [Troubleshooting](#troubleshooting)

---

## Quick Start

**New user? Start here:**

```bash
# 1. Discover jobs (automated)
python scripts/job_discovery.py --keywords "Director Product" --location "London"

# 2. Analyze batch
/bulk-process

# 3. Review opportunities
cat staging/2-shortlist/README.md

# 4. Start application
/analyze-job loveholidays

# 5. Generate materials
/generate-cv loveholidays
/generate-cl loveholidays

# 6. Submit and track
/update-status loveholidays applied "Applied Nov 5"
```

---

## Complete Lifecycle

```
┌────────────────────────────────────────────────────────────┐
│ STAGE 1: DISCOVERY                                         │
│                                                            │
│ Automated Scripts  →  staging/0-discovery/automated/      │
│ Bookmarklet Saves  →  staging/0-discovery/manual/         │
│                                                            │
│ Duration: Continuous (daily/weekly)                       │
└────────────────────────────────────────────────────────────┘
                          ↓
                  /bulk-process
                          ↓
┌────────────────────────────────────────────────────────────┐
│ STAGE 2: BULK ANALYSIS                                     │
│                                                            │
│ 0-discovery/ → 1-triage/ → Analyze & Score                │
│                                                            │
│ Apply career preferences weighting:                       │
│ - Travel: +2 points                                       │
│ - AdTech: +1.5 points                                     │
│ - Director level: +2 points                               │
│                                                            │
│ Output: insights/bulk-analysis-YYYY-MM-DD.md              │
│ Duration: 5-10 minutes per batch                          │
└────────────────────────────────────────────────────────────┘
                          ↓
            Auto-categorize by weighted fit
                          ↓
┌────────────────────────────────────────────────────────────┐
│ STAGE 3: SHORTLISTING                                      │
│                                                            │
│ Fit 9-11/10  →  2-shortlist/high/                        │
│ Fit 7-8.5/10 →  2-shortlist/medium/                      │
│ Fit <7       →  archive/low-fit/                         │
│ Filtered     →  archive/filtered/                        │
│                                                            │
│ Human reviews shortlist, decides which to pursue          │
│ Duration: 30-60 min review, then ongoing                  │
└────────────────────────────────────────────────────────────┘
                          ↓
                  /analyze-job
                          ↓
┌────────────────────────────────────────────────────────────┐
│ STAGE 4: APPLICATION CREATION                              │
│                                                            │
│ /analyze-job → Auto-moves to 3-applying/                 │
│              → Creates applications/YYYY-MM-Company/      │
│                                                            │
│ /generate-cv → Tailored CV (2 pages max)                 │
│ /generate-cl → Tailored cover letter (1 page)            │
│                                                            │
│ Review → Iterate → Finalize                               │
│ Duration: 2-4 hours per application                       │
└────────────────────────────────────────────────────────────┘
                          ↓
          /update-status applied
                          ↓
┌────────────────────────────────────────────────────────────┐
│ STAGE 5: SUBMISSION & TRACKING                             │
│                                                            │
│ /update-status applied → Auto-archives from 3-applying/  │
│                        → Tracks in applications/ folder   │
│                                                            │
│ Status progression:                                       │
│ applied → interview → final-round → offer → accepted     │
│                                                            │
│ Duration: Days to weeks (company response time)           │
└────────────────────────────────────────────────────────────┘
```

---

## Stage 1: Discovery

**Goal:** Find relevant job opportunities

### Automated Discovery

**LinkedIn Job Search:**
```bash
python scripts/job_discovery.py \
    --keywords "Director Product Data Platform" \
    --location "London, United Kingdom" \
    --date past_week
```

**Output:**
- Jobs saved to: `staging/0-discovery/automated/YYYY-MM-DD-batch/`
- Each job in separate folder with `job-description.md`

**Frequency:** Run weekly or as needed

### Manual Discovery (Bookmarklet)

**When you find interesting job:**
1. Click bookmarklet on LinkedIn/company site
2. Job saved to: `staging/0-discovery/manual/`
3. Ready for next bulk-process

**Use case:** Jobs that automated search might miss

### Discovery Sources

**Primary:**
- LinkedIn Jobs
- Company career pages (via bookmarklet)

**Secondary (future):**
- Indeed, Glassdoor APIs
- Recruiter emails → manual save

---

## Stage 2: Bulk Analysis

**Goal:** Score and prioritize all discovered jobs

### Running Bulk Analysis

```bash
/bulk-process
```

**System workflow:**

**1. Scan Discovery**
```
Scans: staging/0-discovery/automated/**/*
       staging/0-discovery/manual/*

Finds: All .mhtml, .md, .pdf job description files
```

**2. Move to Triage**
```
Moves all jobs to: staging/1-triage/
Temporary holding while analysis runs
```

**3. Analyze & Score**

For each job:
- Extract company, role, requirements
- Match against master CV experience
- Calculate base fit score (0-10)
- Apply career preferences weighting
- Identify gaps and positioning strategy

**Base fit score calculation:**
```python
base_fit = (
    keyword_match_score +      # 0-5 pts
    seniority_match_score +     # 0-2 pts
    location_bonus +            # 0-2 pts
    industry_bonus              # 0-1 pt
) # Max 10 pts

weighted_fit = base_fit + career_bonus

career_bonus = {
    'travel': +2,      # Travel industry (#1 preference)
    'adtech': +1.5,    # AdTech (#2 preference)
    'director': +2,    # Director/Head level
    'fintech': +1      # FinTech experience overlap
}
```

**4. Auto-Categorize**
```
Weighted Fit 9-11/10  → staging/2-shortlist/high/
Weighted Fit 7-8.5/10 → staging/2-shortlist/medium/
Weighted Fit <7       → staging/archive/low-fit/
Pre-filtered          → staging/archive/filtered/
```

**5. Generate Report**
```
Creates: insights/bulk-analysis-YYYY-MM-DD.md
Updates: staging/2-shortlist/README.md
Updates: MASTER-SHORTLIST.md (root)
```

### Pre-Filtering Rules

**Auto-filtered (not analyzed):**
- ❌ Product Owner level (too junior)
- ❌ Crypto/Web3 companies (career preferences)
- ❌ US-only locations (visa constraints)
- ❌ Pure engineering roles (not PM)
- ❌ Duplicate postings

### Output

**Bulk analysis report includes:**
- Priority table (ranked by weighted fit)
- Top 10 opportunities
- Detailed breakdown for each job (fit score, why high/low, gaps, positioning)
- Summary insights (patterns, common gaps, recommendations)
- Next actions (which to apply to this week)

**Example:**
```markdown
## Top 10 Opportunities

1. Expedia Group - Director PM Growth Marketing (11/10)
2. loveholidays - Head of Product Selling (10.5/10)
3. Hopper - Senior PM Supply (10/10)
4. Moloco - Group PM Dynamic Product Ads (10/10)
...
```

---

## Stage 3: Shortlisting

**Goal:** Review opportunities and decide which to pursue

### Review High Priority

**Check shortlist:**
```bash
cat staging/2-shortlist/README.md
# or
ls staging/2-shortlist/high/
```

**Current high priority (16 jobs):**
- 8 Travel roles
- 3 AdTech roles
- 5 High-tier other (AmEx, Delivery Hero, etc.)

### Decision Criteria

**Must-haves (all required):**
- ✅ Director/Head level
- ✅ Fit score 7+
- ✅ Location acceptable (UK, EU, or strategic relocation)
- ✅ Not auto-filtered

**Nice-to-haves (3+ preferred):**
- ✅ Travel/hospitality industry
- ✅ AdTech/MarTech focus
- ✅ Hybrid/remote-friendly
- ✅ Equity upside
- ✅ Team leadership opportunity

**Apply if:**
- All must-haves + 3+ nice-to-haves = High priority (apply this week)
- All must-haves + 2 nice-to-haves = Medium priority (apply if capacity)
- Missing must-have = Skip

### Special: Insider Intel

**If you have network contacts:**

1. Move job to: `staging/2-shortlist/pending-insider-intel/`
2. Reach out to contacts for hiring manager info
3. When feedback received:
   - Good intel → Move to `high/` and apply
   - Bad intel (hiring freeze, etc.) → Move to `archive/withdrawn/`

**Example:** Expedia Group (current state)
- Location: `staging/2-shortlist/pending-insider-intel/`
- Status: Awaiting network feedback on hiring manager and location
- Action: Don't apply until feedback received

---

## Stage 4: Application Creation

**Goal:** Generate tailored CV and cover letter

### Step 1: Start Application

**Command:**
```bash
/analyze-job loveholidays
```

**System automatically:**
1. Finds `loveholidays.mhtml` in `staging/2-shortlist/high/`
2. **Moves** it to `staging/3-applying/loveholidays.mhtml`
3. Creates `applications/2025-11-loveholidays-HeadofProduct/`
4. Generates detailed analysis:
   - Fit score with justification
   - Key requirements match
   - Gap analysis
   - Positioning strategy
   - Hallucination risk warnings
5. Creates `status.md` (status: "drafting")

**Output example:**
```
applications/2025-11-loveholidays-HeadofProduct/
├── analysis.md            # Full job analysis
├── job-description.md     # Original JD
└── status.md             # Tracking
```

**Job location:**
```
staging/3-applying/loveholidays.mhtml  ← MOVED HERE
```

### Step 2: Generate CV

**Command:**
```bash
/generate-cv loveholidays
```

**System workflow:**

1. **Read Analysis**
   - Load `analysis.md` for positioning strategy
   - Identify key requirements to emphasize
   - Note gaps to address

2. **Create Tailoring Plan**
   - Generates `cv-tailoring-plan.md`
   - Lists modifications to master CV
   - Validates against real experience (hallucination check)
   - Gets human approval

3. **Generate CV**
   - Creates `ArturSwadzba_CV_loveholidays.md`
   - Applies Eisvogel template
   - Generates PDF via Pandoc + XeLaTeX

4. **Validate**
   - Checks: Exactly 2 pages, A4 size, proper formatting
   - If fails: Auto-adjusts margins/font before removing content

5. **Human Review**
   - Opens PDF for review
   - Prompts: "Approve? Edit? Regenerate?"

**Formatting hierarchy (critical):**
```
If CV > 2 pages:
1. FIRST: Adjust margins (20mm → 18mm)
2. SECOND: Adjust font size (11pt → 10pt)
3. THIRD: Adjust line spacing
4. LAST RESORT: Remove least relevant content
```

**Output:**
```
applications/2025-11-loveholidays-HeadofProduct/
├── cv-tailoring-plan.md
├── ArturSwadzba_CV_loveholidays.md
└── ArturSwadzba_CV_loveholidays.pdf  ✅ Ready to submit
```

### Step 3: Generate Cover Letter

**Command:**
```bash
/generate-cl loveholidays
```

**System workflow:**

1. **Research Company**
   - WebSearch for recent news, product launches, funding
   - Creates `company-research-brief.md`

2. **Draft Cover Letter**
   - Generates 3 opening hook options
   - Creates `cover-letter-draft.md`
   - AI self-critique for improvements
   - Gets human approval

3. **Generate Final**
   - Creates `ArturSwadzba_CoverLetter_loveholidays.md`
   - Applies Eisvogel template
   - Generates PDF

4. **Validate**
   - Checks: Exactly 1 page, 300-400 words, proper formatting
   - If fails: Condense before removing content

**If form field character limit:**
```bash
# System detects character limit issue
# Automatically creates condensed version
# File: cover-letter-condensed-form-version.txt
```

**Output:**
```
applications/2025-11-loveholidays-HeadofProduct/
├── company-research-brief.md
├── cover-letter-draft.md
├── ArturSwadzba_CoverLetter_loveholidays.md
└── ArturSwadzba_CoverLetter_loveholidays.pdf  ✅ Ready to submit
```

### Step 4: Review & Iterate

**Human review checklist:**
- [ ] CV emphasizes right experience?
- [ ] No hallucinations (all claims accurate)?
- [ ] Formatting looks professional?
- [ ] Cover letter addresses domain gaps?
- [ ] Company research is current?
- [ ] Both fit on required pages?

**If changes needed:**
```bash
# Edit markdown source, then:
/generate-cv loveholidays --regenerate
/generate-cl loveholidays --regenerate
```

**Job stays in:**
```
staging/3-applying/loveholidays.mhtml  ← Still here while iterating
```

---

## Stage 5: Submission & Tracking

### Submit Application

**After submitting via company website:**

```bash
/update-status loveholidays applied "Applied via careers page on Nov 6, 2025. Application ID: ABC123"
```

**System automatically:**
1. Updates `applications/.../status.md`:
   - Status: "applied"
   - Applied date: "2025-11-06"
   - Notes: Application details
2. **Moves** `staging/3-applying/loveholidays.mhtml` → `staging/archive/low-fit/`
3. Updates root `STATUS.md` (active applications count)

**Result:**
```
staging/3-applying/  ← loveholidays GONE
staging/archive/low-fit/loveholidays.mhtml  ← Archived for reference

applications/2025-11-loveholidays-HeadofProduct/
├── All CV/CL files
└── status.md (status: "applied", applied_on: "2025-11-06")
```

### Track Interview Process

**As you progress through stages:**

```bash
# Recruiter contact
/update-status loveholidays recruiter-screen "Phone screen scheduled Nov 12 at 2pm GMT with Sarah (Talent team)"

# After phone screen
/update-status loveholidays interview "Moved to hiring manager round. Interview Nov 15 with John (Head of Product)"

# After hiring manager
/update-status loveholidays interview-complete "Went well! Discussed team structure, roadmap. Waiting on next steps."

# Final round
/update-status loveholidays final-round "Final round Nov 20: Panel with CPO, CTO, and CEO. Prepared STAR stories."

# Offer
/update-status loveholidays offer "Offer received: £125k base + 0.5% equity + £10k sign-on. Negotiating equity."

# Accept
/update-status loveholidays accepted "Accepted offer: £130k + 0.7% equity. Start date: Jan 15, 2026. Notice given at current job."
```

**Job never returns to staging/** - tracked in `applications/` only

### Monitor All Applications

**Check overall status:**
```bash
/status
```

**Output:**
```
# Current Status - Job Search

## Active Applications (6)
- loveholidays: interview (next: Nov 15)
- Hopper: applied (0 days, awaiting response)
- Moloco: recruiter-screen (scheduled Nov 12)
- American Express: applied (3 days)
- Expedia: applied (1 day)
- Delivery Hero: applied (5 days)

## Success Rate
- Applications: 6
- Interviews: 2 (33%)
- Offers: 0
```

---

## Special Workflows

### Withdrawing After Analysis

**Use case:** Analyzed job but decided not to apply

```bash
/withdraw loveholidays "After analysis, realized role is too junior. JD says 'Senior PM' but requirements suggest IC role."
```

**System:**
1. Moves `staging/3-applying/loveholidays.mhtml` → `staging/archive/withdrawn/`
2. Updates `applications/.../status.md` (status: "withdrawn", reason logged)
3. Preserves analysis for future reference

### Rejected Applications

**When you receive rejection:**

```bash
/update-status loveholidays rejected "Rejected on Nov 10. Feedback: Looking for more travel industry experience. Applied Aug 2025, 30 days to response."
```

**System:**
- Updates status.md with rejection date and reason
- Moves to STATUS.md rejected applications section
- Tracks time-to-response for analytics

### Bulk Applying (Travel Roles)

**Apply to multiple similar roles:**

```bash
# Day 1: Travel roles batch
/analyze-job loveholidays
/analyze-job hopper
/analyze-job holiday-extras

# Day 2: Generate all CVs
/generate-cv loveholidays
/generate-cv hopper
/generate-cv holiday-extras

# Day 3: Generate all CLs
/generate-cl loveholidays
/generate-cl hopper
/generate-cl holiday-extras

# Day 4-5: Review and submit all
```

**Benefit:** Similar roles = similar tailoring = faster iteration

---

## Commands Reference

### Core Workflow

```bash
# Discovery
python scripts/job_discovery.py --keywords "Director Product" --location "London"

# Bulk Analysis
/bulk-process

# Application Creation
/analyze-job [company-name]
/generate-cv [company-name]
/generate-cl [company-name]

# Submission & Tracking
/update-status [company] applied "notes"
/update-status [company] interview "notes"
/update-status [company] offer "notes"
/update-status [company] accepted "notes"
```

### Utility

```bash
# Withdraw application
/withdraw [company] "reason"

# See active work
/active-applications

# Overall status
/status

# Weekly review
/weekly-review
```

### Regeneration

```bash
# Regenerate CV with edits
/generate-cv [company] --regenerate

# Regenerate CL with edits
/generate-cl [company] --regenerate
```

---

## Troubleshooting

### Job Not Found in Shortlist

**Error:** `/analyze-job loveholidays` → "Job not found"

**Fix:**
```bash
# Check location:
ls staging/2-shortlist/high/ | grep loveholidays

# If in different folder:
mv staging/2-shortlist/medium/loveholidays.mhtml staging/2-shortlist/high/

# Then retry:
/analyze-job loveholidays
```

### CV > 2 Pages

**System should auto-fix, but if manual fix needed:**

1. Check margins first:
```yaml
---
geometry: margin=18mm  # Try this
---
```

2. Check font size second:
```yaml
---
geometry: margin=18mm
fontsize: 10pt  # Reduce from 11pt
---
```

3. Only then remove content

### Application Folder Already Exists

**Error:** `/analyze-job loveholidays` → "Folder already exists"

**Likely:** Previous attempt created folder but wasn't completed

**Fix:**
```bash
# Check status:
cat applications/2025-11-loveholidays-HeadofProduct/status.md

# If status is "drafting" or "in_progress":
# Delete folder and restart:
rm -rf applications/2025-11-loveholidays-HeadofProduct/
/analyze-job loveholidays

# If status is "applied" or later:
# This is already tracked, don't reanalyze
```

### Bookmarklet Not Saving

**Issue:** Bookmarklet click does nothing

**Fix:**
1. Check bookmarklet code is current
2. Ensure `staging/0-discovery/manual/` folder exists
3. Try manual save: Copy JD → Create `.md` file in `0-discovery/manual/`

---

## Best Practices

### Weekly Rhythm

**Sunday:**
- Run `python scripts/job_discovery.py` for new jobs
- Run `/bulk-process` to analyze
- Review `staging/2-shortlist/README.md`
- Plan week's applications (target: 3-5)

**Monday-Friday:**
- Focus on high-priority applications
- 1-2 applications per day max (quality > quantity)
- Track responses daily

**Saturday:**
- Run `/weekly-review`
- Analyze what's working (which roles getting responses)
- Adjust search keywords if needed

### Application Quality

**Time per application:**
- Analysis: 20-30 min
- CV tailoring: 1-2 hours
- CL drafting: 1-2 hours
- Review & iteration: 30-60 min
- **Total: 3-5 hours per quality application**

**Don't rush:**
- 3 high-quality applications > 10 generic applications
- Tailoring matters for Director-level roles
- Cover letters differentiate at this level

### Career Preferences Alignment

**Always prioritize:**
1. Travel industry (#1 preference)
2. AdTech/MarTech (#2 preference)
3. Director/Head level (target seniority)

**Don't waste time on:**
- Crypto/Web3 (preference: avoid)
- Product Owner level (too junior)
- Pure B2B SaaS without consumer element

---

## System Metrics

**Track these for improvement:**

**Funnel metrics:**
- Discovery → Shortlist conversion (target: 20-30%)
- Shortlist → Apply conversion (target: 30-40%)
- Apply → Interview conversion (target: 20-30%)
- Interview → Offer conversion (target: 30-50%)

**Efficiency metrics:**
- Time per application (target: <4 hours)
- Applications per week (target: 3-5)
- Response rate by industry (track: travel vs fintech vs adtech)

**Quality metrics:**
- Fit score accuracy (are 9/10 fit roles actually good?)
- Career preferences weighting (are travel roles surfacing first?)
- No lost opportunities (check: any gold jobs buried?)

---

## Version History

**v2.0 (2025-11-05)** - Current
- Implemented Option 2: Auto-move workflow
- Added persistent priority queue
- Career preferences weighting
- Staging folder reorganization (Pipeline structure)

**v1.0 (2025-10-30)**
- Initial system with tier-based folders
- Basic CV/CL generation
- Manual file management

---

**For developers/contributors:** See `.claude/project-guide.md` for technical implementation details
**For system architecture:** See `docs/architecture/ARCHITECTURE.md`
**For command implementation:** See `.claude/commands/` folder
