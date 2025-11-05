# AI-Powered Job Application Management System

An intelligent job application system powered by Claude Code CLI that automates CV tailoring, job analysis, and application tracking for Product Management roles (or any professional role).

## 🎯 What This System Does

This system uses Claude Code (Anthropic's CLI tool) to automate your entire job application workflow:

1. **🔍 Discover Jobs Automatically** - NEW: Search LinkedIn Jobs, scrape descriptions, deduplicate (saves 2-3 hrs/week)
2. **Analyze Job Descriptions** - Extract keywords, calculate fit scores, identify gaps
3. **Tailor CVs Automatically** - Generate role-specific CVs from your master CV with Pandoc + Eisvogel template
4. **Generate Cover Letters** - Create personalized cover letters based on job analysis
5. **Track Applications** - Monitor status, response rates, and success metrics
6. **Extract Insights** - Learn from your application patterns over time
7. **Prepare for Interviews** - Generate company research and interview prep materials

## 🚀 Quick Start

### Prerequisites

- **Claude Code CLI** installed ([Installation Guide](https://docs.claude.com/claude-code))
- **Pandoc** with XeLaTeX ([Pandoc Installation](https://pandoc.org/installing.html))
- **Eisvogel template** for professional PDFs ([Template](https://github.com/Wandmalfarbe/pandoc-latex-template))
- **Python 3.x** + **Playwright** (for job discovery automation)
- A master CV (your comprehensive CV with all achievements)
- Basic command line knowledge

### Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/ai-job-search-system.git
cd ai-job-search-system
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
python -m playwright install chromium
```

3. Create the required folder structure:
```bash
mkdir -p master applications insights staging archive
```

4. Add your master CV to `master/YourName_MasterCV.docx`

5. Review and customize the commands in `.claude/commands/` to match your needs

See [SETUP.md](SETUP.md) for detailed setup instructions.

### First Application

1. **Analyze a job posting:**
```bash
# Using Claude Code, prompt:
Read .claude/commands/analyze-job.md and follow those instructions.

Here's the job description:
[paste JD or URL]
```

2. **Review the analysis** in `applications/YYYY-MM-CompanyName-Role/analysis.md`

3. **Generate tailored CV** (markdown + professional PDF):
```bash
Read .claude/commands/generate-cv.md and follow those instructions for [CompanyName].
```

4. **Track your application:**
```bash
Read .claude/commands/update-status.md

Company: [CompanyName]
Status: applied
```

See [USAGE-GUIDE.md](USAGE-GUIDE.md) for detailed usage instructions.

## 📁 Folder Structure

```
.
├── .claude/
│   └── commands/          # AI agent command files
│       ├── analyze-job.md
│       ├── generate-cv.md
│       ├── generate-cl.md
│       └── ...
├── master/               # Your master CV (NOT in git)
├── applications/         # Generated applications (NOT in git)
│   └── _example-application/  # Example folder (safe for git)
├── insights/            # Analytics (NOT in git)
├── staging/             # Draft JDs (NOT in git)
└── archive/             # Old applications (NOT in git)
```

## 🎨 Key Features

### 🔍 Automated Job Discovery (NEW - Nov 2025)
- **Search LinkedIn Jobs** with customizable criteria (keywords, location, date)
- **Smart deduplication** - Never apply to the same job twice
- **Bulk scraping** - Extract full job descriptions automatically
- **Seamless integration** - Works with existing bulk analysis workflow
- **Time savings:** 2-3 hours/week on manual job searching

**Quick example:**
```bash
python scripts/job_discovery.py --keywords "Director Product" --location "London"
# Discovers 20-30 jobs, saves to staging/, ready for bulk analysis
```

See [QUICKSTART-JOB-DISCOVERY.md](QUICKSTART-JOB-DISCOVERY.md) for details.

### CV Tailoring with Anti-Hallucination Safeguards
- Creates tailoring plan for human review before generation
- **Never fabricates** - only uses content from master CV
- Integrates keywords naturally
- Generates both Markdown and PDF versions using Pandoc + Eisvogel template
- Professional formatting: Calibri font, proper spacing, 2-page max
- **Automated validation** - Ensures 2-page max, A4 size, correct formatting

### Cover Letter Generation with Formatting Guardrails
- **1-page enforcement** - Automatic validation ensures professional length
- Word count limits: 300-400 words (optimized for Eisvogel spacing)
- Company research integration with recent news/products
- Multi-draft generation with AI self-critique
- **Automated validation** - Catches 2-page issues before delivery

### Intelligent Job Analysis
- Calculates honest fit scores (0-10)
- Identifies strong points and gaps
- Extracts ATS keywords
- Provides CV and cover letter strategies

### Application Tracking & Analytics
- Status tracking through full lifecycle
- Success metrics and conversion rates
- Pattern recognition over time
- Weekly review reports

## 🔧 Customization

This system was built for Product Management roles but can be adapted:

1. Update command prompts in `.claude/commands/` for your industry
2. Modify CV structure in `generate-cv.md` for your field's conventions
3. Adjust fit scoring in `analyze-job.md` based on what matters in your domain

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to adapt for other fields.

## 📋 Complete Application Workflow

### End-to-End Example: Applying to a Product Lead Role

This is a real example workflow from discovering jobs to submitting applications:

#### 0. Discover Jobs (OPTIONAL - 5 minutes for 20-30 jobs)

**NEW:** Automate job discovery instead of manual searching:

```bash
python scripts/job_discovery.py --keywords "Director Product Data Platform" --location "London, United Kingdom" --date past_week
```

**What happens:**
- Searches LinkedIn Jobs with your criteria
- Scrolls to load all results (handles pagination)
- Checks against existing applications (deduplicates)
- Scrapes full job descriptions for new jobs
- Saves to `staging/YYYY-MM-DD-discovery-batch/`

**Output:**
```
staging/2025-11-05-discovery-batch/
├── DISCOVERY-SUMMARY.json          # Metadata
├── Spotify-DirectorProductGrowth/
│   └── job-description.md
├── Monzo-HeadOfDataPlatform/
│   └── job-description.md
└── ... (18 more jobs)
```

**Next:** Run bulk analysis on discovered jobs:
```bash
python scripts/bulk_analyze.py staging/2025-11-05-discovery-batch
# Reviews BULK-ANALYSIS-SUMMARY.md sorted by fit score
# Apply to 8+ fit roles
```

**Time saved:** 2-3 hours vs. manual searching

---

#### 1. Analyze Job Posting (5-10 minutes)

```bash
/analyze-job https://company.com/careers/product-lead
```

**What happens:**
- Fetches job description (or paste manually if needed)
- Extracts company details, role requirements, keywords
- Calculates honest fit score (e.g., 7.5/10)
- Identifies your strong points vs. gaps
- Suggests CV and cover letter strategies
- Researches company news/products via web search

**Output:**
```
applications/2025-10-CompanyName-ProductLead/
├── job-description.md          # Saved JD with keywords
└── analysis.md                 # Fit analysis with strategy
```

**Example fit score output:**
```
Fit Score: 7.5/10

Strong Points:
✅ Two-sided marketplace experience (Vrbo: 23 markets)
✅ Fast-growth digital bank (Chase UK doubled customers)
✅ Team leadership (2 Senior PMs + 2 PMs)

Gaps to Address:
⚠️ Limited FinTech experience → Frame as fresh perspective
```

---

#### 2. Generate Tailored CV (10-15 minutes)

```bash
/generate-cv CompanyName
```

**What happens:**
- Reads your master CV (source of truth)
- Reads job analysis for keywords and strategy
- Creates tailoring plan with proposed changes
- **Human review gate** - you approve before generation
- Generates Markdown CV with YAML front matter
- Creates professional PDF using Pandoc + Eisvogel template
- Documents all changes in cv-changes-log.md

**Output:**
```
applications/2025-10-CompanyName-ProductLead/
├── cv-tailoring-plan.md               # Human-reviewed plan
├── ArturSwadzba_CV_CompanyName.md     # Markdown source
├── ArturSwadzba_CV_CompanyName.pdf    # Final PDF (2 pages)
└── cv-changes-log.md                  # Change documentation
```

**Key features:**
- ✅ **Anti-hallucination:** Never fabricates - only reframes existing achievements
- ✅ **Keyword optimization:** Integrates JD keywords naturally (e.g., 12/12 keywords)
- ✅ **Metric preservation:** All numbers verified against master CV
- ✅ **Human control:** You approve before PDF generation

**Example CV modification:**
```markdown
Before: "Led MarTech stack at Vrbo"
After:  "Led MarTech stack for global vacation rental marketplace
         connecting millions of travelers with property owners across
         23 markets" (emphasizes two-sided platform for relevant role)
```

---

#### 3. Generate Cover Letter (15-20 minutes)

```bash
/generate-cl CompanyName
```

**What happens:**
- **Phase 1: Company Research** - Web search for recent news, products, milestones
- **Phase 2: Multi-Draft Generation** - Creates 3-4 opening hook options
- **Phase 3: AI Self-Critique** - Identifies strengths and weaknesses
- **Phase 4: Human Review & Iteration** - You choose opening and approve
- Generates professional PDF with proper business letter format

**Output:**
```
applications/2025-10-CompanyName-ProductLead/
├── company-research-brief.md           # Recent intel
├── cover-letter-draft.md               # All options + critique
├── ArturSwadzba_CoverLetter_CompanyName.md
├── ArturSwadzba_CoverLetter_CompanyName.pdf
└── cover-letter-log.md                 # Strategy documentation
```

**Opening hook options example:**
```
Option A: Achievement-First
"At Chase UK, I led a 15-person team to reduce time-to-market by 40%
while delivering $5M in cost savings..."

Option B: Company-Specific Research
"Your achievement of 1 billion annual transactions demonstrates the
scale I thrive in..."

Option D: Hybrid (Recommended)
"Having built the MarTech platform connecting millions of travelers
with property owners across Vrbo's 23-market marketplace, I understand
two-sided platforms..."
```

**Company research incorporated:**
- ✅ Recent milestones (e.g., "1 billion transactions")
- ✅ Product launches (e.g., "SumUp Pay")
- ✅ Competitive context (e.g., "4 million merchant network")

---

#### 4. Submit & Track Application (2 minutes)

```bash
/update-status CompanyName applied "Submitted via company ATS, can track on Greenhouse"
```

**What happens:**
- Creates status.md with application timeline
- Records CV/cover letter versions used
- Sets up follow-up reminders
- Updates analytics dashboard

**Output:**
```
applications/2025-10-CompanyName-ProductLead/
└── status.md                           # Status tracking
```

**Status file includes:**
```markdown
Current Status: Applied
Applied On: 2025-10-31

Application Highlights:
- Fit Score: 7.5/10
- Key Differentiators: Two-sided platform, FinTech scale-up
- Documents: CV + Cover Letter (condensed, 275 words)

Follow-Up Plan:
- Week 1: No action (let them review)
- Week 2: Consider check-in if no response
- Expected response: 7-14 days
```

---

### Total Time Investment Per Application

| Phase | Time | Automated? |
|-------|------|------------|
| Job Analysis | 5-10 min | ✅ Fully automated |
| CV Tailoring | 10-15 min | ⚠️ Semi-automated (human approval) |
| Cover Letter | 15-20 min | ⚠️ Semi-automated (human approval) |
| Submit & Track | 2 min | ✅ Fully automated |
| **Total** | **30-45 min** | **~70% automated** |

Compare to manual process: **2-3 hours per application**

---

### Real Results Example (SumUp Product Lead)

**Before workflow:**
- Generic CV with heavy B2B/MarTech focus
- Initial fit score: 6.5/10

**After workflow:**
1. **Analysis revealed:** B2C consumer product background (not B2B!)
   - Vrbo: Two-sided marketplace (travelers ↔ property owners)
   - Chase UK: Fast-growth digital bank (doubled customers)
   - Trip Boards: Consumer-facing shareable feature

2. **CV tailored to emphasize:**
   - Two-sided platform credibility (23 markets)
   - Consumer product building (Trip Boards)
   - FinTech scale-up experience
   - Team leadership (2 Senior PMs, coaching/1:1s)

3. **Cover letter optimized:**
   - Researched company (1B transactions, 4M merchants)
   - Addressed FinTech gap proactively
   - Condensed to 275 words (natural tone, no AI tells)
   - Perfect keyword alignment (12/12)

**Result:** Revised fit score: **7.5/10** → Strong application submitted

---

## 📋 Commands Quick Reference

| Command | Purpose | Time | Output |
|---------|---------|------|--------|
| `/analyze-job` | Analyze JD and create fit score | 5-10 min | analysis.md, job-description.md |
| `/generate-cv` | Create tailored CV (MD + PDF) | 10-15 min | CV.pdf, cv-changes-log.md |
| `/generate-cl` | Generate cover letter | 15-20 min | CoverLetter.pdf, cover-letter-log.md |
| `/update-status` | Track application status | 2 min | status.md |
| `/weekly-review` | Generate weekly summary | 5 min | Review of all applications |
| `/prepare-interview` | Interview preparation | 10 min | Company research, practice questions |

## 🔍 Validation Scripts

Automated quality control to ensure professional document formatting:

### CV Validation
```bash
python scripts/validate-cv.py <cv.pdf> [<cv.md>]
```

**Checks:**
- ✅ Exactly 2 pages (not 4, not 6)
- ✅ A4 paper size (595 x 842 pts)
- ✅ File size 60-80KB (Eisvogel typical)
- ✅ Clean YAML (no problematic formatting)

### Cover Letter Validation
```bash
python scripts/validate-cover-letter.py <cl.pdf> [<cl.md>]
```

**Checks:**
- ✅ Exactly 1 page (CRITICAL - 2 pages is unprofessional)
- ✅ Word count 300-400 (optimal for Eisvogel)
- ✅ A4 paper size
- ✅ File size 10-20KB

**Why validation matters:**
- Prevents 2-page cover letters (unprofessional)
- Ensures consistent formatting across applications
- Catches issues before submission
- Automated - no manual checking needed

See `docs/cv-formatting-guardrails.md` and `docs/cover-letter-formatting-guardrails.md` for details.

## 🛡️ Privacy & Data Protection

**IMPORTANT:** This repository does NOT include:
- Your actual CV or personal documents
- Job applications with your personal information
- Any files with your contact details

The `.gitignore` is configured to protect all personal data.

## 📚 Documentation

- [SETUP.md](SETUP.md) - Initial setup instructions
- [USAGE-GUIDE.md](USAGE-GUIDE.md) - Detailed usage guide
- [GIT-SETUP-GUIDE.md](GIT-SETUP-GUIDE.md) - How to safely publish to GitHub
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines

## 🤝 Contributing

Contributions welcome! Especially:
- Industry-specific adaptations
- Additional command templates
- CV formatting improvements
- Analytics enhancements

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

## 🙏 Credits

Built with:
- [Claude Code](https://docs.claude.com/claude-code) by Anthropic
- [Pandoc](https://pandoc.org/) for document conversion
- [Eisvogel template](https://github.com/Wandmalfarbe/pandoc-latex-template) for professional PDFs

## 💡 Example Application

Check out `applications/_example-application/` for a complete example showing:
- Job description analysis
- Fit score calculation
- CV tailoring plan
- Application tracking

---

**Happy job hunting!** 🎯

*System optimized for Product Management roles but adaptable to any field.*
