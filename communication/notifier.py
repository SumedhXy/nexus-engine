"""
Communication Layer — Unified Alerting (Twilio & Firebase FCM)
Handles SMS/Voice for users and Push/Web notifications for responders.
"""
import os
from pathlib import Path
from dotenv import load_dotenv
import httpx
from typing import List, Optional
from models.schemas import Responder, ActionCard, StructuredIncidentObject

load_dotenv(Path(__file__).parent.parent / ".env")

# ---------------------------------------------------------------------------
# Twilio (SMS/Voice)
# ---------------------------------------------------------------------------
_TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
_TWILIO_AUTH = os.getenv("TWILIO_AUTH_TOKEN")
_TWILIO_FROM = os.getenv("TWILIO_FROM_NUMBER")

# ---------------------------------------------------------------------------
# Firebase (FCM) - We'll use the REST API to keep it simple without heavy SDK
# ---------------------------------------------------------------------------
_FCM_SERVER_KEY = os.getenv("FCM_SERVER_KEY")


class Notifier:
    """
    Unified communication hub for alerts.
    """

    def __init__(self):
        self.client = httpx.Client()

    def send_sms(self, to_number: str, message: str) -> bool:
        """Sends an SMS via Twilio REST API."""
        if not all([_TWILIO_SID, _TWILIO_AUTH, _TWILIO_FROM]):
            print("[Communication] ⚠️ Twilio credentials missing. Skipping SMS.")
            return False
            
        url = f"https://api.twilio.com/2010-04-01/Accounts/{_TWILIO_SID}/Messages.json"
        data = {
            "To": to_number,
            "From": _TWILIO_FROM,
            "Body": message
        }
        try:
            resp = self.client.post(url, data=data, auth=(_TWILIO_SID, _TWILIO_AUTH))
            if resp.status_code == 201:
                print(f"[Communication] ✅ SMS sent to {to_number}")
                return True
            else:
                print(f"[Communication] ❌ Twilio error {resp.status_code}: {resp.text}")
                return False
        except Exception as e:
            print(f"[Communication] ❌ SMS failed: {e}")
            return False

    def send_push_notification(self, topic: str, title: str, body: str, data: dict = None) -> bool:
        """Sends a push notification to responders via FCM."""
        if not _FCM_SERVER_KEY:
            print("[Communication] ⚠️ FCM Server Key missing. Skipping Push.")
            return False
            
        url = "https://fcm.googleapis.com/fcm/send"
        headers = {
            "Authorization": f"key={_FCM_SERVER_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "to": f"/topics/{topic}",
            "notification": {
                "title": title,
                "body": body,
                "sound": "default"
            },
            "data": data or {},
            "priority": "high"
        }
        try:
            resp = self.client.post(url, json=payload, headers=headers)
            if resp.status_code == 200:
                print(f"[Communication] ✅ Push notification sent to topic: {topic}")
                return True
            else:
                print(f"[Communication] ❌ FCM error {resp.status_code}: {resp.text}")
                return False
        except Exception as e:
            print(f"[Communication] ❌ Push failed: {e}")
            return False

    def notify_incident_received(self, incident: StructuredIncidentObject):
        """Notifies the user that their incident has been received."""
        # In a real app, we would look up the user's phone number
        user_phone = incident.raw_input.metadata.get("user_phone")
        if user_phone:
            msg = f"NEXUS ALERT: Your emergency request ({incident.incident_type.value}) has been received at {incident.location}. Help is being dispatched."
            self.send_sms(user_phone, msg)

    def notify_responders(self, assignments: List[ActionCard]):
        """Notifies assigned responders via Push."""
        for card in assignments:
            title = f"NEW MISSION: {card.role.value.upper()}"
            body = f"Incident: {card.priority}. Location: {card.location}. Action: {card.actions[0]}"
            self.send_push_notification(
                topic=f"responder_{card.responder_id}",
                title=title,
                body=body,
                data={"card_id": card.card_id}
            )
