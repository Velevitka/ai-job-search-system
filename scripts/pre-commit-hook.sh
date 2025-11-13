#!/bin/bash
# Pre-commit hook for CV application tracking system
# Runs health checks and tests before allowing commits
#
# Installation:
#   Copy this file to .git/hooks/pre-commit and make it executable
#   OR run: bash scripts/install-hooks.sh

echo "=========================================="
echo "Pre-Commit Hook: CV Application Tracker"
echo "=========================================="
echo ""

# Change to repository root
cd "$(git rev-parse --show-toplevel)" || exit 1

# Track overall status
all_passed=true

# ============================================
# 1. Run Health Check
# ============================================
echo "📊 Running system health check..."
echo ""

python scripts/health_check.py
health_exit=$?

if [ $health_exit -eq 0 ]; then
    echo "✅ Health check passed (Excellent: 85-100)"
    echo ""
elif [ $health_exit -eq 2 ]; then
    echo "⚠️  Health check passed (Fair: 70-84)"
    echo "   Consider fixing warnings before committing"
    echo ""
    # Allow commit but warn
elif [ $health_exit -eq 1 ]; then
    echo "❌ Health check failed (Poor: <70)"
    echo "   Critical issues detected. Fix before committing:"
    echo "   - Missing CVs for 'applied' status"
    echo "   - Invalid status values"
    echo "   - Broken application structure"
    echo ""
    all_passed=false
else
    echo "⚠️  Health check script error (exit code: $health_exit)"
    echo "   Continuing with commit, but investigate this"
    echo ""
fi

# ============================================
# 2. Run Tests (if pytest available)
# ============================================
if command -v pytest &> /dev/null; then
    echo "🧪 Running automated tests..."
    echo ""

    pytest tests/ --tb=short -v
    test_exit=$?

    if [ $test_exit -eq 0 ]; then
        echo ""
        echo "✅ All tests passed"
        echo ""
    else
        echo ""
        echo "❌ Tests failed"
        echo "   Fix failing tests before committing"
        echo ""
        all_passed=false
    fi
else
    echo "⚠️  pytest not found - skipping tests"
    echo "   Install: pip install pytest"
    echo ""
fi

# ============================================
# 3. Validate Critical Files
# ============================================
echo "📁 Validating critical files..."

critical_files=(
    "master/ArturSwadzba_MasterCV.pdf"
    "scripts/health_check.py"
)

for file in "${critical_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Missing critical file: $file"
        all_passed=false
    fi
done

if [ "$all_passed" = true ]; then
    echo "✅ Critical files present"
fi
echo ""

# ============================================
# Final Decision
# ============================================
if [ "$all_passed" = true ]; then
    echo "=========================================="
    echo "✅ All checks passed - proceeding with commit"
    echo "=========================================="
    exit 0
else
    echo "=========================================="
    echo "❌ Pre-commit checks failed"
    echo "=========================================="
    echo ""
    echo "To bypass this hook (NOT recommended):"
    echo "  git commit --no-verify"
    echo ""
    exit 1
fi
