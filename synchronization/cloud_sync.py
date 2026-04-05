from __future__ import annotations
import os
from datetime import datetime
from typing import Any, List, Optional
from pathlib import Path
from dotenv import load_dotenv
import httpx

load_dotenv(Path(__file__).parent.parent / ".env")
_FIREBASE_URL = os.getenv("FIREBASE_DATABASE_URL", "").rstrip("/")
_TIMEOUT = 5.0

class CloudSync:
    def __init__(self, firebase_url: str = _FIREBASE_URL):
        self._url = firebase_url.rstrip("/")

    def _get_auth_url(self, path: str, token: str | None = None) -> str:
        url = f"{self._url}{path}"
        if token:
            prefix = "&" if "?" in url else "?"
            url = f"{url}{prefix}auth={token}"
        return url

    def _json_serialize(self, obj: Any) -> Any:
        if isinstance(obj, datetime): return obj.isoformat()
        if isinstance(obj, dict): return {k: self._json_serialize(v) for k, v in obj.items()}
        if isinstance(obj, list): return [self._json_serialize(i) for i in obj]
        return obj

    def write_user_profile(self, user_id: str, profile_data: dict, auth_token: str | None = None) -> bool:
        payload = self._json_serialize(profile_data)
        try:
            resp = httpx.put(self._get_auth_url(f"/users/{user_id}/profile.json", auth_token), json=payload, timeout=_TIMEOUT)
            resp.raise_for_status()
            return True
        except Exception as e:
            print(f"[CloudSync] ❌ User profile write failed: {e}")
            return False

    def get_user_profile(self, user_id: str, auth_token: str | None = None) -> dict | None:
        try:
            resp = httpx.get(self._get_auth_url(f"/users/{user_id}/profile.json", auth_token), timeout=_TIMEOUT)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"[CloudSync] ❌ User profile fetch failed: {e}")
            return None

    def write_user_incident(self, user_id: str, incident_id: str, data: dict, auth_token: str | None = None) -> bool:
        payload = self._json_serialize(data)
        try:
            resp = httpx.put(self._get_auth_url(f"/users/{user_id}/incidents/{incident_id}.json", auth_token), json=payload, timeout=_TIMEOUT)
            resp.raise_for_status()
            return True
        except Exception as e:
            print(f"[CloudSync] ❌ History write failed: {e}")
            return False

    def get_user_incidents(self, user_id: str, auth_token: str | None = None) -> List[dict]:
        try:
            resp = httpx.get(self._get_auth_url(f"/users/{user_id}/incidents.json", auth_token), timeout=_TIMEOUT)
            resp.raise_for_status()
            data = resp.json() or {}
            return list(data.values())
        except Exception as e:
            print(f"[CloudSync] ❌ History fetch failed: {e}")
            return []
