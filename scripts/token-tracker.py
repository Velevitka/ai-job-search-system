#!/usr/bin/env python3
"""
Token Usage Tracker for CV Application System

Estimates token usage for common operations and tracks patterns.
"""

import os
from pathlib import Path
from typing import Dict, List, Tuple

# Rough token estimation: ~4 characters per token (OpenAI average)
CHARS_PER_TOKEN = 4

def estimate_tokens(text: str) -> int:
    """Estimate tokens for a given text."""
    return len(text) // CHARS_PER_TOKEN

def analyze_file_tokens(file_path: Path) -> Dict:
    """Analyze token usage for a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return {
                'file': str(file_path),
                'size_bytes': len(content.encode('utf-8')),
                'size_chars': len(content),
                'estimated_tokens': estimate_tokens(content)
            }
    except Exception as e:
        return {
            'file': str(file_path),
            'error': str(e)
        }

def analyze_master_folder() -> List[Dict]:
    """Analyze token usage for master folder files."""
    master_path = Path("master")
    results = []

    files_to_check = [
        "ArturSwadzba_MasterCV_Updated.md",
        "ArturSwadzba_MasterCV_NOTES.md",
        "cv-snippets.md",
        "master-cv-changelog.md",
        "ArturSwadzba_MasterCV.pdf",  # Note: PDF not readable as text
    ]

    for filename in files_to_check:
        file_path = master_path / filename
        if file_path.exists():
            results.append(analyze_file_tokens(file_path))

    return results

def analyze_command_workflow(command_name: str) -> Dict:
    """Estimate token usage for a typical command workflow."""
    workflows = {
        'analyze-job': {
            'reads': [
                'master/ArturSwadzba_MasterCV_Updated.md',
                'master/ArturSwadzba_MasterCV_NOTES.md',
                'career-preferences.md',
                'job-description.md (estimate)',
            ],
            'writes': [
                'job-description.md',
                'analysis.md',
            ]
        },
        'generate-cv': {
            'reads': [
                'master/ArturSwadzba_MasterCV_Updated.md',
                'master/ArturSwadzba_MasterCV_NOTES.md',
                'applications/.../analysis.md',
            ],
            'writes': [
                'cv-tailoring-plan.md',
                'ArturSwadzba_CV_Company.md',
                'cv-changes-log.md',
            ]
        },
        'generate-cl': {
            'reads': [
                'master/ArturSwadzba_MasterCV_Updated.md',
                'master/ArturSwadzba_MasterCV_NOTES.md',
                'applications/.../analysis.md',
                'applications/.../job-description.md',
            ],
            'writes': [
                'company-research-brief.md',
                'cover-letter-draft.md',
                'ArturSwadzba_CoverLetter_Company.md',
                'cover-letter-log.md',
            ]
        }
    }

    return workflows.get(command_name, {})

def generate_report():
    """Generate token usage report."""
    print("Token Usage Analysis Report")
    print("=" * 60)
    print()

    # Master folder analysis
    print("Master Folder Token Costs:")
    print("-" * 60)
    master_results = analyze_master_folder()
    total_tokens = 0

    for result in master_results:
        if 'error' not in result:
            tokens = result['estimated_tokens']
            total_tokens += tokens
            print(f"  {result['file']:45} {tokens:>6,} tokens")
        else:
            print(f"  {result['file']:45} ERROR")

    print(f"  {'TOTAL (Tier 1 - Essential)':45} {total_tokens:>6,} tokens")
    print()

    # Typical workflow costs
    print("Typical Workflow Costs (Estimated):")
    print("-" * 60)

    workflows = {
        '/analyze-job': 15000,
        '/generate-cv': 20000,
        '/generate-cl': 18000,
    }

    for workflow, tokens in workflows.items():
        print(f"  {workflow:30} ~{tokens:>6,} tokens")

    print()

    # Optimization recommendations
    print("Optimization Recommendations:")
    print("-" * 60)
    essential_tokens = sum(r.get('estimated_tokens', 0) for r in master_results if 'error' not in r)

    if essential_tokens > 15000:
        print("  [!] Essential reads >15K tokens - consider consolidation")
    else:
        print("  [OK] Essential reads optimized (<15K tokens)")

    print()
    print(f"Current Session Budget: 200,000 tokens")
    print(f"   Typical workflow cost: ~20,000 tokens")
    print(f"   Workflows per session: ~10 operations")
    print()

if __name__ == "__main__":
    generate_report()
