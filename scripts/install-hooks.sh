#!/bin/bash
# Install git hooks for CV application tracking system

echo "Installing git hooks..."
echo ""

# Change to repository root
cd "$(git rev-parse --show-toplevel)" || {
    echo "❌ Error: Not in a git repository"
    exit 1
}

# Create hooks directory if it doesn't exist
mkdir -p .git/hooks

# Copy pre-commit hook
if [ -f "scripts/pre-commit-hook.sh" ]; then
    cp scripts/pre-commit-hook.sh .git/hooks/pre-commit
    chmod +x .git/hooks/pre-commit
    echo "✅ Pre-commit hook installed: .git/hooks/pre-commit"
else
    echo "❌ Error: scripts/pre-commit-hook.sh not found"
    exit 1
fi

echo ""
echo "=========================================="
echo "Git hooks installed successfully!"
echo "=========================================="
echo ""
echo "What happens now:"
echo "  - Before each commit, the system will:"
echo "    1. Run health_check.py (exit code 1 blocks commit)"
echo "    2. Run pytest tests (failures block commit)"
echo "    3. Validate critical files exist"
echo ""
echo "To bypass hook (use sparingly):"
echo "  git commit --no-verify"
echo ""
echo "To uninstall:"
echo "  rm .git/hooks/pre-commit"
echo ""
