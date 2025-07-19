# Voice-to-Voice AI Assistant - Test Suite

This directory contains comprehensive unit tests for the Voice-to-Voice AI Assistant project. The test suite covers all major modules and components of the application.

## Test Structure

### Test Files

- **`test_audio.py`** - Tests for audio recording, device management, and preprocessing
- **`test_transcription.py`** - Tests for Whisper transcription and model management
- **`test_utils.py`** - Tests for error handling and file utilities
- **`test_ui.py`** - Tests for UI components and Streamlit integration
- **`test_config.py`** - Tests for configuration constants and settings
- **`test_runner.py`** - Test runner script for executing all tests
- **`conftest.py`** - Pytest configuration and shared fixtures

### Test Categories

#### Audio Module Tests (`test_audio.py`)
- **TestAudioRecorder**: Tests audio recording functionality
  - Device enumeration and selection
  - Audio recording with different parameters
  - Recording validation and error handling
- **TestAudioDeviceManager**: Tests audio device management
  - Device listing and filtering
  - Device selection and configuration
- **TestAudioPreprocessor**: Tests audio preprocessing
  - Audio quality enhancement
  - Noise reduction and filtering
  - Audio validation and statistics

#### Transcription Module Tests (`test_transcription.py`)
- **TestWhisperClient**: Tests Whisper model integration
  - Model loading and initialization
  - Audio transcription with different settings
  - Model switching and configuration
  - Confidence scoring
- **TestTranscriptionManager**: Tests high-level transcription management
  - Language selection and mapping
  - Transcription workflow
  - Error handling and fallbacks
- **TestTranscriptionIntegration**: Tests end-to-end transcription flow

#### Utils Module Tests (`test_utils.py`)
- **TestErrorHandler**: Tests error handling utilities
  - Error message formatting
  - Safe execution wrappers
  - Module-specific error handling
- **TestAudioFileManager**: Tests file management utilities
  - Temporary file creation and cleanup
  - Audio file validation
  - Directory management
- **TestTempFileContext**: Tests context manager for temporary files
- **TestUtilsIntegration**: Tests utility integration scenarios

#### UI Module Tests (`test_ui.py`)
- **TestUIComponents**: Tests Streamlit UI components
  - Header and layout rendering
  - Settings sidebar
  - Recording interface
  - Results display
  - Error and success messages
- **TestUIComponentsIntegration**: Tests complete UI workflows

#### Config Module Tests (`test_config.py`)
- **TestLanguageOptions**: Tests language configuration
- **TestAudioSettings**: Tests audio recording settings
- **TestWhisperSettings**: Tests Whisper model settings
- **TestUISettings**: Tests UI configuration
- **TestFileSettings**: Tests file management settings
- **TestErrorMessages**: Tests error message constants
- **TestSuccessMessages**: Tests success message constants
- **TestAccuracyTips**: Tests accuracy improvement tips
- **TestTroubleshootingTips**: Tests troubleshooting guidance
- **TestConfigIntegration**: Tests configuration consistency

## Running Tests

### Prerequisites

```bash
pip install -r requirements.txt
pip install pytest pytest-cov
```

### Running All Tests

```bash
# Using the test runner
python tests/test_runner.py

# Using pytest
pytest tests/

# Using unittest
python -m unittest discover tests/
```

### Running Specific Test Categories

```bash
# Run only audio tests
python tests/test_runner.py --category audio
pytest tests/ -m audio

# Run only transcription tests
python tests/test_runner.py --category transcription
pytest tests/ -m transcription

# Run only utils tests
python tests/test_runner.py --category utils
pytest tests/ -m utils

# Run only UI tests
python tests/test_runner.py --category ui
pytest tests/ -m ui

# Run only config tests
python tests/test_runner.py --category config
pytest tests/ -m config
```

### Running with Coverage

```bash
# Generate coverage report
pytest tests/ --cov=src --cov-report=html --cov-report=term

# View coverage report
open htmlcov/index.html
```

### Running with Detailed Report

```bash
python tests/test_runner.py --report
```

## Test Fixtures

The `conftest.py` file provides shared fixtures for all tests:

- **`temp_audio_file`**: Creates temporary audio files for testing
- **`sample_audio_data`**: Provides sample audio data
- **`mock_streamlit`**: Mocks Streamlit components for UI testing
- **`mock_whisper`**: Mocks Whisper model for transcription testing
- **`mock_sounddevice`**: Mocks audio device operations
- **`mock_scipy`**: Mocks audio processing operations
- **`mock_wavfile`**: Mocks file I/O operations
- **`test_config`**: Provides test configuration values
- **`error_handler`**: Provides error handler instance
- **`audio_file_manager`**: Provides file manager instance
- **`ui_components`**: Provides UI components instance

## Test Markers

Tests are automatically categorized using pytest markers:

- `@pytest.mark.audio` - Audio module tests
- `@pytest.mark.transcription` - Transcription module tests
- `@pytest.mark.utils` - Utils module tests
- `@pytest.mark.ui` - UI module tests
- `@pytest.mark.config` - Config module tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.unit` - Unit tests

## Test Coverage

The test suite provides comprehensive coverage of:

### Functionality Coverage
- ✅ Audio recording and device management
- ✅ Audio preprocessing and enhancement
- ✅ Whisper model integration
- ✅ Transcription workflow
- ✅ Error handling and recovery
- ✅ File management and cleanup
- ✅ UI component rendering
- ✅ Configuration validation

### Edge Cases Coverage
- ✅ Invalid audio data
- ✅ Missing audio devices
- ✅ Model loading failures
- ✅ File I/O errors
- ✅ Network connectivity issues
- ✅ Invalid user inputs
- ✅ Resource cleanup

### Integration Coverage
- ✅ End-to-end audio processing
- ✅ UI workflow integration
- ✅ Error handling integration
- ✅ Configuration consistency

## Test Output

### Standard Output
```
test_audio.py::TestAudioRecorder::test_get_audio_devices PASSED
test_audio.py::TestAudioRecorder::test_record_audio PASSED
...
```

### Detailed Report
```
============================================================
VOICE-TO-VOICE AI ASSISTANT - TEST REPORT
============================================================

SUMMARY:
  Tests run: 150
  Failures: 0
  Errors: 0
  Skipped: 0

SUCCESS RATE: 100.0%

TEST COVERAGE BY MODULE:
  Audio: 3 test classes
  Transcription: 3 test classes
  Utils: 4 test classes
  UI: 2 test classes
  Config: 10 test classes
============================================================
```

## Continuous Integration

The test suite is designed to run in CI/CD environments:

```yaml
# Example GitHub Actions workflow
- name: Run Tests
  run: |
    python tests/test_runner.py --report
    pytest tests/ --cov=src --cov-report=xml
```

## Adding New Tests

### For New Features
1. Create test class in appropriate test file
2. Follow naming convention: `Test[ClassName]`
3. Use descriptive test method names
4. Include both positive and negative test cases
5. Add appropriate markers

### Example Test Structure
```python
class TestNewFeature(unittest.TestCase):
    """Test cases for NewFeature class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.feature = NewFeature()
    
    def test_feature_basic_functionality(self):
        """Test basic functionality."""
        result = self.feature.do_something()
        self.assertIsNotNone(result)
    
    def test_feature_error_handling(self):
        """Test error handling."""
        with self.assertRaises(ValueError):
            self.feature.do_something_invalid()
```

## Best Practices

1. **Isolation**: Each test should be independent
2. **Mocking**: Use mocks for external dependencies
3. **Cleanup**: Always clean up resources after tests
4. **Descriptive Names**: Use clear, descriptive test names
5. **Documentation**: Include docstrings for test classes and methods
6. **Coverage**: Aim for high test coverage
7. **Performance**: Keep tests fast and efficient

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure `src` directory is in Python path
2. **Mock Issues**: Check that mocks are properly configured
3. **File Permission Errors**: Ensure proper cleanup in tests
4. **Resource Leaks**: Use context managers for file operations

### Debug Mode
```bash
# Run with verbose output
python tests/test_runner.py --verbose

# Run single test
pytest tests/test_audio.py::TestAudioRecorder::test_record_audio -v

# Run with debugger
python -m pdb tests/test_runner.py
```

## Performance

- **Test Execution Time**: ~30 seconds for full suite
- **Memory Usage**: Minimal, uses mocks for heavy operations
- **Parallel Execution**: Tests can run in parallel (use `pytest-xdist`)

## Maintenance

- Update tests when adding new features
- Review test coverage regularly
- Refactor tests for better maintainability
- Keep test data and fixtures up to date 