# Pre-Publish Checklist

Before pushing to GitHub, run through this checklist to ensure NO personal data is exposed.

## ✅ Quick Verification (Run These Commands)

```bash
cd "C:\Users\ArturSwadzba\OneDrive\4. CV"

# 1. Test what git will track
git init
git add .
git status

# 2. Check for your name in files that will be committed
git diff --cached | grep -i "Artur"
# (Should only appear in LICENSE and CONTRIBUTING as generic examples)

# 3. Check for your email
git diff --cached | grep -i "artur@swadzba"
# (Should be ZERO matches)

# 4. Check for your phone
git diff --cached | grep -i "7383 431055"
# (Should be ZERO matches)

# 5. List all files that WILL be committed
git ls-files
```

## 📋 Expected Files to Commit

**Should See (✅):**
- `.gitignore`
- `.claude/commands/*.md` (all command files)
- `README.md` (the public version, renamed from README-PUBLIC.md)
- `SETUP.md`
- `USAGE-GUIDE.md`
- `GIT-SETUP-GUIDE.md`
- `PRE-PUBLISH-CHECKLIST.md` (this file)
- `CONTRIBUTING.md`
- `LICENSE`
- `master/README.md` (placeholder)
- `applications/README.md` (placeholder)
- `applications/_example-application/` (example folder)
- `insights/README.md` (placeholder)

**Should NOT See (❌):**
- `master/ArturSwadzba_MasterCV.*`
- `applications/2025-*` (your real applications)
- `applications/*/ArturSwadzba_*` (your actual CVs)
- Any `.pdf` or `.docx` files
- `insights/metrics-dashboard.md`
- `insights/patterns.md`
- `README-PERSONAL.md`

## 🔍 Manual Verification Steps

### Step 1: Check README.md
```bash
cat README.md | head -20
```

**Verify:**
- [ ] Title is generic (no "Artur Swadzba's")
- [ ] No personal information
- [ ] Examples use placeholder names
- [ ] Links are generic

### Step 2: Check .gitignore
```bash
cat .gitignore | grep "master/"
cat .gitignore | grep "applications/"
cat .gitignore | grep "*.docx"
```

**Verify:**
- [ ] `master/` is ignored
- [ ] `applications/` is ignored (except _example-application/)
- [ ] `.docx` files are blocked
- [ ] `.pdf` files are blocked

### Step 3: Check Example Application
```bash
cat applications/_example-application/job-description.md | grep -i "artur"
cat applications/_example-application/analysis.md | grep -i "artur"
```

**Verify:**
- [ ] Uses placeholder company (TechCorp, not real)
- [ ] Uses generic examples
- [ ] No real personal data
- [ ] References "Master CV" generically

### Step 4: Check Command Files
```bash
grep -r "Artur" .claude/commands/
grep -r "7383" .claude/commands/
grep -r "swadzba" .claude/commands/
```

**Verify:**
- [ ] No personal names in examples
- [ ] No phone numbers
- [ ] No email addresses
- [ ] All examples are generic

## 🚨 Red Flags to Look For

**If you see ANY of these, STOP and fix:**

1. **Your actual name in file contents** (except LICENSE and as example)
2. **Your phone number anywhere**
3. **Your email address**
4. **Real company names from your applications**
5. **Your actual CV files (.docx, .pdf)**
6. **Specific dates/details from your real job search**
7. **Real interview transcripts**
8. **Personal metrics or analytics**

## ✏️ Final Preparation Steps

### Before First Commit:

```bash
# 1. Rename READMEs
mv README.md README-PERSONAL.md
mv README-PUBLIC.md README.md

# 2. Verify renamed correctly
head README.md
# Should see: "# AI-Powered Job Application Management System"
# NOT: "Artur Swadzba's Product Management job search"

# 3. Initialize git (if not done)
git init

# 4. Add all files
git add .

# 5. PAUSE - Review what will be committed
git status
git diff --cached

# 6. Check file count (should be ~20-30 files)
git ls-files | wc -l

# 7. Final safety check - search for personal data
git diff --cached > /tmp/commit-preview.txt
grep -i "artur" /tmp/commit-preview.txt
grep -i "7383" /tmp/commit-preview.txt
grep -i "bromley" /tmp/commit-preview.txt
```

## ✅ Safe to Commit When:

- [ ] No personal data in `git diff --cached`
- [ ] Only system/template files in `git status`
- [ ] Example folder uses placeholder data
- [ ] README.md is the public version
- [ ] .gitignore blocks all personal files
- [ ] Verified with all search commands above

## 🚀 Ready to Commit

If all checks pass:

```bash
# Commit
git commit -m "Initial commit: AI-powered job application system

- Claude Code command files for automated job analysis
- CV tailoring with anti-hallucination safeguards
- Application tracking and analytics
- PDF generation via Pandoc + Eisvogel
- Comprehensive documentation and examples
- .gitignore configured to protect personal data"

# Verify commit contents one more time
git show HEAD

# Look for personal data in commit
git show HEAD | grep -i "artur"
# Should only see in LICENSE

git show HEAD | grep -i "7383"
# Should be ZERO matches

git show HEAD | grep -i "swadzba"
# Should only see in LICENSE or generic examples
```

## 🎯 Post-Commit Actions

After committing locally but BEFORE pushing:

1. **One more review:**
```bash
git log --stat
git show HEAD
```

2. **Check GitHub is ready:**
   - Created public repository on GitHub
   - Repository is set to PUBLIC
   - No personal repos accidentally selected

3. **Push with confidence:**
```bash
git remote add origin https://github.com/yourusername/ai-job-search-system.git
git branch -M main
git push -u origin main
```

4. **Verify on GitHub:**
   - Visit repository page
   - Check README renders correctly
   - Browse files - verify no personal data
   - Check commit history
   - Review any visible file contents

## 🔒 If You Find Personal Data After Pushing

**Immediate actions:**

1. **Make repository private:**
   - Go to Settings → Danger Zone → Change visibility

2. **Remove from git history:**
```bash
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/personal-file" \
  --prune-empty --tag-name-filter cat -- --all

git push origin --force --all
```

3. **Update .gitignore:**
```bash
echo "path/to/personal-file" >> .gitignore
git add .gitignore
git commit -m "Update .gitignore"
git push
```

4. **Make public again only after verified clean**

## 📞 Need Help?

- Review GIT-SETUP-GUIDE.md for detailed troubleshooting
- Test with a private repo first if unsure
- Ask a developer friend to review before making public
- When in doubt, keep it private until verified

---

## Summary: The Three Critical Checks

Before pushing, verify:

1. **`git diff --cached` contains NO personal data**
2. **`git status` shows ONLY system files**
3. **README.md is the public version (not personal)**

If all three pass, you're safe to publish! 🎉

---

**Last Updated:** 2025-01-30
