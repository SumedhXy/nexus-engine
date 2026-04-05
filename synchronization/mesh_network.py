"""
Synchronization Layer — P2P Mesh Network (Google Nearby Connections stub)
Simulates offline peer-to-peer state sharing via UDP multicast.
"""
from __future__ import annotations
import json
import socket
import threading
from models.schemas import DistributedMissionState, MissionStateEntry

_MULTICAST_GROUP = "224.0.0.251"
_PORT = 5353
_BUFFER = 4096


class MeshNetwork:
    """
    Offline P2P mesh using UDP multicast to simulate Google Nearby Connections.
    Nodes broadcast their CRDT state; listeners merge incoming data.
    """

    def __init__(self, node_id: str = "nexus-primary"):
        self._node_id = node_id
        self._sock: socket.socket | None = None
        self._running = False
        self._received_states: list[DistributedMissionState] = []

    def start_listener(self) -> None:
        """Start listening for mesh broadcasts in a background thread."""
        self._running = True
        t = threading.Thread(target=self._listen, daemon=True)
        t.start()
        print(f"[MeshNetwork] Listener started on {_MULTICAST_GROUP}:{_PORT}")

    def stop(self) -> None:
        self._running = False
        if self._sock:
            self._sock.close()

    def broadcast(self, state: DistributedMissionState) -> None:
        """Broadcast local CRDT state snapshot to mesh peers."""
        try:
            payload = json.dumps({
                "node_id": self._node_id,
                "entries": {
                    k: {"value": str(v.value), "timestamp": v.timestamp, "node_id": v.node_id}
                    for k, v in state.entries.items()
                }
            }).encode()
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
            sock.sendto(payload, (_MULTICAST_GROUP, _PORT))
            sock.close()
            print(f"[MeshNetwork] Broadcast {len(state.entries)} keys to mesh.")
        except Exception as e:
            print(f"[MeshNetwork] Broadcast failed: {e}")

    def pop_received(self) -> list[DistributedMissionState]:
        """Return and clear received remote states."""
        states = list(self._received_states)
        self._received_states.clear()
        return states

    def _listen(self) -> None:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(("", _PORT))
            mreq = socket.inet_aton(_MULTICAST_GROUP) + socket.inet_aton("0.0.0.0")
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            sock.settimeout(1.0)
            self._sock = sock
            while self._running:
                try:
                    data, _ = sock.recvfrom(_BUFFER)
                    self._parse(data)
                except socket.timeout:
                    continue
        except Exception as e:
            print(f"[MeshNetwork] Listener error: {e}")

    def _parse(self, data: bytes) -> None:
        if not data or not data.strip():
            return
        try:
            obj = json.loads(data.decode())
            entries = {}
            for k, v in obj.get("entries", {}).items():
                entries[k] = MissionStateEntry(
                    key=k,
                    value=v["value"],
                    timestamp=float(v["timestamp"]),
                    node_id=v["node_id"],
                )
            self._received_states.append(DistributedMissionState(entries=entries))
        except Exception:
            # Silently ignore malformed packets from other network services
            pass
