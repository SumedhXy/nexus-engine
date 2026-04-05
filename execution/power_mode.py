"""
Execution Layer — Power Mode Controller
Toggles between SENTRY (passive monitoring) and CRISIS (full activation).
"""
from __future__ import annotations
from models.schemas import PowerMode, SeverityLevel


# Auto-crisis threshold
_CRISIS_THRESHOLD = SeverityLevel.HIGH


class PowerModeController:
    """
    Manages the power mode of the Nexus Engine.
    SENTRY: low-resource passive mode (background monitoring only).
    CRISIS: full resource activation (all layers running at full capacity).
    """

    def __init__(self):
        self._mode: PowerMode = PowerMode.SENTRY

    @property
    def mode(self) -> PowerMode:
        return self._mode

    def auto_set(self, severity: SeverityLevel) -> PowerMode:
        """Automatically switch to CRISIS if severity meets threshold."""
        if severity >= _CRISIS_THRESHOLD:
            self._mode = PowerMode.CRISIS
        else:
            self._mode = PowerMode.SENTRY
        return self._mode

    def force(self, mode: PowerMode) -> None:
        """Manually force a power mode."""
        self._mode = mode
        print(f"[PowerMode] Forced to {mode.value.upper()}")

    def is_crisis(self) -> bool:
        return self._mode == PowerMode.CRISIS

    def is_sentry(self) -> bool:
        return self._mode == PowerMode.SENTRY
