"""
Tests for SharedMemoryLog TTL / expiry behavior.

Covers MemoryEntry.is_expired, SharedMemoryLog.expire_stale(), and TTL interaction
with write()/read()/read_all(). This path previously had zero direct test coverage
(test_gsm_scope_enforcement.py only exercises SharedMemoryLog indirectly through
SwarmOrchestrator and never sets a ttl).

Time-control note (found while writing these tests): MemoryEntry.timestamp uses
`field(default_factory=time.monotonic)`, which is evaluated ONCE at class-definition
time (module import) -- default_factory holds a direct reference to the original
`time.monotonic` function object, not a name that gets re-resolved on every call.
Monkeypatching `shared_memory_log.time.monotonic` after import therefore has NO
effect on timestamps assigned via that default_factory. It DOES affect
`is_expired`'s own `time.monotonic()` call, since that is a fresh attribute lookup
performed at call time. Tests below that exercise SharedMemoryLog.write() rely on
this: they let write() stamp entries with the real clock, capture that real
timestamp, then monkeypatch time.monotonic() to return `real_timestamp + offset`
for the "now" the expiry check sees -- deterministic, no real sleeping required.
The boundary test constructs MemoryEntry directly with an explicit `timestamp=`
kwarg, which bypasses default_factory entirely for full control.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from implementations import shared_memory_log
from implementations.shared_memory_log import MemoryEntry, MemoryScope, SharedMemoryLog


def _patch_now(monkeypatch, value: float) -> None:
    """Patch shared_memory_log's time.monotonic() to return a fixed value."""
    monkeypatch.setattr(shared_memory_log.time, "monotonic", lambda: value)


def test_entry_with_no_ttl_never_expires(monkeypatch):
    """An entry written with no ttl (default None) is never expired, no matter how
    much simulated time passes."""
    log = SharedMemoryLog()
    entry = log.write("agent-1", "fleet-1", MemoryScope.FLEET, "key", "value")

    assert entry.ttl_seconds is None
    assert entry.is_expired is False

    _patch_now(monkeypatch, entry.timestamp + 1_000_000.0)
    assert entry.is_expired is False


def test_entry_with_unelapsed_ttl_is_not_expired(monkeypatch):
    """An entry whose ttl has not yet elapsed reports is_expired as False."""
    log = SharedMemoryLog()
    entry = log.write(
        "agent-1", "fleet-1", MemoryScope.FLEET, "key", "value", ttl=10.0
    )

    _patch_now(monkeypatch, entry.timestamp + 5.0)
    assert entry.is_expired is False


def test_entry_with_elapsed_ttl_is_expired(monkeypatch):
    """An entry whose ttl has elapsed reports is_expired as True."""
    log = SharedMemoryLog()
    entry = log.write(
        "agent-1", "fleet-1", MemoryScope.FLEET, "key", "value", ttl=1.0
    )

    _patch_now(monkeypatch, entry.timestamp + 5.0)
    assert entry.is_expired is True


def test_expire_stale_purges_only_expired_entries(monkeypatch):
    """expire_stale() removes expired entries from _entries, returns the correct
    purge count, and leaves non-expired entries untouched."""
    log = SharedMemoryLog()
    stale = log.write(
        "agent-1", "fleet-1", MemoryScope.FLEET, "stale-key", "v1", ttl=1.0
    )
    fresh = log.write(
        "agent-1", "fleet-1", MemoryScope.FLEET, "fresh-key", "v2", ttl=100.0
    )
    permanent = log.write(
        "agent-1", "fleet-1", MemoryScope.FLEET, "permanent-key", "v3"
    )

    # Advance simulated "now" relative to `stale`'s own creation time so it crosses
    # its ttl, while `fresh` (much longer ttl, created moments later) does not.
    _patch_now(monkeypatch, stale.timestamp + 5.0)

    purged_count = log.expire_stale()

    assert purged_count == 1
    remaining_ids = {e.entry_id for e in log._entries}
    assert stale.entry_id not in remaining_ids
    assert fresh.entry_id in remaining_ids
    assert permanent.entry_id in remaining_ids
    assert len(log._entries) == 2


def test_read_skips_expired_entry_by_key(monkeypatch):
    """read() treats an expired entry as not found, even though a matching key
    exists in the log -- current actual behavior of the `entry.is_expired` skip in
    the read() scan loop."""
    log = SharedMemoryLog()
    entry = log.write(
        "agent-1", "fleet-1", MemoryScope.FLEET, "shared-key", "value", ttl=1.0
    )

    _patch_now(monkeypatch, entry.timestamp + 5.0)

    result = log.read(
        requesting_agent_id="agent-1",
        requesting_fleet_id="fleet-1",
        key="shared-key",
    )
    assert result is None


def test_read_all_filters_out_expired_entries(monkeypatch):
    """read_all() excludes expired entries from its returned list while keeping
    non-expired ones."""
    log = SharedMemoryLog()
    expiring = log.write(
        "agent-1", "fleet-1", MemoryScope.FLEET, "expiring-key", "v1", ttl=1.0
    )
    surviving = log.write(
        "agent-1", "fleet-1", MemoryScope.FLEET, "surviving-key", "v2", ttl=100.0
    )

    _patch_now(monkeypatch, expiring.timestamp + 5.0)

    visible = log.read_all(requesting_agent_id="agent-1", requesting_fleet_id="fleet-1")
    visible_ids = {e.entry_id for e in visible}

    assert expiring.entry_id not in visible_ids
    assert surviving.entry_id in visible_ids
    assert len(visible) == 1


def test_is_expired_boundary_behavior(monkeypatch):
    """Document the actual boundary behavior: is_expired compares elapsed time to
    ttl_seconds with a strict `>`, so an entry exactly at its ttl boundary
    (elapsed == ttl_seconds) is NOT yet expired; one tick past the boundary, it
    is. This is current, observed behavior -- not assumed."""
    entry = MemoryEntry(
        agent_id="agent-1",
        fleet_id="fleet-1",
        scope=MemoryScope.FLEET,
        key="boundary-key",
        value="value",
        timestamp=100.0,
        ttl_seconds=5.0,
    )

    # Exactly at the boundary: elapsed (5.0) == ttl_seconds (5.0) -> not expired.
    _patch_now(monkeypatch, 105.0)
    assert entry.is_expired is False

    # One tick past the boundary -> expired.
    _patch_now(monkeypatch, 105.0000001)
    assert entry.is_expired is True
