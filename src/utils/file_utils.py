"""
File utilities for the Voice-to-Voice AI Assistant.
"""

import tempfile
import os
from typing import Optional
from scipy.io import wavfile
import numpy as np
from ..config.constants import FILE_SETTINGS
from .error_handler import ErrorHandler

class AudioFileManager:
    """Manages temporary audio files and file operations."""
    
    @staticmethod
    def save_audio_to_temp(
        audio_data: np.ndarray,
        sample_rate: int = 16000
    ) -> Optional[str]:
        """
        Save audio data to a temporary WAV file.
        
        Args:
            audio_data: Audio data as numpy array
            sample_rate: Sample rate of the audio
            
        Returns:
            Path to the temporary file or None if failed
        """
        try:
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=FILE_SETTINGS["TEMP_AUDIO_SUFFIX"]
            ) as tmp_file:
                wavfile.write(tmp_file.name, sample_rate, audio_data.astype(np.float32))
                return tmp_file.name
        except Exception as e:
            ErrorHandler.handle_audio_error(e, "saving")
            return None
    
    @staticmethod
    def cleanup_temp_file(file_path: str) -> bool:
        """
        Clean up a temporary file.
        
        Args:
            file_path: Path to the file to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
                return True
        except Exception as e:
            ErrorHandler.log_error(f"Failed to cleanup temp file {file_path}: {e}")
            return False
        return False
    
    @staticmethod
    def ensure_directory_exists(directory: str) -> bool:
        """
        Ensure a directory exists, create it if it doesn't.
        
        Args:
            directory: Directory path to ensure exists
            
        Returns:
            True if successful, False otherwise
        """
        try:
            os.makedirs(directory, exist_ok=True)
            return True
        except Exception as e:
            ErrorHandler.log_error(f"Failed to create directory {directory}: {e}")
            return False
    
    @staticmethod
    def get_file_size(file_path: str) -> Optional[int]:
        """
        Get the size of a file in bytes.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File size in bytes or None if failed
        """
        try:
            return os.path.getsize(file_path)
        except Exception as e:
            ErrorHandler.log_error(f"Failed to get file size for {file_path}: {e}")
            return None
    
    @staticmethod
    def is_valid_audio_file(file_path: str) -> bool:
        """
        Check if a file is a valid audio file.
        
        Args:
            file_path: Path to the file to check
            
        Returns:
            True if valid audio file, False otherwise
        """
        try:
            if not os.path.exists(file_path):
                return False
            
            # Check file extension
            if not file_path.lower().endswith('.wav'):
                return False
            
            # Check file size (should be > 0)
            file_size = AudioFileManager.get_file_size(file_path)
            if file_size is None or file_size == 0:
                return False
            
            return True
        except Exception:
            return False

class TempFileContext:
    """Context manager for temporary files."""
    
    def __init__(self, suffix: str = ".wav"):
        self.suffix = suffix
        self.file_path = None
    
    def __enter__(self):
        """Create temporary file."""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=self.suffix)
        self.file_path = temp_file.name
        temp_file.close()
        return self.file_path
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up temporary file."""
        if self.file_path and os.path.exists(self.file_path):
            AudioFileManager.cleanup_temp_file(self.file_path) 