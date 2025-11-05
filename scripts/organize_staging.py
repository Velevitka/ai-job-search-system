#!/usr/bin/env python3
"""
Organize staging files into tier folders based on fit scores
"""

import shutil
from pathlib import Path
from bulk_analyze import analyze_all_jobs


def organize_by_tier(results, staging_dir='staging'):
    """Move files to tier folders based on fit scores"""
    staging_path = Path(staging_dir)

    # Ensure tier folders exist
    tier1 = staging_path / 'tier1-apply-now'
    tier2 = staging_path / 'tier2-research'
    tier3 = staging_path / 'tier3-maybe'
    archive = staging_path / 'archive'

    tier1.mkdir(exist_ok=True)
    tier2.mkdir(exist_ok=True)
    tier3.mkdir(exist_ok=True)
    archive.mkdir(exist_ok=True)

    moved_counts = {
        'tier1': 0,
        'tier2': 0,
        'tier3': 0,
        'archive': 0
    }

    for job in results:
        source = job['filepath']

        # Skip if file doesn't exist (might be in subfolder already)
        if not source.exists():
            continue

        # Determine destination based on fit score
        if job['fit_score'] >= 8.0:
            dest = tier1 / source.name
            moved_counts['tier1'] += 1
        elif job['fit_score'] >= 6.0:
            dest = tier2 / source.name
            moved_counts['tier2'] += 1
        elif job['fit_score'] >= 4.0:
            dest = tier3 / source.name
            moved_counts['tier3'] += 1
        else:
            dest = archive / source.name
            moved_counts['archive'] += 1

        # Move file
        try:
            shutil.move(str(source), str(dest))
            print(f"✅ Moved: {source.name[:60]} → {dest.parent.name}/ (Fit: {job['fit_score']}/10)")
        except Exception as e:
            print(f"⚠️ Error moving {source.name}: {e}")

    return moved_counts


def main():
    """Main execution"""
    print("📁 Organizing staging folder by fit score...")
    print()

    # Re-analyze to get fit scores
    results = analyze_all_jobs('staging')

    print()
    print("Moving files to tier folders...")
    print()

    counts = organize_by_tier(results)

    print()
    print("=" * 70)
    print("✅ ORGANIZATION COMPLETE")
    print("=" * 70)
    print()
    print(f"📁 tier1-apply-now/  → {counts['tier1']} files (Fit 8-10) 🔥")
    print(f"📁 tier2-research/   → {counts['tier2']} files (Fit 6-7) ⭐")
    print(f"📁 tier3-maybe/      → {counts['tier3']} files (Fit 4-5) ⚠️")
    print(f"📁 archive/          → {counts['archive']} files (Fit 1-3) ❌")
    print()
    print(f"Total files organized: {sum(counts.values())}")
    print()
    print("Next steps:")
    print("1. Focus on tier1-apply-now/ folder (24 high-priority roles)")
    print("2. Run /analyze-job for top 5 roles")
    print("3. Generate CVs and cover letters")
    print()


if __name__ == '__main__':
    main()
