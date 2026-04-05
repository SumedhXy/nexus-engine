import os
from pathlib import Path
from dotenv import load_dotenv
import httpx
from datetime import datetime

# Load configuration from the primary .env
load_dotenv(Path(__file__).parent / ".env")

def test_firebase():
    url = os.getenv("FIREBASE_DATABASE_URL", "").rstrip("/")
    project_id = os.getenv("FIREBASE_PROJECT_ID")
    
    print("--- [NEXUS FIREBASE DIAGNOSTIC V2] ---")
    print(f"Project ID:   {project_id}")
    print(f"Database URL: {url}")
    print("----------------------------------")

    if not url:
        print("[ERROR] Database URL is missing from .env")
        return

    payload = {
        "status": "connected",
        "last_ping": datetime.utcnow().isoformat(),
        "mission": "NEXUS Core Integration"
    }

    print("\n[Action] Attempting secure handshake with Firebase RTDB...")
    
    try:
        # We append /.json for the Firebase REST API
        resp = httpx.put(f"{url}/nexus_diagnostic.json", json=payload, timeout=15.0)
        
        if resp.status_code == 200:
            print("[SUCCESS] Connection Established!")
            print(f"[Link] Data written to: {url}/nexus_diagnostic")
            print(f"[Details] Result: {resp.text}")
        else:
            print(f"[FAILED] Firebase rejected the request (Status: {resp.status_code})")
            print("[TIP] Ensure your 'Realtime Database Rules' are set to allow access.")
            print(f"[Error Summary] {resp.text}")
            
    except httpx.ConnectError:
        print("[CRITICAL] Could not resolve host or reach Firebase. Check your internet connection.")
    except Exception as e:
        print(f"[CRITICAL] Connection error: {type(e).__name__}")
        print(f"[Details] {e}")

if __name__ == "__main__":
    test_firebase()
