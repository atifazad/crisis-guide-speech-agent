"""
Test configuration and shared fixtures for the Voice-to-Voice AI Assistant project.
"""

import pytest
import tempfile
import os
import numpy as np
from unittest.mock import Mock, patch


@pytest.fixture
def temp_audio_file():
    """Create a temporary audio file for testing."""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        # Write some fake audio data
        tmp_file.write(b"fake audio data for testing")
        tmp_file.flush()
        yield tmp_file.name
    
    # Cleanup
    if os.path.exists(tmp_file.name):
        os.unlink(tmp_file.name)


@pytest.fixture
def sample_audio_data():
    """Create sample audio data for testing."""
    return np.random.rand(16000).astype(np.float32)


@pytest.fixture
def mock_streamlit():
    """Mock Streamlit for UI testing."""
    with patch('src.ui.components.st') as mock_st:
        # Mock common Streamlit components
        mock_st.title.return_value = None
        mock_st.markdown.return_value = None
        mock_st.header.return_value = None
        mock_st.subheader.return_value = None
        mock_st.button.return_value = True
        mock_st.text_area.return_value = None
        mock_st.success.return_value = None
        mock_st.error.return_value = None
        mock_st.info.return_value = None
        mock_st.warning.return_value = None
        mock_st.metric.return_value = None
        mock_st.write.return_value = None
        mock_st.spinner.return_value = None
        mock_st.columns.return_value = [Mock(), Mock()]
        mock_st.expander.return_value = None
        mock_st.progress_bar.return_value = None
        mock_st.code.return_value = None
        mock_st.dataframe.return_value = None
        mock_st.line_chart.return_value = None
        mock_st.download_button.return_value = None
        
        # Mock sidebar components
        mock_st.sidebar.header.return_value = None
        mock_st.sidebar.slider.return_value = 5
        mock_st.sidebar.selectbox.side_effect = [16000, "English"]
        
        yield mock_st


@pytest.fixture
def mock_whisper():
    """Mock Whisper for transcription testing."""
    with patch('src.transcription.whisper_client.whisper') as mock_whisper:
        mock_model = Mock()
        mock_model.transcribe.return_value = {"text": "Test transcription"}
        mock_whisper.load_model.return_value = mock_model
        yield mock_whisper


@pytest.fixture
def mock_sounddevice():
    """Mock sounddevice for audio testing."""
    with patch('src.audio.recorder.sd') as mock_sd:
        mock_devices = [
            {'name': 'Test Mic', 'max_input_channels': 1, 'max_output_channels': 0},
            {'name': 'Test Speaker', 'max_input_channels': 0, 'max_output_channels': 2}
        ]
        mock_sd.query_devices.return_value = mock_devices
        mock_sd.rec.return_value = np.random.rand(16000).astype(np.float32)
        mock_sd.wait.return_value = None
        yield mock_sd


@pytest.fixture
def mock_scipy():
    """Mock scipy for audio processing testing."""
    with patch('src.audio.preprocessor.scipy') as mock_scipy:
        mock_scipy.signal.resample.return_value = np.random.rand(16000).astype(np.float32)
        mock_scipy.signal.filtfilt.return_value = np.random.rand(16000).astype(np.float32)
        yield mock_scipy


@pytest.fixture
def mock_wavfile():
    """Mock wavfile for file operations testing."""
    with patch('src.utils.file_utils.wavfile') as mock_wavfile:
        mock_wavfile.write.return_value = None
        yield mock_wavfile


@pytest.fixture
def test_config():
    """Test configuration values."""
    return {
        'sample_rate': 16000,
        'recording_duration': 5,
        'language': 'en',
        'model_name': 'base',
        'audio_channels': 1,
        'audio_dtype': 'float32'
    }


@pytest.fixture
def error_handler():
    """Error handler instance for testing."""
    from src.utils.error_handler import ErrorHandler
    return ErrorHandler


@pytest.fixture
def audio_file_manager():
    """Audio file manager instance for testing."""
    from src.utils.file_utils import AudioFileManager
    return AudioFileManager


@pytest.fixture
def ui_components():
    """UI components instance for testing."""
    from src.ui.components import UIComponents
    return UIComponents


# Test markers for categorizing tests
def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line(
        "markers", "audio: marks tests as audio module tests"
    )
    config.addinivalue_line(
        "markers", "transcription: marks tests as transcription module tests"
    )
    config.addinivalue_line(
        "markers", "utils: marks tests as utils module tests"
    )
    config.addinivalue_line(
        "markers", "ui: marks tests as UI module tests"
    )
    config.addinivalue_line(
        "markers", "config: marks tests as config module tests"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )


# Test collection hooks
def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names."""
    for item in items:
        # Add module-specific markers based on test file names
        if "test_audio" in item.nodeid:
            item.add_marker(pytest.mark.audio)
        elif "test_transcription" in item.nodeid:
            item.add_marker(pytest.mark.transcription)
        elif "test_utils" in item.nodeid:
            item.add_marker(pytest.mark.utils)
        elif "test_ui" in item.nodeid:
            item.add_marker(pytest.mark.ui)
        elif "test_config" in item.nodeid:
            item.add_marker(pytest.mark.config)
        
        # Add integration marker for integration test classes
        if "Integration" in item.name:
            item.add_marker(pytest.mark.integration)
        else:
            item.add_marker(pytest.mark.unit) 