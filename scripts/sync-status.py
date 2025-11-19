#!/usr/bin/env python3
"""
Sync script to aggregate all application status files and regenerate derived views.
Parses all applications/*/status.md files and generates STATUS.md and metrics-dashboard.md
"""

import os
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Define base path
BASE_PATH = Path(r"C:\Users\ArturSwadzba\OneDrive\4. CV")
APPLICATIONS_PATH = BASE_PATH / "applications"

def parse_status_file(file_path):
    """Parse a status.md file and extract key metadata."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract metadata
        data = {
            'file_path': str(file_path),
            'folder_name': file_path.parent.name,
            'status': 'unknown',
            'fit_score': None,
            'last_updated': None,
            'analyzed_date': None,
            'company': None,
            'role': None,
            'location': None,
            'days_waiting': 0,
            'cv_generated': False,
            'cover_letter_generated': False,
            'applied_date': None,
            'interview_dates': [],
            'rejected_date': None,
            'withdrawn_date': None,
            'outcome': None
        }

        # Extract title (first line)
        title_match = re.search(r'# Application Status - (.+?) - (.+?)$', content, re.MULTILINE)
        if title_match:
            data['company'] = title_match.group(1).strip()
            data['role'] = title_match.group(2).strip()

        # Extract current status
        status_match = re.search(r'\*\*Current Status:\*\* (.+?)$', content, re.MULTILINE)
        if status_match:
            data['status'] = status_match.group(1).strip().lower()

        # Extract last updated
        updated_match = re.search(r'\*\*Last Updated:\*\* (.+?)$', content, re.MULTILINE)
        if updated_match:
            data['last_updated'] = updated_match.group(1).strip()

        # Extract fit score
        fit_match = re.search(r'\*\*Fit Score:\*\* ([\d\.]+)/10', content)
        if fit_match:
            data['fit_score'] = float(fit_match.group(1))

        # Extract analyzed date
        analyzed_match = re.search(r'\*\*Analyzed On:\*\* (.+?)$', content, re.MULTILINE)
        if analyzed_match:
            data['analyzed_date'] = analyzed_match.group(1).strip()

        # Extract location
        location_match = re.search(r'\*\*Location:\*\* (.+?)$', content, re.MULTILINE)
        if location_match:
            data['location'] = location_match.group(1).strip()

        # Check CV/Cover Letter generation
        data['cv_generated'] = bool(re.search(r'\*\*CV Version:\*\*.+?(?!Not generated)', content))
        data['cover_letter_generated'] = bool(re.search(r'\*\*Cover Letter:\*\*.+?(?!Not generated|No)', content))

        # Extract timeline events
        if '### Applied -' in content:
            applied_match = re.search(r'### Applied - (.+?)$', content, re.MULTILINE)
            if applied_match:
                data['applied_date'] = applied_match.group(1).strip()

        if '### Withdrawn -' in content:
            withdrawn_match = re.search(r'### Withdrawn - (.+?)$', content, re.MULTILINE)
            if withdrawn_match:
                data['withdrawn_date'] = withdrawn_match.group(1).strip()
                data['status'] = 'withdrawn'

        if '### Rejected -' in content:
            rejected_match = re.search(r'### Rejected - (.+?)$', content, re.MULTILINE)
            if rejected_match:
                data['rejected_date'] = rejected_match.group(1).strip()
                data['status'] = 'rejected'

        # Interview dates
        interview_matches = re.findall(r'### Interview .+ - (.+?)$', content, re.MULTILINE)
        data['interview_dates'] = [m.strip() for m in interview_matches]

        return data

    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None

def calculate_metrics(applications):
    """Calculate aggregate metrics from all applications."""
    metrics = {
        'total': len(applications),
        'by_status': defaultdict(int),
        'by_fit_score': defaultdict(int),
        'avg_fit_score': 0,
        'high_priority_count': 0,
        'cv_generated_count': 0,
        'cover_letter_count': 0,
        'applied_count': 0,
        'interview_count': 0,
        'rejected_count': 0,
        'withdrawn_count': 0,
        'analysis_phase_count': 0,
    }

    fit_scores = []

    for app in applications:
        # Count by status
        status = app['status']
        metrics['by_status'][status] += 1

        # Fit score stats
        if app['fit_score']:
            fit_scores.append(app['fit_score'])
            score_bucket = f"{int(app['fit_score'])}-{int(app['fit_score'])+0.9}"
            metrics['by_fit_score'][score_bucket] += 1

            if app['fit_score'] >= 8:
                metrics['high_priority_count'] += 1

        # CV/CL tracking
        if app['cv_generated']:
            metrics['cv_generated_count'] += 1
        if app['cover_letter_generated']:
            metrics['cover_letter_count'] += 1

        # Pipeline stages
        if app['applied_date']:
            metrics['applied_count'] += 1
        if app['interview_dates']:
            metrics['interview_count'] += 1
        if app['rejected_date']:
            metrics['rejected_count'] += 1
        if app['withdrawn_date']:
            metrics['withdrawn_count'] += 1
        if 'analysis' in status:
            metrics['analysis_phase_count'] += 1

    # Calculate averages
    if fit_scores:
        metrics['avg_fit_score'] = round(sum(fit_scores) / len(fit_scores), 2)

    return metrics

def generate_status_md(applications, metrics):
    """Generate the STATUS.md file content."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    content = f"""# Application Status Dashboard

**Last Updated:** {now}
**Total Applications:** {metrics['total']}

---

## Quick Stats

| Metric | Count |
|--------|-------|
| **Total Applications** | {metrics['total']} |
| **Analysis Phase** | {metrics['analysis_phase_count']} |
| **Applied** | {metrics['applied_count']} |
| **In Interview Process** | {metrics['interview_count']} |
| **Rejected** | {metrics['rejected_count']} |
| **Withdrawn** | {metrics['withdrawn_count']} |
| **High Priority (8+ fit)** | {metrics['high_priority_count']} |
| **Average Fit Score** | {metrics['avg_fit_score']}/10 |

---

## Applications by Status

"""

    # Group by status
    apps_by_status = defaultdict(list)
    for app in applications:
        apps_by_status[app['status']].append(app)

    # Analysis Phase
    if apps_by_status['analysis phase']:
        content += f"### Analysis Phase ({len(apps_by_status['analysis phase'])})\n\n"
        for app in sorted(apps_by_status['analysis phase'], key=lambda x: x.get('fit_score', 0), reverse=True):
            fit = f"{app['fit_score']}/10" if app['fit_score'] else "N/A"
            content += f"- **{app['company']} - {app['role']}** (Fit: {fit})\n"
            content += f"  - Analyzed: {app['analyzed_date']}\n"
            if app['location']:
                content += f"  - Location: {app['location']}\n"
        content += "\n"

    # Applied
    if apps_by_status.get('applied'):
        content += f"### Applied ({len(apps_by_status['applied'])})\n\n"
        for app in apps_by_status['applied']:
            fit = f"{app['fit_score']}/10" if app['fit_score'] else "N/A"
            content += f"- **{app['company']} - {app['role']}** (Fit: {fit})\n"
            if app['applied_date']:
                content += f"  - Applied: {app['applied_date']}\n"
        content += "\n"

    # Withdrawn
    if apps_by_status.get('withdrawn'):
        content += f"### Withdrawn ({len(apps_by_status['withdrawn'])})\n\n"
        for app in apps_by_status['withdrawn']:
            fit = f"{app['fit_score']}/10" if app['fit_score'] else "N/A"
            content += f"- **{app['company']} - {app['role']}** (Fit: {fit})\n"
            if app['withdrawn_date']:
                content += f"  - Withdrawn: {app['withdrawn_date']}\n"
        content += "\n"

    # Rejected
    if apps_by_status.get('rejected'):
        content += f"### Rejected ({len(apps_by_status['rejected'])})\n\n"
        for app in apps_by_status['rejected']:
            fit = f"{app['fit_score']}/10" if app['fit_score'] else "N/A"
            content += f"- **{app['company']} - {app['role']}** (Fit: {fit})\n"
            if app['rejected_date']:
                content += f"  - Rejected: {app['rejected_date']}\n"
        content += "\n"

    content += "---\n\n## High Priority Applications (8+ Fit)\n\n"

    high_priority = [app for app in applications if app.get('fit_score') and app['fit_score'] >= 8]
    high_priority.sort(key=lambda x: x.get('fit_score') or 0, reverse=True)

    if high_priority:
        for app in high_priority:
            content += f"### {app['company']} - {app['role']} ({app['fit_score']}/10)\n\n"
            content += f"- **Status:** {app['status'].title()}\n"
            content += f"- **Location:** {app.get('location', 'N/A')}\n"
            content += f"- **Analyzed:** {app.get('analyzed_date', 'N/A')}\n"
            content += f"- **CV Generated:** {'Yes' if app['cv_generated'] else 'No'}\n"
            content += f"- **Cover Letter:** {'Yes' if app['cover_letter_generated'] else 'No'}\n"
            content += "\n"
    else:
        content += "*No high-priority applications currently.*\n\n"

    return content

def generate_metrics_dashboard(applications, metrics):
    """Generate the metrics-dashboard.md file content."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    content = f"""# Job Application Metrics Dashboard

**Generated:** {now}
**Data Source:** {metrics['total']} application folders in `applications/*/status.md`

---

## Summary KPIs

| KPI | Value | Notes |
|-----|-------|-------|
| **Total Applications Tracked** | {metrics['total']} | All applications in system |
| **Average Fit Score** | {metrics['avg_fit_score']}/10 | Based on {len([a for a in applications if a['fit_score']])} scored applications |
| **High Priority (8+ fit)** | {metrics['high_priority_count']} | Applications worth pursuing |
| **Analysis Phase** | {metrics['analysis_phase_count']} | Analyzed but not yet applied |
| **Applied** | {metrics['applied_count']} | Submitted applications |
| **In Interview Process** | {metrics['interview_count']} | Active interview pipelines |
| **Rejected** | {metrics['rejected_count']} | Explicit rejections |
| **Withdrawn** | {metrics['withdrawn_count']} | Self-withdrawn after analysis |

---

## Conversion Funnel

```
Applications Analyzed ({metrics['total']})
    ↓
High Priority 8+ fit ({metrics['high_priority_count']})
    ↓
CVs Generated ({metrics['cv_generated_count']})
    ↓
Applications Submitted ({metrics['applied_count']})
    ↓
Interviews ({metrics['interview_count']})
```

**Conversion Rates:**
- Analysis → High Priority: {round(metrics['high_priority_count']/metrics['total']*100, 1) if metrics['total'] > 0 else 0}%
- High Priority → Applied: {round(metrics['applied_count']/metrics['high_priority_count']*100, 1) if metrics['high_priority_count'] > 0 else 0}%
- Applied → Interview: {round(metrics['interview_count']/metrics['applied_count']*100, 1) if metrics['applied_count'] > 0 else 0}%

---

## Applications by Fit Score

"""

    # Fit score distribution
    fit_distribution = defaultdict(int)
    for app in applications:
        if app['fit_score']:
            bucket = int(app['fit_score'])
            fit_distribution[bucket] += 1

    content += "| Score Range | Count | Bar |\n"
    content += "|-------------|-------|-----|\n"
    for score in sorted(fit_distribution.keys(), reverse=True):
        bar = "█" * fit_distribution[score]
        content += f"| {score}-{score}.9 | {fit_distribution[score]} | {bar} |\n"

    content += f"\n---\n\n## Applications by Status\n\n"

    status_counts = sorted(metrics['by_status'].items(), key=lambda x: x[1], reverse=True)
    content += "| Status | Count |\n"
    content += "|--------|-------|\n"
    for status, count in status_counts:
        content += f"| {status.title()} | {count} |\n"

    content += f"\n---\n\n## Recent Activity (Last 7 Days)\n\n"

    # Find recent applications (analyzed in last 7 days)
    recent = []
    today = datetime.now()
    for app in applications:
        if app['analyzed_date']:
            try:
                analyzed = datetime.strptime(app['analyzed_date'], "%Y-%m-%d")
                days_ago = (today - analyzed).days
                if days_ago <= 7:
                    recent.append((app, days_ago))
            except:
                pass

    if recent:
        recent.sort(key=lambda x: x[1])
        for app, days_ago in recent:
            fit = f"{app['fit_score']}/10" if app['fit_score'] else "N/A"
            content += f"- **{app['company']} - {app['role']}** (Fit: {fit}) - {days_ago} days ago\n"
    else:
        content += "*No activity in last 7 days.*\n"

    content += f"\n---\n\n## Top 10 Applications by Fit Score\n\n"

    top_apps = sorted([a for a in applications if a['fit_score']],
                     key=lambda x: x['fit_score'], reverse=True)[:10]

    content += "| Rank | Company | Role | Fit | Status | Location |\n"
    content += "|------|---------|------|-----|--------|----------|\n"
    for i, app in enumerate(top_apps, 1):
        content += f"| {i} | {app['company']} | {app['role']} | {app['fit_score']}/10 | {app['status'].title()} | {app.get('location', 'N/A')} |\n"

    return content

def main():
    """Main sync function."""
    print("Starting sync process...")
    print(f"Scanning {APPLICATIONS_PATH}")

    # Find all status.md files in new hierarchical structure
    status_files = []
    status_files.extend(APPLICATIONS_PATH.glob("active/*/*/status.md"))
    status_files.extend(APPLICATIONS_PATH.glob("archive/*/*/*/status.md"))

    # Convert to list and remove duplicates
    status_files = list(set(status_files))
    print(f"Found {len(status_files)} application folders")

    # Parse all status files
    applications = []
    for status_file in status_files:
        data = parse_status_file(status_file)
        if data:
            applications.append(data)

    print(f"Successfully parsed {len(applications)} applications")

    # Calculate metrics
    metrics = calculate_metrics(applications)
    print(f"Calculated metrics: {metrics['total']} total, {metrics['high_priority_count']} high priority")

    # Generate STATUS.md
    status_content = generate_status_md(applications, metrics)
    status_path = BASE_PATH / "STATUS.md"
    with open(status_path, 'w', encoding='utf-8') as f:
        f.write(status_content)
    print(f"[OK] Generated {status_path}")

    # Generate metrics-dashboard.md
    metrics_content = generate_metrics_dashboard(applications, metrics)
    metrics_path = BASE_PATH / "insights" / "metrics-dashboard.md"
    with open(metrics_path, 'w', encoding='utf-8') as f:
        f.write(metrics_content)
    print(f"[OK] Generated {metrics_path}")

    print("\n=== Sync Complete ===")
    print(f"Total applications: {metrics['total']}")
    print(f"High priority (8+): {metrics['high_priority_count']}")
    print(f"Analysis phase: {metrics['analysis_phase_count']}")
    print(f"Applied: {metrics['applied_count']}")
    print(f"Interviews: {metrics['interview_count']}")
    print(f"Withdrawn: {metrics['withdrawn_count']}")
    print(f"Rejected: {metrics['rejected_count']}")
    print(f"Average fit score: {metrics['avg_fit_score']}/10")

if __name__ == "__main__":
    main()
