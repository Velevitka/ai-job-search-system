/**
 * CONSOLE TEST VERSION
 *
 * To test in browser console:
 * 1. Go to a LinkedIn job posting
 * 2. Open browser console (F12)
 * 3. Copy and paste THIS ENTIRE FILE
 * 4. Press Enter
 *
 * If it works, you'll see an alert and a download.
 */

(function() {
    'use strict';

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

    function extractJobData() {
        const url = window.location.href;

        if (url.includes('linkedin.com/jobs')) {
            return extractLinkedInJob();
        } else {
            alert('Unsupported platform. Currently supports: LinkedIn, Greenhouse, Lever');
            return null;
        }
    }

    function createMarkdown(data) {
        return `# ${data.title}

**Company:** ${data.company}
**Location:** ${data.location}
**Source:** [${data.platform}](${data.url})
**Saved:** ${new Date(data.timestamp).toLocaleString()}

${data.metadata ? `**Additional Info:** ${data.metadata}\n` : ''}---

## Job Description

${data.description}

---

**URL:** ${data.url}
`;
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
        const safeName = (str) => str
            .replace(/[^a-zA-Z0-9\s]/g, '')
            .replace(/\s+/g, '-')
            .substring(0, 50);

        return `${safeName(company)}-${safeName(title)}.md`;
    }

    try {
        const jobData = extractJobData();

        if (!jobData) {
            return;
        }

        const markdown = createMarkdown(jobData);
        const filename = createFilename(jobData.company, jobData.title);

        downloadFile(filename, markdown);

        alert(`✅ Job saved!\n\nCompany: ${jobData.company}\nRole: ${jobData.title}\n\nFile: ${filename}\n\nNext steps:\n1. Save to: staging/manual-saves/\n2. Run: python scripts/process_saved_jobs.py`);

    } catch (error) {
        alert(`❌ Error saving job:\n\n${error.message}\n\nPlease try again or manually copy the job description.`);
        console.error('Job saver error:', error);
    }
})();
