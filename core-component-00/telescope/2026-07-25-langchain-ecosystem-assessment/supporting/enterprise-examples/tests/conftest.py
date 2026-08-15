import sys
from pathlib import Path

# Make src/ importable without an editable install — mirrors how CC-00's own
# module test suites resolve their implementations/ package (core-component-00/CLAUDE.md
# § Import Path), applied to this project's own src layout.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import pytest  # noqa: E402


@pytest.fixture(autouse=True)
def _reset_telemetry():
    """Clear recorded spans between tests so span-count assertions don't leak."""
    from cc00_langchain.telemetry import reset_recorder

    reset_recorder()
    yield
    reset_recorder()
