# Testing & Evaluation Framework

Comprehensive testing infrastructure for the job application tracking system, ensuring workflow consistency, data integrity, and fit scoring accuracy.

---

## Quick Start

### Run All Tests
```bash
# Run entire test suite
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=. --cov-report=term-missing

# Run specific test file
pytest tests/test_file_movement.py -v
```

### Run Health Checks
```bash
# System health check (daily or before major activities)
python scripts/health_check.py

# Application quality audit (before submissions)
python scripts/audit_application_quality.py

# Fit score accuracy evaluation (monthly or after 10+ completed apps)
python scripts/evaluate_fit_accuracy.py
```

---

## Test Files Overview

### `test_file_movement.py`
**Purpose:** Validate file movement operations through the staging pipeline

**Test Coverage:**
- ✅ `/analyze-job` file movement (shortlist → applying)
- ✅ `/update-status` archiving (applying → archive/[rejected|withdrawn|accepted])
- ✅ Edge cases (special characters, missing files, duplicates)
- ✅ Bulk processing (discovery → shortlist tiers)
- ✅ Orphaned file detection

**Key Test Cases:**
```python
test_moves_mhtml_from_shortlist_high_to_applying()
test_archives_to_rejected_on_rejected_status()
test_archives_to_withdrawn_on_withdrawn_status()
test_detect_orphaned_files_no_application_folder()
```

**Run:**
```bash
pytest tests/test_file_movement.py -v
```

---

### `test_state_transitions.py`
**Purpose:** Validate state machine transitions and timeline integrity

**Test Coverage:**
- ✅ Valid state transitions (drafting → applied → interview-invited → offer → accepted)
- ✅ Terminal states (accepted, rejected, withdrawn)
- ✅ Invalid transition blocking
- ✅ Concurrent applications to same company
- ✅ Timeline chronological ordering
- ✅ Status history preservation

**Valid State Machine:**
```
drafting → applied → interview-invited → interview-completed → offer → accepted
    ↓          ↓              ↓                    ↓              ↓
withdrawn   rejected      withdrawn           rejected       withdrawn

Terminal states: accepted, rejected, withdrawn (no further transitions)
```

**Key Test Cases:**
```python
test_lifecycle_drafting_to_applied()
test_lifecycle_applied_to_interview_invited()
test_lifecycle_interview_to_offer_to_accepted()
test_cannot_skip_states()  # e.g., drafting → offer is invalid
test_cannot_transition_from_terminal_state()
```

**Run:**
```bash
pytest tests/test_state_transitions.py -v
```

---

### `test_sync_integrity.py`
**Purpose:** Validate `/sync-all` regeneration accuracy

**Test Coverage:**
- ✅ Count accuracy (active, rejected, withdrawn counts match source files)
- ✅ Calculation accuracy (fit score averages, percentages)
- ✅ Data consistency (orphaned files, status/location mismatches)
- ✅ Error handling (missing files, corrupted data)
- ✅ Manual edit preservation in STATUS.md

**Key Test Cases:**
```python
test_active_count_matches_applied_status_files()
test_rejected_count_matches_status_files()
test_average_fit_score_calculated_correctly()
test_detects_orphaned_files()
test_preserves_manual_edits_in_status_md()
```

**Run:**
```bash
pytest tests/test_sync_integrity.py -v
```

---

### `test_validation.py` (Legacy)
**Purpose:** Validate CV/CL PDF format requirements

**Test Coverage:**
- ✅ File size validation (60-80KB for CV)
- ✅ Page count validation (≤2 for CV, =1 for CL)
- ✅ Paper size validation (A4: 595x842 pts)

**Run:**
```bash
pytest tests/test_validation.py -v
```

---

## Evaluation Scripts

### `scripts/health_check.py`
**Purpose:** Comprehensive system health monitoring

**Checks Performed:**
1. **Orphaned Files:** Job files without corresponding application folders
2. **Status Consistency:** Status matches file location (e.g., withdrawn status → file in archive/withdrawn/)
3. **Missing CVs:** Applications with status='applied' but no CV PDF
4. **Stale Applications:** Drafting status for >7 days
5. **Archive Integrity:** Proper archive folder structure
6. **Pipeline Structure:** All expected staging folders exist
7. **Duplicate Applications:** Multiple applications to same company
8. **Missing Files:** Required files (job-description.md, analysis.md, status.md)
9. **Long Wait Times:** Applied applications waiting >14 days

**Output:** `insights/health-check-YYYY-MM-DD.md`

**Health Score:**
- 100 (Excellent): No issues, no warnings
- 85 (Good): 0 issues, ≤3 warnings
- 70 (Fair): ≤2 issues, ≤5 warnings
- 50 (Poor): >2 issues or >5 warnings

**Run:**
```bash
python scripts/health_check.py
```

**Schedule:**
- Daily: Before starting work session
- Before bulk submissions
- After bulk `/analyze-job` runs
- Weekly maintenance (Sunday evening)
- When suspecting data inconsistency

**Example Output:**
```
🏥 System Health Check
==================================================

  Checking for orphaned job files...
  Checking status/location consistency...
  Checking for missing CVs...
  ...

✅ Health checks complete

📊 Health Score: 85/100 (Good)
  Critical Issues: 0
  Warnings: 2

📄 Report saved to: insights/health-check-2025-01-13.md
```

---

### `scripts/audit_application_quality.py`
**Purpose:** Audit CV and cover letter quality across all applications

**Checks Performed:**
1. **CV Format Validation:**
   - Page count: ≤2 pages (strict requirement)
   - File size: 60-80KB (ideal for Eisvogel template)
   - Paper size: A4 (595 x 842 pts)
   - Keyword integration from analysis.md

2. **Cover Letter Validation:**
   - Page count: Exactly 1 page (strict requirement)
   - File size: <30KB
   - Company-specific research included

3. **Application Completeness:**
   - job-description.md exists
   - analysis.md exists
   - status.md exists
   - CV PDF exists if status='applied'

**Output:** `insights/application-quality-audit-YYYY-MM-DD.md`

**Run:**
```bash
python scripts/audit_application_quality.py
```

**Schedule:**
- Before bulk submission
- Monthly quality review
- After template changes

**Example Output:**
```
🔍 Application Quality Audit
==================================================

  Checking 2025-01-AmericanExpress-DirectorDigitalTrackerRemediation...
  Checking 2025-01-LeonardoAi-HeadOfProductAI...
  ...

✅ Audit complete: 15 applications checked

📊 Results:
  Critical Issues: 1
  Warnings: 3
  Successes: 8

📄 Report saved to: insights/application-quality-audit-2025-01-13.md
```

---

### `scripts/evaluate_fit_accuracy.py`
**Purpose:** Correlate fit scores with actual outcomes to validate scoring algorithm

**Metrics Calculated:**
1. **High-Fit (8.5-10) Success Rate:** Target >60%
2. **Medium-Fit (7-8.5) Success Rate:** Target >40%
3. **False Positive Rate:** High-fit applications that get rejected (Target <20%)
4. **Time to Response:** Average days from applied to response by fit tier

**Output:** `insights/fit-score-evaluation-YYYY-MM-DD.md`

**Run:**
```bash
python scripts/evaluate_fit_accuracy.py
```

**Schedule:**
- Monthly
- After every 10 completed applications
- Before recalibrating fit scoring criteria

**Example Output:**
```
🔍 Evaluating Fit Score Accuracy...

📊 Metrics Summary:
  High-Fit Success Rate: 65.0% (Target: >60%)
  Medium-Fit Success Rate: 42.0% (Target: >40%)
  False Positive Rate: 15.0% (Target: <20%)

📄 Full report: insights/fit-score-evaluation-2025-01-13.md

💡 Key Recommendations:
  1. ✅ All fit score targets met! Scoring algorithm appears well-calibrated.
```

**Recommendations Generated:**
- Recalibration suggestions if targets not met
- Rejection pattern analysis for high-fit false positives
- Threshold adjustment recommendations

---

## Testing Philosophy

### Anti-Hallucination Gates
- Tests validate that `/analyze-job` doesn't auto-generate CVs without human review
- Ensures analysis.md content comes from actual job description, not hallucinated
- Validates fit scores are calculated based on real keyword matching

### Source of Truth Pattern
- `applications/*/status.md` files are authoritative
- `STATUS.md` and `metrics-dashboard.md` are derived views (auto-generated)
- Tests ensure derived views accurately reflect source data

### Workflow Atomicity
- Multi-step operations (update status + move file + sync) must complete fully
- Health checks detect partial completion (e.g., status changed but file not moved)
- Tests validate pre/post-conditions for each command

### State Machine Integrity
- Valid transitions enforced
- Terminal states cannot be exited
- Timeline maintains chronological order
- Previous status references preserved

---

## Coverage Goals

### Current Coverage
- **File Movement:** 6 test classes, 20+ test cases
- **State Transitions:** 5 test classes, 15+ test cases
- **Sync Integrity:** 4 test classes, 12+ test cases
- **System Health:** 9 check functions
- **Quality Audit:** 5 validation categories
- **Fit Evaluation:** 4 metric calculations

### Target Coverage
- ✅ All critical workflows tested (file movement, status updates, archiving)
- ✅ Edge cases covered (special characters, missing files, duplicates)
- ✅ Data integrity validated (counts, calculations, consistency)
- ⏳ Integration tests (end-to-end workflows) - Future work
- ⏳ Performance tests (bulk operations) - Future work

---

## Running Tests in CI/CD

### Pre-Commit Hook (Recommended)
```bash
# .git/hooks/pre-commit
#!/bin/bash
pytest tests/ --tb=short
if [ $? -ne 0 ]; then
    echo "❌ Tests failed. Commit aborted."
    exit 1
fi
```

### GitHub Actions (Future)
```yaml
# .github/workflows/test.yml
name: Test Suite
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install pytest
      - run: pytest tests/ -v
```

---

## Troubleshooting

### Test Failures

**Symptom:** `test_moves_mhtml_from_shortlist_high_to_applying` fails
- **Cause:** File not moved during `/analyze-job`
- **Fix:** Check if file movement step executed in slash command
- **Prevention:** Add file movement validation to `/analyze-job`

**Symptom:** `test_active_count_matches_applied_status_files` fails
- **Cause:** STATUS.md out of sync with source files
- **Fix:** Run `/sync-all` to regenerate derived views
- **Prevention:** Add pre-commit hook to run `/sync-all`

**Symptom:** `test_cannot_skip_states` fails
- **Cause:** `/update-status` allowed invalid transition
- **Fix:** Add state validation to `/update-status` command
- **Prevention:** Enforce state machine rules in command definition

### Health Check Issues

**Critical Issue:** "Status is 'rejected' but job file still in staging/3-applying/"
- **Fix:** Run `/update-status [company] rejected "[reason]"` again to trigger archiving
- **Or:** Manually move file: `mv staging/3-applying/[file].mhtml staging/archive/rejected/`

**Warning:** "CV file size 95KB outside ideal range (60-80KB)"
- **Fix:** Review CV content, remove unnecessary sections
- **Or:** Adjust Eisvogel template margins/spacing

**Warning:** "Keywords not found in CV: Python, Kubernetes, CI/CD"
- **Fix:** Edit `ArturSwadzba_CV_[Company].md` to integrate missing keywords
- **Then:** Regenerate PDF with `/generate-cv [Company]`

---

## Maintenance Schedule

### Daily
- Run `python scripts/health_check.py` before starting work

### Weekly
- Review health check report trends
- Address stale applications (>7 days in drafting)
- Follow up on long-wait applications (>14 days applied)

### Monthly
- Run `python scripts/evaluate_fit_accuracy.py`
- Run `python scripts/audit_application_quality.py`
- Review test coverage and add new tests for gaps

### Before Major Activities
- **Before Bulk Submissions:** Health check + quality audit
- **Before Template Changes:** Full test suite + quality audit
- **After Bulk `/analyze-job`:** Health check to detect orphaned files
- **Before Recalibrating Fit Scoring:** Fit accuracy evaluation

---

## Adding New Tests

### Example: Testing New Command
```python
# tests/test_new_command.py
import pytest
from pathlib import Path

class TestNewCommand:
    """Test /new-command functionality"""

    def test_command_creates_expected_files(self, tmp_path):
        """Verify new command creates required files"""
        output_path = tmp_path / "expected_output.md"

        # Simulate command execution
        # (Replace with actual command logic)
        output_path.write_text("Expected content")

        # Assert
        assert output_path.exists()
        assert "Expected content" in output_path.read_text()

    def test_command_handles_missing_input(self, tmp_path):
        """Verify error handling for missing inputs"""
        # Test implementation
        pass
```

### Running New Test
```bash
pytest tests/test_new_command.py -v
```

---

## Integration with Slash Commands

### Commands with Test Coverage
- `/analyze-job` → `test_file_movement.py`
- `/update-status` → `test_state_transitions.py`, `test_file_movement.py`
- `/sync-all` → `test_sync_integrity.py`
- `/generate-cv` → `audit_application_quality.py`

### Commands Needing Test Coverage (Future Work)
- `/generate-cl` → Quality validation tests
- `/review-analysis` → Content accuracy tests
- `/summarize-week` → Aggregation accuracy tests

---

## Test Structure

```
tests/
├── __init__.py                    # Test package initialization
├── conftest.py                    # Pytest configuration and fixtures
├── README.md                      # This file
├── test_validation.py             # CV/CL format validation (legacy)
├── test_file_movement.py          # Pipeline file movement validation
├── test_state_transitions.py     # State machine and timeline tests
├── test_sync_integrity.py         # Sync algorithm accuracy tests
└── fixtures/                      # Test data files
```

---

## Best Practices

1. **Run Health Check Daily:** Catch issues early before they compound
2. **Quality Audit Before Submissions:** Ensure CVs/CLs meet format requirements
3. **Evaluate Fit Scores Regularly:** Recalibrate algorithm based on outcomes
4. **Fix Critical Issues Immediately:** Don't let health score drop below 70
5. **Document Test Failures:** Add regression tests when bugs are found
6. **Keep Tests Fast:** Use `tmp_path` fixtures, avoid external dependencies

---

## Resources

- **Pytest Documentation:** https://docs.pytest.org/
- **Testing Best Practices:** https://docs.pytest.org/en/stable/goodpractices.html
- **Coverage.py:** https://coverage.readthedocs.io/

---

**Last Updated:** 2025-01-13
**Test Framework Version:** 1.0
**Maintainer:** Artur Swadzba
