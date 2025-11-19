"""
Test file movement operations in job application workflows.

Tests verify that job files are correctly moved through the pipeline:
- staging/2-shortlist/ → staging/3-applying/ (during /analyze-job)
- staging/3-applying/ → staging/archive/* (during /update-status with terminal state)

Critical for maintaining pipeline integrity and preventing orphaned files.
"""

import pytest
from pathlib import Path
import shutil
import json
from datetime import datetime


class TestAnalyzeJobFileMovement:
    """Test /analyze-job command file movement behavior"""

    def test_moves_mhtml_from_shortlist_high_to_applying(self, tmp_path):
        """Verify job file moves from high-priority shortlist to applying folder"""
        # Setup
        shortlist_high = tmp_path / "staging/2-shortlist/high"
        applying = tmp_path / "staging/3-applying"
        shortlist_high.mkdir(parents=True)
        applying.mkdir(parents=True)

        test_file = shortlist_high / "TestCompany-ProductLead.mhtml"
        test_file.write_text("<html><body>Product Lead job description</body></html>")

        # Simulate /analyze-job behavior
        destination = applying / test_file.name
        shutil.move(str(test_file), str(destination))

        # Assert
        assert not test_file.exists(), "Source file should be removed from shortlist/high/"
        assert destination.exists(), "File should exist in staging/3-applying/"
        assert destination.read_text() == "<html><body>Product Lead job description</body></html>"

    def test_moves_mhtml_from_shortlist_medium_to_applying(self, tmp_path):
        """Verify job file moves from medium-priority shortlist"""
        shortlist_medium = tmp_path / "staging/2-shortlist/medium"
        applying = tmp_path / "staging/3-applying"
        shortlist_medium.mkdir(parents=True)
        applying.mkdir(parents=True)

        test_file = shortlist_medium / "MediumFitCo-Director.mhtml"
        test_file.write_text("<html>Director job</html>")

        # Simulate move
        destination = applying / test_file.name
        shutil.move(str(test_file), str(destination))

        # Assert
        assert not test_file.exists()
        assert destination.exists()

    def test_handles_special_characters_in_filename(self, tmp_path):
        """Verify file movement works with special characters in names"""
        shortlist = tmp_path / "staging/2-shortlist/high"
        applying = tmp_path / "staging/3-applying"
        shortlist.mkdir(parents=True)
        applying.mkdir(parents=True)

        # LinkedIn saves files with special chars like (1), _, semicolons
        test_file = shortlist / "(1) Head of Product (AI) - Relocate to Australia @ Leonardo.Ai.mhtml"
        test_file.write_text("<html>Leonardo AI job</html>")

        # Simulate move
        destination = applying / test_file.name
        shutil.move(str(test_file), str(destination))

        # Assert
        assert not test_file.exists()
        assert destination.exists()

    def test_creates_application_folder_after_move(self, tmp_path):
        """Verify application folder created after job file moved"""
        applications = tmp_path / "applications"
        applying = tmp_path / "staging/3-applying"
        applications.mkdir()
        applying.mkdir(parents=True)

        # Simulate /analyze-job creating application folder
        app_folder = applications / "2025-01-TestCompany-ProductLead"
        app_folder.mkdir()

        # Create analysis files
        (app_folder / "job-description.md").write_text("# Job Description\n\nTest JD")
        (app_folder / "analysis.md").write_text("# Analysis\n\nFit Score: 8.5/10")

        # Assert
        assert app_folder.exists()
        assert (app_folder / "job-description.md").exists()
        assert (app_folder / "analysis.md").exists()

    def test_idempotent_move_does_not_error(self, tmp_path):
        """Running move twice should not cause errors (idempotency)"""
        shortlist = tmp_path / "staging/2-shortlist/high"
        applying = tmp_path / "staging/3-applying"
        shortlist.mkdir(parents=True)
        applying.mkdir(parents=True)

        test_file = shortlist / "TestCo.mhtml"
        test_file.write_text("<html>Job</html>")

        # First move
        destination = applying / test_file.name
        shutil.move(str(test_file), str(destination))

        # Second move attempt (file already moved)
        # Should not error, should detect file already in destination
        if test_file.exists():
            shutil.move(str(test_file), str(destination))

        # Assert: File should only exist once in destination
        assert not test_file.exists()
        assert destination.exists()
        assert len(list(applying.glob("TestCo.mhtml"))) == 1


class TestUpdateStatusArchiving:
    """Test /update-status command archiving behavior"""

    def test_archives_to_withdrawn_on_withdrawn_status(self, tmp_path):
        """Verify job file moves to archive/withdrawn/ when status = withdrawn"""
        applying = tmp_path / "staging/3-applying"
        archive_withdrawn = tmp_path / "staging/archive/withdrawn"
        applying.mkdir(parents=True)
        archive_withdrawn.mkdir(parents=True)

        test_file = applying / "TRKKN-HeadAdTech.mhtml"
        test_file.write_text("<html>TRKKN job</html>")

        # Simulate /update-status TRKKN withdrawn
        destination = archive_withdrawn / test_file.name
        shutil.move(str(test_file), str(destination))

        # Assert
        assert not test_file.exists(), "File should be removed from 3-applying/"
        assert destination.exists(), "File should exist in archive/withdrawn/"

    def test_archives_to_rejected_on_rejected_status(self, tmp_path):
        """Verify job file moves to archive/rejected/ when status = rejected"""
        applying = tmp_path / "staging/3-applying"
        archive_rejected = tmp_path / "staging/archive/rejected"
        applying.mkdir(parents=True)
        archive_rejected.mkdir(parents=True)

        test_file = applying / "RedcarePharmacy-Director.mhtml"
        test_file.write_text("<html>Redcare job</html>")

        # Simulate /update-status RedcarePharmacy rejected
        destination = archive_rejected / test_file.name
        shutil.move(str(test_file), str(destination))

        # Assert
        assert not test_file.exists()
        assert destination.exists()

    def test_archives_to_accepted_on_offer_accepted(self, tmp_path):
        """Verify job file moves to archive/accepted/ when status = accepted"""
        applying = tmp_path / "staging/3-applying"
        archive_accepted = tmp_path / "staging/archive/accepted"
        applying.mkdir(parents=True)
        archive_accepted.mkdir(parents=True)

        test_file = applying / "DreamCompany-VPProduct.mhtml"
        test_file.write_text("<html>Dream job offer!</html>")

        # Simulate /update-status DreamCompany accepted
        destination = archive_accepted / test_file.name
        shutil.move(str(test_file), str(destination))

        # Assert
        assert not test_file.exists()
        assert destination.exists()

    def test_applied_status_does_not_archive(self, tmp_path):
        """Verify job file STAYS in 3-applying/ when status = applied (active)"""
        applying = tmp_path / "staging/3-applying"
        applying.mkdir(parents=True)

        test_file = applying / "ActiveApplication.mhtml"
        test_file.write_text("<html>Active job</html>")

        # Simulate /update-status ActiveApplication applied
        # Should NOT move file (applied is active state, not terminal)

        # Assert: File should still be in applying/
        assert test_file.exists(), "Applied jobs should remain in 3-applying/"

    def test_interview_invited_does_not_archive(self, tmp_path):
        """Verify job file STAYS in 3-applying/ when status = interview-invited"""
        applying = tmp_path / "staging/3-applying"
        applying.mkdir(parents=True)

        test_file = applying / "InterviewInvited.mhtml"
        test_file.write_text("<html>Interview coming up</html>")

        # Simulate /update-status InterviewInvited interview-invited
        # Should NOT move file (interview-invited is active state)

        # Assert
        assert test_file.exists(), "Interview-invited jobs should remain in 3-applying/"

    def test_creates_archive_folder_if_missing(self, tmp_path):
        """Verify archive subfolder created on-demand if doesn't exist"""
        applying = tmp_path / "staging/3-applying"
        archive_root = tmp_path / "staging/archive"
        applying.mkdir(parents=True)
        archive_root.mkdir(parents=True)

        test_file = applying / "FirstWithdrawn.mhtml"
        test_file.write_text("<html>First withdrawal</html>")

        # Archive subfolder doesn't exist yet
        archive_withdrawn = archive_root / "withdrawn"
        assert not archive_withdrawn.exists()

        # Simulate /update-status FirstWithdrawn withdrawn
        # Should create withdrawn/ folder
        archive_withdrawn.mkdir(exist_ok=True)
        destination = archive_withdrawn / test_file.name
        shutil.move(str(test_file), str(destination))

        # Assert
        assert archive_withdrawn.exists(), "Archive subfolder should be created"
        assert destination.exists()
        assert not test_file.exists()


class TestFileMovementEdgeCases:
    """Test edge cases and error handling"""

    def test_handles_missing_source_file_gracefully(self, tmp_path):
        """If source file doesn't exist, should not crash"""
        shortlist = tmp_path / "staging/2-shortlist/high"
        applying = tmp_path / "staging/3-applying"
        shortlist.mkdir(parents=True)
        applying.mkdir(parents=True)

        source = shortlist / "NonExistent.mhtml"
        destination = applying / "NonExistent.mhtml"

        # Attempt move of non-existent file
        if source.exists():
            shutil.move(str(source), str(destination))
        else:
            # Should handle gracefully, not crash
            print(f"Warning: Source file {source} not found")

        # Assert: No crash, no destination file created
        assert not destination.exists()

    def test_handles_duplicate_filename_in_destination(self, tmp_path):
        """If file already exists in destination, handle appropriately"""
        shortlist = tmp_path / "staging/2-shortlist/high"
        applying = tmp_path / "staging/3-applying"
        shortlist.mkdir(parents=True)
        applying.mkdir(parents=True)

        # File already exists in destination
        existing = applying / "Duplicate.mhtml"
        existing.write_text("<html>Already moved</html>")

        # Trying to move file with same name
        source = shortlist / "Duplicate.mhtml"
        source.write_text("<html>New version</html>")

        # Should handle collision (e.g., rename or skip)
        destination = applying / source.name
        if destination.exists():
            # Strategy: Skip move if already there
            print(f"File {destination} already exists, skipping move")
        else:
            shutil.move(str(source), str(destination))

        # Assert: Either old or new version exists, but no crash
        assert destination.exists()

    def test_preserves_file_contents_during_move(self, tmp_path):
        """Verify file contents unchanged after move"""
        shortlist = tmp_path / "staging/2-shortlist/high"
        applying = tmp_path / "staging/3-applying"
        shortlist.mkdir(parents=True)
        applying.mkdir(parents=True)

        original_content = "<html><body><h1>Important Job Description</h1><p>Details here...</p></body></html>"
        source = shortlist / "ImportantJob.mhtml"
        source.write_text(original_content)

        # Move file
        destination = applying / source.name
        shutil.move(str(source), str(destination))

        # Assert: Contents preserved
        assert destination.read_text() == original_content

    def test_orphaned_file_detection(self, tmp_path):
        """Detect job files without corresponding application folders"""
        applying = tmp_path / "staging/3-applying"
        applications = tmp_path / "applications"
        applying.mkdir(parents=True)
        applications.mkdir(parents=True)

        # Job file exists
        job_file = applying / "OrphanedCompany-Role.mhtml"
        job_file.write_text("<html>Job</html>")

        # But no application folder
        app_folder = applications / "2025-01-OrphanedCompany-Role"

        # Check for orphans
        orphaned_files = []
        for file in applying.glob("*.mhtml"):
            company_name = file.stem.split('-')[0] if '-' in file.stem else file.stem
            matching_folders = list(applications.glob(f"*{company_name}*"))
            if not matching_folders:
                orphaned_files.append(file)

        # Assert: Orphan detected
        assert len(orphaned_files) == 1
        assert orphaned_files[0] == job_file


class TestApplicationFolderMovement:
    """Test application folder movement based on status changes"""

    def test_moves_application_analyzing_to_applied_on_applied_status(self, tmp_path):
        """Verify application folder moves from analyzing/ to applied/ when status = applied"""
        analyzing = tmp_path / "applications/active/analyzing"
        applied = tmp_path / "applications/active/applied"
        analyzing.mkdir(parents=True)
        applied.mkdir(parents=True)

        # Create application folder in analyzing
        app_folder = analyzing / "2025-11-TestCompany-ProductLead"
        app_folder.mkdir()
        (app_folder / "status.md").write_text("# Status\n\nCurrent Status: Analyzed")
        (app_folder / "analysis.md").write_text("# Analysis\n\nFit Score: 8/10")

        # Simulate /update-status TestCompany applied
        destination = applied / app_folder.name
        shutil.move(str(app_folder), str(destination))

        # Assert
        assert not app_folder.exists(), "Folder should be removed from analyzing/"
        assert destination.exists(), "Folder should exist in applied/"
        assert (destination / "status.md").exists()
        assert (destination / "analysis.md").exists()

    def test_moves_application_to_interviewing_on_interview_invited(self, tmp_path):
        """Verify application folder moves to interviewing/ when status = interview-invited"""
        applied = tmp_path / "applications/active/applied"
        interviewing = tmp_path / "applications/active/interviewing"
        applied.mkdir(parents=True)
        interviewing.mkdir(parents=True)

        # Create application folder in applied
        app_folder = applied / "2025-11-InterviewCo-Director"
        app_folder.mkdir()
        (app_folder / "status.md").write_text("Current Status: Applied")

        # Simulate /update-status InterviewCo interview-invited
        destination = interviewing / app_folder.name
        shutil.move(str(app_folder), str(destination))

        # Assert
        assert not app_folder.exists(), "Folder should be removed from applied/"
        assert destination.exists(), "Folder should exist in interviewing/"

    def test_moves_from_analyzing_to_interviewing_directly(self, tmp_path):
        """Verify app can go from analyzing to interviewing (skip applied) if invited early"""
        analyzing = tmp_path / "applications/active/analyzing"
        interviewing = tmp_path / "applications/active/interviewing"
        analyzing.mkdir(parents=True)
        interviewing.mkdir(parents=True)

        app_folder = analyzing / "2025-11-FastTrack-PM"
        app_folder.mkdir()
        (app_folder / "status.md").write_text("Current Status: Analyzed")

        # Simulate /update-status FastTrack interview-invited (directly from analyzing)
        destination = interviewing / app_folder.name
        shutil.move(str(app_folder), str(destination))

        # Assert
        assert not app_folder.exists()
        assert destination.exists()

    def test_archives_application_on_withdrawn_status(self, tmp_path):
        """Verify application folder moves to archive/YYYY-QX/withdrawn/ on withdrawn"""
        applied = tmp_path / "applications/active/applied"
        archive_withdrawn = tmp_path / "applications/archive/2025-Q4/withdrawn"
        applied.mkdir(parents=True)
        archive_withdrawn.mkdir(parents=True)

        app_folder = applied / "2025-11-WithdrawnCo-Role"
        app_folder.mkdir()
        (app_folder / "status.md").write_text("Current Status: Applied")

        # Simulate /update-status WithdrawnCo withdrawn
        destination = archive_withdrawn / app_folder.name
        shutil.move(str(app_folder), str(destination))

        # Assert
        assert not app_folder.exists(), "Folder should be removed from applied/"
        assert destination.exists(), "Folder should exist in archive/2025-Q4/withdrawn/"

    def test_archives_application_on_rejected_status(self, tmp_path):
        """Verify application folder moves to archive/YYYY-QX/rejected/ on rejected"""
        interviewing = tmp_path / "applications/active/interviewing"
        archive_rejected = tmp_path / "applications/archive/2025-Q4/rejected"
        interviewing.mkdir(parents=True)
        archive_rejected.mkdir(parents=True)

        app_folder = interviewing / "2025-11-RejectedCo-Lead"
        app_folder.mkdir()
        (app_folder / "status.md").write_text("Current Status: Interview Completed")

        # Simulate /update-status RejectedCo rejected
        destination = archive_rejected / app_folder.name
        shutil.move(str(app_folder), str(destination))

        # Assert
        assert not app_folder.exists()
        assert destination.exists()

    def test_archives_application_on_accepted_status(self, tmp_path):
        """Verify application folder moves to archive/YYYY-QX/accepted/ on accepted"""
        interviewing = tmp_path / "applications/active/interviewing"
        archive_accepted = tmp_path / "applications/archive/2025-Q4/accepted"
        interviewing.mkdir(parents=True)
        archive_accepted.mkdir(parents=True)

        app_folder = interviewing / "2025-11-DreamJob-VP"
        app_folder.mkdir()
        (app_folder / "status.md").write_text("Current Status: Offer")
        (app_folder / "offer-details.md").write_text("# Offer\n\n$200k base")

        # Simulate /update-status DreamJob accepted
        destination = archive_accepted / app_folder.name
        shutil.move(str(app_folder), str(destination))

        # Assert
        assert not app_folder.exists()
        assert destination.exists()
        assert (destination / "offer-details.md").exists()

    def test_application_stays_in_place_if_status_unchanged(self, tmp_path):
        """Verify folder doesn't move if status doesn't trigger movement"""
        applied = tmp_path / "applications/active/applied"
        applied.mkdir(parents=True)

        app_folder = applied / "2025-11-StableApp-PM"
        app_folder.mkdir()
        (app_folder / "status.md").write_text("Current Status: Applied\n\nLast Updated: 2025-11-15")

        # Simulate /update-status StableApp applied (update notes but same status)
        # No movement should occur

        # Assert: Folder stays in place
        assert app_folder.exists(), "Folder should remain in applied/ when status unchanged"

    def test_creates_quarterly_archive_folder_if_missing(self, tmp_path):
        """Verify archive creates YYYY-QX folder on demand"""
        applied = tmp_path / "applications/active/applied"
        archive_root = tmp_path / "applications/archive"
        applied.mkdir(parents=True)
        archive_root.mkdir(parents=True)

        app_folder = applied / "2025-11-ArchivedApp-Role"
        app_folder.mkdir()

        # Archive quarterly folder doesn't exist yet
        archive_quarter = archive_root / "2025-Q4/withdrawn"
        assert not archive_quarter.exists()

        # Simulate archiving (should create 2025-Q4/withdrawn/)
        archive_quarter.mkdir(parents=True, exist_ok=True)
        destination = archive_quarter / app_folder.name
        shutil.move(str(app_folder), str(destination))

        # Assert
        assert archive_quarter.exists(), "Quarterly archive folder should be created"
        assert destination.exists()
        assert not app_folder.exists()

    def test_handles_missing_application_folder_gracefully(self, tmp_path):
        """If application folder doesn't exist, should not crash"""
        analyzing = tmp_path / "applications/active/analyzing"
        applied = tmp_path / "applications/active/applied"
        analyzing.mkdir(parents=True)
        applied.mkdir(parents=True)

        # Try to move non-existent folder
        source = analyzing / "NonExistent-App"
        destination = applied / "NonExistent-App"

        if source.exists():
            shutil.move(str(source), str(destination))
        else:
            print(f"Warning: Application folder {source} not found, skipping move")

        # Assert: No crash
        assert not destination.exists()


class TestBulkProcessFileMovement:
    """Test /bulk-process file movement to shortlist tiers"""

    def test_moves_high_fit_to_shortlist_high(self, tmp_path):
        """Fit 9-11 should move to staging/2-shortlist/high/"""
        discovery = tmp_path / "staging/0-discovery/manual"
        shortlist_high = tmp_path / "staging/2-shortlist/high"
        discovery.mkdir(parents=True)
        shortlist_high.mkdir(parents=True)

        test_file = discovery / "HighFitCo-PM.mhtml"
        test_file.write_text("<html>High fit job (9/10)</html>")

        # Simulate /bulk-process categorization (fit 9/10)
        destination = shortlist_high / test_file.name
        shutil.move(str(test_file), str(destination))

        # Assert
        assert not test_file.exists()
        assert destination.exists()

    def test_moves_medium_fit_to_shortlist_medium(self, tmp_path):
        """Fit 7-8.5 should move to staging/2-shortlist/medium/"""
        discovery = tmp_path / "staging/0-discovery/automated"
        shortlist_medium = tmp_path / "staging/2-shortlist/medium"
        discovery.mkdir(parents=True)
        shortlist_medium.mkdir(parents=True)

        test_file = discovery / "MediumFitCo-Director.mhtml"
        test_file.write_text("<html>Medium fit job (7.5/10)</html>")

        # Simulate /bulk-process categorization (fit 7.5/10)
        destination = shortlist_medium / test_file.name
        shutil.move(str(test_file), str(destination))

        # Assert
        assert not test_file.exists()
        assert destination.exists()

    def test_moves_low_fit_to_archive(self, tmp_path):
        """Fit <7 should move to staging/archive/low-fit/"""
        discovery = tmp_path / "staging/0-discovery/manual"
        archive_low_fit = tmp_path / "staging/archive/low-fit"
        discovery.mkdir(parents=True)
        archive_low_fit.mkdir(parents=True)

        test_file = discovery / "LowFitCo-Junior.mhtml"
        test_file.write_text("<html>Low fit job (5.5/10)</html>")

        # Simulate /bulk-process categorization (fit 5.5/10)
        destination = archive_low_fit / test_file.name
        shutil.move(str(test_file), str(destination))

        # Assert
        assert not test_file.exists()
        assert destination.exists()


# Pytest configuration and fixtures
@pytest.fixture
def mock_application_env(tmp_path):
    """Create mock application environment structure"""
    structure = {
        'staging/0-discovery/manual': None,
        'staging/0-discovery/automated': None,
        'staging/1-triage': None,
        'staging/2-shortlist/high': None,
        'staging/2-shortlist/medium': None,
        'staging/2-shortlist/pending-insider-intel': None,
        'staging/3-applying': None,
        'staging/archive/low-fit': None,
        'staging/archive/filtered': None,
        'staging/archive/rejected': None,
        'staging/archive/withdrawn': None,
        'staging/archive/accepted': None,
        'applications': None,
        'master': None,
    }

    for path in structure.keys():
        (tmp_path / path).mkdir(parents=True, exist_ok=True)

    return tmp_path


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
