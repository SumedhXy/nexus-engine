import httpx
import json

url = "http://127.0.0.1:8000"

def test_multilingual():
    print("--- 🌍 NEXUS MULTILINGUAL SIMULATION 🌍 ---")
    
    # 1. Spanish Request
    print("\n[TEST 1] Spanish Input: '¡Ayuda! Hay un incendio en la cocina del segundo piso.'")
    payload_es = {
        "user_id": "user_123",
        "content": "¡Ayuda! Hay un incendio en la cocina del segundo piso. Hay mucho humo.",
        "metadata": {"location": "Building A"}
    }
    r_es = httpx.post(f"{url}/incident", json=payload_es, timeout=30)
    print(f"Status: {r_es.status_code}")
    if r_es.status_code == 200:
        d = r_es.json()
        print(f"   Detected Lang: {d['incident']['detected_language']}")
        print(f"   English Translation: {d['incident']['description']}")
        print(f"   SOP Matched: {d['sop']}")

    # 2. Hindi Request
    print("\n[TEST 2] Hindi Input: 'मदद करो, मुख्य प्रवेश द्वार पर एक आदमी बेहोश हो गया है।'")
    payload_hi = {
        "user_id": "user_123",
        "content": "मदद करो, मुख्य प्रवेश द्वार पर एक आदमी बेहोश हो गया है। उसे सांस लेने में तकलीफ हो रही है।",
        "metadata": {"location": "Main Entrance"}
    }
    r_hi = httpx.post(f"{url}/incident", json=payload_hi, timeout=30)
    if r_hi.status_code == 200:
        d = r_hi.json()
        print(f"   Detected Lang: {d['incident']['detected_language']}")
        print(f"   English Translation: {d['incident']['description']}")
        print(f"   Incident Type: {d['incident']['incident_type']}")

    # 3. History Retrieval
    print("\n[TEST 3] User History Check for 'user_123'")
    r_hist = httpx.get(f"{url}/history/user_123")
    if r_hist.status_code == 200:
        history = r_hist.json()
        print(f"   Found {len(history)} past incidents for this user.")
        for i, h in enumerate(history):
            print(f"   {i+1}: {h['incident_type']} at {h['location']} (Original: {h['original_content'][:30]}...)")

if __name__ == "__main__":
    test_multilingual()
