import sys, json, pathlib

_SERVER_DIR = pathlib.Path(__file__).parent
sys.path.insert(0, str(_SERVER_DIR / ".venv" / "Lib" / "site-packages"))

import torch

embed_dir = _SERVER_DIR / "embedding"
faiss_path = embed_dir / "faiss.index"
state_path = embed_dir / "index_state.json"

files_count = len(json.loads(state_path.read_text())) if state_path.exists() else 0

try:
    import faiss as _faiss

    if faiss_path.exists():
        idx = _faiss.read_index(str(faiss_path))
        chunks_count = idx.ntotal
        tier = "hybrid"
    else:
        tier, chunks_count = "bm25", 0
except ImportError:
    tier, chunks_count = "bm25", 0

print(f"tier       : {tier}")
print(f"chunks     : {chunks_count}")
print(f"files      : {files_count}")
print(f"cuda_avail : {torch.cuda.is_available()}")
print(f"faiss.index: {'exists' if faiss_path.exists() else 'MISSING'}")
