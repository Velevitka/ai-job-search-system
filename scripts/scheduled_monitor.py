#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scheduled Job Discovery Monitor

Runs job discovery automatically on a schedule and sends notifications
for high-fit jobs.

Usage:
    python scripts/scheduled_monitor.py              # Run once (for cron/task scheduler)
    python scripts/scheduled_monitor.py --test       # Test run (shows what would happen)
    python scripts/scheduled_monitor.py --email your@email.com  # Email notifications
"""

import argparse
import json
import smtplib
import sys
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path
from typing import List, Dict

# Add parent directory to path to import job_discovery
sys.path.insert(0, str(Path(__file__).parent))

from job_discovery import LinkedInJobSearcher, JobDeduplicator, save_to_staging


def load_search_criteria(preferences_file: Path) -> List[Dict]:
    """
    Load search criteria from career-preferences.md.

    For now, returns hardcoded searches. TODO: Parse from file.
    """
    # TODO: Parse career-preferences.md
    return [
        {
            'keywords': 'Director Product Data Platform',
            'location': 'London, United Kingdom',
            'experience_level': ['director']
        },
        {
            'keywords': 'Head of Product Growth',
            'location': 'London, United Kingdom',
            'experience_level': ['director']
        },
        {
            'keywords': 'VP Product',
            'location': 'Remote, United Kingdom',
            'experience_level': ['executive', 'director']
        }
    ]


def send_email_notification(
    recipient: str,
    high_fit_jobs: List[Dict],
    total_discovered: int,
    smtp_config: Dict = None
):
    """
    Send email notification about new high-fit jobs.

    Args:
        recipient: Email address to send to
        high_fit_jobs: List of jobs with 8+ fit scores
        total_discovered: Total jobs found
        smtp_config: SMTP configuration (defaults to Gmail)
    """
    if not smtp_config:
        smtp_config = {
            'server': 'smtp.gmail.com',
            'port': 587,
            'username': None,  # Set via environment variable
            'password': None   # Set via environment variable or app password
        }

    msg = EmailMessage()
    msg['Subject'] = f'🎯 {len(high_fit_jobs)} High-Fit Jobs Discovered!'
    msg['From'] = smtp_config.get('username', 'job-monitor@yourdomain.com')
    msg['To'] = recipient

    # Build email body
    body = f"""
Job Discovery Report - {datetime.now().strftime('%Y-%m-%d')}

================================================================================
SUMMARY
================================================================================

Total jobs discovered: {total_discovered}
High-fit jobs (8+): {len(high_fit_jobs)}

================================================================================
HIGH-FIT JOBS
================================================================================

"""

    for i, job in enumerate(high_fit_jobs, 1):
        body += f"""
{i}. {job['title']} @ {job['company']}
   Location: {job['location']}
   Fit Score: {job.get('fit_score', 'TBD')}/10
   URL: {job['url']}

"""

    body += f"""
================================================================================
NEXT STEPS
================================================================================

1. Review full analysis: staging/{datetime.now().strftime('%Y-%m-%d')}-discovery-batch/
2. Generate CVs for 8+ fit jobs using: /generate-cv CompanyName
3. Apply within 48 hours for best response rates

---
This is an automated notification from your job discovery monitor.
"""

    msg.set_content(body)

    # Send email
    try:
        if smtp_config.get('username') and smtp_config.get('password'):
            with smtplib.SMTP(smtp_config['server'], smtp_config['port']) as server:
                server.starttls()
                server.login(smtp_config['username'], smtp_config['password'])
                server.send_message(msg)
            print(f"  ✅ Email sent to {recipient}")
        else:
            print(f"  ⚠️ Email configuration incomplete - email not sent")
            print(f"     Set SMTP_USERNAME and SMTP_PASSWORD environment variables")
    except Exception as e:
        print(f"  ❌ Failed to send email: {e}")


def run_scheduled_discovery(
    test_mode: bool = False,
    email_notify: str = None,
    headless: bool = True
):
    """
    Run automated job discovery.

    Args:
        test_mode: If True, doesn't actually scrape (dry run)
        email_notify: Email address for notifications
        headless: Run browser in headless mode
    """
    print("=" * 80)
    print(f"Scheduled Job Discovery Monitor - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 80)

    if test_mode:
        print("\n⚠️  TEST MODE - Will not actually scrape jobs\n")

    # Setup paths
    project_root = Path(__file__).parent.parent
    staging_dir = project_root / 'staging'
    applications_dir = project_root / 'applications'
    preferences_file = project_root / 'career-preferences.md'
    browser_data_dir = project_root / '.browser_data'

    # Create browser data directory
    browser_data_dir.mkdir(exist_ok=True)

    # Load search criteria
    print("\n📋 Loading search criteria...")
    searches = load_search_criteria(preferences_file)
    print(f"  ✓ Loaded {len(searches)} search queries")

    # Initialize searcher
    if not test_mode:
        searcher = LinkedInJobSearcher(
            headless=headless,
            slow_mo=100,
            user_data_dir=str(browser_data_dir)
        )

    deduplicator = JobDeduplicator(applications_dir)

    try:
        all_jobs = []

        # Perform searches
        if test_mode:
            print("\n🔍 Would run searches:")
            for search in searches:
                print(f"  - {search['keywords']} in {search['location']}")
            print("\n⏭️  Skipping actual search (test mode)")
        else:
            for search in searches:
                jobs = searcher.search(
                    keywords=search['keywords'],
                    location=search['location'],
                    date_posted='past_week',
                    experience_level=search.get('experience_level')
                )
                all_jobs.extend(jobs)

        # Deduplicate
        print(f"\n📊 Jobs discovered: {len(all_jobs) if not test_mode else 'N/A (test mode)'}")

        if not test_mode and all_jobs:
            new_jobs = []
            for job in all_jobs:
                existing = deduplicator.is_duplicate(job['company'], job['title'])
                if not existing:
                    new_jobs.append(job)

            print(f"✅ New jobs: {len(new_jobs)}")
            print(f"⏭️  Duplicates: {len(all_jobs) - len(new_jobs)}")

            if new_jobs:
                # Scrape new jobs
                batch_name = datetime.now().strftime('%Y-%m-%d-discovery-batch')
                print(f"\n📥 Scraping {len(new_jobs)} new jobs...")

                scraped = []
                for i, job in enumerate(new_jobs, 1):
                    print(f"  [{i}/{len(new_jobs)}] {job['company']} - {job['title']}")
                    description = searcher.scrape_job_description(job['url'])

                    if description:
                        save_to_staging(job, description, staging_dir, batch_name)
                        scraped.append(job)

                        # Rate limiting
                        if i < len(new_jobs):
                            import time
                            time.sleep(2)

                print(f"\n✅ Scraped {len(scraped)}/{len(new_jobs)} jobs")
                print(f"📁 Saved to: {staging_dir / batch_name}")

                # TODO: Run bulk analysis to get fit scores
                # For now, assume jobs need manual analysis
                high_fit_jobs = []  # Would filter by fit_score >= 8

                # Send email notification if configured
                if email_notify:
                    send_email_notification(
                        recipient=email_notify,
                        high_fit_jobs=high_fit_jobs,
                        total_discovered=len(new_jobs)
                    )

                print("\n" + "=" * 80)
                print("✅ Monitoring complete!")
                print("=" * 80)
                print(f"\nNext steps:")
                print(f"1. Run bulk analysis: python scripts/bulk_analyze.py {staging_dir / batch_name}")
                print(f"2. Review fit scores in BULK-ANALYSIS-SUMMARY.md")
                print(f"3. Apply to 8+ fit jobs")
            else:
                print("\n✨ No new jobs found (all are duplicates)")

    finally:
        if not test_mode:
            searcher.close_browser()


def main():
    parser = argparse.ArgumentParser(description='Scheduled Job Discovery Monitor')
    parser.add_argument('--test', action='store_true',
                       help='Test mode (dry run, no actual scraping)')
    parser.add_argument('--email', type=str,
                       help='Email address for notifications')
    parser.add_argument('--visible', action='store_true',
                       help='Show browser window (default: headless)')

    args = parser.parse_args()

    run_scheduled_discovery(
        test_mode=args.test,
        email_notify=args.email,
        headless=not args.visible
    )


if __name__ == '__main__':
    main()
