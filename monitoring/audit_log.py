"""
Monitoring Layer — Immutable Black Box Audit Log & Post-Incident Report
Append-only JSON log; no modifications or deletions allowed.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
from datetime import datetime
from models.schemas import AuditEvent, PostIncidentReport

_LOG_DIR = Path(__file__).parent.parent / "data" / "audit_logs"
_LOG_DIR.mkdir(parents=True, exist_ok=True)


class AuditLog:
    """
    Immutable append-only Black Box.
    Each event is written as a JSON line to a date-stamped log file.
    No event can be modified or removed after writing.
    """

    def __init__(self, log_dir: Path = _LOG_DIR):
        self._log_dir = log_dir
        self._log_dir.mkdir(parents=True, exist_ok=True)

    def _log_file(self) -> Path:
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
        return self._log_dir / f"audit_{date_str}.jsonl"

    def log(self, event: AuditEvent) -> None:
        """Append an audit event. Files are opened in append mode only."""
        with open(self._log_file(), "a", encoding="utf-8") as f:
            f.write(event.model_dump_json() + "\n")

    def get_all(self, incident_id: str | None = None) -> list[AuditEvent]:
        """Read all events from today's log (optionally filter by incident)."""
        events: list[AuditEvent] = []
        if not self._log_file().exists():
            return events
        with open(self._log_file(), "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    event = AuditEvent.model_validate_json(line)
                    if incident_id is None or event.incident_id == incident_id:
                        events.append(event)
                except Exception:
                    continue
        return events

    def generate_report(
        self,
        incident_id: str,
        outcome: str = "Resolved",
    ) -> PostIncidentReport:
        """Generate a post-incident report from the audit trail."""
        events = self.get_all(incident_id=incident_id)
        responder_ids = list({
            e.details.get("responder_id") or e.details.get("to_responder")
            for e in events
            if isinstance(e.details, dict) and
               ("responder_id" in e.details or "to_responder" in e.details)
        } - {None})

        event_types = [e.event_type for e in events]
        summary = (
            f"Incident {incident_id} involved {len(events)} logged events. "
            f"Event types: {', '.join(set(event_types))}. "
            f"Responders involved: {len(responder_ids)}."
        )

        return PostIncidentReport(
            incident_id=incident_id,
            summary=summary,
            timeline=events,
            responders_involved=responder_ids,
            outcome=outcome,
        )
