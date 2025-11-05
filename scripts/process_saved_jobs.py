#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Job Processing Script - ToS-Compliant Job Organization

Processes manually saved jobs (via bookmarklet) to:
- Deduplicate against existing applications
- Organize into proper folder structure
- Validate job description format
- Generate batch summary

COMPLIANT: This script only processes jobs that were MANUALLY saved by the user.
No scraping, no automation, no ToS violations.

Usage:
    python scripts/process_saved_jobs.py
    python scripts/process_saved_jobs.py --batch staging/my-batch
    python scripts/process_saved_jobs.py --dry-run
"""

import argparse
import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple


class JobDeduplicator:
    """Check if job already exists in applications folder."""

    def __init__(self, applications_dir: Path):
        self.applications_dir = applications_dir

    def is_duplicate(self, company: str, title: str) -> Optional[Path]:
        """
        Check if job already exists.

        Returns:
            Path to existing application if duplicate, None otherwise
        """
        if not self.applications_dir.exists():
            return None

        # Normalize for comparison
        company_norm = self._normalize(company)
        title_norm = self._normalize(title)

        for app_folder in self.applications_dir.iterdir():
            if not app_folder.is_dir() or app_folder.name.startswith('_'):
                continue

            folder_name = app_folder.name.lower()

            # Check if company and partial title match
            if company_norm in folder_name:
                # Allow partial title match (first 3 words)
                title_words = title_norm.split()[:3]
                if all(word in folder_name for word in title_words):
                    return app_folder

        return None

    def _normalize(self, text: str) -> str:
        """Normalize text for comparison."""
        return re.sub(r'[^a-z0-9\s]', '', text.lower())


class JobProcessor:
    """Process saved jobs: deduplicate, organize, validate."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.applications_dir = project_root / 'applications'
        self.staging_dir = project_root / 'staging'
        self.deduplicator = JobDeduplicator(self.applications_dir)

    def process_batch(self, input_dir: Path, dry_run: bool = False) -> Dict:
        """
        Process a batch of saved jobs.

        Args:
            input_dir: Directory containing saved job markdown files
            dry_run: If True, show what would happen without actually processing

        Returns:
            Summary dict with processing statistics
        """
        if not input_dir.exists():
            raise FileNotFoundError(f"Input directory not found: {input_dir}")

        print(f"\n{'='*80}")
        print(f"Job Processing {'(DRY RUN)' if dry_run else ''}")
        print(f"{'='*80}\n")
        print(f"Input: {input_dir}")

        # Find all job markdown files
        job_files = list(input_dir.glob('*.md'))
        print(f"Found {len(job_files)} job files\n")

        if not job_files:
            print("No job files found. Make sure files are saved to this directory.")
            return {'total': 0, 'processed': 0, 'duplicates': 0, 'errors': 0}

        # Create output batch directory
        batch_name = datetime.now().strftime('%Y-%m-%d-processed-batch')
        output_dir = self.staging_dir / batch_name

        if not dry_run:
            output_dir.mkdir(parents=True, exist_ok=True)

        # Process each job
        results = {
            'total': len(job_files),
            'processed': 0,
            'duplicates': 0,
            'errors': 0,
            'jobs': []
        }

        for i, job_file in enumerate(job_files, 1):
            print(f"[{i}/{len(job_files)}] Processing: {job_file.name}")

            try:
                # Parse job file
                job_data = self._parse_job_file(job_file)

                if not job_data:
                    print(f"  ❌ Failed to parse job file")
                    results['errors'] += 1
                    continue

                # Check for duplicates
                existing = self.deduplicator.is_duplicate(
                    job_data['company'],
                    job_data['title']
                )

                if existing:
                    print(f"  ⏭️  Duplicate: Already tracked in {existing.name}")
                    results['duplicates'] += 1
                    results['jobs'].append({
                        'company': job_data['company'],
                        'title': job_data['title'],
                        'status': 'duplicate',
                        'existing_folder': str(existing)
                    })
                    continue

                # Create folder name
                folder_name = self._create_folder_name(
                    job_data['company'],
                    job_data['title']
                )

                # Save to output directory
                if not dry_run:
                    job_folder = output_dir / folder_name
                    job_folder.mkdir(parents=True, exist_ok=True)

                    # Copy job description
                    shutil.copy2(job_file, job_folder / 'job-description.md')

                    print(f"  ✅ Saved to: {folder_name}/")
                else:
                    print(f"  ✓ Would save to: {folder_name}/")

                results['processed'] += 1
                results['jobs'].append({
                    'company': job_data['company'],
                    'title': job_data['title'],
                    'location': job_data.get('location', 'Unknown'),
                    'url': job_data.get('url', ''),
                    'status': 'processed',
                    'folder': folder_name
                })

            except Exception as e:
                print(f"  ❌ Error: {e}")
                results['errors'] += 1

        # Generate summary
        print(f"\n{'='*80}")
        print("Summary")
        print(f"{'='*80}\n")
        print(f"Total jobs: {results['total']}")
        print(f"✅ Processed: {results['processed']}")
        print(f"⏭️  Duplicates: {results['duplicates']}")
        print(f"❌ Errors: {results['errors']}")

        if not dry_run and results['processed'] > 0:
            print(f"\n📁 Saved to: {output_dir}")

            # Save summary JSON
            summary_file = output_dir / 'PROCESSING-SUMMARY.json'
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)

            print(f"📄 Summary saved: {summary_file}")

            # Print next steps
            print(f"\n🎯 Next Steps:")
            print(f"1. Run bulk analysis: python scripts/bulk_analyze.py {output_dir}")
            print(f"2. Review fit scores in: {output_dir}/BULK-ANALYSIS-SUMMARY.md")
            print(f"3. Apply to 8+ fit roles using /generate-cv and /generate-cover-letter")

        return results

    def _parse_job_file(self, file_path: Path) -> Optional[Dict]:
        """Parse job markdown file and extract metadata."""
        try:
            content = file_path.read_text(encoding='utf-8')

            # Extract title (first # heading)
            title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
            title = title_match.group(1).strip() if title_match else None

            # Extract company
            company_match = re.search(r'\*\*Company:\*\* (.+)$', content, re.MULTILINE)
            company = company_match.group(1).strip() if company_match else None

            # Extract location
            location_match = re.search(r'\*\*Location:\*\* (.+)$', content, re.MULTILINE)
            location = location_match.group(1).strip() if location_match else None

            # Extract URL
            url_match = re.search(r'\*\*URL:\*\* (.+)$', content, re.MULTILINE)
            url = url_match.group(1).strip() if url_match else None

            if not title or not company:
                return None

            return {
                'title': title,
                'company': company,
                'location': location,
                'url': url,
                'content': content
            }

        except Exception as e:
            print(f"  Error parsing {file_path.name}: {e}")
            return None

    def _create_folder_name(self, company: str, title: str) -> str:
        """Create standardized folder name."""
        # Clean company name
        company_clean = re.sub(r'[^a-zA-Z0-9\s]', '', company)
        company_clean = re.sub(r'\s+', '', company_clean)

        # Clean title (take first 3-4 words)
        title_words = re.findall(r'\b[a-zA-Z]+\b', title)[:4]
        title_clean = ''.join(title_words)

        # Format: YYYY-MM-Company-Role
        date_prefix = datetime.now().strftime('%Y-%m')
        return f"{date_prefix}-{company_clean}-{title_clean}"


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Process manually saved jobs (ToS-compliant)'
    )
    parser.add_argument(
        '--batch',
        type=str,
        help='Input directory (default: staging/manual-saves/)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would happen without actually processing'
    )

    args = parser.parse_args()

    # Setup paths
    project_root = Path(__file__).parent.parent
    default_input = project_root / 'staging' / 'manual-saves'

    input_dir = Path(args.batch) if args.batch else default_input

    # Create manual-saves directory if it doesn't exist
    if not input_dir.exists() and input_dir == default_input:
        input_dir.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {input_dir}")
        print(f"\nNo jobs found. Save jobs using the bookmarklet first.")
        print(f"See BOOKMARKLET-GUIDE.md for setup instructions.")
        return

    # Process jobs
    processor = JobProcessor(project_root)
    results = processor.process_batch(input_dir, dry_run=args.dry_run)

    # Exit code
    if results['errors'] > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
