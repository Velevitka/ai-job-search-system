# Quick Start: Automated Job Discovery

**Goal:** Automate finding jobs on LinkedIn instead of manual searching.

## Installation (One-time setup)

```bash
# 1. Install Python dependencies
pip install playwright

# 2. Install Chromium browser
python -m playwright install chromium

# Done! Takes ~2 minutes
```

## Basic Usage

### Option 1: Quick Test (Default Search)

```bash
python scripts/job_discovery.py
```

This will search for "Director Product Data Platform" in London (default).

### Option 2: Custom Search

```bash
python scripts/job_discovery.py \
  --keywords "Head of Product Growth" \
  --location "London, United Kingdom" \
  --date past_week
```

### Option 3: Run in Background (Headless)

```bash
python scripts/job_discovery.py --headless
```

## What It Does

1. **Searches LinkedIn** with your criteria
2. **Scrolls** to load all results
3. **Checks for duplicates** against your existing applications
4. **Scrapes full job descriptions** for new jobs
5. **Saves to** `staging/YYYY-MM-DD-discovery-batch/`
6. **Generates summary** with metadata

## Example Output

```
🔍 Searching LinkedIn Jobs:
  Keywords: Director Product Data Platform
  Location: London, United Kingdom
  Date: past_week
  ⏬ Scrolling to load all job cards...
  ✓ Found 23 job cards

📊 Total jobs discovered: 23
✅ New jobs: 18
⏭️  Duplicates (already tracked): 5

📥 Scraping full job descriptions for 18 new jobs...

  [1/18] Spotify - Director Product Growth
    📄 Scraping: https://linkedin.com/jobs/view/...
    ✓ Scraped 2847 characters
    ✅ Saved to: Spotify-DirectorProductGrowth/

  [2/18] Monzo - Head of Data Platform
    📄 Scraping: https://linkedin.com/jobs/view/...
    ✓ Scraped 3251 characters
    ✅ Saved to: Monzo-HeadOfDataPlatform/

...

✅ Successfully scraped 18/18 jobs
📁 Saved to: staging/2025-11-05-discovery-batch
📄 Summary saved: DISCOVERY-SUMMARY.json

🎯 Next Steps:
1. Run bulk analysis: python scripts/bulk_analyze.py staging/2025-11-05-discovery-batch
2. Review results in: staging/2025-11-05-discovery-batch/BULK-ANALYSIS-SUMMARY.md
3. Apply to 8+ fit score roles using /generate-cv and /generate-cover-letter
```

## Next Steps

After jobs are discovered:

```bash
# 1. Analyze all discovered jobs
python scripts/bulk_analyze.py staging/2025-11-05-discovery-batch

# 2. Review the summary (sorted by fit score)
cat staging/2025-11-05-discovery-batch/BULK-ANALYSIS-SUMMARY.md

# 3. Apply to top fits
# For each 8+ fit job:
/generate-cv CompanyName
/generate-cover-letter CompanyName
```

## Typical Workflow

**Old way (manual):**
1. Search LinkedIn Jobs manually (30 min)
2. Click through 20-30 jobs (60 min)
3. Copy/paste job descriptions (30 min)
4. **Total: 2 hours**

**New way (automated):**
1. Run: `python scripts/job_discovery.py` (5 min to run, mostly automated)
2. Review summary of fit scores (10 min)
3. Apply to top fits only
4. **Total: 15-20 minutes**

**Time saved: ~90-100 minutes per search session**

## Customization

Edit search parameters in the script or use command-line arguments:

```bash
# Multiple searches in one run (edit script)
searches = [
    {'keywords': 'Director Product Data Platform', 'location': 'London'},
    {'keywords': 'Head of Product Growth', 'location': 'London'},
    {'keywords': 'VP Product', 'location': 'Remote, UK'}
]
```

## Troubleshooting

### "playwright not found"
```bash
pip install playwright
python -m playwright install chromium
```

### "No jobs found"
- LinkedIn might show login page - try running without `--headless` first
- Check search URL is valid
- Try broader keywords

### "Scraping failed"
- LinkedIn changed selectors - report issue
- Network timeout - try again
- Rate limiting - add delays

## Future Enhancements

**Phase 2 (Next Week):**
- Scheduled runs (daily at 9am)
- Email alerts for 8+ fit jobs
- Track search effectiveness

**Phase 3 (Week 3):**
- Add Greenhouse/Lever scrapers
- Monitor specific company boards
- Multi-platform aggregation

**Future:**
- Scrape from company career pages (not LinkedIn)
- Auto-apply to Perfect Fits (10/10)
- Interview scheduling integration
