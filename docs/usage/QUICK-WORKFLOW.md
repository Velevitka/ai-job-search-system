# Quick Workflow: Save Jobs with Bookmarklet

**5-minute guide to using the ToS-compliant job saving system**

---

## One-Time Setup (2 minutes)

### 1. Install Bookmarklet

See `BOOKMARKLET-INSTALL.md` for detailed instructions, or:

**Quick version:**
1. Show bookmarks bar: `Ctrl+Shift+B`
2. Right-click → "Add page"
3. Name: `Save Job`
4. URL: Copy from `BOOKMARKLET-INSTALL.md` (the minified code starting with `javascript:`)

### 2. Create Folders

```bash
mkdir -p staging/manual-saves
```

---

## Daily Workflow (Repeat as needed)

### Phase 1: Browse and Save (10-15 minutes for 10-20 jobs)

1. **Browse LinkedIn jobs** normally
   - Search for roles: "Director Product Data", "Head of Product", etc.
   - Filter: Location, Date Posted (Past Week), Experience Level

2. **For each interesting job:**
   - Read job summary
   - If it looks promising (potential 7+ fit) → Click "Save Job" bookmarklet
   - Alert appears: "✅ Job saved!"
   - File downloads to your **Downloads folder**
   - Continue browsing

3. **After saving 10-20 jobs:**
   - Go to your Downloads folder
   - Select all the `.md` files you just saved
   - **Move them** to `staging/manual-saves/`

**Time:** 10-15 minutes for 10-20 jobs

---

### Phase 2: Process Saved Jobs (30 seconds)

```bash
cd ~/path/to/cv-project
python scripts/process_saved_jobs.py
```

**What it does:**
- Deduplicates against existing applications
- Organizes into batch folder: `staging/2025-11-05-processed-batch/`
- Creates summary: `PROCESSING-SUMMARY.json`

**Output:**
```
✅ Processed: 18
⏭️  Duplicates: 2
❌ Errors: 0

📁 Saved to: staging/2025-11-05-processed-batch
```

**Time:** 30 seconds

---

### Phase 3: Bulk Analysis (10-15 minutes)

```bash
python scripts/bulk_analyze.py staging/2025-11-05-processed-batch
```

**What it does:**
- Runs `/analyze-job` on each job
- Calculates fit scores
- Generates prioritization report

**Review results:**
```bash
cat staging/2025-11-05-processed-batch/BULK-ANALYSIS-SUMMARY.md
```

**Time:** 10-15 minutes (automated)

---

### Phase 4: Apply to Top Fits (Rest of your time)

**Focus on 8+ fit score roles:**

For each high-fit job:
```bash
/generate-cv CompanyName
/generate-cover-letter CompanyName
```

**Time:** 30-45 minutes per application

---

## Complete Example: Saturday Morning Job Search

**Goal:** Find and apply to 3-5 high-fit roles

**Schedule (2 hours total):**

| Time | Activity | Details |
|------|----------|---------|
| **9:00-9:15** | Browse & Save | LinkedIn search, save 20 jobs to Downloads |
| **9:15-9:16** | Move Files | Move all .md files to `staging/manual-saves/` |
| **9:16-9:17** | Process | `python scripts/process_saved_jobs.py` |
| **9:17-9:32** | Analyze | `python scripts/bulk_analyze.py ...` |
| **9:32-9:40** | Review | Read `BULK-ANALYSIS-SUMMARY.md`, pick top 5 |
| **9:40-11:00** | Apply | Generate CVs + cover letters for 3-5 roles |

**Result:** 20 jobs analyzed, 3-5 applications submitted

---

## Tips for Efficiency

### Batch Saving (Recommended)

**Don't:**
- Save one job → Move to staging → Process → Repeat

**Do:**
- Save 10-20 jobs first (stay in browser)
- Move all files at once
- Process all at once

**Time saved:** 50% faster

### Browser Download Settings

**Optional:** Set your browser to ask where to save files:

**Chrome:**
1. Settings → Downloads
2. Check "Ask where to save each file before downloading"
3. When bookmarklet triggers download, choose `staging/manual-saves/` directly

**Firefox:**
1. Settings → General → Downloads
2. Select "Always ask you where to save files"

**Benefit:** Skip the manual move step

### Keyboard Shortcuts

**Speed up browsing:**
- `Ctrl+T`: New tab
- `Ctrl+W`: Close tab
- `Alt+Left`: Back to search results
- `Ctrl+Click`: Open job in new tab (review multiple before saving)

### Weekly Routine

**Monday morning (30 minutes):**
- Save 20-30 "past week" jobs
- Process and analyze
- Apply to 8+ fit roles throughout the week

**Result:** Steady pipeline without spending hours job hunting

---

## Troubleshooting

### "I forgot to move files from Downloads"

No problem! Files stay in Downloads until you move them. Just:
1. Sort Downloads by date
2. Find today's `.md` files (Company-Role.md format)
3. Move to `staging/manual-saves/`
4. Run processor

### "I accidentally moved the same files twice"

The processor will detect duplicates:
```
⏭️  Duplicates: 5
```

Nothing bad happens, just ignore the duplicate count.

### "Processor says 0 jobs found"

Check:
1. Files are in `staging/manual-saves/` (not Downloads)
2. Files are `.md` format (not `.txt` or `.html`)
3. File names match pattern: `Company-Role.md`

### "Job has 'Unknown Title' or 'Unknown Company'"

LinkedIn page wasn't fully loaded when you clicked bookmarklet. Either:
- Manually edit the `.md` file to fix
- Delete it and re-save the job

---

## Advanced: Semi-Automated Browser Setup

**For power users:**

1. Use browser automation extensions (e.g., "Download Router")
2. Set rule: Files matching `*.md` from `linkedin.com` → auto-save to `staging/manual-saves/`
3. Now bookmarklet saves directly to the right folder

**Compliance note:** This is still ToS-compliant because YOU are clicking the bookmarklet manually, just automating the file move.

---

## Comparison: Old vs New Workflow

### Old (Manual Copy/Paste)

```
1. Open job (30s)
2. Copy title, company, location (15s)
3. Open text editor (5s)
4. Paste and format (30s)
5. Copy job description (20s)
6. Paste (5s)
7. Save file with correct name (20s)
8. Repeat for next job

Time per job: ~2 minutes
Time for 20 jobs: 40 minutes
```

### New (Bookmarklet + Processor)

```
1. Open job (30s)
2. Click bookmarklet (1s)
3. Repeat for next job

After 20 jobs:
4. Move files from Downloads (30s)
5. Run processor (30s)

Time per job: ~31 seconds
Time for 20 jobs: 11 minutes
```

**Time saved:** 29 minutes per 20 jobs (73% faster)

---

## Next Steps

1. ✅ Install bookmarklet (if not done)
2. ✅ Save 5 jobs to test the workflow
3. ✅ Run processor and verify it works
4. ✅ Continue with normal bulk analysis

**You're all set!** The workflow is ToS-compliant, fast, and integrates perfectly with your existing CV/cover letter system.

---

**Questions?** See:
- `BOOKMARKLET-INSTALL.md` - Installation troubleshooting
- `BOOKMARKLET-GUIDE.md` - Complete reference
- `deprecated/DEPRECATION-NOTICE.md` - Why we sunset automation
