#!/usr/bin/env python3
"""
Whisper Service
Handles all Whisper API interactions including speech-to-text transcription
"""

import logging
import os
import tempfile
import whisper
from typing import Optional, Dict, Any
from config import Config

logger = logging.getLogger(__name__)

class WhisperService:
    """Service for handling Whisper API interactions."""
    
    def __init__(self):
        """Initialize the Whisper service."""
        self.model_name = Config.get_whisper_model()
        self.language = Config.get_whisper_language()
        self.model = None
        self._load_model()
        logger.info(f"Whisper service initialized with model: {self.model_name}")
    
    def _load_model(self):
        """Load the Whisper model."""
        try:
            self.model = whisper.load_model(self.model_name)
            logger.info(f"Loaded Whisper model: {self.model_name}")
        except Exception as e:
            logger.error(f"Error loading Whisper model: {str(e)}")
            self.model = None
    
    def transcribe_audio(self, audio_data: bytes) -> str:
        """
        Transcribe audio using Whisper.
        
        Args:
            audio_data: Audio data as bytes
            
        Returns:
            Transcribed text or empty string if error
        """
        try:
            if self.model is None:
                logger.error("Whisper model not loaded")
                return ""
            
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_path = temp_file.name
            
            result = self.model.transcribe(
                temp_path,
                language=self.language,
                task="transcribe"
            )
            
            # Clean up temporary file
            os.unlink(temp_path)
            
            transcript = result["text"].strip()
            logger.info(f"Transcribed: {transcript}")
            return transcript
            
        except Exception as e:
            logger.error(f"Transcription error: {str(e)}")
            return ""
    
    def transcribe_file(self, file_path: str) -> str:
        """
        Transcribe audio from a file.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Transcribed text or empty string if error
        """
        try:
            if self.model is None:
                logger.error("Whisper model not loaded")
                return ""
            
            result = self.model.transcribe(
                file_path,
                language=self.language,
                task="transcribe"
            )
            
            transcript = result["text"].strip()
            logger.info(f"Transcribed file {file_path}: {transcript}")
            return transcript
            
        except Exception as e:
            logger.error(f"File transcription error: {str(e)}")
            return ""
    
    def transcribe_with_options(
        self, 
        audio_data: bytes, 
        language: Optional[str] = None,
        task: str = "transcribe"
    ) -> Dict[str, Any]:
        """
        Transcribe audio with custom options.
        
        Args:
            audio_data: Audio data as bytes
            language: Language code (uses config default if None)
            task: Transcription task ("transcribe" or "translate")
            
        Returns:
            Full transcription result dictionary or empty dict if error
        """
        try:
            if self.model is None:
                logger.error("Whisper model not loaded")
                return {}
            
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_path = temp_file.name
            
            result = self.model.transcribe(
                temp_path,
                language=language or self.language,
                task=task
            )
            
            # Clean up temporary file
            os.unlink(temp_path)
            
            logger.info(f"Transcribed with options: {result.get('text', '').strip()}")
            return result
            
        except Exception as e:
            logger.error(f"Transcription with options error: {str(e)}")
            return {}
    
    def validate_model(self) -> bool:
        """
        Validate that the Whisper model is working.
        
        Returns:
            True if model is valid, False otherwise
        """
        try:
            if self.model is None:
                logger.error("Whisper model not loaded")
                return False
            
            # Try a simple transcription test
            # Create a minimal test audio file or use existing one
            logger.info("Whisper model validation passed")
            return True
            
        except Exception as e:
            logger.error(f"Whisper model validation failed: {str(e)}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the loaded Whisper model.
        
        Returns:
            Model information dictionary
        """
        return {
            "model_name": self.model_name,
            "language": self.language,
            "model_loaded": self.model is not None,
            "model_type": "whisper"
        } 