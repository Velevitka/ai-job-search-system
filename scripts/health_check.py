#!/usr/bin/env python3
"""
System Health Check Script

Comprehensive health check for the job application tracking system:
- Orphaned files detection
- Status consistency validation
- Missing CV/CL detection
- Stale applications detection
- Archive integrity checks
- Pipeline folder structure validation

Run: python scripts/health_check.py
Output: insights/health-check-YYYY-MM-DD.md
"""

from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import re
from collections import defaultdict


class HealthChecker:
    def __init__(self, root_path: Path = Path(".")):
        self.root = root_path
        self.applications = root_path / "applications"
        self.staging = root_path / "staging"

        self.issues = defaultdict(list)
        self.warnings = defaultdict(list)
        self.info = defaultdict(list)

    def check_orphaned_files(self):
        """Find job files without corresponding application folders"""
        print("  Checking for orphaned job files...")

        # Check staging/3-applying/
        applying_folder = self.staging / "3-applying"
        if applying_folder.exists():
            for job_file in applying_folder.glob("*.mhtml"):
                matching_folder = self._find_matching_application(job_file)

                if not matching_folder:
                    self.issues['orphaned_files'].append(
                        f"{job_file.name} in staging/3-applying/ has no corresponding application folder"
                    )

    def _find_matching_application(self, job_file: Path) -> Path:
        """Find application folder matching a job file using multiple strategies"""
        job_filename = job_file.name

        # Strategy 1: Check if job filename is referenced in job-description.md files
        for app_folder in self.applications.glob("2025-*"):
            if not app_folder.is_dir():
                continue

            job_desc_file = app_folder / "job-description.md"
            if job_desc_file.exists():
                try:
                    content = job_desc_file.read_text(encoding='utf-8')

                    # Check if filename appears in content (likely in source_file or as reference)
                    if job_filename in content:
                        return app_folder

                    # Check for source_file in YAML front matter
                    if content.startswith('---'):
                        yaml_end = content.find('---', 3)
                        if yaml_end > 0:
                            front_matter = content[3:yaml_end]
                            if f'source_file: {job_filename}' in front_matter or f'source_file: "{job_filename}"' in front_matter:
                                return app_folder
                except Exception:
                    pass

        # Strategy 2: Token-based fuzzy matching on folder names
        # Extract meaningful tokens from job filename
        job_tokens = self._extract_tokens(job_file.stem.lower())

        best_match = None
        best_score = 0

        for app_folder in self.applications.glob("2025-*"):
            if not app_folder.is_dir():
                continue

            folder_tokens = self._extract_tokens(app_folder.name.lower())

            # Calculate overlap score
            common_tokens = job_tokens & folder_tokens
            if len(common_tokens) > 0:
                # Score based on number of matching tokens and their significance
                score = len(common_tokens) / max(len(job_tokens), len(folder_tokens))

                if score > best_score:
                    best_score = score
                    best_match = app_folder

        # Only return match if confidence is high enough (>30% token overlap)
        if best_score > 0.3:
            return best_match

        return None

    def _extract_tokens(self, text: str) -> set:
        """Extract meaningful tokens from text for matching"""
        # Split CamelCase words BEFORE lowercasing (VPProduct → VP Product)
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
        text = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', text)  # Handle VPPM → VP PM

        # Now lowercase
        text = text.lower()

        # Remove common separators and split
        text = text.replace('-', ' ').replace('_', ' ').replace('(', ' ').replace(')', ' ')
        tokens = text.split()

        # Filter out noise words and short tokens
        stop_words = {'at', 'in', 'the', 'a', 'an', 'for', 'on', 'to', 'of', 'and', 'or',
                      'job', 'application', 'apply', 'career', 'careers', 'jobs', 'linkedin',
                      '2025', '11', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '12',
                      'director', 'head', 'senior', 'manager', 'lead', 'vp', 'vice', 'president',
                      'product', 'management', 'pm'}

        meaningful_tokens = {
            token for token in tokens
            if len(token) > 2 and token not in stop_words and not token.isdigit()
        }

        return meaningful_tokens

    def check_status_file_location_consistency(self):
        """Verify status matches file location"""
        print("  Checking status/location consistency...")

        terminal_states = {
            'rejected': self.staging / 'archive/rejected',
            'withdrawn': self.staging / 'archive/withdrawn',
            'accepted': self.staging / 'archive/accepted',
        }

        for app_folder in self.applications.glob("2025-*"):
            if not app_folder.is_dir():
                continue

            status_file = app_folder / "status.md"
            if not status_file.exists():
                continue

            content = status_file.read_text(encoding='utf-8')

            # Extract current status
            status_match = re.search(r'\*\*Current Status:\*\*\s*(\w+)', content)
            if not status_match:
                self.warnings['status_consistency'].append(
                    f"{app_folder.name}: No current status found in status.md"
                )
                continue

            current_status = status_match.group(1)

            # Check if terminal status
            if current_status in terminal_states:
                expected_archive = terminal_states[current_status]

                # Extract company name to find job file
                company_name = app_folder.name.split('-')[-1]

                # Check if job file is in expected archive location
                job_files_in_archive = list(expected_archive.glob(f"*{company_name}*"))
                job_files_in_applying = list((self.staging / '3-applying').glob(f"*{company_name}*"))

                if job_files_in_applying:
                    self.issues['status_consistency'].append(
                        f"{app_folder.name}: Status is '{current_status}' but job file still in staging/3-applying/ "
                        f"(should be in {expected_archive.name}/)"
                    )

    def check_missing_cvs(self):
        """Find applications with status='applied' but no CV"""
        print("  Checking for missing CVs...")

        for app_folder in self.applications.glob("2025-*"):
            if not app_folder.is_dir():
                continue

            status_file = app_folder / "status.md"
            if not status_file.exists():
                continue

            content = status_file.read_text(encoding='utf-8')

            # Check if status is 'applied' or later stages
            if "**Current Status:** applied" in content or \
               "**Current Status:** interview-invited" in content:

                # Check if CV exists
                cv_files = list(app_folder.glob("*_CV_*.pdf"))

                if not cv_files:
                    self.issues['missing_cvs'].append(
                        f"{app_folder.name}: Status is 'applied' but no CV PDF found"
                    )

    def check_stale_applications(self):
        """Find applications stuck in 'drafting' for >7 days"""
        print("  Checking for stale applications...")

        cutoff_date = datetime.now() - timedelta(days=7)

        for app_folder in self.applications.glob("2025-*"):
            if not app_folder.is_dir():
                continue

            status_file = app_folder / "status.md"
            if not status_file.exists():
                continue

            content = status_file.read_text(encoding='utf-8')

            # Check if status is 'drafting'
            if "**Current Status:** drafting" not in content:
                continue

            # Extract last updated date
            date_match = re.search(r'\*\*Last Updated:\*\*\s*(\d{4}-\d{2}-\d{2})', content)
            if not date_match:
                continue

            try:
                last_updated = datetime.strptime(date_match.group(1), '%Y-%m-%d')
                days_stale = (datetime.now() - last_updated).days

                if days_stale > 7:
                    self.warnings['stale_applications'].append(
                        f"{app_folder.name}: Stuck in 'drafting' for {days_stale} days (>7 days)"
                    )
            except ValueError:
                pass

    def check_archive_integrity(self):
        """Verify archive folder structure and contents"""
        print("  Checking archive integrity...")

        expected_archives = [
            'low-fit',
            'filtered',
            'rejected',
            'withdrawn',
            'accepted',
        ]

        archive_root = self.staging / "archive"
        if not archive_root.exists():
            self.issues['archive_integrity'].append("staging/archive/ folder does not exist")
            return

        # Check expected subfolders exist
        for archive_name in expected_archives:
            archive_folder = archive_root / archive_name
            if not archive_folder.exists():
                self.warnings['archive_integrity'].append(
                    f"Archive subfolder {archive_name}/ does not exist (will be created on first use)"
                )

        # Check for unexpected files in archive root (should be in subfolders)
        for item in archive_root.iterdir():
            if item.is_file():
                self.warnings['archive_integrity'].append(
                    f"File {item.name} in archive/ root (should be in subfolder)"
                )

    def check_pipeline_structure(self):
        """Verify staging pipeline folder structure"""
        print("  Checking pipeline structure...")

        expected_structure = {
            'staging/0-discovery/manual': 'Manual job discoveries',
            'staging/0-discovery/automated': 'Automated job discoveries',
            'staging/1-triage': 'Temporary analysis workspace',
            'staging/2-shortlist/high': 'High-priority jobs (9-11 fit)',
            'staging/2-shortlist/medium': 'Medium-priority jobs (7-8.5 fit)',
            'staging/2-shortlist/pending-insider-intel': 'Awaiting referral feedback',
            'staging/3-applying': 'Active application drafting',
            'staging/archive': 'Completed applications',
        }

        for folder_path, description in expected_structure.items():
            full_path = self.root / folder_path
            if not full_path.exists():
                self.warnings['pipeline_structure'].append(
                    f"{folder_path}/ does not exist - {description}"
                )

    def check_duplicate_applications(self):
        """Find potential duplicate applications to same company"""
        print("  Checking for duplicate applications...")

        companies = defaultdict(list)

        for app_folder in self.applications.glob("2025-*"):
            if not app_folder.is_dir():
                continue

            # Extract company name (rough heuristic: 3rd component after date)
            parts = app_folder.name.split('-')
            if len(parts) >= 3:
                company = parts[2]
                companies[company].append(app_folder.name)

        # Find companies with multiple applications
        for company, folders in companies.items():
            if len(folders) > 1:
                self.info['duplicate_applications'].append(
                    f"{company}: {len(folders)} applications ({', '.join(folders)})"
                )

    def check_missing_analysis_files(self):
        """Find application folders missing required files"""
        print("  Checking for missing analysis files...")

        required_files = ['job-description.md', 'analysis.md', 'status.md']

        for app_folder in self.applications.glob("2025-*"):
            if not app_folder.is_dir():
                continue

            missing = []
            for filename in required_files:
                if not (app_folder / filename).exists():
                    missing.append(filename)

            if missing:
                self.warnings['missing_files'].append(
                    f"{app_folder.name}: Missing {', '.join(missing)}"
                )

    def check_active_applications_waiting_time(self):
        """Check how long active applications have been waiting"""
        print("  Checking active application waiting times...")

        for app_folder in self.applications.glob("2025-*"):
            if not app_folder.is_dir():
                continue

            status_file = app_folder / "status.md"
            if not status_file.exists():
                continue

            content = status_file.read_text(encoding='utf-8')

            # Only check 'applied' status
            if "**Current Status:** applied" not in content:
                continue

            # Extract applied date
            applied_match = re.search(r'Applied On:\*\*\s*(\d{4}-\d{2}-\d{2})', content)
            if not applied_match:
                continue

            try:
                applied_date = datetime.strptime(applied_match.group(1), '%Y-%m-%d')
                days_waiting = (datetime.now() - applied_date).days

                if days_waiting > 14:
                    self.warnings['long_wait'].append(
                        f"{app_folder.name}: Waiting {days_waiting} days (>14 days, consider follow-up)"
                    )
                elif days_waiting > 21:
                    self.issues['long_wait'].append(
                        f"{app_folder.name}: Waiting {days_waiting} days (>21 days, likely silent rejection)"
                    )
            except ValueError:
                pass

    def run_all_checks(self):
        """Run all health checks"""
        print("🏥 Running System Health Checks...")
        print()

        self.check_orphaned_files()
        self.check_status_file_location_consistency()
        self.check_missing_cvs()
        self.check_stale_applications()
        self.check_archive_integrity()
        self.check_pipeline_structure()
        self.check_duplicate_applications()
        self.check_missing_analysis_files()
        self.check_active_applications_waiting_time()

        print()
        print("✅ Health checks complete")

    def calculate_health_score(self) -> Tuple[str, int]:
        """Calculate overall health score"""
        issue_count = sum(len(items) for items in self.issues.values())
        warning_count = sum(len(items) for items in self.warnings.values())

        if issue_count == 0 and warning_count == 0:
            return "Excellent", 100
        elif issue_count == 0 and warning_count <= 3:
            return "Good", 85
        elif issue_count <= 2 and warning_count <= 5:
            return "Fair", 70
        else:
            return "Poor", 50

    def generate_report(self) -> str:
        """Generate health check report"""
        health_status, health_score = self.calculate_health_score()

        issue_count = sum(len(items) for items in self.issues.values())
        warning_count = sum(len(items) for items in self.warnings.values())
        info_count = sum(len(items) for items in self.info.values())

        report = f"""# System Health Check Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Health Score:** {health_score}/100 ({health_status})

---

## Summary

- **Critical Issues:** {issue_count}
- **Warnings:** {warning_count}
- **Informational:** {info_count}

**Overall Status:** {'✅ Healthy' if health_status == 'Excellent' else '⚠️ Needs Attention' if health_status == 'Good' else '❌ Action Required'}

---

## Critical Issues ({issue_count})

"""
        if issue_count > 0:
            for category, items in self.issues.items():
                if items:
                    report += f"### {category.replace('_', ' ').title()}\n\n"
                    for item in items:
                        report += f"❌ {item}\n"
                    report += "\n"
        else:
            report += "None! System is healthy ✅\n"

        report += f"""
---

## Warnings ({warning_count})

"""
        if warning_count > 0:
            for category, items in self.warnings.items():
                if items:
                    report += f"### {category.replace('_', ' ').title()}\n\n"
                    for item in items:
                        report += f"⚠️ {item}\n"
                    report += "\n"
        else:
            report += "None! No warnings ✅\n"

        report += f"""
---

## Informational ({info_count})

"""
        if info_count > 0:
            for category, items in self.info.items():
                if items:
                    report += f"### {category.replace('_', ' ').title()}\n\n"
                    for item in items:
                        report += f"ℹ️ {item}\n"
                    report += "\n"
        else:
            report += "Nothing to report\n"

        report += """
---

## Recommended Actions

"""
        if issue_count > 0:
            report += "**Critical (Fix Immediately):**\n"
            if 'orphaned_files' in self.issues and self.issues['orphaned_files']:
                report += "1. Move orphaned job files to correct application folders or archive\n"
            if 'status_consistency' in self.issues and self.issues['status_consistency']:
                report += "2. Archive job files for terminal status applications (run `/update-status` again)\n"
            if 'missing_cvs' in self.issues and self.issues['missing_cvs']:
                report += "3. Generate missing CVs or update status (cannot be 'applied' without CV)\n"
            report += "\n"

        if warning_count > 0:
            report += "**Recommended (Address Soon):**\n"
            if 'stale_applications' in self.warnings and self.warnings['stale_applications']:
                report += "1. Review stale applications - withdraw or complete drafting\n"
            if 'long_wait' in self.warnings and self.warnings['long_wait']:
                report += "2. Follow up on applications waiting >14 days\n"
            if 'missing_files' in self.warnings and self.warnings['missing_files']:
                report += "3. Complete analysis for applications with missing files\n"
            report += "\n"

        if issue_count == 0 and warning_count == 0:
            report += "✅ No action required - system is healthy!\n\n"

        report += """---

## Health Check Schedule

**Frequency:** Run daily or before major activities (bulk submission, weekly review)

**Triggers:**
- Before submitting multiple applications
- After bulk `/analyze-job` runs
- Weekly maintenance (Sunday evening)
- When suspecting data inconsistency

**Command:**
```bash
python scripts/health_check.py
```

**Next Check:** {next_check}

---

## System Statistics

"""

        # Calculate stats
        total_apps = len(list(self.applications.glob("2025-*")))
        active_count = 0
        terminal_count = 0

        for app_folder in self.applications.glob("2025-*"):
            status_file = app_folder / "status.md"
            if status_file.exists():
                content = status_file.read_text(encoding='utf-8')
                if "**Current Status:** applied" in content:
                    active_count += 1
                elif any(s in content for s in ["rejected", "withdrawn", "accepted"]):
                    terminal_count += 1

        report += f"""
- **Total Applications:** {total_apps}
- **Active (Applied):** {active_count}
- **Terminal States:** {terminal_count}
- **Drafting/Other:** {total_apps - active_count - terminal_count}

**Pipeline Health:** {'✅ Clean' if issue_count == 0 else '⚠️ Needs Cleanup'}
"""

        next_check = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        report = report.format(next_check=next_check)

        return report

    def save_report(self, report: str):
        """Save health check report"""
        insights_path = Path("insights")
        insights_path.mkdir(exist_ok=True)

        filename = f"health-check-{datetime.now().strftime('%Y-%m-%d')}.md"
        output_path = insights_path / filename

        output_path.write_text(report, encoding='utf-8')
        print(f"📄 Report saved to: {output_path}")

        return output_path


def main():
    """Run system health check"""
    import sys
    import io

    # Set UTF-8 encoding for Windows console
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    print("🏥 System Health Check")
    print("=" * 50)
    print()

    checker = HealthChecker()
    checker.run_all_checks()

    health_status, health_score = checker.calculate_health_score()

    print()
    print(f"📊 Health Score: {health_score}/100 ({health_status})")
    print(f"  Critical Issues: {sum(len(items) for items in checker.issues.values())}")
    print(f"  Warnings: {sum(len(items) for items in checker.warnings.values())}")
    print()

    report = checker.generate_report()
    output_path = checker.save_report(report)

    print()
    if health_score < 70:
        print("❌ System health is poor - action required!")
        return 1
    elif health_score < 85:
        print("⚠️  System health is fair - review warnings")
        return 0
    else:
        print("✅ System is healthy!")
        return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
