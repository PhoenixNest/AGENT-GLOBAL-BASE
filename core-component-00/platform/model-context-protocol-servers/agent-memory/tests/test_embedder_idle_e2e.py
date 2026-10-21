"""
Slow, real end-to-end idle-recovery check (see e2e_embedder_idle.py). Launches
a real embedder-service on a non-default port, so it is skipped unless
RUN_EMBEDDER_E2E=1 is set.
"""
import os
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.skipif(
    os.environ.get("RUN_EMBEDDER_E2E") != "1", reason="set RUN_EMBEDDER_E2E=1 to run the real idle-recovery e2e"
)


def test_service_relaunches_after_idle_shutdown():
    script = Path(__file__).resolve().parent / "e2e_embedder_idle.py"
    env = {k: v for k, v in os.environ.items() if k != "EMBEDDER_SERVICE_ENABLED"}
    proc = subprocess.run([sys.executable, str(script)], env=env, capture_output=True, text=True, timeout=600)
    assert proc.returncode == 0, proc.stdout + proc.stderr[-3000:]
    assert "PASS" in proc.stdout
