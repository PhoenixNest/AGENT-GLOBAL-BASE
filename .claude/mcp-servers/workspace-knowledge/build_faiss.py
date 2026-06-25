import sys, time, os, json, pathlib, types

_SERVER_DIR = pathlib.Path(__file__).parent
sys.path.insert(0, str(_SERVER_DIR / ".venv" / "Lib" / "site-packages"))
sys.path.insert(0, str(_SERVER_DIR))

fm = types.ModuleType("fastmcp")


class _M:
    def tool(self):
        def d(f):
            return f

        return d

    def run(self):
        pass


fm.FastMCP = lambda *a, **k: _M()
sys.modules["fastmcp"] = fm

os.environ.setdefault("WORKSPACE_ROOT", str(_SERVER_DIR.parent.parent.parent))
import server as srv

time.sleep(3)
e = srv.engine
print(f"BM25 chunks: {len(e._chunks)}")

import torch, numpy as np, faiss
from sentence_transformers import SentenceTransformer

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"device: {device}")
print("Loading model from local path...")
t0 = time.time()
model = SentenceTransformer(str(srv.SearchEngine._MODEL_DIR), device=device)
print(f"Model loaded: {time.time()-t0:.1f}s on {model.device}")

texts = [c["text"][:512] for c in e._chunks]
print(f"Encoding {len(texts)} chunks (batch_size=64)...")
t1 = time.time()
embs = model.encode(texts, show_progress_bar=True, batch_size=64)
print(f"Encoded in {time.time()-t1:.1f}s")

embs = embs / np.linalg.norm(embs, axis=1, keepdims=True)
index = faiss.IndexFlatIP(embs.shape[1])
index.add(embs.astype("float32"))

out_dir = srv.SearchEngine._EMBED_DIR
faiss.write_index(index, str(out_dir / "faiss.index"))

root = pathlib.Path(os.environ["WORKSPACE_ROOT"])
mtimes = {}
for d in srv.SearchEngine.KEY_DIRS:
    dp = root / d
    if dp.exists():
        for f in dp.rglob("*.md"):
            rel = str(f.relative_to(root)).replace("\\", "/")
            mtimes[rel] = f.stat().st_mtime
(out_dir / "index_state.json").write_text(json.dumps(mtimes))

size_mb = round((out_dir / "faiss.index").stat().st_size / 1024 / 1024, 1)
print(f"Total: {time.time()-t0:.1f}s — faiss.index written ({size_mb} MB)")
