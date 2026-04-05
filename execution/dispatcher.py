"""
Execution Layer — Proximity-Priority Dispatcher
Assigns responders to the action plan using the priority defined in the SOP steps.
Ensures critical authorities (Fire, Ambulance) are dispatched first.
"""
from __future__ import annotations
import math
from models.schemas import (
    OrchestratedActionPlan, Responder, ResponderRole,
    ActionCard, DispatchResult
)

def _distance(r: Responder, incident_x: float, incident_y: float) -> float:
    return math.sqrt((r.location_x - incident_x) ** 2 + (r.location_y - incident_y) ** 2)

def _skill_bonus(responder: Responder, role: ResponderRole) -> float:
    """Bonus for role match."""
    if responder.role == role:
        return 10.0
    return 0.0

def _dispatch_score(responder: Responder, role: ResponderRole,
                    inc_x: float, inc_y: float) -> float:
    dist = _distance(responder, inc_x, inc_y)
    proximity = 1.0 / (dist + 0.1)
    skill = _skill_bonus(responder, role)
    return skill + proximity

class ProximityRoleDispatcher:
    """
    Assigns authorities per required SOP step.
    Enforces priority sequencing based on SOP step order.
    """

    def dispatch(
        self,
        plan: OrchestratedActionPlan,
        responders: list[Responder],
        incident_x: float = 0.0,
        incident_y: float = 0.0,
    ) -> DispatchResult:
        incident = plan.incident
        sop = plan.matched_sop
        
        # MISSION-CRITICAL: Sort roles by their first appearance in the SOP steps (Priority order)
        # step_number 1 = Highest Priority
        roles_with_priority = []
        seen_roles = set()
        for step in sorted(sop.steps, key=lambda s: s.step_number):
            if step.responsible_role not in seen_roles:
                roles_with_priority.append((step.responsible_role, step.step_number))
                seen_roles.add(step.responsible_role)

        available = [r for r in responders if r.is_available]
        assignments: list[ActionCard] = []
        unassigned: list[ResponderRole] = []
        assigned_ids: set[str] = set()

        for role, priority_level in roles_with_priority:
            candidates = [r for r in available if r.responder_id not in assigned_ids]
            
            # Find best responder for this authority
            if not candidates:
                unassigned.append(role)
                continue

            best = max(
                candidates,
                key=lambda r: _dispatch_score(r, role, incident_x, incident_y)
            )
            assigned_ids.add(best.responder_id)

            # Build action list for this SPECIFIC authority
            role_actions = [
                step.action for step in sop.steps if step.responsible_role == role
            ]

            card = ActionCard(
                incident_id=incident.incident_id,
                responder_id=best.responder_id,
                responder_name=best.name,
                role=role,
                actions=role_actions,
                location=incident.location,
                priority=priority_level, # Higher priority based on SOP step
            )
            assignments.append(card)

        # Final mission result: Sorted by priority level (1 first)
        assignments.sort(key=lambda c: c.priority)

        return DispatchResult(
            incident_id=incident.incident_id,
            assignments=assignments,
            unassigned_roles=unassigned,
        )
