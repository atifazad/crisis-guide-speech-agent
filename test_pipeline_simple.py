#!/usr/bin/env python3
"""
Simple pipeline test without blocking runner.
Tests individual components and response detection.
"""

import asyncio
import time
import sys
import os
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.pipecat.pipeline_manager import PipecatPipelineManager

def test_pipeline_components():
    """Test individual pipeline components."""
    print("🧪 Pipeline Components Test")
    print("=" * 50)
    
    # Load environment
    load_dotenv()
    
    # Initialize pipeline manager
    manager = PipecatPipelineManager()
    
    print("\n1. Testing Service Initialization...")
    services = manager.test_services()
    
    for service, result in services.items():
        status = "✅" if result.get('success', False) else "❌"
        print(f"   {service}: {status} - {result.get('message', 'Unknown')}")
    
    print("\n2. Testing Pipeline Creation...")
    pipeline_created = manager.create_pipeline()
    print(f"   Pipeline Created: {'✅' if pipeline_created else '❌'}")
    
    print("\n3. Testing Pipeline Status...")
    status = manager.get_pipeline_status()
    print(f"   Pipeline Created: {'✅' if status['pipeline_created'] else '❌'}")
    print(f"   Audio Initialized: {'✅' if status['audio_initialized'] else '❌'}")
    print(f"   Services Configured: {'✅' if all(status['services'].values()) else '❌'}")
    
    return manager, pipeline_created

async def test_response_detection_integration(manager: PipecatPipelineManager):
    """Test response detection without blocking pipeline."""
    print("\n🧪 Response Detection Integration Test")
    print("=" * 50)
    
    print("\nThis test will:")
    print("1. Test response detection callbacks")
    print("2. Simulate AI responses")
    print("3. Test timeout/escalation logic")
    print("4. Verify user response detection")
    
    # Set up response detector callbacks
    manager.response_detector.set_callbacks(
        on_timeout=lambda msg: print(f"⏰ TIMEOUT: {msg}"),
        on_escalation=lambda msg: print(f"🚨 ESCALATION: {msg}"),
        on_emergency=lambda msg: print(f"🚨 EMERGENCY: {msg}")
    )
    
    print("\n1. Testing Response Detection Initialization...")
    status = manager.response_detector.get_status()
    print(f"   Status: {status['status']}")
    print(f"   Is Monitoring: {status['is_monitoring']}")
    print(f"   Timeout Threshold: {status['timeout_threshold']}s")
    
    print("\n2. Testing Response Monitoring Start...")
    manager.response_detector.start_monitoring()
    status = manager.response_detector.get_status()
    print(f"   Status: {status['status']}")
    print(f"   Is Monitoring: {status['is_monitoring']}")
    
    print("\n3. Testing User Response Detection...")
    print("   Simulating user response...")
    manager.response_detector.user_responded()
    status = manager.response_detector.get_status()
    print(f"   Status: {status['status']}")
    print(f"   Is Monitoring: {status['is_monitoring']}")
    
    print("\n4. Testing Timeout Scenario...")
    print("   Starting monitoring and waiting for timeout...")
    manager.response_detector.start_monitoring()
    
    # Wait for timeout with shorter threshold for testing
    for i in range(3):
        print(f"   Waiting... ({i+1}/3)")
        await asyncio.sleep(1)
    
    status = manager.response_detector.get_status()
    print(f"   Final Status: {status['status']}")
    print(f"   Time Since AI Speech: {status['time_since_ai_speech']:.1f}s")
    
    print("\n✅ Response detection integration test completed!")

async def test_conversation_state(manager: PipecatPipelineManager):
    """Test conversation state management."""
    print("\n🧪 Conversation State Test")
    print("=" * 50)
    
    print("\n1. Testing Conversation State Initialization...")
    summary = manager.conversation_state.get_conversation_summary()
    print(f"   Current Urgency: {summary['current_urgency']}")
    print(f"   Total Turns: {summary['total_turns']}")
    
    print("\n2. Testing User Input Addition...")
    manager.conversation_state.add_user_input("I need help, there's a fire")
    summary = manager.conversation_state.get_conversation_summary()
    print(f"   Updated Urgency: {summary['current_urgency']}")
    print(f"   Total Turns: {summary['total_turns']}")
    
    print("\n3. Testing AI Response Update...")
    manager.conversation_state.update_ai_response("I'm here to help. Are you safe? Can you breathe?")
    summary = manager.conversation_state.get_conversation_summary()
    print(f"   Final Urgency: {summary['current_urgency']}")
    print(f"   Total Turns: {summary['total_turns']}")
    
    print("\n✅ Conversation state test completed!")

async def test_audio_components(manager: PipecatPipelineManager):
    """Test audio components without blocking."""
    print("\n🧪 Audio Components Test")
    print("=" * 50)
    
    print("\n1. Testing Audio Initialization...")
    audio_initialized = manager._test_audio_initialization()
    print(f"   Audio Initialized: {'✅' if audio_initialized else '❌'}")
    
    print("\n2. Testing ElevenLabs TTS...")
    try:
        # Test TTS generation
        test_message = "Hello, this is a test of the crisis response system."
        audio_file = manager.elevenlabs_service.generate_crisis_speech(test_message, "normal")
        
        if audio_file:
            print(f"   TTS Generated: ✅ - {audio_file}")
            # Clean up
            manager.elevenlabs_service.cleanup_audio_file(audio_file)
        else:
            print("   TTS Generated: ❌")
    except Exception as e:
        print(f"   TTS Error: ❌ - {str(e)}")
    
    print("\n3. Testing Whisper Transcription...")
    try:
        # Test transcription service
        whisper_adapter = manager.whisper_client
        test_result = whisper_adapter.test_connection()
        print(f"   Whisper Available: {'✅' if test_result.get('success', False) else '❌'}")
    except Exception as e:
        print(f"   Whisper Error: ❌ - {str(e)}")
    
    print("\n✅ Audio components test completed!")

async def main():
    """Main test function."""
    print("🧪 Simple Pipeline Test Suite")
    print("=" * 60)
    
    # Load environment
    load_dotenv()
    
    # Test 1: Pipeline Components
    manager, pipeline_created = test_pipeline_components()
    
    if not pipeline_created:
        print("\n❌ Pipeline creation failed. Cannot proceed with component tests.")
        return
    
    print("\n" + "=" * 60)
    print("🎯 Running Component Tests...")
    
    # Test 2: Response Detection Integration
    await test_response_detection_integration(manager)
    
    # Test 3: Conversation State
    await test_conversation_state(manager)
    
    # Test 4: Audio Components
    await test_audio_components(manager)
    
    print("\n" + "=" * 60)
    print("✅ All component tests completed!")
    print("\nNext steps:")
    print("1. Test with real microphone input")
    print("2. Test with real speaker output")
    print("3. Test complete end-to-end flow")

if __name__ == "__main__":
    asyncio.run(main()) 