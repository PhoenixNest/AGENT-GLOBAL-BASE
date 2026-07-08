#!/usr/bin/env bash
# H-P03: UserPromptSubmit — ASE Compliance Quality Gate (bash port)
# Runs FIRST in the UserPromptSubmit chain. Blocks prompts that would
# instruct agents to violate ASE governance rules, skip pipeline gates,
# override P0/P1 severity, or access denied files.

raw_input=$(cat)

prompt=$(echo "$raw_input" | python3 -c "import sys,json
try:
    d=json.load(sys.stdin)
except Exception:
    sys.exit(0)
print(d.get('prompt','') or '')")

[ -z "$prompt" ] && exit 0

detected=$(PROMPT="$prompt" python3 -c "
import os,re
p=os.environ['PROMPT']
violations=[
 (r'skip.{0,40}(stage|gate|pipeline|review|approval)','Pipeline stages cannot be skipped — CLAUDE.md §8 (hard stop)'),
 (r'(downgrade|change|override|ignore|bypass).{0,40}(P0|P1|severity|defect|critical|blocker)','P0/P1 defect classification is non-overridable — CLAUDE.md §8'),
 (r'(remove|weaken|disable|trim|strip).{0,30}(feature|security|functionality|test).{0,30}(pass|review|gate|check)','Trim-to-Pass is a P0 defect — removing features to pass a review is blocked — CLAUDE.md §8'),
 (r'(force.{0,10}push|push.{0,10}--force).{0,20}(master|main)','Force-pushing to master is prohibited — CLAUDE.md §6, rules/git-workflow.md'),
 (r'auto.{0,20}advance.{0,20}(stage|gate|pipeline)','Auto-advancing past User Approval gates is forbidden — CLAUDE.md §8'),
]
for pat,rule in violations:
    if re.search(pat,p,re.IGNORECASE):
        print('  * '+rule)
")

[ -z "$detected" ] && exit 0

reason="[PROMPT QUALITY GATE — H-P03] ASE Compliance Violation Detected

The following governance rules would be violated:
$detected

This prompt has been blocked. Please rephrase within the ASE governance framework.
Reference: CLAUDE.md §1, §6, §8 | core-component-00/agent-systems-engineering/governance/"

REASON="$reason" python3 -c "import os,json; print(json.dumps({'decision':'block','reason':os.environ['REASON'],'hookSpecificOutput':{'hookEventName':'UserPromptSubmit'}}))"
exit 0
