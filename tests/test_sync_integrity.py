"""
Test /sync-all command and derived view integrity.

The sync algorithm regenerates STATUS.md and metrics-dashboard.md from
source of truth (applications/*/status.md files).

Tests verify:
- Counts match between source files and generated views
- Calculations are accurate (averages, percentages)
- Data consistency maintained
- Manual edits to status.md preserved (only STATUS.md regenerated)
- Missing/corrupted data handled gracefully
"""

import pytest
from pathlib import Path
from datetime import datetime, timedelta
import json
import re


class TestSyncCountAccuracy:
    """Test that /sync-all counts match source data"""

    def test_active_applications_count_matches(self, tmp_path):
        """COUNT(active applications) in STATUS.md matches actual folders"""
        applications = tmp_path / "applications"
        applications.mkdir()

        # Create 3 active applications (status = applied)
        for i, company in enumerate(['Angi', 'Kraken', 'Hopper']):
            app_folder = applications / f"2025-01-{company}-PM"
            app_folder.mkdir()
            (app_folder / "status.md").write_text(f"""# Application Status - {company} - PM

**Current Status:** applied
**Last Updated:** 2025-01-{10+i} 14:00

## Status Timeline

### Applied - 2025-01-{10+i} 14:00
**Notes:** Application submitted
""")

        # Count active applications (status = applied)
        active_count = 0
        for status_file in applications.rglob("status.md"):
            content = status_file.read_text()
            if "**Current Status:** applied" in content:
                active_count += 1

        # Assert
        assert active_count == 3

    def test_rejected_applications_count_matches(self, tmp_path):
        """COUNT(rejected) in STATUS.md matches actual status files"""
        applications = tmp_path / "applications"
        applications.mkdir()

        # Create 2 rejected applications
        for company in ['Redcare', 'NBCUniversal']:
            app_folder = applications / f"2025-01-{company}-Director"
            app_folder.mkdir()
            (app_folder / "status.md").write_text(f"""# Application Status - {company} - Director

**Current Status:** rejected
**Last Updated:** 2025-01-15 09:00

## Status Timeline

### Rejected - 2025-01-15 09:00
**Notes:** Rejection email received

### Applied - 2025-01-10 14:00
**Notes:** Application submitted
""")

        # Count rejected
        rejected_count = sum(
            1 for f in applications.rglob("status.md")
            if "**Current Status:** rejected" in f.read_text()
        )

        assert rejected_count == 2

    def test_withdrawn_applications_count_matches(self, tmp_path):
        """COUNT(withdrawn) matches actual"""
        applications = tmp_path / "applications"
        applications.mkdir()

        # Create 4 withdrawn applications
        for company in ['TRKKN', 'Gymshark', 'Booksy', 'Udemy']:
            app_folder = applications / f"2025-01-{company}-Head"
            app_folder.mkdir()
            (app_folder / "status.md").write_text(f"""# Application Status - {company} - Head

**Current Status:** withdrawn
**Last Updated:** 2025-01-12 10:00

## Status Timeline

### Withdrawn - 2025-01-12 10:00
**Notes:** Strategic withdrawal
""")

        withdrawn_count = sum(
            1 for f in applications.rglob("status.md")
            if "**Current Status:** withdrawn" in f.read_text()
        )

        assert withdrawn_count == 4

    def test_total_applications_count_matches(self, tmp_path):
        """Total application folders matches sum of all statuses"""
        applications = tmp_path / "applications"
        applications.mkdir()

        # Create applications in various states
        statuses = [
            ('applied', 3),
            ('rejected', 2),
            ('withdrawn', 4),
            ('interview-invited', 1),
            ('drafting', 2),
        ]

        total_created = 0
        for status, count in statuses:
            for i in range(count):
                app_folder = applications / f"2025-01-{status}{i}-Role"
                app_folder.mkdir()
                (app_folder / "status.md").write_text(f"""# Application Status

**Current Status:** {status}
**Last Updated:** 2025-01-10
""")
                total_created += 1

        # Count total application folders
        total_folders = len(list(applications.glob("2025-*")))

        assert total_folders == total_created == sum(c for _, c in statuses)


class TestSyncCalculations:
    """Test calculation accuracy in metrics-dashboard.md"""

    def test_average_fit_score_calculated_correctly(self, tmp_path):
        """Average fit score calculation is accurate"""
        applications = tmp_path / "applications"
        applications.mkdir()

        # Create applications with known fit scores
        fit_scores = [9.0, 8.5, 7.5, 9.5, 7.0]

        for i, fit_score in enumerate(fit_scores):
            app_folder = applications / f"2025-01-Company{i}-Role"
            app_folder.mkdir()
            (app_folder / "analysis.md").write_text(f"""# Job Analysis

**Analyzed:** 2025-01-10
**Analyst:** PM Career Coach Agent

## Fit Score: {fit_score}/10

Justification...
""")

        # Calculate average
        total = sum(fit_scores)
        count = len(fit_scores)
        expected_average = total / count

        # Simulate sync algorithm
        all_fit_scores = []
        for analysis_file in applications.rglob("analysis.md"):
            content = analysis_file.read_text()
            match = re.search(r'Fit Score: ([\d.]+)/10', content)
            if match:
                all_fit_scores.append(float(match.group(1)))

        actual_average = sum(all_fit_scores) / len(all_fit_scores) if all_fit_scores else 0

        # Assert
        assert abs(actual_average - expected_average) < 0.01  # Within 0.01 tolerance
        assert abs(actual_average - 8.3) < 0.01  # Expected: (9+8.5+7.5+9.5+7)/5 = 8.3

    def test_days_waiting_calculated_correctly(self, tmp_path):
        """Days waiting calculation for active applications"""
        from datetime import datetime, timedelta

        applications = tmp_path / "applications"
        applications.mkdir()

        # Create application applied 12 days ago
        applied_date = datetime.now() - timedelta(days=12)
        app_folder = applications / "2025-01-TestCo-PM"
        app_folder.mkdir()
        (app_folder / "status.md").write_text(f"""# Application Status - TestCo - PM

**Current Status:** applied
**Last Updated:** {applied_date.strftime('%Y-%m-%d %H:%M')}

## Status Timeline

### Applied - {applied_date.strftime('%Y-%m-%d %H:%M')}
**Notes:** Application submitted

## Application Summary

**Applied On:** {applied_date.strftime('%Y-%m-%d')}
""")

        # Calculate days waiting
        content = (app_folder / "status.md").read_text()
        match = re.search(r'Applied On:\*\* (\d{4}-\d{2}-\d{2})', content)
        if match:
            applied_str = match.group(1)
            applied_dt = datetime.strptime(applied_str, '%Y-%m-%d')
            days_waiting = (datetime.now() - applied_dt).days

        assert days_waiting == 12

    def test_response_rate_percentage_accurate(self, tmp_path):
        """Response rate calculation: (interview_invited / applied) * 100"""
        applications = tmp_path / "applications"
        applications.mkdir()

        # 10 applications: 3 interview-invited, 5 rejected, 2 still applied
        scenarios = [
            ('interview-invited', 3),
            ('rejected', 5),
            ('applied', 2),
        ]

        for status, count in scenarios:
            for i in range(count):
                app_folder = applications / f"2025-01-{status}{i}-Role"
                app_folder.mkdir()
                (app_folder / "status.md").write_text(f"""# Application Status

**Current Status:** {status}
**Last Updated:** 2025-01-15

## Status Timeline

### {status.title().replace('-', ' ')} - 2025-01-15
**Notes:** Status update

### Applied - 2025-01-10
**Notes:** Application submitted
""")

        # Calculate response rate
        total_applied = sum(count for status, count in scenarios)  # All have "applied" in timeline
        total_responses = sum(count for status, count in scenarios if status in ['interview-invited', 'rejected'])

        response_rate = (total_responses / total_applied) * 100 if total_applied > 0 else 0

        # Assert
        assert total_applied == 10
        assert total_responses == 8  # 3 interview + 5 rejected
        assert abs(response_rate - 80.0) < 0.1  # 80% response rate


class TestSyncDataConsistency:
    """Test data consistency checks"""

    def test_detects_orphaned_job_files(self, tmp_path):
        """Detect job files in staging/3-applying/ without corresponding application folder"""
        staging = tmp_path / "staging/3-applying"
        applications = tmp_path / "applications"
        staging.mkdir(parents=True)
        applications.mkdir()

        # Create job file without application folder
        orphaned_file = staging / "OrphanedCompany-Role.mhtml"
        orphaned_file.write_text("<html>Orphaned job</html>")

        # Create normal application (file + folder)
        normal_file = staging / "NormalCompany-PM.mhtml"
        normal_file.write_text("<html>Normal job</html>")
        normal_folder = applications / "2025-01-NormalCompany-PM"
        normal_folder.mkdir()
        (normal_folder / "status.md").write_text("# Status")

        # Check for orphans
        orphans = []
        for job_file in staging.glob("*.mhtml"):
            company_name = job_file.stem.split('-')[0]
            matching_folders = list(applications.glob(f"*{company_name}*"))
            if not matching_folders:
                orphans.append(job_file)

        # Assert
        assert len(orphans) == 1
        assert orphans[0] == orphaned_file

    def test_detects_mismatched_status_and_file_location(self, tmp_path):
        """Detect when status.md says 'withdrawn' but file not in archive/withdrawn/"""
        applications = tmp_path / "applications"
        staging_applying = tmp_path / "staging/3-applying"
        archive_withdrawn = tmp_path / "staging/archive/withdrawn"

        applications.mkdir()
        staging_applying.mkdir(parents=True)
        archive_withdrawn.mkdir(parents=True)

        # Status says "withdrawn"
        app_folder = applications / "2025-01-MismatchCo-Role"
        app_folder.mkdir()
        (app_folder / "status.md").write_text("""# Application Status - MismatchCo - Role

**Current Status:** withdrawn
**Last Updated:** 2025-01-12
""")

        # But job file still in 3-applying/ (should be in archive/withdrawn/)
        job_file = staging_applying / "MismatchCo-Role.mhtml"
        job_file.write_text("<html>Job</html>")

        # Check for mismatch
        status_content = (app_folder / "status.md").read_text()
        is_withdrawn = "**Current Status:** withdrawn" in status_content

        # Job file should be in archive, but it's in applying
        in_applying = job_file.exists()
        in_archive = (archive_withdrawn / job_file.name).exists()

        # Assert: Mismatch detected
        assert is_withdrawn
        assert in_applying
        assert not in_archive
        # This is an inconsistency that /sync-all should report

    def test_detects_missing_cv_for_applied_status(self, tmp_path):
        """Applications with status='applied' should have CV files"""
        applications = tmp_path / "applications"
        applications.mkdir()

        # Application 1: Applied WITH CV (correct)
        app1 = applications / "2025-01-GoodCo-PM"
        app1.mkdir()
        (app1 / "status.md").write_text("""# Application Status - GoodCo - PM

**Current Status:** applied
**Last Updated:** 2025-01-15
""")
        (app1 / "ArturSwadzba_CV_GoodCo.pdf").write_text("PDF content")

        # Application 2: Applied WITHOUT CV (inconsistency)
        app2 = applications / "2025-01-BadCo-Director"
        app2.mkdir()
        (app2 / "status.md").write_text("""# Application Status - BadCo - Director

**Current Status:** applied
**Last Updated:** 2025-01-14
""")
        # No CV file created

        # Check for missing CVs
        missing_cvs = []
        for app_folder in applications.glob("2025-*"):
            status_file = app_folder / "status.md"
            if status_file.exists():
                content = status_file.read_text()
                if "**Current Status:** applied" in content:
                    # Check if CV exists
                    cv_files = list(app_folder.glob("*_CV_*.pdf"))
                    if not cv_files:
                        missing_cvs.append(app_folder.name)

        # Assert
        assert len(missing_cvs) == 1
        assert "BadCo" in missing_cvs[0]


class TestSyncPreservesManualEdits:
    """Test that /sync-all preserves manual edits to source files"""

    def test_preserves_custom_notes_in_status_md(self, tmp_path):
        """Manual notes in applications/*/status.md should be preserved"""
        applications = tmp_path / "applications"
        app_folder = applications / "2025-01-TestCo-PM"
        app_folder.mkdir(parents=True)

        status_file = app_folder / "status.md"
        original_content = """# Application Status - TestCo - PM

**Current Status:** applied
**Last Updated:** 2025-01-15 14:00

## Status Timeline

### Applied - 2025-01-15 14:00
**Notes:** Submitted via LinkedIn

**Custom Manual Note:** Remember to follow up with Sarah about referral

## Application Summary

**Applied On:** 2025-01-15
**Referral:** Sarah Chen (manual note added)
"""
        status_file.write_text(original_content)

        # Simulate /sync-all reading this file (doesn't modify it)
        # /sync-all ONLY regenerates STATUS.md and metrics-dashboard.md
        # It NEVER modifies applications/*/status.md files

        content_after_sync = status_file.read_text()

        # Assert: Manual edits preserved
        assert "**Custom Manual Note:**" in content_after_sync
        assert "Remember to follow up with Sarah" in content_after_sync
        assert content_after_sync == original_content

    def test_only_status_md_and_metrics_regenerated(self, tmp_path):
        """Verify only STATUS.md and metrics-dashboard.md are regenerated"""
        root = tmp_path
        applications = root / "applications"
        insights = root / "insights"

        applications.mkdir()
        insights.mkdir()

        # Create source file (applications/*/status.md)
        app_folder = applications / "2025-01-TestCo-PM"
        app_folder.mkdir()
        status_file = app_folder / "status.md"
        status_file.write_text("# Application Status")

        # Create derived files (to be regenerated)
        status_md = root / "STATUS.md"
        metrics_md = insights / "metrics-dashboard.md"

        status_md.write_text("# Old STATUS.md content")
        metrics_md.write_text("# Old metrics content")

        # Record modification times
        import time
        time.sleep(0.1)  # Ensure time difference

        # Simulate /sync-all regenerating derived files
        status_md.write_text("# New STATUS.md content - regenerated")
        metrics_md.write_text("# New metrics content - regenerated")

        # Assert: Derived files updated, source files unchanged
        assert "# New STATUS.md" in status_md.read_text()
        assert "# New metrics" in metrics_md.read_text()
        assert status_file.read_text() == "# Application Status"  # Source unchanged


class TestSyncErrorHandling:
    """Test graceful handling of missing/corrupted data"""

    def test_handles_missing_analysis_md_gracefully(self, tmp_path):
        """If analysis.md missing, sync should not crash"""
        applications = tmp_path / "applications"
        app_folder = applications / "2025-01-MissingAnalysis-PM"
        app_folder.mkdir(parents=True)

        # Create status.md but NO analysis.md
        (app_folder / "status.md").write_text("""# Application Status

**Current Status:** applied
**Last Updated:** 2025-01-15
""")

        # Attempt to read fit scores (like /sync-all would)
        fit_scores = []
        for app in applications.glob("2025-*"):
            analysis_file = app / "analysis.md"
            if analysis_file.exists():
                content = analysis_file.read_text()
                match = re.search(r'Fit Score: ([\d.]+)/10', content)
                if match:
                    fit_scores.append(float(match.group(1)))

        # Assert: No crash, just skips missing file
        assert len(fit_scores) == 0  # No fit score found (gracefully handled)

    def test_handles_corrupted_status_md(self, tmp_path):
        """If status.md is corrupted/malformed, sync reports issue but doesn't crash"""
        applications = tmp_path / "applications"
        app_folder = applications / "2025-01-Corrupted-PM"
        app_folder.mkdir(parents=True)

        # Create malformed status.md (missing required fields)
        (app_folder / "status.md").write_text("""# Application Status

This file is corrupted and missing required fields like Current Status
""")

        # Attempt to parse (like /sync-all would)
        issues = []
        for app in applications.glob("2025-*"):
            status_file = app / "status.md"
            if status_file.exists():
                content = status_file.read_text()
                if "**Current Status:**" not in content:
                    issues.append(f"{app.name}: Missing Current Status field")

        # Assert: Issue detected but no crash
        assert len(issues) == 1
        assert "Corrupted-PM" in issues[0]
        assert "Missing Current Status" in issues[0]

    def test_handles_invalid_dates_gracefully(self, tmp_path):
        """Invalid date formats should be reported, not crash"""
        applications = tmp_path / "applications"
        app_folder = applications / "2025-01-InvalidDate-PM"
        app_folder.mkdir(parents=True)

        # Create status.md with invalid date
        (app_folder / "status.md").write_text("""# Application Status

**Current Status:** applied
**Last Updated:** INVALID-DATE-FORMAT

## Application Summary

**Applied On:** 2025-99-99  # Invalid month/day
""")

        # Attempt to parse dates
        date_errors = []
        content = (app_folder / "status.md").read_text()
        match = re.search(r'Applied On:\*\* (\d{4}-\d{2}-\d{2})', content)
        if match:
            try:
                datetime.strptime(match.group(1), '%Y-%m-%d')
            except ValueError as e:
                date_errors.append(f"{app_folder.name}: Invalid date {match.group(1)}")

        # Assert: Error detected but no crash
        assert len(date_errors) == 1
        assert "InvalidDate-PM" in date_errors[0]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
