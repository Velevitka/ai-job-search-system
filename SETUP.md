# Setup Guide

Quick setup instructions for your job application management system.

## Step 1: Organize Your Files

### Move Your Master CV
Find your current base CV file and move it to:
```
master/ArturSwadzba_MasterCV.docx
```

This is now your **source of truth** - all tailored CVs will be based on this.

### Clean Up Old CVs
Your current directory has many CV versions. Here's what to do:

**Keep:**
- `ArturSwadzba_MasterCV.docx` (or your newest/best version) → Move to `master/`
- Any CVs from active applications → Can reference for now

**Archive or Delete:**
- All the dated CV files (e.g., `Artur_Swadzba_CV_27April.docx`)
- Company-specific CVs from past applications (e.g., `ArturSwadzba_Revolut.docx`)

These are now replaced by your new system which will generate tailored CVs in `applications/` folders.

---

## Step 2: Test the System

### Quick Test with One Application

1. **Find a job posting** (can be real or practice)

2. **Run analysis:**
   ```bash
   /analyze-job https://linkedin.com/jobs/...
   # Or paste the full job description text
   ```

3. **Check the output:**
   - Look in `applications/2025-01-CompanyName-Role/`
   - Review `job-description.md`
   - Review `analysis.md` - check the fit score

4. **If fit score is good (7+), generate CV:**
   ```bash
   /generate-cv CompanyName
   ```

5. **Review the tailoring plan:**
   - Open `cv-tailoring-plan.md`
   - Check for hallucinations (made-up achievements)
   - Verify all metrics match your master CV
   - Type "approved" to generate the Word doc

6. **Verify the final CV:**
   - Open `ArturSwadzba_CompanyName.docx`
   - Spot-check 3-5 bullets for accuracy
   - Ensure formatting looks good

**If everything looks good, you're ready to use the system!**

---

## Step 3: Populate CV Snippets

Open `master/cv-snippets.md` and add your key achievements organized by theme:

**Example:**
```markdown
## Growth & Experimentation
• Led growth experimentation program driving 30% increase in user activation
• Reduced CAC by 40% while scaling from 500K to 2M users

## Platform & Infrastructure
• Built CDP serving 2M+ users and processing $2B in transactions
• Delivered $5M in cost savings through MarTech stack optimization
```

This library makes CV tailoring much faster - you can quickly pull relevant bullets.

---

## Step 4: Set Up Your Weekly Routine

### Sunday Evening (30 min)
```bash
/weekly-review
```
- Review the week's progress
- Identify patterns
- Plan next week's targets

### Daily (when actively applying)
- Morning: Check staging folder, bulk process JDs
- Throughout day: Apply to 1-3 high-fit roles
- Track everything with `/update-status`

---

## Step 5: Migrate Existing Applications (Optional)

If you have active applications in progress:

1. **For each active application:**
   - Create a folder: `applications/2025-01-CompanyName-Role/`
   - Add `status.md` with current status
   - Copy the job description to `job-description.md`

2. **Update status:**
   ```bash
   /update-status CompanyName [current-status] "notes"
   ```

This gets them into the tracking system.

---

## Step 6: Clean Up Root Directory

After migrating to the new system, your root directory should contain:

**Folders:**
- `.claude/` (commands)
- `master/` (base CV and snippets)
- `staging/` (JDs to process)
- `applications/` (active applications)
- `insights/` (analytics and patterns)

**Files:**
- `CLAUDE.md` (system architecture - for AI)
- `README.md` (usage guide - for you)
- `SETUP.md` (this file - one-time setup)

**To Archive:**
- All old CV versions (move to `archive/` or delete)
- Old cover letters (move to `archive/` or delete)
- Random docs (organize or delete)

---

## Common Setup Issues

### Issue: Commands not working

**Check:**
1. Are you in the correct directory?
2. Is `.claude/commands/` folder present with command files?
3. Try running a simple command like `/analyze-job --help`

### Issue: Master CV not found

**Check:**
1. Is file named exactly `ArturSwadzba_MasterCV.docx`?
2. Is it in the `master/` folder?
3. Is it a `.docx` file (not `.pdf` or `.doc`)?

### Issue: Folders not created

Run this command to create the structure:
```bash
mkdir -p .claude/commands master staging applications insights
```

---

## Next Steps

Once setup is complete:

1. ✅ Master CV in place
2. ✅ Test run completed successfully
3. ✅ CV snippets populated
4. ✅ Directory cleaned up
5. ✅ Ready to apply!

**Start with:**
```bash
# Put JDs in staging/ folder, then:
/bulk-process

# Or analyze a single job:
/analyze-job [url or paste JD]
```

**Read:** `README.md` for daily workflows and detailed usage

**Reference:** `CLAUDE.md` for system architecture (if you're curious)

---

## Quick Command Reference

```bash
# Core workflow
/analyze-job <url-or-paste>     # Analyze job and create fit score
/generate-cv CompanyName         # Generate tailored CV
/generate-cl CompanyName         # Generate cover letter
/update-status Company status    # Track application

# Batch processing
/bulk-process                    # Process all JDs in staging/

# Analytics
/weekly-review                   # Weekly insights and metrics

# Interview
/prepare-interview Company       # Prep questions
/analyze-interview Company file  # Analyze performance
```

---

## Support

**Questions about:**
- System usage → Read `README.md`
- Daily workflow → Check `README.md` daily routines section
- Commands → See `.claude/commands/` or `CLAUDE.md`
- Strategy → Review `insights/patterns.md` as data accumulates

---

**Setup complete? Delete this file and start applying!**

Or keep it as reference for troubleshooting.

Good luck! 🚀
