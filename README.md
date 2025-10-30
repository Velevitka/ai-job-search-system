# AI-Powered Job Application Management System

An intelligent job application system powered by Claude Code CLI that automates CV tailoring, job analysis, and application tracking for Product Management roles (or any professional role).

## 🎯 What This System Does

This system uses Claude Code (Anthropic's CLI tool) to automate your entire job application workflow:

1. **Analyze Job Descriptions** - Extract keywords, calculate fit scores, identify gaps
2. **Tailor CVs Automatically** - Generate role-specific CVs from your master CV
3. **Generate Cover Letters** - Create personalized cover letters based on job analysis
4. **Track Applications** - Monitor status, response rates, and success metrics
5. **Extract Insights** - Learn from your application patterns over time
6. **Prepare for Interviews** - Generate company research and interview prep materials

## 🚀 Quick Start

### Prerequisites

- **Claude Code CLI** installed ([Installation Guide](https://docs.claude.com/claude-code))
- A master CV (your comprehensive CV with all achievements)
- Basic command line knowledge

### Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/pm-job-search-system.git
cd pm-job-search-system
```

2. Create the required folder structure:
```bash
mkdir -p master applications insights staging archive
```

3. Add your master CV to `master/YourName_MasterCV.docx`

4. Review and customize the commands in `.claude/commands/` to match your needs

### First Application

1. **Analyze a job posting:**
```bash
# Using Claude Code, prompt:
Read .claude/commands/analyze-job.md and follow those instructions.

Here's the job description:
[paste JD or URL]
```

2. **Review the analysis:**
   - Check `applications/YYYY-MM-CompanyName-Role/analysis.md`
   - Review fit score (X/10)
   - Decide whether to proceed

3. **Generate tailored CV:**
```bash
Read .claude/commands/generate-cv.md and follow those instructions for [CompanyName].
```

4. **Generate cover letter (optional):**
```bash
Read .claude/commands/generate-cl.md and follow those instructions for [CompanyName].
```

5. **Track your application:**
```bash
Read .claude/commands/update-status.md

Company: [CompanyName]
Status: applied
Notes: "Submitted via LinkedIn"
```

## 📁 Folder Structure

```
.
├── .claude/
│   └── commands/          # AI agent command files
│       ├── analyze-job.md
│       ├── generate-cv.md
│       ├── generate-cl.md
│       ├── prepare-interview.md
│       ├── update-status.md
│       └── weekly-review.md
├── master/               # Your master CV (NOT in git)
│   └── YourName_MasterCV.docx
├── applications/         # Generated applications (NOT in git)
│   └── YYYY-MM-Company-Role/
│       ├── job-description.md
│       ├── analysis.md
│       ├── YourName_CV_Company.md
│       ├── YourName_CV_Company.pdf
│       └── cv-tailoring-plan.md
├── insights/            # Analytics and metrics (NOT in git)
│   ├── metrics-dashboard.md
│   └── patterns.md
├── staging/             # Draft job descriptions (NOT in git)
└── archive/             # Old applications (NOT in git)
```

## 🎨 Key Features

### 1. Intelligent Job Analysis
- Extracts key requirements and keywords
- Calculates honest fit scores (0-10)
- Identifies your strong points and gaps
- Provides CV and cover letter strategies

### 2. CV Tailoring with Human Review
- Creates tailoring plan for your approval
- **Never fabricates** - only uses content from master CV
- Integrates keywords naturally
- Maintains 2-page format
- Generates both Markdown and PDF versions (using Pandoc + Eisvogel template)

### 3. Application Tracking
- Status tracking (analysis → applied → interview → offer/rejection)
- Success metrics and conversion rates
- Pattern recognition over time
- Weekly review reports

### 4. Interview Preparation
- Company research summaries
- Role-specific talking points
- STAR format answer preparation
- Question anticipation based on JD

## 🔧 Customization

### Adapting for Your Field

This system was built for Product Management roles but can be adapted:

1. **Update command prompts** in `.claude/commands/` to match your industry language
2. **Modify CV structure** in `generate-cv.md` to match your field's conventions
3. **Adjust fit scoring** in `analyze-job.md` based on what matters in your domain

### Changing the Tone/Style

Edit the agent descriptions in command files:
- **analyze-job.md** - Adjust the "PM Career Coach Agent" persona
- **generate-cv.md** - Modify the "CV Tailoring Agent" guidelines
- **generate-cl.md** - Change cover letter tone and structure

## 📋 Commands Reference

| Command | Purpose |
|---------|---------|
| `/analyze-job` | Analyze job description and create fit score |
| `/generate-cv` | Create tailored CV for specific company |
| `/generate-cl` | Generate cover letter |
| `/update-status` | Track application status |
| `/weekly-review` | Generate weekly summary of applications |
| `/prepare-interview` | Prepare for upcoming interview |
| `/bulk-process` | Analyze multiple jobs from staging folder |

See [USAGE-GUIDE.md](USAGE-GUIDE.md) for detailed instructions.

## 🛡️ Privacy & Data Protection

**IMPORTANT:** This repository does NOT include:
- Your actual CV or personal documents
- Job applications with your personal information
- Any files with your contact details

The `.gitignore` is configured to protect all personal data. Only share:
- Command files (agent instructions)
- Documentation
- System configuration

## 🏗️ System Architecture

### How It Works

1. **Master CV as Source of Truth**
   - One comprehensive CV with ALL your achievements
   - Never modified - only used as reference
   - All tailored CVs derived from this

2. **Job-Specific Folders**
   - Each application gets its own folder
   - Contains analysis, tailored CV, cover letter
   - Maintains full history

3. **AI Agents via Claude Code**
   - Each command file defines a specialized agent
   - Agents have specific instructions and constraints
   - Human review gates prevent hallucinations

4. **PDF Generation**
   - Uses Pandoc with Eisvogel template
   - Professional formatting (Calibri font, proper spacing)
   - Maintains consistent 2-page layout

### Agent Design Philosophy

**Golden Rules:**
1. Never fabricate achievements or metrics
2. Always verify against master CV
3. Human review before final generation
4. Focus on emphasis and framing, not invention

## 📊 Analytics & Insights

The system tracks:
- **Fit scores** for each application
- **Response rates** by role type, seniority, company size
- **Time-to-response** metrics
- **Conversion rates** through each stage
- **Keyword effectiveness** (which keywords correlate with interviews)

Weekly reviews help you:
- Identify which roles to pursue
- Recognize patterns in successful applications
- Adjust your CV strategy over time

## 🤝 Contributing

Contributions welcome! Especially:
- Industry-specific adaptations (SWE, Design, Data Science, etc.)
- Additional command templates
- CV formatting improvements
- Analytics dashboards

## 📄 License

MIT License - feel free to use and adapt for your own job search.

## 🙏 Credits

Built with:
- [Claude Code](https://docs.claude.com/claude-code) by Anthropic
- [Pandoc](https://pandoc.org/) for document conversion
- [Eisvogel template](https://github.com/Wandmalfarbe/pandoc-latex-template) for beautiful PDFs

## 💡 Tips for Success

1. **Keep master CV comprehensive** - Include everything, even if not relevant to all roles
2. **Review tailoring plans carefully** - Catch hallucinations before they become CVs
3. **Track everything** - More data = better insights over time
4. **Be honest with fit scores** - Don't waste time on 3/10 roles
5. **Weekly reviews** - Reflect and adjust strategy regularly

## 🆘 Troubleshooting

See [USAGE-GUIDE.md](USAGE-GUIDE.md) for common issues and solutions.

**Common issues:**
- Claude not following command files → Be more explicit in prompts
- Hallucinations in CV → Reject and regenerate, remind about master CV
- PDF formatting issues → Check Pandoc/Eisvogel installation

## 📞 Support

- File issues on GitHub
- Check Claude Code documentation
- See USAGE-GUIDE.md for detailed help

---

**Happy job hunting!** 🎯
