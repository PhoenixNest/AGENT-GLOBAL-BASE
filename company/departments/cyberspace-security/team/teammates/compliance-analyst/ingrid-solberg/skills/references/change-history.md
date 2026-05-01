---
version: "1.0.0"
---

---- | ------------------------------------ | -------------- |
| 2026-03-15 | Quarterly review — no changes needed | Ingrid Solberg |
| 2025-12-15 | Updated to reflect OIDC migration | Ingrid Solberg |
| 2025-09-01 | Initial control documentation | Ingrid Solberg |

```

### 3. Evidence Collection Automation

**Evidence Collection Pipeline Architecture:**

```

┌─────────────────────────────────────────────────────────────┐
│ Evidence Sources │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────┐│
│ │ GitHub │ │ AWS │ │ Okta │ │ SAST/DAST ││
│ │ API │ │ CloudTrail│ │ Admin │ │ Pipeline ││
│ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────────┬─────────┘│
│ │ │ │ │ │
└───────┼─────────────┼─────────────┼────────────────┼──────────┘
│ │ │ │
▼ ▼ ▼ ▼
┌─────────────────────────────────────────────────────────────┐
│ Evidence Collection Layer │
│ ┌──────────────────────────────────────────────────────┐ │
│ │ Lambda Functions (scheduled & event-driven) │ │
│ │ • github-access-export.py │ │
│ │ • cloudtrail-log-aggregator.py │ │
│ │ • okta-mfa-report.py │ │
│ │ • sast-results-export.py │ │
│ └──────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│ Evidence Storage Layer │
│ ┌──────────────────────────────────────────────────────┐ │
│ │ S3 Bucket: compliance-evidence-prod │ │
│ │ ├── SOC2/ │ │
│ │ │ ├── CC6/ │ │
│ │ │ │ ├── 2026-03/ │ │
│ │ │ │ │ ├── EV-CC6.1-01-2026-03.json │ │
│ │ │ │ │ └── EV-CC6.1-01-2026-03.sha256 │ │
│ │ │ │ └── ... │ │
│ │ │ └── ... │ │
│ │ ├── PCI-DSS/ │ │
│ │ ├── GDPR/ │ │
│ │ └── ISO27001/ │ │
│ └──────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│ Evidence Index & Retrieval │
│ ┌──────────────────────────────────────────────────────┐ │
│ │ DynamoDB: evidence-index │ │
│ │ • Evidence ID │ │
│ │ • Control ID mapping │ │
│ │ • Collection date │ │
│ │ • S3 location │ │
│ │ • Integrity hash (SHA-256) │ │
│ │ • Retention expiry │ │
│ └──────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘

````

**Evidence Collection Script Template:**

```python
#!/usr/bin/env python3
"""
Evidence Collection Script — GitHub Access Export
Collects: EV-CC6.1-01 — GitHub access list export
Frequency: Quarterly
"""

import json
import hashlib
import boto3
import requests
from datetime import datetime
import os

def collect_github_access():
    """Export GitHub organization member and repository access data."""

    # Configuration
    org = os.environ['GITHUB_ORG']
    token = os.environ['GITHUB_TOKEN']
    bucket = os.environ['EVIDENCE_BUCKET']

    # Collect organization members
    members = []
    page = 1
    while True:
        resp = requests.get(
            f'https://api.github.com/orgs/{org}/members',
            headers={'Authorization': f'token {token}'},
            params={'page': page, 'per_page': 100}
        )
        if not resp.json():
            break
        members.extend(resp.json())
        page += 1

    # Collect repository access
    repos = []
    for member in members:
        member_repos = requests.get(
            f'https://api.github.com/orgs/{org}/repos',
            headers={'Authorization': f'token {token}'}
        ).json()
        repos.append({
            'login': member['login'],
            'repo_count': len(member_repos),
            'repos': [r['name'] for r in member_repos]
        })

    # Build evidence package
    evidence = {
        'evidence_id': 'EV-CC6.1-01',
        'control_id': 'CC6.1',
        'collection_date': datetime.utcnow().isoformat(),
        'collected_by': 'evidence-collection-lambda',
        'framework': 'SOC2',
        'data': {
            'organization': org,
            'total_members': len(members),
            'members': members,
            'repository_access': repos
        }
    }

    # Calculate integrity hash
    data_json = json.dumps(evidence['data'], sort_keys=True).encode()
    evidence['integrity_hash'] = hashlib.sha256(data_json).hexdigest()

    # Upload to S3
    s3 = boto3.client('s3')
    month = datetime.utcnow().strftime('%Y-%m')
    key = f"SOC2/CC6/{month}/EV-CC6.1-01-{month}.json"

    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=json.dumps(evidence, indent=2),
        ServerSideEncryption='aws:kms'
    )

    # Update evidence index (DynamoDB)
    dynamodb = boto3.client('dynamodb')
    dynamodb.put_item(
        TableName='evidence-index',
        Item={
            'evidence_id': {'S': 'EV-CC6.1-01'},
            'collection_date': {'S': evidence['collection_date']},
            's3_location': {'S': f's3://{bucket}/{key}'},
            'integrity_hash': {'S': evidence['integrity_hash']},
            'retention_expiry': {'S': '2029-12-31'},
            'status': {'S': 'collected'}
        }
    )

    return evidence

if __name__ == '__main__':
    collect_github_access()
    print("Evidence collected and stored successfully.")
````

### 4. Remediation Plan Documentation

**Remediation Plan Template:**

```markdown
# Remediation Plan — [Finding Title]
```
