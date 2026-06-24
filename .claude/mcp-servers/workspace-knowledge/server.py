# ── venv bootstrap (MUST be first, before any other imports) ──────────────
import sys
from pathlib import Path as _Path

_venv_sp = _Path(__file__).parent / ".venv" / "Lib" / "site-packages"
if _venv_sp.exists():
    sys.path.insert(0, str(_venv_sp))
# ─────────────────────────────────────────────────────────────────────────

import os
import re
from enum import Enum
from pathlib import Path
from typing import Any

from fastmcp import FastMCP

WORKSPACE_ROOT = Path(os.getenv("WORKSPACE_ROOT", "."))

mcp = FastMCP("workspace-knowledge")


class SearchTier(Enum):
    BM25 = "bm25"
    RAWFS = "rawfs"


class BM25Engine:
    KEY_DIRS = [
        "company",
        "studio",
        "core-component-00",
        "telescope",
        ".claude/rules",
        ".claude/skills",
        ".claude/agents",
        ".claude/mcp-servers",
    ]

    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self._tier = SearchTier.RAWFS
        self._degradation_reason: str | None = None
        self._chunks: list[dict] = []
        self._bm25 = None
        self._initialize_search_engine()

    def _extract_chunks(self, file_path: Path) -> list[dict]:
        """Split a markdown file into overlapping 512-word paragraph chunks."""
        try:
            text = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return []

        rel_path = str(file_path.relative_to(self.workspace_root)).replace("\\", "/")

        # Extract YAML frontmatter description
        fm_desc = ""
        fm_match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
        if fm_match:
            desc_m = re.search(r"^description:\s*(.+)$", fm_match.group(1), re.MULTILINE)
            if desc_m:
                fm_desc = desc_m.group(1).strip()

        # Split on double newlines
        paragraphs = re.split(r"\n{2,}", text)

        # Track current section header
        current_section = fm_desc or rel_path
        words_buffer = []
        chunk_idx = 0
        chunks = []
        CHUNK_SIZE = 512
        OVERLAP = 64

        for para in paragraphs:
            # Update section from headers
            header_m = re.match(r"^#{1,3}\s+(.+)$", para.strip(), re.MULTILINE)
            if header_m:
                current_section = header_m.group(1).strip()

            para_words = para.split()
            words_buffer.extend(para_words)

            while len(words_buffer) >= CHUNK_SIZE:
                chunk_text = " ".join(words_buffer[:CHUNK_SIZE])
                chunks.append(
                    {
                        "text": chunk_text,
                        "file_path": str(file_path),
                        "rel_path": rel_path,
                        "section": current_section,
                        "chunk_idx": chunk_idx,
                    }
                )
                chunk_idx += 1
                words_buffer = words_buffer[CHUNK_SIZE - OVERLAP:]

        # Remaining words
        if words_buffer:
            chunks.append(
                {
                    "text": " ".join(words_buffer),
                    "file_path": str(file_path),
                    "rel_path": rel_path,
                    "section": current_section,
                    "chunk_idx": chunk_idx,
                }
            )

        return chunks

    def _initialize_search_engine(self):
        """Try to build BM25 index; fall back to RAWFS on failure."""
        try:
            from rank_bm25 import BM25Okapi
        except ImportError:
            self._tier = SearchTier.RAWFS
            self._degradation_reason = "rank_bm25 not installed"
            return

        try:
            all_chunks = []
            for dir_name in self.KEY_DIRS:
                dir_path = self.workspace_root / dir_name
                if not dir_path.exists():
                    continue
                for md_file in dir_path.rglob("*.md"):
                    all_chunks.extend(self._extract_chunks(md_file))

            if not all_chunks:
                self._tier = SearchTier.RAWFS
                self._degradation_reason = "No markdown files found"
                return

            self._chunks = all_chunks
            tokenized = [c["text"].lower().split() for c in self._chunks]
            self._bm25 = BM25Okapi(tokenized)
            self._tier = SearchTier.BM25
            self._degradation_reason = None
        except Exception as exc:
            self._tier = SearchTier.RAWFS
            self._degradation_reason = f"BM25 index build failed: {exc}"

    def _search_bm25(self, query: str, top_k: int) -> list[dict]:
        scores = self._bm25.get_scores(query.lower().split())
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[: top_k * 3]
        seen_files = set()
        results = []
        for idx in top_indices:
            chunk = self._chunks[idx]
            if chunk["rel_path"] not in seen_files:
                seen_files.add(chunk["rel_path"])
                results.append(
                    {
                        "file": chunk["rel_path"],
                        "section": chunk["section"],
                        "score": float(scores[idx]),
                        "snippet": chunk["text"][:400],
                    }
                )
            if len(results) >= top_k:
                break
        return results

    def _search_rawfs(self, query: str, top_k: int) -> list[dict]:
        results = []
        query_lower = query.lower()
        for dir_name in self.KEY_DIRS:
            dir_path = self.workspace_root / dir_name
            if not dir_path.exists():
                continue
            for md_file in dir_path.rglob("*.md"):
                try:
                    content = md_file.read_text(encoding="utf-8", errors="ignore")
                    count = content.lower().count(query_lower)
                    if count > 0:
                        rel = str(md_file.relative_to(self.workspace_root)).replace("\\", "/")
                        idx = content.lower().find(query_lower)
                        snippet = content[max(0, idx - 100) : idx + 300]
                        results.append(
                            {"file": rel, "section": "", "score": float(count), "snippet": snippet}
                        )
                except Exception:
                    pass
        results.sort(key=lambda r: r["score"], reverse=True)
        return results[:top_k]

    def _search_with_fallback(self, query: str, top_k: int = 10) -> list[dict]:
        if self._tier == SearchTier.BM25:
            try:
                return self._search_bm25(query, top_k)
            except Exception as exc:
                self._tier = SearchTier.RAWFS
                self._degradation_reason = f"BM25 search failed: {exc}"
        return self._search_rawfs(query, top_k)

    def _meta_block(self) -> dict:
        return {
            "search_tier": self._tier.value,
            "degradation_reason": self._degradation_reason,
            "result_quality": self._tier.value,
            "rebuild_available": True,
        }

    def rebuild(self):
        self._chunks = []
        self._bm25 = None
        self._initialize_search_engine()

    def list_files(self) -> list[str]:
        seen = set()
        for chunk in self._chunks:
            seen.add(chunk["rel_path"])
        if seen:
            return sorted(seen)
        # RAWFS fallback
        files = []
        for dir_name in self.KEY_DIRS:
            dir_path = self.workspace_root / dir_name
            if dir_path.exists():
                for md_file in dir_path.rglob("*.md"):
                    files.append(
                        str(md_file.relative_to(self.workspace_root)).replace("\\", "/")
                    )
        return sorted(files)


engine = BM25Engine(WORKSPACE_ROOT)


@mcp.tool()
def search_docs(query: str, top_k: int = 10) -> dict[str, Any]:
    """BM25 keyword search across workspace markdown files with graceful fallback to raw-FS string matching.
    Returns ranked results with file path, section heading, relevance score, and text snippet."""
    results = engine._search_with_fallback(query, top_k)
    return {"query": query, "results": results, "_meta": engine._meta_block()}


@mcp.tool()
def retrieve_context(file_path: str) -> dict[str, Any]:
    """Retrieve the full content of a specific workspace document by its relative path."""
    target = WORKSPACE_ROOT / file_path
    if not target.exists():
        return {"error": f"File not found: {file_path}", "_meta": engine._meta_block()}
    try:
        content = target.read_text(encoding="utf-8", errors="ignore")
        return {"file_path": file_path, "content": content, "_meta": engine._meta_block()}
    except Exception as exc:
        return {"error": str(exc), "_meta": engine._meta_block()}


@mcp.tool()
def list_indexed_files() -> dict[str, Any]:
    """List all markdown files currently in the search index."""
    files = engine.list_files()
    return {"files": files, "count": len(files), "_meta": engine._meta_block()}


@mcp.tool()
def rebuild_index() -> dict[str, Any]:
    """Rebuild the BM25 search index from scratch, re-scanning all workspace markdown files."""
    engine.rebuild()
    return {"status": "rebuilt", "tier": engine._tier.value, "_meta": engine._meta_block()}


@mcp.tool()
def summarize_context(topics: list[str], max_docs_per_topic: int = 3) -> dict[str, Any]:
    """Pre-digest multi-document briefings for agent context slots.
    Returns top matching docs per topic, deduped across topics."""
    seen = set()
    combined = []
    for topic in topics:
        for r in engine._search_with_fallback(topic, max_docs_per_topic):
            if r["file"] not in seen:
                seen.add(r["file"])
                combined.append({**r, "topic": topic})
    return {
        "topics_covered": topics,
        "doc_count": len(combined),
        "results": combined,
        "_meta": engine._meta_block(),
    }


@mcp.tool()
def check_adr_precedent(technology: str) -> dict[str, Any]:
    """Surface prior ADRs before a Technology Decision.
    Returns matching ADR documents and whether precedent exists."""
    results = engine._search_with_fallback(f"ADR {technology}", top_k=10)
    adr_results = [r for r in results if "adr" in r["file"].lower() or "ADR" in r["snippet"]]
    if not adr_results:
        adr_results = engine._search_with_fallback(technology, top_k=10)
        adr_results = [r for r in adr_results if "adr" in r["file"].lower()]
    return {
        "technology": technology,
        "has_precedent": len(adr_results) > 0,
        "adr_count": len(adr_results),
        "results": adr_results,
        "_meta": engine._meta_block(),
    }


@mcp.tool()
def validate_pipeline_document(doc_path: str) -> dict[str, Any]:
    """Validate a workspace document against its structural requirements.
    Detects document type and checks for required sections."""
    target = WORKSPACE_ROOT / doc_path
    if not target.exists():
        return {"doc_path": doc_path, "valid": False, "error": "File not found"}

    try:
        content = target.read_text(encoding="utf-8", errors="ignore")
    except Exception as exc:
        return {"doc_path": doc_path, "valid": False, "error": str(exc)}

    name = target.name.lower()
    missing = []
    warnings = []
    doc_type = "generic"

    if name == "pipeline.md":
        doc_type = "pipeline"
        for required in ["Stage", "User Approval", "Deliverable"]:
            if required.lower() not in content.lower():
                missing.append(required)
    elif name == "profile.md":
        doc_type = "agent_profile"
        for field in ["name:", "role:", "authority:"]:
            if field not in content:
                missing.append(field)
        if not content.startswith("---"):
            warnings.append("Missing YAML frontmatter")
    else:
        doc_type = "generic_markdown"
        if not re.search(r"^#{1,2}\s+", content, re.MULTILINE):
            missing.append("At least one H1 or H2 heading")
        if len(content.strip()) < 50:
            warnings.append("Document appears nearly empty")

    return {
        "doc_path": doc_path,
        "doc_type": doc_type,
        "valid": len(missing) == 0,
        "missing_sections": missing,
        "warnings": warnings,
        "_meta": engine._meta_block(),
    }


if __name__ == "__main__":
    mcp.run()
