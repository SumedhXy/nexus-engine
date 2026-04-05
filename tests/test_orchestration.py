"""Tests for the Orchestration Layer."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from orchestration.sop_library import SOPLibrary
from orchestration.protocol_matcher import ProtocolMatcher
from orchestration.safety_gate import SafetyGate
from orchestration.constraint_logic import ConstraintLogic
from models.schemas import StructuredIncidentObject, IncidentType, SeverityLevel


@pytest.fixture
def library():
    return SOPLibrary()

@pytest.fixture
def matcher(library):
    return ProtocolMatcher(library)

@pytest.fixture
def fire_incident():
    return StructuredIncidentObject(
        incident_type=IncidentType.FIRE,
        severity=SeverityLevel.CRITICAL,
        location="Block B, Floor 3",
        reporter="IoT-42",
        description="Smoke and fire detected",
        confidence_score=0.85,
    )

@pytest.fixture
def low_confidence_incident():
    return StructuredIncidentObject(
        incident_type=IncidentType.FIRE,
        severity=SeverityLevel.HIGH,
        location="Block A",
        reporter="Manual",
        description="Possible fire smell",
        confidence_score=0.3,
    )

def test_sop_library_loads(library):
    sops = library.get_all()
    assert len(sops) >= 1

def test_sop_library_fire_type(library):
    sops = library.get_by_type(IncidentType.FIRE)
    assert len(sops) >= 1

def test_protocol_matcher_fire(matcher, fire_incident):
    sop = matcher.match(fire_incident)
    assert sop is not None
    assert IncidentType.FIRE in sop.incident_types

def test_safety_gate_passes(fire_incident, library):
    sop = library.get_by_type(IncidentType.FIRE)[0]
    gate = SafetyGate()
    result = gate.validate(fire_incident, sop)
    assert result.passed is True

def test_safety_gate_blocks_low_confidence(low_confidence_incident, library):
    sop = library.get_by_type(IncidentType.FIRE)[0]
    gate = SafetyGate()
    result = gate.validate(low_confidence_incident, sop)
    # Confidence 0.3 < 0.4 threshold → should fail
    assert result.passed is False
    assert len(result.violations) >= 1

def test_constraint_logic_fire(fire_incident, library):
    sop = library.get_by_type(IncidentType.FIRE)[0]
    logic = ConstraintLogic()
    constraints = logic.evaluate(fire_incident, sop)
    assert any("elevator" in c.lower() for c in constraints)
