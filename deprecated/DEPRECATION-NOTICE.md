# Deprecation Notice: Automated LinkedIn Scraping

**Date:** 2025-11-05
**Reason:** LinkedIn Terms of Service Violation
**Status:** SUNSET - Do Not Use

---

## ⚠️ Why These Files Are Deprecated

The automated LinkedIn job discovery system in this folder **violates LinkedIn's Terms of Service** (Section 8.2) and has been sunset.

### Specific ToS Violations

LinkedIn's User Agreement Section 8.2 explicitly prohibits:

1. **Automated Access**: "Use bots or other automated methods to access the Services"
2. **Scraping**: "Develop, support or use software, devices, scripts, robots or any other means to scrape the Services or otherwise copy profiles and other data"
3. **Bypass Controls**: "Bypass or circumvent any access controls or use limits of the Service"

### Risks of Using This Code

- ❌ **Account suspension** or permanent ban from LinkedIn
- ❌ **Legal action** - LinkedIn actively sues scrapers
- ❌ **GDPR violations** in Europe for collecting personal data
- ❌ **Professional reputation damage** if flagged during active job search

### What Was Deprecated

- `scripts/job_discovery.py` - Playwright-based LinkedIn scraper
- `scripts/scheduled_monitor.py` - Scheduled automation wrapper
- `QUICKSTART-JOB-DISCOVERY.md` - User guide
- `DEPLOYMENT-GUIDE.md` - Deployment options (local, cloud)
- `TESTING-LOGIN.md` - Testing guide

---

## ✅ Compliant Alternative: Hybrid Bookmarklet System

We've replaced the automated scraper with a **ToS-compliant hybrid approach**:

### How It Works

1. **Manual Browsing** - You browse LinkedIn jobs normally (no automation)
2. **Bookmarklet Click** - While viewing a job, click "Save Job" bookmarklet in your browser
3. **Auto-Extract** - JavaScript extracts job data from the current page
4. **Local Save** - Job saved to your staging folder
5. **Auto-Process** - Python script deduplicates and organizes saved jobs

### Key Benefits

- ✅ **Fully ToS-compliant** - You're manually browsing, just assisted saving
- ✅ **Zero risk** - No automation, no scraping, no bot detection
- ✅ **Still saves time** - One-click save vs. copy/paste
- ✅ **Same workflow** - Integrates with existing bulk analysis

### Getting Started

See the new documentation:
- `BOOKMARKLET-GUIDE.md` - How to install and use the bookmarklet
- `scripts/process_saved_jobs.py` - Job processing automation

---

## Historical Context (Nov 2025)

This automated scraper was built to solve a real problem: manual job searching is time-consuming. However, after reviewing LinkedIn's Terms of Service, we discovered it violated multiple provisions.

**Lesson learned**: Always verify ToS compliance before building automation for third-party platforms. The hybrid bookmarklet approach achieves similar time savings while staying compliant.

---

## For Reference Only

These files are preserved for reference but **should not be used**:

```
deprecated/
├── DEPRECATION-NOTICE.md           # This file
├── job_discovery.py                # LinkedIn scraper (DO NOT USE)
├── scheduled_monitor.py            # Scheduled automation (DO NOT USE)
├── QUICKSTART-JOB-DISCOVERY.md    # Old guide
├── DEPLOYMENT-GUIDE.md            # Deployment options
└── TESTING-LOGIN.md               # Testing guide
```

**If you use these files, you accept full responsibility for any LinkedIn ToS violations and consequences.**

---

## Contact

Questions about the deprecation or the new bookmarklet system? See:
- Main README.md
- BOOKMARKLET-GUIDE.md
- GitHub Issues: https://github.com/yourusername/ai-job-search-system/issues
