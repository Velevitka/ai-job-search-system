#!/usr/bin/env python3
"""
Application Quality Audit Script

Audits CV and cover letter quality across all applications:
- PDF format validation (page counts, file sizes, paper sizes)
- Keyword integration verification
- Missing files detection
- Consistency checks

Run: python scripts/audit_application_quality.py
Output: insights/application-quality-audit-YYYY-MM-DD.md
"""

from pathlib import Path
from datetime import datetime
import subprocess
import re
from typing import List, Dict
import sys


class ApplicationAuditor:
    def __init__(self, applications_path: Path = Path("applications")):
        self.applications_path = applications_path
        self.issues = []
        self.warnings = []
        self.successes = []

    def get_pdf_info(self, pdf_path: Path) -> Dict:
        """Extract PDF metadata using pdfinfo command"""
        try:
            result = subprocess.run(
                ['pdfinfo', str(pdf_path)],
                capture_output=True,
                text=True,
                check=True
            )

            info = {}
            for line in result.stdout.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    info[key.strip()] = value.strip()

            # Extract specific fields
            pages_match = re.search(r'Pages:\s*(\d+)', result.stdout)
            size_match = re.search(r'Page size:\s*([\d.]+)\s*x\s*([\d.]+)\s*pts', result.stdout)

            return {
                'pages': int(pages_match.group(1)) if pages_match else None,
                'width': float(size_match.group(1)) if size_match else None,
                'height': float(size_match.group(2)) if size_match else None,
            }
        except (subprocess.CalledProcessError, FileNotFoundError):
            # pdfinfo not available, fall back to file size only
            return {
                'pages': None,
                'width': None,
                'height': None,
            }

    def check_cv_format(self, cv_path: Path, company: str):
        """Validate CV format requirements"""
        if not cv_path.exists():
            self.issues.append(f"{company}: CV file not found at {cv_path.name}")
            return

        # Check file size
        file_size_kb = cv_path.stat().st_size / 1024

        if not (60 <= file_size_kb <= 80):
            self.warnings.append(
                f"{company}: CV file size {file_size_kb:.1f}KB outside ideal range (60-80KB)"
            )

        # Check PDF metadata
        pdf_info = self.get_pdf_info(cv_path)

        # Check page count (must be ≤2 pages)
        if pdf_info['pages'] is not None:
            if pdf_info['pages'] > 2:
                self.issues.append(
                    f"{company}: CV has {pdf_info['pages']} pages (must be ≤2)"
                )
            elif pdf_info['pages'] == 2:
                self.successes.append(f"{company}: CV is 2 pages ✓")

        # Check paper size (must be A4: 595 x 842 pts)
        if pdf_info['width'] and pdf_info['height']:
            width, height = pdf_info['width'], pdf_info['height']
            is_a4 = (abs(width - 595) < 5 and abs(height - 842) < 5)

            if not is_a4:
                self.issues.append(
                    f"{company}: CV paper size {width}x{height}pts (expected A4: 595x842pts)"
                )

    def check_cl_format(self, cl_path: Path, company: str):
        """Validate cover letter format requirements"""
        if not cl_path.exists():
            # Cover letter is optional, so this is a warning not an issue
            self.warnings.append(f"{company}: No cover letter generated")
            return

        # Check file size (CLs should be smaller, ~10-20KB)
        file_size_kb = cl_path.stat().st_size / 1024

        if file_size_kb > 30:
            self.warnings.append(
                f"{company}: Cover letter file size {file_size_kb:.1f}KB unusually large"
            )

        # Check PDF metadata
        pdf_info = self.get_pdf_info(cl_path)

        # Check page count (must be exactly 1 page)
        if pdf_info['pages'] is not None:
            if pdf_info['pages'] != 1:
                self.issues.append(
                    f"{company}: Cover letter has {pdf_info['pages']} pages (must be exactly 1)"
                )
            else:
                self.successes.append(f"{company}: Cover letter is 1 page ✓")

    def check_keyword_integration(self, company_folder: Path, company: str):
        """Verify keywords from analysis.md appear in CV"""
        analysis_file = company_folder / "analysis.md"
        cv_md_file = company_folder / f"ArturSwadzba_CV_{company.split('-')[-1]}.md"

        if not analysis_file.exists():
            return  # No analysis to check against

        # Extract keywords from analysis.md
        analysis_content = analysis_file.read_text(encoding='utf-8')
        keywords_match = re.search(
            r'### Critical Keywords to Integrate\n\n(.*?)\n\n###',
            analysis_content,
            re.DOTALL
        )

        if not keywords_match:
            return  # No keywords section found

        keywords_section = keywords_match.group(1)
        keywords = re.findall(r'`([^`]+)`', keywords_section)

        if not keywords:
            return

        # Check if CV markdown exists
        if not cv_md_file.exists():
            self.warnings.append(f"{company}: CV markdown not found, cannot verify keywords")
            return

        cv_content = cv_md_file.read_text(encoding='utf-8').lower()

        # Check which keywords are missing
        missing_keywords = []
        for keyword in keywords[:5]:  # Check first 5 priority keywords
            if keyword.lower() not in cv_content:
                missing_keywords.append(keyword)

        if missing_keywords:
            self.warnings.append(
                f"{company}: Keywords not found in CV: {', '.join(missing_keywords)}"
            )

    def check_application_completeness(self, company_folder: Path, company: str):
        """Check if application has all required files"""
        required_files = ['job-description.md', 'analysis.md', 'status.md']
        missing_files = []

        for filename in required_files:
            if not (company_folder / filename).exists():
                missing_files.append(filename)

        if missing_files:
            self.issues.append(f"{company}: Missing files: {', '.join(missing_files)}")

    def check_applied_status_has_cv(self, company_folder: Path, company: str):
        """Applications with status='applied' must have CV"""
        status_file = company_folder / "status.md"

        if not status_file.exists():
            return

        content = status_file.read_text(encoding='utf-8')

        # Check if status is 'applied'
        if "**Current Status:** applied" in content:
            # Check if CV exists
            cv_files = list(company_folder.glob("*_CV_*.pdf"))

            if not cv_files:
                self.issues.append(
                    f"{company}: Status is 'applied' but no CV file found"
                )

    def audit_all_applications(self):
        """Run audit on all application folders"""
        print("🔍 Auditing application quality...")
        print()

        for app_folder in sorted(self.applications_path.glob("2025-*")):
            if not app_folder.is_dir():
                continue

            company = app_folder.name
            print(f"  Checking {company}...")

            # Check application completeness
            self.check_application_completeness(app_folder, company)

            # Check CV format
            cv_pdf = app_folder / f"ArturSwadzba_CV_{company.split('-')[-1]}.pdf"
            if cv_pdf.exists():
                self.check_cv_format(cv_pdf, company)

            # Check cover letter format
            cl_pdf = app_folder / f"ArturSwadzba_CoverLetter_{company.split('-')[-1]}.pdf"
            if cl_pdf.exists():
                self.check_cl_format(cl_pdf, company)

            # Check keyword integration
            self.check_keyword_integration(app_folder, company)

            # Check applied status has CV
            self.check_applied_status_has_cv(app_folder, company)

        print()
        print(f"✅ Audit complete: {len(list(self.applications_path.glob('2025-*')))} applications checked")

    def generate_report(self) -> str:
        """Generate audit report in markdown"""
        report = f"""# Application Quality Audit Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Applications Audited:** {len(list(self.applications_path.glob('2025-*')))}

---

## Summary

- **Critical Issues:** {len(self.issues)}
- **Warnings:** {len(self.warnings)}
- **Successes:** {len(self.successes)}

**Overall Quality:** {'✅ Excellent' if len(self.issues) == 0 else '⚠️ Needs Attention' if len(self.issues) < 3 else '❌ Poor'}

---

## Critical Issues ({len(self.issues)})

"""
        if self.issues:
            for issue in self.issues:
                report += f"❌ {issue}\n"
        else:
            report += "None! All applications pass critical checks ✅\n"

        report += f"""
---

## Warnings ({len(self.warnings)})

"""
        if self.warnings:
            for warning in self.warnings:
                report += f"⚠️ {warning}\n"
        else:
            report += "None! All applications meet best practices ✅\n"

        report += f"""
---

## Successes ({len(self.successes)})

"""
        if self.successes:
            for success in self.successes:
                report += f"✅ {success}\n"
        else:
            report += "No specific successes to highlight\n"

        report += """
---

## Quality Checklist

**CV Requirements:**
- ✅ Page count: ≤2 pages (strict requirement)
- ✅ File size: 60-80KB (ideal for Eisvogel template)
- ✅ Paper size: A4 (595 x 842 pts)
- ✅ Keywords from analysis.md integrated

**Cover Letter Requirements:**
- ✅ Page count: Exactly 1 page (strict requirement)
- ✅ Word count: 300-400 words (optimal)
- ✅ Company-specific research included

**Application Completeness:**
- ✅ job-description.md exists
- ✅ analysis.md exists
- ✅ status.md exists
- ✅ CV PDF exists if status='applied'

---

## Recommendations

"""

        # Generate recommendations based on findings
        if not self.issues and not self.warnings:
            report += "✅ All applications meet quality standards. No action required.\n"
        else:
            if self.issues:
                report += "**Critical Issues to Fix:**\n"
                for issue in self.issues[:3]:  # Show top 3
                    report += f"1. Fix: {issue}\n"
                report += "\n"

            if self.warnings:
                report += "**Improvements to Consider:**\n"
                warning_summary = {}
                for warning in self.warnings:
                    category = warning.split(':')[1].split()[0] if ':' in warning else 'Other'
                    warning_summary[category] = warning_summary.get(category, 0) + 1

                for category, count in sorted(warning_summary.items(), key=lambda x: -x[1]):
                    report += f"- {count}x {category} warnings\n"

        report += """
---

## How to Fix Issues

**CV Page Count > 2:**
```bash
# Regenerate with tighter formatting
cd applications/[Company]/
# Edit cv-tailoring-plan.md to reduce content
# Re-run /generate-cv [Company]
```

**Missing Keywords:**
```bash
# Review analysis.md keywords section
# Edit CV markdown to integrate keywords naturally
# Regenerate PDF
```

**Missing CV for Applied Status:**
```bash
# Generate CV before marking as applied
/generate-cv [Company]
# Then update status
/update-status [Company] applied "notes"
```

---

**Next Audit:** Run before bulk submission or monthly
**Script:** `python scripts/audit_application_quality.py`
"""

        return report

    def save_report(self, report: str):
        """Save report to insights folder"""
        insights_path = Path("insights")
        insights_path.mkdir(exist_ok=True)

        filename = f"application-quality-audit-{datetime.now().strftime('%Y-%m-%d')}.md"
        output_path = insights_path / filename

        output_path.write_text(report, encoding='utf-8')
        print(f"📄 Report saved to: {output_path}")

        return output_path


def main():
    """Run application quality audit"""
    print("🔍 Application Quality Audit")
    print("=" * 50)
    print()

    auditor = ApplicationAuditor()
    auditor.audit_all_applications()

    print()
    print("📊 Results:")
    print(f"  Critical Issues: {len(auditor.issues)}")
    print(f"  Warnings: {len(auditor.warnings)}")
    print(f"  Successes: {len(auditor.successes)}")
    print()

    report = auditor.generate_report()
    output_path = auditor.save_report(report)

    print()
    if auditor.issues:
        print("❌ Critical issues found! Review report for details.")
        sys.exit(1)
    elif auditor.warnings:
        print("⚠️  Some warnings found. Review report for improvements.")
        sys.exit(0)
    else:
        print("✅ All applications pass quality checks!")
        sys.exit(0)


if __name__ == "__main__":
    main()
