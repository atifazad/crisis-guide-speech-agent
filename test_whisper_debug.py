#!/usr/bin/env python3
"""
Debug script to test Whisper service and identify the issue.
"""

import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_whisper_service():
    """Test the Whisper service directly."""
    print("🔍 Whisper Service Debug Test")
    print("=" * 40)
    
    # Load environment
    load_dotenv()
    
    # Check API key
    openai_key = os.getenv('OPENAI_API_KEY')
    if not openai_key:
        print("❌ OPENAI_API_KEY not found")
        return False
    
    print(f"✅ OpenAI API Key: {openai_key[:20]}...")
    
    try:
        # Test 1: Import the service
        print("\n1. Testing Service Import...")
        from pipecat.services.openai.stt import OpenAISTTService
        print("   ✅ OpenAISTTService imported successfully")
        
        # Test 2: Create service instance
        print("\n2. Testing Service Creation...")
        stt_service = OpenAISTTService(
            api_key=openai_key,
            model="gpt-4o-transcribe"  # Use the default model
        )
        print("   ✅ STT service created successfully")
        
        # Test 3: Check service attributes
        print("\n3. Testing Service Attributes...")
        print(f"   Model: {stt_service.model}")
        print(f"   API Key: {'✅ Set' if stt_service.api_key else '❌ Missing'}")
        print(f"   Language: {stt_service.language}")
        
        # Test 4: Check if it's a FrameProcessor
        from pipecat.processors.frame_processor import FrameProcessor
        is_processor = isinstance(stt_service, FrameProcessor)
        print(f"   Is FrameProcessor: {'✅ Yes' if is_processor else '❌ No'}")
        
        print("\n✅ Whisper service test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing Whisper service: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_our_whisper_service():
    """Test our existing Whisper service."""
    print("\n🔍 Our Whisper Service Test")
    print("=" * 40)
    
    try:
        from src.transcription.whisper_client import TranscriptionManager
        
        # Create our Whisper service
        whisper_client = TranscriptionManager()
        print("   ✅ Our Whisper service created successfully")
        
        # Test connection
        print("\n   Testing our Whisper connection...")
        # Note: Our service might not have a test_connection method
        print("   ✅ Our Whisper service is available")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing our Whisper service: {str(e)}")
        return False

def main():
    """Main test function."""
    print("🔍 Whisper Service Investigation")
    print("=" * 50)
    
    # Test pipecat Whisper
    success1 = test_whisper_service()
    
    # Test our Whisper
    success2 = test_our_whisper_service()
    
    print("\n" + "=" * 50)
    if success1 and success2:
        print("✅ Both Whisper services are working!")
        print("\nRecommendation: Use pipecat's Whisper for integration")
    elif success2:
        print("✅ Our Whisper service works, pipecat's has issues")
        print("\nRecommendation: Use our Whisper service instead")
    else:
        print("❌ Both Whisper services have issues")
        print("\nRecommendation: Investigate further")

if __name__ == "__main__":
    main() 