"""
Sets EMBEDDER_SERVICE_ENABLED=false before workspace-knowledge/server.py is
first imported, so importing it during a unit-test run never probes for or
launches the shared embedder-service subprocess. This only changes what
happens at import time; tests that exercise the service path set
`server.EMBEDDER_SERVICE_ENABLED` and the state globals explicitly, with a
fake `embedder_client`.
"""
import os

os.environ.setdefault("EMBEDDER_SERVICE_ENABLED", "false")
