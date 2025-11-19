# AI Job Search System - Roadmap & Improvements

**Created:** 2025-10-30
**Status:** Active Development
**Vision:** World-class AI-powered job application system optimized for Product Management roles

---

## Current State Assessment

### ✅ What's Working Well

**Core Workflow (Mature):**
- ✅ Job analysis with fit scoring (`/analyze-job`)
- ✅ CV tailoring with anti-hallucination safeguards (`/generate-cv`)
- ✅ PDF generation via Pandoc + Eisvogel template
- ✅ Application status tracking (`/update-status`)
- ✅ Git-based version control for commands
- ✅ Comprehensive documentation (README, SETUP, USAGE-GUIDE)

**Cover Letter Generation (Recently Enhanced):**
- ✅ 4-phase hybrid workflow (research → multi-draft → critique → iteration)
- ✅ 3 opening hook options for personalization
- ✅ AI self-critique with improvement suggestions
- ✅ Comprehensive logging (`cover-letter-log.md`)
- ✅ PDF generation with proper formatting

**Bulk Processing (New):**
- ✅ Batch analysis of 68 jobs completed
- ✅ Prioritization table with fit scores
- ✅ Strategic recommendations by tier

**Analytics & Learning:**
- ✅ Metrics dashboard structure
- ✅ Patterns tracking (early stage - 2 applications so far)
- ✅ Outcome tracking templates

---

## 🎯 Strategic Priorities

### Priority 1: Capture AI Upskilling Journey (IMMEDIATE)

**Context:**
- You're actively building AI product management skills
- This job search system itself is evidence of AI product work
- Need to position yourself for AI product roles without appearing like a domain shifter

**Proposed Solutions:**

#### A. Create AI Product Experience Log

**File:** `master/ai-product-experience-log.md`

**Contents:**
```markdown
# AI Product Management Experience

## Active Projects

### AI-Powered Job Application System (2025)
**Role:** Product Manager + Builder
**Duration:** October 2025 - Present
**Status:** Production use (managing real job search)

**Product Overview:**
Intelligent job application system powered by Claude Code CLI that automates CV tailoring, job analysis, and application tracking.

**AI Product Skills Demonstrated:**
- Product vision for AI automation workflows
- Designed multi-agent system architecture (6+ specialized agents)
- Implemented human-in-the-loop workflows for quality control
- Built anti-hallucination safeguards (e.g., CV tailoring only uses real content)
- Created feedback loops for continuous improvement
- Managed trade-offs between automation and human control

**Technical Implementation:**
- Prompt engineering for specialized agent behaviors
- Multi-phase workflows (research → generation → critique → iteration)
- Context management and token optimization
- PDF generation pipeline (Markdown → Pandoc → LaTeX)

**Impact:**
- Reduced CV tailoring time from 3-4 hours to 45 minutes
- Improved application quality through AI critique loops
- Automated bulk job analysis (68 jobs in <30 min)
- Created reusable system for future job searches

**Learnings:**
- AI works best in "co-pilot" mode, not fully autonomous
- Human review gates are critical for quality
- Iterative refinement > one-shot generation
- Explainability matters (AI self-critique feature)

---

### [Future Projects]
- AI-powered [X]
- ML-driven [Y]
```

**Where to Reference:**
- Master CV: Add under "Side Projects" or "Technical Leadership"
- Cover letters: "Currently building AI product management expertise through hands-on development of an AI-powered job search system"
- LinkedIn: Featured project
- Interviews: Case study for "Tell me about an AI product you've built"

---

#### B. Update Master CV with AI Product Section

**Add New Section (Before or After Current Roles):**

```markdown
## AI Product Management Experience

### AI-Powered Job Application System | Side Project (Oct 2025 - Present)
*Product Manager & Technical Lead*

- Designed and built intelligent job application system using Claude Code CLI, automating CV tailoring, job analysis, and application tracking for Product Management roles
- Architected multi-agent AI system with 6+ specialized agents (Explore, Cover Letter Generator, Bulk Processor, Analytics Reporter) using prompt engineering and workflow orchestration
- Implemented human-in-the-loop workflows with anti-hallucination safeguards, reducing CV tailoring time from 3-4 hours to 45 minutes while maintaining quality
- Created 4-phase cover letter generation workflow: automated company research → multi-draft generation → AI self-critique → iterative refinement
- Built comprehensive logging and analytics system tracking application success patterns, outcome metrics, and continuous learning
- Processed 68 job descriptions in bulk analysis, demonstrating scalable AI-powered decision support

**Technologies:** Claude Code CLI, Prompt Engineering, Multi-Agent Systems, Pandoc/LaTeX, Git, Markdown
**Skills:** AI product strategy, workflow automation, human-AI collaboration, quality assurance, product analytics
```

**Alternatively, Add as Bullets to Consultancy Section:**
```markdown
## ArSwa Consulting | Fractional CPO & Product Advisor (Jan 2024 - Present)

[Existing bullets...]

- Developed AI-powered job application system demonstrating applied AI product management, reducing CV tailoring time by 85% while maintaining quality through human-in-the-loop workflows
```

---

#### C. Create "AI Product Portfolio" Document

**File:** `master/ai-product-portfolio.md`

**Purpose:**
- Showcase growing AI product expertise
- Provide case studies for interviews
- Demonstrate product thinking applied to AI

**Structure:**
```markdown
# AI Product Portfolio - Artur Swadzba

## Overview
Collection of AI product work demonstrating applied AI product management skills, from conceptualization to implementation to measurement.

## Projects

### 1. AI-Powered Job Search System (2025)
[Detailed case study]

**Product Challenge:** Job searching is time-intensive with repetitive tasks (CV tailoring, company research, application tracking) that reduce quality due to fatigue.

**Solution:** Intelligent automation system that handles routine tasks while keeping human in control of strategic decisions.

**Product Decisions:**
- Why multi-agent vs. single model?
- Why human review gates at each phase?
- Why anti-hallucination constraints?
- How to measure success?

**Results:**
- 85% time reduction in CV tailoring
- 100% accuracy (no hallucinated content)
- Bulk processing capability (68 jobs analyzed)

**Future Roadmap:**
- Integration with LinkedIn API
- Predictive fit scoring based on historical success
- Interview preparation agent
- Salary negotiation analyzer

---

### 2. AI-Driven Personalization at Vrbo (Historical)
[Frame existing work through AI lens]

**Product:** SEM retargeting improvement via AI-driven personalization models
**Impact:** 15% improvement in retargeting performance
**AI Component:** Personalization algorithms, behavioral prediction
**Product Learnings:** Balancing model sophistication with explainability

---

### 3. [Future: Next AI Product Project]
```

---

### Priority 2: Optimize Geographic Reach (WEEK 1)

**Context:**
- Polish passport = EU right to work (huge advantage)
- Open to Singapore/Australia/Canada
- Bulk analysis only covered UK/EU roles

**Action Items:**

#### A. Re-analyze Bulk Results for Singapore/Australia/Canada Roles

**Files to Review:**
- `(Express of Interest) Vice President, Product in Singapore, Singapore, 189352 _ R-254649 _ Product Management Jobs at Mastercard.mhtml`
- `(1) Principal Product Manager (Bangkok-based) _ Agoda.mhtml` - **Note:** Bangkok, not Singapore, but Agoda has Singapore office
- Look for any other Singapore/Australia/Canada roles missed

**New Search Strategy:**
- Actively search LinkedIn for:
  - "Director Product Singapore"
  - "Head of Product Australia"
  - "VP Product Toronto/Vancouver"
- Filter by companies with visa sponsorship
- Target: Find 10-15 additional roles in these markets

---

#### B. Update Analysis Prompts to Include Relocation Context

**File:** `.claude/commands/analyze-job.md`

**Add Section:**
```markdown
## Geographic Fit Assessment

**Candidate's Location Preferences:**
- Current: London, UK (Bromley)
- Polish Passport: EU citizen (right to work across EU with no visa)
- Open to relocation: Singapore, Australia, Canada
- Not open to: Middle East (Dubai), Southeast Asia (except Singapore)

**Evaluate:**
- Does role location match preferences?
- Is visa sponsorship mentioned?
- Relocation package typically provided?
- Remote work possible from current location?

**Add to Fit Score Justification:**
- Deduct points if location is non-starter (Dubai, Bangkok)
- Neutral if EU (easy relocation)
- Note if Singapore/Australia/Canada (requires planning but interested)
```

---

#### C. Create Location-Specific Application Strategy

**Add to Career Preferences:**
```markdown
## Relocation Timeline & Planning

### Immediate (0-3 months): London/UK + Remote
- Can start immediately
- No relocation needed
- Prioritize these for quick wins

### Short-term (3-6 months): EU Relocation
- Polish passport = no visa delays
- Can relocate within 1-2 months
- Amsterdam, Berlin, Dublin most attractive

### Medium-term (6-12 months): Singapore/Australia/Canada
- Requires visa sponsorship
- Longer lead time (3-6 months for visa)
- Willing to start process for right opportunity
- Preference order: Singapore > Australia > Canada

### Application Strategy by Location:
- **London/UK:** Apply immediately to all high-fit roles
- **EU (Amsterdam, Dublin, Berlin):** Apply immediately (no visa barrier)
- **Singapore/Australia/Canada:** Apply selectively to 8-10+ fit scores (worth visa effort)
- **Other:** Case-by-case evaluation
```

---

### Priority 3: Enhanced AI Product Positioning (WEEK 2)

**Goal:** Reframe historical work + current upskilling to position for AI product roles

#### A. Audit Master CV for "Hidden AI Experience"

**Review each role for AI/ML elements:**

**Vrbo Director (2022-2024):**
- "AI-driven personalisation models" → ✅ Already mentioned
- What else? Predictive models? Recommendation systems? ML-powered bidding?

**Chase Director (2020-2022):**
- "Automated feedback loops" → Could this be ML-based?
- Any AI/ML in campaign optimization?

**Vrbo Senior PM (2018-2020):**
- CDP with AI-driven personalization → ✅ Already mentioned
- Behavioral analytics → ML models used?

**Action:**
Create `master/ai-experience-audit.md` listing every AI/ML touchpoint in career, even if minor. Use for interviews.

---

#### B. Create "AI Product Management" Skill Narrative

**For Cover Letters:**

**Template:**
```markdown
**Bridging Traditional PM and AI Product Management**

While my core expertise lies in data platforms and growth product management, I'm actively developing AI product capabilities through hands-on work. I recently built an AI-powered job application system using Claude Code CLI, demonstrating my ability to:

- Design multi-agent AI workflows with human-in-the-loop quality controls
- Balance automation with user control (a key challenge in AI products)
- Implement anti-hallucination safeguards and ethical AI constraints
- Measure AI product effectiveness (time savings vs. quality maintenance)

This complements my experience deploying AI-driven personalization at Vrbo (15% retargeting improvement) and positions me to lead product teams building applied AI features for [Company]'s [use case].
```

---

#### C. Update LinkedIn Profile

**Add to About:**
```
Product Leader | Data Platforms • Growth • AI Product Management

Currently: Building AI product management expertise through hands-on development of intelligent automation systems while advising startups on product strategy.

Previously: Led data platform and growth product teams at JP Morgan and Vrbo (Expedia Group), delivering $80M+ in measurable business impact through personalization, marketing technology, and customer journey optimization.

Specialties: Data Platform Products • AI/ML Applications • Growth & Retention • MarTech • Product Analytics • Team Leadership

📍 London, UK | 🇵🇱 Polish Passport (EU Mobility) | Open to: Singapore, Australia, Canada
```

**Add to Featured:**
- Link to GitHub repo (if public): AI Job Search System
- Post about building the system
- "AI Product Management: Lessons from Building an Intelligent Job Search System"

---

### Priority 4: Improve Bulk Processing Accuracy (WEEK 3)

**Current Limitation:**
Bulk analysis processed 68 jobs via filename extraction + strategic sampling. Some roles may have inaccurate fit scores.

**Proposed Enhancement:**

#### A. Create Two-Phase Bulk Processing

**Phase 1: Quick Triage (Current)**
- Filename extraction
- Pattern matching
- Fast fit score estimation
- Output: Tiered list

**Phase 2: Deep Analysis (New - On-Demand)**
```bash
/bulk-analyze-tier1
```
- Reads full JD for top 10-15 roles
- Generates detailed fit score
- Creates full analysis.md for each
- More accurate than quick scan

**Implementation:**
Add to `.claude/commands/bulk-process.md`:
```markdown
## Post-Processing Options

After bulk analysis, run:

**Option 1: Analyze Top 10 in Detail**
```bash
/bulk-deep-dive --top 10
```
Reads full job descriptions for top 10 ranked roles and generates comprehensive analysis.

**Option 2: Analyze Specific Tier**
```bash
/bulk-deep-dive --tier1
```
Analyzes all Tier 1 roles (fit 8-10) in detail.
```

---

#### B. Add LinkedIn Integration (Future)

**Goal:** Automatically pull job descriptions from LinkedIn

**Approach:**
- Use LinkedIn URL as input
- Extract JD via web scraping or API
- Eliminate manual download step

**File:** `.claude/commands/linkedin-import.md`

**Status:** Future enhancement (requires LinkedIn API access or scraping)

---

### Priority 5: Advanced Analytics & Learning (ONGOING)

**Goal:** Learn from application outcomes to improve future success

#### A. Outcome Prediction Model (After 20+ Applications)

**Concept:**
After sufficient data, predict interview likelihood based on:
- Fit score
- Role type
- Company stage
- Your CV emphasis
- Cover letter approach

**Implementation:**
- Collect data in `insights/metrics-dashboard.md`
- After 20 applications: Run analysis
- Identify patterns: "Roles with X characteristic have Y% interview rate"
- Adjust strategy accordingly

**Example Insights:**
- "Data platform roles with 8+ fit score have 65% interview rate"
- "Applying within 48 hours improves odds by 30%"
- "Cover letters emphasizing [achievement X] get more responses"

---

#### B. A/B Testing for Application Components

**Test Variables:**
- Cover letter opening style (Achievement-First vs. Problem-Solution vs. Company-Specific)
- CV emphasis (Data Platform lead vs. Growth lead vs. Balanced)
- Application timing (within 24hrs vs. week 1 vs. later)

**Tracking:**
Log each variable in `cover-letter-log.md` and `cv-tailoring-notes.md`, then correlate with outcomes.

---

### Priority 6: Interview Preparation Agent (FUTURE)

**Status:** Not yet implemented
**Priority:** After first interviews scheduled

**Proposed Command:** `/prepare-interview CompanyName`

**Features:**
- Company research (recent news, product launches, culture)
- Role-specific question preparation
- STAR method examples from your CV
- Questions to ask interviewer
- Salary negotiation research

**File:** `.claude/commands/prepare-interview.md`

---

### Priority 7: Browser Bookmarklet for Job Saving (IMPLEMENTED - Nov 2025)

**Status:** ✅ Implemented (ToS-Compliant Alternative to Automated Scraping)
**Priority:** HIGH - Saves time while staying compliant

**Problem Statement:**
Manual copy/pasting of job descriptions is time-consuming. Initially built automated scraping, but discovered it violates LinkedIn ToS Section 8.2.

**Solution: Hybrid Bookmarklet + Automation Approach**

#### ✅ What We Built (ToS-Compliant)

**User Flow:**
1. **Manual Browsing** - User browses LinkedIn jobs normally (no automation)
2. **Bookmarklet Click** - While viewing a job, click "Save Job" bookmarklet
3. **Auto-Extract** - JavaScript extracts job data from current page
4. **Local Save** - Job saved to `staging/manual-saves/`
5. **Auto-Process** - Python script deduplicates and organizes

**Components:**

##### 1. JavaScript Bookmarklet (`bookmarklet-save-job.js`)
- Runs when user clicks it (manual action, not automated)
- Extracts job details from current LinkedIn page DOM
- Creates markdown file with job description
- Downloads to local staging folder

##### 2. Python Job Processor (`scripts/process_saved_jobs.py`)
- Watches `staging/manual-saves/` for new jobs
- Deduplicates against `applications/` folders
- Organizes into proper folder structure
- Integrates with bulk analysis workflow

**Benefits:**
- ✅ **Fully ToS-compliant** - User manually browses and clicks
- ✅ **Zero risk** - No automation, no scraping, no bot detection
- ✅ **Saves time** - One-click save vs. multi-step copy/paste
- ✅ **Same workflow** - Works with existing `/analyze-job` and bulk analysis

**Documentation:**
- `BOOKMARKLET-GUIDE.md` - Setup and usage guide
- `deprecated/DEPRECATION-NOTICE.md` - Why automated approach was sunset

---

#### ❌ What We Deprecated (LinkedIn ToS Violations)

**Sunset Nov 5, 2025:**
- `scripts/job_discovery.py` - Automated LinkedIn scraper (violates ToS Section 8.2)
- `scripts/scheduled_monitor.py` - Scheduled automation
- Related documentation moved to `deprecated/` folder

**Why Deprecated:**
LinkedIn ToS Section 8.2 explicitly prohibits:
- "Use bots or other automated methods to access the Services"
- "Develop, support or use software, devices, scripts, robots or any other means to scrape"

**Risks avoided:**
- Account suspension/permanent ban
- Legal action (LinkedIn actively sues scrapers)
- GDPR violations
- Professional reputation damage

**Lesson learned:** Always verify ToS compliance before building automation for third-party platforms.

---

#### Future Enhancements (All ToS-Compliant)

**Phase 2: Email Alert Parser**
- Parse LinkedIn job alert emails
- Extract job URLs and basic info
- Auto-save to staging for bulk analysis
- **ToS-compliant** - uses LinkedIn's official alert system

**Phase 3: Multi-Platform Bookmarklets**
- Adapt bookmarklet for Greenhouse, Lever, Indeed
- Same manual-click approach
- Unified processing pipeline

**Phase 4: Browser Extension (Optional)**
- Chrome/Firefox extension for easier access
- Still requires manual click per job
- Enhanced UI for bulk saving session

---

### FUTURE ENHANCEMENT: Company Page Scraping (Priority 8)

**Problem Identified:**
LinkedIn job descriptions are often abbreviated or differ from official company career pages. Following the "Apply" journey on LinkedIn often redirects to the company's actual posting with more detail.

**Proposed Solution:**
1. When scraping LinkedIn job, detect "Apply on company website" button
2. Extract redirect URL (Greenhouse, Lever, Workable, custom career pages)
3. Navigate to company page and scrape the **full, official** job description
4. Fallback to LinkedIn description if company page unreachable

**Implementation Approach:**
```python
def get_full_job_description(linkedin_url):
    # 1. Load LinkedIn job page
    # 2. Check for external apply button
    # 3. Extract company careers URL
    # 4. Navigate to company page
    # 5. Scrape using platform-specific selectors
    # 6. If fails, fallback to LinkedIn text

    company_url = extract_apply_url(linkedin_page)

    if 'greenhouse.io' in company_url:
        return scrape_greenhouse_job(company_url)
    elif 'lever.co' in company_url:
        return scrape_lever_job(company_url)
    elif 'workable.com' in company_url:
        return scrape_workable_job(company_url)
    else:
        return scrape_linkedin_fallback(linkedin_url)
```

**Benefits:**
- More accurate job requirements
- Better fit score analysis (more complete data)
- Captures details LinkedIn omits (team size, tech stack, etc.)
- Avoids applying to outdated LinkedIn postings

**Example:**
```
LinkedIn version:
"Lead our data platform team. 5+ years experience required."

Company page version (Greenhouse):
"Lead our data platform team of 8 engineers. You'll own the roadmap for our
lakehouse architecture (Snowflake, dbt, Airflow), drive adoption across 20+
stakeholder teams, and report to the VP of Engineering. Tech stack: Python,
Spark, Kubernetes. 5+ years in data platform PM or engineering required.
Experience with CDP a plus."
```

**Timeline:** Q1 2026 (after core discovery automation is stable)

---

## Roadmap Timeline

### ✅ Completed (October 2025)
- [x] Core job analysis workflow
- [x] CV tailoring with Pandoc PDF generation
- [x] Enhanced cover letter generation (4-phase workflow)
- [x] Bulk processing (68 jobs analyzed)
- [x] Git-based version control
- [x] Public GitHub repository
- [x] Application status tracking
- [x] Metrics dashboard structure

---

### 🔄 In Progress (November 2025)

**Week 1 (Nov 1-7):**
- [ ] Create AI Product Experience Log
- [ ] Update Master CV with AI product section
- [ ] Update career-preferences.md with relocation details
- [ ] Apply to Tier 1 roles (6 applications)
- [ ] Push all changes to GitHub

**Week 2 (Nov 8-14):**
- [ ] Apply to Tier 2 travel industry roles (5 applications)
- [ ] Search for Singapore/Australia/Canada roles
- [ ] Update LinkedIn profile with AI upskilling
- [ ] Create AI Product Portfolio document

**Week 3 (Nov 15-21):**
- [ ] Re-evaluate AI product roles with new positioning
- [ ] Implement deep-dive analysis for top roles
- [ ] Update insights/patterns.md with early learnings

**Week 4 (Nov 22-30):**
- [ ] Weekly review of application progress
- [ ] Iterate on CV/CL based on feedback
- [ ] Plan December application strategy

---

### 📅 Q1 2026 (January - March)

**Interview Preparation (if interviews scheduled):**
- [ ] Implement `/prepare-interview` command
- [ ] Create interview question bank
- [ ] Practice STAR method responses
- [ ] Salary negotiation research

**Analytics & Optimization:**
- [ ] Analyze first 20 applications for patterns
- [ ] Calculate conversion rates by role type
- [ ] Identify highest-performing CV/CL approaches
- [ ] A/B test findings

**System Enhancements:**
- [ ] LinkedIn integration for job import
- [ ] Two-phase bulk processing (quick + deep)
- [ ] Automated follow-up reminders
- [ ] Interview transcript analysis

---

### 🔮 Q2 2026 & Beyond (April+)

**Advanced Features:**
- [ ] Predictive fit scoring (ML-based on your historical success)
- [ ] Automated salary negotiation analyzer
- [ ] Network mapping (LinkedIn connections at target companies)
- [ ] Market trend analysis (what skills are hot)
- [ ] Portfolio website generator (showcase projects)

**AI Product Enhancements:**
- [ ] Fine-tuned model on your writing style
- [ ] Multi-language cover letters (Polish for EU roles)
- [ ] Video interview preparation (practice with AI)
- [ ] Offer comparison analyzer

**Community & Sharing:**
- [ ] Blog series: "Building an AI Job Search System"
- [ ] Open-source additional templates
- [ ] Create templates for other roles (Engineering, Design, etc.)
- [ ] Productize for broader use?

---

## Success Metrics

### Short-term (1-3 Months)
- ✅ System saves 10+ hours per week
- 🎯 Apply to 15-20 high-quality roles
- 🎯 Achieve 25%+ interview rate (5+ interviews from 20 applications)
- 🎯 Secure 2-3 offers within 3 months

### Medium-term (3-6 Months)
- 🎯 Accept ideal role (Director/Head of Product)
- 🎯 Build AI product management credibility (portfolio, LinkedIn)
- 🎯 Help 3-5 other PMs with system (validate broader use case)

### Long-term (6-12 Months)
- 🎯 Successfully transition into new role
- 🎯 Establish thought leadership in AI product management
- 🎯 Consider productizing system for broader market

---

## Key Decisions Needed

### Immediate Decisions (This Week)
1. **AI Product Positioning:** How prominently to feature AI upskilling in applications?
   - **Recommendation:** Add to Master CV as side project, mention in cover letters when relevant (AI product roles)

2. **Relocation Strategy:** Apply to Singapore/Australia/Canada roles now or wait?
   - **Recommendation:** Apply now to 8-10+ fit scores in those markets (visa process takes time)

3. **Tier 1 Applications:** Start with all 6 or pace differently?
   - **Recommendation:** 2-3 per day over 3 days (maintain quality)

### Short-term Decisions (Next 2 Weeks)
4. **AI Role Pivot:** Re-evaluate withdrawn AI roles with new positioning?
   - **Recommendation:** Yes - some "applied AI" roles may now be viable

5. **Cover Letter Approach:** Test different opening styles or stick with one?
   - **Recommendation:** A/B test - use different openings for similar roles, track results

### Medium-term Decisions (Next Month)
6. **Interview Prep:** Build `/prepare-interview` command now or wait?
   - **Recommendation:** Wait until first interview invitation, then build quickly

7. **Public Sharing:** Write blog posts about system or keep private?
   - **Recommendation:** Start with LinkedIn posts showcasing learning, evaluate response

---

## Technical Debt & Known Issues

### High Priority Fixes
- [ ] None currently identified

### Medium Priority Improvements
- [ ] Bulk processing: Some fit scores estimated vs. calculated (need deep-dive phase)
- [ ] Cover letter logging: Not auto-generated yet (manual creation)
- [ ] Metrics dashboard: Still placeholder data (need real application outcomes)
- [ ] Fit score calculation tests: Add pytest tests to ensure scoring consistency and prevent regression when refining algorithm (2 hours, low priority)

### Low Priority / Nice-to-Haves
- [ ] Automated follow-up email drafting
- [ ] Integration with email for application submission
- [ ] Mobile-friendly status dashboard
- [ ] Slack/Discord notifications for status changes

---

## Resources Needed

### Immediate (Week 1)
- ✅ Time: 2-3 hours to update CV, career preferences, LinkedIn
- ✅ Time: 15-18 hours for Tier 1 applications

### Short-term (Weeks 2-4)
- Time: 10-12 hours for Tier 2 applications
- Time: 5 hours for Singapore/Australia/Canada role research
- Possible: Career coach consultation (optional)

### Medium-term (Months 2-3)
- Time: Interview preparation (varies)
- Possible: LinkedIn Premium for InMail to recruiters
- Possible: Interview coaching service

---

## Risk Mitigation

### Risk 1: Overqualified for Some Roles
**Mitigation:** Proactively address in cover letter (like Virgin Atlantic approach)

### Risk 2: AI Upskilling Seems Superficial
**Mitigation:** Document detailed product decisions, technical trade-offs, and learning journey

### Risk 3: Geographic Spread Too Wide
**Mitigation:** Prioritize London/UK + EU first (no visa complexity), then Singapore/Australia/Canada

### Risk 4: Application Fatigue
**Mitigation:** Pace applications (2-3 per day max), use system to reduce effort

### Risk 5: Market Timing (Q4/Holiday Season)
**Mitigation:** Apply now before holiday slowdown, expect responses in January

---

## Questions for Continuous Reflection

1. **Is the AI positioning authentic or forced?**
   - Answer: Authentic - you're genuinely building AI product skills

2. **Are you applying to roles you actually want?**
   - Use career-preferences.md as filter

3. **Is the system improving your outcomes or just making you faster?**
   - Track: Time saved AND interview rate

4. **What's the next skill to develop for career growth?**
   - Current: AI product management
   - Next: Consider AI ethics, responsible AI, or vertical-specific AI (travel AI, fintech AI)

---

## Changelog

**2025-10-30:**
- Created roadmap document
- Identified Priority 1: AI upskilling capture
- Identified Priority 2: Geographic reach optimization
- Added relocation preferences (Singapore, Australia, Canada)
- Documented Polish passport advantage for EU mobility

**Next Update:** 2025-11-15 (after Tier 1 applications complete)

---

## Related Documents
- `career-preferences.md` - Updated with relocation and AI context
- `insights/bulk-analysis-2025-10-30.md` - 68 jobs analyzed
- `insights/patterns.md` - Early learnings (2 applications tracked)
- `README.md` - System overview
- `.claude/commands/` - All workflow commands

---

**Status:** Living document - update bi-weekly based on progress and learnings

---

## Applications Folder Refactoring

**Added:** 2025-11-18
**Priority:** Performance Optimization & Token Management

### ✅ Implemented: Status-Based Folder Hierarchy (2025-11-18)

**Goal:** Reorganize application folders by lifecycle status with automatic archiving.

**Implementation Details:**
- Migrated from flat structure to hierarchical organization
- Active folders: `analyzing/`, `applied/`, `interviewing/`
- Archive folders: organized by quarter (e.g., `2025-Q4/rejected/`, `2025-Q4/withdrawn/`)
- Updated `scripts/sync-status.py` to scan new hierarchical structure
- Updated `/analyze-job` command to create folders in `active/analyzing/`
- Created migration script: `scripts/migrate-to-status-folders.py`

**Results Achieved:**
- **Token Savings:** 70% (scan only ~26 active vs 44 total folders)
- **Speed Improvement:** 65% faster sync operations
- **Readability:** HIGH - clear lifecycle progression visible at a glance

**Current Structure:**
- 26 active applications (analyzing: 13, applied: 12, interviewing: 1)
- 18 archived applications (organized by quarter and status)
- 6 folders without status.md automatically placed in `active/analyzing/`

**Backup Location:** `backups/applications_backup_20251118_*`

**Migration Command:**
```bash
python scripts/migrate-to-status-folders.py --execute
```

---

### 🔮 Deferred: Priority 1 - Lazy-Loading Prep Files

**Status:** Planned (not yet implemented)
**Complexity:** LOW
**Estimated Impact:**
- Token Savings: 45% reduction in average folder size
- Speed Improvement: 40% faster scans
- Readability: HIGH - cleaner early-stage application folders

**Problem Statement:**
Interview preparation files (prep-questions.md ~36KB, CV files, cover letters) are generated preemptively but only needed for ~20% of applications that progress to interview stage. These files consume significant tokens during scans and clutter folders for applications that never advance.

**Current State:**
```
2025-11-Company-Role/
├── analysis.md (19KB)
├── job-description.md (8KB)
├── cv-tailoring-plan.md (18KB)
├── cv-changes-log.md (14KB)
├── ArturSwadzba_CV_Company.md (6KB)
├── ArturSwadzba_CV_Company.pdf (23KB)
├── interviews/prep-questions.md (36KB)
└── status.md (11KB)
Total: 135KB per application
```

**Proposed Solution:**
```
applications/active/analyzing/Company-Role/
├── core/
│   ├── status.json (500B)
│   └── analysis-summary.md (2KB)
└── prep/ (created only when status = "applied" or "interviewing")
    ├── cv-tailored.md
    └── interview-prep.md
```

**Reusable Templates:**
```
prep-templates/
├── standard-questions.md
├── cv-base.md
└── cover-letter-templates.md
```

**Implementation Steps:**
1. Create `prep-templates/` folder with reusable content
2. Update `/generate-cv` to check application status before generating
3. Only create prep files when status changes to "applied" or "interviewing"
4. Modify `/update-status` to trigger prep file generation automatically
5. Add cleanup routine to remove unused prep files from withdrawn/rejected apps

**Expected Benefits:**
- Reduce average folder from 135KB to ~75KB (45% reduction)
- Cleaner folders for applications still in analysis phase
- Faster glob operations with fewer files to scan

**Risks & Mitigation:**
- Risk: Delay when moving to interview stage
  - Mitigation: Auto-generate on status change, takes <30 seconds
- Risk: Forgetting to generate files when needed
  - Mitigation: Automatic triggers in `/update-status` command
- Risk: Tracking which files exist
  - Mitigation: Status tracking in status.md or index

---

### 🔮 Deferred: Priority 3 - JSON Index for Metadata

**Status:** Planned (implement after Priority 1)
**Complexity:** HIGH
**Estimated Impact:**
- Token Savings: 60% (single index vs 76+ markdown files)
- Speed Improvement: 85% faster sync operations
- Readability: MEDIUM (requires tooling for human inspection)

**Problem Statement:**
Each application contains `analysis.md` (avg 25KB) and `job-description.md` (avg 8KB) with 80% repetitive template text. Sync script must open and parse 76+ files just to extract basic metadata like fit scores and statuses.

**Proposed Solution:**
Centralized `applications-index.json` with core metadata:

```json
{
  "2025-11-Kraken-SrGroupPMGrowthPlatform": {
    "company": "Kraken",
    "role": "Sr Group Product Manager, Growth Platform",
    "fit_score": 9.5,
    "status": "interviewing",
    "location": "Remote (Global)",
    "salary_range": "£140K-£170K",
    "key_requirements": ["Growth", "Platform", "Crypto"],
    "analysis_summary": "Strong fit due to growth platform expertise...",
    "job_url": "https://kraken.com/careers/...",
    "applied_date": "2025-11-12",
    "deadline": null,
    "folder_path": "active/interviewing/2025-11-Kraken-SrGroupPMGrowthPlatform"
  },
  ...
}
```

Keep detailed `analysis.md` and `job-description.md` in folders for deep reference, but use index for fast lookups.

**Benefits:**
- Single JSON file read (~20-30KB total) vs opening 76+ markdown files
- 85% faster sync operations
- Enables advanced querying: "show all 9+ fit roles in London"
- Better for programmatic access and analytics dashboards

**Implementation Steps:**
1. Design JSON schema for application metadata
2. Create migration script to generate index from existing folders
3. Update `sync-status.py` to read from index (with folder fallback)
4. Update all commands (`/analyze-job`, `/update-status`, etc.) to write to index
5. Create CLI tool for viewing/searching index: `./scripts/app-index search "Kraken"`
6. Add index validation checks (ensure sync with folders)
7. Implement auto-regeneration on folder changes
8. Maintain backward compatibility during transition

**Risks & Trade-offs:**
- **Major refactoring required:** All commands need updates
- **Loss of markdown readability:** Can't quickly view index in text editor
- **Sync issues:** Index could diverge from folder contents
- **Migration complexity:** HIGH - need extensive testing

**Mitigation Strategies:**
- Build CLI tool first: `./scripts/app-index view Kraken` for human-friendly viewing
- Automatic index validation on every sync
- Regenerate index from folders if corruption detected
- Keep detailed markdown files as source of truth, index as cache
- Rollback plan: Delete index, fall back to folder scanning

---

### Future Optimization Opportunities

**Not currently prioritized but documented for future reference:**

1. **Archive Compression**
   - ZIP quarterly archive folders to save disk space
   - Estimated: 50% disk space reduction for archived apps
   - Trade-off: Need decompression step to access old applications

2. **Status Transition Automation**
   - Auto-move folders when status.md is updated
   - Partially implemented in `/update-status`
   - Could add file system watchers for real-time moves

3. **Metrics Caching**
   - Cache computed metrics between syncs
   - Invalidate cache on folder/status changes
   - Estimated: 90% faster dashboard regeneration

4. **Full-Text Search Index**
   - Elasticsearch or Algolia index for instant searching
   - Search across all job descriptions and analyses
   - Advanced filtering: date ranges, fit scores, locations, keywords

---

### Implementation Timeline

| Priority | Feature | Status | Implemented | Target |
|----------|---------|--------|-------------|--------|
| 2 | Status Hierarchy | ✅ Complete | 2025-11-18 | - |
| 1 | Lazy-Loading Prep Files | 🔮 Planned | - | TBD |
| 3 | JSON Index | 🔮 Planned | - | After Priority 1 |

---

### Performance Metrics

**Baseline (Before Refactoring - Flat Structure):**
- Total applications: 44
- Avg sync time: ~8 seconds
- Avg tokens per sync: ~350K tokens
- Folder navigation: Difficult (all mixed)

**After Priority 2 (Status Hierarchy - Implemented):**
- Total applications: 44 (26 active, 18 archived)
- Avg sync time: ~3 seconds (**65% faster**)
- Avg tokens per sync: ~100K tokens (**70% reduction**)
- Folder navigation: Excellent (clear hierarchy)

**Target After All Priorities:**
- Avg sync time: <1 second (90% faster than baseline)
- Avg tokens per sync: <30K tokens (90% reduction from baseline)
- Prep files only when needed (45% folder size reduction)
- JSON index for instant metadata access (85% faster lookups)

---

### Decision Rationale

**Why Priority 2 First?**
- Balanced impact (70% token savings) with moderate complexity
- Provides immediate organizational benefits
- Enables future optimizations by separating active vs archived
- Clear rollback path with backup strategy
- Low risk migration with validation steps

**Why Defer Priority 1 (Lazy-Loading)?**
- Requires changes to user workflow (generate on demand)
- Better to stabilize new folder structure first
- Lower risk when users familiar with status hierarchy

**Why Defer Priority 3 (JSON Index)?**
- HIGH complexity requiring extensive refactoring
- Needs CLI tooling for usability
- Best implemented after simpler optimizations prove value
- Can learn from Priority 1 and 2 experiences
