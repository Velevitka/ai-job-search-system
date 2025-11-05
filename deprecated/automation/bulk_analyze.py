#!/usr/bin/env python3
"""
Bulk analyze job postings from staging folder
"""

import re
import sys
import codecs
from pathlib import Path
from datetime import datetime
from extract_mhtml import extract_job_info_from_mhtml

# Force UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'ignore')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'ignore')


# Career preferences for filtering and scoring
PREFERENCES = {
    'locations_high_priority': ['london', 'remote uk', 'uk', 'united kingdom'],
    'locations_medium_priority': ['amsterdam', 'dublin', 'berlin', 'cologne', 'eu', 'europe', 'singapore', 'dubai', 'manila', 'seoul', 'bangkok'],
    'locations_reject': ['saudi arabia', 'vietnam', 'united states', 'san francisco'],
    'keywords_high_value': [
        'data platform', 'cdp', 'customer data platform', 'martech', 'adtech',
        'growth', 'experimentation', 'a/b testing', 'marketplace', 'two-sided platform',
        'travel', 'hospitality', 'hotels', 'airline'
    ],
    'keywords_medium_value': [
        'product management', 'product manager', 'product lead', 'director',
        'ai product', 'ml product', 'platform', 'payments', 'fintech'
    ],
    'seniority_target': ['director', 'head of', 'vp', 'vice president', 'lead', 'principal'],
    'role_reject_keywords': ['engineer', 'engineering manager', 'software engineer', 'b2b only']
}


def calculate_fit_score(job_info):
    """Calculate fit score based on quick heuristics"""
    description = job_info.get('description', '').lower()
    job_title = job_info.get('job_title', '').lower()
    company = job_info.get('company', '').lower()

    score = 5.0  # Base score
    reasons = []
    concerns = []

    # Auto-reject based on location
    for reject_loc in PREFERENCES['locations_reject']:
        if reject_loc in description or reject_loc in job_title:
            return 1.0, [f"❌ Requires relocation to {reject_loc}"], []

    # Auto-reject if pure engineering role
    if 'engineer' in job_title and 'product' not in job_title:
        return 2.0, [f"❌ Engineering role, not Product Management"], []

    # Location scoring
    location_match = False
    for loc in PREFERENCES['locations_high_priority']:
        if loc in description or loc in job_title:
            score += 2.0
            reasons.append(f"✅ Location: {loc.title()}")
            location_match = True
            break

    if not location_match:
        for loc in PREFERENCES['locations_medium_priority']:
            if loc in description or loc in job_title:
                score += 1.0
                reasons.append(f"⭐ Location: {loc.title()}")
                location_match = True
                break

    if not location_match:
        concerns.append("⚠️ Location not in preferred list")
        score -= 1.0

    # High-value keyword matching
    keyword_score = 0
    matched_keywords = []
    for keyword in PREFERENCES['keywords_high_value']:
        if keyword in description or keyword in job_title:
            keyword_score += 1.5
            matched_keywords.append(keyword)

    if matched_keywords:
        score += min(keyword_score, 3.0)  # Cap at 3 points
        reasons.append(f"✅ Keywords: {', '.join(matched_keywords[:3])}")

    # Medium-value keyword matching
    for keyword in PREFERENCES['keywords_medium_value']:
        if keyword in description or keyword in job_title:
            score += 0.5
            break

    # Seniority match
    seniority_match = False
    for level in PREFERENCES['seniority_target']:
        if level in job_title:
            if level in ['director', 'head of', 'vp', 'vice president']:
                score += 2.0
                reasons.append(f"✅ Seniority: {level.title()}")
            else:
                score += 1.0
                reasons.append(f"⭐ Seniority: {level.title()}")
            seniority_match = True
            break

    if not seniority_match and 'senior' not in job_title:
        concerns.append("⚠️ May be junior role")
        score -= 0.5

    # Industry/domain bonuses
    if any(word in description or word in job_title for word in ['travel', 'hospitality', 'hotel', 'airline', 'booking']):
        score += 1.5
        reasons.append("✅ Travel/hospitality domain (strong fit)")

    if any(word in description or word in job_title for word in ['martech', 'adtech', 'advertising', 'marketing technology']):
        score += 1.0
        reasons.append("✅ MarTech/AdTech domain")

    # Cap score at 10
    score = min(score, 10.0)
    score = max(score, 1.0)

    return round(score, 1), reasons[:5], concerns[:3]


def analyze_all_jobs(staging_dir='staging'):
    """Analyze all jobs in staging directory"""
    staging_path = Path(staging_dir)

    # Find all mhtml files
    mhtml_files = list(staging_path.glob('*.mhtml'))

    print(f"📊 Found {len(mhtml_files)} job postings to analyze...")
    print()

    results = []

    for i, filepath in enumerate(mhtml_files, 1):
        print(f"Analyzing {i}/{len(mhtml_files)}: {filepath.name[:60]}...")

        job_info = extract_job_info_from_mhtml(filepath)

        if job_info and 'error' not in job_info:
            fit_score, reasons, concerns = calculate_fit_score(job_info)

            results.append({
                'filename': filepath.name,
                'filepath': filepath,
                'company': job_info['company'],
                'job_title': job_info['job_title'],
                'fit_score': fit_score,
                'reasons': reasons,
                'concerns': concerns,
                'description': job_info['description']
            })
        else:
            print(f"  ⚠️ Error extracting: {job_info.get('error', 'Unknown error')}")

    # Sort by fit score (highest first)
    results.sort(key=lambda x: x['fit_score'], reverse=True)

    return results


def generate_markdown_report(results):
    """Generate markdown bulk analysis report"""
    today = datetime.now().strftime('%Y-%m-%d')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M UTC')

    # Count by priority
    high_priority = [r for r in results if r['fit_score'] >= 8.0]
    medium_priority = [r for r in results if 6.0 <= r['fit_score'] < 8.0]
    low_priority = [r for r in results if 4.0 <= r['fit_score'] < 6.0]
    skip = [r for r in results if r['fit_score'] < 4.0]

    # Start report
    report = f"""# Bulk Job Analysis - {today}

**Analyzed:** {timestamp}
**Jobs Reviewed:** {len(results)}
**Source:** staging/ folder

---

## Executive Summary

**Priority Breakdown:**
- 🔥 **High Priority (8-10):** {len(high_priority)} jobs - APPLY FIRST
- ⭐ **Medium Priority (6-7):** {len(medium_priority)} jobs - Apply if time
- ⚠️ **Low Priority (4-5):** {len(low_priority)} jobs - Only if strategic
- ❌ **Skip (1-3):** {len(skip)} jobs - Poor fit

**Time Investment Estimate:**
- Top 5 high-priority roles: ~15-20 hours (3-4 hours each)
- All high-priority roles: ~{len(high_priority) * 3}-{len(high_priority) * 4} hours

---

## Quick Prioritization Table

| Rank | Fit | Company | Role | Priority | Top Strength |
|------|-----|---------|------|----------|--------------|
"""

    # Add top 20 to table
    for i, job in enumerate(results[:20], 1):
        priority = "🔥 High" if job['fit_score'] >= 8.0 else "⭐ Medium" if job['fit_score'] >= 6.0 else "⚠️ Low" if job['fit_score'] >= 4.0 else "❌ Skip"
        strength = job['reasons'][0] if job['reasons'] else "See details"
        strength = strength.replace('✅', '').replace('⭐', '').strip()[:40]
        report += f"| {i} | {job['fit_score']}/10 | {job['company'][:25]} | {job['job_title'][:30]} | {priority} | {strength} |\n"

    if len(results) > 20:
        report += f"\n*... and {len(results) - 20} more (see detailed breakdown below)*\n"

    report += """
---

## 🔥 High Priority Roles (Fit 8-10)

**Action: Apply within next 24-48 hours**

"""

    for i, job in enumerate(high_priority, 1):
        report += f"""### {i}. {job['company']} - {job['job_title']} - Fit: {job['fit_score']}/10

**Source File:** `{job['filename']}`

**Why High Fit:**
"""
        for reason in job['reasons']:
            report += f"{reason}\n"

        if job['concerns']:
            report += "\n**Considerations:**\n"
            for concern in job['concerns']:
                report += f"{concern}\n"

        report += f"""
**Next Steps:**
```bash
# Analyze this role in detail
/analyze-job {job['company'].replace(' ', '')}

# Then generate CV and cover letter
/generate-cv {job['company'].replace(' ', '')}
/generate-cl {job['company'].replace(' ', '')}
```

---

"""

    report += """
## ⭐ Medium Priority Roles (Fit 6-7)

**Action: Review and apply if you have capacity after high-priority roles**

"""

    for i, job in enumerate(medium_priority[:10], 1):
        report += f"""### {i}. {job['company']} - {job['job_title']} - Fit: {job['fit_score']}/10

**Why Worth Considering:**
"""
        for reason in job['reasons'][:3]:
            report += f"{reason}\n"

        if job['concerns']:
            report += f"\n**Concerns:** {', '.join(job['concerns'])}\n"

        report += "\n---\n\n"

    if len(medium_priority) > 10:
        report += f"\n*... and {len(medium_priority) - 10} more medium-priority roles*\n"

    report += """
## ⚠️ Low Priority & Skip Roles

**Total to skip:** """ + str(len(low_priority) + len(skip)) + """ roles

These roles have significant gaps or misalignment. Only consider if you have a specific strategic reason.

"""

    report += """
---

## Recommended Application Strategy

### This Week (Priority 1)

**Focus on these top 5 roles:**

"""

    for i, job in enumerate(high_priority[:5], 1):
        report += f"""**{i}. {job['company']} - {job['job_title']}** (Fit: {job['fit_score']}/10)
   - Time estimate: 3-4 hours (analysis + CV + CL)
   - Key strength: {job['reasons'][0] if job['reasons'] else 'See details'}
"""

    report += f"""
**Total time investment:** {min(len(high_priority[:5]), len(high_priority)) * 3}-{min(len(high_priority[:5]), len(high_priority)) * 4} hours

### Next Week (Priority 2)

If interviews haven't started, continue with remaining high-priority roles ({max(0, len(high_priority) - 5)} remaining).

### File Management

After reviewing this analysis:

**Move to proper folders:**
```bash
# Create tier folders
mkdir -p staging/tier1-apply-now
mkdir -p staging/tier2-research
mkdir -p staging/tier3-maybe
mkdir -p staging/archive

# Move files (do this automatically or manually)
```

**Files will be organized by fit score:**
- `tier1-apply-now/` - Fit 8-10 ({len(high_priority)} files)
- `tier2-research/` - Fit 6-7 ({len(medium_priority)} files)
- `tier3-maybe/` - Fit 4-5 ({len(low_priority)} files)
- `archive/` - Fit 1-3 ({len(skip)} files)

---

## Next Actions

- [ ] Review this full analysis
- [ ] Decide on top 5 roles to pursue this week
- [ ] Run `/analyze-job [company]` for each priority role
- [ ] Generate tailored CVs and cover letters
- [ ] Submit applications
- [ ] Track in application folders

**Suggested workflow for each role:**
```bash
/analyze-job [paste-job-description]
/generate-cv CompanyName
/generate-cl CompanyName
/update-status CompanyName applied
```

---

**Auto-generated by:** `/bulk-process` command
**Last Generated:** {timestamp}
**Source:** `staging/` folder ({len(results)} MHTML files analyzed)
"""

    return report


def main():
    """Main execution"""
    print("🚀 Bulk Job Analysis Starting...")
    print()

    results = analyze_all_jobs('staging')

    print()
    print(f"✅ Analysis complete! {len(results)} jobs analyzed")
    print()

    # Generate markdown report
    report = generate_markdown_report(results)

    # Save report
    today = datetime.now().strftime('%Y-%m-%d')
    report_path = Path(f'insights/bulk-analysis-{today}.md')
    report_path.parent.mkdir(exist_ok=True)

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"📄 Report saved: {report_path}")
    print()

    # Display summary
    high_priority = [r for r in results if r['fit_score'] >= 8.0]
    medium_priority = [r for r in results if 6.0 <= r['fit_score'] < 8.0]

    print("=" * 70)
    print("📊 BULK ANALYSIS SUMMARY")
    print("=" * 70)
    print()
    print(f"**Jobs analyzed:** {len(results)}")
    print(f"**High priority (8-10):** {len(high_priority)} jobs 🔥")
    print(f"**Medium priority (6-7):** {len(medium_priority)} jobs ⭐")
    print()
    print("**Top 5 Recommendations:**")
    print()
    for i, job in enumerate(results[:5], 1):
        print(f"{i}. [{job['fit_score']}/10] {job['company']} - {job['job_title']}")
        if job['reasons']:
            print(f"   {job['reasons'][0]}")
    print()
    print("=" * 70)
    print()
    print(f"📁 Full analysis: insights/bulk-analysis-{today}.md")
    print()
    print("Next steps:")
    print("1. Review full report")
    print("2. Run /analyze-job for top priority roles")
    print("3. Generate CVs and cover letters")
    print()


if __name__ == '__main__':
    main()
