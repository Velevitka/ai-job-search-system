# Quick Bookmarklet Installation Guide

**2 Methods: Browser Bookmark (recommended) or Console Test**

---

## Method 1: Browser Bookmark (Recommended for Daily Use)

### Step 1: Copy the Bookmarklet Code

Copy this ENTIRE code block (click the copy button):

```
javascript:(function(){'use strict';function extractLinkedInJob(){const data={url:window.location.href,platform:'LinkedIn',timestamp:new Date().toISOString()};const titleEl=document.querySelector('.job-details-jobs-unified-top-card__job-title, .jobs-unified-top-card__job-title, h1');data.title=titleEl?titleEl.textContent.trim():'Unknown Title';const companyEl=document.querySelector('.job-details-jobs-unified-top-card__company-name, .jobs-unified-top-card__company-name, .jobs-unified-top-card__subtitle-primary-grouping a');data.company=companyEl?companyEl.textContent.trim():'Unknown Company';const locationEl=document.querySelector('.job-details-jobs-unified-top-card__bullet, .jobs-unified-top-card__bullet');data.location=locationEl?locationEl.textContent.trim():'Unknown Location';const descEl=document.querySelector('.jobs-description__content, .jobs-box__html-content, .description__text');data.description=descEl?descEl.innerText.trim():'No description found';const criteriaList=document.querySelectorAll('.jobs-unified-top-card__job-insight span');data.metadata=Array.from(criteriaList).map(el=>el.textContent.trim()).join(' | ');return data}function extractJobData(){const url=window.location.href;if(url.includes('linkedin.com/jobs')){return extractLinkedInJob()}else{alert('Unsupported platform. Currently supports: LinkedIn');return null}}function createMarkdown(data){return`# ${data.title}\n\n**Company:** ${data.company}\n**Location:** ${data.location}\n**Source:** [${data.platform}](${data.url})\n**Saved:** ${new Date(data.timestamp).toLocaleString()}\n\n${data.metadata?`**Additional Info:** ${data.metadata}\n`:''---\n\n## Job Description\n\n${data.description}\n\n---\n\n**URL:** ${data.url}\n`}function downloadFile(filename,content){const blob=new Blob([content],{type:'text/markdown'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=filename;document.body.appendChild(a);a.click();document.body.removeChild(a);URL.revokeObjectURL(url)}function createFilename(company,title){const safeName=(str)=>str.replace(/[^a-zA-Z0-9\s]/g,'').replace(/\s+/g,'-').substring(0,50);return`${safeName(company)}-${safeName(title)}.md`}try{const jobData=extractJobData();if(!jobData){return}const markdown=createMarkdown(jobData);const filename=createFilename(jobData.company,jobData.title);downloadFile(filename,markdown);alert(`✅ Job saved!\n\nCompany: ${jobData.company}\nRole: ${jobData.title}\n\nFile: ${filename}\n\nNext steps:\n1. Save to: staging/manual-saves/\n2. Run: python scripts/process_saved_jobs.py`)}catch(error){alert(`❌ Error saving job:\n\n${error.message}\n\nPlease try again or manually copy the job description.`);console.error('Job saver error:',error)}})();
```

### Step 2: Create a Bookmark

**Chrome/Edge:**
1. Press `Ctrl+Shift+B` to show bookmarks bar
2. Right-click on bookmarks bar → "Add page..."
3. Name: `Save Job`
4. URL: Paste the code you copied above
5. Click "Save"

**Firefox:**
1. Press `Ctrl+Shift+B` to show bookmarks toolbar
2. Bookmarks → Manage Bookmarks
3. Toolbar → Right-click → "New Bookmark..."
4. Name: `Save Job`
5. Location: Paste the code you copied above
6. Click "Save"

### Step 3: Test It

1. Go to any LinkedIn job posting (e.g., https://www.linkedin.com/jobs/view/...)
2. Click the "Save Job" bookmark in your bookmarks bar
3. You should see an alert: "✅ Job saved!"
4. A markdown file should download
5. Save it to `staging/manual-saves/`

---

## Method 2: Console Test (For Testing Before Installing)

### Step 1: Open Browser Console

1. Go to a LinkedIn job posting
2. Press `F12` (or right-click → Inspect)
3. Click the "Console" tab

### Step 2: Paste Test Code

Copy and paste the code from `bookmarklet-save-job-console-test.js` into the console and press Enter.

**OR** paste this:

```javascript
(function() {
    'use strict';
    function extractLinkedInJob() {
        const data = {
            url: window.location.href,
            platform: 'LinkedIn',
            timestamp: new Date().toISOString()
        };
        const titleEl = document.querySelector('.job-details-jobs-unified-top-card__job-title, .jobs-unified-top-card__job-title, h1');
        data.title = titleEl ? titleEl.textContent.trim() : 'Unknown Title';
        const companyEl = document.querySelector('.job-details-jobs-unified-top-card__company-name, .jobs-unified-top-card__company-name, .jobs-unified-top-card__subtitle-primary-grouping a');
        data.company = companyEl ? companyEl.textContent.trim() : 'Unknown Company';
        const locationEl = document.querySelector('.job-details-jobs-unified-top-card__bullet, .jobs-unified-top-card__bullet');
        data.location = locationEl ? locationEl.textContent.trim() : 'Unknown Location';
        const descEl = document.querySelector('.jobs-description__content, .jobs-box__html-content, .description__text');
        data.description = descEl ? descEl.innerText.trim() : 'No description found';
        const criteriaList = document.querySelectorAll('.jobs-unified-top-card__job-insight span');
        data.metadata = Array.from(criteriaList).map(el => el.textContent.trim()).join(' | ');
        return data;
    }
    function extractJobData() {
        const url = window.location.href;
        if (url.includes('linkedin.com/jobs')) {
            return extractLinkedInJob();
        } else {
            alert('Not on a LinkedIn job page');
            return null;
        }
    }
    function createMarkdown(data) {
        return `# ${data.title}\n\n**Company:** ${data.company}\n**Location:** ${data.location}\n**Source:** [${data.platform}](${data.url})\n**Saved:** ${new Date(data.timestamp).toLocaleString()}\n\n${data.metadata ? `**Additional Info:** ${data.metadata}\n` : ''}---\n\n## Job Description\n\n${data.description}\n\n---\n\n**URL:** ${data.url}\n`;
    }
    function downloadFile(filename, content) {
        const blob = new Blob([content], { type: 'text/markdown' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
    function createFilename(company, title) {
        const safeName = (str) => str.replace(/[^a-zA-Z0-9\s]/g, '').replace(/\s+/g, '-').substring(0, 50);
        return `${safeName(company)}-${safeName(title)}.md`;
    }
    try {
        const jobData = extractJobData();
        if (!jobData) return;
        const markdown = createMarkdown(jobData);
        const filename = createFilename(jobData.company, jobData.title);
        downloadFile(filename, markdown);
        alert(`✅ Job saved!\n\nCompany: ${jobData.company}\nRole: ${jobData.title}\n\nFile: ${filename}`);
    } catch (error) {
        alert(`❌ Error: ${error.message}`);
        console.error('Error:', error);
    }
})();
```

### Step 3: Check Results

You should see:
- Alert popup: "✅ Job saved!"
- Markdown file downloaded
- Console shows no errors

If it works, install the bookmark using Method 1.

---

## Troubleshooting

### "Nothing happens when I click the bookmark"

**Fix:**
1. Make sure the bookmark URL starts with `javascript:`
2. Try deleting and re-creating the bookmark
3. Test with Method 2 (console) first

### "Downloads are blocked"

**Chrome/Edge:**
- Click shield icon in address bar
- Allow downloads from linkedin.com

**Firefox:**
- Tools → Options → Privacy & Security → Downloads
- Uncheck "Always ask where to save files" OR add exception for linkedin.com

### "Unknown Title" or "Unknown Company"

**Fix:**
- Wait for the page to fully load before clicking
- Refresh the page and try again
- LinkedIn might have changed their page structure (report as issue)

### Console shows errors about selectors

LinkedIn occasionally updates their HTML structure. If selectors don't work:
1. Open an issue on GitHub
2. Use manual copy/paste as fallback
3. Check for bookmarklet updates

---

## Next Steps

Once the bookmarklet works:

1. **Create staging folder:**
   ```bash
   mkdir -p staging/manual-saves
   ```

2. **Save 5-10 jobs using the bookmarklet**

3. **Process the saved jobs:**
   ```bash
   python scripts/process_saved_jobs.py
   ```

4. **Analyze the batch:**
   ```bash
   python scripts/bulk_analyze.py staging/2025-11-05-processed-batch
   ```

---

## Support

If you're still having issues:
1. Try the console test method first
2. Check browser console for error messages
3. Report issue with console errors included
4. See full guide: `BOOKMARKLET-GUIDE.md`
