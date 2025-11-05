# Staging Folder Redesign - 3 Approaches

**Current Date:** 2025-11-05
**Current State:** 7 subfolders, 86 files, multiple organizational schemes overlapping

---

## Current Problems

**Folder chaos:**
- `tier1-apply-now/`, `tier2-research/`, `tier3-maybe/` (priority-based, but unclear workflow)
- `2025-11-05-discovery-batch/`, `2025-11-05-processed-batch/` (date-based batches)
- `archive/` with date-based subfolders (`2025-10-analyzed/`, `2025-11-bulk-analyzed/`)
- `manual-saves/` (bookmarklet saves, but then what?)

**Workflow issues:**
1. **No clear path:** Manual saves → Where do they go after saving?
2. **Multiple systems:** Tier-based AND date-based AND archive
3. **Unclear lifecycle:** When does a job move from staging → applications folder?
4. **Archive confusion:** Archive has dated subfolders - should it just be flat?

---

## Design Principles (All Approaches)

**Must support these workflows:**
1. **Automated discovery** → Scripts save to staging
2. **Manual saves** → Bookmarklet saves interesting jobs
3. **Bulk analysis** → `/bulk-process` analyzes batch, scores, and prioritizes
4. **Decision making** → Human reviews analysis, decides apply/skip
5. **Application creation** → `/analyze-job` moves to applications folder
6. **Archival** → Jobs not pursued go to "folder of no return"

**Key constraints:**
- `manual-saves/` must exist (bookmarklet target)
- `archive/` is "folder of no return" (jobs we won't pursue)
- System must be simple enough to maintain
- Must work with existing automation scripts

---

## Approach 1: Simple Status-Based (Immediate Fix)

**Philosophy:** Minimize folders, clear next actions, status-driven

### Folder Structure

```
staging/
├── inbox/                    # NEW - All new jobs land here
│   ├── manual-saves/        # Bookmarklet target (subfolder of inbox)
│   └── discovery-YYYY-MM-DD/  # Script discoveries (dated folders)
│
├── to-review/               # NEW - Ready for bulk analysis
│   └── [job files to analyze]
│
├── to-apply/                # NEW - Decided to apply (Fit 7+)
│   └── [jobs awaiting /analyze-job]
│
└── archive/                 # Folder of no return (flat, no subfolders)
    └── [all rejected/skipped jobs]
```

### Workflow

**1. Job Discovery:**
```bash
# Automated script:
scripts/job_discovery.py → staging/inbox/discovery-2025-11-05/

# Manual bookmarklet:
Bookmarklet → staging/inbox/manual-saves/
```

**2. Bulk Analysis:**
```bash
# Human runs:
/bulk-process

# System:
- Scans staging/inbox/**/*
- Analyzes all jobs
- Creates insights/bulk-analysis-YYYY-MM-DD.md
- Prompts: "Move analyzed jobs to to-review/? (yes/no)"
```

**3. Human Review:**
```
Human reads: insights/bulk-analysis-2025-11-05.md

Decision for each job:
- Fit 7-10 → Move to staging/to-apply/
- Fit 1-6 → Move to staging/archive/
```

**4. Application Creation:**
```bash
# For each job in to-apply/:
/analyze-job [company] [paste JD]

# System:
- Creates applications/YYYY-MM-CompanyName-Role/
- Moves job file from staging/to-apply/ → archive/
  (because it's now in applications/ folder)
```

### Migration Plan (Immediate)

```bash
# 1. Create new folders
mkdir staging/inbox
mkdir staging/to-review
mkdir staging/to-apply

# 2. Move existing content
mv staging/manual-saves staging/inbox/manual-saves
mv staging/2025-11-05-discovery-batch staging/inbox/discovery-2025-11-05
mv staging/2025-11-05-processed-batch staging/inbox/discovery-2025-11-05-processed

# 3. Consolidate tiers
mv staging/tier1-apply-now/* staging/to-apply/
mv staging/tier2-research/* staging/to-review/
mv staging/tier3-maybe/* staging/archive/

# 4. Flatten archive (remove date-based subfolders)
mv staging/archive/*/* staging/archive/
rmdir staging/archive/2025-10-analyzed
rmdir staging/archive/2025-11-bulk-analyzed

# 5. Remove old tier folders
rmdir staging/tier1-apply-now
rmdir staging/tier2-research
rmdir staging/tier3-maybe
```

### Pros
- ✅ Simple, clear next actions
- ✅ Easy to understand workflow
- ✅ Minimal folders (4 total)
- ✅ Works with existing scripts (just change target path)
- ✅ Quick migration (30 min)

### Cons
- ⚠️ Loses date-based organization (can't see "Week 1 batch" vs "Week 2 batch")
- ⚠️ Manual moving of files between folders (no automation)
- ⚠️ "to-apply" vs "to-review" distinction may be unclear

---

## Approach 2: Time-Based Batches (Sprint-Like)

**Philosophy:** Organize by discovery week, support sprint-based job search

### Folder Structure

```
staging/
├── manual-saves/            # Bookmarklet target (always here)
│   └── [unbatched manual saves]
│
├── batches/                 # Weekly job search batches
│   ├── 2025-W45/           # Week 45 (Nov 4-10)
│   │   ├── jobs/           # Job descriptions
│   │   ├── analysis.md     # Bulk analysis results
│   │   └── README.md       # Batch summary (3 applied, 2 researching, 10 archived)
│   │
│   ├── 2025-W46/           # Week 46 (Nov 11-17)
│   └── current/            # Symlink to current week
│
└── archive/                 # Folder of no return (flat)
    └── [all skipped jobs, organized by batch if needed]
```

### Workflow

**1. Weekly Batch Creation:**
```bash
# Monday morning:
/new-batch

# System:
- Creates staging/batches/2025-W45/jobs/
- Moves staging/manual-saves/* → staging/batches/2025-W45/jobs/
- Creates symlink: staging/batches/current → 2025-W45
```

**2. Discovery During Week:**
```bash
# Scripts automatically save to:
staging/batches/current/jobs/

# Manual bookmarklet saves to:
staging/manual-saves/ (then batch in next /new-batch)
```

**3. End-of-Week Analysis:**
```bash
# Friday or Sunday:
/bulk-process

# System:
- Scans staging/batches/current/jobs/
- Creates staging/batches/current/analysis.md
- Generates staging/batches/current/README.md
```

**4. Application Creation:**
```bash
# For high-priority jobs:
/analyze-job [company]

# System:
- Creates applications/YYYY-MM-CompanyName/
- Adds note to batches/2025-W45/README.md: "Applied: CompanyName"
- Archives job file
```

### Example Batch README.md

```markdown
# Job Search Batch - Week 45 (Nov 4-10, 2025)

**Jobs discovered:** 15
**Analyzed:** 12
**Auto-filtered:** 3 (too junior)

**Outcomes:**
- ✅ Applied: Redpin (8.5/10), Mastercard (7.5/10)
- 🔍 Researching: Multiverse (7/10)
- 📊 Awaiting response: NBCUniversal, Storio
- ❌ Archived: 10 jobs (low fit)

**Time invested:** 8 hours
**Applications submitted:** 2
**Success rate:** TBD (tracking in applications/)
```

### Migration Plan

```bash
# 1. Create batch structure
mkdir -p staging/batches/2025-W45/jobs
mkdir staging/batches

# 2. Move current active jobs to current week batch
mv staging/tier1-apply-now/* staging/batches/2025-W45/jobs/
mv staging/tier2-research/* staging/batches/2025-W45/jobs/
mv staging/2025-11-05-discovery-batch/* staging/batches/2025-W45/jobs/

# 3. Archive old content
mv staging/tier3-maybe/* staging/archive/
mv staging/2025-11-05-processed-batch/* staging/archive/

# 4. Keep manual-saves at root
# (no change - manual-saves stays where it is)

# 5. Create symlink
ln -s 2025-W45 staging/batches/current

# 6. Remove old folders
rmdir staging/tier1-apply-now staging/tier2-research staging/tier3-maybe
rmdir staging/2025-11-05-discovery-batch staging/2025-11-05-processed-batch
```

### Pros
- ✅ Clear time-based organization (see progress week-by-week)
- ✅ Batch README.md tracks outcomes (applied, researching, archived)
- ✅ Supports sprint-based job search (6-day cycles align with weekly batches)
- ✅ Historical tracking (can review "What did I do in Week 45?")
- ✅ Easy to calculate weekly stats (time invested, applications, success rate)

### Cons
- ⚠️ More folders over time (one per week)
- ⚠️ Requires weekly `/new-batch` command to create new week
- ⚠️ Symlink complexity (`current/`) may be unfamiliar
- ⚠️ Mixing jobs from different dates in same batch may feel odd

---

## Approach 3: Priority Pipeline (Strategic Workflow)

**Philosophy:** Funnel-based, mirrors application pipeline stages

### Folder Structure

```
staging/
├── 0-discovery/             # Raw incoming jobs (unprocessed)
│   ├── automated/          # From scripts
│   └── manual/             # From bookmarklet (was manual-saves/)
│
├── 1-triage/               # Being analyzed (bulk-process working here)
│   └── [jobs currently being scored]
│
├── 2-shortlist/            # High-priority (Fit 7-10)
│   ├── high/              # Fit 8-10 - Apply this week
│   ├── medium/            # Fit 7-7.9 - Apply if capacity
│   └── README.md          # Current shortlist summary
│
├── 3-applying/             # In process of application creation
│   └── [jobs where /analyze-job started but not submitted]
│
└── archive/                # Folder of no return
    ├── low-fit/           # Fit <7 (analyzed but not pursuing)
    ├── filtered/          # Pre-filtered (too junior, wrong type)
    └── withdrawn/         # Started analysis but withdrew
```

### Workflow

**1. Job Discovery:**
```bash
# Scripts:
job_discovery.py → staging/0-discovery/automated/

# Bookmarklet:
Saves to → staging/0-discovery/manual/
```

**2. Bulk Analysis:**
```bash
/bulk-process

# System:
1. Scans 0-discovery/**/*
2. Moves files to 1-triage/
3. Analyzes all jobs
4. Auto-categorizes by fit score:
   - Fit 8-10 → 2-shortlist/high/
   - Fit 7-7.9 → 2-shortlist/medium/
   - Fit <7 → archive/low-fit/
5. Creates 2-shortlist/README.md (current opportunities)
```

**3. Application Creation:**
```bash
/analyze-job Redpin

# System:
1. Moves Redpin from 2-shortlist/high/ → 3-applying/
2. Creates applications/2025-11-Redpin-CorePlatform/
3. Generates CV, CL
4. When /update-status applied → moves from 3-applying/ → archive/low-fit/
   (because it's now tracked in applications/)
```

### Example Shortlist README.md

```markdown
# Current Shortlist

**Last Updated:** 2025-11-05
**High Priority:** 3 jobs (Apply this week)
**Medium Priority:** 5 jobs (Apply if capacity)

---

## 🔥 High Priority (Fit 8-10)

### 1. Redpin - Senior Product Director, Core Platform (Fit: 8.5/10)
- **Status:** In shortlist
- **Deadline:** Unknown (apply within 48h)
- **Next action:** Run `/analyze-job Redpin`

### 2. Storio - Senior PM Data Platform (Fit: 8.5/10)
- **Status:** Application submitted 2025-11-05
- **Next action:** Monitor for response

---

## ⭐ Medium Priority (Fit 7-7.9)

### 3. Mastercard - Director Cross-border Services (Fit: 7.5/10)
- **Status:** In shortlist
- **Research needed:** Confirm product vs. product marketing role
- **Next action:** LinkedIn research, then `/analyze-job`

---

**Quick actions:**
```bash
# Apply to Redpin:
/analyze-job Redpin

# Research Mastercard:
# (LinkedIn search for team members)
```
```

### Migration Plan

```bash
# 1. Create pipeline folders
mkdir -p staging/0-discovery/automated
mkdir -p staging/0-discovery/manual
mkdir -p staging/1-triage
mkdir -p staging/2-shortlist/high
mkdir -p staging/2-shortlist/medium
mkdir -p staging/3-applying
mkdir -p staging/archive/low-fit
mkdir -p staging/archive/filtered
mkdir -p staging/archive/withdrawn

# 2. Categorize existing content by fit score
# High priority (tier1) → shortlist/high
mv staging/tier1-apply-now/* staging/2-shortlist/high/

# Medium priority (tier2) → shortlist/medium
mv staging/tier2-research/* staging/2-shortlist/medium/

# Low priority/unprocessed → discovery
mv staging/2025-11-05-discovery-batch/* staging/0-discovery/automated/
mv staging/manual-saves/* staging/0-discovery/manual/

# Archive low-fit
mv staging/tier3-maybe/* staging/archive/low-fit/
mv staging/archive/*/* staging/archive/low-fit/

# 3. Remove old folders
rmdir staging/tier1-apply-now staging/tier2-research staging/tier3-maybe
rmdir staging/2025-11-05-discovery-batch
rmdir staging/archive/2025-10-analyzed staging/archive/2025-11-bulk-analyzed
```

### Automation Enhancements

**Auto-move on /bulk-process:**
```python
# After analysis, automatically organize:
for job in analyzed_jobs:
    if job.fit_score >= 8:
        move_to("staging/2-shortlist/high/")
    elif job.fit_score >= 7:
        move_to("staging/2-shortlist/medium/")
    else:
        move_to("staging/archive/low-fit/")

# Update shortlist README
generate_shortlist_readme()
```

**Auto-move on /analyze-job:**
```python
# When starting application:
move_job("staging/2-shortlist/high/Redpin" → "staging/3-applying/")

# When submitted:
move_job("staging/3-applying/Redpin" → "staging/archive/low-fit/")
# (because now tracked in applications/ folder)
```

### Pros
- ✅ Clear pipeline stages (discovery → triage → shortlist → applying → archive)
- ✅ Mirrors real application funnel
- ✅ Automation-friendly (scripts can auto-move based on fit scores)
- ✅ Always know status ("Where is this job? In shortlist/high → need to apply")
- ✅ 2-shortlist/README.md = single source of truth for current opportunities
- ✅ Supports workflow analytics (conversion rates: discovery → shortlist → applying → submitted)

### Cons
- ⚠️ Most complex structure (9 subfolders)
- ⚠️ Requires automation updates to scripts
- ⚠️ May be over-engineered for solo job search (designed for team workflows)
- ⚠️ Longer migration (requires fit score categorization)

---

## Comparison Matrix

| Criteria | Approach 1: Status | Approach 2: Time-Based | Approach 3: Pipeline |
|----------|-------------------|----------------------|---------------------|
| **Simplicity** | ★★★★★ (4 folders) | ★★★☆☆ (batches add up) | ★★☆☆☆ (9 folders) |
| **Clarity** | ★★★★☆ (clear next actions) | ★★★★☆ (weekly rhythm) | ★★★★★ (funnel stages) |
| **Automation** | ★★☆☆☆ (manual moves) | ★★★☆☆ (weekly setup) | ★★★★★ (fully automated) |
| **Historical Tracking** | ★★☆☆☆ (no history) | ★★★★★ (weekly batches) | ★★★☆☆ (pipeline metrics) |
| **Migration Effort** | ★★★★★ (30 min) | ★★★★☆ (1 hour) | ★★☆☆☆ (2-3 hours) |
| **Scalability** | ★★★☆☆ (works for now) | ★★★★☆ (supports sprints) | ★★★★★ (enterprise-grade) |
| **Maintenance** | ★★★★★ (low effort) | ★★★☆☆ (weekly batch) | ★★★★☆ (automated) |

---

## Recommendations

### For Now (Next 2-4 Weeks)

**Recommendation: Approach 1 (Simple Status-Based)**

**Why:**
- You have 6 active applications already - focus on managing those, not folder reorganization
- Simple = less cognitive overhead during active job search
- Quick migration (can do today in 30 min)
- Easier to maintain while interviewing

**Implementation:**
```bash
# Run this today:
/reorganize-staging approach1
```

### Strategically (After Landing Role, Retrospective)

**Recommendation: Approach 3 (Priority Pipeline) IF building this as a product**

**Why:**
- You're already building an AI-powered job search system
- Pipeline approach supports metrics (conversion rates, time-in-stage)
- Automation-friendly for future users
- Showcases product thinking in your job search (meta: using PM skills to manage PM job search)

**But only if:**
- You're productizing this system (GitHub repo, sharing with others)
- You want to analyze "What's my discovery → offer conversion rate?"
- You're treating this as an AI PM upskilling project (building applied AI products)

**Implementation:**
```bash
# After getting offer, during retrospective:
/reorganize-staging approach3
# Then extract learnings for product documentation
```

### Alternative: Hybrid Approach

**Combine Approach 1 (Now) + Approach 2 (Weekly Batches) Later**

**Structure:**
```
staging/
├── inbox/                    # All new jobs
│   ├── manual-saves/
│   └── automated/
├── to-apply/                 # High-priority
└── archive/
    └── batches/             # Historical batches (after applying)
        ├── 2025-W45/
        └── 2025-W46/
```

**Workflow:**
- Use Approach 1 for active job search
- On Sundays: Move week's activity to archive/batches/2025-WXX/ for tracking
- Get simplicity NOW + historical tracking LATER

---

## Decision Time

**Questions to answer:**

1. **Immediate priority:** Fix staging chaos today? Or can it wait?
2. **Long-term vision:** Is this just for you, or are you building a product?
3. **Complexity tolerance:** Prefer simple (4 folders) or sophisticated (9 folders)?
4. **Tracking needs:** Need weekly stats? Or just "apply to high-priority jobs"?

**My recommendation based on current context:**

```
Short-term (Today): Approach 1 - Simple Status-Based
- You have 6 active applications to manage
- Focus on applying to Redpin + Mastercard this week
- Simple system = less distraction

Long-term (After offer): Decide based on:
- If productizing → Approach 3 (Pipeline)
- If personal use → Stick with Approach 1
- If want retrospectives → Approach 2 (Batches)
```

---

**Ready to proceed? Choose one:**

A. `/reorganize-staging approach1` - Implement Simple Status-Based now
B. `/reorganize-staging approach2` - Implement Time-Based Batches now
C. `/reorganize-staging approach3` - Implement Priority Pipeline now
D. "Let me think about it" - No changes yet

**Or tell me:**
- What feels most intuitive to you?
- What's your main frustration with current system?
- How much time do you want to spend on folder organization vs. applying?
