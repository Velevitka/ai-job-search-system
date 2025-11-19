#!/usr/bin/env python3
"""
Create status.md files for application folders that don't have them.
Extracts information from analysis.md to populate status.md.
"""

import re
from pathlib import Path
from datetime import datetime

def extract_fit_score(analysis_content):
    """Extract fit score from analysis.md"""
    match = re.search(r'## Fit Score:\s*(\d+\.?\d*)/10', analysis_content)
    return match.group(1) if match else "N/A"

def extract_analyzed_date(analysis_content):
    """Extract analyzed date from analysis.md"""
    match = re.search(r'\*\*Analyzed:\*\*\s*(\d{4}-\d{2}-\d{2})', analysis_content)
    return match.group(1) if match else datetime.now().strftime("%Y-%m-%d")

def extract_location(analysis_content):
    """Extract location from analysis.md"""
    match = re.search(r'- \*\*Role Location:\*\*\s*(.+)', analysis_content)
    return match.group(1).strip() if match else "Not specified"

def extract_location_match(analysis_content):
    """Extract location match from analysis.md"""
    match = re.search(r'- \*\*Preference Match:\*\*\s*(.+)', analysis_content)
    if match:
        return match.group(1).strip()
    return "Not specified"

def extract_seniority_match(analysis_content):
    """Extract seniority match from analysis.md"""
    # Find the Seniority section
    seniority_section = re.search(r'### Seniority\n- \*\*Role Level:\*\*.*?\n- \*\*Preference Match:\*\*\s*(.+)', analysis_content, re.DOTALL)
    if seniority_section:
        return seniority_section.group(1).strip().split('\n')[0]
    return "Not specified"

def extract_industry_match(analysis_content):
    """Extract industry match from analysis.md"""
    # Find the Industry section
    industry_section = re.search(r'### Industry\n- \*\*Industry:\*\*.*?\n- \*\*Preference Match:\*\*\s*(.+)', analysis_content, re.DOTALL)
    if industry_section:
        return industry_section.group(1).strip().split('\n')[0]
    return "Not specified"

def extract_overall_alignment(analysis_content):
    """Extract overall alignment from analysis.md"""
    match = re.search(r'### Overall Preference Alignment\n(.+)', analysis_content)
    if match:
        return match.group(1).strip()
    return "Not specified"

def extract_recommendation(analysis_content):
    """Extract recommendation from analysis.md"""
    match = re.search(r'\*\*Proceed with application\?\*\*\s*(\w+)', analysis_content)
    return match.group(1) if match else "MAYBE"

def create_status_md(folder_path, analysis_content):
    """Create status.md file for a folder"""
    # Extract information
    fit_score = extract_fit_score(analysis_content)
    analyzed_date = extract_analyzed_date(analysis_content)
    location = extract_location(analysis_content)
    location_match = extract_location_match(analysis_content)
    seniority_match = extract_seniority_match(analysis_content)
    industry_match = extract_industry_match(analysis_content)
    overall_alignment = extract_overall_alignment(analysis_content)
    recommendation = extract_recommendation(analysis_content)

    # Extract company and role from analysis.md title
    title_match = re.search(r'# Job Analysis - (.+?) - (.+?)$', analysis_content, re.MULTILINE)
    if title_match:
        company = title_match.group(1).strip()
        role = title_match.group(2).strip()
    else:
        # Fallback to folder name
        folder_name = folder_path.name
        parts = folder_name.split('-', 2)
        if len(parts) >= 3:
            company = parts[1]
            role = parts[2].replace('-', ' ')
        else:
            company = "Unknown"
            role = folder_name

    # Get current timestamp
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M")

    # Create status.md content
    status_content = f"""# Application Status - {company} - {role}

**Current Status:** Analysis Phase
**Last Updated:** {timestamp}

---

## Application Details

**Analyzed On:** {analyzed_date}
**Fit Score:** {fit_score}/10
**Location:** {location}
**Source File:** "N/A - Backfilled"

**CV Version:** Not generated
**Cover Letter:** Not generated

---

## Career Preferences Alignment

**Location Match:** {location_match}
**Seniority Match:** {seniority_match}
**Industry Match:** {industry_match}
**Overall Alignment:** {overall_alignment}

---

## Status Timeline

### Analysis Phase - {timestamp}
**Notes:** Initial analysis completed. Fit score: {fit_score}/10. Recommendation: {recommendation}. Status file backfilled during system migration.
"""

    # Write status.md
    status_file = folder_path / "status.md"
    status_file.write_text(status_content, encoding='utf-8')

    return folder_path.name, fit_score

def main():
    """Main function to create status.md for all folders missing it"""
    applications_path = Path("applications")

    # Find all folders without status.md
    folders_missing_status = []
    for loc in ['active', 'archive']:
        loc_path = applications_path / loc
        if loc_path.exists():
            for folder in loc_path.glob('*/*'):
                if folder.is_dir() and not (folder / 'status.md').exists():
                    folders_missing_status.append(folder)

    print(f"Found {len(folders_missing_status)} folders without status.md\n")

    if not folders_missing_status:
        print("All folders already have status.md files!")
        return

    created_count = 0
    for folder in folders_missing_status:
        analysis_file = folder / "analysis.md"

        if not analysis_file.exists():
            print(f"[SKIP] {folder.name} - No analysis.md found")
            continue

        # Read analysis.md
        analysis_content = analysis_file.read_text(encoding='utf-8')

        # Create status.md
        folder_name, fit_score = create_status_md(folder, analysis_content)
        created_count += 1
        print(f"[OK] Created status.md for {folder_name} (Fit: {fit_score}/10)")

    print(f"\n{created_count} status.md files created successfully!")

if __name__ == "__main__":
    main()
