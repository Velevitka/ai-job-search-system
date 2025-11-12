#!/usr/bin/env python3
"""
System Sync Script - Parse all application status files
Generates consolidated view of all applications
"""

import os
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# Base directory
BASE_DIR = Path(r"C:\Users\ArturSwadzba\OneDrive\4. CV")
APPLICATIONS_DIR = BASE_DIR / "applications"

def parse_status_file(status_path):
    """Parse a single status.md file and extract key information"""
    try:
        with open(status_path, 'r', encoding='utf-8') as f:
            content = f.read()

        data = {
            'folder': status_path.parent.name,
            'path': str(status_path.parent)
        }

        # Extract company and role from first line
        first_line_match = re.search(r'# Application Status - (.+?) - (.+?)$', content, re.MULTILINE)
        if first_line_match:
            data['company'] = first_line_match.group(1)
            data['role'] = first_line_match.group(2)

        # Extract current status
        status_match = re.search(r'\*\*Current Status:\*\* (.+?)$', content, re.MULTILINE)
        if status_match:
            data['status'] = status_match.group(1).strip()

        # Extract last updated
        updated_match = re.search(r'\*\*Last Updated:\*\* (.+?)$', content, re.MULTILINE)
        if updated_match:
            data['last_updated'] = updated_match.group(1).strip()

        # Extract applied date
        applied_match = re.search(r'\*\*Applied On:\*\* (.+?)$', content, re.MULTILINE)
        if applied_match:
            data['applied_on'] = applied_match.group(1).strip()

        # Extract fit score
        fit_match = re.search(r'\*\*Fit Score:\*\* ([\d.]+)/10', content)
        if fit_match:
            data['fit_score'] = float(fit_match.group(1))

        # Extract days in process
        days_match = re.search(r'\*\*Days in Process:\*\* (\d+)', content)
        if days_match:
            data['days_in_process'] = int(days_match.group(1))

        # Extract location
        location_match = re.search(r'\*\*Location:\*\* (.+?)$', content, re.MULTILINE)
        if location_match:
            data['location'] = location_match.group(1).strip()

        return data

    except Exception as e:
        print(f"Error parsing {status_path}: {e}")
        return None

def calculate_days_since(date_str):
    """Calculate days since a date string"""
    try:
        if not date_str or date_str == 'N/A':
            return None
        # Try parsing YYYY-MM-DD
        date = datetime.strptime(date_str, '%Y-%m-%d')
        today = datetime.now()
        return (today - date).days
    except:
        return None

def main():
    # Find all status.md files
    status_files = list(APPLICATIONS_DIR.glob('*/status.md'))

    print(f"Found {len(status_files)} status files")

    # Parse all status files
    applications = []
    for status_file in status_files:
        data = parse_status_file(status_file)
        if data:
            applications.append(data)

    # Categorize by status
    by_status = defaultdict(list)
    for app in applications:
        status = app.get('status', 'Unknown')
        by_status[status].append(app)

    # Calculate statistics
    total = len(applications)
    active = len([a for a in applications if a.get('status') == 'Applied'])
    withdrawn = len([a for a in applications if a.get('status') == 'Withdrawn'])
    rejected = len([a for a in applications if a.get('status') == 'Rejected'])

    fit_scores = [a['fit_score'] for a in applications if 'fit_score' in a]
    avg_fit = sum(fit_scores) / len(fit_scores) if fit_scores else 0

    days_waiting = [a['days_in_process'] for a in applications if a.get('status') == 'Applied' and 'days_in_process' in a]
    avg_days = sum(days_waiting) / len(days_waiting) if days_waiting else 0

    print(f"\n=== APPLICATION SUMMARY ===")
    print(f"Total applications: {total}")
    print(f"Active (Applied): {active}")
    print(f"Withdrawn: {withdrawn}")
    print(f"Rejected: {rejected}")
    print(f"Average fit score: {avg_fit:.1f}/10")
    print(f"Average days waiting: {avg_days:.1f} days")

    print(f"\n=== ACTIVE APPLICATIONS ===")
    active_apps = sorted([a for a in applications if a.get('status') == 'Applied'],
                        key=lambda x: x.get('days_in_process', 0), reverse=True)

    for app in active_apps:
        company = app.get('company', 'Unknown')
        role = app.get('role', 'Unknown')[:40]
        fit = app.get('fit_score', 0)
        days = app.get('days_in_process', 0)
        print(f"  • {company} - {role} | {fit}/10 fit | {days} days")

    print(f"\n=== WITHDRAWN APPLICATIONS ===")
    withdrawn_apps = [a for a in applications if a.get('status') == 'Withdrawn']
    for app in withdrawn_apps:
        company = app.get('company', 'Unknown')
        fit = app.get('fit_score', 0)
        print(f"  • {company} | {fit}/10 fit")

    print(f"\n=== REJECTED APPLICATIONS ===")
    rejected_apps = [a for a in applications if a.get('status') == 'Rejected']
    for app in rejected_apps:
        company = app.get('company', 'Unknown')
        fit = app.get('fit_score', 0)
        applied = app.get('applied_on', 'Unknown')
        print(f"  • {company} | {fit}/10 fit | Applied: {applied}")

    # Return data for further processing
    return {
        'applications': applications,
        'by_status': dict(by_status),
        'stats': {
            'total': total,
            'active': active,
            'withdrawn': withdrawn,
            'rejected': rejected,
            'avg_fit': avg_fit,
            'avg_days': avg_days
        }
    }

if __name__ == '__main__':
    main()
