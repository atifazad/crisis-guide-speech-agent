"""
Centralized error handling for the Voice-to-Voice AI Assistant.
"""

import streamlit as st
from typing import Optional, Callable, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ErrorHandler:
    """Centralized error handling for the application."""
    
    @staticmethod
    def handle_error(
        error: Exception,
        error_message: str,
        show_to_user: bool = True,
        log_error: bool = True,
        fallback_value: Any = None
    ) -> Any:
        """
        Handle errors consistently across the application.
        
        Args:
            error: The exception that occurred
            error_message: User-friendly error message
            show_to_user: Whether to show error to user via Streamlit
            log_error: Whether to log the error
            fallback_value: Value to return if error occurs
            
        Returns:
            The fallback value if error occurs, None otherwise
        """
        if log_error:
            logger.error(f"{error_message}: {str(error)}")
        
        if show_to_user:
            st.error(f"❌ {error_message}")
        
        return fallback_value
    
    @staticmethod
    def handle_audio_error(error: Exception, operation: str) -> None:
        """Handle audio-related errors specifically."""
        error_messages = {
            "recording": "Failed to record audio",
            "saving": "Failed to save audio file",
            "preprocessing": "Failed to preprocess audio",
            "transcription": "Failed to transcribe audio"
        }
        
        message = error_messages.get(operation, f"Audio {operation} failed")
        ErrorHandler.handle_error(error, message)
    
    @staticmethod
    def handle_model_error(error: Exception) -> None:
        """Handle Whisper model-related errors."""
        ErrorHandler.handle_error(error, "Failed to load Whisper model")
    
    @staticmethod
    def handle_device_error(error: Exception) -> None:
        """Handle audio device-related errors."""
        ErrorHandler.handle_error(error, "No audio input devices found")
    
    @staticmethod
    def safe_execute(
        func: Callable,
        error_message: str,
        fallback_value: Any = None,
        *args,
        **kwargs
    ) -> Any:
        """
        Safely execute a function with error handling.
        
        Args:
            func: Function to execute
            error_message: Error message if function fails
            fallback_value: Value to return if function fails
            *args: Arguments to pass to function
            **kwargs: Keyword arguments to pass to function
            
        Returns:
            Function result or fallback value
        """
        try:
            return func(*args, **kwargs)
        except Exception as e:
            ErrorHandler.handle_error(e, error_message, fallback_value=fallback_value)
            return fallback_value

def log_info(message: str) -> None:
    """Log informational messages."""
    logger.info(message)

def log_warning(message: str) -> None:
    """Log warning messages."""
    logger.warning(message)

def log_error(message: str) -> None:
    """Log error messages."""
    logger.error(message) 