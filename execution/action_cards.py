"""
Execution Layer — Dynamic Action Cards
Renders ActionCards with constraint annotations and priority banners.
"""
from __future__ import annotations
from models.schemas import ActionCard, OrchestratedActionPlan


class ActionCardRenderer:
    """
    Takes raw ActionCards from the dispatcher and enriches them
    with active constraints from the orchestration plan.
    """

    def render(
        self,
        cards: list[ActionCard],
        plan: OrchestratedActionPlan,
    ) -> list[dict]:
        rendered = []
        for card in cards:
            rendered.append({
                "card_id": card.card_id,
                "incident_id": card.incident_id,
                "priority": f"P{card.priority}",
                "role": card.role.value.upper().replace("_", " "),
                "responder": card.responder_name,
                "location": card.location,
                "actions": card.actions,
                "active_constraints": plan.active_constraints,
                "issued_at": card.issued_at.isoformat(),
            })
        return rendered

    def text_card(self, card: ActionCard, plan: OrchestratedActionPlan) -> str:
        """Returns a human-readable text card for CLI/logging purposes."""
        lines = [
            f"{'='*50}",
            f"  ACTION CARD — {card.role.value.upper().replace('_',' ')}",
            f"  Responder : {card.responder_name}",
            f"  Location  : {card.location}",
            f"  Priority  : P{card.priority}",
            f"{'='*50}",
            "  ACTIONS:",
        ]
        for i, action in enumerate(card.actions, start=1):
            lines.append(f"    {i}. {action}")
        if plan.active_constraints:
            lines.append("  CONSTRAINTS:")
            for c in plan.active_constraints:
                lines.append(f"    • {c}")
        lines.append("=" * 50)
        return "\n".join(lines)
