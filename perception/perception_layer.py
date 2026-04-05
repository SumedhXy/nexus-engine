"""
Perception Layer — Input ingestion and AI classification.
Uses Google Gemini API for primary classification, with a local heuristic fallback.
API key loaded from .env → GEMINI_API_KEY
"""
from __future__ import annotations
import os
import re
import json
import uuid
import concurrent.futures
from pathlib import Path
from dotenv import load_dotenv

# MISSION-CRITICAL: Pre-load the AI client library to prevent analytical stalls
try:
    from google import genai
    _GENAI_LOADED = True
except ImportError:
    _GENAI_LOADED = False
    print("[PerceptionLayer] ❌ Critical: google-genai library not found.")

from models.schemas import (
    RawInput, StructuredIncidentObject,
    IncidentType, SeverityLevel
)

# Load API key from .env
load_dotenv(Path(__file__).parent.parent / ".env")
_GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")

# ---------------------------------------------------------------------------
# Gemini client (Global Instance)
# ---------------------------------------------------------------------------
_gemini_client = None

def _get_model():
    global _gemini_client
    if _gemini_client is None and _GEMINI_KEY and _GENAI_LOADED:
        try:
            _gemini_client = genai.Client(api_key=_GEMINI_KEY)
            print("[PerceptionLayer] 🟢 Gemini AI link active.")
        except Exception as e:
            print(f"[PerceptionLayer] ⚠️ Gemini init failed: {e} — using local fallback.")
    return _gemini_client

_GEMINI_PROMPT = """You are the Perception Layer of the Nexus Crisis Engine.
Return a JSON object with EXACTLY these fields:
- detected_language: string
- translated_description: string
- incident_type: one of [fire, flood, earthquake, medical, chemical, structural, police, vehicle, unknown]
- severity: integer 1-5
- location: string
- semantic_tags: list
- confidence_score: float 0.0-1.0

Incident report: {content}
Respond with ONLY valid JSON."""

import time

# MISSION-CRITICAL: Quota Tracking Signal
_last_gemini_call = 0

def _classify_with_gemini(content: Optional[str], audio_b64: Optional[str] = None) -> dict | None:
    global _last_gemini_call
    client = _get_model()
    if not client:
        return None
        
    # TACTICAL QUOTA SHIELD: Ensure 4s gap (15 RPM Max)
    now = time.time()
    elapsed = now - _last_gemini_call
    if elapsed < 4.0:
        delay = 4.0 - elapsed
        print(f"[PerceptionLayer] ⏳ Quota Shield: Waiting {delay:.1f}s for high-fidelity Mission Link...")
        time.sleep(delay)

    try:
        _last_gemini_call = time.time()
        parts = [content or "Voice incident report."]
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=parts,
        )
        text = response.text.strip()
        text = re.sub(r"^```[a-z]*\n?", "", text); text = re.sub(r"\n?```$", "", text)
        return json.loads(text)
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
             print("[PerceptionLayer] ⚠️ Gemini Quota Exceeded — Switching to SENTRY Local Intelligence.")
        else:
             print(f"[PerceptionLayer] ⚠️ Gemini call failed: {error_msg}")
        return None

# ---------------------------------------------------------------------------
# Local heuristic fallback (keyword-based)
# ---------------------------------------------------------------------------

_TYPE_KEYWORDS: dict[str, list[str]] = {
    IncidentType.FIRE:        ["fire", "smoke", "flame", "burning", "ignition", "blaze"],
    IncidentType.FLOOD:       ["flood", "water", "submerged", "overflow", "inundation"],
    IncidentType.EARTHQUAKE:  ["earthquake", "tremor", "seismic", "shake", "quake"],
    IncidentType.MEDICAL:     ["medical", "injury", "injured", "unconscious", "cardiac", "sos", "help", "emergency"],
    IncidentType.CHEMICAL:    ["chemical", "toxic", "gas leak", "hazmat", "spill", "fumes"],
    IncidentType.STRUCTURAL:  ["collapse", "structural", "ceiling", "wall", "crack", "fallen"],
}

_SEVERITY_KEYWORDS: dict[int, list[str]] = {
    5: ["catastrophic", "mass casualty", "explosion"],
    4: ["critical", "severe", "major", "urgent"],
    3: ["high", "significant", "spreading"],
    2: ["moderate", "contained"],
    1: ["low", "suspected", "possible"],
}

def _classify_type_local(text: str) -> IncidentType:
    text_lower = text.lower()
    best_type, best_count = IncidentType.UNKNOWN, 0
    for itype, keywords in _TYPE_KEYWORDS.items():
        count = sum(1 for kw in keywords if kw in text_lower)
        if count > best_count:
            best_count, best_type = count, itype
    return best_type

def _score_severity_local(text: str) -> SeverityLevel:
    text_lower = text.lower()
    for level in sorted(_SEVERITY_KEYWORDS.keys(), reverse=True):
        if any(kw in text_lower for kw in _SEVERITY_KEYWORDS[level]):
            return SeverityLevel(level)
    return SeverityLevel.MODERATE

def _extract_location(text: str, metadata: dict) -> str:
    if "location" in metadata: return metadata["location"]
    match = re.search(r"\b(?:at|in|near)\s+([A-Za-z0-9 ,\-]+?)(?:\.|,|$)", text, re.IGNORECASE)
    return match.group(1).strip() if match else "Unknown Location"

class PerceptionLayer:
    def process(self, raw: RawInput) -> StructuredIncidentObject:
        text = raw.content or ""
        metadata = raw.metadata
        
        # Try Gemini with a strict 1.0s tactical timeout
        gemini_result = None
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(_classify_with_gemini, text, raw.audio_content)
            try:
                gemini_result = future.result(timeout=1.0) # AGGRESSIVE BYPASS: Prevent 30s library stals
            except Exception:
                print("[PerceptionLayer] ⚠️ AI Latency Detected — Seizing control with high-intensity heuristics.")

        if gemini_result:
            try:
                return StructuredIncidentObject(
                    incident_id=str(uuid.uuid4()),
                    user_id=raw.user_id,
                    incident_type=IncidentType(gemini_result.get("incident_type", "unknown")),
                    severity=SeverityLevel(int(gemini_result.get("severity", 2))),
                    location=gemini_result.get("location") or _extract_location(text, metadata),
                    reporter=metadata.get("reporter", raw.source),
                    description=gemini_result.get("translated_description", text),
                    confidence_score=float(gemini_result.get("confidence_score", 0.85)),
                    raw_input=raw,
                )
            except Exception: pass

        # Local fallback
        incident_type = _classify_type_local(text)
        severity = _score_severity_local(text)
        location = _extract_location(text, metadata)
        confidence = min(0.4 + (sum(1 for kws in _TYPE_KEYWORDS.values() for kw in kws if kw in text.lower()) * 0.1), 1.0)

        return StructuredIncidentObject(
            incident_id=str(uuid.uuid4()),
            user_id=raw.user_id,
            incident_type=incident_type,
            severity=severity,
            location=location,
            reporter=metadata.get("reporter", raw.source),
            description=text,
            confidence_score=round(confidence, 2),
            raw_input=raw,
        )
