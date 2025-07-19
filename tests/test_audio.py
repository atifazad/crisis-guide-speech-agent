"""
Unit tests for the audio module.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import numpy as np
import tempfile
import os

# Import the modules to test
from src.audio.recorder import AudioRecorder, AudioDeviceManager
from src.audio.preprocessor import AudioPreprocessor


class TestAudioRecorder(unittest.TestCase):
    """Test cases for AudioRecorder class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.recorder = AudioRecorder()
    
    @patch('src.audio.recorder.sd')
    def test_get_audio_devices(self, mock_sd):
        """Test getting audio devices."""
        # Mock device data
        mock_devices = [
            {'name': 'Test Mic', 'max_input_channels': 1, 'max_output_channels': 0},
            {'name': 'Test Speaker', 'max_input_channels': 0, 'max_output_channels': 2}
        ]
        mock_sd.query_devices.return_value = mock_devices
        
        devices = self.recorder._get_audio_devices()
        
        self.assertIn('all', devices)
        self.assertIn('input', devices)
        self.assertIn('output', devices)
        self.assertEqual(len(devices['input']), 1)
        self.assertEqual(len(devices['output']), 1)
    
    @patch('src.audio.recorder.sd')
    def test_get_input_devices(self, mock_sd):
        """Test getting input devices."""
        # Mock device data
        mock_devices = [
            {'name': 'Test Mic 1', 'max_input_channels': 1},
            {'name': 'Test Mic 2', 'max_input_channels': 2}
        ]
        self.recorder.devices = {'input': mock_devices}
        
        input_devices = self.recorder.get_input_devices()
        
        self.assertEqual(len(input_devices), 2)
        self.assertEqual(input_devices[0]['name'], 'Test Mic 1')
    
    @patch('src.audio.recorder.sd')
    def test_get_default_input_device(self, mock_sd):
        """Test getting default input device."""
        mock_device = {'name': 'Default Mic', 'max_input_channels': 1}
        mock_sd.query_devices.return_value = mock_device
        
        device = self.recorder.get_default_input_device()
        
        self.assertEqual(device['name'], 'Default Mic')
    
    @patch('src.audio.recorder.sd')
    @patch('src.audio.recorder.st')
    def test_record_audio(self, mock_st, mock_sd):
        """Test audio recording."""
        # Mock audio data
        mock_audio = np.random.rand(16000).astype(np.float32)
        mock_sd.rec.return_value = mock_audio
        mock_sd.wait.return_value = None
        
        result = self.recorder.record_audio(duration=1, sample_rate=16000)
        
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 16000)
    
    def test_validate_recording_settings_valid(self):
        """Test validation of valid recording settings."""
        result = self.recorder.validate_recording_settings(5, 16000)
        self.assertTrue(result)
    
    def test_validate_recording_settings_invalid_duration(self):
        """Test validation of invalid recording duration."""
        result = self.recorder.validate_recording_settings(1, 16000)
        self.assertFalse(result)
    
    def test_validate_recording_settings_invalid_sample_rate(self):
        """Test validation of invalid sample rate."""
        result = self.recorder.validate_recording_settings(5, 22050)
        self.assertFalse(result)
    
    def test_get_device_info(self):
        """Test getting device information."""
        info = self.recorder.get_device_info()
        
        self.assertIn('total_input_devices', info)
        self.assertIn('input_devices', info)
        self.assertIn('default_device', info)
        self.assertIn('has_devices', info)


class TestAudioDeviceManager(unittest.TestCase):
    """Test cases for AudioDeviceManager class."""
    
    @patch('src.audio.recorder.sd')
    def test_list_devices(self, mock_sd):
        """Test listing audio devices."""
        mock_devices = [
            {'name': 'Device 1', 'max_input_channels': 1},
            {'name': 'Device 2', 'max_output_channels': 2}
        ]
        mock_sd.query_devices.return_value = mock_devices
        
        devices = AudioDeviceManager.list_devices()
        
        self.assertEqual(len(devices), 2)
    
    @patch('src.audio.recorder.sd')
    def test_get_device_by_name(self, mock_sd):
        """Test getting device by name."""
        mock_devices = [
            {'name': 'Test Device', 'max_input_channels': 1},
            {'name': 'Other Device', 'max_output_channels': 2}
        ]
        mock_sd.query_devices.return_value = mock_devices
        
        device = AudioDeviceManager.get_device_by_name('Test Device')
        
        self.assertIsNotNone(device)
        self.assertEqual(device['name'], 'Test Device')
    
    @patch('src.audio.recorder.sd')
    def test_set_default_device(self, mock_sd):
        """Test setting default device."""
        result = AudioDeviceManager.set_default_device('Test Device')
        
        # Should not raise exception
        self.assertIsInstance(result, bool)


class TestAudioPreprocessor(unittest.TestCase):
    """Test cases for AudioPreprocessor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.preprocessor = AudioPreprocessor()
    
    def test_preprocess_audio_basic(self):
        """Test basic audio preprocessing."""
        # Create test audio data
        audio_data = np.random.rand(16000).astype(np.float32)
        sample_rate = 16000
        
        processed_audio, processed_sample_rate = self.preprocessor.preprocess_audio(
            audio_data, sample_rate
        )
        
        self.assertIsNotNone(processed_audio)
        self.assertEqual(processed_sample_rate, 16000)
        self.assertEqual(len(processed_audio), len(audio_data))
    
    def test_preprocess_audio_resampling(self):
        """Test audio preprocessing with resampling."""
        # Create test audio data at different sample rate
        audio_data = np.random.rand(8000).astype(np.float32)
        sample_rate = 8000
        
        processed_audio, processed_sample_rate = self.preprocessor.preprocess_audio(
            audio_data, sample_rate
        )
        
        self.assertEqual(processed_sample_rate, 16000)
    
    def test_apply_noise_reduction(self):
        """Test noise reduction."""
        audio_data = np.random.rand(16000).astype(np.float32)
        sample_rate = 16000
        
        filtered_audio = self.preprocessor._apply_noise_reduction(audio_data, sample_rate)
        
        self.assertIsNotNone(filtered_audio)
        self.assertEqual(len(filtered_audio), len(audio_data))
    
    def test_enhance_audio_quality(self):
        """Test audio quality enhancement."""
        audio_data = np.random.rand(16000).astype(np.float32)
        sample_rate = 16000
        
        enhanced_audio, enhanced_sample_rate = self.preprocessor.enhance_audio_quality(
            audio_data, sample_rate
        )
        
        self.assertIsNotNone(enhanced_audio)
        self.assertEqual(enhanced_sample_rate, sample_rate)
    
    def test_validate_audio_data_valid(self):
        """Test validation of valid audio data."""
        audio_data = np.random.rand(16000).astype(np.float32)
        sample_rate = 16000
        
        result = self.preprocessor.validate_audio_data(audio_data, sample_rate)
        
        self.assertTrue(result)
    
    def test_validate_audio_data_empty(self):
        """Test validation of empty audio data."""
        audio_data = np.array([])
        sample_rate = 16000
        
        result = self.preprocessor.validate_audio_data(audio_data, sample_rate)
        
        self.assertFalse(result)
    
    def test_validate_audio_data_low_amplitude(self):
        """Test validation of low amplitude audio data."""
        audio_data = np.random.rand(16000).astype(np.float32) * 0.001  # Very low amplitude
        sample_rate = 16000
        
        result = self.preprocessor.validate_audio_data(audio_data, sample_rate)
        
        self.assertFalse(result)
    
    def test_get_audio_statistics(self):
        """Test getting audio statistics."""
        audio_data = np.random.rand(16000).astype(np.float32)
        sample_rate = 16000
        
        stats = self.preprocessor.get_audio_statistics(audio_data, sample_rate)
        
        self.assertIn('duration', stats)
        self.assertIn('sample_rate', stats)
        self.assertIn('rms', stats)
        self.assertIn('peak', stats)
        self.assertIn('snr', stats)
        self.assertIn('is_valid', stats)
        self.assertEqual(stats['sample_rate'], sample_rate)
        self.assertEqual(stats['duration'], 1.0)  # 16000 samples at 16kHz = 1 second


if __name__ == '__main__':
    unittest.main() 