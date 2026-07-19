#!/usr/bin/env bash
# H-P02: UserPromptSubmit — Pipeline Stage Context Injector (bash port)
# Runs LAST in the UserPromptSubmit chain (after optimizer). Detects pipeline-stage
# signals in the prompt and injects the canonical stage reference as additionalContext
# so Claude reads the gate criteria before responding.

raw_input=$(cat)

prompt=$(echo "$raw_input" | python3 -c "import sys,json
try:
    d=json.load(sys.stdin)
except Exception:
    sys.exit(0)
print(d.get('prompt','') or '')")

[ -z "$prompt" ] && exit 0
echo "$prompt" | grep -qE '^[[:space:]]*/' && exit 0

# Ordered stage detection — returns 'stage|label|hint' for the first matching signal
detected=$(PROMPT="$prompt" python3 -c "
import os,re
p=os.environ['PROMPT']
signals=[
 (r'(Stage 1\b|requirements gathering|PRD\b|SRD\b|product requirements|user stories|acceptance criteria doc)',1,'Requirements + PRD/SRD','Deliverables: PRD + SRD (must travel together). User Approval gate at end.'),
 (r'(Stage 2\b|prototype|IDS\b|design spec|wireframe|mockup|interaction design)',2,'Prototype + IDS','Deliverable: Interaction Design Spec (IDS). CDO owns this stage.'),
 (r'(Stage 3\b|UML\b|ADR\b|architecture decision|technology decision|TSD\b|tech stack)',3,'UML + Architecture Decisions','Technology Decision Lock applies at approval. ADRs are immutable after sign-off.'),
 (r'(Stage 4\b|implementation plan|gantt|task breakdown|sprint planning|work breakdown)',4,'Implementation Plan + Gantt','Progress monitoring (progress.md, session-log.md, checkpoint.json) starts here.'),
 (r'(Stage 5\b|\bfeature implementation\b|write the code|build the feature|android impl|ios impl|backend impl)',5,'Development','CTO owns cross-team coordination. Platform engineers own platform tracks.'),
 (r'(Stage 6\b|code review|architectural audit|review the code|code quality review|defect clas)',6,'Code Review','Full review panel. Stage 6 remediation restarts the full panel — no partial re-entry.'),
 (r'(Stage 7\b|\bQA\b|testing phase|test cases|unit tests|integration tests|test suite)',7,'Testing + QA','Coverage target: 80%+ for business logic. P0/P1 defects block release.'),
 (r'(Stage 8\b|integrity|regression|security audit|penetration|MASVS|stealthy weakening)',8,'Integrity + Security','Trim-to-Pass is itself a P0 defect. No feature removal to pass this stage.'),
 (r'(Stage 9\b|localization|i18n\b|l10n\b|translation|string extraction|RTL)',9,'Localization (i18n)','CTO-L owns this stage. ICU MessageFormat for plurals and gender. All strings must be externalized.'),
 (r'(Stage 10\b|release\b|deploy\b|ship\b|launch\b|go.no.go|store submission|production deploy)',10,'Release','Final gate: all P0/P1 resolved, regression + security scan + accessibility audit complete.'),
]
for pat,stage,label,hint in signals:
    if re.search(pat,p,re.IGNORECASE):
        print(f'{stage}|{label}|{hint}')
        break
")

[ -z "$detected" ] && exit 0

stage="${detected%%|*}"
rest="${detected#*|}"
label="${rest%%|*}"
hint="${rest#*|}"

# Resolve workspace root: hooks dir -> .claude -> root
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
workspace_root="$(cd "$script_dir/../.." && pwd)"

pipeline_paths=(
    "company/pipeline/mobile-development/pipeline.md"
    "company/pipeline/web-development/pipeline.md"
    "company/pipeline/backend-api/pipeline.md"
    "company/pipeline/full-stack/pipeline.md"
)

doc_list=""
for rel in "${pipeline_paths[@]}"; do
    if [ -f "$workspace_root/$rel" ]; then
        doc_list="$doc_list  - $workspace_root/$rel
"
    fi
done
if [ -z "$doc_list" ]; then
    doc_list="  (no pipeline docs found at expected paths)"
else
    doc_list="$(printf '%s' "$doc_list" | sed -e 's/[[:space:]]*$//')"
fi

msg="[PIPELINE CONTEXT INJECTOR — H-P02]
Detected stage signal: Stage $stage — $label
Stage hint: $hint

Before responding, read the Stage $stage section of the relevant pipeline.md:
$doc_list

Key reminders for Stage $stage:
- Satisfy all gate criteria before presenting the deliverable
- If this stage has a User Approval gate (marked with checkmark), present the deliverable
  and explicitly request sign-off — do not auto-advance
- P0/P1 defects are non-overridable and block progression"

MSG="$msg" python3 -c "import os,json; print(json.dumps({'hookSpecificOutput':{'hookEventName':'UserPromptSubmit','additionalContext':os.environ['MSG']}}))"
exit 0
