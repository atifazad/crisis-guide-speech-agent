#!/usr/bin/env python3
"""
Test script for ElevenLabs TTS service.
Run this to verify TTS functionality and voice quality.
"""

import os
import sys
import time
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from services.elevenlabs_service import ElevenLabsService

def test_elevenlabs_service():
    """Test the ElevenLabs TTS service."""
    print("🔊 Testing ElevenLabs TTS Service")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check environment variables
    print("\n0. Checking Environment Variables...")
    elevenlabs_key = os.getenv('ELEVENLABS_API_KEY')
    if elevenlabs_key:
        print(f"   ✅ ELEVENLABS_API_KEY found: {elevenlabs_key[:20]}...")
    else:
        print("   ❌ ELEVENLABS_API_KEY not found")
        return False
    
    # Initialize service
    tts_service = ElevenLabsService()
    
    # Test 1: Connection test
    print("\n1. Testing API Connection...")
    connection_result = tts_service.test_connection()
    print(f"   Status: {'✅ Success' if connection_result['success'] else '❌ Failed'}")
    print(f"   Message: {connection_result.get('message', 'N/A')}")
    
    if not connection_result['success']:
        print(f"   Error details: {connection_result.get('error', 'No error details')}")
        print("   ⚠️  Please check your ELEVENLABS_API_KEY in .env file")
        return False
    
    # Test 2: Basic TTS generation
    print("\n2. Testing Basic TTS Generation...")
    test_text = "Hello, this is a test of the ElevenLabs text-to-speech service for crisis response."
    audio_file = tts_service.generate_speech(test_text)
    
    if audio_file:
        print(f"   ✅ Audio generated: {audio_file}")
        print(f"   📁 File size: {os.path.getsize(audio_file)} bytes")
        
        # Clean up test file
        tts_service.cleanup_audio_file(audio_file)
        print("   🗑️  Test file cleaned up")
    else:
        print("   ❌ Failed to generate audio")
        return False
    
    # Test 3: Crisis-specific TTS with different urgency levels
    print("\n3. Testing Crisis-Specific TTS...")
    
    crisis_texts = [
        ("normal", "I'm here to help. Can you tell me what's happening?"),
        ("urgent", "Can you breathe? Are you safe right now?"),
        ("emergency", "I will wait 5 seconds. If you don't respond, I will call 911.")
    ]
    
    for urgency, text in crisis_texts:
        print(f"   Testing {urgency} urgency: {text[:50]}...")
        audio_file = tts_service.generate_crisis_speech(text, urgency)
        
        if audio_file:
            print(f"      ✅ {urgency} audio generated")
            tts_service.cleanup_audio_file(audio_file)
        else:
            print(f"      ❌ Failed to generate {urgency} audio")
    
    # Test 4: Available voices
    print("\n4. Testing Voice Availability...")
    voices_result = tts_service.get_available_voices()
    
    if voices_result.get('success'):
        print(f"   ✅ Found {voices_result['count']} available voices")
        print("   📋 Sample voices:")
        for voice in voices_result['voices'][:3]:  # Show first 3
            print(f"      - {voice['name']} ({voice['category']})")
    else:
        print(f"   ❌ Failed to get voices: {voices_result.get('error', 'Unknown error')}")
    
    print("\n" + "=" * 50)
    print("✅ ElevenLabs TTS Service Test Complete!")
    print("\nNext steps:")
    print("1. Listen to the generated audio files to verify quality")
    print("2. Adjust voice settings if needed")
    print("3. Proceed to Step 2: Pipecat Audio Pipeline Integration")
    
    return True

if __name__ == "__main__":
    success = test_elevenlabs_service()
    sys.exit(0 if success else 1) 