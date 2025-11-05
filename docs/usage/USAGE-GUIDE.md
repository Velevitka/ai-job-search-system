# Usage Guide - How to Use the System

Since custom slash commands may not be working yet, here's how to use the system with direct Claude Code prompts.

## Working Method (Use This Now)

Instead of slash commands like `/analyze-job`, use direct prompts to Claude Code with references to the command files.

### 1. Analyze a Job

**Prompt to use:**
```
Read the file .claude/commands/analyze-job.md and follow those instructions.

Here's the job description:
[paste job description or URL]
```

**What happens:**
- Claude reads the instructions from analyze-job.md
- Analyzes the JD based on your master CV
- Creates the application folder with analysis

### 2. Generate Tailored CV

**Prompt to use:**
```
Read the file .claude/commands/generate-cv.md and follow those instructions for [CompanyName].
```

**What happens:**
- Claude reads the CV generation instructions
- Creates tailoring plan
- Waits for your approval
- Generates the Word document

### 3. Generate Cover Letter

**Prompt to use:**
```
Read the file .claude/commands/generate-cl.md and follow those instructions for [CompanyName].
```

### 4. Update Application Status

**Prompt to use:**
```
Read the file .claude/commands/update-status.md and follow those instructions.

Company: [CompanyName]
Status: applied
Notes: "Submitted via LinkedIn, mentioned John as referral"
```

### 5. Weekly Review

**Prompt to use:**
```
Read the file .claude/commands/weekly-review.md and follow those instructions to generate my weekly review.
```

### 6. Prepare for Interview

**Prompt to use:**
```
Read the file .claude/commands/prepare-interview.md and follow those instructions for [CompanyName].
```

### 7. Analyze Interview Transcript

**Prompt to use:**
```
Read the file .claude/commands/analyze-interview.md and follow those instructions.

Company: [CompanyName]
Transcript file: applications/[folder]/interviews/transcript-YYYY-MM-DD.md
```

### 8. Bulk Process Staging Folder

**Prompt to use:**
```
Read the file .claude/commands/bulk-process.md and follow those instructions to process all JDs in staging/.
```

---

## Alternative: Create Agent-Based Tasks

You can also use Claude Code's Task tool for complex operations:

**Example for job analysis:**
```
Create a general-purpose agent to:
1. Read my master CV from master/ArturSwadzba_MasterCV.docx
2. Read the job description I provide
3. Create a fit score analysis
4. Generate the application folder structure
5. Create job-description.md and analysis.md files

Here's the job description:
[paste JD]
```

---

## Quick Reference Table

| Task | What to Say to Claude |
|------|----------------------|
| Analyze job | "Read .claude/commands/analyze-job.md and follow those instructions. Here's the JD: [paste]" |
| Generate CV | "Read .claude/commands/generate-cv.md and follow those instructions for [Company]" |
| Generate CL | "Read .claude/commands/generate-cl.md and follow those instructions for [Company]" |
| Update status | "Read .claude/commands/update-status.md and follow those instructions. Company: [X], Status: [Y], Notes: [Z]" |
| Weekly review | "Read .claude/commands/weekly-review.md and follow those instructions" |
| Interview prep | "Read .claude/commands/prepare-interview.md and follow those instructions for [Company]" |
| Analyze interview | "Read .claude/commands/analyze-interview.md and follow those instructions for [Company], transcript: [file]" |
| Bulk process | "Read .claude/commands/bulk-process.md and follow those instructions" |

---

## Even Simpler: Natural Language Prompts

You can also just ask Claude Code directly:

**For job analysis:**
```
I have a job description for [Company] - [Role].

Please:
1. Read my master CV from master/ArturSwadzba_MasterCV.docx
2. Analyze this JD and give me a fit score out of 10
3. Identify my strong points and gaps
4. Extract keywords for ATS
5. Create the application folder and analysis files

Here's the JD:
[paste job description]
```

**For CV generation:**
```
I want to create a tailored CV for [Company].

Please:
1. Read my master CV from master/ArturSwadzba_MasterCV.docx
2. Read the analysis from applications/[folder]/analysis.md
3. Create a CV tailoring plan
4. Show me the plan for approval
5. After I approve, generate the Word document

Don't fabricate anything - only use content from my master CV.
```

---

## Why Slash Commands Aren't Working

Custom slash commands in Claude Code may require:
1. Specific file format or metadata
2. Claude Code to be restarted
3. Additional configuration in settings

**For now, use the methods above.** They work exactly the same way - the command files contain the instructions that Claude follows.

---

## Recommended Workflow (Using Direct Prompts)

### Morning: Find and Analyze Jobs

1. **Find interesting jobs**, save JDs to `staging/` folder

2. **Bulk process:**
   ```
   Read .claude/commands/bulk-process.md and analyze all JDs in staging/
   ```

3. **Review the priority list** in `insights/bulk-analysis-YYYY-MM-DD.md`

### Daily: Apply to Jobs

For each job you decide to pursue:

1. **Full analysis** (if not done in bulk):
   ```
   Read .claude/commands/analyze-job.md and analyze this job:
   [paste JD or URL]
   ```

2. **Generate CV:**
   ```
   Read .claude/commands/generate-cv.md for [CompanyName]
   ```
   - Review tailoring plan
   - Approve
   - Verify final CV for hallucinations

3. **Generate CL** (if needed):
   ```
   Read .claude/commands/generate-cl.md for [CompanyName]
   ```
   - Review draft
   - Approve
   - Verify final CL

4. **Submit and track:**
   ```
   Read .claude/commands/update-status.md

   Company: [CompanyName]
   Status: applied
   Notes: "Submitted via LinkedIn on [date]"
   ```

### Weekly: Review and Learn

**Every Sunday:**
```
Read .claude/commands/weekly-review.md and generate my weekly review
```

Review the insights and adjust strategy for next week.

---

## Tips

**Be Specific:**
- Reference the exact command file you want Claude to follow
- Provide all necessary context (company name, job description, etc.)
- Ask Claude to confirm understanding before starting

**Verify Everything:**
- Check all AI-generated CVs for hallucinations
- Review metrics and dates for accuracy
- Approve tailoring plans before final generation

**Track Consistently:**
- Update status after every action (applied, interview, rejection)
- This builds your analytics database
- Enables pattern recognition over time

---

## Example: Full Application Workflow

Here's a complete example of applying to one job:

**Step 1: Analyze**
```
Read .claude/commands/analyze-job.md and follow those instructions.

Company: Spotify
Job Title: Senior Growth Product Manager
JD: [paste full job description]
```

**Step 2: Review Analysis**
- Open `applications/2025-01-Spotify-SeniorGrowthPM/analysis.md`
- Check fit score
- Decide to proceed (assuming 8/10)

**Step 3: Generate CV**
```
Read .claude/commands/generate-cv.md and follow those instructions for Spotify.
```

**Step 4: Review Tailoring Plan**
- Open `cv-tailoring-plan.md`
- Check for hallucinations
- Type "approved"

**Step 5: Verify Final CV**
- Open `ArturSwadzba_Spotify.docx`
- Spot-check 3-5 bullets
- Verify formatting

**Step 6: Generate CL** (if job requires)
```
Read .claude/commands/generate-cl.md and follow those instructions for Spotify.
```

**Step 7: Submit**
- Apply via LinkedIn/company website
- Track:
```
Read .claude/commands/update-status.md

Company: Spotify
Status: applied
Notes: "Applied via LinkedIn on 2025-01-29, mentioned Sarah Chen as referral"
```

**Done!** Application tracked, CV saved, ready for next one.

---

## Troubleshooting

**Q: Claude isn't following the instructions in the command file**
A: Try being more explicit: "Read the file .claude/commands/analyze-job.md word-for-word and follow every instruction in that file."

**Q: Files aren't being created**
A: Make sure the folder structure exists (master/, staging/, applications/, insights/)

**Q: CV has hallucinations**
A: Reject it and regenerate. Remind Claude: "Only use achievements from my master CV. Do not fabricate or inflate metrics."

**Q: This is too verbose**
A: Once you get comfortable, you can shorten prompts: "Analyze this job using the analyze-job process: [paste JD]"

---

## Future: Getting Slash Commands Working

To get proper slash commands working:
1. Check Claude Code documentation for slash command format
2. May need to add metadata or frontmatter to .md files
3. May need to restart Claude Code
4. May need specific file naming or location

For now, the direct prompt method works perfectly and does the same thing.

---

**Start with one job to test the system, then scale up!**
