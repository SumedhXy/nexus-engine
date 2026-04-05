"""
Shared Pydantic schemas for the Nexus Engine.
All layers communicate via these models.
"""
from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
import uuid


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class IncidentType(str, Enum):
    FIRE = "fire"
    FLOOD = "flood"
    EARTHQUAKE = "earthquake"
    MEDICAL = "medical"
    CHEMICAL = "chemical"
    STRUCTURAL = "structural"
    POLICE = "police"
    VEHICLE = "vehicle"
    UNKNOWN = "unknown"


class SeverityLevel(int, Enum):
    LOW = 1
    MODERATE = 2
    HIGH = 3
    CRITICAL = 4
    CATASTROPHIC = 5


class ResponderRole(str, Enum):
    POLICE = "police"
    AMBULANCE = "ambulance"
    HOSPITAL = "hospital"
    FIRE_BRIGADE = "fire_brigade"
    DISASTER_SAFETY = "disaster_safety"
    MANAGER = "manager"


class PowerMode(str, Enum):
    SENTRY = "sentry"      # Passive monitoring
    CRISIS = "crisis"      # Full activation


class ConnectivityState(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"


# ---------------------------------------------------------------------------
# Perception Layer Output
# ---------------------------------------------------------------------------

class RawInput(BaseModel):
    source: str = Field(..., description="Source of input: text|voice|iot|manual")
    content: Optional[str] = None
    audio_content: Optional[str] = Field(None, description="Base64 encoded audio/voice data for multimodal perception")
    user_id: str = Field(default="anonymous", description="ID of the user who submitted the request")
    language: Optional[str] = Field(None, description="Optional language hint (e.g., 'en', 'es', 'hi')")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class StructuredIncidentObject(BaseModel):
    incident_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str = "anonymous"
    incident_type: IncidentType
    severity: SeverityLevel
    location: str
    reporter: str
    description: str  # Translated to English for the engine
    original_content: Optional[str] = None
    detected_language: str = "en"
    semantic_tags: List[str] = Field(default_factory=list)
    confidence_score: float = Field(ge=0.0, le=1.0, default=1.0)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    raw_input: Optional[RawInput] = None


# ---------------------------------------------------------------------------
# Orchestration Layer Output
# ---------------------------------------------------------------------------

class SOPStep(BaseModel):
    step_number: int
    action: str
    responsible_role: ResponderRole
    constraints: List[str] = Field(default_factory=list)
    estimated_duration_mins: Optional[int] = None


class SOP(BaseModel):
    sop_id: str
    name: str
    incident_types: List[IncidentType]
    min_severity: SeverityLevel
    steps: List[SOPStep]
    constraints: List[str] = Field(default_factory=list)


class SafetyCheckResult(BaseModel):
    passed: bool
    violations: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


class OrchestratedActionPlan(BaseModel):
    plan_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    incident: StructuredIncidentObject
    matched_sop: SOP
    safety_check: SafetyCheckResult
    active_constraints: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    approved: bool = True


# ---------------------------------------------------------------------------
# Execution Layer
# ---------------------------------------------------------------------------

class Responder(BaseModel):
    responder_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    role: ResponderRole
    skills: List[str] = Field(default_factory=list)
    location_x: float = 0.0
    location_y: float = 0.0
    is_available: bool = True
    last_heartbeat: datetime = Field(default_factory=datetime.utcnow)


class ActionCard(BaseModel):
    card_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    incident_id: str
    responder_id: str
    responder_name: str
    role: ResponderRole
    actions: List[str]
    location: str
    priority: int = Field(ge=1, le=5)
    issued_at: datetime = Field(default_factory=datetime.utcnow)


class DispatchResult(BaseModel):
    incident_id: str
    assignments: List[ActionCard]
    unassigned_roles: List[ResponderRole] = Field(default_factory=list)
    dispatched_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Synchronization Layer
# ---------------------------------------------------------------------------

class MissionStateEntry(BaseModel):
    key: str
    value: Any
    timestamp: float          # Unix timestamp for LWW
    node_id: str


class DistributedMissionState(BaseModel):
    state_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    entries: Dict[str, MissionStateEntry] = Field(default_factory=dict)
    connectivity: ConnectivityState = ConnectivityState.ONLINE
    last_synced: Optional[datetime] = None


# ---------------------------------------------------------------------------
# Monitoring Layer
# ---------------------------------------------------------------------------

class HeartbeatStatus(BaseModel):
    responder_id: str
    last_seen: datetime
    is_alive: bool
    missed_beats: int = 0


class AuditEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    incident_id: Optional[str] = None
    event_type: str
    details: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    node_id: str = "nexus-primary"


class PostIncidentReport(BaseModel):
    report_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    incident_id: str
    summary: str
    timeline: List[AuditEvent]
    responders_involved: List[str]
    outcome: str
class UserProfile(BaseModel):
    user_id: str
    full_name: str
    emergency_contact_number: str
    medical_info: Optional[str] = None
    blood_group: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
