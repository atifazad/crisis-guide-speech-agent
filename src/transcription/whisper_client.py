"""
Whisper transcription client for the Voice-to-Voice AI Assistant.
"""

import whisper
import streamlit as st
from typing import Optional, Dict, Any
from ..config.constants import WHISPER_SETTINGS, LANGUAGE_OPTIONS
from ..utils.error_handler import ErrorHandler

class WhisperClient:
    """Wrapper for OpenAI Whisper model with caching and improved settings."""
    
    def __init__(self, model_name: str = WHISPER_SETTINGS["DEFAULT_MODEL"]):
        self.model_name = model_name
        self.model = None
        self._load_model()
    
    def _load_model(self) -> None:
        """Load the Whisper model with caching."""
        try:
            with st.spinner(f"Loading Whisper model ({self.model_name})..."):
                self.model = whisper.load_model(self.model_name)
            st.success(f"✅ Whisper model loaded successfully!")
        except Exception as e:
            ErrorHandler.handle_model_error(e)
            self.model = None
    
    def transcribe_audio(
        self,
        audio_file_path: str,
        language: Optional[str] = None,
        task: str = "transcribe",
        fp16: bool = WHISPER_SETTINGS["FP16_ENABLED"],
        verbose: bool = WHISPER_SETTINGS["VERBOSE"]
    ) -> Optional[str]:
        """
        Transcribe audio using Whisper.
        
        Args:
            audio_file_path: Path to audio file
            language: Language code (None for auto-detect)
            task: Transcription task ("transcribe" or "translate")
            fp16: Whether to use FP16 precision
            verbose: Whether to show verbose output
            
        Returns:
            Transcribed text or None if failed
        """
        if self.model is None:
            ErrorHandler.handle_error(
                Exception("Model not loaded"),
                "Whisper model not available"
            )
            return None
        
        try:
            # Use improved transcription parameters
            result = self.model.transcribe(
                audio_file_path,
                language=language,
                task=task,
                fp16=fp16,
                verbose=verbose
            )
            
            return result["text"].strip()
            
        except Exception as e:
            ErrorHandler.handle_audio_error(e, "transcription")
            return None
    
    def get_available_models(self) -> list:
        """Get list of available Whisper models."""
        return WHISPER_SETTINGS["AVAILABLE_MODELS"]
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model."""
        if self.model is None:
            return {
                'name': self.model_name,
                'loaded': False,
                'type': 'None'
            }
        
        return {
            'name': self.model_name,
            'loaded': True,
            'type': type(self.model).__name__,
            'parameters': self._estimate_model_size()
        }
    
    def _estimate_model_size(self) -> str:
        """Estimate model size based on model name."""
        model_sizes = {
            "tiny": "39M",
            "base": "74M", 
            "small": "244M",
            "medium": "769M",
            "large": "1550M"
        }
        return model_sizes.get(self.model_name, "Unknown")
    
    def change_model(self, model_name: str) -> bool:
        """
        Change to a different Whisper model.
        
        Args:
            model_name: Name of the model to load
            
        Returns:
            True if successful, False otherwise
        """
        if model_name not in WHISPER_SETTINGS["AVAILABLE_MODELS"]:
            st.error(f"Invalid model: {model_name}")
            return False
        
        try:
            self.model_name = model_name
            self._load_model()
            return self.model is not None
        except Exception as e:
            ErrorHandler.handle_model_error(e)
            return False
    
    def get_transcription_confidence(
        self,
        audio_file_path: str,
        language: Optional[str] = None
    ) -> Optional[float]:
        """
        Get transcription confidence score.
        
        Args:
            audio_file_path: Path to audio file
            language: Language code
            
        Returns:
            Confidence score (0-1) or None if failed
        """
        if self.model is None:
            return None
        
        try:
            result = self.model.transcribe(
                audio_file_path,
                language=language,
                return_confidence=True
            )
            
            # Calculate average confidence from segments
            if 'segments' in result and result['segments']:
                confidences = [seg.get('avg_logprob', 0) for seg in result['segments']]
                return sum(confidences) / len(confidences)
            
            return None
            
        except Exception as e:
            ErrorHandler.log_error(f"Failed to get confidence: {e}")
            return None

class TranscriptionManager:
    """Manages transcription operations and settings."""
    
    def __init__(self, model_name: str = WHISPER_SETTINGS["DEFAULT_MODEL"]):
        self.whisper_client = WhisperClient(model_name)
        self.language_options = LANGUAGE_OPTIONS
    
    def transcribe_with_settings(
        self,
        audio_file_path: str,
        language_name: str = "Auto-detect",
        task: str = "transcribe"
    ) -> Optional[str]:
        """
        Transcribe audio with specified settings.
        
        Args:
            audio_file_path: Path to audio file
            language_name: Language name from options
            task: Transcription task
            
        Returns:
            Transcribed text or None if failed
        """
        language_code = self.language_options.get(language_name)
        
        return self.whisper_client.transcribe_audio(
            audio_file_path,
            language=language_code,
            task=task
        )
    
    def get_language_options(self) -> Dict[str, Optional[str]]:
        """Get available language options."""
        return self.language_options
    
    def validate_language(self, language_name: str) -> bool:
        """Validate if language is supported."""
        return language_name in self.language_options
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get current model information."""
        return self.whisper_client.get_model_info()
    
    def change_model(self, model_name: str) -> bool:
        """Change the Whisper model."""
        return self.whisper_client.change_model(model_name)
    
    def get_available_models(self) -> list:
        """Get available Whisper models."""
        return self.whisper_client.get_available_models() 