# Testing Job Discovery with Persistent Login

Quick walkthrough for testing the updated job discovery script with proper LinkedIn login handling.

---

## What's Fixed

✅ **Persistent browser session** - Log in once, stay logged in forever
✅ **Manual login support** - Script pauses and waits for you to log in
✅ **No more refresh issues** - Browser won't navigate away during login
✅ **Session saved locally** - Stored in `.browser_data/` (excluded from git)

---

## Step 1: First Run (One-Time Login)

Run the script to log in and save your session:

```bash
python scripts/job_discovery.py --keywords "Director Product Data Platform" --location "London, United Kingdom"
```

**What happens:**

1. Browser window opens
2. Script checks if you're logged in
3. If not logged in, you'll see:

```
🔐 Checking LinkedIn login status...

  ⚠️ Not logged in to LinkedIn

================================================================================
MANUAL LOGIN REQUIRED
================================================================================

The browser window is now showing LinkedIn's login page.

Please:
  1. Log in to your LinkedIn account in the browser window
  2. Complete any 2FA/security checks if prompted
  3. Wait until you see your LinkedIn feed
  4. Then come back here and press ENTER to continue

The script will pause and wait for you...
================================================================================

Press ENTER after you've logged in to LinkedIn...
```

4. **In the browser window:**
   - Enter your LinkedIn email/password
   - Complete 2FA if prompted
   - Wait until you see your feed

5. **Back in terminal:**
   - Press ENTER
   - Script verifies login successful
   - Session saved to `.browser_data/`

6. Script proceeds with job search

---

## Step 2: Subsequent Runs (Already Logged In)

Next time you run the script:

```bash
python scripts/job_discovery.py --keywords "VP Product" --location "Remote, UK"
```

**What happens:**

1. Browser opens
2. Script checks login status
3. Sees you're already logged in: ✅
4. Proceeds directly to job search
5. **No manual login needed!**

---

## Step 3: Headless Mode (After First Login)

Once you've logged in once, you can run headless (no browser window):

```bash
python scripts/job_discovery.py --keywords "Head of Product" --location "London" --headless
```

**Perfect for:**
- Scheduled runs
- Background monitoring
- Faster execution

---

## Troubleshooting

### "Session expired" or "Login verification failed"

LinkedIn logged you out. Just run again and log in:

```bash
python scripts/job_discovery.py --keywords "Test" --location "London"
# Browser opens → Log in → Press ENTER
```

### "Browser keeps refreshing"

That's the old bug - **FIXED** in the new version!

The updated script:
1. Checks login status first
2. Pauses at login page (doesn't navigate away)
3. Waits for your ENTER confirmation
4. Only then proceeds to job search

### Want to force re-login?

Delete the saved session:

```bash
# Windows
rmdir /s .browser_data

# Mac/Linux
rm -rf .browser_data
```

Next run will require login again.

---

## Session Storage

Your LinkedIn session is saved in:
```
.browser_data/
├── Default/
│   ├── Cookies
│   ├── Local Storage/
│   └── ... (browser profile)
```

**Security:**
- ✅ Excluded from git (in `.gitignore`)
- ✅ Stays on your local machine
- ✅ Same as your regular browser data

---

## Testing Checklist

- [ ] Run script for first time
- [ ] Log in to LinkedIn when prompted
- [ ] Press ENTER after seeing LinkedIn feed
- [ ] Verify "Login successful!" message
- [ ] Let script complete job search
- [ ] Run script again - should skip login
- [ ] Try headless mode after successful login
- [ ] Check that `.browser_data/` folder was created
- [ ] Verify jobs saved to `staging/YYYY-MM-DD-discovery-batch/`

---

## Full Test Command

```bash
# First run (with login)
python scripts/job_discovery.py \
  --keywords "Director Product Data Platform" \
  --location "London, United Kingdom" \
  --date past_week

# Second run (already logged in, headless)
python scripts/job_discovery.py \
  --keywords "Head of Product Growth" \
  --location "London, United Kingdom" \
  --date past_week \
  --headless

# Check results
dir staging\2025-11-05-discovery-batch
```

---

## Expected Output (First Run)

```
================================================================================
🤖 LinkedIn Job Discovery Automation
================================================================================

🔐 Checking LinkedIn login status...

  ⚠️ Not logged in to LinkedIn

[... manual login prompt ...]

Press ENTER after you've logged in to LinkedIn... [WAITING]

[You press ENTER]

  🔍 Verifying login...
  ✅ Login successful! Session will be saved for future runs.
  💾 Session saved to: C:\Users\...\4. CV\.browser_data
  ℹ️  Next time you run this script, you won't need to log in again!

🔍 Searching LinkedIn Jobs:
  Keywords: Director Product Data Platform
  Location: London, United Kingdom
  Date: past_week
  🌐 Loading: https://www.linkedin.com/jobs/search/?keywords=...
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

[... continues for all jobs ...]

✅ Successfully scraped 18/18 jobs
📁 Saved to: staging/2025-11-05-discovery-batch
📄 Summary saved: DISCOVERY-SUMMARY.json

🎯 Next Steps:
1. Run bulk analysis: python scripts/bulk_analyze.py staging/2025-11-05-discovery-batch
2. Review results in: staging/2025-11-05-discovery-batch/BULK-ANALYSIS-SUMMARY.md
3. Apply to 8+ fit score roles using /generate-cv and /generate-cover-letter

✅ Done!
```

---

## Next: Bulk Analysis

After jobs are discovered:

```bash
# Analyze all discovered jobs
python scripts/bulk_analyze.py staging/2025-11-05-discovery-batch

# Review fit scores
cat staging/2025-11-05-discovery-batch/BULK-ANALYSIS-SUMMARY.md

# Apply to top fits
# For each 8+ fit job, run:
/generate-cv CompanyName
/generate-cover-letter CompanyName
```

---

## Ready for Scheduling

Once manual login works:

**See `DEPLOYMENT-GUIDE.md` for:**
- Windows Task Scheduler setup (local, free)
- GitHub Actions (cloud, free)
- Google Cloud (cloud, free tier)
- Cost comparisons

---

**You're all set! The login issue is fixed. Time to test it!** 🚀
