#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cover Letter Format Validation Script
Validates cover letter PDF formatting to ensure 1-page requirement
Usage: python validate-cover-letter.py <path-to-cl.pdf> [<path-to-markdown.md>]
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
MAX_PAGES = 1  # CRITICAL: Cover letters MUST be 1 page
MIN_WORD_COUNT = 250
MAX_WORD_COUNT = 400
TARGET_MIN_WORD_COUNT = 300
TARGET_MAX_WORD_COUNT = 400
MIN_FILE_SIZE_KB = 10
MAX_FILE_SIZE_KB = 25
TARGET_MIN_SIZE_KB = 12
TARGET_MAX_SIZE_KB = 18
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
    print(f"{Colors.BLUE}   COVER LETTER VALIDATION TOOL{Colors.NC}")
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
    print(f"{Colors.BLUE}[1/6]{Colors.NC} Checking file existence...")

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
    print(f"{Colors.BLUE}[2/6]{Colors.NC} Checking file size...")

    file_size_bytes = os.path.getsize(pdf_path)
    file_size_kb = file_size_bytes // 1024

    print(f"   File size: {file_size_kb}KB")

    if file_size_kb < MIN_FILE_SIZE_KB:
        print_fail(f"File too small ({file_size_kb}KB < {MIN_FILE_SIZE_KB}KB)")
        print("   This suggests wrong template or missing fonts")
        print()
        return 0, 1, 0
    elif file_size_kb > MAX_FILE_SIZE_KB:
        print_warn(f"File larger than expected ({file_size_kb}KB > {MAX_FILE_SIZE_KB}KB)")
        print("   This might indicate embedded images or unusual content")
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
    """Check 3: Page count (CRITICAL - MUST BE 1)"""
    print(f"{Colors.BLUE}[3/6]{Colors.NC} Checking page count...")

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
        print_fail(f"TOO MANY PAGES ({page_count} pages)")
        print(f"   {Colors.RED}CRITICAL: Cover letters MUST be {MAX_PAGES} page{Colors.NC}")
        print(f"   {Colors.RED}This is UNPROFESSIONAL and will hurt your application{Colors.NC}")
        print()
        print(f"   {Colors.YELLOW}FIX:{Colors.NC}")
        print(f"   1. Reduce word count to 300-400 words (currently likely 450-500)")
        print(f"   2. Shorten paragraphs (max 3-4 sentences each)")
        print(f"   3. Remove excessive spacing")
        print(f"   4. Regenerate PDF")
        print()
        return 0, 1, 0
    elif page_count == MAX_PAGES:
        print_pass(f"Perfect page count ({MAX_PAGES} page)")
        print()
        return 1, 0, 0
    else:
        print_warn(f"Less than 1 page ({page_count} pages)")
        print("   Cover letter might be too short")
        print()
        return 0, 0, 1

def check_paper_size(pdf_info):
    """Check 4: Paper size"""
    print(f"{Colors.BLUE}[4/6]{Colors.NC} Checking paper size...")

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
        print("   Cover letters should be A4 format")
        print()
        return 0, 1, 0

def check_word_count(md_path):
    """Check 5: Word count in markdown"""
    print(f"{Colors.BLUE}[5/6]{Colors.NC} Checking word count...")

    if not md_path or not os.path.exists(md_path):
        print_skip("Markdown file not provided or not found")
        if md_path:
            print(f"   Looked for: {md_path}")
        print()
        return 0, 0, 1

    print(f"   Analyzing: {md_path}")

    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract body text (between "Dear" and signature)
    body_match = re.search(r'Dear.*?(?=\\vspace|Warm regards|Best regards|Sincerely)', content, re.DOTALL)

    if body_match:
        body_text = body_match.group(0)
        # Remove LaTeX commands and count words
        clean_text = re.sub(r'\\[a-zA-Z]+(\{[^}]*\})?', '', body_text)
        words = clean_text.split()
        word_count = len(words)
    else:
        # Fallback: count all non-YAML words
        lines = content.split('\n')
        in_yaml = False
        body_lines = []
        for line in lines:
            if line.strip() == '---':
                in_yaml = not in_yaml
                continue
            if not in_yaml and line.strip():
                body_lines.append(line)
        clean_text = ' '.join(body_lines)
        clean_text = re.sub(r'\\[a-zA-Z]+(\{[^}]*\})?', '', clean_text)
        words = clean_text.split()
        word_count = len(words)

    print(f"   Word count: {word_count} words")

    if word_count < MIN_WORD_COUNT:
        print_warn(f"Word count too low ({word_count} < {MIN_WORD_COUNT})")
        print("   Cover letter might be too brief")
        print()
        return 0, 0, 1
    elif word_count > MAX_WORD_COUNT:
        print_fail(f"Word count too high ({word_count} > {MAX_WORD_COUNT})")
        print(f"   {Colors.RED}This will create a 2-page cover letter!{Colors.NC}")
        print(f"   {Colors.YELLOW}FIX: Reduce to {TARGET_MIN_WORD_COUNT}-{TARGET_MAX_WORD_COUNT} words{Colors.NC}")
        print()
        return 0, 1, 0
    elif TARGET_MIN_WORD_COUNT <= word_count <= TARGET_MAX_WORD_COUNT:
        print_pass(f"Word count in optimal range ({TARGET_MIN_WORD_COUNT}-{TARGET_MAX_WORD_COUNT})")
        print()
        return 1, 0, 0
    else:
        print_pass(f"Word count acceptable ({MIN_WORD_COUNT}-{MAX_WORD_COUNT})")
        print()
        return 1, 0, 0

def check_markdown_yaml(md_path):
    """Check 6: Markdown YAML validation"""
    print(f"{Colors.BLUE}[6/6]{Colors.NC} Checking markdown YAML...")

    if not md_path or not os.path.exists(md_path):
        print_skip("Markdown file not provided or not found")
        print()
        return 0, 0, 1

    with open(md_path, 'r', encoding='utf-8') as f:
        yaml_content = ''.join(f.readlines()[:30])

    issues = []
    if 'documentclass:' in yaml_content:
        print(f"{Colors.RED}   ❌ Found 'documentclass:' - DO NOT USE{Colors.NC}")
        issues.append('documentclass')

    if 'header-includes:' in yaml_content:
        print(f"{Colors.RED}   ❌ Found 'header-includes:' - DO NOT USE{Colors.NC}")
        issues.append('header-includes')

    if re.search(r'\\usepackage', yaml_content):
        print(f"{Colors.RED}   ❌ Found '\\usepackage' commands - DO NOT USE{Colors.NC}")
        issues.append('usepackage')

    # Count \vspace commands
    vspace_count = len(re.findall(r'\\vspace', yaml_content))
    if vspace_count > 2:
        print(f"{Colors.YELLOW}   ⚠️  Found {vspace_count} \\vspace commands - excessive spacing{Colors.NC}")
        issues.append('excessive vspace')

    if issues:
        print_fail(f"Markdown has problematic elements ({len(issues)} issues)")
        print(f"   {Colors.YELLOW}FIX: Use minimal YAML (geometry + fontsize only){Colors.NC}")
        print()
        return 0, 1, 0
    else:
        print_pass("Markdown YAML looks clean")
        print()
        return 1, 0, 0

def main():
    print_header()

    if len(sys.argv) < 2:
        print(f"{Colors.RED}❌ ERROR: No PDF file specified{Colors.NC}")
        print(f"Usage: {sys.argv[0]} <path-to-cl.pdf> [<path-to-markdown.md>]")
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

    # Check 3: Page count (CRITICAL)
    p, f, w = check_page_count(pdf_info)
    pass_count += p; fail_count += f; warn_count += w

    # Check 4: Paper size
    p, f, w = check_paper_size(pdf_info)
    pass_count += p; fail_count += f; warn_count += w

    # Check 5: Word count
    p, f, w = check_word_count(md_path)
    pass_count += p; fail_count += f; warn_count += w

    # Check 6: Markdown YAML
    p, f, w = check_markdown_yaml(md_path)
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
            print(f"{Colors.GREEN}✅ OVERALL: PERFECT - Cover letter formatting is correct!{Colors.NC}")
            sys.exit(0)
        else:
            print(f"{Colors.YELLOW}⚠️  OVERALL: GOOD - Cover letter passed with warnings{Colors.NC}")
            print("Review warnings above for potential improvements")
            sys.exit(0)
    else:
        print(f"{Colors.RED}❌ OVERALL: FAILED - Cover letter has critical formatting issues{Colors.NC}")
        print()
        print(f"{Colors.YELLOW}REMEDIATION STEPS:{Colors.NC}")
        print("1. Check markdown word count - reduce to 300-400 words")
        print("2. Shorten paragraphs (3-4 sentences max each)")
        print("3. Remove excessive \\vspace commands")
        print("4. Ensure YAML has only geometry + fontsize")
        print("5. Regenerate PDF with Eisvogel template")
        print("6. Run this validator again")
        print()
        sys.exit(1)

if __name__ == '__main__':
    main()
