"""
Orchestration Layer — Constraint Logic
Applies active constraint rules to the action plan, filtering/annotating steps.
"""
from __future__ import annotations
from models.schemas import OrchestratedActionPlan, SOP, StructuredIncidentObject, IncidentType


# Constraint rule registry: (description, check_fn) → returns active constraint string or None
_CONSTRAINT_RULES: list[tuple[str, callable]] = [
    (
        "No elevator use during fire",
        lambda i, s: "⚠️ DO NOT USE ELEVATORS — use stairwells only"
        if i.incident_type == IncidentType.FIRE else None,
    ),
    (
        "Verify before broadcast",
        lambda i, s: "⚠️ VERIFY INCIDENT BEFORE BROADCAST — do not alert externally until confirmed"
        if i.confidence_score < 0.8 else None,
    ),
    (
        "Chemical hazard PPE",
        lambda i, s: "⚠️ CHEMICAL HAZARD — all responders must don PPE before entering area"
        if i.incident_type == IncidentType.CHEMICAL else None,
    ),
    (
        "Flood electrical isolation",
        lambda i, s: "⚠️ FLOOD — isolate all electrical circuits in affected zones before entry"
        if i.incident_type == IncidentType.FLOOD else None,
    ),
]


class ConstraintLogic:
    """Evaluates global constraint rules and returns the active set."""

    def evaluate(
        self,
        incident: StructuredIncidentObject,
        sop: SOP,
    ) -> list[str]:
        active: list[str] = []
        for _, rule_fn in _CONSTRAINT_RULES:
            result = rule_fn(incident, sop)
            if result:
                active.append(result)
        # Also include any SOP-level constraints
        active.extend(sop.constraints)
        return list(dict.fromkeys(active))  # Deduplicate, preserve order
