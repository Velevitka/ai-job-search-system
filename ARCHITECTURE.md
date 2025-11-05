# Project Architecture

**Clean, organized structure for AI-powered job application system**

---

## Directory Structure

```
ai-job-search-system/
│
├── README.md                    # Main entry point
├── career-preferences.md        # User configuration
├── STATUS.md                    # Auto-generated status (git-ignored)
├── requirements.txt             # Python dependencies
├── LICENSE
├── .gitignore
│
├── docs/                        # All documentation
│   ├── setup/
│   │   ├── SETUP.md
│   │   └── GIT-SETUP-GUIDE.md
│   ├── usage/
│   │   ├── USAGE-GUIDE.md
│   │   ├── QUICK-WORKFLOW.md
│   │   └── bookmarklet/
│   │       ├── BOOKMARKLET-GUIDE.md
│   │       ├── BOOKMARKLET-INSTALL.md
│   │       └── BOOKMARKLET-CODE.txt
│   ├── reference/
│   │   ├── ROADMAP.md
│   │   ├── CONTRIBUTING.md
│   │   ├── DOCUMENTATION-GUIDE.md
│   │   └── PRE-PUBLISH-CHECKLIST.md
│   ├── history/
│   │   ├── SUNSET-SUMMARY.md
│   │   ├── ARCHIVE-SUMMARY.md
│   │   ├── BULK-PROCESS-SUMMARY.md
│   │   └── SYNC-COMMANDS-SUMMARY.md
│   └── formatting/
│       ├── cv-formatting-guardrails.md
│       ├── cover-letter-formatting-guardrails.md
│       └── eisvogel-assessment.md
│
├── scripts/                     # Active automation scripts
│   ├── bookmarklet/
│   │   ├── bookmarklet-save-job.js
│   │   ├── console-test.js
│   │   └── test-page.html
│   ├── validation/
│   │   ├── validate-cv.py
│   │   └── validate-cover-letter.py
│   └── README.md
│
├── deprecated/                  # Obsolete code with warnings
│   ├── DEPRECATION-NOTICE.md
│   ├── automation/              # OLD: Automated scraping (ToS violation)
│   │   ├── job_discovery.py
│   │   ├── scheduled_monitor.py
│   │   ├── process_saved_jobs.py
│   │   ├── bulk_analyze.py
│   │   ├── extract_mhtml.py
│   │   ├── DEPLOYMENT-GUIDE.md
│   │   ├── TESTING-LOGIN.md
│   │   └── QUICKSTART-JOB-DISCOVERY.md
│   └── other-deprecated-files/
│
├── .claude/                     # Claude Code configuration
│   ├── commands/                # Slash commands
│   │   ├── analyze-job.md
│   │   ├── generate-cv.md
│   │   ├── generate-cover-letter.md
│   │   ├── bulk-process.md
│   │   └── ...
│   └── settings.json
│
├── master/                      # Master CV (PRIVATE - gitignored)
│   ├── ArturSwadzba_MasterCV.docx
│   └── README.md
│
├── applications/                # Job applications (PRIVATE - gitignored)
│   ├── 2025-11-Company-Role/
│   │   ├── job-description.md
│   │   ├── analysis.md
│   │   ├── cv-tailoring-plan.md
│   │   ├── ArturSwadzba_CV_Company.md
│   │   ├── ArturSwadzba_CV_Company.pdf
│   │   └── status.md
│   ├── _example-application/    # Example (safe for git)
│   └── archive/                 # Old applications (2020-2024)
│       └── [old CVs and apps]
│
├── staging/                     # Job descriptions (PRIVATE - gitignored)
│   ├── manual-saves/            # Bookmarklet downloads
│   └── 2025-11-05-processed-batch/
│
└── insights/                    # Analytics (PRIVATE - gitignored)
    ├── bulk-analysis-2025-11-05.md
    └── metrics/
```

---

## Key Principles

### 1. Separation of Concerns
- **docs/** = All documentation
- **scripts/** = Active automation
- **deprecated/** = Obsolete code
- **applications/** = Private work data

### 2. Root Directory = Minimal
Only essential files in root:
- README.md (entry point)
- career-preferences.md (user config)
- STATUS.md (auto-generated)
- Standard project files (LICENSE, .gitignore, requirements.txt)

### 3. No Duplication
- One place for archived applications: `applications/archive/`
- One place for docs: `docs/`
- No staging/archive (use staging/ with date-based batches)

### 4. Clear Naming
- Folders: lowercase with hyphens
- Docs: UPPERCASE-WITH-HYPHENS.md
- Scripts: lowercase_with_underscores.py or kebab-case.js

---

## Migration Plan

### Phase 1: Move Documentation (Low Risk)
```bash
# Create structure
mkdir -p docs/{setup,usage/bookmarklet,reference,history,formatting}

# Move files
mv SETUP.md docs/setup/
mv GIT-SETUP-GUIDE.md docs/setup/
mv USAGE-GUIDE.md docs/usage/
mv QUICK-WORKFLOW.md docs/usage/
mv BOOKMARKLET-*.md docs/usage/bookmarklet/
mv BOOKMARKLET-CODE.txt docs/usage/bookmarklet/
mv ROADMAP.md docs/reference/
mv CONTRIBUTING.md docs/reference/
mv DOCUMENTATION-GUIDE.md docs/reference/
mv PRE-PUBLISH-CHECKLIST.md docs/reference/
mv *-SUMMARY.md docs/history/
mv docs/cv-formatting-guardrails.md docs/formatting/
mv docs/cover-letter-formatting-guardrails.md docs/formatting/
mv docs/eisvogel-assessment.md docs/formatting/
```

### Phase 2: Move Scripts
```bash
mkdir -p scripts/{bookmarklet,validation}
mv bookmarklet-save-job.js scripts/bookmarklet/
mv bookmarklet-save-job-console-test.js scripts/bookmarklet/console-test.js
mv test-bookmarklet.html scripts/bookmarklet/test-page.html
```

### Phase 3: Consolidate Archives
```bash
# Move old applications to proper location
mv archive/* applications/archive/
rmdir archive/
```

### Phase 4: Deprecate Obsolete Scripts
```bash
mkdir -p deprecated/automation
mv scripts/process_saved_jobs.py deprecated/automation/
mv scripts/bulk_analyze.py deprecated/automation/
mv scripts/extract_mhtml.py deprecated/automation/
```

### Phase 5: Update Links
- Update README.md links
- Update docs/ internal links
- Update .claude/commands/ references

---

## Benefits

✅ **Clean root directory** - Only 6 essential files
✅ **Organized docs** - Easy to find any guide
✅ **No duplication** - Single source of truth
✅ **Clear separation** - Active vs. deprecated
✅ **Scalable** - Easy to add new docs/scripts

---

## File Counts

### Before
- Root: 18 markdown files
- Scattered scripts: 7 locations
- Documentation: 3 locations (root, docs/, deprecated/)

### After
- Root: 1 markdown file (README.md)
- Scripts: Organized in scripts/{bookmarklet,validation}/
- Documentation: All in docs/ with clear categories
