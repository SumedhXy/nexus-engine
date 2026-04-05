"""
Synchronization Layer — CRDT / LWW Distributed Mission State
Implements Last-Write-Wins (LWW) merge for distributed state across nodes.
"""
from __future__ import annotations
import time
from models.schemas import DistributedMissionState, MissionStateEntry, ConnectivityState


_LOCAL_NODE_ID = "nexus-primary"


class CRDTState:
    """
    Last-Write-Wins Element Register (LWW-Register) for mission state.
    Each key stores the value with the highest timestamp.
    Two replicas can be merged by taking the max-timestamp entry per key.
    """

    def __init__(self, node_id: str = _LOCAL_NODE_ID):
        self._node_id = node_id
        self._state: DistributedMissionState = DistributedMissionState()

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------
    def set(self, key: str, value) -> MissionStateEntry:
        entry = MissionStateEntry(
            key=key,
            value=value,
            timestamp=time.time(),
            node_id=self._node_id,
        )
        self._state.entries[key] = entry
        return entry

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------
    def get(self, key: str):
        entry = self._state.entries.get(key)
        return entry.value if entry else None

    def get_entry(self, key: str) -> MissionStateEntry | None:
        return self._state.entries.get(key)

    def snapshot(self) -> DistributedMissionState:
        return self._state.model_copy(deep=True)

    # ------------------------------------------------------------------
    # Merge (LWW — higher timestamp wins per key)
    # ------------------------------------------------------------------
    def merge(self, remote: DistributedMissionState) -> list[str]:
        """
        Merge remote state into local state.
        Returns list of keys where remote won (i.e., newer data pulled in).
        """
        updated_keys: list[str] = []
        for key, remote_entry in remote.entries.items():
            local_entry = self._state.entries.get(key)
            if local_entry is None or remote_entry.timestamp > local_entry.timestamp:
                self._state.entries[key] = remote_entry
                updated_keys.append(key)
        return updated_keys

    def set_connectivity(self, state: ConnectivityState) -> None:
        self._state.connectivity = state
