#!/usr/bin/env python3
"""
Test script to verify the voice-to-voice AI assistant setup.
This script checks if all required dependencies are properly installed.
"""

import sys
import importlib

def test_imports():
    """Test if all required packages can be imported"""
    required_packages = [
        'streamlit',
        'sounddevice',
        'numpy',
        'whisper',
        'scipy',
        'tempfile',
        'os'
    ]
    
    print("🔍 Testing package imports...")
    
    failed_imports = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError as e:
            print(f"❌ {package}: {e}")
            failed_imports.append(package)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        print("Please install missing packages using: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All packages imported successfully!")
        return True

def test_whisper_model():
    """Test if Whisper model can be loaded"""
    try:
        import whisper
        print("\n🔍 Testing Whisper model loading...")
        
        # Load the base model (smaller and faster for testing)
        model = whisper.load_model("base")
        print(f"✅ Whisper model loaded successfully: {type(model).__name__}")
        return True
    except Exception as e:
        print(f"❌ Failed to load Whisper model: {e}")
        return False

def test_audio_devices():
    """Test if audio devices are available"""
    try:
        import sounddevice as sd
        print("\n🔍 Testing audio devices...")
        
        devices = sd.query_devices()
        input_devices = [d for d in devices if d.get('max_input_channels', 0) > 0]
        
        if input_devices:
            print(f"✅ Found {len(input_devices)} input device(s):")
            for i, device in enumerate(input_devices[:3]):  # Show first 3
                print(f"   {i+1}. {device['name']}")
            if len(input_devices) > 3:
                print(f"   ... and {len(input_devices) - 3} more")
            return True
        else:
            print("❌ No input devices found")
            return False
    except Exception as e:
        print(f"❌ Failed to query audio devices: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Voice-to-Voice AI Assistant - Setup Test")
    print("=" * 50)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test Whisper model
    whisper_ok = test_whisper_model()
    
    # Test audio devices
    audio_ok = test_audio_devices()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"   Package Imports: {'✅ PASS' if imports_ok else '❌ FAIL'}")
    print(f"   Whisper Model: {'✅ PASS' if whisper_ok else '❌ FAIL'}")
    print(f"   Audio Devices: {'✅ PASS' if audio_ok else '❌ FAIL'}")
    
    if all([imports_ok, whisper_ok, audio_ok]):
        print("\n🎉 All tests passed! Your setup is ready.")
        print("\nTo start the application, run:")
        print("   streamlit run app.py")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        print("\nCommon solutions:")
        print("1. Install missing packages: pip install -r requirements.txt")
        print("2. Check microphone permissions")
        print("3. Ensure internet connection for Whisper model download")

if __name__ == "__main__":
    main() 