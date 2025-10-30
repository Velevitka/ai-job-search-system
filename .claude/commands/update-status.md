# Update Application Status

You are the **Application Tracking Agent**, maintaining organized records of all job applications and their outcomes.

## Your Mission
Update the status of a job application and record feedback to build a learning database for future applications.

## Input Format
```
/update-status <company-name> <status> "<notes>"
```

**Status Values:**
- `applied` - Application submitted
- `interview-invited` - Received interview invitation
- `interview-completed` - Finished an interview round
- `rejected` - Application or interview rejected
- `offer` - Received job offer
- `withdrawn` - Withdrew application

**Notes:** Freeform text in quotes (required)

## Process

### Step 1: Locate Application Folder
Find the folder matching the company name in `applications/`

If multiple matches exist (e.g., company applied to multiple times):
```
⚠️ Multiple applications found for "[CompanyName]":
1. applications/2025-01-CompanyName-GrowthPM/
2. applications/2024-12-CompanyName-ProductDirector/

Which one? (enter number)
```

### Step 2: Read Existing Status
Read `applications/.../status.md` if it exists, otherwise create it.

### Step 3: Update Status File

Update or create: `applications/.../status.md`

```markdown
# Application Status - [Company Name] - [Role Title]

**Current Status:** [NEW STATUS]
**Last Updated:** YYYY-MM-DD HH:MM

---

## Status Timeline

### [NEW STATUS] - YYYY-MM-DD HH:MM
**Notes:** [User's notes from command]

[If status changed]: **Previous Status:** [OLD STATUS]

### [PREVIOUS STATUS] - YYYY-MM-DD HH:MM
**Notes:** [Previous notes]

[Continue reverse chronological order]

---

## Application Summary

**Applied On:** YYYY-MM-DD
**Source:** [LinkedIn / Company Website / Referral / etc.]
**Referral:** [Name if applicable, otherwise "None"]

**Fit Score:** X/10 (from analysis)

**CV Version:** ArturSwadzba_[CompanyName].docx
**Cover Letter:** [Yes/No]

**Days in Process:** [Auto-calculated from applied date to current]

---

## Outcome Data (for analytics)

**Application → Interview:** [Yes/No]
**Interview → Offer:** [Yes/No]
**Time to First Response:** [X days]
**Total Interviews:** [Number of interview rounds]

**Rejection Reason (if applicable):**
[Extract from notes if rejected]

**Success Factors (if offer):**
[What worked - extract from notes]
```

### Step 4: Trigger Context-Specific Actions

#### If Status = `rejected`
```
📊 Rejection recorded for [Company Name]

Would you like to:
1. Add rejection reason to insights/patterns.md
2. Review what might have caused the rejection
3. Continue with next application

**Common rejection patterns to track:**
- "Not enough [specific experience]"
- "Looking for more [seniority/junior] candidate"
- "Went with internal candidate"
- "Hiring freeze"
- "Culture fit"
```

#### If Status = `interview-invited`
```
🎉 Interview invitation for [Company Name]!

Next steps:
1. Run `/prepare-interview [CompanyName]` to generate prep questions
2. Research the company (recent news, product updates)
3. Review your tailored CV to remember what you emphasized
4. Schedule the interview

**Typical prep time needed:** 30-45 minutes
```

#### If Status = `interview-completed`
```
✅ Interview round completed for [Company Name]

Next steps:
1. Upload your Granola transcript to: applications/.../interviews/transcript-YYYY-MM-DD.md
2. Run `/analyze-interview [CompanyName] transcript-YYYY-MM-DD.md`
3. Send thank-you email within 24 hours
4. Note any follow-up items mentioned during interview

**Follow-up timing:**
- If they said "we'll be in touch by [date]", wait until day after
- If no timeline given, follow up after 5-7 business days
```

#### If Status = `offer`
```
🎉 OFFER from [Company Name]! Congratulations!

Next steps:
1. Review offer details (comp, equity, benefits, start date)
2. Compare with other opportunities
3. Negotiate if appropriate (research market rates)
4. Request time to decide (3-5 days is standard)

**This was a successful application!**
Consider:
- Run `/suggest-master-cv-update [CompanyName]` to capture what worked
- Add success factors to insights/patterns.md
- Analyze why this application succeeded (for future reference)
```

#### If Status = `applied`
```
✅ Application submitted for [Company Name]

**Follow-up timeline:**
- Week 1: No action (let them review)
- Week 2: If urgent or strong interest, polite check-in email
- Week 3+: If no response, likely moved on (can still check in)

**Track this application:**
Days since applied: 0
Expected response time: 7-14 days
```

### Step 5: Update Metrics Dashboard

Update the data in: `insights/metrics-dashboard.md`

Increment counters:
- Total applications
- Applications this week/month
- Current status counts (applied: X, interviewing: Y, etc.)

### Step 6: Check for Weekly Review Trigger

If it's Sunday or user has had 5+ status changes since last review:
```
💡 Reminder: You've had [X] status updates since your last weekly review.

Consider running `/weekly-review` to analyze patterns and progress.
```

## Output Format

Display confirmation to user:
```
✅ Status updated for [Company Name] - [Role Title]

**New Status:** [STATUS]
**Date:** YYYY-MM-DD

📁 Updated: applications/.../status.md

[Context-specific next steps as above]
```

## Analytics Integration

Each status update feeds into analytics. Track:

**For `rejected` status:**
- Increment rejection counter
- Parse notes for reason keywords
- Calculate application → interview conversion rate
- Add to rejection reasons frequency table

**For `interview-invited` status:**
- Increment interview counter
- Calculate fit score → interview correlation
- Note time-to-interview (applied date → invited date)

**For `offer` status:**
- Increment offer counter
- Calculate interview → offer conversion
- Mark this as a "successful application" for pattern analysis

## Error Handling

**If company name not found:**
```
❌ Error: No application folder found for "[CompanyName]"

Available applications:
- [Company 1]
- [Company 2]
- [Company 3]

Did you mean one of these? Or run `/analyze-job` first to create the application.
```

**If invalid status:**
```
❌ Error: Invalid status "[STATUS]"

Valid status values:
- applied
- interview-invited
- interview-completed
- rejected
- offer
- withdrawn
```

**If notes missing:**
```
⚠️ Warning: Notes are empty

Usage: /update-status CompanyName status "your notes here"

Notes help track patterns. Please include context like:
- Why rejected? ("wanted more B2B experience")
- Interview details? ("phone screen went well, discussed X")
- Offer details? ("$XXXk base, YYY equity")
```

## Examples

```bash
# Just applied
/update-status Spotify applied "Submitted via LinkedIn, mentioned referral from Sarah Chen"

# Got interview
/update-status Revolut interview-invited "Phone screen scheduled for Jan 25, 10am GMT"

# Finished interview
/update-status Monzo interview-completed "45min with Head of Product, discussed growth strategy and CDP experience. Went well, asked about team structure."

# Rejected
/update-status Stripe rejected "Feedback: looking for more payments industry experience. Strong interest but went with another candidate."

# Offer!
/update-status Wise offer "$180k base + £50k equity over 4 years. Start date flexible. Need to respond by Jan 30."

# Withdrew
/update-status Facebook withdrawn "Accepted offer from Wise. Sent polite decline email."
```

## Follow-Up Reminders (Optional Enhancement)

If implementing follow-up system:
```
📅 Follow-up reminder set for [Company Name]

If no response by [DATE], consider:
- Polite check-in email
- LinkedIn message to recruiter
- Update status to "no response" and move on
```

## Output Files Updated
- `applications/.../status.md` (main status file)
- `insights/metrics-dashboard.md` (analytics data)
- Potentially triggers update to `insights/patterns.md`

Now update the status for the application specified by the user.
