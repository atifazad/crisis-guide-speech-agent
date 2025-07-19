"""
ElevenLabs TTS service for crisis response voice output.
Handles text-to-speech conversion with configurable voice settings.
"""

import os
import tempfile
from typing import Optional, Dict, Any
from elevenlabs.client import ElevenLabs
from elevenlabs import save, voices, VoiceSettings
from src.utils.error_handler import log_error

class ElevenLabsService:
    """ElevenLabs TTS service for crisis response voice output."""
    
    def __init__(self):
        """Initialize the ElevenLabs service."""
        self.api_key = self._get_api_key()
        self.is_configured = bool(self.api_key)
        
        if self.is_configured:
            self.client = ElevenLabs(api_key=self.api_key)
            self._configure_default_voice()
        else:
            self.client = None
            self.default_voice_id = None
            self.voice_settings = None
    
    def _get_api_key(self) -> Optional[str]:
        """Get ElevenLabs API key from environment."""
        return os.getenv('ELEVENLABS_API_KEY')
    
    def _configure_default_voice(self):
        """Configure default voice settings for crisis response."""
        # Use a professional, calm voice suitable for crisis situations
        self.default_voice_id = "pNInz6obpgDQGcFmaJgB"  # Adam voice (professional)
        
        # Configure voice settings for crisis response
        self.voice_settings = VoiceSettings(
            stability=0.7,        # Balanced stability
            similarity_boost=0.75, # Good voice clarity
            style=0.0,            # Neutral style
            use_speaker_boost=True # Enhanced clarity
        )
    
    def generate_speech(self, text: str, voice_id: Optional[str] = None, 
                       voice_settings: Optional[VoiceSettings] = None) -> Optional[str]:
        """
        Generate speech from text using ElevenLabs TTS.
        
        Args:
            text: Text to convert to speech
            voice_id: Optional voice ID (uses default if None)
            voice_settings: Optional voice settings (uses default if None)
            
        Returns:
            Path to generated audio file or None if error
        """
        if not self.is_configured:
            log_error("ElevenLabs API not configured")
            return None
        
        try:
            # Use default settings if not provided
            voice_id = voice_id or self.default_voice_id
            voice_settings = voice_settings or self.voice_settings
            
            # Generate audio using the client API
            audio = self.client.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id="eleven_monolingual_v1",
                voice_settings=voice_settings
            )
            
            # Save to temporary file
            temp_file = tempfile.NamedTemporaryFile(
                suffix=".mp3", 
                delete=False,
                prefix="crisis_response_"
            )
            save(audio, temp_file.name)
            
            return temp_file.name
            
        except Exception as e:
            log_error(f"Error generating speech: {str(e)}")
            return None
    
    def generate_crisis_speech(self, text: str, urgency_level: str = "normal") -> Optional[str]:
        """
        Generate speech optimized for crisis response scenarios.
        
        Args:
            text: Text to convert to speech
            urgency_level: "normal", "urgent", or "emergency"
            
        Returns:
            Path to generated audio file or None if error
        """
        if not self.is_configured:
            return None
        
        try:
            # Adjust voice settings based on urgency
            settings = self._get_urgency_settings(urgency_level)
            
            return self.generate_speech(text, voice_settings=settings)
            
        except Exception as e:
            log_error(f"Error generating crisis speech: {str(e)}")
            return None
    
    def _get_urgency_settings(self, urgency_level: str) -> VoiceSettings:
        """
        Get voice settings optimized for different urgency levels.
        
        Args:
            urgency_level: "normal", "urgent", or "emergency"
            
        Returns:
            VoiceSettings optimized for the urgency level
        """
        base_settings = VoiceSettings(
            stability=0.7,
            similarity_boost=0.75,
            style=0.0,
            use_speaker_boost=True
        )
        
        if urgency_level == "urgent":
            return VoiceSettings(
                stability=0.6,        # Slightly less stable for urgency
                similarity_boost=0.8,  # Higher clarity
                style=0.2,            # Slight urgency in tone
                use_speaker_boost=True
            )
        elif urgency_level == "emergency":
            return VoiceSettings(
                stability=0.5,        # Less stable for high urgency
                similarity_boost=0.85, # Maximum clarity
                style=0.4,            # Clear urgency in tone
                use_speaker_boost=True
            )
        else:
            return base_settings
    
    def get_available_voices(self) -> Dict[str, Any]:
        """
        Get list of available voices.
        
        Returns:
            Dictionary with voice information
        """
        if not self.is_configured:
            return {"error": "ElevenLabs API not configured"}
        
        try:
            available_voices = self.client.voices.get_all()
            
            voice_list = []
            for voice in available_voices:
                # Handle different response formats from ElevenLabs API
                try:
                    if hasattr(voice, 'voice_id'):
                        voice_id = voice.voice_id
                    elif hasattr(voice, 'id'):
                        voice_id = voice.id
                    else:
                        voice_id = str(voice)  # Fallback
                    
                    voice_info = {
                        "id": voice_id,
                        "name": getattr(voice, 'name', 'Unknown'),
                        "category": getattr(voice, 'category', 'Unknown'),
                        "description": ""
                    }
                    
                    # Try to get description from labels if available
                    if hasattr(voice, 'labels') and voice.labels:
                        voice_info["description"] = voice.labels.get("description", "")
                    
                    voice_list.append(voice_info)
                    
                except Exception as voice_error:
                    # Skip problematic voice entries
                    continue
            
            return {
                "success": True,
                "voices": voice_list,
                "count": len(voice_list)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test the ElevenLabs API connection.
        
        Returns:
            Dictionary with test results
        """
        if not self.is_configured:
            return {
                "success": False,
                "error": "ElevenLabs API not configured",
                "message": "Add ELEVENLABS_API_KEY to .env file"
            }
        
        try:
            # Test with a simple text-to-speech conversion
            test_text = "ElevenLabs TTS connection test successful."
            audio_file = self.generate_speech(test_text)
            
            if audio_file and os.path.exists(audio_file):
                # Clean up test file
                os.unlink(audio_file)
                return {
                    "success": True,
                    "message": "ElevenLabs TTS connection successful",
                    "api": "ElevenLabs TTS"
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to generate test audio",
                    "message": "TTS generation failed"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "ElevenLabs API connection failed"
            }
    
    def cleanup_audio_file(self, file_path: str):
        """
        Clean up temporary audio file.
        
        Args:
            file_path: Path to the audio file to delete
        """
        try:
            if file_path and os.path.exists(file_path):
                os.unlink(file_path)
        except Exception as e:
            log_error(f"Error cleaning up audio file: {str(e)}") 