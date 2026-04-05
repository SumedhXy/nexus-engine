import json
import httpx
import time

url = "http://127.0.0.1:8888"

def run_simulation():
    try:
        print("--- SUBMITTING TACTICAL INCIDENT ---")
        payload = {
            "source": "web-app",
            "content": "TEST SOS: Medical emergency in the north lobby. Unconscious individual.",
            "user_id": "test-user-001",
            "metadata": {"location": "North Lobby"}
        }
        
        start_time = time.time()
        print(f"[NEXUS SIGNAL] Sending SOS to {url}/incident...")
        r = httpx.post(f"{url}/incident", json=payload, timeout=30)
        end_time = time.time()
        
        if r.status_code == 200:
            d = r.json()
            print(f"[SUCCESS] (Response: {end_time - start_time:.2f}s)")
            print(f"Type: {d['incident']['incident_type']}")
            print(f"Description: {d['incident']['description']}")
            print(f"Severity: {d['incident']['severity']}")
            print(f"Confidence: {d['incident']['confidence_score']}")
            print(f"Active Protocol: {d['sop']['name']}")
            
            print(f"\n[DISPATCH ROSTER]:")
            assignments = d['dispatch']['assignments']
            if not assignments:
                print("No responders unassigned currently.")
            for card in assignments:
                print(f"- UNIT: [{card['role']}] {card['responder_name']}")
                print(f"  MISSION: {card['actions'][0] if card['actions'] else 'Standby'}")
        else:
            print(f"ERROR {r.status_code}: {r.text}")

    except Exception as e:
        print(f"CONNECTION FAILED: {e}")

if __name__ == "__main__":
    run_simulation()
