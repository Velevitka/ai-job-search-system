#!/usr/bin/env python3
"""
Migration script to reorganize applications folder into status-based hierarchy.
Moves application folders from flat structure to active/archive hierarchy based on status.

Special handling: Folders without status.md are placed in active/analyzing/
"""

import os
import re
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Define base path
BASE_PATH = Path(r"C:\Users\ArturSwadzba\OneDrive\4. CV")
APPLICATIONS_PATH = BASE_PATH / "applications"

# Status to folder mapping
STATUS_MAP = {
    'analyzing': 'active/analyzing',
    'analysis': 'active/analyzing',
    'analysis phase': 'active/analyzing',
    'analyzed': 'active/analyzing',
    'applied': 'active/applied',
    'submitted': 'active/applied',
    'interviewing': 'active/interviewing',
    'interview scheduled': 'active/interviewing',
    'interview invited': 'active/interviewing',
    'rejected': 'archive',  # Will add quarter subfolder
    'withdrawn': 'archive',  # Will add quarter subfolder
    'offer': 'archive',  # Rare but possible
}

def get_quarter_folder(date_str):
    """Determine quarter folder from date string YYYY-MM-DD"""
    try:
        year, month, _ = date_str.split('-')
        quarter = (int(month) - 1) // 3 + 1
        return f"{year}-Q{quarter}"
    except:
        # Default to current quarter
        now = datetime.now()
        quarter = (now.month - 1) // 3 + 1
        return f"{now.year}-Q{quarter}"

def parse_status_from_file(status_file):
    """Parse status and relevant dates from status.md file."""
    try:
        with open(status_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract current status
        status_match = re.search(r'\*\*Current Status:\*\* (.+?)$', content, re.MULTILINE)
        status = status_match.group(1).strip().lower() if status_match else 'analyzing'

        # Extract last updated date
        updated_match = re.search(r'\*\*Last Updated:\*\* (.+?)$', content, re.MULTILINE)
        last_updated = updated_match.group(1).strip() if updated_match else datetime.now().strftime("%Y-%m-%d")

        return {
            'status': status,
            'last_updated': last_updated,
            'has_status_file': True
        }
    except Exception as e:
        print(f"Error parsing {status_file}: {e}")
        return {
            'status': 'analyzing',
            'last_updated': datetime.now().strftime("%Y-%m-%d"),
            'has_status_file': False
        }

def determine_target_location(app_folder):
    """Determine target location for an application folder."""
    status_file = app_folder / "status.md"

    # Special case: No status.md → active/analyzing
    if not status_file.exists():
        return "applications/active/analyzing", "analyzing (no status.md)"

    # Parse status
    data = parse_status_from_file(status_file)
    status = data['status']

    # Map status to folder
    base_folder = STATUS_MAP.get(status, 'active/analyzing')

    # Handle archive with quarterly organization
    if base_folder == 'archive':
        quarter = get_quarter_folder(data['last_updated'])
        target = f"applications/archive/{quarter}/{status}"
        reason = f"{status} (archived to {quarter})"
    else:
        target = f"applications/{base_folder}"
        reason = status

    return target, reason

def create_folder_structure(dry_run=False):
    """Create the new folder hierarchy."""
    folders = [
        "applications/active/analyzing",
        "applications/active/applied",
        "applications/active/interviewing",
        "applications/archive/2025-Q4/rejected",
        "applications/archive/2025-Q4/withdrawn",
        "applications/archive/2025-Q4/accepted",
        "applications/archive/2025-Q3/rejected",
        "applications/archive/2025-Q3/withdrawn",
    ]

    for folder in folders:
        folder_path = BASE_PATH / folder
        if dry_run:
            print(f"[DRY-RUN] Would create: {folder}")
        else:
            folder_path.mkdir(parents=True, exist_ok=True)
            print(f"[OK] Created: {folder}")

def migrate_application(app_folder, dry_run=False):
    """Migrate a single application folder to new structure."""
    target_base, reason = determine_target_location(app_folder)
    target_path = BASE_PATH / target_base / app_folder.name

    if dry_run:
        return {
            'source': str(app_folder),
            'target': str(target_path),
            'reason': reason,
            'action': 'WOULD MOVE'
        }
    else:
        # Create target directory if needed
        target_path.parent.mkdir(parents=True, exist_ok=True)

        # Move folder
        shutil.move(str(app_folder), str(target_path))

        return {
            'source': str(app_folder),
            'target': str(target_path),
            'reason': reason,
            'action': 'MOVED'
        }

def validate_migration():
    """Validate migration was successful."""
    print("\n=== Validation ===")

    # Count folders in new structure
    active_folders = list(Path(BASE_PATH / "applications/active").glob("*/*"))
    archive_folders = list(Path(BASE_PATH / "applications/archive").glob("*/*/*"))

    print(f"Active folders: {len(active_folders)}")
    print(f"Archive folders: {len(archive_folders)}")
    print(f"Total in new structure: {len(active_folders) + len(archive_folders)}")

    # Check for any remaining folders in old structure
    old_structure_folders = []
    for item in (BASE_PATH / "applications").iterdir():
        if item.is_dir() and item.name not in ['active', 'archive', '_example-application']:
            old_structure_folders.append(item)

    if old_structure_folders:
        print(f"\n[!] WARNING: {len(old_structure_folders)} folders still in old structure:")
        for folder in old_structure_folders:
            print(f"  - {folder.name}")
    else:
        print("\n[OK] All folders migrated successfully!")

    return len(old_structure_folders) == 0

def main():
    """Main migration function."""
    parser = argparse.ArgumentParser(description='Migrate applications to status-based folder structure')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without executing')
    parser.add_argument('--execute', action='store_true', help='Execute migration')
    parser.add_argument('--validate', action='store_true', help='Validate migration results')
    args = parser.parse_args()

    if args.validate:
        success = validate_migration()
        return 0 if success else 1

    dry_run = not args.execute

    if dry_run:
        print("="*60)
        print("DRY RUN MODE - No changes will be made")
        print("="*60)
    else:
        print("="*60)
        print("EXECUTING MIGRATION")
        print("="*60)

    # Create new folder structure
    print("\n--- Creating folder structure ---")
    create_folder_structure(dry_run)

    # Find all application folders (excluding special folders)
    print("\n--- Scanning application folders ---")
    app_folders = []
    for item in APPLICATIONS_PATH.iterdir():
        if item.is_dir() and item.name not in ['active', 'archive', '_example-application']:
            app_folders.append(item)

    print(f"Found {len(app_folders)} folders to migrate")

    # Track migration results
    results = {
        'total': len(app_folders),
        'by_target': defaultdict(int),
        'no_status_md': 0,
        'migrations': []
    }

    # Migrate each folder
    print("\n--- Migrating folders ---")
    for app_folder in sorted(app_folders):
        result = migrate_application(app_folder, dry_run)
        results['migrations'].append(result)

        # Extract target category (use reason which has clean category)
        reason = result['reason']

        if 'no status.md' in reason:
            results['by_target']['active/analyzing'] += 1
            results['no_status_md'] += 1
        elif 'applied' in reason:
            results['by_target']['active/applied'] += 1
        elif 'interview' in reason:
            results['by_target']['active/interviewing'] += 1
        elif 'archived to' in reason:
            results['by_target']['archive'] += 1
        else:
            # analyzing, analyzed, analysis phase
            results['by_target']['active/analyzing'] += 1

        # Print progress
        action_prefix = "[DRY-RUN] " if dry_run else ""
        print(f"{action_prefix}{result['action']}: {app_folder.name} -> {result['reason']}")

    # Summary
    print("\n" + "="*60)
    print("MIGRATION SUMMARY")
    print("="*60)
    print(f"Total folders processed: {results['total']}")
    print(f"\nDestination breakdown:")
    for target, count in sorted(results['by_target'].items()):
        print(f"  {target}: {count}")
    print(f"\nFolders without status.md: {results['no_status_md']}")

    if dry_run:
        print("\n[!] This was a DRY RUN. No changes were made.")
        print("To execute migration, run: python scripts/migrate-to-status-folders.py --execute")
    else:
        print("\n[OK] Migration complete!")
        print("To validate results, run: python scripts/migrate-to-status-folders.py --validate")

    return 0

if __name__ == "__main__":
    exit(main())
