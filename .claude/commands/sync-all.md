# Sync All Derived Views

You are the **System Synchronization Agent**, responsible for regenerating ALL derived views from application folder data to ensure complete system consistency.

## ⚡ Purpose

This command regenerates **ALL auto-generated files** from the source of truth (application folders) to ensure complete data consistency across the system.

**What this does:**
1. Regenerates `STATUS.md` (current status snapshot)
2. Regenerates `insights/metrics-dashboard.md` (aggregate metrics)
3. Validates consistency across all files
4. Reports any data quality issues found

**When to use this:**
- After making multiple status changes to applications
- When you suspect files are out of sync
- After manually editing application status files
- Before important reviews or presentations
- As part of weekly maintenance routine

**Commands executed:**
- `/status` → Regenerates STATUS.md
- `/update-metrics` → Regenerates metrics-dashboard.md

---

## Your Task

Execute a complete system synchronization:

### Step 1: Pre-Sync Validation

**Before regenerating, check current state:**

1. **Count application folders:**
   - Use Glob to find all `applications/*/status.md` files
   - Count total folders

2. **Check existing derived files:**
   - Does STATUS.md exist? When was it last updated?
   - Does insights/metrics-dashboard.md exist? When was it last updated?

3. **Identify potential issues:**
   - Folders without status.md files
   - status.md files with invalid formats
   - Missing required fields (status, dates, etc.)

**Display to user:**
```
🔄 Starting System Sync...

**Pre-sync Status:**
- Application folders found: X
- STATUS.md last updated: YYYY-MM-DD (X days ago)
- metrics-dashboard.md last updated: YYYY-MM-DD (X days ago)
- Potential issues: [None/X found]

**Regenerating all derived views...**
```

### Step 2: Regenerate STATUS.md

**Execute `/status` command logic:**

1. Scan all application folders
2. Parse status.md files
3. Calculate days waiting, averages, counts
4. Categorize: active, withdrawn, rejected
5. Validate data consistency
6. Generate STATUS.md content
7. Write to STATUS.md file

**Track metrics:**
- Folders scanned: X
- Status files read: X
- Active applications: X
- Data quality issues: X

### Step 3: Regenerate metrics-dashboard.md

**Execute `/update-metrics` command logic:**

1. Scan all application folders (reuse data from Step 2 if possible)
2. Calculate KPIs and conversion rates
3. Analyze by fit score, location, role type
4. Calculate time metrics
5. Validate data quality
6. Generate metrics-dashboard.md content
7. Write to insights/metrics-dashboard.md file

**Track metrics:**
- Data points analyzed: X
- Conversion rates calculated: X
- Data quality issues: X

### Step 4: Cross-File Validation

**Check consistency between regenerated files:**

1. **STATUS.md vs metrics-dashboard.md:**
   - Do application counts match?
   - Do fit score averages match?
   - Do active application lists match?

2. **Both vs application folders:**
   - Are all folders represented?
   - Are statuses consistent?
   - Are dates consistent?

3. **Flag any discrepancies:**
   - Report what doesn't match
   - Explain potential cause
   - Recommend fix

### Step 5: Generate Sync Report

**Display comprehensive report to user:**

```markdown
✅ System Sync Complete!

**Files Updated:**
- ✅ STATUS.md
- ✅ insights/metrics-dashboard.md

**Sync Summary:**
- Folders scanned: X
- Status files read: X
- Data points analyzed: X

**Current State:**
- Active applications: X
- Applications withdrawn: X
- Applications rejected: X
- Interviews scheduled: X
- Offers received: X

**Metrics Snapshot:**
- Average fit score: X.X/10
- Average days waiting: X.X days
- Conversion rate (app→interview): X%

**Data Quality:** [High/Medium/Low]
- ✅ All folders have status.md files
- ✅ All dates valid
- ✅ All calculations correct
- ✅ Cross-file consistency verified
- [✅/❌] No orphaned data

**Issues Found:** [None / X issues]
[List any issues if found]

**Validation Results:**
- STATUS.md shows X active applications
- metrics-dashboard.md shows X active applications
- ✅ Counts match / ❌ Mismatch detected (details below)

**Timestamps:**
- STATUS.md generated: YYYY-MM-DD HH:MM UTC
- metrics-dashboard.md generated: YYYY-MM-DD HH:MM UTC

---

📊 **All derived views now reflect current application data.**

💡 **Next Steps:**
- Review STATUS.md for current priorities
- Check insights/metrics-dashboard.md for performance trends
- Run `/status` anytime to refresh current state
- Run `/update-metrics` to refresh metrics only
- Run `/sync-all` again if you make bulk changes

⚠️ **Remember:** Manual edits to STATUS.md or metrics-dashboard.md will be overwritten by these commands. Always edit source files (applications/*/status.md) instead.
```

---

## Advanced Features

### Consistency Checks

**Check 1: Application Count Consistency**
```
STATUS.md active count: X
metrics-dashboard.md submitted count: Y
Application folders with status="applied": Z

Expected: X = Y = Z
Result: [✅ Match / ❌ Mismatch]
```

**Check 2: Fit Score Consistency**
```
STATUS.md average fit: X.X/10
metrics-dashboard.md average fit: Y.Y/10
Calculated from folders: Z.Z/10

Expected: X = Y = Z (within 0.1 rounding)
Result: [✅ Match / ❌ Mismatch]
```

**Check 3: Date Consistency**
```
All application dates in valid format (YYYY-MM-DD)
No dates in the future
Days waiting calculations make sense

Result: [✅ All valid / ❌ X issues found]
```

### Error Recovery

**If STATUS.md generation fails:**
```
❌ Error generating STATUS.md: [error message]

Attempting recovery:
1. Validating application folder structure
2. Checking for corrupted status.md files
3. Generating partial report from valid data

Result: [✅ Recovered / ❌ Manual intervention needed]
```

**If metrics-dashboard.md generation fails:**
```
❌ Error generating metrics-dashboard.md: [error message]

STATUS.md was successfully updated.

Attempting recovery:
[Recovery steps...]

Result: [✅ Recovered / ❌ Manual intervention needed]
```

**If cross-validation fails:**
```
⚠️ Files regenerated but consistency check failed:

Discrepancy found:
- STATUS.md shows X active applications
- metrics-dashboard.md shows Y applications

Possible causes:
- Different filtering criteria
- Timing issue (one file generated before status change)
- Data parsing inconsistency

Recommendation:
1. Check applications/*/status.md for data quality
2. Run /sync-all again
3. If persists, report as potential bug

Files updated but investigate discrepancy.
```

---

## Performance Optimization

**For large datasets (50+ applications):**

1. **Read all status.md files once** and cache in memory
2. **Reuse parsed data** for both STATUS.md and metrics-dashboard.md generation
3. **Parallel processing** where possible (though Claude Code is single-threaded)
4. **Progress indicators** for long operations

**Display during sync:**
```
🔄 Scanning application folders... [10/50 complete]
🔄 Parsing status files... [25/50 complete]
🔄 Calculating metrics... [40/50 complete]
✅ Writing STATUS.md...
✅ Writing metrics-dashboard.md...
✅ Validating consistency...
```

---

## Rules & Best Practices

**CRITICAL:**
1. **Complete atomicity** - If one file fails, report but continue with others
2. **Validate everything** - Never trust existing data, always recalculate
3. **Report clearly** - User should understand exactly what changed
4. **Add timestamps** - All generated files show when created
5. **Flag issues** - Don't hide data quality problems
6. **Be idempotent** - Running multiple times should be safe

**Execution Order:**
1. Pre-validation (understand current state)
2. STATUS.md generation (most frequently used file)
3. metrics-dashboard.md generation (depends on same data)
4. Cross-file validation (ensure consistency)
5. Report to user (clear summary)

**Never do:**
- ❌ Trust existing calculated values
- ❌ Skip validation checks
- ❌ Hide errors or inconsistencies
- ❌ Generate files without timestamps
- ❌ Leave partial updates if one file fails

---

## Output Format

**Success Case:**
```
✅ System Sync Complete!

Files Updated: 2
Data Quality: High
Issues Found: None

STATUS.md: X active applications
metrics-dashboard.md: Y total applications, Z% interview rate

⏱️ Sync completed in <1 second
```

**Partial Success:**
```
⚠️ System Sync Partially Complete

Files Updated: 1/2
- ✅ STATUS.md updated
- ❌ metrics-dashboard.md failed (error details)

Data Quality: Medium
Issues Found: 1

Recommendation: [Fix suggestion]
```

**Failure Case:**
```
❌ System Sync Failed

Files Updated: 0/2

Errors:
- STATUS.md: [Error message]
- metrics-dashboard.md: [Error message]

Source Data Issues:
- [Issue 1]
- [Issue 2]

Recommendation: Fix source data in applications/*/status.md files and try again.
```

---

## Related Commands

**Lighter alternatives:**
- `/status` - Regenerate STATUS.md only (faster)
- `/update-metrics` - Regenerate metrics-dashboard.md only
- `/weekly-review` - Full analysis + regenerates metrics (deeper)

**Use cases:**
- Daily check: `/status`
- After applying: `/status`
- Weekly maintenance: `/sync-all`
- Deep analysis: `/weekly-review`

---

**Now execute the complete system synchronization:**
1. Run `/status` logic internally
2. Run `/update-metrics` logic internally
3. Validate cross-file consistency
4. Report comprehensive sync results to user
