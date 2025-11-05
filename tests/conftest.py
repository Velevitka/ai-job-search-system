"""
Pytest configuration and shared fixtures

This file provides:
- Import helpers for scripts with hyphens in filenames
- Shared test fixtures
- Test data setup
"""

import sys
import importlib.util
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def import_module_from_file(module_name, file_path):
    """
    Import a module from a file path, works with hyphens in filename

    Note: Delayed import to avoid conflicts with pytest output capturing
    """
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)

    # Temporarily disable stdout redirection during import
    original_stdout = sys.stdout
    original_stderr = sys.stderr

    try:
        spec.loader.exec_module(module)
    finally:
        # Restore original streams if they were changed
        sys.stdout = original_stdout
        sys.stderr = original_stderr

    return module


# Lazy import function for tests to use
def get_validate_cv():
    """Lazily import validate-cv module"""
    if 'validate_cv' not in sys.modules:
        validate_cv_path = project_root / "scripts" / "validation" / "validate-cv.py"
        module = import_module_from_file("validate_cv", validate_cv_path)
        sys.modules['validate_cv'] = module
        sys.modules['scripts.validation.validate_cv'] = module
    return sys.modules['validate_cv']


def get_validate_cl():
    """Lazily import validate-cover-letter module"""
    if 'validate_cover_letter' not in sys.modules:
        validate_cl_path = project_root / "scripts" / "validation" / "validate-cover-letter.py"
        module = import_module_from_file("validate_cover_letter", validate_cl_path)
        sys.modules['validate_cover_letter'] = module
        sys.modules['scripts.validation.validate_cover_letter'] = module
    return sys.modules['validate_cover_letter']


# Pytest fixtures
import pytest

@pytest.fixture
def validate_cv():
    """Fixture providing validate_cv module"""
    return get_validate_cv()


@pytest.fixture
def validate_cl():
    """Fixture providing validate_cover_letter module"""
    return get_validate_cl()
