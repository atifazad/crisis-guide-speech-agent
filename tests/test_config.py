"""
Unit tests for the config module.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock

# Import the modules to test
from src.config.constants import (
    LANGUAGE_OPTIONS,
    AUDIO_SETTINGS,
    WHISPER_SETTINGS,
    UI_SETTINGS,
    FILE_SETTINGS,
    ERROR_MESSAGES,
    SUCCESS_MESSAGES,
    ACCURACY_TIPS,
    TROUBLESHOOTING_TIPS
)


class TestLanguageOptions(unittest.TestCase):
    """Test cases for language options configuration."""
    
    def test_language_options_structure(self):
        """Test that language options have correct structure."""
        self.assertIsInstance(LANGUAGE_OPTIONS, dict)
        self.assertGreater(len(LANGUAGE_OPTIONS), 0)
    
    def test_auto_detect_option(self):
        """Test that Auto-detect option is present and has None value."""
        self.assertIn("Auto-detect", LANGUAGE_OPTIONS)
        self.assertIsNone(LANGUAGE_OPTIONS["Auto-detect"])
    
    def test_english_option(self):
        """Test that English option is present and has correct code."""
        self.assertIn("English", LANGUAGE_OPTIONS)
        self.assertEqual(LANGUAGE_OPTIONS["English"], "en")
    
    def test_language_codes_are_strings(self):
        """Test that all language codes are strings (except Auto-detect)."""
        for language, code in LANGUAGE_OPTIONS.items():
            if language != "Auto-detect":
                self.assertIsInstance(code, str)
                self.assertEqual(len(code), 2)  # ISO 639-1 codes are 2 characters


class TestAudioSettings(unittest.TestCase):
    """Test cases for audio settings configuration."""
    
    def test_audio_settings_structure(self):
        """Test that audio settings have correct structure."""
        self.assertIsInstance(AUDIO_SETTINGS, dict)
        self.assertGreater(len(AUDIO_SETTINGS), 0)
    
    def test_default_sample_rate(self):
        """Test default sample rate setting."""
        self.assertIn("DEFAULT_SAMPLE_RATE", AUDIO_SETTINGS)
        self.assertEqual(AUDIO_SETTINGS["DEFAULT_SAMPLE_RATE"], 16000)
        self.assertIsInstance(AUDIO_SETTINGS["DEFAULT_SAMPLE_RATE"], int)
    
    def test_default_recording_duration(self):
        """Test default recording duration setting."""
        self.assertIn("DEFAULT_RECORDING_DURATION", AUDIO_SETTINGS)
        self.assertEqual(AUDIO_SETTINGS["DEFAULT_RECORDING_DURATION"], 5)
        self.assertIsInstance(AUDIO_SETTINGS["DEFAULT_RECORDING_DURATION"], int)
    
    def test_supported_sample_rates(self):
        """Test supported sample rates setting."""
        self.assertIn("SUPPORTED_SAMPLE_RATES", AUDIO_SETTINGS)
        self.assertIsInstance(AUDIO_SETTINGS["SUPPORTED_SAMPLE_RATES"], list)
        self.assertIn(8000, AUDIO_SETTINGS["SUPPORTED_SAMPLE_RATES"])
        self.assertIn(16000, AUDIO_SETTINGS["SUPPORTED_SAMPLE_RATES"])
        self.assertIn(44100, AUDIO_SETTINGS["SUPPORTED_SAMPLE_RATES"])
    
    def test_min_recording_duration(self):
        """Test minimum recording duration setting."""
        self.assertIn("MIN_RECORDING_DURATION", AUDIO_SETTINGS)
        self.assertEqual(AUDIO_SETTINGS["MIN_RECORDING_DURATION"], 3)
        self.assertIsInstance(AUDIO_SETTINGS["MIN_RECORDING_DURATION"], int)
    
    def test_max_recording_duration(self):
        """Test maximum recording duration setting."""
        self.assertIn("MAX_RECORDING_DURATION", AUDIO_SETTINGS)
        self.assertEqual(AUDIO_SETTINGS["MAX_RECORDING_DURATION"], 15)
        self.assertIsInstance(AUDIO_SETTINGS["MAX_RECORDING_DURATION"], int)
    
    def test_audio_channels(self):
        """Test audio channels setting."""
        self.assertIn("AUDIO_CHANNELS", AUDIO_SETTINGS)
        self.assertEqual(AUDIO_SETTINGS["AUDIO_CHANNELS"], 1)
        self.assertIsInstance(AUDIO_SETTINGS["AUDIO_CHANNELS"], int)
    
    def test_audio_dtype(self):
        """Test audio data type setting."""
        self.assertIn("AUDIO_DTYPE", AUDIO_SETTINGS)
        self.assertEqual(AUDIO_SETTINGS["AUDIO_DTYPE"], "float32")
        self.assertIsInstance(AUDIO_SETTINGS["AUDIO_DTYPE"], str)
    
    def test_duration_constraints(self):
        """Test that duration constraints are logical."""
        self.assertLess(
            AUDIO_SETTINGS["MIN_RECORDING_DURATION"],
            AUDIO_SETTINGS["MAX_RECORDING_DURATION"]
        )
        self.assertLess(
            AUDIO_SETTINGS["MIN_RECORDING_DURATION"],
            AUDIO_SETTINGS["DEFAULT_RECORDING_DURATION"]
        )
        self.assertLess(
            AUDIO_SETTINGS["DEFAULT_RECORDING_DURATION"],
            AUDIO_SETTINGS["MAX_RECORDING_DURATION"]
        )


class TestWhisperSettings(unittest.TestCase):
    """Test cases for Whisper settings configuration."""
    
    def test_whisper_settings_structure(self):
        """Test that Whisper settings have correct structure."""
        self.assertIsInstance(WHISPER_SETTINGS, dict)
        self.assertGreater(len(WHISPER_SETTINGS), 0)
    
    def test_default_model(self):
        """Test default model setting."""
        self.assertIn("DEFAULT_MODEL", WHISPER_SETTINGS)
        self.assertEqual(WHISPER_SETTINGS["DEFAULT_MODEL"], "small")
        self.assertIsInstance(WHISPER_SETTINGS["DEFAULT_MODEL"], str)
    
    def test_available_models(self):
        """Test available models setting."""
        self.assertIn("AVAILABLE_MODELS", WHISPER_SETTINGS)
        self.assertIsInstance(WHISPER_SETTINGS["AVAILABLE_MODELS"], list)
        self.assertIn("tiny", WHISPER_SETTINGS["AVAILABLE_MODELS"])
        self.assertIn("base", WHISPER_SETTINGS["AVAILABLE_MODELS"])
        self.assertIn("small", WHISPER_SETTINGS["AVAILABLE_MODELS"])
        self.assertIn("medium", WHISPER_SETTINGS["AVAILABLE_MODELS"])
        self.assertIn("large", WHISPER_SETTINGS["AVAILABLE_MODELS"])
    
    def test_model_cache_dir(self):
        """Test model cache directory setting."""
        self.assertIn("MODEL_CACHE_DIR", WHISPER_SETTINGS)
        self.assertEqual(WHISPER_SETTINGS["MODEL_CACHE_DIR"], "data/models")
        self.assertIsInstance(WHISPER_SETTINGS["MODEL_CACHE_DIR"], str)
    
    def test_fp16_enabled(self):
        """Test FP16 enabled setting."""
        self.assertIn("FP16_ENABLED", WHISPER_SETTINGS)
        self.assertFalse(WHISPER_SETTINGS["FP16_ENABLED"])
        self.assertIsInstance(WHISPER_SETTINGS["FP16_ENABLED"], bool)
    
    def test_verbose(self):
        """Test verbose setting."""
        self.assertIn("VERBOSE", WHISPER_SETTINGS)
        self.assertFalse(WHISPER_SETTINGS["VERBOSE"])
        self.assertIsInstance(WHISPER_SETTINGS["VERBOSE"], bool)
    
    def test_default_model_in_available_models(self):
        """Test that default model is in available models."""
        self.assertIn(
            WHISPER_SETTINGS["DEFAULT_MODEL"],
            WHISPER_SETTINGS["AVAILABLE_MODELS"]
        )


class TestUISettings(unittest.TestCase):
    """Test cases for UI settings configuration."""
    
    def test_ui_settings_structure(self):
        """Test that UI settings have correct structure."""
        self.assertIsInstance(UI_SETTINGS, dict)
        self.assertGreater(len(UI_SETTINGS), 0)
    
    def test_page_title(self):
        """Test page title setting."""
        self.assertIn("PAGE_TITLE", UI_SETTINGS)
        self.assertEqual(UI_SETTINGS["PAGE_TITLE"], "Voice-to-Voice AI Assistant")
        self.assertIsInstance(UI_SETTINGS["PAGE_TITLE"], str)
    
    def test_page_icon(self):
        """Test page icon setting."""
        self.assertIn("PAGE_ICON", UI_SETTINGS)
        self.assertEqual(UI_SETTINGS["PAGE_ICON"], "🎤")
        self.assertIsInstance(UI_SETTINGS["PAGE_ICON"], str)
    
    def test_layout(self):
        """Test layout setting."""
        self.assertIn("LAYOUT", UI_SETTINGS)
        self.assertEqual(UI_SETTINGS["LAYOUT"], "wide")
        self.assertIsInstance(UI_SETTINGS["LAYOUT"], str)
    
    def test_sidebar_title(self):
        """Test sidebar title setting."""
        self.assertIn("SIDEBAR_TITLE", UI_SETTINGS)
        self.assertEqual(UI_SETTINGS["SIDEBAR_TITLE"], "Settings")
        self.assertIsInstance(UI_SETTINGS["SIDEBAR_TITLE"], str)
    
    def test_main_title(self):
        """Test main title setting."""
        self.assertIn("MAIN_TITLE", UI_SETTINGS)
        self.assertEqual(UI_SETTINGS["MAIN_TITLE"], "🎤 Voice-to-Voice AI Assistant")
        self.assertIsInstance(UI_SETTINGS["MAIN_TITLE"], str)
    
    def test_subtitle(self):
        """Test subtitle setting."""
        self.assertIn("SUBTITLE", UI_SETTINGS)
        self.assertEqual(UI_SETTINGS["SUBTITLE"], "Speech Input Interface with Google Whisper")
        self.assertIsInstance(UI_SETTINGS["SUBTITLE"], str)


class TestFileSettings(unittest.TestCase):
    """Test cases for file settings configuration."""
    
    def test_file_settings_structure(self):
        """Test that file settings have correct structure."""
        self.assertIsInstance(FILE_SETTINGS, dict)
        self.assertGreater(len(FILE_SETTINGS), 0)
    
    def test_temp_audio_suffix(self):
        """Test temporary audio suffix setting."""
        self.assertIn("TEMP_AUDIO_SUFFIX", FILE_SETTINGS)
        self.assertEqual(FILE_SETTINGS["TEMP_AUDIO_SUFFIX"], ".wav")
        self.assertIsInstance(FILE_SETTINGS["TEMP_AUDIO_SUFFIX"], str)
    
    def test_temp_audio_prefix(self):
        """Test temporary audio prefix setting."""
        self.assertIn("TEMP_AUDIO_PREFIX", FILE_SETTINGS)
        self.assertEqual(FILE_SETTINGS["TEMP_AUDIO_PREFIX"], "temp_audio_")
        self.assertIsInstance(FILE_SETTINGS["TEMP_AUDIO_PREFIX"], str)
    
    def test_delete_temp_files(self):
        """Test delete temporary files setting."""
        self.assertIn("DELETE_TEMP_FILES", FILE_SETTINGS)
        self.assertTrue(FILE_SETTINGS["DELETE_TEMP_FILES"])
        self.assertIsInstance(FILE_SETTINGS["DELETE_TEMP_FILES"], bool)


class TestErrorMessages(unittest.TestCase):
    """Test cases for error messages configuration."""
    
    def test_error_messages_structure(self):
        """Test that error messages have correct structure."""
        self.assertIsInstance(ERROR_MESSAGES, dict)
        self.assertGreater(len(ERROR_MESSAGES), 0)
    
    def test_audio_recording_failed(self):
        """Test audio recording failed message."""
        self.assertIn("AUDIO_RECORDING_FAILED", ERROR_MESSAGES)
        self.assertEqual(ERROR_MESSAGES["AUDIO_RECORDING_FAILED"], "Failed to record audio")
        self.assertIsInstance(ERROR_MESSAGES["AUDIO_RECORDING_FAILED"], str)
    
    def test_audio_save_failed(self):
        """Test audio save failed message."""
        self.assertIn("AUDIO_SAVE_FAILED", ERROR_MESSAGES)
        self.assertEqual(ERROR_MESSAGES["AUDIO_SAVE_FAILED"], "Failed to save audio file")
        self.assertIsInstance(ERROR_MESSAGES["AUDIO_SAVE_FAILED"], str)
    
    def test_transcription_failed(self):
        """Test transcription failed message."""
        self.assertIn("TRANSCRIPTION_FAILED", ERROR_MESSAGES)
        self.assertEqual(ERROR_MESSAGES["TRANSCRIPTION_FAILED"], "Failed to transcribe audio")
        self.assertIsInstance(ERROR_MESSAGES["TRANSCRIPTION_FAILED"], str)
    
    def test_model_load_failed(self):
        """Test model load failed message."""
        self.assertIn("MODEL_LOAD_FAILED", ERROR_MESSAGES)
        self.assertEqual(ERROR_MESSAGES["MODEL_LOAD_FAILED"], "Failed to load Whisper model")
        self.assertIsInstance(ERROR_MESSAGES["MODEL_LOAD_FAILED"], str)
    
    def test_device_not_found(self):
        """Test device not found message."""
        self.assertIn("DEVICE_NOT_FOUND", ERROR_MESSAGES)
        self.assertEqual(ERROR_MESSAGES["DEVICE_NOT_FOUND"], "No audio input devices found")
        self.assertIsInstance(ERROR_MESSAGES["DEVICE_NOT_FOUND"], str)
    
    def test_preprocessing_failed(self):
        """Test preprocessing failed message."""
        self.assertIn("PREPROCESSING_FAILED", ERROR_MESSAGES)
        self.assertEqual(ERROR_MESSAGES["PREPROCESSING_FAILED"], "Failed to preprocess audio")
        self.assertIsInstance(ERROR_MESSAGES["PREPROCESSING_FAILED"], str)


class TestSuccessMessages(unittest.TestCase):
    """Test cases for success messages configuration."""
    
    def test_success_messages_structure(self):
        """Test that success messages have correct structure."""
        self.assertIsInstance(SUCCESS_MESSAGES, dict)
        self.assertGreater(len(SUCCESS_MESSAGES), 0)
    
    def test_audio_recorded(self):
        """Test audio recorded message."""
        self.assertIn("AUDIO_RECORDED", SUCCESS_MESSAGES)
        self.assertEqual(SUCCESS_MESSAGES["AUDIO_RECORDED"], "Audio recorded successfully")
        self.assertIsInstance(SUCCESS_MESSAGES["AUDIO_RECORDED"], str)
    
    def test_audio_transcribed(self):
        """Test audio transcribed message."""
        self.assertIn("AUDIO_TRANSCRIBED", SUCCESS_MESSAGES)
        self.assertEqual(SUCCESS_MESSAGES["AUDIO_TRANSCRIBED"], "Audio transcribed successfully")
        self.assertIsInstance(SUCCESS_MESSAGES["AUDIO_TRANSCRIBED"], str)
    
    def test_model_loaded(self):
        """Test model loaded message."""
        self.assertIn("MODEL_LOADED", SUCCESS_MESSAGES)
        self.assertEqual(SUCCESS_MESSAGES["MODEL_LOADED"], "Whisper model loaded successfully")
        self.assertIsInstance(SUCCESS_MESSAGES["MODEL_LOADED"], str)
    
    def test_audio_processed(self):
        """Test audio processed message."""
        self.assertIn("AUDIO_PROCESSED", SUCCESS_MESSAGES)
        self.assertEqual(SUCCESS_MESSAGES["AUDIO_PROCESSED"], "Audio processed with improved settings")
        self.assertIsInstance(SUCCESS_MESSAGES["AUDIO_PROCESSED"], str)


class TestAccuracyTips(unittest.TestCase):
    """Test cases for accuracy tips configuration."""
    
    def test_accuracy_tips_structure(self):
        """Test that accuracy tips have correct structure."""
        self.assertIsInstance(ACCURACY_TIPS, list)
        self.assertGreater(len(ACCURACY_TIPS), 0)
    
    def test_accuracy_tips_content(self):
        """Test that accuracy tips contain expected content."""
        expected_tips = [
            "Speak clearly and at a normal pace",
            "Minimize background noise",
            "Keep the microphone close to your mouth",
            "Use quiet environment",
            "Select correct language in settings",
            "Speak for full duration of recording"
        ]
        
        for tip in expected_tips:
            self.assertIn(tip, ACCURACY_TIPS)
    
    def test_accuracy_tips_are_strings(self):
        """Test that all accuracy tips are strings."""
        for tip in ACCURACY_TIPS:
            self.assertIsInstance(tip, str)
            self.assertGreater(len(tip), 0)


class TestTroubleshootingTips(unittest.TestCase):
    """Test cases for troubleshooting tips configuration."""
    
    def test_troubleshooting_tips_structure(self):
        """Test that troubleshooting tips have correct structure."""
        self.assertIsInstance(TROUBLESHOOTING_TIPS, dict)
        self.assertGreater(len(TROUBLESHOOTING_TIPS), 0)
    
    def test_poor_quality_tips(self):
        """Test poor quality troubleshooting tips."""
        self.assertIn("POOR_QUALITY", TROUBLESHOOTING_TIPS)
        self.assertIsInstance(TROUBLESHOOTING_TIPS["POOR_QUALITY"], list)
        self.assertGreater(len(TROUBLESHOOTING_TIPS["POOR_QUALITY"]), 0)
        
        expected_tips = [
            "Ensure microphone permissions are granted",
            "Check that microphone is working in other apps",
            "Try speaking louder and more clearly",
            "Reduce background noise"
        ]
        
        for tip in expected_tips:
            self.assertIn(tip, TROUBLESHOOTING_TIPS["POOR_QUALITY"])
    
    def test_no_audio_tips(self):
        """Test no audio troubleshooting tips."""
        self.assertIn("NO_AUDIO", TROUBLESHOOTING_TIPS)
        self.assertIsInstance(TROUBLESHOOTING_TIPS["NO_AUDIO"], list)
        self.assertGreater(len(TROUBLESHOOTING_TIPS["NO_AUDIO"]), 0)
        
        expected_tips = [
            "Check microphone connection",
            "Verify browser microphone permissions",
            "Try refreshing the page"
        ]
        
        for tip in expected_tips:
            self.assertIn(tip, TROUBLESHOOTING_TIPS["NO_AUDIO"])
    
    def test_model_issues_tips(self):
        """Test model issues troubleshooting tips."""
        self.assertIn("MODEL_ISSUES", TROUBLESHOOTING_TIPS)
        self.assertIsInstance(TROUBLESHOOTING_TIPS["MODEL_ISSUES"], list)
        self.assertGreater(len(TROUBLESHOOTING_TIPS["MODEL_ISSUES"]), 0)
        
        expected_tips = [
            "Ensure stable internet connection",
            "Check available disk space",
            "Restart the application"
        ]
        
        for tip in expected_tips:
            self.assertIn(tip, TROUBLESHOOTING_TIPS["MODEL_ISSUES"])
    
    def test_troubleshooting_tips_are_strings(self):
        """Test that all troubleshooting tips are strings."""
        for category, tips in TROUBLESHOOTING_TIPS.items():
            self.assertIsInstance(category, str)
            self.assertIsInstance(tips, list)
            for tip in tips:
                self.assertIsInstance(tip, str)
                self.assertGreater(len(tip), 0)


class TestConfigIntegration(unittest.TestCase):
    """Integration tests for configuration."""
    
    def test_config_consistency(self):
        """Test that configuration values are consistent."""
        # Test that default model is in available models
        self.assertIn(
            WHISPER_SETTINGS["DEFAULT_MODEL"],
            WHISPER_SETTINGS["AVAILABLE_MODELS"]
        )
        
        # Test that default sample rate is in supported sample rates
        self.assertIn(
            AUDIO_SETTINGS["DEFAULT_SAMPLE_RATE"],
            AUDIO_SETTINGS["SUPPORTED_SAMPLE_RATES"]
        )
        
        # Test that default recording duration is within bounds
        self.assertGreaterEqual(
            AUDIO_SETTINGS["DEFAULT_RECORDING_DURATION"],
            AUDIO_SETTINGS["MIN_RECORDING_DURATION"]
        )
        self.assertLessEqual(
            AUDIO_SETTINGS["DEFAULT_RECORDING_DURATION"],
            AUDIO_SETTINGS["MAX_RECORDING_DURATION"]
        )
    
    def test_config_completeness(self):
        """Test that all required configuration sections are present."""
        required_sections = [
            LANGUAGE_OPTIONS,
            AUDIO_SETTINGS,
            WHISPER_SETTINGS,
            UI_SETTINGS,
            FILE_SETTINGS,
            ERROR_MESSAGES,
            SUCCESS_MESSAGES,
            ACCURACY_TIPS,
            TROUBLESHOOTING_TIPS
        ]
        
        for section in required_sections:
            self.assertIsNotNone(section)
            self.assertGreater(len(section), 0)


if __name__ == '__main__':
    unittest.main() 