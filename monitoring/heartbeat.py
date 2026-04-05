"""
Monitoring Layer — Heartbeat Monitor & Dead Man's Switch
Tracks responder heartbeats; triggers escalation on missed beats.
"""
from __future__ import annotations
import threading
import time
from datetime import datetime, timedelta
from models.schemas import Responder, HeartbeatStatus


_BEAT_INTERVAL_SECS = 30      # Expected heartbeat interval
_MAX_MISSED_BEATS = 3         # Trigger Dead Man's Switch after N missed beats


class HeartbeatMonitor:
    """
    Tracks per-responder heartbeats.
    Dead Man's Switch fires when a responder misses MAX_MISSED_BEATS consecutive beats.
    """

    def __init__(self, on_dead_mans_switch: callable | None = None):
        self._statuses: dict[str, HeartbeatStatus] = {}
        self._on_dms = on_dead_mans_switch or (lambda rid: print(
            f"[HeartbeatMonitor] ⚠️ Dead Man's Switch triggered for {rid}"
        ))
        self._lock = threading.Lock()
        self._running = False

    def register(self, responder: Responder) -> None:
        with self._lock:
            self._statuses[responder.responder_id] = HeartbeatStatus(
                responder_id=responder.responder_id,
                last_seen=datetime.utcnow(),
                is_alive=True,
                missed_beats=0,
            )

    def record_beat(self, responder_id: str) -> None:
        with self._lock:
            if responder_id in self._statuses:
                status = self._statuses[responder_id]
                status.last_seen = datetime.utcnow()
                status.is_alive = True
                status.missed_beats = 0

    def get_status(self, responder_id: str) -> HeartbeatStatus | None:
        return self._statuses.get(responder_id)

    def all_statuses(self) -> list[HeartbeatStatus]:
        return list(self._statuses.values())

    def start_monitor(self) -> None:
        """Start background thread that checks for missed beats every interval."""
        self._running = True
        t = threading.Thread(target=self._check_loop, daemon=True)
        t.start()

    def stop(self) -> None:
        self._running = False

    def _check_loop(self) -> None:
        while self._running:
            time.sleep(_BEAT_INTERVAL_SECS)
            self._check_all()

    def _check_all(self) -> None:
        now = datetime.utcnow()
        deadline = now - timedelta(seconds=_BEAT_INTERVAL_SECS)
        with self._lock:
            for rid, status in self._statuses.items():
                if status.last_seen < deadline:
                    status.missed_beats += 1
                    if status.missed_beats >= _MAX_MISSED_BEATS:
                        status.is_alive = False
                        self._on_dms(rid)
