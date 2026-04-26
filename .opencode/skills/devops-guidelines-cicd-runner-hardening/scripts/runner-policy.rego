package pipeline
import rego.v1

deny_unpinned_actions contains msg if {
    some workflow in input.workflows
    some job in workflow.jobs
    some step in job.steps
    uses := step.uses
    not re_match("@[a-f0-9]{40}$", uses)
    msg := sprintf("Unpinned action: '%s' — pin to commit SHA", [uses])
}

deny_broad_permissions contains msg if {
    some workflow in input.workflows
    workflow.permissions == "write-all"
    msg := sprintf("Workflow uses 'write-all' — use least privilege", [workflow.name])
}