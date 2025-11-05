# Contributing to AI-Powered Job Application System

Thank you for your interest in contributing! This project helps job seekers automate their application process using Claude Code CLI.

## 🎯 How You Can Contribute

### 1. Industry-Specific Adaptations
The system was built for Product Management roles but can be adapted for other fields:
- Software Engineering
- Design (UX/UI, Product Design)
- Data Science / Analytics
- Marketing / Growth Marketing
- Sales / Business Development

**To contribute an adaptation:**
1. Create a new branch: `git checkout -b industry/software-engineering`
2. Modify command files in `.claude/commands/` to match industry language
3. Update CV structure recommendations
4. Adjust fit scoring criteria
5. Add industry-specific examples to documentation
6. Submit a PR with detailed explanation

### 2. New Command Templates
Add new automation capabilities:
- `/analyze-interview` - Post-interview analysis and follow-up
- `/salary-negotiation` - Offer analysis and negotiation prep
- `/linkedin-optimize` - LinkedIn profile optimization
- `/company-research` - Deep-dive company research
- `/networking-tracker` - Connection and referral management

**To add a new command:**
1. Create new file in `.claude/commands/your-command.md`
2. Follow existing command structure (see template below)
3. Include clear agent instructions
4. Add examples and expected outputs
5. Update USAGE-GUIDE.md with new command
6. Submit PR

### 3. Documentation Improvements
- Clarify confusing instructions
- Add more examples
- Fix typos or errors
- Translate to other languages
- Add video tutorials or screenshots
- Improve onboarding experience

### 4. PDF Generation Enhancements
- Alternative templates (different styles)
- Additional formatting options
- Page length optimization
- Different fonts/themes
- Industry-specific layouts

### 5. Analytics & Insights
- Better tracking metrics
- Visualization dashboards
- Pattern recognition improvements
- Success prediction models
- Keyword effectiveness analysis

## 📋 Contribution Guidelines

### Before You Start

1. **Check existing issues** - Someone might already be working on it
2. **Open an issue first** - Discuss large changes before implementing
3. **Keep it generic** - No personal data in contributions
4. **Test thoroughly** - Verify your changes work end-to-end

### Code of Conduct

- Be respectful and constructive
- No personal attacks or harassment
- Focus on helping job seekers
- Assume positive intent
- Help newcomers learn

### What NOT to Contribute

❌ **Personal data:**
- Your actual CV or applications
- Company-specific applications with real data
- Personal contact information
- Specific job descriptions from your search

❌ **Hallucination-prone changes:**
- Commands that generate fake achievements
- Metrics inflation suggestions
- Fabrication of experience

❌ **Low-quality additions:**
- Untested command files
- Commands without clear instructions
- Breaking changes without migration guide

## 🛠️ Development Setup

### Prerequisites
- Claude Code CLI installed
- Basic understanding of markdown
- Familiarity with AI prompting (helpful but not required)

### Local Setup
```bash
# 1. Fork the repository on GitHub

# 2. Clone your fork
git clone https://github.com/yourusername/ai-job-search-system.git
cd ai-job-search-system

# 3. Create your personal data folders (not tracked by git)
mkdir -p master applications insights staging archive

# 4. Add your master CV for testing
cp /path/to/your/cv.docx master/YourName_MasterCV.docx

# 5. Create a new branch
git checkout -b feature/your-feature-name

# 6. Make your changes

# 7. Test your changes
# Run through the full workflow to verify everything works
```

### Testing Your Changes

**For command file changes:**
1. Test the command end-to-end with a real job description
2. Verify the output is accurate and useful
3. Check for hallucinations or fabrications
4. Ensure it follows the existing patterns

**For documentation changes:**
1. Read through as a new user would
2. Verify all links work
3. Check formatting renders correctly
4. Test any code examples

### Submitting a Pull Request

1. **Ensure .gitignore is working:**
```bash
git status
# Should show ONLY system files, no personal data
```

2. **Write a clear PR description:**
```markdown
## Summary
[Brief description of what this PR does]

## Motivation
[Why is this change needed?]

## Changes
- [List key changes]
- [Be specific]

## Testing
[How did you test this?]

## Screenshots (if applicable)
[Add before/after screenshots for UI changes]
```

3. **Follow the commit message format:**
```bash
git commit -m "Add: Brief description of addition"
git commit -m "Fix: Brief description of fix"
git commit -m "Update: Brief description of update"
git commit -m "Docs: Brief description of doc change"
```

4. **Push and create PR:**
```bash
git push origin feature/your-feature-name
# Then create PR on GitHub
```

## 📝 Command File Template

When creating a new command file, use this structure:

```markdown
# Command Name

You are the **[Agent Name]**, [brief description of agent expertise].

## Your Mission
[What this command accomplishes]

## Context
- **Input Files:** [What files are read]
- **Output Files:** [What files are generated]
- **User Input:** [What user must provide]

## Golden Rules
1. [Key constraint 1]
2. [Key constraint 2]
3. [Key constraint 3]

## Process

### Step 1: [First Step Name]
[Detailed instructions]

### Step 2: [Second Step Name]
[Detailed instructions]

### Step 3: [Output Generation]
[What to create and format]

## Output Structure
```markdown
# [Output File Template]
[Show expected structure]
```

## Human Decision Point
[When to stop and wait for user input]

## Important Reminders
- [Critical point 1]
- [Critical point 2]
```

## 🐛 Reporting Bugs

Found a bug? Please open an issue with:

1. **Clear title**: "Bug: CV generation fails with special characters"
2. **Description**: What happened vs. what you expected
3. **Steps to reproduce**: Exact steps to trigger the bug
4. **Environment**: OS, Claude Code version, etc.
5. **Relevant logs**: Error messages (remove personal info!)

## 💡 Suggesting Features

Have an idea? Open an issue with:

1. **Use case**: What problem does this solve?
2. **Proposed solution**: How would it work?
3. **Alternatives considered**: Other approaches you thought about
4. **Mockups** (if applicable): Screenshots or diagrams

## 🎨 Style Guidelines

### Markdown Files
- Use proper heading hierarchy (##, ###, ####)
- Include examples for complex concepts
- Keep paragraphs short (3-5 lines max)
- Use lists for readability
- Add code blocks for commands

### Command Files
- Be explicit and detailed in agent instructions
- Include safety checks (anti-hallucination measures)
- Add examples of good vs. bad outputs
- Specify output file formats
- Include human review gates

### Documentation
- Write for beginners
- Assume no prior AI/automation knowledge
- Provide context and "why" not just "how"
- Use consistent terminology
- Add visual aids when helpful

## 🏆 Recognition

Contributors will be:
- Listed in README.md credits section
- Thanked in release notes
- Mentioned in documentation they helped create

## 📞 Questions?

- **General questions:** Open a GitHub issue with "Question:" prefix
- **Security concerns:** Email maintainer directly (see README)
- **Feature discussions:** Use GitHub Discussions

## 📚 Resources

**Helpful for Contributors:**
- [Claude Code Documentation](https://docs.claude.com/claude-code)
- [Markdown Guide](https://www.markdownguide.org/)
- [Pandoc Documentation](https://pandoc.org/MANUAL.html)
- [Eisvogel Template](https://github.com/Wandmalfarbe/pandoc-latex-template)

**Project Documentation:**
- [README.md](README.md) - Project overview
- [USAGE-GUIDE.md](USAGE-GUIDE.md) - How to use the system
- [SETUP.md](SETUP.md) - Initial setup instructions
- [GIT-SETUP-GUIDE.md](GIT-SETUP-GUIDE.md) - Publishing safely

## 🎖️ Types of Contributors We Need

**Beginner Friendly:**
- Documentation improvements
- Example additions
- Typo fixes
- Industry-specific CV format suggestions

**Intermediate:**
- New command templates
- CV tailoring improvements
- Analytics enhancements
- Testing and bug reports

**Advanced:**
- Integration with other tools
- Automation improvements
- Architecture enhancements
- Performance optimizations

## ✅ Checklist Before Submitting PR

- [ ] Tested changes end-to-end
- [ ] No personal data in commits
- [ ] Documentation updated
- [ ] Examples added (if applicable)
- [ ] Follows existing patterns and style
- [ ] .gitignore still protects personal data
- [ ] PR description is clear and complete
- [ ] Commit messages are descriptive

---

**Thank you for contributing to help job seekers automate their search!** 🎯

Every contribution—big or small—makes the job search easier for someone.
