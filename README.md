# AI-Powered Job Application Management System

An intelligent job application system powered by Claude Code CLI that automates CV tailoring, job analysis, and application tracking for Product Management roles (or any professional role).

## 🎯 What This System Does

This system uses Claude Code (Anthropic's CLI tool) to automate your entire job application workflow:

1. **Analyze Job Descriptions** - Extract keywords, calculate fit scores, identify gaps
2. **Tailor CVs Automatically** - Generate role-specific CVs from your master CV with Pandoc + Eisvogel template
3. **Generate Cover Letters** - Create personalized cover letters based on job analysis
4. **Track Applications** - Monitor status, response rates, and success metrics
5. **Extract Insights** - Learn from your application patterns over time
6. **Prepare for Interviews** - Generate company research and interview prep materials

## 🚀 Quick Start

### Prerequisites

- **Claude Code CLI** installed ([Installation Guide](https://docs.claude.com/claude-code))
- **Pandoc** with XeLaTeX ([Pandoc Installation](https://pandoc.org/installing.html))
- **Eisvogel template** for professional PDFs ([Template](https://github.com/Wandmalfarbe/pandoc-latex-template))
- A master CV (your comprehensive CV with all achievements)
- Basic command line knowledge

### Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/ai-job-search-system.git
cd ai-job-search-system
```

2. Create the required folder structure:
```bash
mkdir -p master applications insights staging archive
```

3. Add your master CV to `master/YourName_MasterCV.docx`

4. Review and customize the commands in `.claude/commands/` to match your needs

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

### CV Tailoring with Anti-Hallucination Safeguards
- Creates tailoring plan for human review before generation
- **Never fabricates** - only uses content from master CV
- Integrates keywords naturally
- Generates both Markdown and PDF versions using Pandoc + Eisvogel template
- Professional formatting: Calibri font, proper spacing, 2-page max

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

## 📋 Commands Reference

| Command | Purpose |
|---------|---------|
| `analyze-job` | Analyze JD and create fit score |
| `generate-cv` | Create tailored CV (MD + PDF) |
| `generate-cl` | Generate cover letter |
| `update-status` | Track application status |
| `weekly-review` | Generate weekly summary |
| `prepare-interview` | Interview preparation |

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
