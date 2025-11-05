# Git Setup Guide - Publishing to GitHub

This guide helps you safely publish the **system/commands** to GitHub while keeping your **personal data** private.

## ⚠️ Safety First: Two-Repository Approach

We use TWO separate repositories to ensure zero risk of leaking personal data:

### Repository 1: PUBLIC - System Repository
**Contains:** Commands, documentation, templates
**Does NOT contain:** Your CV, applications, or personal information

### Repository 2: PRIVATE (Optional) - Your Personal Data
**Contains:** Your actual master CV, applications, insights
**Recommendation:** Don't version control this, or use private GitHub repo

---

## Quick Start: Publishing the Public Repository

### Step 1: Verify .gitignore Protection

The `.gitignore` file is already configured to protect all personal data. Let's verify it's working:

```bash
cd "C:\Users\ArturSwadzba\OneDrive\4. CV"

# Test: See what git would commit (should be ONLY system files)
git status --porcelain --ignored
```

**Expected result:** Only these files/folders should be tracked:
- `.claude/commands/`
- `.gitignore`
- `README-PUBLIC.md` (will become README.md)
- `SETUP.md`
- `USAGE-GUIDE.md`
- `GIT-SETUP-GUIDE.md` (this file)
- Placeholder READMEs in master/, applications/, insights/

**SHOULD BE IGNORED (safe):**
- `master/ArturSwadzba_MasterCV.*`
- `applications/2025-*` (all your real applications)
- `insights/metrics-dashboard.md`, `patterns.md`
- All `.pdf` and `.docx` files

### Step 2: Prepare for Public Release

1. **Rename README for public:**
```bash
mv README.md README-PERSONAL.md
mv README-PUBLIC.md README.md
```

2. **Initialize git repository:**
```bash
git init
git add .
```

3. **Review what will be committed:**
```bash
git status
```

**STOP HERE.** Carefully review the list. You should see:
- ✅ Command files (.claude/commands/)
- ✅ Documentation (README.md, SETUP.md, etc.)
- ✅ .gitignore
- ✅ Placeholder READMEs
- ❌ NO .docx or .pdf files
- ❌ NO files with your name/contact info
- ❌ NO application folders with company names

4. **If everything looks safe, commit:**
```bash
git commit -m "Initial commit: AI-powered job application system

- Claude Code command files for job analysis and CV generation
- Documentation and setup guides
- .gitignore configured to protect personal data
- Template folder structure"
```

### Step 3: Create GitHub Repository

1. Go to https://github.com/new

2. Create a **public** repository:
   - Name: `ai-job-search-system` (or your preferred name)
   - Description: "AI-powered job application management system using Claude Code"
   - Public ✅
   - Do NOT initialize with README (we already have one)

3. Push your local repository:
```bash
# Replace 'yourusername' with your GitHub username
git remote add origin https://github.com/yourusername/ai-job-search-system.git
git branch -M main
git push -u origin main
```

### Step 4: Verify on GitHub

1. Go to your repository on GitHub
2. Check that ONLY system files are present
3. Verify NO personal data is visible
4. Check that README.md renders correctly

**Checklist:**
- [ ] No files with "Artur" or your name in filename
- [ ] No .docx or .pdf files
- [ ] No company names from your applications
- [ ] No phone number or email visible
- [ ] Command files are present
- [ ] Documentation is present

---

## Maintaining the Repository

### Adding New Commands or Documentation

```bash
# 1. Make changes to command files or documentation
# 2. Check what changed
git status

# 3. Add only the system files
git add .claude/commands/
git add README.md SETUP.md USAGE-GUIDE.md

# 4. Commit
git commit -m "Update: [describe your changes]"

# 5. Push
git push
```

### Before Every Push: Safety Check

**ALWAYS run this before pushing:**
```bash
# See what will be pushed
git diff HEAD origin/main

# Verify no personal data
git show HEAD
```

**Red flags to look for:**
- Personal name in file contents
- Phone number or email
- Specific company names from your applications
- Any .docx or .pdf files

---

## What to Share, What to Keep Private

### ✅ SAFE TO SHARE (Public Repo)

**Command Files:**
- `.claude/commands/*.md` - All agent command files
- These are templates, no personal data

**Documentation:**
- `README.md` (genericized version)
- `SETUP.md`
- `USAGE-GUIDE.md`
- `GIT-SETUP-GUIDE.md`
- Placeholder READMEs for folders

**System Configuration:**
- `.gitignore`
- Folder structure documentation

### ❌ NEVER SHARE (Keep Local Only)

**Personal Documents:**
- `master/` folder contents (your actual CV)
- `applications/` folder contents (your applications)
- `insights/` folder contents (your metrics)
- All `.docx` and `.pdf` files

**Personal Information:**
- Any file with your contact information
- Company-specific applications
- Interview transcripts
- Personal tracking data

---

## Alternative: Private Repository for Personal Data

If you want version control for your personal data:

```bash
# In a DIFFERENT directory
mkdir ~/my-job-search-private
cd ~/my-job-search-private

# Copy only personal data
cp -r "C:\Users\ArturSwadzba\OneDrive\4. CV\master" .
cp -r "C:\Users\ArturSwadzba\OneDrive\4. CV\applications" .
cp -r "C:\Users\ArturSwadzba\OneDrive\4. CV\insights" .

# Create a PRIVATE GitHub repository
git init
git add .
git commit -m "Private: My job search data"
git remote add origin https://github.com/yourusername/my-job-search-PRIVATE.git
git push -u origin main
```

**Make ABSOLUTELY SURE this repository is set to PRIVATE on GitHub.**

---

## Troubleshooting

### "Git wants to commit my personal files!"

**Solution:**
```bash
# Remove from git tracking (keeps local file)
git rm --cached <filename>

# Or remove entire folder from tracking
git rm -r --cached master/
git rm -r --cached applications/

# Then add to .gitignore if not already there
echo "master/" >> .gitignore
echo "applications/" >> .gitignore

# Commit the .gitignore update
git add .gitignore
git commit -m "Update .gitignore to protect personal data"
```

### "I accidentally committed personal data!"

**If not pushed yet:**
```bash
# Undo last commit, keep changes
git reset --soft HEAD~1

# Remove the personal files
git rm --cached <personal-file>

# Update .gitignore
echo "<personal-file>" >> .gitignore

# Recommit without personal data
git add .
git commit -m "System files only"
```

**If already pushed to GitHub:**
```bash
# Nuclear option: Remove from entire history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch <personal-file>" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (rewrites history)
git push origin --force --all

# Then make the file private immediately on GitHub if visible
```

### "How do I know what's safe to commit?"

**Run this test:**
```bash
# See exactly what git sees
git diff --cached

# See what would be committed
git status

# Check each file manually
git diff --cached <filename>
```

**Safe files have:**
- ✅ No personal names
- ✅ No contact information
- ✅ No company names from YOUR applications
- ✅ Generic template language only

---

## Sample .gitignore Testing

Test your .gitignore is working:

```bash
# This should show personal files as "Ignored"
git status --ignored

# This should show NO personal files
git status

# This should only show system files
git ls-files
```

---

## Collaboration & Contributions

If others want to contribute to your public system:

1. **They fork your repo**
2. **They make changes to command files or docs**
3. **They submit pull request**
4. **You review for:**
   - No personal data
   - No breaking changes
   - Quality improvements

**Never accept PRs that include:**
- Personal information
- Specific CVs or applications
- Hardcoded names or contact details

---

## Best Practices

1. **Always review before pushing**
2. **Use two separate repos (public system, private data)**
3. **Test .gitignore regularly**
4. **Keep README.md generic** (no personal references)
5. **Document improvements** that others can benefit from
6. **Never commit secrets** (API keys, tokens, credentials)

---

## Summary Checklist

Before making your first push:

- [ ] .gitignore file is in place
- [ ] README-PUBLIC.md renamed to README.md
- [ ] README.md has no personal information
- [ ] Ran `git status` - only system files listed
- [ ] No .docx or .pdf files in git
- [ ] No folders with company names
- [ ] No personal contact information visible
- [ ] Created GitHub repo as PUBLIC
- [ ] Pushed and verified on GitHub
- [ ] Double-checked no personal data visible

---

**You're ready to publish!** 🚀

Your AI-powered job application system is now open source while your personal data stays private and secure.
