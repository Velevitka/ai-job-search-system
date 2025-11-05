"""
Tests for validation scripts

Tests CV and cover letter validation logic to ensure:
- Page count validation works correctly
- File size checks are accurate
- Paper size validation catches formatting issues
- YAML validation detects problematic patterns
"""

import pytest
from pathlib import Path


class TestFileExistenceCheck:
    """Test file existence validation"""

    def test_file_exists(self, validate_cv, tmp_path):
        """Test that existing file passes validation"""
        # Use fixture

        # Create temporary PDF file
        test_pdf = tmp_path / "test_cv.pdf"
        test_pdf.write_text("dummy pdf content")

        passed, passes, fails, warns = validate_cv.check_file_existence(str(test_pdf))

        assert passed is True
        assert passes == 1
        assert fails == 0
        assert warns == 0

    def test_file_not_exists(self, validate_cv, tmp_path):
        """Test that missing file fails validation"""
        # Use fixture
        missing_pdf = tmp_path / "nonexistent.pdf"

        passed, passes, fails, warns = validate_cv.check_file_existence(str(missing_pdf))

        assert passed is False
        assert passes == 0
        assert fails == 1
        assert warns == 0


class TestFileSizeCheck:
    """Test file size validation"""

    def test_optimal_size_range(self, tmp_path):
        """Test file in optimal size range (60-80KB) passes"""
        # Use fixture
        test_pdf = tmp_path / "optimal_cv.pdf"
        # Create file ~70KB
        test_pdf.write_bytes(b"x" * (70 * 1024))

        passes, fails, warns = validate_cv.check_file_size(str(test_pdf))

        assert passes == 1
        assert fails == 0
        assert warns == 0

    def test_too_small_file(self, tmp_path):
        """Test file below minimum (40KB) fails"""
        # Use fixture
        test_pdf = tmp_path / "small_cv.pdf"
        # Create file ~30KB
        test_pdf.write_bytes(b"x" * (30 * 1024))

        passes, fails, warns = validate_cv.check_file_size(str(test_pdf))

        assert passes == 0
        assert fails == 1
        assert warns == 0

    def test_acceptable_size_range(self, tmp_path):
        """Test file in acceptable range (40-100KB) passes"""
        # Use fixture
        test_pdf = tmp_path / "acceptable_cv.pdf"
        # Create file ~90KB (outside optimal but acceptable)
        test_pdf.write_bytes(b"x" * (90 * 1024))

        passes, fails, warns = validate_cv.check_file_size(str(test_pdf))

        assert passes == 1
        assert fails == 0
        assert warns == 0

    def test_too_large_file(self, tmp_path):
        """Test file above maximum (100KB) warns"""
        # Use fixture
        test_pdf = tmp_path / "large_cv.pdf"
        # Create file ~120KB
        test_pdf.write_bytes(b"x" * (120 * 1024))

        passes, fails, warns = validate_cv.check_file_size(str(test_pdf))

        assert passes == 0
        assert fails == 0
        assert warns == 1


class TestPageCountCheck:
    """Test page count validation"""

    def test_perfect_page_count(self):
        """Test 2-page PDF passes validation"""
        # Use fixture
        mock_pdf_info = "Pages:          2\nOther: data"

        passes, fails, warns = validate_cv.check_page_count(mock_pdf_info)

        assert passes == 1
        assert fails == 0
        assert warns == 0

    def test_too_many_pages(self):
        """Test PDF with >2 pages fails validation"""
        # Use fixture
        mock_pdf_info = "Pages:          3\nOther: data"

        passes, fails, warns = validate_cv.check_page_count(mock_pdf_info)

        assert passes == 0
        assert fails == 1
        assert warns == 0

    def test_one_page_acceptable(self):
        """Test 1-page PDF passes (acceptable for some use cases)"""
        # Use fixture
        mock_pdf_info = "Pages:          1\nOther: data"

        passes, fails, warns = validate_cv.check_page_count(mock_pdf_info)

        assert passes == 1
        assert fails == 0
        assert warns == 0

    def test_no_pdf_info(self):
        """Test gracefully handles missing pdfinfo"""
        # Use fixture
        passes, fails, warns = validate_cv.check_page_count(None)

        assert passes == 0
        assert fails == 0
        assert warns == 1

    def test_malformed_pdf_info(self):
        """Test handles pdfinfo without page count"""
        # Use fixture
        mock_pdf_info = "Title: Some PDF\nAuthor: Someone"

        passes, fails, warns = validate_cv.check_page_count(mock_pdf_info)

        assert passes == 0
        assert fails == 0
        assert warns == 1


class TestPaperSizeCheck:
    """Test paper size validation (A4 = 595 x 842 pts)"""

    def test_correct_a4_size(self):
        """Test exact A4 dimensions pass"""
        # Use fixture
        mock_pdf_info = "Page size:      595 x 842 pts"

        passes, fails, warns = validate_cv.check_paper_size(mock_pdf_info)

        assert passes == 1
        assert fails == 0
        assert warns == 0

    def test_a4_with_tolerance(self):
        """Test A4 within tolerance (±5 pts) passes"""
        # Use fixture
        mock_pdf_info = "Page size:      597 x 840 pts"

        passes, fails, warns = validate_cv.check_paper_size(mock_pdf_info)

        assert passes == 1
        assert fails == 0
        assert warns == 0

    def test_wrong_paper_size(self):
        """Test non-A4 size fails"""
        # Use fixture
        # US Letter size
        mock_pdf_info = "Page size:      612 x 792 pts"

        passes, fails, warns = validate_cv.check_paper_size(mock_pdf_info)

        assert passes == 0
        assert fails == 1
        assert warns == 0

    def test_no_pdf_info(self):
        """Test gracefully handles missing pdfinfo"""
        # Use fixture
        passes, fails, warns = validate_cv.check_paper_size(None)

        assert passes == 0
        assert fails == 0
        assert warns == 1


class TestIntegrationScenarios:
    """Integration tests for common validation scenarios"""

    def test_perfect_cv_scenario(self, tmp_path):
        """Test a perfect CV passes all checks"""
        # Use fixture

        # Create CV with optimal size (70KB)
        test_pdf = tmp_path / "perfect_cv.pdf"
        test_pdf.write_bytes(b"x" * (70 * 1024))

        # File existence check
        passed, passes, fails, warns = validate_cv.check_file_existence(str(test_pdf))
        assert passed is True

        # File size check
        passes, fails, warns = validate_cv.check_file_size(str(test_pdf))
        assert passes == 1
        assert fails == 0

        # Page count check (mocked)
        mock_pdf_info = "Pages:          2\nPage size:      595 x 842 pts"
        passes, fails, warns = validate_cv.check_page_count(mock_pdf_info)
        assert passes == 1
        assert fails == 0

        # Paper size check
        passes, fails, warns = validate_cv.check_paper_size(mock_pdf_info)
        assert passes == 1
        assert fails == 0

    def test_broken_formatting_scenario(self):
        """Test CV with broken formatting is caught"""
        # Use fixture

        # 4-page CV on US Letter paper
        mock_pdf_info = "Pages:          4\nPage size:      612 x 792 pts"

        # Page count should fail
        passes, fails, warns = validate_cv.check_page_count(mock_pdf_info)
        assert fails == 1

        # Paper size should fail
        passes, fails, warns = validate_cv.check_paper_size(mock_pdf_info)
        assert fails == 1


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "requires_pdfinfo: mark test as requiring pdfinfo tool"
    )
