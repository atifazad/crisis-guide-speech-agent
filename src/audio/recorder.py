"""
Audio recording functionality for the Voice-to-Voice AI Assistant.
"""

import sounddevice as sd
import numpy as np
import streamlit as st
from typing import Optional, List, Dict, Any
from ..config.constants import AUDIO_SETTINGS
from ..utils.error_handler import ErrorHandler

class AudioRecorder:
    """Handles audio recording and device management."""
    
    def __init__(self):
        self.devices = self._get_audio_devices()
    
    def _get_audio_devices(self) -> Dict[str, Any]:
        """Get available audio devices."""
        try:
            devices = sd.query_devices()
            return {
                'all': devices,
                'input': [d for d in devices if d.get('max_input_channels', 0) > 0],
                'output': [d for d in devices if d.get('max_output_channels', 0) > 0]
            }
        except Exception as e:
            ErrorHandler.handle_device_error(e)
            return {'all': [], 'input': [], 'output': []}
    
    def get_input_devices(self) -> List[Dict[str, Any]]:
        """Get list of available input devices."""
        return self.devices.get('input', [])
    
    def get_default_input_device(self) -> Optional[Dict[str, Any]]:
        """Get the default input device."""
        try:
            default_device = sd.query_devices(kind='input')
            return default_device
        except Exception as e:
            ErrorHandler.log_error(f"Failed to get default input device: {e}")
            return None
    
    def record_audio(
        self,
        duration: int = AUDIO_SETTINGS["DEFAULT_RECORDING_DURATION"],
        sample_rate: int = AUDIO_SETTINGS["DEFAULT_SAMPLE_RATE"],
        channels: int = AUDIO_SETTINGS["AUDIO_CHANNELS"],
        dtype: str = AUDIO_SETTINGS["AUDIO_DTYPE"]
    ) -> Optional[np.ndarray]:
        """
        Record audio for specified duration.
        
        Args:
            duration: Recording duration in seconds
            sample_rate: Sample rate in Hz
            channels: Number of audio channels
            dtype: Data type for audio recording
            
        Returns:
            Recorded audio data as numpy array or None if failed
        """
        try:
            st.info(f"Recording for {duration} seconds... Speak now!")
            
            # Record audio with specified parameters
            recording = sd.rec(
                int(duration * sample_rate),
                samplerate=sample_rate,
                channels=channels,
                dtype=getattr(np, dtype)
            )
            sd.wait()
            
            # Normalize and flatten audio
            recording = recording.flatten()
            if np.max(np.abs(recording)) > 0:
                recording = recording / np.max(np.abs(recording))
            
            return recording
            
        except Exception as e:
            ErrorHandler.handle_audio_error(e, "recording")
            return None
    
    def test_recording(self, duration: int = 2) -> bool:
        """
        Test if audio recording works.
        
        Args:
            duration: Test recording duration in seconds
            
        Returns:
            True if recording works, False otherwise
        """
        try:
            test_audio = self.record_audio(duration=duration)
            return test_audio is not None and len(test_audio) > 0
        except Exception as e:
            ErrorHandler.log_error(f"Recording test failed: {e}")
            return False
    
    def get_device_info(self) -> Dict[str, Any]:
        """Get information about available audio devices."""
        input_devices = self.get_input_devices()
        default_device = self.get_default_input_device()
        
        return {
            'total_input_devices': len(input_devices),
            'input_devices': input_devices,
            'default_device': default_device,
            'has_devices': len(input_devices) > 0
        }
    
    def validate_recording_settings(
        self,
        duration: int,
        sample_rate: int
    ) -> bool:
        """
        Validate recording settings.
        
        Args:
            duration: Recording duration
            sample_rate: Sample rate
            
        Returns:
            True if settings are valid, False otherwise
        """
        # Check duration
        if duration < AUDIO_SETTINGS["MIN_RECORDING_DURATION"]:
            st.error(f"Recording duration must be at least {AUDIO_SETTINGS['MIN_RECORDING_DURATION']} seconds")
            return False
        
        if duration > AUDIO_SETTINGS["MAX_RECORDING_DURATION"]:
            st.error(f"Recording duration must be at most {AUDIO_SETTINGS['MAX_RECORDING_DURATION']} seconds")
            return False
        
        # Check sample rate
        if sample_rate not in AUDIO_SETTINGS["SUPPORTED_SAMPLE_RATES"]:
            st.error(f"Sample rate must be one of {AUDIO_SETTINGS['SUPPORTED_SAMPLE_RATES']}")
            return False
        
        # Check if devices are available
        if not self.get_device_info()['has_devices']:
            st.error("No audio input devices found")
            return False
        
        return True

class AudioDeviceManager:
    """Manages audio device selection and configuration."""
    
    @staticmethod
    def list_devices() -> List[Dict[str, Any]]:
        """List all available audio devices."""
        try:
            devices = sd.query_devices()
            return devices
        except Exception as e:
            ErrorHandler.handle_device_error(e)
            return []
    
    @staticmethod
    def get_device_by_name(name: str) -> Optional[Dict[str, Any]]:
        """Get device information by name."""
        try:
            devices = sd.query_devices()
            for device in devices:
                if device['name'] == name:
                    return device
            return None
        except Exception as e:
            ErrorHandler.log_error(f"Failed to get device by name {name}: {e}")
            return None
    
    @staticmethod
    def set_default_device(device_name: str) -> bool:
        """Set default audio device."""
        try:
            sd.default.device = device_name
            return True
        except Exception as e:
            ErrorHandler.log_error(f"Failed to set default device {device_name}: {e}")
            return False 