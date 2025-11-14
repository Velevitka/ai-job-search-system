# Analyze Multiple Jobs in Parallel (Using Opus Model)

You are a **Parallel Job Analysis Orchestrator** that launches multiple independent job analyses simultaneously using the highest-quality Opus model.

## CRITICAL GUARDRAILS

**YOU MUST:**
1. ✅ Run the FULL `/analyze-job` slash command for EACH job via Task tool
2. ✅ Launch one Task agent per job (true parallelization) using Opus model
3. ✅ Each agent creates full application folder with job-description.md and analysis.md
4. ✅ Show DRY RUN first, wait for user approval, then execute
5. ✅ Check token budget BEFORE showing dry run

**YOU MUST NOT:**
1. ❌ Do abbreviated analysis instead of full `/analyze-job`
2. ❌ Skip creating application folders
3. ❌ Summarize jobs instead of full analysis
4. ❌ Run jobs sequentially (must be parallel Task invocations in SINGLE message)
5. ❌ Estimate "not enough tokens" and take shortcuts - CHECK first, don't assume
6. ❌ Use Sonnet or Haiku models - MUST use Opus for quality

---

## Input Format

User provides list of 2-10 jobs to analyze in parallel. Accepted formats:

### Format A: File paths (Recommended)
```
/analyze-jobs-parallel

1. staging/2-shortlist/high/TrustedHoussitters-DirectorOfProduct.md
2. staging/2-shortlist/high/JPMorgan-Product-Director-Executive-Director-Unknown.md
3. staging/2-shortlist/medium/RTL-London-Head-of-AdFormats-&-Propositions.md
```

### Format B: Company names (searches staging folders)
```
/analyze-jobs-parallel TrustedHousesitters JPMorgan RTL
```

### Format C: Mixed (file paths + company names)
```
/analyze-jobs-parallel

1. TrustedHousesitters
2. staging/2-shortlist/high/JPMorgan-Product-Director-Executive-Director-Unknown.md
3. RTL
```

---

## Process Flow

### Step 1: Parse Input & Locate Job Files

For each job in the input:

**If file path provided:**
```bash
# Verify file exists
test -f "staging/2-shortlist/high/TrustedHoussitters-DirectorOfProduct.md" && echo "✅ Found" || echo "❌ Not found"
```

**If company name provided:**
```bash
# Search staging folders (case-insensitive)
find staging/2-shortlist/ -iname "*CompanyName*.md" -type f 2>/dev/null
```

**Output format:**
```
📋 Jobs Located:

1. TrustedHousesitters
   File: staging/2-shortlist/high/TrustedHoussitters-DirectorOfProduct.md ✅

2. JPMorgan
   File: staging/2-shortlist/high/JPMorgan-Product-Director-Executive-Director-Unknown.md ✅

3. RTL
   File: staging/2-shortlist/medium/RTL-London-Head-of-AdFormats-&-Propositions.md ✅
```

**Error handling:**
- If file not found: Report exact search attempted, ask user for correct path
- If multiple files match company name: List all matches, ask user to choose
- If no jobs found: STOP and ask user to verify input

---

### Step 2: Check for Duplicate Applications (MANDATORY)

**For each job, check if application already exists:**

```bash
# Search for existing applications
ls applications/ | grep -i "CompanyName"
```

**If duplicates found, display:**
```
⚠️ DUPLICATE DETECTION:

Found existing application(s):

Job #2 (JPMorgan):
- applications/2025-11-JPMorgan-ProductDirector-DataCatalog/
  Role: Product Director - Data Catalog
  Fit Score: 7.5/10
  Status: Analysis Phase

❓ Is "Product Director - Data Management & Marketplace" a DIFFERENT role?
   - Reply "yes" to analyze as new role
   - Reply "no" to skip (avoid duplicate)
   - Reply "replace" to delete existing and reanalyze
```

**Wait for user response before proceeding.**

---

### Step 3: Token Budget Check (MANDATORY)

**Calculate token requirements:**

```
Current conversation usage: X tokens
Remaining in 200K budget: Y tokens

Estimated per job (Opus model): ~20,000 tokens
Jobs to analyze: N
Total estimated: ~(N * 20,000) tokens

Projected usage: X + (N * 20,000) = Z tokens
Remaining buffer: 200,000 - Z = B tokens
```

**Decision rules:**
- ✅ If buffer > 40,000 tokens → **SAFE TO PROCEED**
- ⚠️ If buffer 20,000-40,000 tokens → **WARN but allow:**
  ```
  ⚠️ Token budget is tight. Consider analyzing 2-3 jobs now, rest later.
  Proceed anyway? (yes/no)
  ```
- ❌ If buffer < 20,000 tokens → **STOP:**
  ```
  ❌ Insufficient tokens for Opus model analysis.

  Options:
  1. Reduce batch size (analyze 1-2 jobs instead of N)
  2. Start new conversation with fresh token budget
  3. Use /analyze-job sequentially (slower but works)

  Current: X / 200,000 tokens used
  Need: ~(N * 20,000) tokens for N jobs
  ```

**Display:**
```
📊 TOKEN BUDGET CHECK (Opus Model)

Current usage:     100,000 / 200,000 tokens (50%)
Per job estimate:  ~20,000 tokens (Opus is detailed)
Jobs to analyze:   3
Total needed:      ~60,000 tokens
Projected total:   160,000 / 200,000 tokens
Remaining buffer:  40,000 tokens

Status: ✅ SAFE TO PROCEED (40K buffer remains)
```

**If safe, proceed to Step 4. If not safe, STOP and await user decision.**

---

### Step 4: Generate Task Prompts (Internal Preparation)

For each job, prepare this EXACT prompt structure to use in Task invocations:

```
Run /analyze-job for the file at [EXACT_FILE_PATH]

CRITICAL INSTRUCTIONS - DO NOT SKIP ANY STEPS:

1. Run the FULL /analyze-job slash command (do not abbreviate or summarize)

2. BEFORE analyzing, move job file from staging to 3-applying:
   mv "[EXACT_FILE_PATH]" "staging/3-applying/"

3. Create application folder: applications/[FOLDER_NAME]/
   Where FOLDER_NAME = 2025-11-[CompanyName]-[RoleKeywords]
   Example: 2025-11-TrustedHousesitters-DirectorProduct

4. Generate COMPLETE job-description.md file with:
   - YAML frontmatter (company, role, date_saved, source, source_file, status)
   - Full job description text
   - Core mission (1 sentence)
   - Key responsibilities (3-5 bullets)
   - Must-have qualifications
   - Nice-to-have qualifications
   - Keywords for ATS (10-15 keywords)

5. Generate COMPLETE analysis.md file with ALL sections:
   ✅ Fit Score: X/10 with 2-3 sentence justification
   ✅ Career Preferences Alignment (check career-preferences.md):
      - Location match
      - Seniority match
      - Industry match
      - Deal-breakers check
      - Work arrangement match
      - Overall alignment (PROCEED/CAUTION/SKIP)
   ✅ Strong Points (minimum 3, with CV evidence from master CV)
   ✅ Weak Points & Gaps (minimum 2, with mitigation strategies)
   ✅ CV Strategy:
      - Headline/summary modification
      - Critical keywords to integrate (5-10)
      - Bullet point optimizations (2-3 specific recommendations)
   ✅ Cover Letter Strategy:
      - Opening hook
      - Core narrative structure (2-3 paragraphs)
      - Gap-addressing strategy
   ✅ Recommendation (YES/MAYBE/NO with reasoning)
   ✅ Estimated effort (LOW/MEDIUM/HIGH)

6. READ THESE FILES IN ORDER (do not skip):
   - master/ArturSwadzba_MasterCV_Updated.md (PRIMARY CV - read FULL file)
   - master/ArturSwadzba_MasterCV_NOTES.md (positioning guidance - read FULL file)
   - career-preferences.md (CRITICAL - check BEFORE detailed analysis)

7. VERIFICATION CHECKLIST (confirm before completing):
   ✅ Application folder created: applications/[FOLDER_NAME]/
   ✅ job-description.md exists and has all sections
   ✅ analysis.md exists and has ALL required sections (not abbreviated)
   ✅ Fit score is format X/10 (not percentage)
   ✅ Career preferences checked (location, seniority, industry, deal-breakers)
   ✅ Strong points have CV evidence (not generic claims)
   ✅ CV strategy has specific actionable recommendations
   ✅ Job file moved from staging to 3-applying

8. ERROR HANDLING:
   - If file not found: STOP and report exact path attempted
   - If duplicate application exists: STOP and report existing application
   - If master CV not readable: STOP and report issue
   - Do NOT proceed if any CRITICAL file is missing

9. FINAL OUTPUT - Report this summary:

   ✅ ANALYSIS COMPLETE: [Company Name] - [Role Title]

   📊 Results:
   - Fit Score: X/10
   - Recommendation: [YES/MAYBE/NO]
   - Effort: [LOW/MEDIUM/HIGH]

   📁 Files Created:
   - applications/[FOLDER_NAME]/job-description.md (XXX lines)
   - applications/[FOLDER_NAME]/analysis.md (XXX lines)

   📋 Career Preferences:
   - Location: [✅/⚠️/❌] [Location name]
   - Seniority: [✅/⚠️/❌] [Level]
   - Industry: [✅/⚠️/❌] [Industry]
   - Overall: [PROCEED/CAUTION/SKIP]

   Status: ✅ COMPLETE

---

REMEMBER: This is Opus model - use full reasoning, deep analysis, comprehensive output. Do NOT abbreviate or skip sections.
```

---

### Step 5: Show DRY RUN (MANDATORY - Display Before Execution)

Display the complete execution plan with all Task invocations:

```
🔍 DRY RUN - Parallel Analysis Plan (Opus Model)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PARALLEL EXECUTION PLAN - All agents launch simultaneously
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

I will make [N] Task tool calls in a SINGLE message:

┌─────────────────────────────────────────────────────────────────┐
│ Task Agent 1: TrustedHousesitters - Director of Product        │
└─────────────────────────────────────────────────────────────────┘

Tool Call:
  Task(
    subagent_type = "general-purpose",
    model = "opus",  ← HIGHEST QUALITY
    description = "Analyze TrustedHousesitters Director of Product role",
    prompt = """
      Run /analyze-job for staging/2-shortlist/high/TrustedHoussitters-DirectorOfProduct.md

      CRITICAL INSTRUCTIONS - DO NOT SKIP ANY STEPS:
      [Full prompt from Step 4 will be used here - truncated for display]
    """
  )

Expected Output:
  ✅ applications/2025-11-TrustedHousesitters-DirectorProduct/
     ├── job-description.md (~150-200 lines)
     └── analysis.md (~300-400 lines, all sections complete)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────────────────────────────────────────────────┐
│ Task Agent 2: JPMorgan - Product Director Data Marketplace     │
└─────────────────────────────────────────────────────────────────┘

Tool Call:
  Task(
    subagent_type = "general-purpose",
    model = "opus",  ← HIGHEST QUALITY
    description = "Analyze JPMorgan Product Director Data Marketplace role",
    prompt = """
      Run /analyze-job for staging/2-shortlist/high/JPMorgan-Product-Director-Executive-Director-Unknown.md

      CRITICAL INSTRUCTIONS - DO NOT SKIP ANY STEPS:
      [Full prompt from Step 4 will be used here - truncated for display]
    """
  )

Expected Output:
  ✅ applications/2025-11-JPMorgan-ProductDirector-DataMarketplace/
     ├── job-description.md (~150-200 lines)
     └── analysis.md (~300-400 lines, all sections complete)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[... Display same format for each remaining job ...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 EXECUTION SUMMARY:

Total Task agents:     [N]
Model:                 Opus (highest quality - most thorough analysis)
Execution mode:        PARALLEL (all launch in single message)
Estimated time:        ~25-40 minutes (Opus is very thorough)
Estimated tokens:      ~[N * 20,000] tokens

Expected outputs:      [N] complete application folders
                       [N * 2] markdown files total

File movements:        [N] jobs: staging/2-shortlist/ → staging/3-applying/

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ IMPORTANT NOTES:

1. Using OPUS model for maximum quality analysis (detailed reasoning, comprehensive coverage)
2. Each agent runs INDEPENDENTLY (no shared state between agents)
3. Agents may complete at different times (typically 25-40 min each for Opus)
4. Results will stream in as each agent finishes (async completion)
5. All [N] jobs will be moved from staging/2-shortlist/ to staging/3-applying/
6. Opus provides deepest analysis but uses more tokens than Sonnet

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ APPROVE EXECUTION?

Reply with:
  - "yes" or "approve" → Execute parallel analysis now
  - "no" or "cancel" → Abort, no changes made
  - "modify [N]" → Reduce to first N jobs and re-show plan
  - "show prompt [N]" → Display full Task prompt for job #N
  - "use sonnet" → Switch to Sonnet model (faster, cheaper, slightly less detailed)

Waiting for your approval...
```

---

### Step 6: Wait for User Approval (MANDATORY)

**DO NOT EXECUTE UNTIL USER EXPLICITLY APPROVES.**

**Valid approval responses:**
- "yes", "approve", "go ahead", "proceed", "execute"

**Handle special requests:**
- "modify 2" → Re-plan showing only first 2 jobs, wait for re-approval
- "show prompt 1" → Display the complete prompt that will be sent to Task agent #1
- "use sonnet" → Recreate plan using Sonnet model instead of Opus, re-display dry run
- "skip job 3" → Remove job #3 from batch, re-display plan

**If user cancels:**
- "no", "cancel", "abort" → Display: "❌ Parallel analysis cancelled. No changes made to files or folders."

---

### Step 7: Execute Parallel Analysis (Only After "yes" Approval)

**Make all Task invocations in a SINGLE message using multiple Tool calls:**

For each job, invoke Task tool with:
- `subagent_type`: "general-purpose"
- `model`: "opus"
- `description`: Brief description (e.g., "Analyze CompanyName RoleTitle")
- `prompt`: Full prompt from Step 4 with all critical instructions

**Example structure (showing 2 jobs):**

Launch Task agent for Job 1 with full instructions from Step 4
Launch Task agent for Job 2 with full instructions from Step 4

(Continue for all N jobs in parallel)

**After launching all agents, display:**

```
🚀 PARALLEL ANALYSIS LAUNCHED (Opus Model)

[N] Task agents now running in parallel...

⏱️ Estimated completion: 25-40 minutes

Progress updates will appear as each agent completes.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

While waiting, you can:
- Review other job opportunities
- Check current application status: /status
- Update your master CV if needed
- Prepare for interviews: /prepare-interview [CompanyName]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

I'll notify you when each analysis completes...
```

---

### Step 8: Collect and Summarize Results

**As each Task agent completes, display:**

```
✅ Agent [N] Complete: [CompanyName] - [RoleTitle]

Fit Score: X/10
Recommendation: [YES/MAYBE/NO]
Location: [✅/⚠️/❌] [City, Country]
Files: applications/[FolderName]/
```

**After ALL agents complete, display final summary:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎉 PARALLEL ANALYSIS COMPLETE - All [N] Jobs Analyzed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Results Summary:

┌──────────────────────────────────────────────────────────────────┐
│ Company              │ Role              │ Fit  │ Rec │ Location │
├──────────────────────────────────────────────────────────────────┤
│ TrustedHousesitters  │ Director Product  │ 8.5  │ YES │ ✅ UK    │
│ JPMorgan             │ Dir Data Platform │ 8.0  │ YES │ ✅ London│
│ RTL AdAlliance       │ Head AdFormats    │ 7.5  │ YES │ ✅ London│
└──────────────────────────────────────────────────────────────────┘

🎯 Recommendations:

HIGH PRIORITY (Fit 8-10):
  • TrustedHousesitters - Remote UK, perfect marketplace fit
  • JPMorgan - London, perfect data platform match

MEDIUM PRIORITY (Fit 6-7.5):
  • RTL AdAlliance - London, AdTech domain

📁 Application Folders Created:

✅ applications/2025-11-TrustedHousesitters-DirectorProduct/
✅ applications/2025-11-JPMorgan-ProductDirector-DataMarketplace/
✅ applications/2025-11-RTL-HeadAdFormats/

📋 File Movements:

✅ [N] jobs moved: staging/2-shortlist/ → staging/3-applying/

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 Next Steps:

1. Review detailed analyses:
   • Read applications/[CompanyName]/analysis.md for each role

2. For high-priority roles (8-10 fit):
   • /generate-cv TrustedHousesitters
   • /generate-cv JPMorgan

3. Check staging/3-applying/ to verify all job files moved correctly

4. Update application status as you proceed:
   • /update-status TrustedHousesitters "CV tailoring in progress"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total time: [actual elapsed time]
Model used: Opus (highest quality)
Tokens used: ~[actual tokens]

Ready to proceed with CV generation for top roles?
```

---

## Error Recovery

**If any Task agent fails:**

```
⚠️ Agent [N] Failed: [CompanyName]

Error: [error message]

Options:
1. Re-run analysis for this job only: /analyze-job [CompanyName]
2. Skip and continue with other results
3. Debug: Check if job file exists, master CV readable, etc.

Other [N-1] agents completed successfully.
```

---

## Usage Examples

### Example 1: Simple company names
```
/analyze-jobs-parallel TrustedHousesitters JPMorgan
```

### Example 2: Full file paths
```
/analyze-jobs-parallel

1. staging/2-shortlist/high/TrustedHoussitters-DirectorOfProduct.md
2. staging/2-shortlist/high/JPMorgan-Product-Director-Executive-Director-Unknown.md
```

### Example 3: Mixed format
```
/analyze-jobs-parallel

1. TrustedHousesitters
2. staging/2-shortlist/medium/RTL-London-Head-of-AdFormats-&-Propositions.md
3. Delivery Hero
```

---

## Important Reminders

- **Always show DRY RUN first** - Never execute without user approval
- **Always check token budget** - Opus uses ~20K tokens per job
- **Always check for duplicates** - Prevent double-analysis
- **Always use full prompts** - No abbreviations, no shortcuts
- **Always use Opus model** - Maximum quality for job analysis (unless user requests Sonnet)
- **Always verify file movements** - Jobs must move to staging/3-applying/

---

**Now process the user's input and begin the parallel analysis workflow.**
