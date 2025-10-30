# Example Application Folder

This is an example of what a complete application folder looks like after going through the full workflow.

## Folder Structure

```
2025-01-TechCorp-SeniorProductManager/
├── job-description.md           # Saved job posting with keywords
├── analysis.md                  # Fit score and strategy
├── cv-tailoring-plan.md         # Proposed CV changes (human-reviewed)
├── YourName_CV_TechCorp.md      # Tailored CV (markdown)
├── YourName_CV_TechCorp.pdf     # Final PDF
├── cv-changes-log.md            # What was modified
├── YourName_CoverLetter_TechCorp.md  # Cover letter (if created)
├── application-tracker.md       # Status tracking
└── interviews/                  # Created if you get interviews
    ├── prep-notes.md
    └── transcript-2025-01-15.md
```

## Workflow Example

1. **Job Analysis** - Created job-description.md and analysis.md
2. **CV Tailoring** - Generated tailoring plan, reviewed, approved
3. **Documents Generated** - Markdown and PDF CV created
4. **Application Submitted** - Tracked in application-tracker.md
5. **Interview Scheduled** - Prep materials created in interviews/
6. **Outcome Tracked** - Final status updated

## Files Explained

### job-description.md
Contains the original job posting, extracted keywords, core responsibilities, and qualifications. Used as reference throughout the application process.

### analysis.md
Your fit score (X/10), strong points, gaps, and recommended strategies for CV and cover letter. This guides all subsequent tailoring.

### cv-tailoring-plan.md
The proposed modifications to your master CV. **You review and approve this** before the final CV is generated. Critical for preventing hallucinations.

### YourName_CV_TechCorp.md
The tailored CV in markdown format with YAML front matter for PDF generation. Includes all modifications from the approved tailoring plan.

### YourName_CV_TechCorp.pdf
Final PDF generated via Pandoc using Eisvogel template. Professional formatting with Calibri font, proper spacing, page numbers.

### cv-changes-log.md
Documentation of what changed from master CV to tailored CV. Helps verify accuracy and track which modifications were effective.

### application-tracker.md
Timeline of all interactions: application submitted, responses received, interview scheduled, outcome. Used for analytics.

### interviews/
Created when you schedule an interview. Contains company research, role-specific prep, STAR examples, and post-interview notes.

## Example Timeline

- **Day 1**: Job analyzed (fit score 8/10)
- **Day 1**: CV tailored and approved
- **Day 1**: Application submitted
- **Day 5**: Recruiter response, phone screen scheduled
- **Day 8**: Phone screen completed, notes saved
- **Day 12**: Technical interview scheduled
- **Day 15**: Technical interview completed
- **Day 18**: Offer received / Rejection received

All tracked in application-tracker.md for analytics and pattern recognition.
