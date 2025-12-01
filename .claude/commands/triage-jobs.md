# Triage Jobs - Parallel Batch Categorization

You are the **Triage Orchestrator** that processes discovery jobs using Sonnet in parallel batches for rapid categorization.

## Mission

Analyze all job files in `staging/0-discovery/` and categorize them into priority tiers based on fit score and career preferences alignment.

## Input

```
/triage-jobs
```

No arguments needed. Scans `staging/0-discovery/` automatically.

## Process

### Step 1: Scan Discovery Folder

List all markdown files in `staging/0-discovery/`:
- Include: `*.md` files in root
- Exclude: `DISCOVERY-AUDIT-*.md` files
- Exclude: Files in subfolders (`automated/`, `manual/`)

Display inventory:
```
Scanning staging/0-discovery/...

Files found: X markdown files
Excluded: Y audit files, Z subfolder files

Proceeding with X files for triage.
```

If no files found, display message and exit.

### Step 2: Read Career Preferences (CRITICAL)

**BEFORE any analysis, read `career-preferences.md` to extract current rules.**

This ensures dynamic filtering that respects preference changes.

Extract from career-preferences.md:
1. **Location preferences** (Preferred / Open to / Avoid)
2. **Seniority preferences** (Target / Consider / Avoid)
3. **Industry preferences** (Tier 1 / Tier 2 / Tier 3 / Avoid)
4. **Deal-breakers** (from "Absolutely Avoid" and "Deal-Breakers" sections)
5. **Work arrangement** preferences

Store these rules for use in categorization.

### Step 3: Pre-Detect Incomplete Files

Before LLM analysis, check each file for completeness:

**Route to `staging/1-triage/` if:**
- Location contains "Unknown" or "UnknownLocation" or is missing
- No `## Job Description` section or section has < 100 words
- No job title (first line should be `# [Title]`)

For incomplete files:
1. Move immediately to `staging/1-triage/`
2. Record in results as `CATEGORY: triage`
3. Do not include in LLM batch analysis

Display pre-filter results:
```
Pre-filtering complete:
- Complete files: X (proceeding to analysis)
- Incomplete files: Y (moved to staging/1-triage/)
  - Missing location: A files
  - Missing/short description: B files
```

### Step 4: Create Parallel Batches

Split remaining files into 8 batches for parallel processing:

```
Total files: N
Batch size: ceil(N / 8)

Batch 1: files[0:batch_size]
Batch 2: files[batch_size:batch_size*2]
...
Batch 8: remaining files
```

### Step 5: Launch Parallel Analysis

Launch 8 Task agents in a SINGLE message using Sonnet model.

**Each agent receives:**
1. Career preferences summary (from Step 2)
2. Candidate profile summary (key experience points)
3. Batch of job files to analyze

**Agent prompt template:**

```
You are a Job Fit Analyst. Analyze these job files against the candidate profile and career preferences.

## Career Preferences
[Insert extracted preferences from career-preferences.md]

## Candidate Profile Summary
- 10+ years Product Management experience
- Current: Executive Director at Chase UK (Growth Platform, Data Platform)
- Previous: Director/Senior PM at Vrbo/Expedia Group (5 years)
- Expertise: Data platforms, MarTech, Growth PM, Consumer marketplaces
- Location: London (BR1), Polish passport (EU citizen)

## Deal-Breakers (from career-preferences.md)
[Insert current deal-breakers dynamically]

## Jobs to Analyze
[Insert batch of job files]

## Output Format
For EACH job, output EXACTLY this format:

---
FILENAME: [exact filename]
CATEGORY: high/medium/low/filtered
FIT_SCORE: [1-10]
LOCATION_OK: yes/no/unknown
SENIORITY_OK: yes/no
INDUSTRY_OK: yes/no
DEAL_BREAKER: none/[specific deal-breaker type]
RATIONALE: [1 sentence explanation]
---

## Categorization Rules
- FIT_SCORE 8-10 + no deal-breakers = high
- FIT_SCORE 6-7.5 + no deal-breakers = medium
- FIT_SCORE < 6 + no deal-breakers = low
- Any deal-breaker present = filtered (regardless of fit score)

Be strict with deal-breakers. Be honest with fit scores.
```

### Step 6: Aggregate Results

After all 8 agents complete:
1. Collect all structured outputs
2. Parse into results array
3. Combine with pre-filtered incomplete files (from Step 3)
4. Verify total matches original file count

### Step 7: Move Files to Destinations

Based on CATEGORY, move each file:

| Category | Destination |
|----------|-------------|
| high | `staging/2-shortlist/high/` |
| medium | `staging/2-shortlist/medium/` |
| low | `staging/2-shortlist/low/` |
| triage | `staging/1-triage/` (already moved in Step 3) |
| filtered | `staging/archive/filtered/` |

Create destination folders if they do not exist.

Verify after moving:
```bash
# staging/0-discovery/ should only have audit files and subfolders
ls staging/0-discovery/*.md | grep -v DISCOVERY-AUDIT
# Should return empty
```

### Step 8: Generate Summary Report

Create: `insights/triage-summary-YYYY-MM-DD.md`

**Report structure:**

```markdown
# Triage Summary - YYYY-MM-DD

**Generated:** YYYY-MM-DD HH:MM
**Files Processed:** X
**Model:** Sonnet (parallel batches)

---

## Quick Reference

| # | Company | Role | Location | Fit | Category | Reason |
|---|---------|------|----------|-----|----------|--------|
| 1 | [Company] | [Role] | [Location] | X/10 | HIGH | [1-line] |
| 2 | ... | ... | ... | ... | ... | ... |

---

## Results by Category

### HIGH (X files) -> staging/2-shortlist/high/
| Company | Role | Fit | Key Match |
|---------|------|-----|-----------|
| ... | ... | ... | ... |

### MEDIUM (X files) -> staging/2-shortlist/medium/
| Company | Role | Fit | Notes |
|---------|------|-----|-------|
| ... | ... | ... | ... |

### LOW (X files) -> staging/2-shortlist/low/
| Company | Role | Fit | Concerns |
|---------|------|-----|----------|
| ... | ... | ... | ... |

### TRIAGE (X files) -> staging/1-triage/
| Company | Role | Missing |
|---------|------|---------|
| ... | ... | ... |

### FILTERED (X files) -> staging/archive/filtered/
| Company | Role | Deal-Breaker |
|---------|------|--------------|
| ... | ... | ... |

---

## Statistics

- Total: X files
- High: Y (Z%)
- Medium: Y (Z%)
- Low: Y (Z%)
- Triage: Y (Z%)
- Filtered: Y (Z%)

---

## Next Actions

1. Review HIGH priority in staging/2-shortlist/high/
2. Complete missing data for TRIAGE files in staging/1-triage/
3. Run /analyze-jobs-parallel on top HIGH candidates
```

### Step 9: Display Final Summary

```
TRIAGE COMPLETE

Processed: X files
Time: Y minutes Z seconds

Results:
- HIGH:     A files -> staging/2-shortlist/high/
- MEDIUM:   B files -> staging/2-shortlist/medium/
- LOW:      C files -> staging/2-shortlist/low/
- TRIAGE:   D files -> staging/1-triage/
- FILTERED: E files -> staging/archive/filtered/

Report: insights/triage-summary-YYYY-MM-DD.md

Next: Review staging/2-shortlist/high/ and run /analyze-jobs-parallel
```

---

## Error Handling

**If file read fails:**
- Log error, continue with other files
- Add to "errors" section of summary

**If batch agent times out:**
- Retry once
- If still fails, process those files sequentially

**If destination folder missing:**
- Create automatically with mkdir -p

**If file move fails:**
- Log error, continue with other files
- Report in summary

---

## Important Notes

1. **Dynamic preferences:** Always read career-preferences.md fresh; do not use hardcoded rules
2. **No duplicates:** Each file processed exactly once
3. **Audit file preservation:** Never move DISCOVERY-AUDIT-*.md files
4. **Subfolder preservation:** Do not process files in automated/ or manual/
5. **Parallel execution:** All 8 Task calls in single message for true parallelization
