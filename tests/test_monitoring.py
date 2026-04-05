"""Tests for the Monitoring Layer."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import time
import pytest
from monitoring.heartbeat import HeartbeatMonitor
from monitoring.audit_log import AuditLog
from models.schemas import Responder, ResponderRole, AuditEvent
import tempfile
from pathlib import Path


@pytest.fixture
def responder():
    return Responder(
        name="Test Responder",
        role=ResponderRole.MEDIC,
    )

def test_heartbeat_register_and_alive(responder):
    monitor = HeartbeatMonitor()
    monitor.register(responder)
    status = monitor.get_status(responder.responder_id)
    assert status is not None
    assert status.is_alive is True

def test_heartbeat_record_beat(responder):
    monitor = HeartbeatMonitor()
    monitor.register(responder)
    monitor.record_beat(responder.responder_id)
    status = monitor.get_status(responder.responder_id)
    assert status.missed_beats == 0

def test_heartbeat_all_statuses(responder):
    monitor = HeartbeatMonitor()
    monitor.register(responder)
    statuses = monitor.all_statuses()
    assert len(statuses) == 1

def test_audit_log_append_and_read():
    with tempfile.TemporaryDirectory() as tmpdir:
        log = AuditLog(log_dir=Path(tmpdir))
        event = AuditEvent(
            incident_id="INC-001",
            event_type="TEST_EVENT",
            details={"key": "value"},
        )
        log.log(event)
        events = log.get_all(incident_id="INC-001")
        assert len(events) == 1
        assert events[0].event_type == "TEST_EVENT"

def test_audit_log_immutable_append():
    """Each call to log() appends; previous entries stay unchanged."""
    with tempfile.TemporaryDirectory() as tmpdir:
        log = AuditLog(log_dir=Path(tmpdir))
        for i in range(3):
            log.log(AuditEvent(
                incident_id="INC-002",
                event_type=f"EVENT_{i}",
                details={},
            ))
        events = log.get_all(incident_id="INC-002")
        assert len(events) == 3

def test_post_incident_report():
    with tempfile.TemporaryDirectory() as tmpdir:
        log = AuditLog(log_dir=Path(tmpdir))
        log.log(AuditEvent(incident_id="INC-003", event_type="DISPATCH", details={"responder_id": "R1"}))
        log.log(AuditEvent(incident_id="INC-003", event_type="COMPLETE", details={}))
        report = log.generate_report("INC-003", outcome="Resolved")
        assert report.incident_id == "INC-003"
        assert len(report.timeline) == 2
        assert report.outcome == "Resolved"
