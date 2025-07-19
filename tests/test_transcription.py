"""
Unit tests for the transcription module.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import tempfile
import os

# Import the modules to test
from src.transcription.whisper_client import WhisperClient, TranscriptionManager


class TestWhisperClient(unittest.TestCase):
    """Test cases for WhisperClient class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.client = WhisperClient("base")  # Use smaller model for testing
    
    @patch('src.transcription.whisper_client.whisper')
    @patch('src.transcription.whisper_client.st')
    def test_load_model(self, mock_st, mock_whisper):
        """Test model loading."""
        mock_model = Mock()
        mock_whisper.load_model.return_value = mock_model
        
        self.client._load_model()
        
        mock_whisper.load_model.assert_called_once_with("base")
        self.assertEqual(self.client.model, mock_model)
    
    @patch('src.transcription.whisper_client.whisper')
    def test_transcribe_audio_success(self, mock_whisper):
        """Test successful audio transcription."""
        # Mock the model
        mock_model = Mock()
        mock_model.transcribe.return_value = {"text": "Hello world"}
        self.client.model = mock_model
        
        # Create a temporary audio file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            tmp_file.write(b"fake audio data")
            audio_file = tmp_file.name
        
        try:
            result = self.client.transcribe_audio(audio_file)
            
            self.assertEqual(result, "Hello world")
            mock_model.transcribe.assert_called_once()
        finally:
            os.unlink(audio_file)
    
    def test_transcribe_audio_no_model(self):
        """Test transcription when model is not loaded."""
        self.client.model = None
        
        result = self.client.transcribe_audio("test.wav")
        
        self.assertIsNone(result)
    
    @patch('src.transcription.whisper_client.whisper')
    def test_transcribe_audio_with_language(self, mock_whisper):
        """Test transcription with specific language."""
        mock_model = Mock()
        mock_model.transcribe.return_value = {"text": "Bonjour le monde"}
        self.client.model = mock_model
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            tmp_file.write(b"fake audio data")
            audio_file = tmp_file.name
        
        try:
            result = self.client.transcribe_audio(audio_file, language="fr")
            
            self.assertEqual(result, "Bonjour le monde")
            # Check that language was passed to transcribe
            call_args = mock_model.transcribe.call_args
            self.assertEqual(call_args[1]['language'], "fr")
        finally:
            os.unlink(audio_file)
    
    def test_get_available_models(self):
        """Test getting available models."""
        models = self.client.get_available_models()
        
        self.assertIsInstance(models, list)
        self.assertIn("base", models)
        self.assertIn("small", models)
    
    def test_get_model_info_no_model(self):
        """Test getting model info when model is not loaded."""
        self.client.model = None
        
        info = self.client.get_model_info()
        
        self.assertEqual(info['name'], "base")
        self.assertFalse(info['loaded'])
        self.assertEqual(info['type'], 'None')
    
    @patch('src.transcription.whisper_client.whisper')
    def test_get_model_info_with_model(self, mock_whisper):
        """Test getting model info when model is loaded."""
        mock_model = Mock()
        mock_model.__class__.__name__ = "Whisper"
        self.client.model = mock_model
        
        info = self.client.get_model_info()
        
        self.assertEqual(info['name'], "base")
        self.assertTrue(info['loaded'])
        self.assertEqual(info['type'], 'Whisper')
        self.assertIn('parameters', info)
    
    def test_estimate_model_size(self):
        """Test model size estimation."""
        # Test known model sizes
        self.client.model_name = "tiny"
        self.assertEqual(self.client._estimate_model_size(), "39M")
        
        self.client.model_name = "base"
        self.assertEqual(self.client._estimate_model_size(), "74M")
        
        self.client.model_name = "small"
        self.assertEqual(self.client._estimate_model_size(), "244M")
        
        # Test unknown model
        self.client.model_name = "unknown"
        self.assertEqual(self.client._estimate_model_size(), "Unknown")
    
    @patch('src.transcription.whisper_client.whisper')
    @patch('src.transcription.whisper_client.st')
    def test_change_model_success(self, mock_st, mock_whisper):
        """Test successful model change."""
        mock_model = Mock()
        mock_whisper.load_model.return_value = mock_model
        
        result = self.client.change_model("small")
        
        self.assertTrue(result)
        self.assertEqual(self.client.model_name, "small")
    
    def test_change_model_invalid(self):
        """Test changing to invalid model."""
        result = self.client.change_model("invalid_model")
        
        self.assertFalse(result)
    
    @patch('src.transcription.whisper_client.whisper')
    def test_get_transcription_confidence(self, mock_whisper):
        """Test getting transcription confidence."""
        mock_model = Mock()
        mock_model.transcribe.return_value = {
            "segments": [
                {"avg_logprob": -0.1},
                {"avg_logprob": -0.2}
            ]
        }
        self.client.model = mock_model
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            tmp_file.write(b"fake audio data")
            audio_file = tmp_file.name
        
        try:
            confidence = self.client.get_transcription_confidence(audio_file)
            
            self.assertIsNotNone(confidence)
            self.assertIsInstance(confidence, float)
        finally:
            os.unlink(audio_file)
    
    def test_get_transcription_confidence_no_model(self):
        """Test getting confidence when model is not loaded."""
        self.client.model = None
        
        confidence = self.client.get_transcription_confidence("test.wav")
        
        self.assertIsNone(confidence)


class TestTranscriptionManager(unittest.TestCase):
    """Test cases for TranscriptionManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.manager = TranscriptionManager("base")
    
    def test_init(self):
        """Test TranscriptionManager initialization."""
        self.assertIsNotNone(self.manager.whisper_client)
        self.assertIsNotNone(self.manager.language_options)
        self.assertIn("Auto-detect", self.manager.language_options)
        self.assertIn("English", self.manager.language_options)
    
    @patch('src.transcription.whisper_client.WhisperClient')
    def test_transcribe_with_settings(self, mock_whisper_client_class):
        """Test transcription with settings."""
        # Mock the whisper client
        mock_client = Mock()
        mock_client.transcribe_audio.return_value = "Transcribed text"
        self.manager.whisper_client = mock_client
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            tmp_file.write(b"fake audio data")
            audio_file = tmp_file.name
        
        try:
            result = self.manager.transcribe_with_settings(
                audio_file,
                language_name="English",
                task="transcribe"
            )
            
            self.assertEqual(result, "Transcribed text")
            # Check that language code was passed correctly
            mock_client.transcribe_audio.assert_called_once()
            call_args = mock_client.transcribe_audio.call_args
            self.assertEqual(call_args[1]['language'], "en")
        finally:
            os.unlink(audio_file)
    
    def test_get_language_options(self):
        """Test getting language options."""
        options = self.manager.get_language_options()
        
        self.assertIsInstance(options, dict)
        self.assertIn("Auto-detect", options)
        self.assertIn("English", options)
        self.assertIn("Spanish", options)
        self.assertIsNone(options["Auto-detect"])
        self.assertEqual(options["English"], "en")
    
    def test_validate_language_valid(self):
        """Test validation of valid language."""
        result = self.manager.validate_language("English")
        self.assertTrue(result)
    
    def test_validate_language_invalid(self):
        """Test validation of invalid language."""
        result = self.manager.validate_language("Invalid Language")
        self.assertFalse(result)
    
    def test_get_model_info(self):
        """Test getting model information."""
        info = self.manager.get_model_info()
        
        self.assertIsInstance(info, dict)
        self.assertIn('name', info)
        self.assertIn('loaded', info)
        self.assertIn('type', info)
    
    @patch('src.transcription.whisper_client.WhisperClient')
    def test_change_model(self, mock_whisper_client_class):
        """Test changing model."""
        mock_client = Mock()
        mock_client.change_model.return_value = True
        self.manager.whisper_client = mock_client
        
        result = self.manager.change_model("small")
        
        self.assertTrue(result)
        mock_client.change_model.assert_called_once_with("small")
    
    def test_get_available_models(self):
        """Test getting available models."""
        models = self.manager.get_available_models()
        
        self.assertIsInstance(models, list)
        self.assertIn("base", models)
        self.assertIn("small", models)


class TestTranscriptionIntegration(unittest.TestCase):
    """Integration tests for transcription functionality."""
    
    def test_language_mapping(self):
        """Test that language names map to correct codes."""
        manager = TranscriptionManager()
        
        # Test some common language mappings
        self.assertEqual(manager.language_options["English"], "en")
        self.assertEqual(manager.language_options["Spanish"], "es")
        self.assertEqual(manager.language_options["French"], "fr")
        self.assertEqual(manager.language_options["German"], "de")
        self.assertIsNone(manager.language_options["Auto-detect"])
    
    def test_model_initialization(self):
        """Test that TranscriptionManager initializes with correct model."""
        manager = TranscriptionManager("small")
        
        self.assertEqual(manager.whisper_client.model_name, "small")
    
    def test_error_handling(self):
        """Test error handling in transcription."""
        manager = TranscriptionManager()
        
        # Test with non-existent file
        result = manager.transcribe_with_settings("non_existent_file.wav")
        
        # Should handle error gracefully
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main() 