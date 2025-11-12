# Privacy Protection System

**Last Updated:** 2025-11-12
**Purpose:** Prevent accidental commits of personal data to GitHub

---

## Why This Matters

This job search system contains **highly sensitive personal information**:
- Your career preferences (visa status, compensation expectations, family details)
- Job shortlists with company names (reveals your job search strategy)
- Application materials (CVs, cover letters with personal achievements)
- Metrics and analytics (rejection patterns, fit scores, strategic decisions)

**Public GitHub repositories are searchable** by recruiters, employers, and search engines. Accidentally committing personal data could:
- ❌ Expose your job search to current employer
- ❌ Reveal compensation expectations to recruiters
- ❌ Share visa/immigration status publicly
- ❌ Leak strategic job search decisions

---

## 3-Layer Protection System

### Layer 1: .gitignore (First Defense)

**Location:** `.gitignore` (root directory)

**Protected folders:**
```gitignore
# Folders with personal data (NEVER committed)
applications/       # All job applications
master/            # Master CV and personal documents
archive/           # Old applications
staging/           # Draft applications
insights/          # Personal metrics and analytics

# Personal configuration files
career-preferences.md    # Your career goals, visa status, compensation
MASTER-SHORTLIST.md     # Your job targets and strategy
```

**How it works:**
- Blocks `git add` for ignored files
- Shows warning: "The following paths are ignored by one of your .gitignore files"
- Can be bypassed with `git add -f` (force) ⚠️

**Test it:**
```bash
# Should fail with warning
git add career-preferences.md

# Shows file is ignored
git check-ignore -v career-preferences.md
```

---

### Layer 2: Pre-commit Hook (Second Defense)

**Location:** `.git/hooks/pre-commit`

**How it works:**
- Runs automatically before every commit
- Scans staged files for sensitive patterns
- Blocks commit if personal data detected
- Cannot be bypassed (unless using `--no-verify`)

**What it checks:**
```bash
# Exact filename matches
career-preferences.md
MASTER-SHORTLIST.md

# Pattern matches
applications/2025-*           # Application folders
master/*.docx                 # Master CV files
*_PRIVATE.md                  # Private files
*-personal.md                 # Personal files
insights/metrics-dashboard.md # Personal metrics

# Content patterns
Polish passport               # Citizenship info
Married to                    # Family details
Bromley                       # Specific location
£XXXk                        # Salary figures
Email addresses              # Contact info
```

**Test it:**
```bash
# Try to commit personal file (should block)
git add -f career-preferences.md
git commit -m "test"

# Output:
# 🚫 COMMIT BLOCKED: Personal data protection
# Files blocked: 1
```

**If hook blocks your commit:**
```bash
# Remove from staging
git reset HEAD <filename>

# Use template version instead
git add career-preferences.template.md
```

**Emergency bypass (NOT RECOMMENDED):**
```bash
# Bypasses pre-commit hook - use only if you're CERTAIN it's safe
git commit --no-verify
```

---

### Layer 3: Template Pattern (Third Defense)

**How it works:**
- Personal files (`.md`) are gitignored
- Template files (`.template.md`) are tracked in git
- New users copy templates and customize

**Files using template pattern:**

| Template File (Tracked ✓) | Personal File (Gitignored ✓) | Contains |
|---------------------------|------------------------------|----------|
| `career-preferences.template.md` | `career-preferences.md` | Visa status, compensation, relocation preferences |
| `MASTER-SHORTLIST.template.md` | `MASTER-SHORTLIST.md` | Company names, role priorities, your strategy |

**Setup for new users:**
```bash
# Copy templates to create personal files
cp career-preferences.template.md career-preferences.md
cp MASTER-SHORTLIST.template.md MASTER-SHORTLIST.md

# Edit personal files (automatically gitignored)
# Templates remain tracked for reference
```

---

## What Files Are Safe to Commit?

### ✅ SAFE (No Personal Data)

**System files:**
- `requirements.txt` - Python dependencies
- `scripts/*.py` - Analysis and automation scripts
- `.claude/commands/*.md` - Claude Code command definitions
- `docs/` - Documentation and guides
- `tests/` - Test files

**Template files:**
- `career-preferences.template.md` - Generic structure
- `MASTER-SHORTLIST.template.md` - Example shortlist
- `applications/_example-application/` - Example application structure

**Aggregate files:**
- `STATUS.md` - Auto-generated, no company-specific details
- `ROADMAP.md` - Feature plans and improvements

### ⚠️ CAREFUL (May Contain Personal Data)

**Context-dependent:**
- `.claude/commands/*.md` - If contains example company names, sanitize first
- `docs/guides/*.md` - If contains your specific examples, use placeholders
- Any file mentioning specific companies, salaries, or locations

### ❌ NEVER COMMIT (Personal Data)

**Always excluded:**
- `career-preferences.md` - Visa, salary, family details
- `MASTER-SHORTLIST.md` - Company names, your strategy
- `applications/*/` - CVs, cover letters, job descriptions
- `master/*.docx` - Master CV files
- `insights/*.md` - Your metrics, rejection patterns
- `staging/*` - Draft applications
- `archive/*` - Old applications
- Any file with `_PRIVATE`, `-personal`, or `PRIVATE` in name

---

## How to Verify Protection is Working

### Test 1: Check .gitignore

```bash
# Verify personal files are ignored
git check-ignore -v career-preferences.md MASTER-SHORTLIST.md

# Expected output:
# .gitignore:170:career-preferences.md	career-preferences.md
# .gitignore:173:MASTER-SHORTLIST.md	MASTER-SHORTLIST.md
```

### Test 2: Check Local Files Exist

```bash
# Verify personal files are still on disk (not deleted)
ls -lh career-preferences.md MASTER-SHORTLIST.md

# Expected output:
# -rw-r--r-- ... 10K ... career-preferences.md
# -rw-r--r-- ... 9.3K ... MASTER-SHORTLIST.md
```

### Test 3: Test Pre-commit Hook

```bash
# Try to add ignored file (should warn)
git add career-preferences.md

# Try to force-add and commit (should block)
git add -f career-preferences.md
git commit -m "test"

# Expected output:
# 🚫 COMMIT BLOCKED: Personal data protection
```

### Test 4: Check Git Status

```bash
git status

# Should NOT show:
# - career-preferences.md
# - MASTER-SHORTLIST.md
# - applications/
# - insights/metrics-dashboard.md
```

---

## What If Personal Data Was Already Committed?

If personal data was committed before these protections were added:

### Option 1: Remove from Git History (Recommended for Public Repos)

**⚠️ WARNING:** This rewrites git history. Only do this if:
- Repository is not shared with others
- Or you can coordinate with all collaborators

```bash
# Remove file from all git history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch career-preferences.md" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (rewrites history on GitHub)
git push origin --force --all
git push origin --force --tags

# Clean up
git for-each-ref --format="delete %(refname)" refs/original | git update-ref --stdin
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

### Option 2: Make Repository Private (Simpler)

```bash
# On GitHub: Settings → Danger Zone → Change visibility → Make private
```

### Option 3: Delete and Recreate Repository

```bash
# Nuclear option - start fresh
# 1. Backup your work
# 2. Delete GitHub repository
# 3. Create new repository
# 4. Push clean history
```

---

## Prevention Checklist (Use Before Every Push)

Before running `git push`:

- [ ] Run `git status` - No personal files listed?
- [ ] Run `git diff --cached` - Review all staged changes
- [ ] Check commit includes no company names, salaries, or personal details
- [ ] Pre-commit hook ran and passed (automatic)
- [ ] If unsure, ask: "Would I be comfortable with my current employer seeing this?"

---

## How to Disable Protection (NOT RECOMMENDED)

If you absolutely need to disable protection (e.g., private repository for personal backup):

### Disable Pre-commit Hook

```bash
# Rename hook to disable it
mv .git/hooks/pre-commit .git/hooks/pre-commit.disabled

# Or bypass for single commit
git commit --no-verify
```

### Remove .gitignore Entries

```bash
# Edit .gitignore and comment out personal files
# career-preferences.md
# MASTER-SHORTLIST.md
```

**⚠️ WARNING:** Only do this for truly private repositories. GitHub private repos can:
- Be accidentally made public
- Be accessed if you leave an organization
- Be forked (if settings allow)

---

## Troubleshooting

### Problem: "File not found" when copying templates

**Solution:**
```bash
# Check templates exist
ls *template.md

# If missing, pull from git
git checkout main -- career-preferences.template.md MASTER-SHORTLIST.template.md
```

### Problem: Pre-commit hook not running

**Solution:**
```bash
# Check hook exists and is executable
ls -la .git/hooks/pre-commit

# Make executable (Unix/Mac)
chmod +x .git/hooks/pre-commit

# Test manually
.git/hooks/pre-commit
```

### Problem: Can't commit anything (hook too strict)

**Solution:**
```bash
# Check what files are staged
git diff --cached --name-only

# Remove problem files
git reset HEAD <filename>

# Bypass for legitimate commit (CAREFUL!)
git commit --no-verify
```

### Problem: Personal file accidentally committed

**Solution:**
```bash
# If not pushed yet - amend last commit
git reset HEAD~1
git reset HEAD <personal-file>
git commit -c ORIG_HEAD

# If already pushed - see "Remove from Git History" above
```

---

## Best Practices

1. **Never use `git add .`** - Always add files explicitly
2. **Review diffs before committing** - Run `git diff --cached`
3. **Use descriptive commit messages** - Helps identify what changed
4. **Test protection regularly** - Run verification tests monthly
5. **Keep templates updated** - When structure changes, update `.template.md` files
6. **Don't trust .gitignore alone** - Use all 3 layers of protection
7. **Assume public by default** - Even private repos can be exposed

---

## Related Documentation

- `.gitignore` - List of ignored files and patterns
- `docs/reference/PROJECT-GUIDE.md` - Overall project architecture
- `.git/hooks/pre-commit` - Pre-commit hook source code
- `README.md` - Getting started guide

---

## Support

If you accidentally commit personal data:

1. **DON'T PANIC** - It's fixable
2. **DON'T PUSH** - If not pushed yet, easier to fix
3. **Check the commit** - `git show HEAD`
4. **Choose a fix** - See "What If Personal Data Was Already Committed?" above
5. **Verify fix** - Ensure data is removed from history

**Remember:** Prevention is easier than cleanup. Use all 3 protection layers.

---

**Last Updated:** 2025-11-12
**Next Review:** 2026-01-12 (Quarterly)
