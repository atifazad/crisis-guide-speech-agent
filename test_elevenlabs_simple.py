#!/usr/bin/env python3
"""
Simple test for ElevenLabs TTS - generates and plays audio.
"""

import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from services.elevenlabs_service import ElevenLabsService

def test_simple_tts():
    """Simple test to generate and optionally play audio."""
    print("🔊 Simple ElevenLabs TTS Test")
    print("=" * 40)
    
    # Load environment
    load_dotenv()
    
    # Initialize service
    tts = ElevenLabsService()
    
    # Test text
    test_text = "Hello, this is a test of the crisis response TTS system."
    
    print(f"Generating speech for: '{test_text}'")
    
    # Generate audio
    audio_file = tts.generate_speech(test_text)
    
    if audio_file:
        print(f"✅ Audio generated: {audio_file}")
        print(f"📁 File size: {os.path.getsize(audio_file)} bytes")
        
        # Option to play audio (if you have afplay on macOS)
        try:
            import subprocess
            print("🔊 Playing audio...")
            subprocess.run(["afplay", audio_file], check=True)
            print("✅ Audio played successfully")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("ℹ️  Audio file saved but couldn't play automatically")
            print(f"   You can play it manually: open {audio_file}")
        
        # Clean up
        tts.cleanup_audio_file(audio_file)
        print("🗑️  Audio file cleaned up")
        
    else:
        print("❌ Failed to generate audio")

if __name__ == "__main__":
    test_simple_tts() 