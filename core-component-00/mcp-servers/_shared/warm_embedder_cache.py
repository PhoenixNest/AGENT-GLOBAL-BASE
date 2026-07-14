"""One-time warm-up for embedding-model imports and their compiled dependencies
(sentence_transformers -> sklearn -> scipy's compiled extension files), run
during provisioning rather than reactively on a live server's first request.

Usage:
    python _shared/warm_embedder_cache.py [hf-model-id ...]

With no arguments, warms every model already provisioned in the shared cache
(_shared/models/). Pass one or more model ids to warm only those:

    python _shared/warm_embedder_cache.py sentence-transformers/all-MiniLM-L6-v2

Run this once per machine after provision_model.py, before starting any
CC-00 MCP server for real. Idempotent — safe to re-run.
"""
import sys
import argparse
import pathlib
import time

_SHARED_DIR = pathlib.Path(__file__).parent
MODELS_CACHE_DIR = _SHARED_DIR / "models"


def _provisioned_slugs() -> list[str]:
    if not MODELS_CACHE_DIR.exists():
        return []
    return sorted(p.name for p in MODELS_CACHE_DIR.iterdir() if p.is_dir() and any(p.iterdir()))


def _slugify(model_id: str) -> str:
    return model_id.replace("/", "--")


def warm(slug: str) -> None:
    cache_dir = MODELS_CACHE_DIR / slug
    if not cache_dir.exists() or not any(cache_dir.iterdir()):
        print(f"SKIP {slug}: not provisioned — run provision_model.py first")
        return

    t0 = time.time()
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(str(cache_dir))
    model.encode(["warm-up"])  # exercises the actual encode path, not just construction
    print(f"OK {slug} warmed in {time.time() - t0:.2f}s")


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "model_ids",
        nargs="*",
        help="Hugging Face model id(s) to warm. Omit to warm every provisioned model.",
    )
    args = parser.parse_args()

    slugs = [_slugify(m) for m in args.model_ids] if args.model_ids else _provisioned_slugs()
    if not slugs:
        print("Nothing to warm — no models provisioned in _shared/models/")
        return

    for slug in slugs:
        warm(slug)


if __name__ == "__main__":
    main()
