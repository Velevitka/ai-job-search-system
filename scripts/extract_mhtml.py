#!/usr/bin/env python3
"""
Extract job descriptions from LinkedIn MHTML files
"""

import re
import sys
from pathlib import Path


def decode_quoted_printable(text):
    """Decode quoted-printable encoding"""
    # Remove soft line breaks (= at end of line)
    text = text.replace('=\n', '')
    text = text.replace('=\r\n', '')

    # Decode =XX hex codes
    def hex_replacer(match):
        try:
            return chr(int(match.group(1), 16))
        except:
            return match.group(0)

    text = re.sub(r'=([0-9A-F]{2})', hex_replacer, text, flags=re.IGNORECASE)
    return text


def extract_html_from_mhtml(mhtml_content):
    """Extract HTML content from MHTML file"""
    # Find the text/html section
    html_match = re.search(
        r'Content-Type: text/html.*?\n\n(.*?)(?=\n------MultipartBoundary|$)',
        mhtml_content,
        re.DOTALL
    )

    if not html_match:
        return None

    html_content = html_match.group(1)

    # Decode quoted-printable
    html_content = decode_quoted_printable(html_content)

    return html_content


def extract_text_from_html(html):
    """Extract visible text from HTML"""
    # Remove script and style tags
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)

    # Remove HTML tags but keep spacing
    text = re.sub(r'<[^>]+>', ' ', html)

    # Decode HTML entities
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    text = text.replace('&#39;', "'")

    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()

    return text


def extract_job_info_from_mhtml(filepath):
    """Extract job information from LinkedIn MHTML file"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            mhtml_content = f.read()

        # Extract filename info
        filename = Path(filepath).name

        # Parse filename: Multiple formats
        company = "Unknown"
        job_title = "Unknown"

        # Format 1: "Job Application for [Role] at [Company].mhtml"
        if filename.startswith('Job Application for'):
            match = re.match(r'Job Application for (.+?) at (.+?)\.mhtml', filename)
            if match:
                job_title = match.group(1).strip()
                company = match.group(2).strip()
        # Format 2: "(1) Job Title _ Company Name _ LinkedIn.mhtml"
        elif '_' in filename:
            parts = filename.replace('.mhtml', '').split(' _ ')
            if len(parts) >= 2:
                # Remove "(1)" prefix if present
                title_part = parts[0].strip()
                title_part = re.sub(r'^\(\d+\)\s*', '', title_part)
                job_title = title_part

                # Company is second to last part (before "LinkedIn")
                company = parts[-2].strip() if len(parts) > 2 else parts[1].strip()
        # Format 3: "[Role] @ [Company].mhtml" or "[Role] - [Company].mhtml"
        elif '@' in filename or ' - ' in filename:
            for sep in [' @ ', ' - ']:
                if sep in filename:
                    parts = filename.replace('.mhtml', '').split(sep)
                    if len(parts) == 2:
                        job_title = parts[0].strip()
                        company = parts[1].strip()
                    break

        # Extract HTML content
        html = extract_html_from_mhtml(mhtml_content)
        if not html:
            return None

        # Extract all text
        full_text = extract_text_from_html(html)

        # Try to find job description section
        # Look for common LinkedIn job page markers
        desc_section = ""

        # Method 1: Look for "About the job" section
        about_match = re.search(r'About the job(.*?)(?=Show more|Show less|Apply|Easy Apply|Save|$)',
                               full_text, re.DOTALL | re.IGNORECASE)
        if about_match:
            desc_section = about_match.group(1).strip()

        # Method 2: Look for sections after company name
        if not desc_section and company in full_text:
            # Find text after first mention of company
            company_pos = full_text.find(company)
            if company_pos > 0:
                # Get next 2000 characters as description
                desc_section = full_text[company_pos:company_pos + 2000]

        # Fallback: Use first 2000 characters of visible text
        if not desc_section:
            desc_section = full_text[:2000]

        return {
            'filename': filename,
            'company': company,
            'job_title': job_title,
            'description': desc_section[:1500],  # Limit to 1500 chars
            'full_text_length': len(full_text)
        }

    except Exception as e:
        return {
            'filename': Path(filepath).name,
            'error': str(e)
        }


if __name__ == '__main__':
    import sys
    import codecs

    # Force UTF-8 output
    if sys.platform == 'win32':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'ignore')

    if len(sys.argv) < 2:
        print("Usage: python extract_mhtml.py <mhtml_file>")
        sys.exit(1)

    result = extract_job_info_from_mhtml(sys.argv[1])

    if result and 'error' not in result:
        print(f"Company: {result['company']}")
        print(f"Job Title: {result['job_title']}")
        print(f"\nDescription (first 500 chars):")
        # Clean up any problematic characters
        desc = result['description'][:500].encode('ascii', 'ignore').decode('ascii')
        print(desc)
        print(f"\n... (full text length: {result['full_text_length']} chars)")
    elif result:
        print(f"Error: {result['error']}")
    else:
        print("Failed to extract information")
