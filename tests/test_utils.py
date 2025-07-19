"""
Unit tests for the utils module.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import tempfile
import os
import numpy as np

# Import the modules to test
from src.utils.error_handler import ErrorHandler
from src.utils.file_utils import AudioFileManager, TempFileContext


class TestErrorHandler(unittest.TestCase):
    """Test cases for ErrorHandler class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.error = Exception("Test error")
    
    @patch('src.utils.error_handler.st')
    def test_handle_error_basic(self, mock_st):
        """Test basic error handling."""
        result = ErrorHandler.handle_error(
            self.error,
            "Test error message",
            show_to_user=True,
            log_error=True,
            fallback_value="fallback"
        )
        
        self.assertEqual(result, "fallback")
        mock_st.error.assert_called_once_with("❌ Test error message")
    
    @patch('src.utils.error_handler.st')
    def test_handle_error_no_user_display(self, mock_st):
        """Test error handling without user display."""
        result = ErrorHandler.handle_error(
            self.error,
            "Test error message",
            show_to_user=False,
            log_error=False,
            fallback_value="fallback"
        )
        
        self.assertEqual(result, "fallback")
        mock_st.error.assert_not_called()
    
    @patch('src.utils.error_handler.st')
    def test_handle_audio_error(self, mock_st):
        """Test audio-specific error handling."""
        ErrorHandler.handle_audio_error(self.error, "recording")
        
        mock_st.error.assert_called_once_with("❌ Failed to record audio")
    
    def test_handle_audio_error_unknown_operation(self):
        """Test audio error handling with unknown operation."""
        with patch('src.utils.error_handler.st') as mock_st:
            ErrorHandler.handle_audio_error(self.error, "unknown_operation")
            
            mock_st.error.assert_called_once_with("❌ Audio unknown_operation failed")
    
    @patch('src.utils.error_handler.st')
    def test_handle_model_error(self, mock_st):
        """Test model-specific error handling."""
        ErrorHandler.handle_model_error(self.error)
        
        mock_st.error.assert_called_once_with("❌ Failed to load Whisper model")
    
    @patch('src.utils.error_handler.st')
    def test_handle_device_error(self, mock_st):
        """Test device-specific error handling."""
        ErrorHandler.handle_device_error(self.error)
        
        mock_st.error.assert_called_once_with("❌ No audio input devices found")
    
    @patch('src.utils.error_handler.ErrorHandler.handle_error')
    def test_safe_execute_success(self, mock_handle_error):
        """Test safe execution with success."""
        def test_func(x, y):
            return x + y
        
        result = ErrorHandler.safe_execute(
            test_func,
            "Test error message",
            fallback_value=0,
            x=2,
            y=3
        )
        
        self.assertEqual(result, 5)
        mock_handle_error.assert_not_called()
    
    @patch('src.utils.error_handler.ErrorHandler.handle_error')
    def test_safe_execute_failure(self, mock_handle_error):
        """Test safe execution with failure."""
        def test_func():
            raise Exception("Test exception")
        
        result = ErrorHandler.safe_execute(
            test_func,
            "Test error message",
            fallback_value="fallback"
        )
        
        self.assertEqual(result, "fallback")
        mock_handle_error.assert_called_once()


class TestAudioFileManager(unittest.TestCase):
    """Test cases for AudioFileManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.audio_data = np.random.rand(16000).astype(np.float32)
        self.sample_rate = 16000
    
    @patch('src.utils.file_utils.wavfile')
    def test_save_audio_to_temp_success(self, mock_wavfile):
        """Test successful audio file saving."""
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            mock_wavfile.write.return_value = None
            
            result = AudioFileManager.save_audio_to_temp(
                self.audio_data,
                self.sample_rate
            )
            
            self.assertIsNotNone(result)
            self.assertTrue(result.endswith('.wav'))
    
    @patch('src.utils.file_utils.wavfile')
    def test_save_audio_to_temp_failure(self, mock_wavfile):
        """Test audio file saving failure."""
        mock_wavfile.write.side_effect = Exception("Write error")
        
        result = AudioFileManager.save_audio_to_temp(
            self.audio_data,
            self.sample_rate
        )
        
        self.assertIsNone(result)
    
    def test_cleanup_temp_file_exists(self):
        """Test cleanup of existing temporary file."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            file_path = tmp_file.name
        
        result = AudioFileManager.cleanup_temp_file(file_path)
        
        self.assertTrue(result)
        self.assertFalse(os.path.exists(file_path))
    
    def test_cleanup_temp_file_not_exists(self):
        """Test cleanup of non-existent file."""
        result = AudioFileManager.cleanup_temp_file("non_existent_file.txt")
        
        self.assertTrue(result)
    
    def test_cleanup_temp_file_error(self):
        """Test cleanup with permission error."""
        # Create a file that can't be deleted (simulate permission error)
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            file_path = tmp_file.name
        
        # Try to delete a directory as if it were a file (will cause OSError)
        result = AudioFileManager.cleanup_temp_file("/tmp")
        
        self.assertFalse(result)
        
        # Clean up manually
        os.unlink(file_path)
    
    def test_ensure_directory_exists_new(self):
        """Test creating new directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            new_dir = os.path.join(temp_dir, "new_subdir")
            
            result = AudioFileManager.ensure_directory_exists(new_dir)
            
            self.assertTrue(result)
            self.assertTrue(os.path.exists(new_dir))
    
    def test_ensure_directory_exists_existing(self):
        """Test ensuring existing directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = AudioFileManager.ensure_directory_exists(temp_dir)
            
            self.assertTrue(result)
    
    def test_get_file_size_exists(self):
        """Test getting file size of existing file."""
        with tempfile.NamedTemporaryFile() as tmp_file:
            tmp_file.write(b"test data")
            tmp_file.flush()
            
            size = AudioFileManager.get_file_size(tmp_file.name)
            
            self.assertEqual(size, 9)  # "test data" is 9 bytes
    
    def test_get_file_size_not_exists(self):
        """Test getting file size of non-existent file."""
        size = AudioFileManager.get_file_size("non_existent_file.txt")
        
        self.assertIsNone(size)
    
    def test_is_valid_audio_file_valid(self):
        """Test validation of valid audio file."""
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            tmp_file.write(b"fake wav data")
            tmp_file.flush()
            
            result = AudioFileManager.is_valid_audio_file(tmp_file.name)
            
            self.assertTrue(result)
            os.unlink(tmp_file.name)
    
    def test_is_valid_audio_file_not_exists(self):
        """Test validation of non-existent file."""
        result = AudioFileManager.is_valid_audio_file("non_existent_file.wav")
        
        self.assertFalse(result)
    
    def test_is_valid_audio_file_wrong_extension(self):
        """Test validation of file with wrong extension."""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp_file:
            tmp_file.write(b"test data")
            tmp_file.flush()
            
            result = AudioFileManager.is_valid_audio_file(tmp_file.name)
            
            self.assertFalse(result)
            os.unlink(tmp_file.name)
    
    def test_is_valid_audio_file_empty(self):
        """Test validation of empty file."""
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            # Empty file
            pass
            
            result = AudioFileManager.is_valid_audio_file(tmp_file.name)
            
            self.assertFalse(result)
            os.unlink(tmp_file.name)


class TestTempFileContext(unittest.TestCase):
    """Test cases for TempFileContext class."""
    
    def test_context_manager_success(self):
        """Test successful context manager usage."""
        with TempFileContext(suffix=".test") as file_path:
            self.assertIsNotNone(file_path)
            self.assertTrue(file_path.endswith('.test'))
            self.assertTrue(os.path.exists(file_path))
        
        # File should be cleaned up after context exit
        self.assertFalse(os.path.exists(file_path))
    
    def test_context_manager_exception(self):
        """Test context manager with exception."""
        file_path = None
        try:
            with TempFileContext(suffix=".test") as fp:
                file_path = fp
                raise Exception("Test exception")
        except Exception:
            pass
        
        # File should still be cleaned up even with exception
        if file_path:
            self.assertFalse(os.path.exists(file_path))
    
    def test_context_manager_default_suffix(self):
        """Test context manager with default suffix."""
        with TempFileContext() as file_path:
            self.assertTrue(file_path.endswith('.wav'))


class TestUtilsIntegration(unittest.TestCase):
    """Integration tests for utils functionality."""
    
    def test_error_handler_with_file_operations(self):
        """Test error handler with file operations."""
        # Test that error handler works with file operations
        with patch('src.utils.error_handler.st') as mock_st:
            ErrorHandler.handle_audio_error(
                Exception("File operation failed"),
                "saving"
            )
            
            mock_st.error.assert_called_once_with("❌ Failed to save audio file")
    
    def test_file_manager_with_error_handler(self):
        """Test file manager error handling."""
        # Test that file manager uses error handler appropriately
        with patch('src.utils.file_utils.ErrorHandler') as mock_error_handler:
            AudioFileManager.save_audio_to_temp(
                np.random.rand(1000).astype(np.float32),
                16000
            )
            
            # Should not call error handler for successful operation
            mock_error_handler.handle_audio_error.assert_not_called()


if __name__ == '__main__':
    unittest.main() 