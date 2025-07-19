#!/usr/bin/env python3
"""
Test script to debug audio transport initialization.
"""

import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_audio_initialization():
    """Test audio transport initialization."""
    print("🔊 Audio Transport Debug Test")
    print("=" * 40)
    
    try:
        # Test 1: Import PyAudio
        print("1. Testing PyAudio Import...")
        import pyaudio
        print("   ✅ PyAudio imported successfully")
        print(f"   Version: {pyaudio.__version__}")
        
        # Test 2: Create PyAudio instance
        print("\n2. Testing PyAudio Instance...")
        py_audio = pyaudio.PyAudio()
        print("   ✅ PyAudio instance created successfully")
        
        # Test 3: Check audio devices
        print("\n3. Testing Audio Devices...")
        input_devices = []
        output_devices = []
        
        for i in range(py_audio.get_device_count()):
            device_info = py_audio.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                input_devices.append(f"{i}: {device_info['name']}")
            if device_info['maxOutputChannels'] > 0:
                output_devices.append(f"{i}: {device_info['name']}")
        
        print(f"   Input devices: {len(input_devices)}")
        for device in input_devices[:3]:  # Show first 3
            print(f"      {device}")
        
        print(f"   Output devices: {len(output_devices)}")
        for device in output_devices[:3]:  # Show first 3
            print(f"      {device}")
        
        # Test 4: Import pipecat audio components
        print("\n4. Testing Pipecat Audio Components...")
        from pipecat.transports.local.audio import (
            LocalAudioInputTransport, 
            LocalAudioOutputTransport, 
            LocalAudioTransportParams
        )
        print("   ✅ Pipecat audio components imported successfully")
        
        # Test 5: Create audio transport parameters
        print("\n5. Testing Audio Transport Parameters...")
        audio_params = LocalAudioTransportParams(
            audio_in_enabled=True,
            audio_out_enabled=True,
            audio_in_sample_rate=16000,
            audio_out_sample_rate=16000,
            audio_in_channels=1,
            audio_out_channels=1
        )
        print("   ✅ Audio transport parameters created successfully")
        
        # Test 6: Create audio transports
        print("\n6. Testing Audio Transport Creation...")
        input_transport = LocalAudioInputTransport(
            py_audio=py_audio,
            params=audio_params
        )
        print("   ✅ Audio input transport created successfully")
        
        output_transport = LocalAudioOutputTransport(
            py_audio=py_audio,
            params=audio_params
        )
        print("   ✅ Audio output transport created successfully")
        
        # Test 7: Check if they're FrameProcessors
        from pipecat.processors.frame_processor import FrameProcessor
        input_is_processor = isinstance(input_transport, FrameProcessor)
        output_is_processor = isinstance(output_transport, FrameProcessor)
        
        print(f"   Input transport is FrameProcessor: {'✅ Yes' if input_is_processor else '❌ No'}")
        print(f"   Output transport is FrameProcessor: {'✅ Yes' if output_is_processor else '❌ No'}")
        
        # Clean up
        py_audio.terminate()
        print("\n   ✅ PyAudio cleaned up successfully")
        
        print("\n✅ Audio transport test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing audio transport: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_pipeline_with_audio():
    """Test pipeline creation with audio transport."""
    print("\n🔊 Pipeline with Audio Test")
    print("=" * 30)
    
    # Load environment variables
    load_dotenv()
    
    try:
        from pipecat.pipeline.pipeline import Pipeline
        from pipecat.processors.aggregators.sentence import SentenceAggregator
        from pipecat.processors.aggregators.llm_response import LLMFullResponseAggregator
        from pipecat.services.openai.llm import OpenAILLMService
        from pipecat.transports.local.audio import (
            LocalAudioInputTransport, 
            LocalAudioOutputTransport, 
            LocalAudioTransportParams
        )
        
        # Check API key
        openai_key = os.getenv('OPENAI_API_KEY')
        if not openai_key:
            print("   ❌ OPENAI_API_KEY not found")
            return False
        
        print("   ✅ OpenAI API key found")
        
        # Initialize PyAudio
        import pyaudio
        py_audio = pyaudio.PyAudio()
        
        # Create audio parameters
        audio_params = LocalAudioTransportParams(
            audio_in_enabled=True,
            audio_out_enabled=True,
            audio_in_sample_rate=16000,
            audio_out_sample_rate=16000,
            audio_in_channels=1,
            audio_out_channels=1
        )
        
        # Create pipeline with audio
        pipeline = Pipeline([
            LocalAudioInputTransport(py_audio=py_audio, params=audio_params),
            SentenceAggregator(),
            OpenAILLMService(
                api_key=openai_key,
                model="gpt-4o",
                system_prompt="You are a helpful assistant."
            ),
            LLMFullResponseAggregator(),
            LocalAudioOutputTransport(py_audio=py_audio, params=audio_params)
        ])
        
        print("   ✅ Pipeline with audio transport created successfully")
        
        # Clean up
        py_audio.terminate()
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing pipeline with audio: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function."""
    print("🔊 Audio Transport Investigation")
    print("=" * 50)
    
    # Test audio initialization
    success1 = test_audio_initialization()
    
    # Test pipeline with audio
    success2 = test_pipeline_with_audio()
    
    print("\n" + "=" * 50)
    if success1 and success2:
        print("✅ All audio transport tests passed!")
        print("\nAudio transport is ready for integration!")
    else:
        print("❌ Some audio transport tests failed")
        print("\nRecommendation: Check audio device permissions")

if __name__ == "__main__":
    main() 