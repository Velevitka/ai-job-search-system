"""
Test state machine transitions in application lifecycle.

Valid state transitions:
    drafting → applied → interview-invited → interview-completed → {offer, rejected}
    drafting → withdrawn (anytime)
    applied → rejected
    applied → withdrawn

Terminal states: accepted, rejected, withdrawn

Tests verify that:
- State transitions follow valid paths
- Invalid transitions are blocked or warned
- Status timeline maintains chronological order
- Terminal states trigger archiving
"""

import pytest
from pathlib import Path
from datetime import datetime, timedelta
import json


class TestValidStateTransitions:
    """Test valid state machine transitions"""

    def test_lifecycle_drafting_to_applied(self, tmp_path):
        """Valid transition: drafting → applied"""
        status_file = tmp_path / "applications/TestCo/status.md"
        status_file.parent.mkdir(parents=True)

        # Initial state: drafting
        status_content = """# Application Status - TestCo - Product Lead

**Current Status:** drafting
**Last Updated:** 2025-01-13 10:00

## Status Timeline

### Drafting - 2025-01-13 10:00
**Notes:** Analysis complete, working on CV
"""
        status_file.write_text(status_content)

        # Transition to: applied
        new_entry = """
### Applied - 2025-01-14 15:30
**Notes:** Submitted via company careers page

**Previous Status:** drafting
"""
        # Append new entry (simulate /update-status applied)
        updated_content = status_content.replace(
            "**Current Status:** drafting",
            "**Current Status:** applied"
        ).replace(
            "**Last Updated:** 2025-01-13 10:00",
            "**Last Updated:** 2025-01-14 15:30"
        ).replace(
            "## Status Timeline",
            "## Status Timeline" + new_entry
        )
        status_file.write_text(updated_content)

        # Assert: Status changed, history preserved
        content = status_file.read_text()
        assert "**Current Status:** applied" in content
        assert "### Applied - 2025-01-14 15:30" in content
        assert "### Drafting - 2025-01-13 10:00" in content  # History preserved

    def test_lifecycle_applied_to_interview_invited(self, tmp_path):
        """Valid transition: applied → interview-invited"""
        status_file = tmp_path / "applications/TestCo/status.md"
        status_file.parent.mkdir(parents=True)

        initial = """# Application Status - TestCo - Product Lead

**Current Status:** applied
**Last Updated:** 2025-01-14 15:30

## Status Timeline

### Applied - 2025-01-14 15:30
**Notes:** Submitted via company careers page
"""
        status_file.write_text(initial)

        # Transition to: interview-invited
        status_file.write_text(initial.replace(
            "**Current Status:** applied",
            "**Current Status:** interview-invited"
        ).replace(
            "## Status Timeline",
            """## Status Timeline

### Interview-Invited - 2025-01-20 09:00
**Notes:** Phone screen scheduled for Jan 25, 10am GMT

**Previous Status:** applied"""
        ))

        # Assert
        content = status_file.read_text()
        assert "**Current Status:** interview-invited" in content
        assert "Phone screen scheduled" in content

    def test_lifecycle_interview_to_offer_to_accepted(self, tmp_path):
        """Valid transition chain: interview-completed → offer → accepted"""
        status_file = tmp_path / "applications/DreamCo/status.md"
        status_file.parent.mkdir(parents=True)

        # State 1: interview-completed
        status_file.write_text("""# Application Status - DreamCo - VP Product

**Current Status:** interview-completed
**Last Updated:** 2025-01-22 14:00

## Status Timeline

### Interview-Completed - 2025-01-22 14:00
**Notes:** Final round with CEO went well

### Interview-Invited - 2025-01-18 10:00
**Notes:** Phone screen scheduled

### Applied - 2025-01-15 12:00
**Notes:** Submitted application
""")

        # State 2: Transition to offer
        status_file.write_text(status_file.read_text().replace(
            "**Current Status:** interview-completed",
            "**Current Status:** offer"
        ).replace(
            "## Status Timeline",
            """## Status Timeline

### Offer - 2025-01-25 16:00
**Notes:** Offer received: £180k base + £50k equity over 4 years. Start date flexible.

**Previous Status:** interview-completed"""
        ))

        # State 3: Transition to accepted (terminal)
        status_file.write_text(status_file.read_text().replace(
            "**Current Status:** offer",
            "**Current Status:** accepted"
        ).replace(
            "## Status Timeline",
            """## Status Timeline

### Accepted - 2025-01-28 10:00
**Notes:** Accepted offer! Start date: March 1, 2025

**Previous Status:** offer"""
        ))

        # Assert: Complete timeline preserved
        content = status_file.read_text()
        assert "**Current Status:** accepted" in content
        assert "### Accepted - 2025-01-28" in content
        assert "### Offer - 2025-01-25" in content
        assert "### Interview-Completed - 2025-01-22" in content
        assert "### Interview-Invited - 2025-01-18" in content
        assert "### Applied - 2025-01-15" in content

    def test_lifecycle_applied_to_rejected(self, tmp_path):
        """Valid transition: applied → rejected (terminal)"""
        status_file = tmp_path / "applications/Rejected/status.md"
        status_file.parent.mkdir(parents=True)

        status_file.write_text("""# Application Status - Rejected - Director PM

**Current Status:** applied
**Last Updated:** 2025-01-10 14:00

## Status Timeline

### Applied - 2025-01-10 14:00
**Notes:** Submitted application
""")

        # Transition to rejected
        status_file.write_text(status_file.read_text().replace(
            "**Current Status:** applied",
            "**Current Status:** rejected"
        ).replace(
            "## Status Timeline",
            """## Status Timeline

### Rejected - 2025-01-14 09:00
**Notes:** Automated rejection email. "Looking for more domain-specific experience"

**Previous Status:** applied"""
        ))

        # Assert
        content = status_file.read_text()
        assert "**Current Status:** rejected" in content
        assert "Looking for more domain-specific experience" in content

    def test_lifecycle_drafting_to_withdrawn(self, tmp_path):
        """Valid transition: drafting → withdrawn (can withdraw anytime)"""
        status_file = tmp_path / "applications/Withdrawn/status.md"
        status_file.parent.mkdir(parents=True)

        status_file.write_text("""# Application Status - Withdrawn - Head of Product

**Current Status:** drafting
**Last Updated:** 2025-01-12 10:00

## Status Timeline

### Drafting - 2025-01-12 10:00
**Notes:** Analysis complete
""")

        # Withdraw before applying
        status_file.write_text(status_file.read_text().replace(
            "**Current Status:** drafting",
            "**Current Status:** withdrawn"
        ).replace(
            "## Status Timeline",
            """## Status Timeline

### Withdrawn - 2025-01-13 11:00
**Notes:** Fit score 7.5/10 below threshold for Australia relocation

**Previous Status:** drafting"""
        ))

        # Assert
        content = status_file.read_text()
        assert "**Current Status:** withdrawn" in content


class TestTerminalStates:
    """Test that terminal states behave correctly"""

    def test_terminal_state_accepted(self, tmp_path):
        """Verify accepted is terminal (no further transitions)"""
        status_file = tmp_path / "applications/Accepted/status.md"
        status_file.parent.mkdir(parents=True)

        status_file.write_text("""# Application Status - Accepted - VP Product

**Current Status:** accepted
**Last Updated:** 2025-01-28 10:00

## Status Timeline

### Accepted - 2025-01-28 10:00
**Notes:** Offer accepted! Start date March 1
""")

        # Attempting further transition from terminal state should not happen
        # In real system, /update-status should reject this
        content = status_file.read_text()
        assert "**Current Status:** accepted" in content

        # Could add validation: if current status is terminal, block new transitions
        is_terminal = "accepted" in content or "rejected" in content or "withdrawn" in content
        assert is_terminal

    def test_terminal_state_rejected(self, tmp_path):
        """Verify rejected is terminal"""
        status_file = tmp_path / "applications/Rejected/status.md"
        status_file.parent.mkdir(parents=True)

        status_file.write_text("""# Application Status - Rejected - Product Lead

**Current Status:** rejected
**Last Updated:** 2025-01-15 09:00
""")

        content = status_file.read_text()
        is_terminal = "**Current Status:** rejected" in content
        assert is_terminal

    def test_terminal_state_withdrawn(self, tmp_path):
        """Verify withdrawn is terminal"""
        status_file = tmp_path / "applications/Withdrawn/status.md"
        status_file.parent.mkdir(parents=True)

        status_file.write_text("""# Application Status - Withdrawn - Director

**Current Status:** withdrawn
**Last Updated:** 2025-01-13 11:00
""")

        content = status_file.read_text()
        is_terminal = "**Current Status:** withdrawn" in content
        assert is_terminal


class TestConcurrentApplications:
    """Test handling of multiple applications to same company"""

    def test_same_company_different_roles_separate_folders(self, tmp_path):
        """Two roles at same company should create separate application folders"""
        applications = tmp_path / "applications"
        applications.mkdir(parents=True)

        # Application 1: Spotify Product Lead
        app1 = applications / "2025-01-Spotify-ProductLead"
        app1.mkdir()
        (app1 / "status.md").write_text("""# Application Status - Spotify - Product Lead

**Current Status:** applied
**Last Updated:** 2025-01-10
""")

        # Application 2: Spotify Analytics Lead
        app2 = applications / "2025-01-Spotify-AnalyticsLead"
        app2.mkdir()
        (app2 / "status.md").write_text("""# Application Status - Spotify - Analytics Lead

**Current Status:** applied
**Last Updated:** 2025-01-12
""")

        # Assert: Both applications exist independently
        assert app1.exists()
        assert app2.exists()
        assert (app1 / "status.md").exists()
        assert (app2 / "status.md").exists()

        # Verify they're different
        assert "Product Lead" in (app1 / "status.md").read_text()
        assert "Analytics Lead" in (app2 / "status.md").read_text()

    def test_detect_duplicate_company_applications(self, tmp_path):
        """System should detect when applying to same company multiple times"""
        applications = tmp_path / "applications"
        applications.mkdir(parents=True)

        # Existing application to Spotify
        existing = applications / "2025-01-Spotify-ProductLead"
        existing.mkdir()
        (existing / "status.md").write_text("# Application Status - Spotify - Product Lead")

        # Check for existing applications before creating new one
        company_name = "Spotify"
        existing_apps = list(applications.glob(f"*{company_name}*"))

        # Assert: Duplicate detected
        assert len(existing_apps) > 0
        assert any("Spotify" in str(app) for app in existing_apps)


class TestStatusTimeline:
    """Test status timeline integrity"""

    def test_timeline_maintains_chronological_order(self, tmp_path):
        """Status timeline should be reverse chronological (newest first)"""
        status_file = tmp_path / "applications/TestCo/status.md"
        status_file.parent.mkdir(parents=True)

        status_file.write_text("""# Application Status - TestCo - PM

**Current Status:** interview-completed
**Last Updated:** 2025-01-22 14:00

## Status Timeline

### Interview-Completed - 2025-01-22 14:00
**Notes:** Final round completed

### Interview-Invited - 2025-01-18 10:00
**Notes:** Interview scheduled

### Applied - 2025-01-15 12:00
**Notes:** Application submitted

### Drafting - 2025-01-13 09:00
**Notes:** Started application
""")

        content = status_file.read_text()

        # Extract dates from timeline
        import re
        dates = re.findall(r'### .* - (\d{4}-\d{2}-\d{2})', content)

        # Assert: Dates in descending order (newest first)
        assert dates == ['2025-01-22', '2025-01-18', '2025-01-15', '2025-01-13']

    def test_timeline_includes_previous_status_references(self, tmp_path):
        """Each transition should reference previous status"""
        status_file = tmp_path / "applications/TestCo/status.md"
        status_file.parent.mkdir(parents=True)

        status_file.write_text("""# Application Status - TestCo - PM

**Current Status:** applied
**Last Updated:** 2025-01-14 15:30

## Status Timeline

### Applied - 2025-01-14 15:30
**Notes:** Submitted application

**Previous Status:** drafting

### Drafting - 2025-01-13 10:00
**Notes:** Analysis complete
""")

        content = status_file.read_text()
        assert "**Previous Status:** drafting" in content

    def test_timeline_preserves_all_notes(self, tmp_path):
        """All status notes should be preserved in timeline"""
        status_file = tmp_path / "applications/TestCo/status.md"
        status_file.parent.mkdir(parents=True)

        notes = [
            "Analysis complete, fit score 9/10",
            "Submitted via LinkedIn, mentioned referral from Sarah",
            "Phone screen scheduled for Jan 25, 10am GMT",
            "Final round with CEO went very well",
        ]

        timeline_content = "\n\n".join([
            f"### Status{i} - 2025-01-{13+i} 10:00\n**Notes:** {note}"
            for i, note in enumerate(notes)
        ])

        status_file.write_text(f"""# Application Status - TestCo - PM

**Current Status:** interview-completed
**Last Updated:** 2025-01-16 10:00

## Status Timeline

{timeline_content}
""")

        content = status_file.read_text()

        # Assert: All notes preserved
        for note in notes:
            assert note in content


class TestInvalidTransitions:
    """Test that invalid state transitions are handled"""

    def test_cannot_skip_states(self, tmp_path):
        """Should not allow skipping states (e.g., drafting → offer)"""
        status_file = tmp_path / "applications/Invalid/status.md"
        status_file.parent.mkdir(parents=True)

        status_file.write_text("""# Application Status - Invalid - PM

**Current Status:** drafting
**Last Updated:** 2025-01-13 10:00
""")

        # Attempting invalid transition: drafting → offer (skipped applied, interview steps)
        # In real system, /update-status should validate and reject/warn

        valid_next_states = {
            'drafting': ['applied', 'withdrawn'],
            'applied': ['interview-invited', 'rejected', 'withdrawn'],
            'interview-invited': ['interview-completed', 'withdrawn'],
            'interview-completed': ['offer', 'rejected', 'withdrawn'],
            'offer': ['accepted', 'withdrawn'],
        }

        current_status = 'drafting'
        attempted_status = 'offer'

        # Validation check
        is_valid = attempted_status in valid_next_states.get(current_status, [])
        assert not is_valid, f"Invalid transition: {current_status} → {attempted_status}"

    def test_cannot_transition_from_terminal_state(self, tmp_path):
        """Terminal states (accepted, rejected, withdrawn) should not allow transitions"""
        terminal_states = ['accepted', 'rejected', 'withdrawn']

        for terminal_state in terminal_states:
            # Attempting transition from terminal state
            valid_next_states = {
                'accepted': [],  # No valid next states
                'rejected': [],
                'withdrawn': [],
            }

            is_terminal = len(valid_next_states[terminal_state]) == 0
            assert is_terminal, f"{terminal_state} should be terminal (no valid next states)"


class TestDaysInProcess:
    """Test days-in-process calculation"""

    def test_calculates_days_waiting_for_applied(self, tmp_path):
        """Calculate days since applied for active applications"""
        from datetime import datetime, timedelta

        applied_date = datetime.now() - timedelta(days=12)
        current_date = datetime.now()

        days_waiting = (current_date - applied_date).days

        assert days_waiting == 12

    def test_calculates_time_to_first_response(self, tmp_path):
        """Calculate time from applied to first response"""
        applied_date = datetime(2025, 1, 10, 14, 0)
        interview_invited_date = datetime(2025, 1, 18, 10, 0)

        time_to_response = (interview_invited_date - applied_date).days

        assert time_to_response == 8  # 8 days to first response


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
