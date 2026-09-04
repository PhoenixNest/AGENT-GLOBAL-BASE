"""
Comparison logic for agent-memory vs. workspace-knowledge's `memory_instance`
health_check blocks — test support code, not a registered MCP tool.

Detects the class of regression where agent-memory's health_check reports
reachable=false with all-zero counts while workspace-knowledge, querying the
*same* qdrant-memory instance in the same breath, reports correctly. This
module is the pure divergence-detection logic that a live integration test
(test_cross_server_health_comparison.py) exercises against real output from
both servers; kept separate from that test file so its correctness can be
verified independently, with fixed, deterministic inputs and no live Qdrant
instance required at all.
"""
from typing import Any, Dict


def compare_memory_instance_health(block_a: Dict[str, Any], block_b: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compares two `memory_instance` health blocks (each shaped like
    compute_memory_instance_telemetry()'s return value: `reachable`,
    `point_counts`, ...) computed independently against what should be the
    same underlying qdrant-memory instance, and reports any divergence.

    Flags:
    - differing `reachable` between the two blocks
    - differing point count for any collection present in either block's
      `point_counts` (a collection missing from one side entirely is itself
      reported as a divergence, not silently ignored)

    Returns {"diverged": bool, "differences": [{"field", "a", "b"}, ...]}.
    Never raises: a missing/malformed key on either side is itself reported
    as a divergence via .get()'s default, not a KeyError — mirrors this
    workspace's graceful-degradation discipline even though this is pure,
    non-I/O comparison logic with nothing to actually "fail" at the network
    layer.
    """
    differences = []

    reachable_a = block_a.get("reachable")
    reachable_b = block_b.get("reachable")
    if reachable_a != reachable_b:
        differences.append({"field": "reachable", "a": reachable_a, "b": reachable_b})

    counts_a = block_a.get("point_counts") or {}
    counts_b = block_b.get("point_counts") or {}
    all_collections = sorted(set(counts_a) | set(counts_b))
    for collection in all_collections:
        count_a = counts_a.get(collection)
        count_b = counts_b.get(collection)
        if count_a != count_b:
            differences.append(
                {"field": f"point_counts.{collection}", "a": count_a, "b": count_b}
            )

    return {"diverged": len(differences) > 0, "differences": differences}
