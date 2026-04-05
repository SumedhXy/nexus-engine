"""
Monitoring Layer — Timeout/Escalation & Auto-Reassignment
Detects incapacitated responders and reassigns their action cards.
"""
from __future__ import annotations
from datetime import datetime
from models.schemas import ActionCard, Responder, ResponderRole, AuditEvent
from monitoring.audit_log import AuditLog


class EscalationManager:
    """
    Monitors active assignments; when a responder is flagged dead/incapacitated,
    re-assigns their ActionCards to the next best available responder.
    """

    def __init__(self, audit_log: AuditLog):
        self._audit = audit_log
        self._active_cards: list[ActionCard] = []
        self._responders: list[Responder] = []

    def register_assignments(self, cards: list[ActionCard]) -> None:
        self._active_cards.extend(cards)

    def register_responders(self, responders: list[Responder]) -> None:
        self._responders = list(responders)

    def escalate(self, incapacitated_responder_id: str) -> list[ActionCard]:
        """
        Called when Dead Man's Switch fires.
        Re-routes cards from incapacitated responder to next available.
        Returns list of newly issued replacement cards.
        """
        affected = [c for c in self._active_cards if c.responder_id == incapacitated_responder_id]
        available = [r for r in self._responders
                     if r.is_available and r.responder_id != incapacitated_responder_id]
        new_cards: list[ActionCard] = []

        for card in affected:
            # Find best available responder matching role
            best = next(
                (r for r in available if r.role == card.role),
                available[0] if available else None
            )
            if not best:
                print(f"[Escalation] No available responder to replace {incapacitated_responder_id}")
                continue

            new_card = ActionCard(
                incident_id=card.incident_id,
                responder_id=best.responder_id,
                responder_name=best.name,
                role=card.role,
                actions=card.actions,
                location=card.location,
                priority=card.priority,
            )
            new_cards.append(new_card)
            self._active_cards.remove(card)
            self._active_cards.append(new_card)
            available.remove(best)  # Prevent double-assignment

            self._audit.log(AuditEvent(
                incident_id=card.incident_id,
                event_type="ESCALATION_REASSIGNMENT",
                details={
                    "from_responder": incapacitated_responder_id,
                    "to_responder": best.responder_id,
                    "role": card.role.value,
                    "card_id": card.card_id,
                },
            ))

        return new_cards
