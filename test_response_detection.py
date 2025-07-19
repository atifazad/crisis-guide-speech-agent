#!/usr/bin/env python3
"""
Simple test for response detection system with async pipeline.
"""

import asyncio
import sys
import os
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.pipecat.response_detector import ResponseDetector, ResponseStatus

async def test_response_detector_async():
    """Test the response detection system with async."""
    print("🧪 Async Response Detection Test")
    print("=" * 50)
    
    # Initialize response detector with shorter timeouts for testing
    detector = ResponseDetector(
        timeout_threshold=2.0,      # 2 seconds for testing
        escalation_threshold=4.0,    # 4 seconds for testing
        emergency_threshold=6.0      # 6 seconds for testing
    )
    
    # Set up callbacks
    def on_timeout(message):
        print(f"⏰ TIMEOUT: {message}")
    
    def on_escalation(message):
        print(f"🚨 ESCALATION: {message}")
    
    def on_emergency(message):
        print(f"🚨 EMERGENCY: {message}")
    
    detector.set_callbacks(
        on_timeout=on_timeout,
        on_escalation=on_escalation,
        on_emergency=on_emergency
    )
    
    print("\n1. Testing Response Detection Initialization...")
    status = detector.get_status()
    print(f"   Status: {status['status']}")
    print(f"   Is Monitoring: {status['is_monitoring']}")
    print(f"   Timeout Threshold: {status['timeout_threshold']}s")
    
    print("\n2. Testing Response Monitoring Start...")
    detector.start_monitoring()
    status = detector.get_status()
    print(f"   Status: {status['status']}")
    print(f"   Is Monitoring: {status['is_monitoring']}")
    
    print("\n3. Testing User Response Detection...")
    print("   Simulating user response...")
    detector.user_responded()
    status = detector.get_status()
    print(f"   Status: {status['status']}")
    print(f"   Is Monitoring: {status['is_monitoring']}")
    
    print("\n4. Testing Timeout Scenario...")
    print("   Starting monitoring and waiting for timeout...")
    detector.start_monitoring()
    
    # Wait for timeout
    for i in range(3):
        print(f"   Waiting... ({i+1}/3)")
        await asyncio.sleep(1)
    
    status = detector.get_status()
    print(f"   Final Status: {status['status']}")
    print(f"   Time Since AI Speech: {status['time_since_ai_speech']:.1f}s")
    
    print("\n✅ Async response detection test completed!")

async def test_escalation_sequence():
    """Test the full escalation sequence."""
    print("\n🧪 Escalation Sequence Test")
    print("=" * 50)
    
    detector = ResponseDetector(
        timeout_threshold=1.0,      # 1 second for testing
        escalation_threshold=2.0,    # 2 seconds for testing
        emergency_threshold=3.0      # 3 seconds for testing
    )
    
    # Set up callbacks
    def on_timeout(message):
        print(f"⏰ TIMEOUT: {message}")
    
    def on_escalation(message):
        print(f"🚨 ESCALATION: {message}")
    
    def on_emergency(message):
        print(f"🚨 EMERGENCY: {message}")
    
    detector.set_callbacks(
        on_timeout=on_timeout,
        on_escalation=on_escalation,
        on_emergency=on_emergency
    )
    
    print("\n1. Starting escalation sequence...")
    detector.start_monitoring()
    
    print("\n2. Waiting for full escalation sequence...")
    # Wait for the full escalation sequence
    await asyncio.sleep(4)
    
    print("\n3. Simulating user response...")
    detector.user_responded()
    
    print("\n4. Final status...")
    status = detector.get_status()
    print(f"   Status: {status['status']}")
    print(f"   Is Monitoring: {status['is_monitoring']}")
    
    print("\n✅ Escalation sequence test completed!")

async def main():
    """Main test function."""
    print("🧪 Response Detection System Test Suite")
    print("=" * 60)
    
    # Test basic async functionality
    await test_response_detector_async()
    
    # Test escalation sequence
    await test_escalation_sequence()
    
    print("\n" + "=" * 60)
    print("✅ All response detection tests completed!")
    print("\nNext steps:")
    print("1. Integrate with pipecat pipeline")
    print("2. Test with real audio input/output")
    print("3. Implement emergency service integration")

if __name__ == "__main__":
    asyncio.run(main()) 