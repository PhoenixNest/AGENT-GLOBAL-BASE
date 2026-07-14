"""Download and locally cache a sentence-transformers embedding model into the
shared cache used by every CC-00 MCP server that needs one.

Usage:
    python _shared/provision_model.py <hf-model-id>

Examples:
    python _shared/provision_model.py sentence-transformers/all-MiniLM-L6-v2
    python _shared/provision_model.py sentence-transformers/all-mpnet-base-v2

Naming convention (same slug scheme as
workspace-knowledge/rag-system/download_model.py's own cache):
    _shared/models/<slug>/   Cache of every model provisioned for use by any
                              CC-00 MCP server, keyed by
                              slug = <hf-model-id> with "/" -> "--"
                              (e.g. sentence-transformers/all-MiniLM-L6-v2 ->
                              sentence-transformers--all-MiniLM-L6-v2).

Unlike download_model.py, this cache has no single "active" slot and no
--activate step. workspace-knowledge's cache backs exactly one FAISS/Qdrant
collection at a time, so promoting a model into an active slot is meaningful
there. This shared cache instead backs multiple MCP servers concurrently that
need different, incompatible-dimension models at once (workspace-knowledge:
all-mpnet-base-v2, 768-dim; agent-memory: all-MiniLM-L6-v2, 384-dim) — each
server reads its own model directly out of _shared/models/<slug>/, so there is
no single model to "activate".

Idempotent: re-running for an already-cached model is a no-op, not a
re-download.
"""
import sys
import argparse
import pathlib

_SHARED_DIR = pathlib.Path(__file__).parent
MODELS_CACHE_DIR = _SHARED_DIR / "models"


def slugify(model_id: str) -> str:
    return model_id.replace("/", "--")


def dir_size_mb(path: pathlib.Path) -> float:
    return sum(f.stat().st_size for f in path.rglob("*") if f.is_file()) / 1024 / 1024


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "model_id", help="Hugging Face model id, e.g. sentence-transformers/all-MiniLM-L6-v2"
    )
    args = parser.parse_args()

    slug = slugify(args.model_id)
    dest = MODELS_CACHE_DIR / slug

    if dest.exists() and any(dest.iterdir()):
        print(f"Already cached: {dest} ({dir_size_mb(dest):.1f} MB) — no-op")
        return

    print(f"Downloading '{args.model_id}' -> {dest}")
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(args.model_id)
    dest.mkdir(parents=True, exist_ok=True)
    model.save(str(dest))
    dim = (
        model.get_embedding_dimension()
        if hasattr(model, "get_embedding_dimension")
        else model.get_sentence_embedding_dimension()
    )
    print(f"Saved {dir_size_mb(dest):.1f} MB to {dest} (embedding dim: {dim})")


if __name__ == "__main__":
    main()
