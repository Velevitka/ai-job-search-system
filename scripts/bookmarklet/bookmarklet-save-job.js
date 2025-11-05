/**
 * LinkedIn Job Saver Bookmarklet
 *
 * USAGE: Drag this file to your bookmarks bar, or copy the minified code below
 * into a new bookmark's URL field.
 *
 * COMPLIANT: This is NOT automation - user manually clicks while viewing a job.
 * No scraping, no bots, no ToS violations. Just assisted data extraction.
 *
 * HOW IT WORKS:
 * 1. User browses to a LinkedIn job posting
 * 2. User clicks this bookmarklet in their browser
 * 3. Bookmarklet extracts job data from the current page DOM
 * 4. Creates markdown file and triggers download
 * 5. User saves to staging/manual-saves/ folder
 */

(function() {
    'use strict';

    /**
     * Extract job details from LinkedIn job posting page
     */
    function extractLinkedInJob() {
        const data = {
            url: window.location.href,
            platform: 'LinkedIn',
            timestamp: new Date().toISOString()
        };

        // Extract job title
        const titleEl = document.querySelector('.job-details-jobs-unified-top-card__job-title, .jobs-unified-top-card__job-title, h1');
        data.title = titleEl ? titleEl.textContent.trim() : 'Unknown Title';

        // Extract company name
        const companyEl = document.querySelector('.job-details-jobs-unified-top-card__company-name, .jobs-unified-top-card__company-name, .jobs-unified-top-card__subtitle-primary-grouping a');
        data.company = companyEl ? companyEl.textContent.trim() : 'Unknown Company';

        // Extract location
        const locationEl = document.querySelector('.job-details-jobs-unified-top-card__bullet, .jobs-unified-top-card__bullet');
        data.location = locationEl ? locationEl.textContent.trim() : 'Unknown Location';

        // Extract job description
        const descEl = document.querySelector('.jobs-description__content, .jobs-box__html-content, .description__text');
        data.description = descEl ? descEl.innerText.trim() : 'No description found';

        // Extract additional metadata
        const criteriaList = document.querySelectorAll('.jobs-unified-top-card__job-insight span');
        data.metadata = Array.from(criteriaList).map(el => el.textContent.trim()).join(' | ');

        return data;
    }

    /**
     * Extract job details from Greenhouse job posting
     */
    function extractGreenhouseJob() {
        const data = {
            url: window.location.href,
            platform: 'Greenhouse',
            timestamp: new Date().toISOString()
        };

        // Extract job title
        const titleEl = document.querySelector('.app-title, h1.app-title');
        data.title = titleEl ? titleEl.textContent.trim() : 'Unknown Title';

        // Extract company name (from URL or page)
        const urlMatch = window.location.href.match(/boards\.greenhouse\.io\/([^\/]+)/);
        const companyEl = document.querySelector('.company-name');
        data.company = companyEl ? companyEl.textContent.trim() : (urlMatch ? urlMatch[1] : 'Unknown Company');

        // Extract location
        const locationEl = document.querySelector('.location');
        data.location = locationEl ? locationEl.textContent.trim() : 'Unknown Location';

        // Extract job description
        const descEl = document.querySelector('#content, .content');
        data.description = descEl ? descEl.innerText.trim() : 'No description found';

        return data;
    }

    /**
     * Extract job details from Lever job posting
     */
    function extractLeverJob() {
        const data = {
            url: window.location.href,
            platform: 'Lever',
            timestamp: new Date().toISOString()
        };

        // Extract job title
        const titleEl = document.querySelector('.posting-headline h2');
        data.title = titleEl ? titleEl.textContent.trim() : 'Unknown Title';

        // Extract company name
        const urlMatch = window.location.href.match(/jobs\.lever\.co\/([^\/]+)/);
        data.company = urlMatch ? urlMatch[1] : 'Unknown Company';

        // Extract location
        const locationEl = document.querySelector('.posting-categories .location, .workplaceTypes');
        data.location = locationEl ? locationEl.textContent.trim() : 'Unknown Location';

        // Extract job description
        const descEl = document.querySelector('.content');
        data.description = descEl ? descEl.innerText.trim() : 'No description found';

        return data;
    }

    /**
     * Detect platform and extract job data
     */
    function extractJobData() {
        const url = window.location.href;

        if (url.includes('linkedin.com/jobs')) {
            return extractLinkedInJob();
        } else if (url.includes('greenhouse.io')) {
            return extractGreenhouseJob();
        } else if (url.includes('lever.co')) {
            return extractLeverJob();
        } else {
            alert('Unsupported platform. Currently supports: LinkedIn, Greenhouse, Lever');
            return null;
        }
    }

    /**
     * Create markdown file content
     */
    function createMarkdown(data) {
        return `# ${data.title}

**Company:** ${data.company}
**Location:** ${data.location}
**Source:** [${data.platform}](${data.url})
**Saved:** ${new Date(data.timestamp).toLocaleString()}

${data.metadata ? `**Additional Info:** ${data.metadata}\n` : ''}
---

## Job Description

${data.description}

---

**URL:** ${data.url}
`;
    }

    /**
     * Download file to user's computer
     */
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

    /**
     * Create safe filename from company and title
     */
    function createFilename(company, title) {
        const safeName = (str) => str
            .replace(/[^a-zA-Z0-9\s]/g, '')
            .replace(/\s+/g, '-')
            .substring(0, 50);

        return `${safeName(company)}-${safeName(title)}.md`;
    }

    /**
     * Main execution
     */
    try {
        // Extract job data
        const jobData = extractJobData();

        if (!jobData) {
            return; // Unsupported platform
        }

        // Create markdown content
        const markdown = createMarkdown(jobData);

        // Create filename
        const filename = createFilename(jobData.company, jobData.title);

        // Download file
        downloadFile(filename, markdown);

        // Show success message
        alert(`✅ Job saved!\n\nCompany: ${jobData.company}\nRole: ${jobData.title}\n\nFile: ${filename}\n\nNext steps:\n1. Save to: staging/manual-saves/\n2. Run: python scripts/process_saved_jobs.py`);

    } catch (error) {
        alert(`❌ Error saving job:\n\n${error.message}\n\nPlease try again or manually copy the job description.`);
        console.error('Job saver error:', error);
    }
})();


/**
 * MINIFIED BOOKMARKLET CODE (Copy this to bookmark URL)
 * ====================================================
 *
 * javascript:(function()%7B'use strict'%3Bfunction extractLinkedInJob()%7Bconst data%3D%7Burl:window.location.href%2Cplatform:'LinkedIn'%2Ctimestamp:new Date().toISOString()%7D%3Bconst titleEl%3Ddocument.querySelector('.job-details-jobs-unified-top-card__job-title%2C .jobs-unified-top-card__job-title%2C h1')%3Bdata.title%3DtitleEl%3FtitleEl.textContent.trim():'Unknown Title'%3Bconst companyEl%3Ddocument.querySelector('.job-details-jobs-unified-top-card__company-name%2C .jobs-unified-top-card__company-name%2C .jobs-unified-top-card__subtitle-primary-grouping a')%3Bdata.company%3DcompanyEl%3FcompanyEl.textContent.trim():'Unknown Company'%3Bconst locationEl%3Ddocument.querySelector('.job-details-jobs-unified-top-card__bullet%2C .jobs-unified-top-card__bullet')%3Bdata.location%3DlocationEl%3FlocationEl.textContent.trim():'Unknown Location'%3Bconst descEl%3Ddocument.querySelector('.jobs-description__content%2C .jobs-box__html-content%2C .description__text')%3Bdata.description%3DdescEl%3FdescEl.innerText.trim():'No description found'%3Bconst criteriaList%3Ddocument.querySelectorAll('.jobs-unified-top-card__job-insight span')%3Bdata.metadata%3DArray.from(criteriaList).map(el%3D>el.textContent.trim()).join(' %7C ')%3Breturn data%7Dfunction extractJobData()%7Bconst url%3Dwindow.location.href%3Bif(url.includes('linkedin.com%2Fjobs'))%7Breturn extractLinkedInJob()%7Delse%7Balert('Unsupported platform. Currently supports: LinkedIn%2C Greenhouse%2C Lever')%3Breturn null%7D%7Dfunction createMarkdown(data)%7Breturn%60%23 %24%7Bdata.title%7D%5Cn%5Cn**Company:** %24%7Bdata.company%7D %5Cn**Location:** %24%7Bdata.location%7D %5Cn**Source:** %5B%24%7Bdata.platform%7D%5D(%24%7Bdata.url%7D) %5Cn**Saved:** %24%7Bnew Date(data.timestamp).toLocaleString()%7D%5Cn%5Cn%24%7Bdata.metadata%3F%60**Additional Info:** %24%7Bdata.metadata%7D%5Cn%60:''%7D---%5Cn%5Cn%23%23 Job Description%5Cn%5Cn%24%7Bdata.description%7D%5Cn%5Cn---%5Cn%5Cn**URL:** %24%7Bdata.url%7D%5Cn%60%7Dfunction downloadFile(filename%2Ccontent)%7Bconst blob%3Dnew Blob(%5Bcontent%5D%2C%7Btype:'text%2Fmarkdown'%7D)%3Bconst url%3DURL.createObjectURL(blob)%3Bconst a%3Ddocument.createElement('a')%3Ba.href%3Durl%3Ba.download%3Dfilename%3Bdocument.body.appendChild(a)%3Ba.click()%3Bdocument.body.removeChild(a)%3BURL.revokeObjectURL(url)%7Dfunction createFilename(company%2Ctitle)%7Bconst safeName%3D(str)%3D>str.replace(%2F%5B%5Ea-zA-Z0-9%5Cs%5D%2Fg%2C'').replace(%2F%5Cs%2B%2Fg%2C'-').substring(0%2C50)%3Breturn%60%24%7BsafeName(company)%7D-%24%7BsafeName(title)%7D.md%60%7Dtry%7Bconst jobData%3DextractJobData()%3Bif(!jobData)%7Breturn%7Dconst markdown%3DcreateMarkdown(jobData)%3Bconst filename%3DcreateFilename(jobData.company%2CjobData.title)%3BdownloadFile(filename%2Cmarkdown)%3Balert(%60%E2%9C%85 Job saved!%5Cn%5CnCompany: %24%7BjobData.company%7D%5CnRole: %24%7BjobData.title%7D%5Cn%5CnFile: %24%7Bfilename%7D%5Cn%5CnNext steps:%5Cn1. Save to: staging%2Fmanual-saves%2F%5Cn2. Run: python scripts%2Fprocess_saved_jobs.py%60)%7Dcatch(error)%7Balert(%60%E2%9D%8C Error saving job:%5Cn%5Cn%24%7Berror.message%7D%5Cn%5CnPlease try again or manually copy the job description.%60)%3Bconsole.error('Job saver error:'%2Cerror)%7D%7D)()%3B
 */
