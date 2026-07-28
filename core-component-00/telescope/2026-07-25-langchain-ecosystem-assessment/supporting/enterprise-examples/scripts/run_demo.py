#!/usr/bin/env python
"""Run the Telescope Research Assistant end to end from the command line.

Default mode (no arguments, no API key) uses `FakeListChatModel` and runs
fully offline — this is the path actually exercised by tests/. If
ANTHROPIC_API_KEY is set in the environment, pass --real to route the draft
step through a real Anthropic model instead; that path has NOT been executed
in this deliverable (no credentials were available) and is offered as-is.

Usage:
    .venv/Scripts/python.exe scripts/run_demo.py "What does LangGraph support?"
    .venv/Scripts/python.exe scripts/run_demo.py --real "..."   # needs ANTHROPIC_API_KEY
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from langgraph.types import Command  # noqa: E402

from cc00_langchain.cc00_path import Document, FixedSizeChunker, RAGPipeline  # noqa: E402
from cc00_langchain.graphs.research_assistant import build_graph, file_checkpointer  # noqa: E402

SAMPLE_CORPUS = [
    Document(
        id="langgraph-durability",
        text=(
            "LangGraph provides durable execution: agent state is checkpointed after every "
            "step, so a run can be interrupted, persisted, and resumed later — including "
            "across process restarts — without losing progress."
        ),
        acl_roles=["public"],
    ),
    Document(
        id="langgraph-interrupt",
        text=(
            "The interrupt() primitive pauses a graph mid-execution and returns control to "
            "the caller. Resuming with Command(resume=...) continues from exactly where "
            "execution paused, making it a clean mechanism for human-in-the-loop approval."
        ),
        acl_roles=["public"],
    ),
    Document(
        id="internal-roadmap",
        text="Internal Q3 roadmap: LangChain pilot adoption decision still pending CEO sign-off.",
        acl_roles=["staff"],
    ),
]


def _build_model(use_real: bool):
    if not use_real:
        from langchain_core.language_models.fake_chat_models import FakeListChatModel

        return FakeListChatModel(
            responses=[
                "Finding: LangGraph's checkpointing and interrupt() primitives together "
                "provide durable, resumable human-in-the-loop execution (per "
                "langgraph-durability, langgraph-interrupt)."
            ]
        )

    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit(
            "--real requires ANTHROPIC_API_KEY to be set. This path has not been executed "
            "in this deliverable — no credentials were available. Falling back is not "
            "automatic; fix the environment or drop --real."
        )
    from langchain.chat_models import init_chat_model

    # UNVERIFIED in this deliverable: no live call was made against this model
    # id. Confirm it against your pinned langchain-anthropic version before
    # relying on it — see requirements.lock.txt for the resolved version.
    return init_chat_model("anthropic:claude-sonnet-5", timeout=60, max_retries=0)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("question", nargs="?", default="What does LangGraph provide?")
    parser.add_argument("--role", default="public", choices=["public", "staff"])
    parser.add_argument("--real", action="store_true", help="Use a real Anthropic model (needs ANTHROPIC_API_KEY)")
    parser.add_argument("--auto-approve", action="store_true", help="Skip the interactive approval prompt")
    args = parser.parse_args()

    pipeline = RAGPipeline(chunker=FixedSizeChunker(chunk_size=300), top_k=5)
    pipeline.ingest(SAMPLE_CORPUS)

    model = _build_model(args.real)
    project_root = Path(__file__).resolve().parent.parent
    checkpointer = file_checkpointer(project_root / ".demo-output" / "checkpoints.sqlite")
    graph = build_graph(pipeline, model, checkpointer, project_root / ".demo-output" / "reports")

    config = {"configurable": {"thread_id": f"demo-{abs(hash(args.question)) % 100000}"}}
    result = graph.invoke({"question": args.question, "user_role": args.role}, config)

    print("\n--- DRAFT ---")
    print(result.get("draft_report", "(no draft)"))
    print("-------------\n")

    if "__interrupt__" not in result:
        print("Graph did not pause (unexpected) — nothing to approve.")
        return

    if args.auto_approve:
        approved = True
    else:
        answer = input("Write this draft to .demo-output/reports/? [y/N] ").strip().lower()
        approved = answer == "y"

    final = graph.invoke(Command(resume={"approved": approved}), config)
    print(f"Status: {final.get('status')}")
    if final.get("status") == "written":
        print(f"Written to: {final['pending_write']['path']}")


if __name__ == "__main__":
    main()
