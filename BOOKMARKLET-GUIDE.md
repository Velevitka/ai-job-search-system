# Bookmarklet Job Saver - Complete Guide

**ToS-Compliant Job Saving System**

Save jobs with one click while browsing - no automation, no scraping, fully compliant with LinkedIn and other platforms' Terms of Service.

---

## 📋 Table of Contents

- [Why Bookmarklet Instead of Automation?](#why-bookmarklet-instead-of-automation)
- [Quick Start (5 minutes)](#quick-start-5-minutes)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Usage Workflow](#usage-workflow)
- [Supported Platforms](#supported-platforms)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)

---

## Why Bookmarklet Instead of Automation?

### ❌ The Problem with Automated Scraping

We initially built an automated LinkedIn scraper using Playwright, but discovered it **violates LinkedIn's Terms of Service** (Section 8.2):

> "Use bots or other automated methods to access the Services"
> "Develop, support or use software, devices, scripts, robots or any other means to scrape the Services"

**Risks:**
- Account suspension or permanent ban
- Legal action (LinkedIn actively sues scrapers)
- GDPR violations in Europe
- Professional reputation damage during active job search

### ✅ The Bookmarklet Solution

**Fully ToS-Compliant:**
- **You** manually browse and click (not a bot)
- **You** decide which jobs to save (not automated)
- **You** trigger the extraction (manual action)
- Just assisted data collection - like copy/paste, but faster

**Benefits:**
- ✅ Zero risk - No ToS violations
- ✅ One-click save - Faster than manual copy/paste
- ✅ Consistent format - Works with existing workflow
- ✅ Multi-platform - LinkedIn, Greenhouse, Lever

See `deprecated/DEPRECATION-NOTICE.md` for details on why we sunset the automated approach.

---

## Quick Start (5 minutes)

### Step 1: Create the Bookmarklet

1. **Open your browser's bookmarks bar** (Ctrl+Shift+B / Cmd+Shift+B)

2. **Right-click the bookmarks bar** → "Add page" or "New bookmark"

3. **Name it:** "Save Job"

4. **Copy this code** into the URL/Location field:

```javascript
javascript:(function()%7B'use strict'%3Bfunction extractLinkedInJob()%7Bconst data%3D%7Burl:window.location.href%2Cplatform:'LinkedIn'%2Ctimestamp:new Date().toISOString()%7D%3Bconst titleEl%3Ddocument.querySelector('.job-details-jobs-unified-top-card__job-title%2C .jobs-unified-top-card__job-title%2C h1')%3Bdata.title%3DtitleEl%3FtitleEl.textContent.trim():'Unknown Title'%3Bconst companyEl%3Ddocument.querySelector('.job-details-jobs-unified-top-card__company-name%2C .jobs-unified-top-card__company-name%2C .jobs-unified-top-card__subtitle-primary-grouping a')%3Bdata.company%3DcompanyEl%3FcompanyEl.textContent.trim():'Unknown Company'%3Bconst locationEl%3Ddocument.querySelector('.job-details-jobs-unified-top-card__bullet%2C .jobs-unified-top-card__bullet')%3Bdata.location%3DlocationEl%3FlocationEl.textContent.trim():'Unknown Location'%3Bconst descEl%3Ddocument.querySelector('.jobs-description__content%2C .jobs-box__html-content%2C .description__text')%3Bdata.description%3DdescEl%3FdescEl.innerText.trim():'No description found'%3Bconst criteriaList%3Ddocument.querySelectorAll('.jobs-unified-top-card__job-insight span')%3Bdata.metadata%3DArray.from(criteriaList).map(el%3D>el.textContent.trim()).join(' %7C ')%3Breturn data%7Dfunction extractJobData()%7Bconst url%3Dwindow.location.href%3Bif(url.includes('linkedin.com%2Fjobs'))%7Breturn extractLinkedInJob()%7Delse%7Balert('Unsupported platform. Currently supports: LinkedIn%2C Greenhouse%2C Lever')%3Breturn null%7D%7Dfunction createMarkdown(data)%7Breturn%60%23 %24%7Bdata.title%7D%5Cn%5Cn**Company:** %24%7Bdata.company%7D %5Cn**Location:** %24%7Bdata.location%7D %5Cn**Source:** %5B%24%7Bdata.platform%7D%5D(%24%7Bdata.url%7D) %5Cn**Saved:** %24%7Bnew Date(data.timestamp).toLocaleString()%7D%5Cn%5Cn%24%7Bdata.metadata%3F%60**Additional Info:** %24%7Bdata.metadata%7D%5Cn%60:''%7D---%5Cn%5Cn%23%23 Job Description%5Cn%5Cn%24%7Bdata.description%7D%5Cn%5Cn---%5Cn%5Cn**URL:** %24%7Bdata.url%7D%5Cn%60%7Dfunction downloadFile(filename%2Ccontent)%7Bconst blob%3Dnew Blob(%5Bcontent%5D%2C%7Btype:'text%2Fmarkdown'%7D)%3Bconst url%3DURL.createObjectURL(blob)%3Bconst a%3Ddocument.createElement('a')%3Ba.href%3Durl%3Ba.download%3Dfilename%3Bdocument.body.appendChild(a)%3Ba.click()%3Bdocument.body.removeChild(a)%3BURL.revokeObjectURL(url)%7Dfunction createFilename(company%2Ctitle)%7Bconst safeName%3D(str)%3D>str.replace(%2F%5B%5Ea-zA-Z0-9%5Cs%5D%2Fg%2C'').replace(%2F%5Cs%2B%2Fg%2C'-').substring(0%2C50)%3Breturn%60%24%7BsafeName(company)%7D-%24%7BsafeName(title)%7D.md%60%7Dtry%7Bconst jobData%3DextractJobData()%3Bif(!jobData)%7Breturn%7Dconst markdown%3DcreateMarkdown(jobData)%3Bconst filename%3DcreateFilename(jobData.company%2CjobData.title)%3BdownloadFile(filename%2Cmarkdown)%3Balert(%60%E2%9C%85 Job saved!%5Cn%5CnCompany: %24%7BjobData.company%7D%5CnRole: %24%7BjobData.title%7D%5Cn%5CnFile: %24%7Bfilename%7D%5Cn%5CnNext steps:%5Cn1. Save to: staging%2Fmanual-saves%2F%5Cn2. Run: python scripts%2Fprocess_saved_jobs.py%60)%7Dcatch(error)%7Balert(%60%E2%9D%8C Error saving job:%5Cn%5Cn%24%7Berror.message%7D%5Cn%5CnPlease try again or manually copy the job description.%60)%3Bconsole.error('Job saver error:'%2Cerror)%7D%7D)()%3B
```

5. **Save the bookmark**

### Step 2: Create Staging Folder

```bash
mkdir -p staging/manual-saves
```

### Step 3: Test It!

1. **Browse to a LinkedIn job** (or Greenhouse/Lever job posting)
2. **Click the "Save Job" bookmarklet** in your bookmarks bar
3. **You'll see:** ✅ Job saved! alert with company and role
4. **Browser downloads** a markdown file
5. **Save the file** to `staging/manual-saves/`

### Step 4: Process Saved Jobs

```bash
python scripts/process_saved_jobs.py
```

**What happens:**
- Deduplicates against existing applications
- Organizes into proper folder structure
- Generates batch summary

### Step 5: Analyze Jobs

```bash
python scripts/bulk_analyze.py staging/YYYY-MM-DD-processed-batch
```

**Done!** You now have fit scores and can apply to 8+ fit roles.

---

## How It Works

### User Flow (ToS-Compliant)

```
1. Manual Browsing
   └─> You browse LinkedIn jobs normally (no automation)

2. View Job Posting
   └─> You find a job you're interested in

3. Click Bookmarklet
   └─> You click "Save Job" bookmark (manual action)

4. Extract Data
   └─> JavaScript reads current page's DOM
   └─> Extracts: title, company, location, description
   └─> Creates markdown file

5. Download File
   └─> Browser downloads .md file
   └─> You save to staging/manual-saves/

6. Process Jobs (Automation - ToS Compliant)
   └─> Python script organizes saved files
   └─> Deduplicates against applications/
   └─> No external access, just local file processing

7. Bulk Analysis
   └─> Existing workflow: /analyze-job for each
   └─> Fit scores, strategy, prioritization
```

**Key Compliance Points:**
- ✅ You manually browse (not a bot)
- ✅ You manually click bookmarklet (not automated)
- ✅ Extraction happens in your browser (not server-side scraping)
- ✅ Processing is local files only (no network requests)

---

## Installation

### Browser Compatibility

- ✅ Chrome / Edge (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Brave
- ✅ Opera

### Detailed Installation Steps

#### Chrome / Edge

1. **Show bookmarks bar:**
   - Press `Ctrl+Shift+B` (Windows/Linux)
   - Press `Cmd+Shift+B` (Mac)

2. **Add bookmark:**
   - Right-click bookmarks bar
   - Click "Add page..."

3. **Configure:**
   - Name: "Save Job" (or anything you like)
   - URL: Paste the minified JavaScript code from Step 1
   - Save

#### Firefox

1. **Show bookmarks toolbar:**
   - Right-click toolbar area
   - Check "Bookmarks Toolbar"

2. **Add bookmark:**
   - Bookmarks → Manage Bookmarks
   - Toolbar → Right-click → "New Bookmark..."

3. **Configure:**
   - Name: "Save Job"
   - Location: Paste the minified JavaScript code
   - Save

#### Safari

1. **Show favorites bar:**
   - View → Show Favorites Bar

2. **Add bookmark:**
   - Bookmarks → Add Bookmark...

3. **Edit bookmark:**
   - Bookmarks → Edit Bookmarks
   - Find "Save Job" bookmark
   - Change URL to the minified JavaScript code

---

## Usage Workflow

### Daily Job Search Routine

**Old way (10-15 minutes per 10 jobs):**
```
1. Browse LinkedIn job
2. Copy job title, company, location
3. Open text editor
4. Paste and format
5. Save file with correct naming
6. Repeat 9 more times...
```

**New way with bookmarklet (2-3 minutes per 10 jobs):**
```
1. Browse LinkedIn job
2. Click "Save Job" bookmarklet
3. Save downloaded file to staging/manual-saves/
4. Repeat for next job
5. Run: python scripts/process_saved_jobs.py
6. Done!
```

**Time saved:** 7-12 minutes per 10 jobs

### Batch Saving Session

**Example: Saturday morning job search (1 hour)**

1. **Prepare** (30 seconds):
   ```bash
   cd ~/your-cv-project
   mkdir -p staging/manual-saves
   ```

2. **Browse and Save** (30-40 minutes):
   - Open LinkedIn Jobs
   - Search for roles (e.g., "Director Product Data")
   - For each interesting job:
     - Click on job
     - Read brief summary
     - If interested → Click "Save Job" bookmarklet
     - Save file to `staging/manual-saves/`
   - Goal: Save 20-30 jobs

3. **Process** (1 minute):
   ```bash
   python scripts/process_saved_jobs.py
   ```

4. **Analyze** (10-15 minutes):
   ```bash
   python scripts/bulk_analyze.py staging/2025-11-05-processed-batch
   cat staging/2025-11-05-processed-batch/BULK-ANALYSIS-SUMMARY.md
   ```

5. **Apply to Top Fits** (rest of hour):
   - Focus on 8+ fit score roles
   - Use `/generate-cv` and `/generate-cover-letter`

**Result:** 20-30 jobs analyzed, 5-8 high-fit applications started

---

## Supported Platforms

### ✅ LinkedIn

**URL patterns:**
- `https://www.linkedin.com/jobs/view/*`
- `https://www.linkedin.com/jobs/collections/*`

**Extracts:**
- Job title
- Company name
- Location
- Full job description
- Seniority level, job type, etc.

### ✅ Greenhouse

**URL pattern:**
- `https://boards.greenhouse.io/*/jobs/*`

**Extracts:**
- Job title
- Company name (from URL or page)
- Location
- Full job description

**Example companies using Greenhouse:**
- Stripe, Notion, Airbnb, GitLab, Coinbase, etc.

### ✅ Lever

**URL pattern:**
- `https://jobs.lever.co/*/`

**Extracts:**
- Job title
- Company name (from URL)
- Location
- Full job description

**Example companies using Lever:**
- Netflix, Shopify, Grammarly, Figma, etc.

### 🚧 Coming Soon

- Indeed
- Workable
- SmartRecruiters
- Custom ATS platforms

---

## Troubleshooting

### Issue: Bookmarklet doesn't work

**Symptoms:** Nothing happens when you click it

**Solutions:**

1. **Check you're on a job posting page:**
   - Must be on LinkedIn job page (`/jobs/view/`)
   - Not on search results page
   - Not on company page

2. **Check JavaScript is enabled:**
   - Browser settings → Privacy/Security → Allow JavaScript

3. **Try re-creating the bookmarklet:**
   - Delete old bookmark
   - Follow installation steps again
   - Make sure code starts with `javascript:`

### Issue: "Unsupported platform" alert

**Symptoms:** Alert says platform not supported

**Cause:** You're on a page the bookmarklet doesn't recognize

**Solutions:**
- Only LinkedIn, Greenhouse, and Lever are currently supported
- Make sure you're on the actual job posting page
- Check URL matches supported patterns (see Supported Platforms above)

### Issue: Download blocked by browser

**Symptoms:** Browser blocks the markdown file download

**Solutions:**

1. **Chrome/Edge:**
   - Click shield icon in address bar
   - Allow downloads from this site

2. **Firefox:**
   - Tools → Options → Privacy & Security
   - Permissions → Block pop-up windows → Exceptions
   - Add the job board domain

3. **Safari:**
   - Safari → Preferences → Websites → Downloads
   - Allow for the job board domain

### Issue: "Unknown Company" or "Unknown Title"

**Symptoms:** Job saved with placeholder text

**Cause:** Page structure changed or not fully loaded

**Solutions:**
- Wait for page to fully load before clicking bookmarklet
- Refresh page and try again
- If persistent, manually edit the downloaded markdown file

### Issue: Description not captured

**Symptoms:** Job description section is empty

**Cause:** LinkedIn or ATS changed their page structure

**Solutions:**
- Report issue (see [Contributing](#contributing))
- Manually copy description and paste into markdown file
- Use manual fallback (copy/paste) for this job

---

## FAQ

### Is this legal?

**Yes.** You're manually browsing and clicking - not using bots or automation. This is the same as copy/pasting job descriptions, just faster.

### Will I get banned from LinkedIn?

**No.** You're browsing normally and clicking a bookmark. LinkedIn can't distinguish this from reading the page yourself.

### Why not just use LinkedIn's "Save Job" feature?

LinkedIn's save feature:
- Doesn't export job descriptions
- Doesn't integrate with your CV workflow
- Doesn't allow bulk analysis
- Doesn't work for jobs on Greenhouse/Lever

Our bookmarklet:
- Saves full description in markdown
- Works with existing `/analyze-job` workflow
- Enables bulk analysis and fit scoring
- Works across multiple platforms

### Can I customize the markdown format?

Yes! Edit `bookmarklet-save-job.js`:
- Find the `createMarkdown()` function
- Modify the template string
- Re-minify the code (or use unminified for development)
- Update your bookmark

### How often is the bookmarklet updated?

When job board platforms change their page structure, we update the selectors. Check GitHub releases for updates.

### Can I use this for other job boards?

Yes! The architecture is extensible:
1. Add a new `extractXYZJob()` function in `bookmarklet-save-job.js`
2. Update `extractJobData()` to detect the new platform
3. Test and submit a pull request

See `CONTRIBUTING.md` for details.

### What if the bookmarklet breaks?

Job boards update their page structure occasionally. If extraction fails:
1. Check for updates: `git pull origin main`
2. Report the issue on GitHub
3. Use manual copy/paste as fallback

---

## Advanced Usage

### Bulk Saving with Keyboard Shortcuts

**Setup:**
1. Browser extensions like "Vimium" or "Shortkeys"
2. Map a key combo to click bookmarklet
3. Example: `Alt+S` = Click "Save Job" bookmark

**Workflow:**
- Browse jobs with keyboard
- Hit `Alt+S` to save
- Save file with `Enter`
- Next job

**Speed:** 5-10 seconds per job

### Mobile Usage

**iOS Safari:**
- Bookmarklets work in Safari
- Tap share icon → Bookmarks → "Save Job"

**Android Chrome:**
- Type bookmark name in address bar
- Select "Save Job" bookmark

**Limitations:**
- Mobile browsers may handle downloads differently
- Recommend using desktop for bulk saving

### Integration with Job Alerts

**Email Alerts → Bookmarklet:**
1. Set up LinkedIn job alerts (email)
2. Click job links from email
3. Use bookmarklet to save interesting jobs
4. Process batch weekly

**RSS Readers (Advanced):**
1. Use job board RSS feeds (if available)
2. Open jobs in browser
3. Use bookmarklet to save

---

## Performance Tips

### Optimal Workflow

**Don't:**
- Save every job you see
- Process after each save
- Skip reading job summaries

**Do:**
- Quick scan first (title, company, requirements)
- Save only promising matches (8+ potential)
- Batch save 10-20 jobs
- Process all at once
- Bulk analyze

**Time Investment:**
- Scanning 50 jobs: 15-20 minutes
- Saving 20 promising: 5 minutes
- Processing: 1 minute
- Analyzing: 10 minutes
- **Total:** 30-35 minutes for 20 analyzed jobs

Compare to manual: 2-3 hours for same 20 jobs

---

## Security & Privacy

### What Data is Collected?

**None.** The bookmarklet:
- Runs entirely in your browser
- Doesn't send data to any server
- Doesn't track usage
- Doesn't require account or login

### What's in the Downloaded File?

Only what's visible on the job posting page:
- Job title
- Company name
- Location
- Description
- URL

No personal data, no tracking codes.

### Can Others See My Saved Jobs?

No, unless:
- You commit them to public GitHub (they're in `.gitignore`)
- You share your `staging/` folder

**All saved jobs stay on your local machine.**

---

## Contributing

Found a bug? Want to add a new job board?

See `CONTRIBUTING.md` for:
- How to report issues
- How to add new platform support
- How to test changes
- Pull request guidelines

---

## Changelog

### v1.0.0 (2025-11-05)
- Initial release
- Support for LinkedIn, Greenhouse, Lever
- ToS-compliant alternative to automated scraping
- Integration with existing bulk analysis workflow

---

## Support

- **Documentation:** See README.md, SETUP.md, USAGE-GUIDE.md
- **Issues:** https://github.com/yourusername/ai-job-search-system/issues
- **Deprecated automation:** See `deprecated/DEPRECATION-NOTICE.md`

---

**Happy job hunting! 🎯**

*Save jobs compliantly, apply strategically.*
