#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Job Discovery & Scraping Automation

This script automates job discovery by searching LinkedIn Jobs and scraping
full job descriptions. It deduplicates against existing applications and
saves results to staging/ for analysis.

Usage:
    python scripts/job_discovery.py                    # Interactive mode
    python scripts/job_discovery.py --auto             # Use career-preferences.md
    python scripts/job_discovery.py --keywords "VP Product" --location "London"
"""

import argparse
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from playwright.sync_api import sync_playwright, Page, Browser

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass  # Fallback if reconfigure not available


class LinkedInJobSearcher:
    """Searches LinkedIn Jobs and scrapes job descriptions."""

    BASE_URL = "https://www.linkedin.com/jobs/search/"

    # Date filter codes
    DATE_FILTERS = {
        'past_24h': 'r86400',
        'past_week': 'r604800',
        'past_month': 'r2592000',
        'any_time': ''
    }

    def __init__(self, headless: bool = True, slow_mo: int = 100, user_data_dir: Optional[str] = None):
        """
        Initialize the searcher.

        Args:
            headless: Run browser in headless mode
            slow_mo: Slow down operations by N milliseconds (helps avoid detection)
            user_data_dir: Directory to store browser session (stays logged in)
        """
        self.headless = headless
        self.slow_mo = slow_mo
        self.user_data_dir = user_data_dir
        self.browser: Optional[Browser] = None
        self.context = None
        self.page: Optional[Page] = None
        self.playwright = None

    def build_search_url(
        self,
        keywords: str,
        location: str,
        date_posted: str = 'past_week',
        experience_level: Optional[List[str]] = None
    ) -> str:
        """
        Build LinkedIn job search URL with filters.

        Args:
            keywords: Job title or keywords (e.g., "Director Product Data Platform")
            location: Location (e.g., "London, United Kingdom")
            date_posted: One of: past_24h, past_week, past_month, any_time
            experience_level: List of: entry, associate, mid_senior, director, executive

        Returns:
            Complete search URL
        """
        params = {
            'keywords': keywords.replace(' ', '%20'),
            'location': location.replace(' ', '%20'),
        }

        # Add date filter
        if date_posted in self.DATE_FILTERS:
            date_code = self.DATE_FILTERS[date_posted]
            if date_code:
                params['f_TPR'] = date_code

        # Add experience level filter
        if experience_level:
            # LinkedIn codes: 2=Entry, 3=Associate, 4=Mid-Senior, 5=Director, 6=Executive
            level_codes = {
                'entry': '2',
                'associate': '3',
                'mid_senior': '4',
                'director': '5',
                'executive': '6'
            }
            codes = [level_codes[level] for level in experience_level if level in level_codes]
            if codes:
                params['f_E'] = '%2C'.join(codes)

        # Build URL
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        return f"{self.BASE_URL}?{query_string}"

    def start_browser(self):
        """Start Playwright browser with persistent context if configured."""
        self.playwright = sync_playwright().start()

        if self.user_data_dir:
            # Use persistent context (stays logged in)
            print(f"  💾 Using persistent browser session: {self.user_data_dir}")
            self.context = self.playwright.chromium.launch_persistent_context(
                user_data_dir=self.user_data_dir,
                headless=self.headless,
                slow_mo=self.slow_mo,
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            self.page = self.context.pages[0] if self.context.pages else self.context.new_page()
        else:
            # Regular browser (no session persistence)
            self.browser = self.playwright.chromium.launch(
                headless=self.headless,
                slow_mo=self.slow_mo
            )
            self.page = self.browser.new_page()

            # Set user agent to look more human
            self.page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })

    def close_browser(self):
        """Close browser."""
        if self.context:
            self.context.close()
        elif self.browser:
            self.browser.close()

        if self.playwright:
            self.playwright.stop()

    def check_login_status(self) -> bool:
        """
        Check if user is logged into LinkedIn.

        Returns:
            True if logged in, False otherwise
        """
        try:
            # Navigate to LinkedIn feed (requires login)
            self.page.goto('https://www.linkedin.com/feed/', wait_until='networkidle', timeout=10000)
            time.sleep(2)

            # Check if we're on the login page or feed
            current_url = self.page.url

            if '/login' in current_url or '/checkpoint' in current_url:
                return False

            # Check for feed elements (indicates logged in)
            try:
                self.page.wait_for_selector('.feed-shared-update-v2', timeout=5000)
                return True
            except:
                return False

        except Exception as e:
            print(f"  ⚠️ Could not check login status: {e}")
            return False

    def ensure_logged_in(self):
        """
        Ensure user is logged into LinkedIn.
        Pauses for manual login if needed.
        """
        print("\n🔐 Checking LinkedIn login status...")

        if not self.browser and not self.context:
            self.start_browser()

        is_logged_in = self.check_login_status()

        if is_logged_in:
            print("  ✅ Already logged in to LinkedIn")
            return

        print("\n  ⚠️ Not logged in to LinkedIn")
        print("\n" + "="*80)
        print("MANUAL LOGIN REQUIRED")
        print("="*80)
        print("\nThe browser window is now showing LinkedIn's login page.")
        print("\nPlease:")
        print("  1. Log in to your LinkedIn account in the browser window")
        print("  2. Complete any 2FA/security checks if prompted")
        print("  3. Wait until you see your LinkedIn feed")
        print("  4. Then come back here and press ENTER to continue")
        print("\nThe script will pause and wait for you...")
        print("="*80 + "\n")

        # Navigate to login page
        self.page.goto('https://www.linkedin.com/login')

        # Wait for user to log in manually
        input("Press ENTER after you've logged in to LinkedIn... ")

        # Verify login successful
        print("\n  🔍 Verifying login...")
        if self.check_login_status():
            print("  ✅ Login successful! Session will be saved for future runs.")

            if self.user_data_dir:
                print(f"  💾 Session saved to: {self.user_data_dir}")
                print("  ℹ️  Next time you run this script, you won't need to log in again!")
        else:
            print("  ❌ Login verification failed. Please try again.")
            raise Exception("LinkedIn login failed")

    def scroll_to_load_all_jobs(self, max_scrolls: int = 10):
        """
        Scroll down to load lazy-loaded job cards.

        Args:
            max_scrolls: Maximum number of scroll actions
        """
        print("  ⏬ Scrolling to load all job cards...")
        for i in range(max_scrolls):
            # Scroll down
            self.page.evaluate("window.scrollBy(0, 1000)")
            time.sleep(0.5)

            # Check if we've reached the bottom
            try:
                # LinkedIn shows "No more jobs" or pagination
                if self.page.query_selector('.jobs-search-results__list-item--load-more'):
                    break
            except:
                pass

        print(f"  ✓ Scrolled {max_scrolls} times to load content")

    def extract_job_cards(self) -> List[Dict[str, str]]:
        """
        Extract job cards from search results page.

        Returns:
            List of job dictionaries with: title, company, location, url
        """
        jobs = []

        # Try multiple selectors (LinkedIn changes them frequently)
        selectors = [
            '.jobs-search__results-list li',
            '.scaffold-layout__list-container li',
            'ul.jobs-search__results-list > li'
        ]

        job_cards = None
        for selector in selectors:
            try:
                job_cards = self.page.query_selector_all(selector)
                if job_cards and len(job_cards) > 0:
                    print(f"  ✓ Found {len(job_cards)} job cards using selector: {selector}")
                    break
            except:
                continue

        if not job_cards:
            print("  ⚠️ No job cards found")
            return jobs

        for card in job_cards:
            try:
                # Extract job title
                title_elem = card.query_selector('.job-card-list__title, .base-search-card__title')
                title = title_elem.inner_text().strip() if title_elem else None

                # Extract company
                company_elem = card.query_selector('.job-card-container__company-name, .base-search-card__subtitle')
                company = company_elem.inner_text().strip() if company_elem else None

                # Extract location
                location_elem = card.query_selector('.job-card-container__metadata-item, .job-search-card__location')
                location = location_elem.inner_text().strip() if location_elem else None

                # Extract URL
                link_elem = card.query_selector('a[href*="/jobs/view/"]')
                url = link_elem.get_attribute('href') if link_elem else None

                if title and company and url:
                    # Clean URL (remove tracking parameters)
                    clean_url = url.split('?')[0]

                    jobs.append({
                        'title': title,
                        'company': company,
                        'location': location or 'Not specified',
                        'url': clean_url
                    })

            except Exception as e:
                # Skip cards that fail to parse
                continue

        return jobs

    def search(
        self,
        keywords: str,
        location: str,
        date_posted: str = 'past_week',
        experience_level: Optional[List[str]] = None
    ) -> List[Dict[str, str]]:
        """
        Perform a job search on LinkedIn.

        Args:
            keywords: Job title or keywords
            location: Location string
            date_posted: Time filter
            experience_level: Experience level filters

        Returns:
            List of job dictionaries
        """
        # Ensure logged in before searching
        if not self.browser and not self.context:
            self.start_browser()

        self.ensure_logged_in()

        url = self.build_search_url(keywords, location, date_posted, experience_level)

        print(f"\n🔍 Searching LinkedIn Jobs:")
        print(f"  Keywords: {keywords}")
        print(f"  Location: {location}")
        print(f"  Date: {date_posted}")

        try:
            # Navigate to search URL
            print(f"  🌐 Loading: {url}")
            self.page.goto(url, timeout=30000, wait_until='networkidle')

            # Wait for job cards to load
            time.sleep(2)

            # Scroll to load more results
            self.scroll_to_load_all_jobs()

            # Extract job cards
            jobs = self.extract_job_cards()

            print(f"  ✅ Found {len(jobs)} jobs")
            return jobs

        except Exception as e:
            print(f"  ❌ Search failed: {e}")
            return []

    def scrape_job_description(self, url: str) -> Optional[str]:
        """
        Scrape full job description from a LinkedIn job posting.

        Args:
            url: LinkedIn job URL

        Returns:
            Job description text or None if failed
        """
        if not self.browser:
            self.start_browser()

        try:
            print(f"    📄 Scraping: {url}")
            self.page.goto(url, timeout=30000, wait_until='networkidle')
            time.sleep(1)

            # Try multiple selectors for job description
            selectors = [
                '.jobs-description__content',
                '.show-more-less-html__markup',
                '.description__text'
            ]

            description = None
            for selector in selectors:
                try:
                    elem = self.page.query_selector(selector)
                    if elem:
                        description = elem.inner_text()
                        break
                except:
                    continue

            if description:
                print(f"    ✓ Scraped {len(description)} characters")
                return description
            else:
                print(f"    ⚠️ No description found")
                return None

        except Exception as e:
            print(f"    ❌ Failed to scrape: {e}")
            return None


class JobDeduplicator:
    """Checks for duplicate jobs against existing applications."""

    def __init__(self, applications_dir: Path):
        """
        Initialize deduplicator.

        Args:
            applications_dir: Path to applications/ folder
        """
        self.applications_dir = applications_dir
        self.existing_jobs = self._load_existing_jobs()

    def _load_existing_jobs(self) -> List[Dict[str, str]]:
        """Load all existing applications."""
        existing = []

        if not self.applications_dir.exists():
            return existing

        for app_folder in self.applications_dir.iterdir():
            if app_folder.is_dir():
                # Extract company and role from folder name
                # Format: YYYY-MM-CompanyName-RoleTitle
                parts = app_folder.name.split('-', 3)
                if len(parts) >= 4:
                    company = parts[2]
                    role = parts[3]
                    existing.append({
                        'company': company.lower(),
                        'role': role.lower(),
                        'folder': app_folder.name
                    })

        return existing

    def is_duplicate(self, company: str, title: str) -> Optional[str]:
        """
        Check if job already exists in applications.

        Args:
            company: Company name
            title: Job title

        Returns:
            Existing folder name if duplicate, None otherwise
        """
        company_clean = company.lower().replace(' ', '')
        title_clean = title.lower().replace(' ', '')

        for existing in self.existing_jobs:
            existing_company = existing['company'].replace(' ', '')
            existing_role = existing['role'].replace(' ', '')

            # Check for close match (allows for slight variations)
            if (existing_company in company_clean or company_clean in existing_company):
                if (existing_role in title_clean or title_clean in existing_role):
                    return existing['folder']

        return None


def sanitize_filename(text: str) -> str:
    """Convert text to safe filename."""
    # Remove invalid characters
    text = re.sub(r'[<>:"/\\|?*]', '', text)
    # Replace spaces and special chars with hyphens
    text = re.sub(r'[\s\-]+', '-', text)
    # Remove leading/trailing hyphens
    text = text.strip('-')
    # Limit length
    return text[:100]


def save_to_staging(
    job: Dict[str, str],
    description: str,
    staging_dir: Path,
    batch_name: str
):
    """
    Save job description to staging folder.

    Args:
        job: Job metadata dictionary
        description: Job description text
        staging_dir: Path to staging directory
        batch_name: Name of this discovery batch
    """
    # Create batch folder
    batch_folder = staging_dir / batch_name
    batch_folder.mkdir(parents=True, exist_ok=True)

    # Create job folder
    company_safe = sanitize_filename(job['company'])
    title_safe = sanitize_filename(job['title'])
    job_folder = batch_folder / f"{company_safe}-{title_safe}"
    job_folder.mkdir(parents=True, exist_ok=True)

    # Save job description
    desc_file = job_folder / "job-description.md"
    with open(desc_file, 'w', encoding='utf-8') as f:
        f.write(f"# {job['title']} @ {job['company']}\n\n")
        f.write(f"**Location:** {job['location']}\n")
        f.write(f"**Source:** {job['url']}\n\n")
        f.write("---\n\n")
        f.write(description)

    print(f"    ✅ Saved to: {job_folder.name}/")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='LinkedIn Job Discovery Automation')
    parser.add_argument('--keywords', type=str, help='Job search keywords')
    parser.add_argument('--location', type=str, help='Job location')
    parser.add_argument('--date', type=str, default='past_week',
                       choices=['past_24h', 'past_week', 'past_month', 'any_time'],
                       help='Date posted filter')
    parser.add_argument('--auto', action='store_true',
                       help='Use career-preferences.md for search criteria')
    parser.add_argument('--headless', action='store_true',
                       help='Run browser in headless mode')
    parser.add_argument('--no-persist', action='store_true',
                       help='Don\'t save browser session (will need to log in each time)')

    args = parser.parse_args()

    # Setup paths
    project_root = Path(__file__).parent.parent
    staging_dir = project_root / 'staging'
    applications_dir = project_root / 'applications'
    browser_data_dir = project_root / '.browser_data' if not args.no_persist else None

    # Create browser data directory if using persistent context
    if browser_data_dir:
        browser_data_dir.mkdir(exist_ok=True)

    # Create batch name
    batch_name = datetime.now().strftime('%Y-%m-%d-discovery-batch')

    print("=" * 80)
    print("🤖 LinkedIn Job Discovery Automation")
    print("=" * 80)

    # Define searches (TODO: Load from career-preferences.md in --auto mode)
    searches = []

    if args.auto:
        # TODO: Parse career-preferences.md for keywords and locations
        print("\n⚠️ --auto mode not yet implemented, using defaults")
        searches = [
            {
                'keywords': 'Director Product Data Platform',
                'location': 'London, United Kingdom',
                'experience_level': ['director']
            },
            {
                'keywords': 'Head of Product Growth',
                'location': 'London, United Kingdom',
                'experience_level': ['director']
            }
        ]
    elif args.keywords and args.location:
        searches = [{
            'keywords': args.keywords,
            'location': args.location,
            'experience_level': None
        }]
    else:
        # Interactive mode - use defaults
        searches = [
            {
                'keywords': 'Director Product Data Platform',
                'location': 'London, United Kingdom',
                'experience_level': ['director']
            }
        ]

    # Initialize searcher and deduplicator
    searcher = LinkedInJobSearcher(
        headless=args.headless,
        slow_mo=100,
        user_data_dir=str(browser_data_dir) if browser_data_dir else None
    )
    deduplicator = JobDeduplicator(applications_dir)

    try:
        all_jobs = []

        # Perform searches
        for search in searches:
            jobs = searcher.search(
                keywords=search['keywords'],
                location=search['location'],
                date_posted=args.date,
                experience_level=search.get('experience_level')
            )
            all_jobs.extend(jobs)

        # Deduplicate
        print(f"\n📊 Total jobs discovered: {len(all_jobs)}")

        new_jobs = []
        duplicates = []

        for job in all_jobs:
            existing = deduplicator.is_duplicate(job['company'], job['title'])
            if existing:
                duplicates.append({**job, 'existing_folder': existing})
            else:
                new_jobs.append(job)

        print(f"✅ New jobs: {len(new_jobs)}")
        print(f"⏭️  Duplicates (already tracked): {len(duplicates)}")

        if duplicates:
            print("\n  Skipped duplicates:")
            for dup in duplicates[:5]:  # Show first 5
                print(f"    - {dup['company']} - {dup['title']} (exists: {dup['existing_folder']})")
            if len(duplicates) > 5:
                print(f"    ... and {len(duplicates) - 5} more")

        # Scrape full descriptions for new jobs
        if new_jobs:
            print(f"\n📥 Scraping full job descriptions for {len(new_jobs)} new jobs...")

            scraped_count = 0
            for i, job in enumerate(new_jobs, 1):
                print(f"\n  [{i}/{len(new_jobs)}] {job['company']} - {job['title']}")

                description = searcher.scrape_job_description(job['url'])

                if description:
                    save_to_staging(job, description, staging_dir, batch_name)
                    scraped_count += 1

                    # Rate limiting - pause between requests
                    if i < len(new_jobs):
                        time.sleep(2)

            print(f"\n✅ Successfully scraped {scraped_count}/{len(new_jobs)} jobs")
            print(f"📁 Saved to: {staging_dir / batch_name}")

            # Save summary
            summary_file = staging_dir / batch_name / "DISCOVERY-SUMMARY.json"
            summary = {
                'batch_name': batch_name,
                'date': datetime.now().isoformat(),
                'searches': searches,
                'total_discovered': len(all_jobs),
                'new_jobs': len(new_jobs),
                'duplicates': len(duplicates),
                'scraped': scraped_count,
                'jobs': new_jobs
            }

            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2)

            print(f"📄 Summary saved: {summary_file.name}")

            # Next steps
            print("\n" + "=" * 80)
            print("🎯 Next Steps:")
            print("=" * 80)
            print(f"1. Run bulk analysis: python scripts/bulk_analyze.py {staging_dir / batch_name}")
            print(f"2. Review results in: {staging_dir / batch_name}/BULK-ANALYSIS-SUMMARY.md")
            print(f"3. Apply to 8+ fit score roles using /generate-cv and /generate-cover-letter")

        else:
            print("\n✨ No new jobs found (all are duplicates)")

    finally:
        searcher.close_browser()
        print("\n✅ Done!")


if __name__ == '__main__':
    main()
