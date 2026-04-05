from __future__ import annotations
from typing import Dict, List, Optional
from models.schemas import (
    IncidentType, ResponderRole, SOP, SOPStep, SeverityLevel
)

class SOPLibrary:
    def __init__(self):
        # We now use the official Pydantic SOP model for 100% mission-consistency
        self.library: Dict[IncidentType, SOP] = {
            # 🚑 MEDICAL: Life-Safety Core
            IncidentType.MEDICAL: SOP(
                sop_id="SOP-MED-01",
                name="Critical Medical Response Protocol",
                incident_types=[IncidentType.MEDICAL],
                min_severity=SeverityLevel.LOW,
                steps=[
                    SOPStep(step_number=1, action="Dispatch Ambulance Alpha to provided GPS location.", responsible_role=ResponderRole.AMBULANCE),
                    SOPStep(step_number=2, action="Alert Hospital Central to prepare Emergency Room.", responsible_role=ResponderRole.HOSPITAL),
                    SOPStep(step_number=3, action="Dispatch Police Unit to clear traffic route.", responsible_role=ResponderRole.POLICE),
                ]
            ),
            
            # 🔥 FIRE: Suppression and Rescue
            IncidentType.FIRE: SOP(
                sop_id="SOP-FIRE-01",
                name="High-Intensity Fire Suppression Protocol",
                incident_types=[IncidentType.FIRE],
                min_severity=SeverityLevel.LOW,
                steps=[
                    SOPStep(step_number=1, action="Dispatch Fire Brigade for primary suppression.", responsible_role=ResponderRole.FIRE_BRIGADE),
                    SOPStep(step_number=2, action="Dispatch Ambulance for casualty assessment.", responsible_role=ResponderRole.AMBULANCE),
                    SOPStep(step_number=3, action="Alert Hospital to prepare burn unit.", responsible_role=ResponderRole.HOSPITAL),
                    SOPStep(step_number=4, action="Dispatch Police for perimeter control.", responsible_role=ResponderRole.POLICE),
                ]
            ),

            # 🚔 CIVIL/POLICE (Scenarios 5 & 6): PRIORITIZE AMBULANCE
            IncidentType.POLICE: SOP(
                sop_id="SOP-POL-01",
                name="Civil Disturbance & Security Response",
                incident_types=[IncidentType.POLICE],
                min_severity=SeverityLevel.LOW,
                steps=[
                    SOPStep(step_number=1, action="Dispatch Ambulance to standby for casualties.", responsible_role=ResponderRole.AMBULANCE),
                    SOPStep(step_number=2, action="Alert Hospital Central for mission intake.", responsible_role=ResponderRole.HOSPITAL),
                    SOPStep(step_number=3, action="Dispatch Police Force for neutralization/arrest.", responsible_role=ResponderRole.POLICE),
                ]
            ),

            # 🛰️ DISASTER: Massive Coordinated Response
            IncidentType.EARTHQUAKE: SOP(
                sop_id="SOP-DIS-01",
                name="Catastrophic Disaster Recovery Protocol",
                incident_types=[IncidentType.EARTHQUAKE],
                min_severity=SeverityLevel.LOW,
                steps=[
                    SOPStep(step_number=1, action="Activate Disaster Safety Authority (DSA) HQ.", responsible_role=ResponderRole.DISASTER_SAFETY),
                    SOPStep(step_number=2, action="Dispatch all Ambulance units for mass-casualty triage.", responsible_role=ResponderRole.AMBULANCE),
                    SOPStep(step_number=3, action="Dispatch Fire Brigades for structural fires.", responsible_role=ResponderRole.FIRE_BRIGADE),
                    SOPStep(step_number=4, action="Alert all local Hospitals to activate Disaster Mode.", responsible_role=ResponderRole.HOSPITAL),
                ]
            ),
            
            # ☣️ CHEMICAL: Containment
            IncidentType.CHEMICAL: SOP(
                sop_id="SOP-CHEM-01",
                name="Toxic/Chemical Hazard Containment",
                incident_types=[IncidentType.CHEMICAL],
                min_severity=SeverityLevel.LOW,
                steps=[
                    SOPStep(step_number=1, action="Activate DSA for hazmat containment.", responsible_role=ResponderRole.DISASTER_SAFETY),
                    SOPStep(step_number=2, action="Dispatch Fire Brigade for decontamination spray.", responsible_role=ResponderRole.FIRE_BRIGADE),
                    SOPStep(step_number=3, action="Alert Hospital to prepare toxicity units.", responsible_role=ResponderRole.HOSPITAL),
                ]
            ),

            # 🏗️ STRUCTURAL: Stabilization
            IncidentType.STRUCTURAL: SOP(
                sop_id="SOP-STR-01",
                name="Structural Integrity & Recovery",
                incident_types=[IncidentType.STRUCTURAL],
                min_severity=SeverityLevel.LOW,
                steps=[
                    SOPStep(step_number=1, action="Activate DSA for heavy engineering support.", responsible_role=ResponderRole.DISASTER_SAFETY),
                    SOPStep(step_number=2, action="Dispatch Ambulance for victim extraction.", responsible_role=ResponderRole.AMBULANCE),
                    SOPStep(step_number=3, action="Dispatch Police for cordon establishment.", responsible_role=ResponderRole.POLICE),
                ]
            ),

            # 🚌 VEHICLE/TRAFFIC (Scenarios 11 & 12): PRIORITIZE AMBULANCE
            IncidentType.VEHICLE: SOP(
                sop_id="SOP-VEH-01",
                name="Multi-Vehicle Collision Response",
                incident_types=[IncidentType.VEHICLE],
                min_severity=SeverityLevel.LOW,
                steps=[
                    SOPStep(step_number=1, action="Dispatch Ambulance Alpha for victim extraction.", responsible_role=ResponderRole.AMBULANCE),
                    SOPStep(step_number=2, action="Alert Hospital Central for internal injuries.", responsible_role=ResponderRole.HOSPITAL),
                    SOPStep(step_number=3, action="Dispatch Police Unit to secure high-speed lanes.", responsible_role=ResponderRole.POLICE),
                ]
            )
        }

    def get_by_type(self, incident_type: IncidentType) -> Optional[SOP]:
        return self.library.get(incident_type)
