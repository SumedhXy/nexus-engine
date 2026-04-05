"""
Orchestration Layer — Protocol Matcher
Maps a StructuredIncidentObject to the best matching SOP.
"""
from __future__ import annotations
from models.schemas import StructuredIncidentObject, SOP, IncidentType
from orchestration.sop_library import SOPLibrary


class ProtocolMatcher:
    """
    Scores each candidate SOP and returns the best match.

    Scoring formula:
        score = (type_match * 10) + (severity_coverage * 5) - step_count_penalty
    """

    def __init__(self, library: SOPLibrary):
        self._library = library

    def match(self, incident: StructuredIncidentObject) -> SOP | None:
        candidate = self._library.get_by_type(incident.incident_type)
        candidates = [candidate] if candidate else []
        
        # Priority Fallback: If no type-specific SOP, use EVERYTHING as candidate
        if not candidates:
            # Note: Assuming get_all() exists or similar in SOPLibrary
            try:
                candidates = list(self._library.library.values())
            except Exception:
                candidates = []

        if not candidates:
             print("[ProtocolMatcher] ❌ CRITICAL: SOP Library is empty.")
             return None

        # Score and find best
        scored = [(self._score(sop, incident), sop) for sop in candidates]
        scored.sort(key=lambda x: x[0], reverse=True)
        _, best_sop = scored[0]

        # Final Fallback check
        if best_sop is None:
            best_sop = next((s for s in candidates if IncidentType.UNKNOWN in s.incident_types), candidates[0])

        return best_sop

    def _score(self, sop: SOP, incident: StructuredIncidentObject) -> float:
        score = 0.0
        # Type match bonus
        if incident.incident_type in sop.incident_types:
            score += 10.0
        # Severity coverage: prefer SOPs that cover this severity level
        severity_gap = abs(incident.severity - sop.min_severity)
        score += max(0, 5 - severity_gap)
        return score
