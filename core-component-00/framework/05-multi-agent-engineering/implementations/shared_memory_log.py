"""
Shared Memory Log — Event-Sourced Agent Coordination Memory

Implements the Governed Shared Memory (GSM) pattern: F = (A, M, G, P, T)
  A = agent registry, M = memory entries, G = governance rules,
  P = scope predicates, T = timestamps

Scope enforcement prevents cross-fleet leakage via predicate evaluation.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class MemoryScope(Enum):
    FLEET = "fleet"
    GLOBAL = "global"


@dataclass
class MemoryEntry:
    entry_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    agent_id: str = ""
    fleet_id: str = ""
    scope: MemoryScope = MemoryScope.FLEET
    key: str = ""
    value: object = None
    timestamp: float = field(default_factory=time.monotonic)
    ttl_seconds: Optional[float] = None

    @property
    def is_expired(self) -> bool:
        if self.ttl_seconds is None:
            return False
        return (time.monotonic() - self.timestamp) > self.ttl_seconds


class SharedMemoryLog:
    """
    Append-only shared memory log with GSM scope enforcement.
    All writes are appended; reads are filtered by scope predicate.
    """

    def __init__(self):
        self._entries: list[MemoryEntry] = []
        self.audit_log: list[dict] = []

    def write(
        self,
        agent_id: str,
        fleet_id: str,
        scope: MemoryScope,
        key: str,
        value: object,
        ttl: Optional[float] = None,
    ) -> MemoryEntry:
        entry = MemoryEntry(
            agent_id=agent_id,
            fleet_id=fleet_id,
            scope=scope,
            key=key,
            value=value,
            ttl_seconds=ttl,
        )
        self._entries.append(entry)
        self.audit_log.append(
            {
                "op": "write",
                "agent": agent_id,
                "fleet": fleet_id,
                "scope": scope.value,
                "key": key,
                "entry_id": entry.entry_id,
            }
        )
        return entry

    def read(
        self,
        requesting_agent_id: str,
        requesting_fleet_id: str,
        key: str,
    ) -> Optional[MemoryEntry]:
        result = None
        for entry in reversed(self._entries):
            if entry.key != key or entry.is_expired:
                continue
            if self._scope_predicate(entry, requesting_fleet_id):
                result = entry
                break
        self.audit_log.append(
            {
                "op": "read",
                "agent": requesting_agent_id,
                "fleet": requesting_fleet_id,
                "key": key,
                "found": result is not None,
            }
        )
        return result

    def read_all(
        self,
        requesting_agent_id: str,
        requesting_fleet_id: str,
    ) -> list[MemoryEntry]:
        visible = [
            e
            for e in self._entries
            if not e.is_expired and self._scope_predicate(e, requesting_fleet_id)
        ]
        self.audit_log.append(
            {
                "op": "read_all",
                "agent": requesting_agent_id,
                "fleet": requesting_fleet_id,
                "count": len(visible),
            }
        )
        return visible

    def expire_stale(self) -> int:
        before = len(self._entries)
        self._entries = [e for e in self._entries if not e.is_expired]
        return before - len(self._entries)

    @staticmethod
    def _scope_predicate(entry: MemoryEntry, requesting_fleet_id: str) -> bool:
        if entry.scope == MemoryScope.GLOBAL:
            return True
        return entry.fleet_id == requesting_fleet_id
