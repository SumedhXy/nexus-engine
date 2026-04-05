"""
Synchronization Layer — Connectivity Monitor
Detects online/offline state and switches sync rail accordingly.
"""
from __future__ import annotations
import socket
from models.schemas import ConnectivityState


class ConnectivityMonitor:
    """
    Checks network connectivity by attempting a DNS lookup.
    In production, replace with a proper health-check ping.
    """

    _TEST_HOST = "8.8.8.8"
    _TEST_PORT = 53
    _TIMEOUT = 2

    def check(self) -> ConnectivityState:
        try:
            socket.setdefaulttimeout(self._TIMEOUT)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(
                (self._TEST_HOST, self._TEST_PORT)
            )
            return ConnectivityState.ONLINE
        except OSError:
            return ConnectivityState.OFFLINE

    def is_online(self) -> bool:
        return self.check() == ConnectivityState.ONLINE
