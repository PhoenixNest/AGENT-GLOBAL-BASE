"""Download and locally cache a sentence-transformers embedding model.

Usage:
    python rag-system/download_model.py <hf-model-id> [--activate]

Examples:
    python rag-system/download_model.py sentence-transformers/all-mpnet-base-v2 --activate
    python rag-system/download_model.py sentence-transformers/all-MiniLM-L6-v2

Naming convention:
    embedding/model/          ACTIVE model — the exact path server.py's
                               SearchEngine._MODEL_DIR loads. Exactly one
                               model lives here at a time.
    embedding/models/<slug>/  Cache of every model ever downloaded, keyed by
                               slug = <hf-model-id> with "/" -> "--"
                               (e.g. sentence-transformers/all-mpnet-base-v2
                               -> sentence-transformers--all-mpnet-base-v2).
                               server.py never reads from here directly.

--activate copies a cached model from embedding/models/<slug>/ into the
active embedding/model/ slot (overwriting whatever was there). Without
--activate, the model is only added to the cache for later use.

Note: Qdrant's `workspace_knowledge` collection is created with a fixed
vector size (768, matching all-mpnet-base-v2). Activating a model with a
different embedding dimension requires rebuild_index (which drops and
re-creates the collection) — this script warns but does not do that for you.
"""
import sys
import argparse
import shutil
import pathlib

_SERVER_DIR = pathlib.Path(__file__).parent.parent
_VENV_SP = _SERVER_DIR / ".venv" / "Lib" / "site-packages"
if _VENV_SP.exists():
    sys.path.insert(0, str(_VENV_SP))

EMBED_DIR = _SERVER_DIR / "embedding"
MODELS_CACHE_DIR = EMBED_DIR / "models"
ACTIVE_MODEL_DIR = EMBED_DIR / "model"
QDRANT_COLLECTION_DIM = 768  # must match _ensure_collection's VectorParams(size=...) in server.py


def slugify(model_id: str) -> str:
    return model_id.replace("/", "--")


def dir_size_mb(path: pathlib.Path) -> float:
    return sum(f.stat().st_size for f in path.rglob("*") if f.is_file()) / 1024 / 1024


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "model_id", help="Hugging Face model id, e.g. sentence-transformers/all-mpnet-base-v2"
    )
    parser.add_argument(
        "--activate",
        action="store_true",
        help="Also promote this model into embedding/model/, the slot server.py loads",
    )
    args = parser.parse_args()

    slug = slugify(args.model_id)
    dest = MODELS_CACHE_DIR / slug

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

    if dim != QDRANT_COLLECTION_DIM:
        print(
            f"WARNING: dim {dim} != existing Qdrant collection dim {QDRANT_COLLECTION_DIM}. "
            "Activating this model will break Qdrant search until rebuild_index is called "
            "(it drops and re-creates the collection with the active model's dimension)."
        )

    if args.activate:
        if ACTIVE_MODEL_DIR.exists():
            shutil.rmtree(ACTIVE_MODEL_DIR)
        shutil.copytree(dest, ACTIVE_MODEL_DIR)
        print(f"Activated: {ACTIVE_MODEL_DIR} now serves '{args.model_id}'")
        print("Reconnect the workspace-knowledge MCP server (or call rebuild_index) to pick it up.")
    else:
        print(f"Cached only. Re-run with --activate to promote it into {ACTIVE_MODEL_DIR}")


if __name__ == "__main__":
    main()
