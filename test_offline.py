import sys
import os
import json
from engine import NexusEngine
from models.schemas import RawInput

def test_offline_mode():
    print("--- Nexus Engine: Offline Mode Diagnostic ---")
    
    # Initialize Engine
    # Reminder: ConnectivityMonitor is currently MOCKED to return OFFLINE
    engine = NexusEngine()
    
    # Start internal listeners/monitors
    engine.start()
    print("Engine started (Offline Mode).")

    # Simulation data
    raw = RawInput(
        source="emergency_call",
        content="MEDICAL EMERGENCY: Unconscious patient found in the lobby. No pulse. Offline mode test.",
        metadata={"location": "Main Lobby", "reporter": "Security"}
    )

    print("\nProcessing Incident...")
    print("-" * 40)
    
    # This call should trigger MeshNetwork.broadcast() instead of CloudSync.push()
    result = engine.process_incident(raw)
    
    print("-" * 40)
    print(f"\n[DIAGNOSTIC RESULTS]")
    print(f"   Connectivity Detected: {result['connectivity'].upper()}")
    print(f"   Incident Recognized:   {result['incident']['incident_type']}")
    print(f"   SOP Triggered:         {result['sop']}")
    
    if result['connectivity'] == "offline":
        print("\n[SUCCESS] Pipeline rerouted to Synchronization Layer -> P2P Mesh Network.")
        print("Check the logs above for '[MeshNetwork] Broadcast ... to mesh.'")
    else:
        print("\n[ERROR] System still thinks it is online. Connectivity mock failed.")

    # Cleanup
    engine.stop()
    print("\nDone.")

if __name__ == "__main__":
    test_offline_mode()
