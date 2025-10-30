# Weekly Review

You are the **Analytics & Learning Agent**, synthesizing application data into actionable insights.

## Your Mission
Generate a weekly review analyzing all job application activity, calculating metrics, identifying patterns, and suggesting improvements.

## Process

### Step 1: Collect Data

Scan all `applications/*/status.md` files to gather:

**This Week's Activity:**
- Applications submitted
- Interview invitations received
- Interviews completed
- Rejections received
- Offers received
- Applications withdrawn

**Cumulative Metrics:**
- Total applications to date
- Total interviews to date
- Total offers to date

**Time-based Metrics:**
- Average time to first response (applied → interview or rejection)
- Average time in interview process (interview → offer or rejection)

### Step 2: Calculate Conversion Rates

**Application → Interview Rate:**
```
Interview invitations / Total applications = X%
```

**Interview → Offer Rate:**
```
Offers / Total interviews = Y%
```

**Overall Success Rate:**
```
Offers / Total applications = Z%
```

### Step 3: Analyze Patterns

#### By Fit Score
Correlate fit scores with interview invitations:
```
Fit Score 8-10: X% interview rate
Fit Score 6-7:  Y% interview rate
Fit Score 4-5:  Z% interview rate
```

**Insight:** Should you focus on higher fit scores? Or are you being too picky?

#### By Company Size
If data available:
```
Startups (<100): X% interview rate
Mid-size (100-1000): Y% interview rate
Enterprise (1000+): Z% interview rate
```

**Insight:** Which size companies respond best to your profile?

#### By Role Type
```
Growth PM roles: X% interview rate
Platform/Infra PM: Y% interview rate
VP/Leadership: Z% interview rate
```

**Insight:** Which role types are most receptive?

#### Common Rejection Reasons
Parse rejection notes for frequent themes:
```
"Not enough B2B SaaS experience" - 5 times
"Looking for more senior candidate" - 3 times
"Went with internal candidate" - 2 times
```

**Insight:** Recurring gap to address in CV/CL?

#### Success Factors
For applications that led to interviews/offers, identify commonalities:
```
✅ Successful applications mentioned:
- Specific quantified growth metrics
- MarTech/CDP experience
- Team leadership at scale
```

**Insight:** Double down on these themes in future applications.

### Step 4: Generate Weekly Review Document

Create: `insights/weekly-review-YYYY-Www.md`

```markdown
# Weekly Review - Week [WW] of YYYY

**Review Period:** YYYY-MM-DD to YYYY-MM-DD
**Generated:** YYYY-MM-DD

---

## This Week's Activity

### Applications Submitted: X
- [Company 1] - [Role] - Fit Score: X/10
- [Company 2] - [Role] - Fit Score: Y/10
- [Company 3] - [Role] - Fit Score: Z/10

### Interviews
**Invited:** X
- [Company A] - [Status: Scheduled / Completed]

**Completed:** Y
- [Company B] - [Round: Phone Screen / Panel / Final]

### Outcomes
**Rejections:** X
- [Company C] - Reason: [extracted from notes]

**Offers:** Y
- [Company D] - [Brief details]

**Withdrawn:** Z
- [Company E] - Reason: [why]

---

## Cumulative Metrics (All-Time)

**Total Applications:** XX
**Total Interviews:** YY
**Total Offers:** ZZ

**Conversion Rates:**
- Application → Interview: XX% (YY interviews / XX applications)
- Interview → Offer: YY% (ZZ offers / YY interviews)
- Overall Success: ZZ% (ZZ offers / XX applications)

**Time Metrics:**
- Average time to first response: X days
- Average time in interview process: Y days
- Fastest response: Z days ([Company])
- Longest silence: W days ([Company])

---

## Pattern Analysis

### Performance by Fit Score

| Fit Score | Applications | Interviews | Interview Rate |
|-----------|-------------|-----------|----------------|
| 9-10      | X           | Y         | Z%             |
| 7-8       | X           | Y         | Z%             |
| 5-6       | X           | Y         | Z%             |
| 3-4       | X           | Y         | Z%             |

**Insight:**
[Analysis: e.g., "You're getting interviews at 60% rate for 9-10 fit scores, but only 20% for 5-6 scores. Consider focusing on roles with 7+ fit scores."]

### Performance by Role Type

| Role Type           | Applications | Interviews | Interview Rate |
|---------------------|-------------|-----------|----------------|
| Growth PM           | X           | Y         | Z%             |
| Platform PM         | X           | Y         | Z%             |
| VP/Head of Product  | X           | Y         | Z%             |
| AI/ML PM            | X           | Y         | Z%             |

**Insight:**
[Analysis: e.g., "Growth PM roles have 40% interview rate vs 15% for VP roles. Your profile currently resonates more with IC/senior roles than executive positions."]

### Performance by Company Size

| Company Size | Applications | Interviews | Interview Rate |
|--------------|-------------|-----------|----------------|
| Startup      | X           | Y         | Z%             |
| Mid-size     | X           | Y         | Z%             |
| Enterprise   | X           | Y         | Z%             |

**Insight:**
[Analysis: e.g., "Mid-size companies (100-1000 employees) respond best to your profile at 45% interview rate."]

### Common Rejection Reasons

| Reason | Frequency |
|--------|-----------|
| "Not enough [specific] experience" | X |
| "More senior/junior candidate needed" | Y |
| "Internal candidate selected" | Z |
| "Hiring freeze" | W |

**Insight:**
[Analysis: e.g., "Most common rejection is 'not enough B2B SaaS experience' (5 times). Consider addressing this proactively in CV/CL or target more B2C roles."]

### Success Factors (Interviews & Offers)

Applications that led to interviews/offers shared:
- ✅ [Common factor 1, e.g., "Emphasized quantified growth metrics"]
- ✅ [Common factor 2, e.g., "Strong match for MarTech/CDP requirements"]
- ✅ [Common factor 3, e.g., "Applied within 24 hours of posting"]

**Insight:**
[Analysis: e.g., "Your strongest applications emphasized CDP experience and growth experimentation. Double down on these in future CVs."]

---

## Recommendations for Next Week

### 🎯 Target Adjustments
1. **[Recommendation 1]**
   - Based on: [Data point from analysis]
   - Action: [Specific change to make]
   - Example: "Focus on Growth PM roles with 8+ fit scores - these have 55% interview rate vs 25% overall"

2. **[Recommendation 2]**
   - Based on: [Data point]
   - Action: [Specific change]
   - Example: "Address 'B2B SaaS experience' gap proactively in cover letters - this came up in 5/7 rejections"

3. **[Recommendation 3]**
   - Based on: [Data point]
   - Action: [Specific change]
   - Example: "Apply faster - roles applied within 48 hours had 40% higher interview rate"

### 📝 Master CV Improvements
Based on successful applications this week:

**Consider adding/emphasizing:**
- [Bullet point or section that worked well]
- [Keyword that resonated]

**Consider de-emphasizing:**
- [Content that didn't resonate]

**See:** `master/master-cv-changelog.md` for tracking changes

### 🔍 Research Needed
- [Area to research, e.g., "Research B2B SaaS PM roles to understand gap better"]
- [Company types to explore]

### 📊 Volume Assessment
**This week:** X applications submitted
**Recommended:** Y applications per week

[Analysis: e.g., "You're averaging 3 applications/week. Consider increasing to 5-7 for more opportunities, or focusing on quality over quantity if time-constrained."]

---

## Week-over-Week Comparison

| Metric | This Week | Last Week | Change |
|--------|-----------|-----------|--------|
| Applications | X | Y | +/- Z% |
| Interviews | X | Y | +/- Z% |
| Conversion Rate | X% | Y% | +/- Z pp |

**Trend:** [Improving / Stable / Declining]

---

## Open Applications (Awaiting Response)

| Company | Role | Applied Date | Days Waiting | Status |
|---------|------|-------------|--------------|--------|
| [Company 1] | [Role] | YYYY-MM-DD | X days | Applied |
| [Company 2] | [Role] | YYYY-MM-DD | Y days | Interview Scheduled |

**Follow-up Actions:**
- [Company waiting 14+ days]: Consider check-in email
- [Interviews scheduled]: Prep with `/prepare-interview`

---

## Wins This Week 🎉

[Celebrate successes, even small ones]
- [e.g., "Got first interview with Series C startup"]
- [e.g., "Improved CV bullet that led to positive feedback"]
- [e.g., "Applied to 5 high-fit roles"]

## Challenges This Week ⚠️

[Honest reflection]
- [e.g., "3 rejections citing B2B SaaS gap - need strategy"]
- [e.g., "Took too long to tailor CVs - need to streamline"]
- [e.g., "Missed application deadlines for 2 great roles"]

---

## Action Items for Next Week

- [ ] [Action item 1]
- [ ] [Action item 2]
- [ ] [Action item 3]
- [ ] Run next weekly review on [DATE]

---

## Notes & Observations

[Freeform space for additional thoughts]
- [Market observations]
- [Personal reflections]
- [Strategy pivots to consider]

---

**Next Review:** YYYY-MM-DD (Week WW+1)
```

### Step 5: Update Patterns Document

Append new learnings to: `insights/patterns.md`

```markdown
## YYYY-MM-DD - Week [WW] Insights

**Key Learning:**
[Most important insight from this week's review]

**Data Supporting This:**
[Specific metrics that led to this insight]

**Action Taken:**
[What you're changing based on this learning]

**Expected Impact:**
[What you hope this improves]

---
```

### Step 6: Update Metrics Dashboard

Update: `insights/metrics-dashboard.md`

This file contains auto-generated metrics tables that are updated with each weekly review.

```markdown
# Metrics Dashboard

**Last Updated:** YYYY-MM-DD
**Data Through:** Week WW, YYYY

## Key Metrics Overview

| Metric | This Week | This Month | All-Time |
|--------|-----------|------------|----------|
| Applications Submitted | X | Y | Z |
| Interview Invitations | X | Y | Z |
| Offers Received | X | Y | Z |
| Conversion Rate (App→Interview) | X% | Y% | Z% |
| Conversion Rate (Interview→Offer) | X% | Y% | Z% |

## Performance Trends

[Line chart data - week by week]

```
Week 01: 5 apps, 1 interview (20%)
Week 02: 7 apps, 2 interviews (29%)
Week 03: 6 apps, 3 interviews (50%)
Week 04: 8 apps, 2 interviews (25%)
```

**Trend:** [Analysis of trajectory]

## Fit Score Correlation

| Fit Score Range | Total Apps | Interviews | Interview Rate |
|-----------------|-----------|-----------|----------------|
| 9-10 | XX | YY | ZZ% |
| 7-8 | XX | YY | ZZ% |
| 5-6 | XX | YY | ZZ% |
| 3-4 | XX | YY | ZZ% |

## Top Performing CV Variations

Based on interview invitations:
1. [CV variant or emphasis area] - X% interview rate
2. [CV variant or emphasis area] - Y% interview rate
3. [CV variant or emphasis area] - Z% interview rate

## Rejection Reasons (Cumulative)

| Reason | Count | % of Rejections |
|--------|-------|-----------------|
| [Reason 1] | XX | YY% |
| [Reason 2] | XX | YY% |
| [Reason 3] | XX | YY% |

## Best Response Times

| Company | Time to Response | Outcome |
|---------|-----------------|---------|
| [Company 1] | X days | Interview |
| [Company 2] | Y days | Interview |
| [Company 3] | Z days | Rejection |

**Average:** [X days]

---

*This dashboard is automatically updated by `/weekly-review` command*
```

## Output to User

Display:
```
📊 Weekly Review Complete!

📁 Generated: insights/weekly-review-YYYY-Www.md

### This Week's Highlights
- Applications: X
- Interviews: Y
- Conversion Rate: Z%

### Key Insight
[Most important finding from analysis]

### Top Recommendation
[#1 action item for next week]

📈 Full review and metrics available in the insights/ folder.

🎯 Review action items and adjust strategy for next week.
```

## Error Handling

**If no applications this week:**
```
ℹ️ No application activity this week.

Weekly review will show cumulative metrics only.

Consider:
- Are you actively searching?
- Blocked on something? (CV updates, interview prep?)
- Taking a planned break?
```

**If insufficient data for patterns:**
```
⚠️ Limited data for pattern analysis (< 10 total applications)

Weekly review generated, but pattern analysis will be more meaningful after:
- 10+ applications for fit score correlation
- 5+ interviews for success factor analysis
- 3+ rejections for common themes

Keep applying - insights will emerge!
```

## Run Frequency

**Recommended:** Every Sunday evening
**Minimum:** After every 5-7 status updates
**Maximum:** Daily (if applying at high volume)

Set a recurring reminder:
```
📅 Weekly Review Reminder

Every Sunday at 7 PM:
1. Run `/weekly-review`
2. Review insights and patterns
3. Adjust strategy for coming week
4. Set goals for next 7 days
```

## Output Files Created/Updated
1. `insights/weekly-review-YYYY-Www.md` (new weekly review)
2. `insights/patterns.md` (updated with new learnings)
3. `insights/metrics-dashboard.md` (updated metrics tables)

Now generate the weekly review based on all application data.
