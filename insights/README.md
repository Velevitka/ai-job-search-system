# Insights Folder

This folder contains analytics, metrics, and learnings from your job search.

## What Goes Here

1. **metrics-dashboard.md** - Overview of your application statistics
   - Total applications submitted
   - Response rates by role type, seniority, industry
   - Conversion rates through each stage
   - Time-to-response metrics
   - Fit score vs. success correlation

2. **patterns.md** - Identified patterns from your applications
   - Which keywords correlate with interviews
   - Best-performing CV bullets
   - Most effective cover letter openings
   - Companies that respond quickly vs. slowly
   - Role types with highest success rate

3. **weekly-reviews/** - Weekly summary reports
   - Applications submitted that week
   - Responses received
   - Interviews scheduled
   - Learnings and adjustments

4. **bulk-analysis-YYYY-MM-DD.md** - Results from bulk processing
   - When you analyze multiple jobs at once
   - Prioritized list of opportunities
   - Pattern recognition across similar roles

## Important Notes

- **This folder is in .gitignore** - Your personal metrics never get committed
- Insights are generated automatically by the `/weekly-review` command
- Use these insights to refine your application strategy
- Track both successes and failures to learn what works

## Example Structure

```
insights/
├── metrics-dashboard.md
├── patterns.md
├── weekly-reviews/
│   ├── 2025-W01.md
│   ├── 2025-W02.md
│   └── 2025-W03.md
└── bulk-analysis-2025-01-15.md
```

## Key Metrics to Track

**Volume Metrics:**
- Applications per week
- Total active applications
- Applications in each stage

**Success Metrics:**
- Response rate (% that respond)
- Interview rate (% that lead to interviews)
- Offer rate (% that result in offers)
- Time-to-response (days until first response)

**Quality Metrics:**
- Average fit score of applications
- Fit score vs. interview correlation
- Which industries/companies respond best

**Keyword Metrics:**
- Which keywords appear in successful CVs
- Keywords that correlate with interviews
- Over-used vs. under-used terms

## Weekly Review Process

1. Run `/weekly-review` command at end of each week
2. Review metrics and patterns
3. Identify what's working and what's not
4. Adjust strategy for next week
5. Update master CV if needed based on successful bullets

## Tips

- Review insights weekly to spot patterns
- Compare fit scores vs. actual outcomes
- Identify your "sweet spot" roles (where you perform best)
- Track response times to know when to follow up
- Use patterns to refine your application strategy
