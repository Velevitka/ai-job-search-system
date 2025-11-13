#!/usr/bin/env python3
"""
Evaluate Fit Score Accuracy

Analyzes correlation between predicted fit scores and actual outcomes:
- High-fit (8.5-10) success rate
- Medium-fit (7-8.5) success rate
- False positive rate (high-fit → rejected)
- Time to response by fit tier
- Provides recommendations for recalibration if needed

Run: python scripts/evaluate_fit_accuracy.py
Output: insights/fit-score-evaluation-YYYY-MM-DD.md
"""

from pathlib import Path
from datetime import datetime, timedelta
import re
from collections import defaultdict
from typing import Dict, List, Tuple
import json


class FitScoreEvaluator:
    def __init__(self, applications_path: Path = Path("applications")):
        self.applications_path = applications_path
        self.results = {
            'high_fit_accepted': [],   # Fit 8.5-10, got offer/interview
            'high_fit_rejected': [],   # Fit 8.5-10, rejected
            'medium_fit_accepted': [], # Fit 7-8.5, got offer/interview
            'medium_fit_rejected': [], # Fit 7-8.5, rejected
            'low_fit_attempted': [],   # Fit <7, applied (shouldn't happen often)
        }
        self.time_to_response = defaultdict(list)

    def parse_fit_score(self, analysis_file: Path) -> float:
        """Extract fit score from analysis.md"""
        if not analysis_file.exists():
            return None

        content = analysis_file.read_text(encoding='utf-8')
        match = re.search(r'Fit Score:\s*([\d.]+)/10', content)
        if match:
            return float(match.group(1))
        return None

    def parse_status(self, status_file: Path) -> Dict:
        """Extract current status and timeline from status.md"""
        if not status_file.exists():
            return None

        content = status_file.read_text(encoding='utf-8')

        # Extract current status
        status_match = re.search(r'\*\*Current Status:\*\*\s*(\w+)', content)
        current_status = status_match.group(1) if status_match else None

        # Extract applied date
        applied_match = re.search(r'Applied On:\*\*\s*(\d{4}-\d{2}-\d{2})', content)
        applied_date = applied_match.group(1) if applied_match else None

        # Extract response date (interview-invited or rejected)
        response_match = re.search(
            r'###\s*(Interview-Invited|Rejected)\s*-\s*(\d{4}-\d{2}-\d{2})',
            content
        )
        response_date = response_match.group(2) if response_match else None

        # Calculate time to response
        time_to_response = None
        if applied_date and response_date:
            try:
                applied_dt = datetime.strptime(applied_date, '%Y-%m-%d')
                response_dt = datetime.strptime(response_date, '%Y-%m-%d')
                time_to_response = (response_dt - applied_dt).days
            except ValueError:
                pass

        return {
            'current_status': current_status,
            'applied_date': applied_date,
            'response_date': response_date,
            'time_to_response': time_to_response
        }

    def categorize_fit_tier(self, fit_score: float) -> str:
        """Categorize fit score into tiers"""
        if fit_score >= 8.5:
            return 'high'
        elif fit_score >= 7.0:
            return 'medium'
        else:
            return 'low'

    def categorize_outcome(self, status: str) -> str:
        """Categorize outcome as success or failure"""
        if status in ['offer', 'accepted', 'interview-invited', 'interview-completed']:
            return 'success'
        elif status in ['rejected']:
            return 'failure'
        else:
            return 'pending'

    def analyze_applications(self):
        """Analyze all applications and categorize by fit/outcome"""
        for app_folder in self.applications_path.glob("2025-*"):
            if not app_folder.is_dir():
                continue

            analysis_file = app_folder / "analysis.md"
            status_file = app_folder / "status.md"

            fit_score = self.parse_fit_score(analysis_file)
            status_data = self.parse_status(status_file)

            if fit_score is None or status_data is None:
                continue

            current_status = status_data['current_status']
            time_to_response = status_data['time_to_response']

            # Skip if still in drafting phase
            if current_status == 'drafting':
                continue

            fit_tier = self.categorize_fit_tier(fit_score)
            outcome = self.categorize_outcome(current_status)

            app_info = {
                'company': app_folder.name,
                'fit_score': fit_score,
                'status': current_status,
                'time_to_response': time_to_response
            }

            # Categorize
            if fit_tier == 'high':
                if outcome == 'success':
                    self.results['high_fit_accepted'].append(app_info)
                elif outcome == 'failure':
                    self.results['high_fit_rejected'].append(app_info)
            elif fit_tier == 'medium':
                if outcome == 'success':
                    self.results['medium_fit_accepted'].append(app_info)
                elif outcome == 'failure':
                    self.results['medium_fit_rejected'].append(app_info)
            else:  # low
                if current_status != 'withdrawn':
                    self.results['low_fit_attempted'].append(app_info)

            # Track time to response by fit tier
            if time_to_response is not None:
                self.time_to_response[fit_tier].append(time_to_response)

    def calculate_metrics(self) -> Dict:
        """Calculate success rates and other metrics"""
        # High-fit success rate
        high_fit_total = len(self.results['high_fit_accepted']) + len(self.results['high_fit_rejected'])
        high_fit_success_rate = (
            len(self.results['high_fit_accepted']) / high_fit_total * 100
            if high_fit_total > 0 else 0
        )

        # Medium-fit success rate
        medium_fit_total = len(self.results['medium_fit_accepted']) + len(self.results['medium_fit_rejected'])
        medium_fit_success_rate = (
            len(self.results['medium_fit_accepted']) / medium_fit_total * 100
            if medium_fit_total > 0 else 0
        )

        # False positive rate (high-fit rejected)
        false_positive_rate = (
            len(self.results['high_fit_rejected']) / high_fit_total * 100
            if high_fit_total > 0 else 0
        )

        # Average time to response by tier
        avg_time_to_response = {}
        for tier, times in self.time_to_response.items():
            avg_time_to_response[tier] = sum(times) / len(times) if times else 0

        return {
            'high_fit_success_rate': high_fit_success_rate,
            'medium_fit_success_rate': medium_fit_success_rate,
            'false_positive_rate': false_positive_rate,
            'high_fit_total': high_fit_total,
            'medium_fit_total': medium_fit_total,
            'avg_time_to_response': avg_time_to_response,
            'high_fit_accepted_count': len(self.results['high_fit_accepted']),
            'high_fit_rejected_count': len(self.results['high_fit_rejected']),
            'medium_fit_accepted_count': len(self.results['medium_fit_accepted']),
            'medium_fit_rejected_count': len(self.results['medium_fit_rejected']),
            'low_fit_attempted_count': len(self.results['low_fit_attempted']),
        }

    def generate_recommendations(self, metrics: Dict) -> List[str]:
        """Generate calibration recommendations based on metrics"""
        recommendations = []

        # Target: High-fit success rate >60%
        if metrics['high_fit_success_rate'] < 60:
            recommendations.append(
                f"⚠️ High-fit success rate ({metrics['high_fit_success_rate']:.1f}%) below target (60%). "
                "Consider recalibrating fit scoring algorithm or adjusting expectations."
            )

        # Target: False positive rate <20%
        if metrics['false_positive_rate'] > 20:
            recommendations.append(
                f"⚠️ False positive rate ({metrics['false_positive_rate']:.1f}%) above target (20%). "
                f"{metrics['high_fit_rejected_count']} high-fit applications were rejected. "
                "Review rejection reasons to identify patterns."
            )

        # Target: Medium-fit success rate >40%
        if metrics['medium_fit_success_rate'] < 40:
            recommendations.append(
                f"⚠️ Medium-fit success rate ({metrics['medium_fit_success_rate']:.1f}%) below target (40%). "
                "Consider focusing efforts on higher-fit opportunities."
            )

        # Low-fit applications (shouldn't apply to <7 fit often)
        if metrics['low_fit_attempted_count'] > 0:
            recommendations.append(
                f"⚠️ {metrics['low_fit_attempted_count']} low-fit (<7) applications attempted. "
                "Stick to 7+ fit threshold to optimize effort."
            )

        # If all targets met
        if not recommendations:
            recommendations.append(
                "✅ All fit score targets met! Scoring algorithm appears well-calibrated."
            )

        return recommendations

    def generate_report(self) -> str:
        """Generate markdown report"""
        metrics = self.calculate_metrics()
        recommendations = self.generate_recommendations(metrics)

        report = f"""# Fit Score Accuracy Evaluation

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Evaluator:** Fit Score Evaluation Script

---

## Executive Summary

**High-Fit (8.5-10) Performance:**
- Success Rate: **{metrics['high_fit_success_rate']:.1f}%** (Target: >60%)
- Applications: {metrics['high_fit_total']} total ({metrics['high_fit_accepted_count']} success, {metrics['high_fit_rejected_count']} rejected)
- False Positive Rate: **{metrics['false_positive_rate']:.1f}%** (Target: <20%)

**Medium-Fit (7-8.5) Performance:**
- Success Rate: **{metrics['medium_fit_success_rate']:.1f}%** (Target: >40%)
- Applications: {metrics['medium_fit_total']} total ({metrics['medium_fit_accepted_count']} success, {metrics['medium_fit_rejected_count']} rejected)

**Low-Fit (<7) Applications:**
- Count: {metrics['low_fit_attempted_count']} (Should be rare - strategic withdrawals expected)

---

## Recommendations

"""

        for i, rec in enumerate(recommendations, 1):
            report += f"{i}. {rec}\n"

        report += f"""
---

## Detailed Breakdown

### High-Fit Applications (8.5-10)

**Successes ({len(self.results['high_fit_accepted'])}):**
"""
        for app in self.results['high_fit_accepted']:
            report += f"- {app['company']}: Fit {app['fit_score']}/10 → {app['status']}"
            if app['time_to_response']:
                report += f" ({app['time_to_response']} days to response)"
            report += "\n"

        report += f"""
**Rejections ({len(self.results['high_fit_rejected'])}):**
"""
        for app in self.results['high_fit_rejected']:
            report += f"- {app['company']}: Fit {app['fit_score']}/10 → REJECTED"
            if app['time_to_response']:
                report += f" ({app['time_to_response']} days)"
            report += "\n"

        report += f"""
### Medium-Fit Applications (7-8.5)

**Successes ({len(self.results['medium_fit_accepted'])}):**
"""
        for app in self.results['medium_fit_accepted']:
            report += f"- {app['company']}: Fit {app['fit_score']}/10 → {app['status']}"
            if app['time_to_response']:
                report += f" ({app['time_to_response']} days)"
            report += "\n"

        report += f"""
**Rejections ({len(self.results['medium_fit_rejected'])}):**
"""
        for app in self.results['medium_fit_rejected']:
            report += f"- {app['company']}: Fit {app['fit_score']}/10 → REJECTED"
            if app['time_to_response']:
                report += f" ({app['time_to_response']} days)"
            report += "\n"

        if self.results['low_fit_attempted']:
            report += f"""
### Low-Fit Applications (<7)

**Attempted ({len(self.results['low_fit_attempted'])}):**
"""
            for app in self.results['low_fit_attempted']:
                report += f"- {app['company']}: Fit {app['fit_score']}/10 → {app['status']}\n"

        report += """
---

## Time to Response Analysis

"""
        for tier, times in sorted(self.time_to_response.items()):
            if times:
                avg = sum(times) / len(times)
                report += f"- **{tier.title()}-Fit:** {avg:.1f} days average (n={len(times)})\n"

        report += """
---

## Interpretation

**Success Rates:**
- High success rates indicate fit scoring aligns with market needs
- Low success rates suggest either scoring miscalibration or external factors (market conditions, competition)

**False Positives (High-Fit Rejections):**
- Review rejection reasons for patterns
- Common causes: timing, competition, specific experience gaps not captured by fit score
- If systematic pattern found, adjust scoring criteria

**Time to Response:**
- Faster responses for high-fit roles suggests companies recognize strong candidates quickly
- Slower responses may indicate processing delays, not fit issues

---

## Next Steps

1. **If targets not met:** Review `/analyze-job` fit scoring criteria
2. **Review rejected high-fit apps:** Identify common rejection reasons
3. **Update career-preferences.md:** Add weighting for undervalued skills
4. **Re-run evaluation:** After 20+ applications to assess changes

**Evaluation Frequency:** Run monthly or after every 10 completed applications
"""

        return report

    def save_report(self, report: str):
        """Save report to insights folder"""
        insights_path = Path("insights")
        insights_path.mkdir(exist_ok=True)

        filename = f"fit-score-evaluation-{datetime.now().strftime('%Y-%m-%d')}.md"
        output_path = insights_path / filename

        output_path.write_text(report, encoding='utf-8')
        print(f"✅ Report saved to: {output_path}")

        return output_path


def main():
    """Run fit score evaluation"""
    print("🔍 Evaluating Fit Score Accuracy...")
    print()

    evaluator = FitScoreEvaluator()
    evaluator.analyze_applications()

    metrics = evaluator.calculate_metrics()

    print("📊 Metrics Summary:")
    print(f"  High-Fit Success Rate: {metrics['high_fit_success_rate']:.1f}% (Target: >60%)")
    print(f"  Medium-Fit Success Rate: {metrics['medium_fit_success_rate']:.1f}% (Target: >40%)")
    print(f"  False Positive Rate: {metrics['false_positive_rate']:.1f}% (Target: <20%)")
    print()

    report = evaluator.generate_report()
    output_path = evaluator.save_report(report)

    print()
    print(f"📄 Full report: {output_path}")
    print()

    recommendations = evaluator.generate_recommendations(metrics)
    print("💡 Key Recommendations:")
    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. {rec}")


if __name__ == "__main__":
    main()
