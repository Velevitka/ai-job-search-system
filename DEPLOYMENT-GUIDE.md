# Deployment Guide: Local vs Cloud

Complete guide for running automated job discovery on a schedule.

---

## 📋 Overview

You have 3 main options for running scheduled job discovery:

| Option | Cost | Requires Laptop On? | Setup Difficulty | Best For |
|--------|------|---------------------|------------------|----------|
| **Local (Windows Task Scheduler)** | Free | ✅ Yes | Easy | Daily use, always-on laptop |
| **GitHub Actions** | Free* | ❌ No | Medium | Budget-conscious, simple setup |
| **Cloud VM (AWS/GCP)** | ~$5-10/month | ❌ No | Hard | Professional, reliable 24/7 |

*GitHub Actions: Free tier = 2000 minutes/month (enough for ~40 runs)

---

## Option 1: Local Scheduling (Windows Task Scheduler)

### ✅ Pros
- **Free** - No monthly costs
- **Fast** - Uses your existing browser session
- **Private** - All data stays on your machine
- **Easy setup** - 10 minutes

### ❌ Cons
- **Requires laptop running** - Won't run if computer is off/asleep
- **Not cloud-based** - Can't run when traveling
- **Manual updates** - Need to pull git changes manually

### 💰 Cost: **$0/month**

---

### Setup Steps (Windows)

#### 1. Save your LinkedIn session

First run to log in and save session:

```bash
python scripts/job_discovery.py --keywords "Director Product" --location "London"
# Browser opens → Log in to LinkedIn → Press ENTER
# Session saved to .browser_data/
```

#### 2. Create a batch script

Create `run_job_monitor.bat` in your project root:

```batch
@echo off
cd /d "C:\Users\ArturSwadzba\OneDrive\4. CV"
python scripts/scheduled_monitor.py --email your@email.com >> logs/job_monitor.log 2>&1
```

#### 3. Set up Windows Task Scheduler

**Open Task Scheduler:**
- Press `Win + R`, type `taskschd.msc`, press Enter

**Create Basic Task:**
1. Click "Create Basic Task"
2. Name: "LinkedIn Job Discovery"
3. Trigger: Daily
4. Time: 9:00 AM
5. Action: Start a program
6. Program: `C:\Users\ArturSwadzba\OneDrive\4. CV\run_job_monitor.bat`
7. Finish

**Important Settings:**
- ✅ "Run whether user is logged on or not"
- ✅ "Run with highest privileges"
- ❌ "Start only if computer is on AC power" (uncheck if laptop)

#### 4. Test it

Right-click task → "Run" to test immediately.

Check `logs/job_monitor.log` for output.

---

### Email Notifications (Optional)

To get email alerts for high-fit jobs:

#### Using Gmail:

1. **Enable 2FA** on your Google account
2. **Create App Password:**
   - Go to https://myaccount.google.com/apppasswords
   - Generate password for "Mail"
   - Copy the 16-character password

3. **Set environment variables:**

```bash
# Add to system environment variables
SMTP_USERNAME=your.email@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop  # The app password
```

4. **Update batch script:**

```batch
@echo off
cd /d "C:\Users\ArturSwadzba\OneDrive\4. CV"
set SMTP_USERNAME=your.email@gmail.com
set SMTP_PASSWORD=your-app-password-here
python scripts/scheduled_monitor.py --email your@email.com >> logs/job_monitor.log 2>&1
```

---

## Option 2: GitHub Actions (Cloud, Free Tier)

### ✅ Pros
- **Free** - 2000 minutes/month
- **Always runs** - Even when laptop off
- **Auto-updates** - Uses latest code from GitHub
- **Easy to modify** - Just edit YAML file

### ❌ Cons
- **LinkedIn login tricky** - Need to store session securely
- **Public logs** - Job titles visible in Action logs (can make private)
- **Limited minutes** - Free tier caps at 2000 min/month

### 💰 Cost: **$0/month** (Free tier sufficient for daily runs)

**Calculation:**
- Daily run: ~5 minutes (browser automation)
- 30 days × 5 min = 150 minutes/month
- Free tier: 2000 minutes/month
- **Plenty of headroom!**

---

### Setup Steps (GitHub Actions)

#### 1. Create workflow file

Create `.github/workflows/job-discovery.yml`:

```yaml
name: Daily Job Discovery

on:
  schedule:
    # Runs at 9am UTC (10am UK, 11am CET)
    - cron: '0 9 * * *'
  workflow_dispatch:  # Allows manual trigger

jobs:
  discover-jobs:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          python -m playwright install chromium
          python -m playwright install-deps

      - name: Run job discovery
        env:
          LINKEDIN_EMAIL: ${{ secrets.LINKEDIN_EMAIL }}
          LINKEDIN_PASSWORD: ${{ secrets.LINKEDIN_PASSWORD }}
        run: |
          python scripts/scheduled_monitor.py --headless --email ${{ secrets.NOTIFICATION_EMAIL }}

      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: job-discovery-results
          path: staging/
          retention-days: 30
```

#### 2. Add LinkedIn credentials as secrets

**In GitHub repository:**
1. Go to Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add:
   - `LINKEDIN_EMAIL`: your LinkedIn email
   - `LINKEDIN_PASSWORD`: your LinkedIn password
   - `NOTIFICATION_EMAIL`: your email for alerts

**⚠️ Security Note:** Store credentials as secrets, never in code!

#### 3. Handle LinkedIn 2FA

LinkedIn 2FA is challenging for automated logins. Options:

**Option A: Use session cookies (Recommended)**
- Log in manually once on your laptop
- Extract session cookies
- Store as GitHub secret
- Script reuses cookies

**Option B: Disable 2FA temporarily**
- Not recommended for security
- Only if you're okay with the risk

#### 4. Test workflow

- Go to Actions tab in GitHub
- Click "Daily Job Discovery"
- Click "Run workflow" → "Run workflow" button
- Monitor the run

---

### Limitations

**GitHub Actions:**
- Browser automation might be detected by LinkedIn
- Rate limiting more aggressive than personal use
- Can't easily handle interactive login (2FA)

**Workaround:** Run locally once/week to refresh session, then GitHub Actions can use saved session.

---

## Option 3: Cloud VM (AWS EC2 / Google Cloud Compute)

### ✅ Pros
- **Always available** - Runs 24/7
- **Reliable** - Professional infrastructure
- **Scalable** - Can add more searches easily
- **Private** - Your own dedicated machine

### ❌ Cons
- **Costs money** - $5-10/month
- **Setup complexity** - Need to configure server
- **Maintenance** - OS updates, security patches

### 💰 Cost Breakdown

#### AWS EC2 t3.micro (Recommended)

| Component | Specs | Cost |
|-----------|-------|------|
| **Instance** | 2 vCPU, 1GB RAM | $7.50/month (on-demand) |
| **Storage** | 8GB SSD | Included |
| **Data Transfer** | First 100GB out | Free |
| **Total** | | **~$7.50/month** |

**Or use Reserved Instance:** $4.50/month (save 40% with 1-year commitment)

#### Google Cloud Compute e2-micro (Free Tier Option!)

| Component | Specs | Cost |
|-----------|-------|------|
| **Instance** | 2 vCPU, 1GB RAM | **$0/month** (Free tier!) |
| **Storage** | 30GB SSD | **$0/month** (Free tier!) |
| **Limit** | 1 instance per account | Free forever |
| **Total** | | **$0/month** 🎉 |

**🎯 Recommendation:** Start with Google Cloud free tier!

---

### Setup Steps (Google Cloud - Free Tier)

#### 1. Create Google Cloud account

- Go to https://cloud.google.com/free
- Sign up (requires credit card but won't charge without upgrade)
- Get $300 free credit + Always Free tier

#### 2. Create VM instance

```bash
# Or use web console: https://console.cloud.google.com/compute

gcloud compute instances create job-discovery-vm \
    --machine-type=e2-micro \
    --zone=europe-west2-a \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=30GB \
    --boot-disk-type=pd-standard
```

#### 3. SSH into VM

```bash
gcloud compute ssh job-discovery-vm --zone=europe-west2-a
```

#### 4. Install dependencies on VM

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3
sudo apt install python3-pip git -y

# Clone your repository
git clone https://github.com/yourusername/ai-job-search-system.git
cd ai-job-search-system

# Install Python dependencies
pip3 install -r requirements.txt
python3 -m playwright install chromium
python3 -m playwright install-deps

# Install xvfb (virtual display for headless browser)
sudo apt install xvfb -y
```

#### 5. Set up cron job

```bash
# Edit crontab
crontab -e

# Add this line (runs daily at 9am UTC):
0 9 * * * cd /home/youruser/ai-job-search-system && xvfb-run python3 scripts/scheduled_monitor.py --email your@email.com >> /home/youruser/logs/job_monitor.log 2>&1
```

#### 6. Initial login (one-time)

```bash
# Run once to log in to LinkedIn
cd ~/ai-job-search-system
xvfb-run python3 scripts/job_discovery.py --keywords "Test" --location "London"

# Follow prompts to log in
# Session saved to .browser_data/
```

---

## Cost Comparison Summary

| Solution | Monthly Cost | Annual Cost | Laptop Required? | Reliability |
|----------|-------------|-------------|------------------|-------------|
| **Windows Task Scheduler** | $0 | $0 | ✅ Yes | Medium (laptop dependent) |
| **GitHub Actions** | $0 | $0 | ❌ No | Medium (2FA issues) |
| **Google Cloud Free Tier** | $0 | $0 | ❌ No | ⭐ High |
| **AWS EC2 t3.micro** | $7.50 | $90 | ❌ No | ⭐ High |
| **AWS EC2 Reserved** | $4.50 | $54 | ❌ No | ⭐ High |

---

## My Recommendations

### For You (Active Job Search):

**Phase 1 (Week 1-2): Local Scheduling**
- Use Windows Task Scheduler
- Free, fast setup
- Test the workflow

**Phase 2 (Week 3+): Move to Google Cloud Free Tier**
- If laptop scheduling works well
- Migrate to Google Cloud e2-micro (free!)
- Set and forget - runs forever for $0

### Why Not GitHub Actions?

LinkedIn 2FA makes it tricky. Possible but requires:
- Session cookie extraction
- Regular manual refreshes
- More maintenance

**Google Cloud is easier** - just SSH once to log in, then forget about it.

---

## Setup Time Estimates

| Solution | Initial Setup | Maintenance |
|----------|--------------|-------------|
| **Windows Task Scheduler** | 10 minutes | 0 min/week |
| **GitHub Actions** | 30 minutes | 10 min/week (refresh session) |
| **Google Cloud** | 45 minutes | 0 min/week |

---

## Monitoring & Logs

### Local (Windows)

Check logs:
```bash
cat logs/job_monitor.log
```

### GitHub Actions

- Go to Actions tab
- Click latest "Daily Job Discovery" run
- View logs

### Google Cloud

SSH and check logs:
```bash
gcloud compute ssh job-discovery-vm
tail -f ~/logs/job_monitor.log
```

---

## Security Best Practices

1. **Never commit LinkedIn credentials** to git
2. **Use environment variables** for sensitive data
3. **Rotate passwords** if compromised
4. **Enable 2FA** on LinkedIn (makes automation harder but more secure)
5. **Store browser data** in `.browser_data/` (in .gitignore)

---

## Troubleshooting

### "LinkedIn login failed"
- Session expired → Log in again manually
- 2FA required → Complete in browser
- Rate limited → Wait 24 hours

### "No jobs found"
- Check search criteria in `scheduled_monitor.py`
- Verify LinkedIn session still valid
- Check internet connection

### "Script failed" (Google Cloud)
- Check logs: `tail -f ~/logs/job_monitor.log`
- Verify cron is running: `crontab -l`
- Test manually: `cd ~/ai-job-search-system && python3 scripts/scheduled_monitor.py --test`

---

## Next Steps

1. **Week 1:** Set up Windows Task Scheduler (10 min)
2. **Week 2:** Test daily runs, verify deduplication works
3. **Week 3:** Migrate to Google Cloud free tier if satisfied
4. **Week 4:** Fine-tune search criteria, add email notifications

---

## Estimated ROI

**Time saved:** 2-3 hours/week on manual job searching

**Over 6 months:**
- Manual: 12-18 hours/month × 6 = 72-108 hours
- Automated: 30 minutes/month × 6 = 3 hours

**Time saved:** 69-105 hours

**Even at $5/month for AWS, you save:**
- Cost: $30 (6 months)
- Time value: 100 hours × $50/hr = $5,000
- **ROI: 16,567%** 🚀

---

**Recommendation:** Start with local scheduling (free, 10 min setup), then move to Google Cloud free tier for set-and-forget automation.
