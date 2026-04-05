"""Tests for the Execution Layer."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from execution.dispatcher import ProximityRoleDispatcher
from execution.power_mode import PowerModeController
from execution.action_cards import ActionCardRenderer
from models.schemas import (
    Responder, ResponderRole, SeverityLevel, PowerMode,
    StructuredIncidentObject, IncidentType, OrchestratedActionPlan,
    SafetyCheckResult, SOP, SOPStep
)


def make_sop():
    return SOP(
        sop_id="TEST-001",
        name="Test SOP",
        incident_types=[IncidentType.FIRE],
        min_severity=SeverityLevel.MODERATE,
        steps=[
            SOPStep(step_number=1, action="Clear exits", responsible_role=ResponderRole.SECURITY_GUARD),
            SOPStep(step_number=2, action="Set up triage", responsible_role=ResponderRole.MEDIC),
        ],
    )

def make_plan():
    incident = StructuredIncidentObject(
        incident_type=IncidentType.FIRE,
        severity=SeverityLevel.CRITICAL,
        location="Block B",
        reporter="Test",
        description="Test fire",
        confidence_score=0.9,
    )
    sop = make_sop()
    return OrchestratedActionPlan(
        incident=incident,
        matched_sop=sop,
        safety_check=SafetyCheckResult(passed=True),
        active_constraints=["Do not use elevators"],
    )

def make_responders():
    return [
        Responder(name="Alice", role=ResponderRole.SECURITY_GUARD, location_x=1.0, location_y=1.0),
        Responder(name="Bob", role=ResponderRole.MEDIC, location_x=2.0, location_y=2.0),
    ]

def test_dispatcher_assigns_cards():
    dispatcher = ProximityRoleDispatcher()
    result = dispatcher.dispatch(make_plan(), make_responders(), 0.0, 0.0)
    assert len(result.assignments) == 2

def test_dispatcher_correct_roles():
    dispatcher = ProximityRoleDispatcher()
    result = dispatcher.dispatch(make_plan(), make_responders(), 0.0, 0.0)
    roles = {c.role for c in result.assignments}
    assert ResponderRole.SECURITY_GUARD in roles
    assert ResponderRole.MEDIC in roles

def test_dispatcher_no_responders():
    dispatcher = ProximityRoleDispatcher()
    result = dispatcher.dispatch(make_plan(), [], 0.0, 0.0)
    assert len(result.assignments) == 0
    assert len(result.unassigned_roles) == 2

def test_power_mode_auto_crisis():
    ctrl = PowerModeController()
    mode = ctrl.auto_set(SeverityLevel.CRITICAL)
    assert mode == PowerMode.CRISIS

def test_power_mode_auto_sentry():
    ctrl = PowerModeController()
    mode = ctrl.auto_set(SeverityLevel.LOW)
    assert mode == PowerMode.SENTRY

def test_action_card_renderer():
    dispatcher = ProximityRoleDispatcher()
    plan = make_plan()
    result = dispatcher.dispatch(plan, make_responders(), 0.0, 0.0)
    renderer = ActionCardRenderer()
    rendered = renderer.render(result.assignments, plan)
    assert len(rendered) == 2
    assert "actions" in rendered[0]
    assert "active_constraints" in rendered[0]
