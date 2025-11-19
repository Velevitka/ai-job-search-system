#!/usr/bin/env python3
"""
Verify that all application folders have required status.md files.

This script checks that:
1. Every application folder has a status.md file
2. Every application folder has job-description.md and analysis.md files
3. Reports any missing files

Usage:
    python scripts/verify-status-files.py
"""

import os
import sys
from pathlib import Path

def verify_status_files():
    """Verify all application folders have required status files."""

    applications_dir = Path("applications")

    if not applications_dir.exists():
        print("[ERROR] applications/ directory not found")
        return False

    # Get all application folders
    app_folders = [d for d in applications_dir.iterdir() if d.is_dir()]

    if not app_folders:
        print("[ERROR] No application folders found")
        return False

    print(f"\nChecking {len(app_folders)} application folders...\n")

    missing_files = []
    success_count = 0

    for folder in sorted(app_folders):
        folder_name = folder.name
        status_file = folder / "status.md"
        job_desc_file = folder / "job-description.md"
        analysis_file = folder / "analysis.md"

        # Check required files
        has_status = status_file.exists()
        has_job_desc = job_desc_file.exists()
        has_analysis = analysis_file.exists()

        if has_status and has_job_desc and has_analysis:
            print(f"[OK] {folder_name}")
            success_count += 1
        else:
            missing = []
            if not has_status:
                missing.append("status.md")
            if not has_job_desc:
                missing.append("job-description.md")
            if not has_analysis:
                missing.append("analysis.md")

            print(f"[FAIL] {folder_name}")
            print(f"   Missing: {', '.join(missing)}")
            missing_files.append((folder_name, missing))

    print(f"\n{'='*60}")
    print(f"SUMMARY:")
    print(f"  Total folders: {len(app_folders)}")
    print(f"  [OK] Complete: {success_count}")
    print(f"  [FAIL] Missing files: {len(missing_files)}")
    print(f"{'='*60}\n")

    if missing_files:
        print("WARNING: FOLDERS WITH MISSING FILES:\n")
        for folder_name, missing in missing_files:
            print(f"  • {folder_name}")
            for file in missing:
                print(f"    - {file}")
        print()
        return False
    else:
        print("SUCCESS: All application folders have required status files!\n")
        return True


def verify_new_applications():
    """Verify the 5 newly analyzed applications have status files."""

    new_apps = [
        "2025-11-TrustedHousesitters-DirectorProduct",
        "2025-11-SoundCloud-DirectorProductAds",
        "2025-11-Orbital-VPProduct",
        "2025-11-DeliveryHero-PrincipalPMBidding",
        "2025-11-Coinbase-DirectorProductGrowth"
    ]

    print("Verifying 5 newly analyzed applications from /analyze-jobs-parallel:\n")

    all_good = True
    for app_name in new_apps:
        app_path = Path("applications") / app_name
        status_file = app_path / "status.md"

        if status_file.exists():
            print(f"[OK] {app_name}/status.md")
        else:
            print(f"[FAIL] {app_name}/status.md MISSING")
            all_good = False

    print()

    if all_good:
        print("SUCCESS: All 5 newly analyzed applications have status.md files!\n")
    else:
        print("WARNING: Some newly analyzed applications are missing status.md files!\n")

    return all_good


if __name__ == "__main__":
    print("\n" + "="*60)
    print("STATUS FILE VERIFICATION")
    print("="*60 + "\n")

    # First verify new applications
    new_apps_ok = verify_new_applications()

    print("-"*60 + "\n")

    # Then verify all applications
    all_apps_ok = verify_status_files()

    # Exit with error code if any checks failed
    if not (new_apps_ok and all_apps_ok):
        sys.exit(1)

    sys.exit(0)
