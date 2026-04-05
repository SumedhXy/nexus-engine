"""
Orchestration Layer — Safety Gate (Deterministic Validator)
NOT AI-based. Pure rule checks before any action plan is broadcast.
"""
from __future__ import annotations
from models.schemas import StructuredIncidentObject, SOP, SafetyCheckResult, IncidentType


# Hard-coded safety rules
_GLOBAL_RULES: list[tuple[str, callable]] = [
    (
        "Do not use elevators in a fire",
        lambda incident, sop: not (
            incident.incident_type == IncidentType.FIRE and
            any("elevator" in step.action.lower() for step in sop.steps)
        ),
    ),
    (
        "Verify before broadcast — incident must have minimum confidence",
        lambda incident, sop: incident.confidence_score >= 0.4,
    ),
    (
        "Severity must be at or above SOP minimum",
        lambda incident, sop: incident.severity >= sop.min_severity,
    ),
    (
        "Incident must have a known location",
        lambda incident, sop: incident.location not in ("Unknown Location", "", None),
    ),
]


class SafetyGate:
    """
    Deterministic validator — all rules must pass before the plan is approved.
    Violations block the plan; warnings allow it but flag issues.
    """

    def validate(
        self,
        incident: StructuredIncidentObject,
        sop: SOP,
    ) -> SafetyCheckResult:
        violations: list[str] = []
        warnings: list[str] = []

        for rule_name, rule_fn in _GLOBAL_RULES:
            try:
                if not rule_fn(incident, sop):
                    violations.append(rule_name)
            except Exception as e:
                warnings.append(f"Rule '{rule_name}' raised error: {e}")

        # Also check SOP-level constraints
        for constraint in sop.constraints:
            if "verify" in constraint.lower() and incident.confidence_score < 0.6:
                warnings.append(f"Low confidence ({incident.confidence_score:.0%}) — '{constraint}'")

        return SafetyCheckResult(
            passed=len(violations) == 0,
            violations=violations,
            warnings=warnings,
        )
