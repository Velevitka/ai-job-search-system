# Documentation Hierarchy - What to Check When

**Created:** 2025-11-02
**Purpose:** Prevent confusion about current state by defining clear documentation hierarchy and trust levels

---

## Quick Reference: "What Should I Do Next?"

### For Current Status (What to Check First)

1. **Primary Source:** `STATUS.md` (root level) - ⭐⭐⭐ ALWAYS CURRENT
   - Updated automatically by `/generate-cv`, `/generate-cover-letter`, `/update-status`
   - Shows active applications, next recommended actions
   - Trust level: **HIGH** (single source of truth)

2. **Alternative:** Run `/status` command
   - Auto-generates current status by checking actual files
   - Verifies state from application folders + metrics dashboard
   - Trust level: **HIGH** (computed from real data)

3. **Detailed View:** Individual `applications/[company-role]/status.md` files
   - Granular tracking for each application
   - Updated when application status changes
   - Trust level: **HIGH** (application-specific detail)

### For Strategic Planning

- **Check:** `ROADMAP.md` - Long-term priorities and improvements
  - Updated bi-weekly based on progress
  - Trust level: **MEDIUM** (future-focused, not current state)
  - Use for: Understanding strategic priorities and planned enhancements

### For Performance Analysis

- **Check:** `insights/metrics-dashboard.md` - Aggregate statistics
  - Updated weekly by `/weekly-review`
  - Shows conversion rates, trends, patterns
  - Trust level: **HIGH** (aggregated data)
  - Use for: Understanding what's working and success patterns

### For Historical Context

- **Check:** `ARCHIVE-SUMMARY.md` - ⚠️ HISTORICAL SNAPSHOT ONLY
  - Created: 2025-10-31 (snapshot from that date)
  - **DO NOT USE for current state** - information may be outdated
  - Trust level: **LOW** (archived, not maintained)
  - Use for: Understanding what was analyzed and when

---

## File Purposes & Update Frequency

| File | Purpose | Update Frequency | Trust Level | Use For |
|------|---------|-----------------|-------------|---------|
| `STATUS.md` | Current state & next actions | Every application event | ⭐⭐⭐ PRIMARY | "What next?" |
| `/status` command | Auto-generated current status | On-demand | ⭐⭐⭐ HIGH | Verify state |
| `applications/*/status.md` | Individual app tracking | Per status change | ⭐⭐ HIGH | App details |
| `ROADMAP.md` | Strategic planning | Bi-weekly | ⭐ MEDIUM | Future plans |
| `metrics-dashboard.md` | Analytics & trends | Weekly | ⭐⭐ HIGH | Performance |
| `ARCHIVE-SUMMARY.md` | Historical snapshot | Never (archived) | ⚠️ LOW | History only |
| `career-preferences.md` | Role criteria | As needed | ⭐⭐ MEDIUM | Filtering |
| `insights/patterns.md` | Qualitative learnings | After outcomes | ⭐⭐ MEDIUM | Learning |

---

## For Claude Code: Decision Tree

When user asks **"what next?"** or **"what should I do?"**

### Step 1: Check Primary Source
```
1. Read STATUS.md (root level)
2. Look at "Next Recommended Actions" section
3. Check "Active Applications" for pending responses
4. Review "Recently Completed" for context
```

### Step 2: Verify Against Application Folders
```
1. List all folders in applications/ directory
2. For each folder, check for:
   - status.md file (current status)
   - PDF files (CV and cover letter completion)
3. Cross-reference with STATUS.md
4. Flag any inconsistencies
```

### Step 3: Consult Strategic Documents
```
1. Read ROADMAP.md for strategic priorities
2. Check career-preferences.md for filtering criteria
3. Review metrics-dashboard.md for performance context
```

### Step 4: Generate Recommendation
```
Based on:
- Fit scores (prioritize 9-10, then 8-9)
- Strategic priorities from ROADMAP.md
- Time since last application
- Open deadlines
- Long-term ROI (e.g., "Update Master CV" benefits all future apps)
```

### ⚠️ NEVER DO THIS:
- **DO NOT** trust ARCHIVE-SUMMARY.md for current state
- **DO NOT** assume todos in historical documents are current
- **DO NOT** rely on memory or old information
- **ALWAYS** verify state from actual files

---

## Common Scenarios

### Scenario 1: User asks "What should I work on next?"

**Correct approach:**
1. Read `STATUS.md` → Check "Next Recommended Actions"
2. Verify application folders for completion state
3. Provide specific recommendation with file paths

**Incorrect approach:**
❌ Reading ARCHIVE-SUMMARY.md and recommending already-completed applications
❌ Assuming todos from historical snapshots are current

---

### Scenario 2: User asks "Did I apply to [Company] yet?"

**Correct approach:**
1. Check `applications/[company]/status.md` for status field
2. Look for PDF files in application folder
3. Cross-reference with `metrics-dashboard.md`
4. Provide definitive answer with evidence

**Incorrect approach:**
❌ Guessing based on ARCHIVE-SUMMARY.md
❌ Assuming based on folder existence (folder exists ≠ applied)

---

### Scenario 3: User asks "How many applications have I submitted?"

**Correct approach:**
1. Read `metrics-dashboard.md` → "Applications Submitted" count
2. Verify by counting application folders with status="Applied"
3. Cross-check STATUS.md "Active Applications" table
4. Provide accurate count with breakdown

**Incorrect approach:**
❌ Using outdated count from historical documents
❌ Counting all folders (some may be analysis-only)

---

### Scenario 4: User asks "What are my strategic priorities?"

**Correct approach:**
1. Read `ROADMAP.md` → Current week priorities
2. Read `STATUS.md` → "Priority 2: Strategic Investment"
3. Combine strategic priorities with current state
4. Recommend based on both short-term and long-term value

**Correct example:**
✅ "Based on ROADMAP.md Priority 1, updating your Master CV with the AI product section will strengthen all future applications. This is a 1-2 hour investment that pays dividends across 10+ applications."

---

## Document Relationship Map

```
STATUS.md (Current State - Single Source of Truth)
    ↓
    ├── Updated by: /generate-cv
    ├── Updated by: /generate-cover-letter
    ├── Updated by: /update-status
    └── Verified by: /status command

applications/*/status.md (Individual Application Details)
    ↓
    └── Aggregated into: metrics-dashboard.md

metrics-dashboard.md (Performance Analytics)
    ↓
    └── Analyzed for: insights/patterns.md

ROADMAP.md (Strategic Planning)
    ↓
    └── Informs: STATUS.md "Priority" sections

ARCHIVE-SUMMARY.md (Historical Snapshot)
    ⚠️ DO NOT USE FOR CURRENT STATE
    └── Use only for: Understanding past analysis context
```

---

## Automated Updates

### Files That Auto-Update

**STATUS.md** - Auto-updated by:
- `/generate-cv [Company]` → Adds CV completion to "Recently Completed"
- `/generate-cover-letter [Company]` → Adds CL completion to "Recently Completed"
- `/update-status [Company] [status]` → Updates application status

**applications/*/status.md** - Auto-updated by:
- `/update-status [Company] [status]` → Adds status timeline entry

**metrics-dashboard.md** - Auto-updated by:
- `/weekly-review` → Refreshes all metrics from application folders

### Files That Require Manual Updates

- `ROADMAP.md` - Update bi-weekly or when priorities shift
- `career-preferences.md` - Update when criteria change
- `insights/patterns.md` - Update after learning from outcomes
- `ARCHIVE-SUMMARY.md` - Never update (frozen snapshot)

---

## Trust Level Definitions

### ⭐⭐⭐ PRIMARY (Always Trust)
- `STATUS.md` - Single source of truth
- `/status` command output - Computed from real files
- `applications/*/status.md` - Direct application state

**When to use:** For "what next?" and current state questions

### ⭐⭐ HIGH (Generally Trust, Verify If Critical)
- `metrics-dashboard.md` - Aggregated data (updated weekly)
- `career-preferences.md` - User-defined criteria

**When to use:** For performance analysis and filtering

### ⭐ MEDIUM (Context Only, Not Current State)
- `ROADMAP.md` - Future-focused planning
- `insights/patterns.md` - Qualitative learnings

**When to use:** For strategic planning, not current actions

### ⚠️ LOW (Historical Only - DO NOT USE for Current State)
- `ARCHIVE-SUMMARY.md` - Frozen snapshot from 2025-10-31
- Any file in `staging/archive/` - Archived job postings

**When to use:** Only for understanding historical context, NEVER for current state

---

## Preventing the "Stale Todos" Problem

### What Went Wrong

**Problem:** ARCHIVE-SUMMARY.md had a "Next Todos" section that became outdated after applications were completed. Claude Code recommended applying to Angi role that was already submitted on Oct 31.

**Root Cause:**
1. Historical snapshot document (ARCHIVE-SUMMARY.md) contained action items
2. No clear warning that document was outdated
3. No single source of truth for "what next?"
4. Claude Code checked historical docs before checking actual state

### The Fix

1. ✅ **Added warning header to ARCHIVE-SUMMARY.md** - Clear notice it's historical
2. ✅ **Created STATUS.md** - Single source of truth for current state
3. ✅ **Created `/status` command** - Auto-generates status from files
4. ✅ **Updated workflow commands** - Auto-update STATUS.md when CV/CL generated
5. ✅ **Created this guide** - Clear hierarchy for checking documents

### Prevention Rules

**For humans:**
- Check STATUS.md first for "what next?"
- Run `/status` if STATUS.md seems outdated
- Don't trust historical documents for current state

**For Claude Code:**
- **ALWAYS** check STATUS.md first when user asks "what next?"
- **ALWAYS** verify state from application folders + metrics dashboard
- **NEVER** use ARCHIVE-SUMMARY.md for current state
- **ALWAYS** flag inconsistencies between documents

---

## Verification Checklist for Claude Code

Before answering "what next?" questions, verify:

- [ ] Read `STATUS.md` (root level)
- [ ] Check `applications/` folders for PDFs
- [ ] Read individual `status.md` files
- [ ] Cross-reference `metrics-dashboard.md`
- [ ] Consult `ROADMAP.md` for strategic priorities
- [ ] **DO NOT** use `ARCHIVE-SUMMARY.md` for current state
- [ ] Flag any inconsistencies found

---

## Quick Commands

### Check Current Status
```bash
# Read STATUS.md
cat STATUS.md

# Or run auto-generated status
/status
```

### Verify Application State
```bash
# List all application folders
ls applications/

# Check specific application
cat applications/2025-10-Angi-DirectorProductDataPlatform/status.md

# Look for completed PDFs
ls applications/2025-10-Angi-*/ArturSwadzba_CV_Angi.pdf
ls applications/2025-10-Angi-*/ArturSwadzba_CoverLetter_Angi.pdf
```

### Update Status After Events
```bash
# After generating CV
/generate-cv Angi
# → Automatically updates STATUS.md

# After generating cover letter
/generate-cover-letter Angi
# → Automatically updates STATUS.md

# After submitting application
/update-status Angi applied "Submitted via company ATS"
# → Updates both applications/*/status.md and STATUS.md
```

---

## When Documents Conflict

**If STATUS.md and application folders disagree:**

1. **Trust the application folders** (source of truth)
2. Flag the inconsistency to user
3. Update STATUS.md to match reality
4. Investigate why STATUS.md wasn't auto-updated

**Example:**
```
⚠️ Inconsistency found:
- STATUS.md shows: Angi - "Not applied"
- Application folder shows: ArturSwadzba_CV_Angi.pdf + ArturSwadzba_CoverLetter_Angi.pdf exist
- status.md shows: "Applied" on 2025-10-31

Reality: Application was submitted on Oct 31.
Fixing: Updating STATUS.md to reflect correct state.
```

---

## Summary: The Golden Rule

**For "What's next?" questions:**

1. ✅ **Check STATUS.md first** (primary source)
2. ✅ **Verify with application folders** (source of truth)
3. ✅ **Consult ROADMAP.md** (strategic context)
4. ❌ **NEVER use ARCHIVE-SUMMARY.md** (historical only)

**For "Performance" questions:**
1. ✅ **Check metrics-dashboard.md** (aggregate stats)
2. ✅ **Check insights/patterns.md** (learnings)

**For "Strategic planning" questions:**
1. ✅ **Check ROADMAP.md** (priorities)
2. ✅ **Check career-preferences.md** (criteria)

---

---

## CRITICAL UPDATE: STATUS.md Sync Issue (Nov 5, 2025)

### What Happened

On November 5, 2025, discovered that **STATUS.md was NOT being auto-updated** as claimed. This contradicts the original design documented above.

**Discovery:**
- `/status` command was run
- Found STATUS.md showed incorrect state:
  - Redcare Pharmacy shown as "CV ready" but NOT applied
  - Reality: Redcare was applied on Nov 2
  - Missing: 4 withdrawn applications (Udemy, Gymshark, Booksy, Stax)
  - Missing: 1 rejection (Yelp, rejected Aug 2025)
  - Active count: 4 (should be 5)

### Root Cause

**The Problem:**
```
Individual status.md files ✅ → Updated correctly
         ↓
   STATUS.md ❌ → NOT auto-updated (manual only)
         ↓
   Out of sync → Stale information
```

**Why It Failed:**
1. Commands (`/generate-cv`, `/generate-cl`, `/update-status`) update individual `applications/*/status.md` files
2. Commands DO NOT update root `STATUS.md`
3. Root `STATUS.md` requires manual updates
4. Manual updates fall behind as applications accumulate
5. No validation that STATUS.md matches reality

### The Fix (Nov 5)

**Immediate Action Taken:**
- ✅ Manually read all 10 application folders
- ✅ Updated STATUS.md to match reality
- ✅ Added Redcare Pharmacy to active list
- ✅ Added 4 withdrawals section
- ✅ Added Yelp rejection
- ✅ Updated all stats and counts

**STATUS.md Now Accurate as of Nov 5, 2025**

### Long-Term Solution

**Recommendation: Make `/status` Command Regenerate STATUS.md**

**Proposed Workflow:**
```
User types: /status
      ↓
Scan: applications/*/status.md (all folders)
      ↓
Parse: Status, dates, fit scores, company, role
      ↓
Categorize: Active, Withdrawn, Rejected
      ↓
Calculate: Stats, averages, days waiting
      ↓
Generate: Fresh STATUS.md from scratch
      ↓
Display: Accurate real-time status
```

**Benefits:**
- ✅ Always accurate (never stale)
- ✅ Single source of truth (application folders)
- ✅ No manual sync required
- ✅ Disposable and regenerable

**Trade-off:**
- ❌ Overwrites any manual edits to STATUS.md
- **Solution:** STATUS.md becomes a VIEW (derived), not a STORE (source of truth)

### Prevention Strategy

**DO:**
- ✅ Update individual `applications/*/status.md` immediately when state changes
- ✅ Run `/status` to regenerate STATUS.md from folders
- ✅ Trust application folders as source of truth
- ✅ Treat STATUS.md as derived/disposable

**DON'T:**
- ❌ Manually edit STATUS.md (it will be regenerated)
- ❌ Trust STATUS.md if it looks stale
- ❌ Duplicate information between files

### Updated Architecture

**Source of Truth (Never Derived):**
```
applications/*/status.md → Updated immediately by commands/manual
```

**Derived Views (Always Regenerated):**
```
STATUS.md → Generated by /status command
metrics-dashboard.md → Generated by /weekly-review
weekly-review-*.md → Generated by /weekly-review
```

**Manual Strategic Documents:**
```
ROADMAP.md → Updated bi-weekly
career-preferences.md → Updated as needed
insights/patterns.md → Updated after learnings
```

### Trust Level Update

**ORIGINAL CLAIM (Nov 2):**
> `STATUS.md` - ⭐⭐⭐ ALWAYS CURRENT
> Auto-updated by: /generate-cv, /generate-cover-letter, /update-status

**REALITY (Nov 5):**
> `STATUS.md` - ⚠️ MANUALLY MAINTAINED (prone to staleness)
> NOT auto-updated - requires manual sync or `/status` regeneration

**NEW DESIGN (Recommended):**
> `STATUS.md` - ⭐⭐⭐ REGENERATED ON-DEMAND
> Auto-generated by: /status command (reads all application folders)
> Treat as: Disposable view, not source of truth

### File Ownership (Updated)

| File | Type | Updated By | Trust |
|------|------|------------|-------|
| `applications/*/status.md` | **SOURCE OF TRUTH** | Commands + Manual | ⭐⭐⭐ |
| `STATUS.md` | **DERIVED VIEW** | `/status` command | ⭐⭐⭐ (if recently regenerated) |
| `metrics-dashboard.md` | **DERIVED VIEW** | `/weekly-review` | ⭐⭐ (weekly) |
| `ROADMAP.md` | **MANUAL** | User edits | ⭐ (strategic only) |
| `ARCHIVE-SUMMARY.md` | **FROZEN** | Never | ⚠️ (historical only) |

### Validation Checklist

When running `/status`, the command should:
- [ ] Scan all folders in `applications/`
- [ ] Read each `status.md` file
- [ ] Parse: status, dates, fit, company, role
- [ ] Categorize: active, withdrawn, rejected
- [ ] Calculate: stats, averages, days waiting
- [ ] Validate: all folders have entries, no orphans
- [ ] Generate: Fresh STATUS.md
- [ ] Display: Accurate current state

### Action Items

**Done (Nov 5):**
- [x] Identified root cause
- [x] Manually synced STATUS.md
- [x] Documented issue and solution

**To Do (This Week):**
- [ ] Enhance `/status` command to regenerate STATUS.md
- [ ] Add validation logic
- [ ] Add timestamps to generated files
- [ ] Test regeneration workflow

**Future:**
- [ ] Apply same pattern to metrics-dashboard.md
- [ ] Create `/sync-all` command
- [ ] Add automated tests for consistency

---

**Last Updated:** 2025-11-05
**Critical Issue:** STATUS.md sync problem identified and fixed
**Next Action:** Implement auto-regeneration in `/status` command
**Maintained By:** Automated workflows + manual strategic updates
**Review Frequency:** Update this guide if new documentation patterns emerge
