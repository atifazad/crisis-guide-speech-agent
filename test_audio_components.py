#!/usr/bin/env python3
"""
Simple audio components test.
Tests microphone, speaker, and TTS without blocking pipeline.
"""

import asyncio
import time
import sys
import os
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.pipecat.pipeline_manager import PipecatPipelineManager

def test_audio_components():
    """Test audio components without starting the full pipeline."""
    print("🎤 Audio Components Test")
    print("=" * 50)
    
    # Load environment
    load_dotenv()
    
    # Initialize pipeline manager
    manager = PipecatPipelineManager()
    
    print("\n1. Testing Service Connections...")
    services = manager.test_services()
    
    all_services_ok = True
    for service, result in services.items():
        status = "✅" if result.get('success', False) else "❌"
        print(f"   {service}: {status} - {result.get('message', 'Unknown')}")
        if not result.get('success', False):
            all_services_ok = False
    
    if not all_services_ok:
        print("\n❌ Some services failed.")
        return False
    
    print("\n2. Testing Audio Initialization...")
    audio_initialized = manager._test_audio_initialization()
    print(f"   Audio Initialized: {'✅' if audio_initialized else '❌'}")
    
    print("\n3. Testing ElevenLabs TTS...")
    try:
        # Test TTS generation
        test_message = "Hello, this is a test of the crisis response system. Can you hear me clearly?"
        audio_file = manager.elevenlabs_service.generate_crisis_speech(test_message, "normal")
        
        if audio_file:
            print(f"   TTS Generated: ✅ - {audio_file}")
            print("   Playing audio through speakers...")
            
            # Play the audio
            try:
                import subprocess
                subprocess.run(["afplay", audio_file], check=True)
                print("   ✅ Audio played successfully!")
            except Exception as e:
                print(f"   ⚠️  Audio play failed: {str(e)}")
            
            # Clean up
            manager.elevenlabs_service.cleanup_audio_file(audio_file)
        else:
            print("   TTS Generated: ❌")
    except Exception as e:
        print(f"   TTS Error: ❌ - {str(e)}")
    
    print("\n4. Testing Whisper Transcription...")
    try:
        # Test transcription service
        whisper_result = manager.whisper_client.test_connection()
        print(f"   Whisper Available: {'✅' if whisper_result.get('success', False) else '❌'}")
        if whisper_result.get('success', False):
            print(f"   Model: {whisper_result.get('model_info', {}).get('name', 'Unknown')}")
    except Exception as e:
        print(f"   Whisper Error: ❌ - {str(e)}")
    
    print("\n5. Testing Pipeline Creation (without starting)...")
    pipeline_created = manager.create_pipeline()
    print(f"   Pipeline Created: {'✅' if pipeline_created else '❌'}")
    
    print("\n✅ Audio components test completed!")
    return True

def test_crisis_tts():
    """Test crisis-specific TTS messages."""
    print("\n🚨 Crisis TTS Test")
    print("=" * 50)
    
    # Load environment
    load_dotenv()
    
    # Initialize services
    from src.services.elevenlabs_service import ElevenLabsService
    elevenlabs_service = ElevenLabsService()
    
    # Test different crisis scenarios
    crisis_messages = [
        ("normal", "Hello, I'm here to help. What's your emergency?"),
        ("urgent", "I understand this is urgent. Can you tell me what's happening?"),
        ("emergency", "EMERGENCY: I'm calling 911 now. Please stay on the line.")
    ]
    
    for urgency, message in crisis_messages:
        print(f"\nTesting {urgency} urgency message...")
        try:
            audio_file = elevenlabs_service.generate_crisis_speech(message, urgency)
            
            if audio_file:
                print(f"   Generated: ✅ - {audio_file}")
                print(f"   Message: {message}")
                
                # Play the audio
                try:
                    import subprocess
                    subprocess.run(["afplay", audio_file], check=True)
                    print("   ✅ Played successfully!")
                except Exception as e:
                    print(f"   ⚠️  Play failed: {str(e)}")
                
                # Clean up
                elevenlabs_service.cleanup_audio_file(audio_file)
                
                # Wait between messages
                time.sleep(2)
            else:
                print("   Generated: ❌")
        except Exception as e:
            print(f"   Error: ❌ - {str(e)}")
    
    print("\n✅ Crisis TTS test completed!")

def main():
    """Main test function."""
    print("🎤 Audio Components Test Suite")
    print("=" * 60)
    
    # Test 1: Audio Components
    success1 = test_audio_components()
    
    if success1:
        print("\n" + "=" * 60)
        print("🎯 Testing Crisis TTS Messages...")
        
        # Test 2: Crisis TTS
        test_crisis_tts()
    
    print("\n" + "=" * 60)
    print("✅ All audio component tests completed!")
    print("\nNext steps:")
    print("1. Test with real microphone input")
    print("2. Test complete pipeline integration")
    print("3. Test emergency service integration")

if __name__ == "__main__":
    main() 