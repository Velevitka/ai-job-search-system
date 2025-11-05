# Test Suite

Automated tests for AI Job Application Management System.

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=scripts --cov-report=html

# Run specific test file
pytest tests/test_validation.py

# Run specific test class
pytest tests/test_validation.py::TestFileSizeCheck

# Run specific test
pytest tests/test_validation.py::TestFileSizeCheck::test_optimal_size_range

# Run with verbose output
pytest -v

# Run only unit tests (fast)
pytest -m unit

# Run only integration tests
pytest -m integration
```

## Test Structure

```
tests/
├── __init__.py              # Test package initialization
├── conftest.py              # Pytest configuration and fixtures
├── test_validation.py       # Validation script tests
└── fixtures/                # Test data files
```

## Fixtures

Defined in `conftest.py`:

- `validate_cv` - Provides validate-cv.py module with all validation functions
- `validate_cl` - Provides validate-cover-letter.py module
- `tmp_path` - Pytest built-in fixture for temporary directories

## Test Coverage Goals

**Priority 1 (Essential):**
- ✅ Validation scripts (file size, page count, paper size)
- ⏳ Fit score calculation logic
- ⏳ File operations (path handling, encoding)

**Priority 2 (Important):**
- ⏳ Bookmarklet data extraction
- ⏳ Markdown to PDF conversion validation
- ⏳ YAML front matter parsing

**Priority 3 (Nice to Have):**
- ⏳ Command workflow integration tests
- ⏳ End-to-end application generation
- ⏳ Performance benchmarks

## Writing Tests

### Example Test

```python
def test_my_feature(validate_cv, tmp_path):
    """Test that my feature works correctly"""
    # Setup
    test_file = tmp_path / "test.pdf"
    test_file.write_bytes(b"content")

    # Execute
    result = validate_cv.some_function(str(test_file))

    # Assert
    assert result == expected_value
```

### Test Markers

```python
@pytest.mark.unit
def test_fast_unit_test():
    """Fast unit test"""
    pass

@pytest.mark.integration
def test_slower_integration():
    """Slower integration test"""
    pass

@pytest.mark.requires_pdfinfo
def test_needs_pdfinfo():
    """Test that requires pdfinfo tool"""
    pass
```

## Current Status

- ✅ Test framework setup complete
- ✅ Validation script tests implemented
- ✅ Pytest fixtures configured
- ⏳ Additional test files needed (fit scoring, file ops, etc.)

Target coverage: 80%+ for validation scripts, 60%+ for utility scripts
