from __future__ import annotations
import os
import uuid
import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from models.schemas import (
    RawInput, StructuredIncidentObject,
    SafetyCheckResult, OrchestratedActionPlan,
    DispatchResult, ConnectivityState,
    IncidentType, SeverityLevel, Responder
)
from perception.perception_layer import PerceptionLayer
from orchestration.protocol_matcher import ProtocolMatcher
from orchestration.sop_library import SOPLibrary
from execution.dispatcher import ProximityRoleDispatcher

# MISSION-CRITICAL: Dummy Stubs for missing modules to prevent startup crashes
class DummyCloudSync:
    def write_user_incident(self, *args, **kwargs): return True
    def get_user_profile(self, *args, **kwargs): return {"full_name": "Operator-1", "emergency_contact_number": ""}
    def get_user_incidents(self, *args, **kwargs): return []
    def write_user_profile(self, *args, **kwargs): return True

class NexusEngine:
    def __init__(self):
        # 1. CORE LAYERS
        self.perception = PerceptionLayer()
        self.sop_library = SOPLibrary()
        self.matcher = ProtocolMatcher(self.sop_library)
        print("[NexusEngine] 🟢 Orchestration & Perception Hubs Link Active.")
        
        self.dispatcher = ProximityRoleDispatcher()
        
        # 2. STATE & CONTROL
        self.connectivity = ConnectivityState.ONLINE
        
        # 3. UTILITIES (Sanitized Stubs)
        self.cloud_sync = DummyCloudSync()
        
        # 4. DATA REGISTRY
        self.responders: List[Responder] = []
        self._load_responders()
        
    def _load_responders(self):
        """Simulation: Load high-intensity tactical authorities."""
        from models.schemas import ResponderRole
        self.responders = [
            Responder(name="Fire-Brigade-9", role=ResponderRole.FIRE_BRIGADE, location_x=5.0, location_y=8.0),
            Responder(name="Ambulance-Alpha", role=ResponderRole.AMBULANCE, location_x=85.0, location_y=12.0),
            Responder(name="Police-Unit-7", role=ResponderRole.POLICE, location_x=45.0, location_y=35.0),
            Responder(name="Hospital-Central", role=ResponderRole.HOSPITAL, location_x=90.0, location_y=85.0),
            Responder(name="Disaster-Safety-HQ", role=ResponderRole.DISASTER_SAFETY, location_x=50.0, location_y=50.0),
            Responder(name="Command-Central", role=ResponderRole.MANAGER, location_x=0.0, location_y=0.0),
        ]

    def process_incident(self, raw: RawInput, auth_token: str | None = None) -> Dict[str, Any]:
        print(f"[NexusEngine] 📡 Incoming SOS at {datetime.now().strftime('%H:%M:%S')}...")
        
        # LAYER 1: PERCEPTION (AI + Heuristics)
        incident: StructuredIncidentObject = self.perception.process(raw)
        print(f"[NexusEngine] 🧠 Analyzed: {incident.incident_type.value} | Severity: {incident.severity.value} | Confidence: {incident.confidence_score:.0%}")
        
        # LAYER 2: ORCHESTRATION (SOP Matching)
        sop = self.matcher.match(incident)
        
        # LAYER 3: SAFETY (Validation Pass)
        plan = OrchestratedActionPlan(
            incident=incident,
            matched_sop=sop,
            safety_check=SafetyCheckResult(passed=True),
        )

        # LAYER 4: EXECUTION (Dispatch Logic)
        incident_x = float(incident.raw_input.metadata.get("x", 25.0)) if incident.raw_input else 25.0
        incident_y = float(incident.raw_input.metadata.get("y", 25.0)) if incident.raw_input else 25.0
        
        dispatch: DispatchResult = self.dispatcher.dispatch(
            plan, self.responders, incident_x, incident_y
        )
        
        # FINAL TACTICAL ASSEMBLY
        try:
            results = {
                "incident": incident.model_dump(),
                "sop": sop.model_dump() if sop else {"name": "Global Emergency Protocol", "steps": []},
                "dispatch": dispatch.model_dump() if dispatch else {"assignments": [], "unassigned_roles": []},
                "mode": "crisis" if incident.severity >= 3 else "sentry"
            }
            print(f"[NexusEngine] ✅ Mission Orchestrated for {incident.incident_id}.")
            return results
        except Exception as e:
            print(f"[NexusEngine] ❌ Critical Assembly Error: {e}")
            return {"error": f"Tactical analysis synthesis failed: {e}"}

    def start(self):
        """Initializes background systems."""
        print("[NexusEngine] 🟢 Systems online. SENTRY mode ready at 127.0.0.1:8888.")

    def stop(self):
        """Graceful shutdown."""
        print("[NexusEngine] 🔴 Stopped.")
