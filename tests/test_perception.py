"""Tests for the Perception Layer."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from perception.perception_layer import PerceptionLayer
from models.schemas import RawInput, IncidentType, SeverityLevel


@pytest.fixture
def layer():
    return PerceptionLayer()

@pytest.fixture
def fire_input():
    return RawInput(source="iot", content="Smoke and fire detected in corridor near Block B Floor 3", metadata={"location": "Block B, Floor 3", "reporter": "IoT-42"})

@pytest.fixture
def medical_input():
    return RawInput(source="manual", content="A person is unconscious and bleeding near the lobby", metadata={"reporter": "Staff-01"})

def test_fire_classification(layer, fire_input):
    result = layer.process(fire_input)
    assert result.incident_type == IncidentType.FIRE

def test_medical_classification(layer, medical_input):
    result = layer.process(medical_input)
    assert result.incident_type == IncidentType.MEDICAL

def test_location_from_metadata(layer, fire_input):
    result = layer.process(fire_input)
    assert result.location == "Block B, Floor 3"

def test_semantic_tags_fire(layer, fire_input):
    result = layer.process(fire_input)
    assert "fire_hazard" in result.semantic_tags

def test_semantic_tags_medical(layer, medical_input):
    result = layer.process(medical_input)
    assert "casualties_reported" in result.semantic_tags

def test_confidence_score_range(layer, fire_input):
    result = layer.process(fire_input)
    assert 0.0 <= result.confidence_score <= 1.0

def test_severity_scoring(layer):
    critical_input = RawInput(source="text", content="Critical explosion multiple casualties confirmed")
    result = layer.process(critical_input)
    assert result.severity >= SeverityLevel.CRITICAL

def test_unknown_incident(layer):
    vague = RawInput(source="text", content="Something happened somewhere")
    result = layer.process(vague)
    assert result.incident_type == IncidentType.UNKNOWN
