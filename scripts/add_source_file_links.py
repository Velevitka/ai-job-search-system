#!/usr/bin/env python3
"""
Retroactively Add source_file Links

Adds 'source_file' field to existing job-description.md files to create
explicit link between application folders and job files in staging/3-applying/.

This improves orphan detection accuracy in health checks.

Run: python scripts/add_source_file_links.py
"""

from pathlib import Path
import re
from typing import Optional


class SourceFileLinkAdder:
    def __init__(self, root_path: Path = Path(".")):
        self.root = root_path
        self.applications = root_path / "applications"
        self.staging = root_path / "staging"
        self.updated_count = 0
        self.already_has_link = 0
        self.no_match_found = 0

        # Search locations for job files
        self.search_paths = [
            self.staging / "3-applying",
            self.staging / "2-shortlist" / "high",
            self.staging / "2-shortlist" / "medium",
            self.staging / "2-shortlist" / "pending-insider-intel",
            self.staging / "archive" / "rejected",
            self.staging / "archive" / "withdrawn",
            self.staging / "archive" / "accepted",
            self.staging / "archive" / "filtered",
            self.staging / "archive" / "low-fit",
        ]

    def extract_tokens(self, text: str) -> set:
        """Extract meaningful tokens from text for matching"""
        # Split CamelCase words BEFORE lowercasing (VPProduct → VP Product)
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
        text = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', text)  # Handle VPPM → VP PM

        # Now lowercase
        text = text.lower()

        # Replace separators with spaces
        text = text.replace('-', ' ').replace('_', ' ').replace('(', ' ').replace(')', ' ')
        tokens = text.split()

        stop_words = {'at', 'in', 'the', 'a', 'an', 'for', 'on', 'to', 'of', 'and', 'or',
                      'job', 'application', 'apply', 'career', 'careers', 'jobs', 'linkedin',
                      '2025', '11', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '12',
                      'director', 'head', 'senior', 'manager', 'lead', 'vp', 'vice', 'president',
                      'product', 'management', 'pm'}

        meaningful_tokens = {
            token for token in tokens
            if len(token) > 2 and token not in stop_words and not token.isdigit()
        }

        return meaningful_tokens

    def find_matching_job_file(self, app_folder: Path) -> Optional[Path]:
        """Find the job file that matches this application folder"""
        folder_tokens = self.extract_tokens(app_folder.name)

        best_match = None
        best_score = 0

        # Search across all staging locations
        for search_path in self.search_paths:
            if not search_path.exists():
                continue

            for job_file in search_path.glob("*.mhtml"):
                job_tokens = self.extract_tokens(job_file.stem)

                # Calculate overlap score
                common_tokens = folder_tokens & job_tokens
                if len(common_tokens) > 0:
                    score = len(common_tokens) / max(len(folder_tokens), len(job_tokens))

                    if score > best_score:
                        best_score = score
                        best_match = job_file

        # Only return match if confidence is reasonably high
        if best_score > 0.20:  # Lowered threshold
            return best_match

        return None

    def has_source_file(self, content: str) -> bool:
        """Check if job-description.md already has source_file field"""
        if not content.startswith('---'):
            return False

        yaml_end = content.find('---', 3)
        if yaml_end < 0:
            return False

        front_matter = content[3:yaml_end]
        return 'source_file:' in front_matter

    def add_source_file_to_yaml(self, content: str, source_file_name: str) -> str:
        """Add source_file field to YAML front matter"""
        if not content.startswith('---'):
            # No YAML front matter, add it
            return f"""---
source_file: "{source_file_name}"
---

{content}"""

        yaml_end = content.find('---', 3)
        if yaml_end < 0:
            # Malformed YAML, add at start
            return f"""---
source_file: "{source_file_name}"
---

{content}"""

        # Insert source_file at the end of YAML front matter
        front_matter = content[3:yaml_end]
        rest_of_content = content[yaml_end + 3:]

        # Add source_file before closing ---
        new_front_matter = front_matter.rstrip() + f'\nsource_file: "{source_file_name}"\n'

        return f"---{new_front_matter}---{rest_of_content}"

    def process_application(self, app_folder: Path):
        """Process a single application folder"""
        job_desc_file = app_folder / "job-description.md"

        if not job_desc_file.exists():
            return

        try:
            content = job_desc_file.read_text(encoding='utf-8')

            # Check if already has source_file
            if self.has_source_file(content):
                self.already_has_link += 1
                print(f"  ✓ {app_folder.name} - Already has source_file")
                return

            # Find matching job file
            job_file = self.find_matching_job_file(app_folder)

            if not job_file:
                self.no_match_found += 1
                print(f"  ⚠ {app_folder.name} - No matching job file found")
                return

            # Add source_file to YAML
            updated_content = self.add_source_file_to_yaml(content, job_file.name)

            # Write back
            job_desc_file.write_text(updated_content, encoding='utf-8')

            self.updated_count += 1
            print(f"  ✅ {app_folder.name} - Added source_file: {job_file.name}")

        except Exception as e:
            print(f"  ❌ {app_folder.name} - Error: {e}")

    def run(self):
        """Process all application folders"""
        print("🔗 Adding source_file Links to Applications")
        print("=" * 60)
        print()

        if not self.applications.exists():
            print("❌ applications/ folder not found")
            return

        app_folders = sorted(self.applications.glob("2025-*"))

        if not app_folders:
            print("No application folders found")
            return

        print(f"Found {len(app_folders)} application folders")
        print()

        for app_folder in app_folders:
            if app_folder.is_dir():
                self.process_application(app_folder)

        print()
        print("=" * 60)
        print("📊 Summary:")
        print(f"  ✅ Updated: {self.updated_count}")
        print(f"  ✓ Already linked: {self.already_has_link}")
        print(f"  ⚠ No match found: {self.no_match_found}")
        print()

        if self.updated_count > 0:
            print(f"✅ Successfully added source_file links to {self.updated_count} applications")
        else:
            print("ℹ️ No updates needed")


def main():
    import sys
    import io

    # Set UTF-8 encoding for Windows console
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    adder = SourceFileLinkAdder()
    adder.run()


if __name__ == "__main__":
    main()
