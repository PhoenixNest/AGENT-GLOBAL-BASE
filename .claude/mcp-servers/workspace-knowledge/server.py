# ── venv bootstrap (MUST be first, before any other imports) ──────────────
import sys
from pathlib import Path as _Path

_venv_sp = _Path(__file__).parent / ".venv" / "Lib" / "site-packages"
if _venv_sp.exists():
    sys.path.insert(0, str(_venv_sp))
# ─────────────────────────────────────────────────────────────────────────

import json
import os
import re
import threading
from enum import Enum
from pathlib import Path
from typing import Any

from fastmcp import FastMCP

WORKSPACE_ROOT = Path(os.getenv("WORKSPACE_ROOT", "."))

mcp = FastMCP("workspace-knowledge")


class SearchTier(Enum):
    HYBRID = "hybrid"
    BM25 = "bm25"
    RAWFS = "rawfs"


class SearchEngine:
    KEY_DIRS = [
        "company",
        "studio",
        "core-component-00",
        "telescope"
    ]

    _INDEX_DIR = Path(__file__).parent  # runtime path via __file__

    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self._tier = SearchTier.RAWFS
        self._degradation_reason: str | None = None
        self._chunks: list[dict] = []
        self._bm25 = None
        self._model = None          # SentenceTransformer
        self._faiss_index = None    # faiss index object
        self._chunk_embeddings = None  # np.ndarray for reference
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
        """Initialization chain: HYBRID -> BM25 -> RAWFS."""
        # Try BM25 (fast, no download required)
        try:
            from rank_bm25 import BM25Okapi
        except ImportError:
            self._tier = SearchTier.RAWFS
            self._degradation_reason = "rank_bm25 not installed"
            return

        try:
            self._build_bm25_index(BM25Okapi)
            self._tier = SearchTier.BM25
        except Exception as e:
            self._tier = SearchTier.RAWFS
            self._degradation_reason = f"BM25 build failed: {e}"
            return

        # Launch FAISS in background so mcp.run() can start within the 30 s handshake window
        t = threading.Thread(target=self._init_faiss_background, daemon=True)
        t.start()

    def _init_faiss_background(self):
        """FAISS model load + encode runs off the critical path (background thread)."""
        try:
            import faiss
            import numpy as np
            from sentence_transformers import SentenceTransformer
            self._build_or_load_faiss_index(faiss, np, SentenceTransformer)
            self._tier = SearchTier.HYBRID
        except ImportError:
            self._degradation_reason = "sentence-transformers or faiss not installed — using BM25"
        except Exception as e:
            self._degradation_reason = f"FAISS init failed: {e} — using BM25"

    def _build_bm25_index(self, BM25Okapi):
        """Build the BM25 index from all markdown chunks."""
        all_chunks = []
        for dir_name in self.KEY_DIRS:
            dir_path = self.workspace_root / dir_name
            if dir_path.exists():
                for md_file in dir_path.rglob("*.md"):
                    all_chunks.extend(self._extract_chunks(md_file))
        if not all_chunks:
            raise RuntimeError("No markdown files found")
        self._chunks = all_chunks
        tokenized = [c["text"].lower().split() for c in self._chunks]
        self._bm25 = BM25Okapi(tokenized)

    def _build_or_load_faiss_index(self, faiss, np, SentenceTransformer):
        """Build or load a FAISS index with mtime-based delta detection."""
        index_file = self._INDEX_DIR / "faiss.index"
        state_file = self._INDEX_DIR / "index_state.json"

        # Compute current file mtimes
        current_mtimes = {}
        for dir_name in self.KEY_DIRS:
            dir_path = self.workspace_root / dir_name
            if dir_path.exists():
                for md_file in dir_path.rglob("*.md"):
                    rel = str(md_file.relative_to(self.workspace_root)).replace("\\", "/")
                    current_mtimes[rel] = md_file.stat().st_mtime

        # Load saved state
        saved_mtimes = {}
        if state_file.exists():
            try:
                saved_mtimes = json.loads(state_file.read_text())
            except Exception:
                pass

        # Check if index is stale
        needs_rebuild = (
            not index_file.exists()
            or current_mtimes != saved_mtimes
        )

        import torch
        _device = "cuda" if torch.cuda.is_available() else "cpu"
        model = SentenceTransformer("all-mpnet-base-v2", device=_device)

        if needs_rebuild:
            # Encode all chunks
            texts = [c["text"][:512] for c in self._chunks]
            embeddings = model.encode(texts, show_progress_bar=False, batch_size=64)
            embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
            dim = embeddings.shape[1]
            index = faiss.IndexFlatIP(dim)  # Inner product = cosine similarity after normalization
            index.add(embeddings.astype("float32"))
            faiss.write_index(index, str(index_file))
            state_file.write_text(json.dumps(current_mtimes))
            self._faiss_index = index
            self._model = model
        else:
            self._faiss_index = faiss.read_index(str(index_file))
            self._model = model

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

    def _search_semantic(self, query: str, top_k: int) -> list[dict]:
        """Dense vector search over the FAISS index using cosine similarity."""
        import numpy as np
        q_emb = self._model.encode([query])
        q_emb = q_emb / np.linalg.norm(q_emb, axis=1, keepdims=True)
        scores, indices = self._faiss_index.search(q_emb.astype("float32"), top_k * 3)
        results = []
        seen = set()
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0 or idx >= len(self._chunks):
                continue
            chunk = self._chunks[idx]
            if chunk["rel_path"] not in seen:
                seen.add(chunk["rel_path"])
                results.append({
                    "file": chunk["rel_path"],
                    "section": chunk["section"],
                    "score": float(score),
                    "snippet": chunk["text"][:400],
                })
            if len(results) >= top_k:
                break
        return results

    def _search_hybrid(self, query: str, top_k: int) -> list[dict]:
        """Reciprocal Rank Fusion (k=60) combining BM25 and semantic results."""
        K = 60
        bm25_results = self._search_bm25(query, top_k * 3)
        sem_results = self._search_semantic(query, top_k * 3)

        rrf_scores: dict[str, float] = {}
        result_map: dict[str, dict] = {}

        for rank, r in enumerate(bm25_results):
            key = r["file"]
            rrf_scores[key] = rrf_scores.get(key, 0.0) + 1.0 / (K + rank + 1)
            result_map[key] = r

        for rank, r in enumerate(sem_results):
            key = r["file"]
            rrf_scores[key] = rrf_scores.get(key, 0.0) + 1.0 / (K + rank + 1)
            if key not in result_map:
                result_map[key] = r

        ranked = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
        return [result_map[k] for k, _ in ranked[:top_k]]

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
                        snippet = content[max(0, idx - 100): idx + 300]
                        results.append(
                            {"file": rel, "section": "", "score": float(count), "snippet": snippet}
                        )
                except Exception:
                    pass
        results.sort(key=lambda r: r["score"], reverse=True)
        return results[:top_k]

    def _search_with_fallback(self, query: str, top_k: int = 10) -> list[dict]:
        if self._tier == SearchTier.HYBRID:
            try:
                return self._search_hybrid(query, top_k)
            except Exception as e:
                self._tier = SearchTier.BM25
                self._degradation_reason = f"Hybrid search failed: {e}"
        if self._tier == SearchTier.BM25:
            try:
                return self._search_bm25(query, top_k)
            except Exception as e:
                self._tier = SearchTier.RAWFS
                self._degradation_reason = f"BM25 search failed: {e}"
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
        self._model = None
        self._faiss_index = None
        # Remove stale state so index rebuilds from scratch
        state_file = self._INDEX_DIR / "index_state.json"
        if state_file.exists():
            state_file.unlink()
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


engine = SearchEngine(WORKSPACE_ROOT)


@mcp.tool()
def search_docs(query: str, top_k: int = 10) -> dict[str, Any]:
    """Hybrid semantic + BM25 keyword search across workspace markdown files with graceful
    fallback through HYBRID -> BM25 -> RAWFS tiers. Returns ranked results with file path,
    section heading, relevance score, and text snippet."""
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
    """Rebuild the search index from scratch, re-scanning all workspace markdown files.
    Clears FAISS state file to force a full re-encode on next startup."""
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


@mcp.tool()
def find_related_documents(seed_doc_path: str, top_k: int = 5) -> dict[str, Any]:
    """Find documents semantically similar to a given workspace document.
    Requires HYBRID tier; falls back to BM25 keyword search on the document's title."""
    target = WORKSPACE_ROOT / seed_doc_path
    if not target.exists():
        return {"error": f"File not found: {seed_doc_path}", "_meta": engine._meta_block()}
    try:
        content = target.read_text(encoding="utf-8", errors="ignore")
        # Use the first 512 words as the query
        query_text = " ".join(content.split()[:512])
        results = engine._search_with_fallback(query_text, top_k + 1)
        # Exclude the seed document itself
        results = [r for r in results if r["file"] != seed_doc_path][:top_k]
        return {"seed": seed_doc_path, "related": results, "_meta": engine._meta_block()}
    except Exception as exc:
        return {"error": str(exc), "_meta": engine._meta_block()}


@mcp.tool()
def list_research_by_topic(topic: str, format: str = "brief") -> dict[str, Any]:
    """List research archives in telescope/ by topic.
    format: 'brief' returns file list; 'full' returns snippets."""
    results = engine._search_with_fallback(topic, top_k=10)
    telescope_results = [r for r in results if r["file"].startswith("telescope/")]
    if format == "full":
        return {
            "topic": topic,
            "count": len(telescope_results),
            "results": telescope_results,
            "_meta": engine._meta_block(),
        }
    return {
        "topic": topic,
        "count": len(telescope_results),
        "files": [r["file"] for r in telescope_results],
        "_meta": engine._meta_block(),
    }


@mcp.tool()
def agent_knowledge_brief(agent_role: str, context_topics: list[str]) -> dict[str, Any]:
    """Generate a pre-digested knowledge brief for an agent role across multiple topics.
    Returns the top documents per topic, deduplicated, with relevant snippets."""
    seen: set[str] = set()
    brief_sections = []
    for topic in context_topics:
        results = engine._search_with_fallback(f"{agent_role} {topic}", top_k=3)
        section_docs = []
        for r in results:
            if r["file"] not in seen:
                seen.add(r["file"])
                section_docs.append(r)
        if section_docs:
            brief_sections.append({"topic": topic, "docs": section_docs})
    return {
        "agent_role": agent_role,
        "topics": context_topics,
        "sections": brief_sections,
        "total_docs": len(seen),
        "_meta": engine._meta_block(),
    }


if __name__ == "__main__":
    mcp.run()
