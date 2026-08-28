"""Compatibility shim for jsonref's stale `proxytypes` import.

jsonref 1.1.0's published PyPI wheel contains `from proxytypes import LazyProxy` (a plain,
top-level absolute import). The only PyPI distribution that actually provides `LazyProxy`
is `ProxyTypes` (PyPI-normalized to the same name as the long-abandoned `proxytypes`
distribution jsonref's wheel was originally built against), but `ProxyTypes` installs its
code under the `peak.util.proxies` namespace, not a top-level `proxytypes` module — so
`uv add proxytypes` resolves and installs correctly, yet jsonref's import still fails with
`ModuleNotFoundError: No module named 'proxytypes'`.

This file re-exports the real implementation under the top-level name jsonref's wheel
expects. `_vendor/` is added to `sys.path` in `server.py`, ahead of the `fastmcp` import
that transitively pulls in `jsonref`.
"""

from peak.util.proxies import *  # noqa: F401,F403
from peak.util.proxies import LazyProxy  # noqa: F401
