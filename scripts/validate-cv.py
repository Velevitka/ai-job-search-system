#!/usr/bin/env python3
"""
CV PDF Validation Script
Usage: python scripts/validate-cv.py path/to/CV.pdf path/to/CV.md
"""

import sys
import subprocess
import os

def validate_cv(pdf_path, md_path=None):
    results = {
        'passed': [],
        'warnings': [],
        'failed': []
    }

    # Check 1: File exists
    if not os.path.exists(pdf_path):
        results['failed'].append(f"PDF not found: {pdf_path}")
        return results

    results['passed'].append(f"✅ File exists: {os.path.basename(pdf_path)}")

    # Check 2: Page count
    try:
        output = subprocess.check_output(['pdfinfo', pdf_path], text=True, stderr=subprocess.DEVNULL)
        for line in output.split('\n'):
            if 'Pages:' in line:
                pages = int(line.split(':')[1].strip())
                if pages <= 2:
                    results['passed'].append(f"✅ Page count: {pages} page(s) (target: ≤2)")
                else:
                    results['failed'].append(f"❌ Page count: {pages} pages (MUST be ≤2)")
                break
    except Exception as e:
        results['warnings'].append(f"⚠️  Could not check page count: {e}")

    # Check 3: File size
    try:
        size_bytes = os.path.getsize(pdf_path)
        size_kb = size_bytes / 1024
        if 40 <= size_kb <= 100:
            results['passed'].append(f"✅ File size: {size_kb:.0f}KB (optimal: 40-100KB)")
        elif 20 <= size_kb < 40:
            results['warnings'].append(f"⚠️  File size: {size_kb:.0f}KB (smaller than typical, but OK)")
        elif 100 < size_kb <= 150:
            results['warnings'].append(f"⚠️  File size: {size_kb:.0f}KB (larger than typical, but OK)")
        else:
            results['failed'].append(f"❌ File size: {size_kb:.0f}KB (expected: 40-100KB)")
    except Exception as e:
        results['failed'].append(f"❌ Could not check file size: {e}")

    # Check 4: Paper size
    try:
        output = subprocess.check_output(['pdfinfo', pdf_path], text=True, stderr=subprocess.DEVNULL)
        for line in output.split('\n'):
            if 'Page size:' in line:
                if '595' in line and '841' in line:  # A4 dimensions
                    results['passed'].append(f"✅ Paper size: A4 (595 x 842 pts)")
                else:
                    results['failed'].append(f"❌ Paper size: {line.split(':')[1].strip()} (expected: A4)")
                break
    except Exception as e:
        results['warnings'].append(f"⚠️  Could not check paper size: {e}")

    # Check 5: Word count (if markdown provided)
    if md_path and os.path.exists(md_path):
        try:
            with open(md_path, 'r', encoding='utf-8') as f:
                content = f.read()

                # Remove YAML front matter
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        content = parts[2]

                words = len(content.split())

                if words < 1400:
                    results['passed'].append(f"✅ Word count: {words} words (fits comfortably in 2 pages)")
                elif 1400 <= words < 1600:
                    results['warnings'].append(f"⚠️  Word count: {words} words (borderline, may need 18mm margins)")
                else:
                    results['warnings'].append(f"⚠️  Word count: {words} words (likely >2 pages, needs compression)")
        except Exception as e:
            results['warnings'].append(f"⚠️  Could not check word count: {e}")
    elif md_path:
        results['warnings'].append(f"⚠️  Markdown file not found: {md_path}")

    # Check 6: Eisvogel template indicators (heuristic)
    try:
        # Check if file size is in typical Eisvogel range
        size_kb = os.path.getsize(pdf_path) / 1024
        if 40 <= size_kb <= 100:
            results['passed'].append(f"✅ Generated with XeLaTeX (Eisvogel indicator)")
        else:
            results['warnings'].append(f"⚠️  File size suggests non-Eisvogel template")
    except:
        pass

    return results


def print_results(results):
    print("\n" + "="*70)
    print("CV PDF VALIDATION RESULTS")
    print("="*70)

    if results['passed']:
        print("\n✅ PASSED:")
        for item in results['passed']:
            print(f"   {item}")

    if results['warnings']:
        print("\n⚠️  WARNINGS:")
        for item in results['warnings']:
            print(f"   {item}")

    if results['failed']:
        print("\n❌ FAILED:")
        for item in results['failed']:
            print(f"   {item}")

    # Overall status
    print("\n" + "="*70)
    if results['failed']:
        print("❌ OVERALL: VALIDATION FAILED")
        print("\n🔧 RECOMMENDED FIXES:")

        # Check if page count failed
        page_fail = any('Page count' in item for item in results['failed'])
        if page_fail:
            print("\n   Pages > 2:")
            print("   1. Try YAML: geometry: margin=18mm, fontsize: 10pt")
            print("   2. If still >2 pages, use: geometry: margin=18mm, fontsize: 10pt, linestretch: 0.95")
            print("   3. Last resort: Remove least relevant content")

        # Check if file size failed
        size_fail = any('File size' in item for item in results['failed'])
        if size_fail:
            print("\n   File size wrong:")
            print("   1. Verify pandoc command includes: --template eisvogel")
            print("   2. Check YAML doesn't override Eisvogel settings")

        # Check if paper size failed
        paper_fail = any('Paper size' in item for item in results['failed'])
        if paper_fail:
            print("\n   Paper size wrong:")
            print("   1. Add to YAML: papersize: a4")
            print("   2. Ensure: --template eisvogel in pandoc command")

        print("\n" + "="*70)
        return 1
    elif results['warnings']:
        print("⚠️  OVERALL: PASSED WITH WARNINGS")
        print("   Review warnings above, but CV is usable.")
        print("="*70)
        return 0
    else:
        print("✅ OVERALL: PERFECT - All checks passed!")
        print("   CV is ready for submission.")
        print("="*70)
        return 0


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/validate-cv.py <pdf_path> [md_path]")
        print("\nExample:")
        print('  python scripts/validate-cv.py "applications/2025-11-Company-Role/CV.pdf" "applications/2025-11-Company-Role/CV.md"')
        sys.exit(1)

    pdf_path = sys.argv[1]
    md_path = sys.argv[2] if len(sys.argv) > 2 else None

    results = validate_cv(pdf_path, md_path)
    exit_code = print_results(results)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
