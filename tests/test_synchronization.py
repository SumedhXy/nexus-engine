"""Tests for the Synchronization Layer."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import time
import pytest
from synchronization.crdt_state import CRDTState
from synchronization.connectivity_monitor import ConnectivityMonitor
from models.schemas import DistributedMissionState, MissionStateEntry


@pytest.fixture
def local_state():
    return CRDTState(node_id="node-A")

@pytest.fixture
def remote_state():
    return CRDTState(node_id="node-B")


def test_crdt_set_and_get(local_state):
    local_state.set("incident:1", "fire")
    assert local_state.get("incident:1") == "fire"

def test_crdt_lww_remote_wins(local_state, remote_state):
    """Remote node sets a key AFTER local — remote should win on merge."""
    local_state.set("key", "local-value")
    time.sleep(0.01)
    remote_state.set("key", "remote-value")

    updated = local_state.merge(remote_state.snapshot())
    assert "key" in updated
    assert local_state.get("key") == "remote-value"

def test_crdt_lww_local_wins(local_state, remote_state):
    """Local node sets a key AFTER remote — local should win."""
    remote_state.set("key", "remote-value")
    time.sleep(0.01)
    local_state.set("key", "local-value")

    updated = local_state.merge(remote_state.snapshot())
    assert "key" not in updated   # Remote entry was older, local wins
    assert local_state.get("key") == "local-value"

def test_crdt_merge_adds_new_keys(local_state, remote_state):
    """New keys from remote should be added to local."""
    remote_state.set("new-key", "from-remote")
    updated = local_state.merge(remote_state.snapshot())
    assert "new-key" in updated
    assert local_state.get("new-key") == "from-remote"

def test_connectivity_monitor_returns_state():
    monitor = ConnectivityMonitor()
    state = monitor.check()
    assert state in ("online", "offline")
