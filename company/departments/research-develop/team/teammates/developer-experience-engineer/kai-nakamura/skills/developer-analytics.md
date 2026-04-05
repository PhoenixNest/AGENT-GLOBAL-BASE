# Developer Analytics

**Category:** Developer Experience
**Owner:** Developer Experience Engineer (Kai Nakamura)

## Overview

Measures and improves engineering productivity through data-driven analytics, covering DORA metrics (Deployment Frequency, Lead Time, Change Failure Rate, MTTR), SPACE framework measurement (Satisfaction, Performance, Activity, Communication, Efficiency), developer survey design, and code review cycle analysis. Uses quantitative and qualitative data to identify bottlenecks and drive productivity improvements.

## Competency Dimensions

| Dimension               | Description                                                                     | Proficiency Indicators                                                                                                                                     |
| ----------------------- | ------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| DORA Metrics            | Deployment Frequency, Lead Time for Changes, Change Failure Rate, MTTR          | Computes all four DORA metrics from CI/CD data; tracks trends over time; correlates DORA metrics with team outcomes; benchmarks against industry standards |
| SPACE Framework         | Satisfaction, Performance, Activity, Communication, Efficiency dimensions       | Designs balanced metrics across all SPACE dimensions; avoids over-indexing on activity; combines quantitative and qualitative signals                      |
| Developer Survey Design | Survey methodology, question design, response rate optimization, trend analysis | Writes unbiased questions; achieves > 60% response rate; tracks sentiment trends over time; acts on survey results                                         |
| Code Review Analysis    | Review cycle time, review size, comment quality, reviewer load distribution     | Analyzes PR data for bottlenecks; identifies review size correlation with defect rate; optimizes reviewer assignment                                       |

## Execution Guidance

### DORA Metrics Implementation

```python
# dora_metrics.py — Compute DORA metrics from CI/CD data
import pandas as pd
from datetime import datetime, timedelta

class DORAMetrics:
    def __init__(self, deployments: pd.DataFrame, incidents: pd.DataFrame):
        """
        deployments columns:
          - timestamp: Deployment time
          - commit_hash: Commit deployed
          - environment: Target environment
          - status: success/failed
          - team: Team name

        incidents columns:
          - timestamp: Incident start time
          - resolved_at: Incident resolution time
          - severity: SEV-0/1/2/3
          - cause_commit: Commit that caused incident
          - team: Team name
        """
        self.deployments = deployments
        self.incidents = incidents

    def deployment_frequency(self, period_days: int = 30) -> dict:
        """How often the team deploys to production."""
        cutoff = datetime.now() - timedelta(days=period_days)
        prod_deploys = self.deployments[
            (self.deployments['timestamp'] >= cutoff) &
            (self.deployments['environment'] == 'production') &
            (self.deployments['status'] == 'success')
        ]

        total = len(prod_deploys)
        per_day = total / period_days

        # Classification (DORA elite/high/medium/low)
        if per_day >= 1:
            classification = "Elite"
        elif per_day >= 1/7:  # Weekly
            classification = "High"
        elif per_day >= 1/30:  # Monthly
            classification = "Medium"
        else:
            classification = "Low"

        return {
            "total_deployments": total,
            "deployments_per_day": round(per_day, 2),
            "classification": classification,
            "period_days": period_days,
        }

    def lead_time_for_changes(self) -> dict:
        """Time from code commit to production deployment."""
        # Merge deployments with commit data
        lead_times = []

        for _, deploy in self.deployments.iterrows():
            if deploy['environment'] != 'production' or deploy['status'] != 'success':
                continue

            # Get commit time (from git log or VCS API)
            commit_time = self._get_commit_time(deploy['commit_hash'])
            deploy_time = deploy['timestamp']

            if commit_time:
                lead_time = (deploy_time - commit_time).total_seconds() / 3600  # hours
                lead_times.append(lead_time)

        if not lead_times:
            return {"median_hours": None, "classification": "N/A"}

        median = sorted(lead_times)[len(lead_times) // 2]
        p90 = sorted(lead_times)[int(len(lead_times) * 0.9)]

        # DORA classification
        if median < 1:  # < 1 hour
            classification = "Elite"
        elif median < 24 * 7:  # < 1 week
            classification = "High"
        elif median < 24 * 30:  # < 1 month
            classification = "Medium"
        else:
            classification = "Low"

        return {
            "median_hours": round(median, 1),
            "p90_hours": round(p90, 1),
            "classification": classification,
            "sample_size": len(lead_times),
        }

    def change_failure_rate(self, period_days: int = 30) -> dict:
        """Percentage of deployments causing production failures."""
        cutoff = datetime.now() - timedelta(days=period_days)

        total_deploys = len(self.deployments[
            (self.deployments['timestamp'] >= cutoff) &
            (self.deployments['environment'] == 'production') &
            (self.deployments['status'] == 'success')
        ])

        # Incidents caused by deployments in this period
        failure_incidents = self.incidents[
            (self.incidents['timestamp'] >= cutoff) &
            (self.incidents['cause_commit'].notna())
        ]

        if total_deploys == 0:
            return {"rate": 0, "classification": "N/A"}

        rate = len(failure_incidents) / total_deploys * 100

        if rate < 5:
            classification = "Elite"
        elif rate < 10:
            classification = "High"
        elif rate < 15:
            classification = "Medium"
        else:
            classification = "Low"

        return {
            "rate": round(rate, 1),
            "total_incidents": len(failure_incidents),
            "total_deployments": total_deploys,
            "classification": classification,
        }

    def mttr(self, period_days: int = 30) -> dict:
        """Mean Time to Recovery from production failures."""
        cutoff = datetime.now() - timedelta(days=period_days)

        resolved_incidents = self.incidents[
            (self.incidents['timestamp'] >= cutoff) &
            (self.incidents['resolved_at'].notna()) &
            (self.incidents['severity'].isin(['SEV-0', 'SEV-1']))
        ]

        if resolved_incidents.empty:
            return {"median_hours": None, "classification": "N/A"}

        recovery_times = (
            resolved_incidents['resolved_at'] - resolved_incidents['timestamp']
        ).dt.total_seconds() / 3600  # hours

        median = recovery_times.median()
        p90 = recovery_times.quantile(0.9)

        if median < 1:  # < 1 hour
            classification = "Elite"
        elif median < 24:  # < 1 day
            classification = "High"
        elif median < 24 * 7:  # < 1 week
            classification = "Medium"
        else:
            classification = "Low"

        return {
            "median_hours": round(median, 1),
            "p90_hours": round(p90, 1),
            "classification": classification,
            "incident_count": len(resolved_incidents),
        }

    def _get_commit_time(self, commit_hash: str) -> datetime | None:
        """Get commit timestamp from git/VCS API."""
        # Implementation depends on your VCS (GitHub, GitLab, etc.)
        pass

    def full_report(self) -> dict:
        """Generate complete DORA metrics report."""
        return {
            "generated_at": datetime.now().isoformat(),
            "period_days": 30,
            "deployment_frequency": self.deployment_frequency(),
            "lead_time": self.lead_time_for_changes(),
            "change_failure_rate": self.change_failure_rate(),
            "mttr": self.mttr(),
        }
```

### SPACE Framework Measurement

```markdown
# SPACE Framework Dashboard

## Satisfaction & Well-being

| Metric                 | Source                   | Target        | Current |
| ---------------------- | ------------------------ | ------------- | ------- |
| Developer satisfaction | Monthly survey           | > 4.0/5.0     | 4.2     |
| Burnout risk           | Survey (Maslach items)   | < 20% at risk | 15%     |
| Work-life balance      | Survey                   | > 3.5/5.0     | 3.8     |
| Psychological safety   | Survey (Edmondson scale) | > 4.0/5.0     | 4.1     |

## Performance

| Metric               | Source          | Target         | Current |
| -------------------- | --------------- | -------------- | ------- |
| DORA composite score | CI/CD data      | Elite          | High    |
| Defect escape rate   | Bug tracker     | < 5%           | 3.2%    |
| Code review quality  | Review analysis | > 80% thorough | 85%     |

## Activity

| Metric                      | Source     | Target            | Current |
| --------------------------- | ---------- | ----------------- | ------- |
| PRs per developer per week  | GitHub API | 3-7               | 4.5     |
| Code commits per week       | Git        | N/A (trend only)  | Stable  |
| Documentation contributions | Wiki/Docs  | > 2 per dev/month | 3.1     |

⚠️ Warning: Activity metrics should NEVER be used for individual performance evaluation.
They indicate system throughput, not individual productivity.

## Communication & Collaboration

| Metric                   | Source               | Target              | Current   |
| ------------------------ | -------------------- | ------------------- | --------- |
| PR review response time  | GitHub API           | < 4 hours           | 2.3 hours |
| Cross-team collaboration | Git (cross-repo PRs) | > 10% of PRs        | 12%       |
| Knowledge sharing        | Tech talks, docs     | > 1 per dev/quarter | 1.4       |

## Efficiency & Flow

| Metric                         | Source        | Target      | Current  |
| ------------------------------ | ------------- | ----------- | -------- |
| Flow time (start to deploy)    | CI/CD         | < 2 days    | 1.5 days |
| Flow efficiency (active/total) | Time tracking | > 30%       | 28%      |
| Interruption rate              | Survey        | < 3 per day | 4.2      |
| Build time (P95)               | CI monitoring | < 15 min    | 12 min   |
```

**Developer survey design:**

```markdown
# Developer Experience Survey — Q1 2026

## Instructions

- Anonymous responses
- Takes ~10 minutes
- All questions use 5-point Likert scale unless noted
- Open-ended questions welcome additional context

## Satisfaction

1. Overall, how satisfied are you with your developer experience?
   [1 - Very Dissatisfied] [2] [3] [4] [5 - Very Satisfied]

2. How would you rate the quality of our codebase?
   [1 - Very Poor] [2] [3] [4] [5 - Excellent]

3. How often do you feel blocked waiting for:
   a. Code reviews: [Never] [Rarely] [Sometimes] [Often] [Always]
   b. CI/CD pipeline: [Never] [Rarely] [Sometimes] [Often] [Always]
   c. Environment setup: [Never] [Rarely] [Sometimes] [Often] [Always]
   d. Dependencies from other teams: [Never] [Rarely] [Sometimes] [Often] [Always]

## Efficiency

4. What percentage of your time is spent on productive development work?
   [0-20%] [20-40%] [40-60%] [60-80%] [80-100%]

5. How long does it take to get a meaningful code review?
   [< 1 hour] [1-4 hours] [4-8 hours] [1 day] [> 1 day]

6. How often do you experience build/CI failures that are not your fault?
   [Never] [Rarely] [Sometimes] [Often] [Always]

## Open-ended

7. What is the biggest frustration in your daily development workflow?
   [Free text]

8. What one change would most improve your productivity?
   [Free text]

## Demographics (optional)

- Team: [Dropdown]
- Experience level: [Junior] [Mid] [Senior] [Staff+]
- Primary language: [Dropdown]
```

### Code Review Cycle Analysis

```python
# code_review_analysis.py
import pandas as pd
from datetime import datetime

class ReviewAnalyzer:
    def __init__(self, pull_requests: pd.DataFrame):
        """
        pull_requests columns:
          - id: PR number
          - author: PR author
          - reviewers: List of reviewer names
          - created_at: PR creation time
          - merged_at: PR merge time
          - lines_added: Lines added
          - lines_deleted: Lines deleted
          - comments: Number of review comments
          - review_rounds: Number of review rounds
          - merged: Whether PR was merged
          - labels: PR labels
        """
        self.pr_data = pull_requests

    def review_cycle_time(self) -> dict:
        """Analyze time from PR creation to merge."""
        merged = self.pr_data[self.pr_data['merged'] == True].copy()
        merged['cycle_time_hours'] = (
            merged['merged_at'] - merged['created_at']
        ).dt.total_seconds() / 3600

        return {
            "median_hours": merged['cycle_time_hours'].median(),
            "p50_hours": merged['cycle_time_hours'].median(),
            "p90_hours": merged['cycle_time_hours'].quantile(0.9),
            "p99_hours": merged['cycle_time_hours'].quantile(0.99),
            "total_merged": len(merged),
        }

    def review_size_analysis(self) -> pd.DataFrame:
        """Correlate PR size with review time and quality."""
        merged = self.pr_data[self.pr_data['merged'] == True].copy()
        merged['total_lines'] = merged['lines_added'] + merged['lines_deleted']
        merged['cycle_time_hours'] = (
            merged['merged_at'] - merged['created_at']
        ).dt.total_seconds() / 3600

        # Size buckets
        merged['size_bucket'] = pd.cut(
            merged['total_lines'],
            bins=[0, 50, 200, 500, 1000, float('inf')],
            labels=['Tiny (<50)', 'Small (50-200)', 'Medium (200-500)',
                    'Large (500-1000)', 'Huge (>1000)']
        )

        return merged.groupby('size_bucket').agg(
            count=('id', 'count'),
            median_cycle_time=('cycle_time_hours', 'median'),
            median_comments=('comments', 'median'),
            median_rounds=('review_rounds', 'median'),
        ).reset_index()

    def reviewer_load(self) -> pd.DataFrame:
        """Analyze review load distribution across team."""
        # Expand reviewers list
        exploded = self.pr_data.explode('reviewers')

        reviewer_stats = exploded.groupby('reviewers').agg(
            reviews_assigned=('id', 'count'),
            avg_response_time_hours=('response_time_hours', 'mean'),
            avg_comments=('comments', 'mean'),
        ).reset_index()

        reviewer_stats.columns = ['reviewer', 'reviews', 'avg_response_time', 'avg_comments']
        reviewer_stats = reviewer_stats.sort_values('reviews', ascending=False)

        return reviewer_stats

    def bottlenecks(self) -> list:
        """Identify review bottlenecks."""
        bottlenecks = []

        # Long review times
        cycle_times = self.review_cycle_time()
        if cycle_times['p90_hours'] > 24:
            bottlenecks.append({
                "type": "slow_reviews",
                "severity": "high",
                "detail": f"P90 review cycle time is {cycle_times['p90_hours']:.1f} hours (> 24h target)",
            })

        # Uneven reviewer load
        load = self.reviewer_load()
        if len(load) > 0:
            max_reviews = load['reviews'].max()
            min_reviews = load['reviews'].min()
            if min_reviews > 0 and max_reviews / min_reviews > 3:
                bottlenecks.append({
                    "type": "uneven_load",
                    "severity": "medium",
                    "detail": f"Reviewer load ratio is {max_reviews/min_reviews:.1f}x (target: < 3x)",
                })

        # Large PRs
        size_analysis = self.review_size_analysis()
        huge_prs = size_analysis[
            size_analysis.index == 'Huge (>1000)'
        ]
        if not huge_prs.empty and huge_prs['count'].values[0] > 0:
            bottlenecks.append({
                "type": "large_prs",
                "severity": "medium",
                "detail": f"{huge_prs['count'].values[0]} PRs > 1000 lines this period",
            })

        return bottlenecks
```

**Code review quality metrics:**

| Metric                 | Good            | Concern                                | Action                                   |
| ---------------------- | --------------- | -------------------------------------- | ---------------------------------------- |
| Median review time     | < 4 hours       | > 8 hours                              | Add reviewers, set expectations          |
| PR size (median)       | < 200 lines     | > 400 lines                            | Encourage smaller PRs                    |
| Review rounds          | < 2             | > 3                                    | Improve PR quality, clearer requirements |
| Comments per PR        | 3-8             | < 1 (rubber stamp) or > 15 (too large) | Adjust review expectations               |
| Reviewer load balance  | < 3x difference | > 5x difference                        | Rotate reviewers, distribute load        |
| Unreviewed PRs (> 24h) | 0               | > 5% of open PRs                       | Add reviewers, set SLAs                  |

## Pipeline Integration

**Stage 4 (Implementation Plan):** Developer analytics tooling provisioned. DORA metric collection configured. Baseline measurements established.

**Stage 5 (Development):** CI/CD pipelines instrumented for DORA data collection. Code review data captured via VCS APIs. Developer survey conducted.

**Stage 7 (Testing):** Test suite execution time tracked as efficiency metric. Flaky test rate monitored as quality indicator.

**Stage 10 (Release Readiness):** DORA metrics reported as part of release readiness. Developer satisfaction survey results reviewed.

## Quality Standards

| Metric                         | Target                             | Measurement          |
| ------------------------------ | ---------------------------------- | -------------------- |
| DORA data completeness         | 100% of deployments tracked        | CI/CD audit          |
| Developer survey response rate | > 60%                              | Survey analytics     |
| Code review data accuracy      | 100% of PRs analyzed               | VCS API audit        |
| Metric freshness               | Updated daily                      | Pipeline monitoring  |
| Actionable insights            | At least 1 improvement per quarter | Improvement tracking |
| SPACE dimension coverage       | All 5 dimensions measured          | Dashboard audit      |
