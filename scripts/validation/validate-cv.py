#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CV Format Validation Script
Validates CV PDF formatting against master CV standards
Usage: python validate-cv.py <path-to-cv.pdf> [<path-to-markdown.md>]
"""

import sys
import os
import subprocess
import re
from pathlib import Path

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Configuration
MAX_PAGES = 2
MIN_FILE_SIZE_KB = 40
MAX_FILE_SIZE_KB = 100
TARGET_MIN_SIZE_KB = 60
TARGET_MAX_SIZE_KB = 80
EXPECTED_WIDTH = 595
EXPECTED_HEIGHT = 842

# ANSI color codes
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

def print_header():
    print(f"{Colors.BLUE}========================================{Colors.NC}")
    print(f"{Colors.BLUE}   CV FORMAT VALIDATION TOOL{Colors.NC}")
    print(f"{Colors.BLUE}========================================{Colors.NC}")
    print()

def print_pass(msg):
    print(f"{Colors.GREEN}✅ PASS:{Colors.NC} {msg}")

def print_fail(msg):
    print(f"{Colors.RED}❌ FAIL:{Colors.NC} {msg}")

def print_warn(msg):
    print(f"{Colors.YELLOW}⚠️  WARN:{Colors.NC} {msg}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ️  INFO:{Colors.NC} {msg}")

def print_skip(msg):
    print(f"{Colors.YELLOW}⚠️  SKIP:{Colors.NC} {msg}")

def get_pdf_info(pdf_path):
    """Get PDF metadata using pdfinfo"""
    try:
        result = subprocess.run(['pdfinfo', pdf_path],
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return result.stdout
        return None
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None

def check_file_existence(pdf_path):
    """Check 1: File existence"""
    print(f"{Colors.BLUE}[1/7]{Colors.NC} Checking file existence...")

    if os.path.exists(pdf_path):
        print_pass("PDF file exists")
        print()
        return True, 1, 0, 0
    else:
        print_fail("PDF file not found")
        print()
        return False, 0, 1, 0

def check_file_size(pdf_path):
    """Check 2: File size"""
    print(f"{Colors.BLUE}[2/7]{Colors.NC} Checking file size...")

    file_size_bytes = os.path.getsize(pdf_path)
    file_size_kb = file_size_bytes // 1024

    print(f"   File size: {file_size_kb}KB")

    if file_size_kb < MIN_FILE_SIZE_KB:
        print_fail(f"File too small ({file_size_kb}KB < {MIN_FILE_SIZE_KB}KB)")
        print("   This suggests wrong template was used (not Eisvogel)")
        print()
        return 0, 1, 0
    elif file_size_kb > MAX_FILE_SIZE_KB:
        print_warn(f"File larger than expected ({file_size_kb}KB > {MAX_FILE_SIZE_KB}KB)")
        print("   This might indicate embedded fonts or images")
        print()
        return 0, 0, 1
    elif TARGET_MIN_SIZE_KB <= file_size_kb <= TARGET_MAX_SIZE_KB:
        print_pass(f"File size in optimal range ({TARGET_MIN_SIZE_KB}-{TARGET_MAX_SIZE_KB}KB)")
        print()
        return 1, 0, 0
    else:
        print_pass(f"File size acceptable (within {MIN_FILE_SIZE_KB}-{MAX_FILE_SIZE_KB}KB range)")
        print()
        return 1, 0, 0

def check_page_count(pdf_info):
    """Check 3: Page count (CRITICAL)"""
    print(f"{Colors.BLUE}[3/7]{Colors.NC} Checking page count...")

    if pdf_info is None:
        print_skip("pdfinfo not available - cannot check page count")
        print()
        return 0, 0, 1

    match = re.search(r'Pages:\s+(\d+)', pdf_info)
    if not match:
        print_warn("Could not determine page count")
        print()
        return 0, 0, 1

    page_count = int(match.group(1))
    print(f"   Pages: {page_count}")

    if page_count > MAX_PAGES:
        print_fail(f"Too many pages ({page_count} > {MAX_PAGES})")
        print(f"   {Colors.RED}CRITICAL: CV must be {MAX_PAGES} pages maximum{Colors.NC}")
        print("   This indicates BROKEN formatting (wrong YAML or missing Eisvogel)")
        print()
        return 0, 1, 0
    elif page_count == MAX_PAGES:
        print_pass(f"Perfect page count ({MAX_PAGES} pages)")
        print()
        return 1, 0, 0
    else:
        print_pass(f"Page count acceptable ({page_count} pages)")
        print()
        return 1, 0, 0

def check_paper_size(pdf_info):
    """Check 4: Paper size (CRITICAL)"""
    print(f"{Colors.BLUE}[4/7]{Colors.NC} Checking paper size...")

    if pdf_info is None:
        print_skip("pdfinfo not available - cannot check paper size")
        print()
        return 0, 0, 1

    match = re.search(r'Page size:\s+([\d.]+)\s+x\s+([\d.]+)', pdf_info)
    if not match:
        print_warn("Could not determine page size")
        print()
        return 0, 0, 1

    width = float(match.group(1))
    height = float(match.group(2))
    print(f"   Page size: {width} x {height} pts")

    # Allow small tolerance (±5 pts)
    if (EXPECTED_WIDTH - 5 <= width <= EXPECTED_WIDTH + 5 and
        EXPECTED_HEIGHT - 5 <= height <= EXPECTED_HEIGHT + 5):
        print_pass(f"A4 paper size confirmed ({int(width)} x {int(height)} pts)")
        print()
        return 1, 0, 0
    else:
        print_fail(f"Wrong paper size (expected {EXPECTED_WIDTH} x {EXPECTED_HEIGHT} pts)")
        print("   This indicates missing Eisvogel template or wrong configuration")
        print()
        return 0, 1, 0

def check_markdown_yaml(md_path):
    """Check 5: Markdown YAML validation"""
    print(f"{Colors.BLUE}[5/7]{Colors.NC} Checking markdown YAML...")

    if not md_path or not os.path.exists(md_path):
        print_skip("Markdown file not provided or not found")
        if md_path:
            print(f"   Looked for: {md_path}")
        print()
        return 0, 0, 1

    print(f"   Analyzing: {md_path}")

    with open(md_path, 'r', encoding='utf-8') as f:
        yaml_content = ''.join(f.readlines()[:30])

    issues = []
    if 'documentclass:' in yaml_content:
        print(f"{Colors.RED}   ❌ Found 'documentclass:' - DO NOT USE{Colors.NC}")
        issues.append('documentclass')

    if 'header-includes:' in yaml_content:
        print(f"{Colors.RED}   ❌ Found 'header-includes:' - DO NOT USE{Colors.NC}")
        issues.append('header-includes')

    if re.search(r'geometry:.*margin', yaml_content):
        print(f"{Colors.RED}   ❌ Found 'geometry: margin' - DO NOT USE{Colors.NC}")
        issues.append('geometry')

    if '\\usepackage' in yaml_content:
        print(f"{Colors.RED}   ❌ Found '\\usepackage' commands - DO NOT USE{Colors.NC}")
        issues.append('usepackage')

    if '\\titleformat' in yaml_content:
        print(f"{Colors.RED}   ❌ Found '\\titleformat' commands - DO NOT USE{Colors.NC}")
        issues.append('titleformat')

    if issues:
        print_fail(f"Markdown contains problematic YAML ({len(issues)} issues)")
        print("   These YAML elements break Eisvogel template formatting")
        print(f"   {Colors.YELLOW}FIX: Remove all custom YAML, use minimal or NO YAML{Colors.NC}")
        print()
        return 0, 1, 0
    else:
        print_pass("Markdown YAML looks clean (no problematic elements)")
        print()
        return 1, 0, 0

def check_pdf_metadata(pdf_info):
    """Check 6: PDF metadata"""
    print(f"{Colors.BLUE}[6/7]{Colors.NC} Checking PDF metadata...")

    if pdf_info is None:
        print_skip("pdfinfo not available - cannot check metadata")
        print()
        return 0, 0, 1

    creator_match = re.search(r'Creator:\s+(.+)', pdf_info)
    producer_match = re.search(r'Producer:\s+(.+)', pdf_info)

    creator = creator_match.group(1).strip() if creator_match else "Unknown"
    producer = producer_match.group(1).strip() if producer_match else "Unknown"

    print(f"   Creator: {creator}")
    print(f"   Producer: {producer}")

    if 'xelatex' in producer.lower() or 'xetex' in producer.lower():
        print_pass("Generated with XeLaTeX (expected for Eisvogel)")
        print()
        return 1, 0, 0
    else:
        print_warn("Not generated with XeLaTeX (might not be Eisvogel template)")
        print()
        return 0, 0, 1

def check_master_comparison(pdf_info):
    """Check 7: Comparison with master CV"""
    print(f"{Colors.BLUE}[7/7]{Colors.NC} Comparing with master CV...")

    master_cv_path = "master/ArturSwadzba_MasterCV.pdf"

    if not os.path.exists(master_cv_path):
        print_skip(f"Master CV not found at: {master_cv_path}")
        print()
        return 0, 0, 1

    print(f"   Found master CV: {master_cv_path}")

    if pdf_info is None:
        print_skip("pdfinfo not available - cannot compare")
        print()
        return 0, 0, 1

    master_info = get_pdf_info(master_cv_path)
    if master_info is None:
        print_skip("Could not read master CV info")
        print()
        return 0, 0, 1

    master_pages_match = re.search(r'Pages:\s+(\d+)', master_info)
    cv_pages_match = re.search(r'Pages:\s+(\d+)', pdf_info)

    if master_pages_match and cv_pages_match:
        master_pages = int(master_pages_match.group(1))
        cv_pages = int(cv_pages_match.group(1))

        if cv_pages == master_pages:
            print_pass(f"Same page count as master CV ({master_pages} pages)")
            print()
            return 1, 0, 0
        else:
            print_info(f"Different page count than master (CV: {cv_pages}, Master: {master_pages})")
            print("   This may be acceptable if CV is tailored/condensed")
            print()
            return 0, 0, 0

    print()
    return 0, 0, 0

def main():
    print_header()

    if len(sys.argv) < 2:
        print(f"{Colors.RED}❌ ERROR: No PDF file specified{Colors.NC}")
        print(f"Usage: {sys.argv[0]} <path-to-cv.pdf> [<path-to-markdown.md>]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    md_path = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.exists(pdf_path):
        print(f"{Colors.RED}❌ ERROR: PDF file not found: {pdf_path}{Colors.NC}")
        sys.exit(1)

    print(f"{Colors.BLUE}Validating:{Colors.NC} {pdf_path}")
    print()
    print(f"{Colors.BLUE}Running validation checks...{Colors.NC}")
    print()

    # Get PDF info once
    pdf_info = get_pdf_info(pdf_path)

    # Run all checks
    pass_count = 0
    fail_count = 0
    warn_count = 0

    # Check 1: File existence
    success, p, f, w = check_file_existence(pdf_path)
    if not success:
        sys.exit(1)
    pass_count += p; fail_count += f; warn_count += w

    # Check 2: File size
    p, f, w = check_file_size(pdf_path)
    pass_count += p; fail_count += f; warn_count += w

    # Check 3: Page count
    p, f, w = check_page_count(pdf_info)
    pass_count += p; fail_count += f; warn_count += w

    # Check 4: Paper size
    p, f, w = check_paper_size(pdf_info)
    pass_count += p; fail_count += f; warn_count += w

    # Check 5: Markdown YAML
    p, f, w = check_markdown_yaml(md_path)
    pass_count += p; fail_count += f; warn_count += w

    # Check 6: PDF metadata
    p, f, w = check_pdf_metadata(pdf_info)
    pass_count += p; fail_count += f; warn_count += w

    # Check 7: Master comparison
    p, f, w = check_master_comparison(pdf_info)
    pass_count += p; fail_count += f; warn_count += w

    # Print summary
    print(f"{Colors.BLUE}========================================{Colors.NC}")
    print(f"{Colors.BLUE}   VALIDATION SUMMARY{Colors.NC}")
    print(f"{Colors.BLUE}========================================{Colors.NC}")
    print()
    print(f"{Colors.GREEN}Passed:  {pass_count}{Colors.NC}")
    print(f"{Colors.RED}Failed:  {fail_count}{Colors.NC}")
    print(f"{Colors.YELLOW}Warnings: {warn_count}{Colors.NC}")
    print()

    # Overall result
    if fail_count == 0:
        if warn_count == 0:
            print(f"{Colors.GREEN}✅ OVERALL: EXCELLENT - CV formatting is perfect!{Colors.NC}")
            sys.exit(0)
        else:
            print(f"{Colors.YELLOW}⚠️  OVERALL: GOOD - CV passed with warnings{Colors.NC}")
            print("Review warnings above for potential improvements")
            sys.exit(0)
    else:
        print(f"{Colors.RED}❌ OVERALL: FAILED - CV has critical formatting issues{Colors.NC}")
        print()
        print(f"{Colors.YELLOW}REMEDIATION STEPS:{Colors.NC}")
        print("1. Check markdown YAML - remove documentclass, header-includes, geometry")
        print("2. Ensure pandoc command uses: --template eisvogel")
        print("3. Regenerate PDF with correct settings")
        print("4. Run this validator again")
        print()
        print(f"Reference working example: {Colors.BLUE}applications/2025-11-VirginAtlantic-DigitalProductLead/ArturSwadzba_CV_VirginAtlantic.pdf{Colors.NC}")
        sys.exit(1)

if __name__ == '__main__':
    main()
