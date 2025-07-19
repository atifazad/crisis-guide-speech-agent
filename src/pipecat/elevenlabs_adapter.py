"""
ElevenLabs adapter for pipecat TTS integration.
Provides text-to-speech functionality for the crisis response pipeline.
"""

import asyncio
import logging
from typing import Optional, Dict, Any
from pipecat.processors.frame_processor import FrameProcessor

from src.services.elevenlabs_service import ElevenLabsService
from src.utils.error_handler import log_error

logger = logging.getLogger(__name__)

class ElevenLabsAdapter(FrameProcessor):
    """ElevenLabs TTS adapter for pipecat pipeline using our existing service."""
    
    def __init__(self, elevenlabs_service: ElevenLabsService):
        """
        Initialize ElevenLabs adapter.
        
        Args:
            elevenlabs_service: Existing ElevenLabs TTS service
        """
        super().__init__()
        self.tts_service = elevenlabs_service
        self.current_urgency = "normal"
        
    async def process_text(self, text: str, urgency_level: str = "normal") -> Optional[str]:
        """
        Process text to speech with urgency-based settings.
        
        Args:
            text: Text to convert to speech
            urgency_level: "normal", "urgent", or "emergency"
            
        Returns:
            Path to generated audio file or None if error
        """
        try:
            self.current_urgency = urgency_level
            audio_file = self.tts_service.generate_crisis_speech(text, urgency_level)
            return audio_file
            
        except Exception as e:
            log_error(f"Error in ElevenLabs adapter: {str(e)}")
            return None
    
    def set_urgency_level(self, urgency: str):
        """
        Set the urgency level for TTS generation.
        
        Args:
            urgency: "normal", "urgent", or "emergency"
        """
        if urgency in ["normal", "urgent", "emergency"]:
            self.current_urgency = urgency
        else:
            log_error(f"Invalid urgency level: {urgency}")
    
    def get_voice_settings(self) -> Dict[str, Any]:
        """
        Get current voice settings.
        
        Returns:
            Dictionary with current voice configuration
        """
        return {
            "urgency_level": self.current_urgency,
            "voice_id": self.tts_service.default_voice_id,
            "service_configured": self.tts_service.is_configured
        }
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test ElevenLabs connection through adapter.
        
        Returns:
            Dictionary with test results
        """
        return self.tts_service.test_connection()
    
    def cleanup_audio(self, file_path: str):
        """
        Clean up audio file.
        
        Args:
            file_path: Path to audio file to delete
        """
        self.tts_service.cleanup_audio_file(file_path) 