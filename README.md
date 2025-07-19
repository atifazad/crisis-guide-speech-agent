# Voice-to-Voice AI Assistant

A modern, modular voice-to-voice AI assistant built with Python, featuring real-time speech input, advanced audio preprocessing, and Google Whisper integration for accurate speech-to-text conversion.

## 🚀 Features

- **Real-time Speech Input**: Record audio directly through your browser
- **Advanced Audio Preprocessing**: Professional audio cleaning and normalization
- **Google Whisper Integration**: High-quality speech-to-text conversion with multiple model options
- **Multi-language Support**: Support for 10+ languages with auto-detection
- **Modern Web Interface**: Built with Streamlit for a beautiful, responsive UI
- **Modular Architecture**: Clean, maintainable code structure
- **Customizable Settings**: Adjustable recording duration, sample rate, and language
- **Audio Statistics**: Word and character count for transcribed text
- **Cross-platform**: Works on Windows, macOS, and Linux

## 🛠️ Technology Stack

- **Python 3.8+**
- **Streamlit**: Web interface framework
- **OpenAI Whisper**: Speech-to-text conversion with multiple model sizes
- **SoundDevice**: Audio recording and playback
- **Librosa**: Professional audio processing and preprocessing
- **NumPy & SciPy**: Audio processing and numerical operations
- **PyAudio**: Audio I/O operations

## 📋 Prerequisites

- Python 3.8 or higher
- Microphone access
- Internet connection (for initial Whisper model download)
- FFmpeg (for audio processing)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd crisis-guide-speech-agent
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   # Using uv (recommended)
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   
   # Or using standard Python
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install system dependencies**
   ```bash
   # macOS
   brew install portaudio ffmpeg
   
   # Ubuntu/Debian
   sudo apt-get install portaudio19-dev ffmpeg
   
   # Windows
   # Download and install FFmpeg from https://ffmpeg.org/download.html
   ```

4. **Install Python dependencies**
   ```bash
   # Using uv
   uv pip install -r requirements.txt
   
   # Or using pip
   pip install -r requirements.txt
   ```

## 🎯 Usage

1. **Start the application**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If it doesn't open automatically, navigate to the URL manually

3. **Using the interface**
   - Adjust settings in the sidebar (recording duration, sample rate, language)
   - Click "🎤 Start Recording" to begin audio capture
   - Speak clearly into your microphone
   - View transcribed text in real-time
   - Use the copy button to copy transcribed text

## ⚙️ Configuration

### Recording Settings (Sidebar)
- **Recording Duration**: 3-15 seconds (default: 5)
- **Sample Rate**: 8000, 16000, or 44100 Hz (default: 16000)
- **Language**: Auto-detect or select from 10+ languages

### Whisper Model
- **Default Model**: "small" (244M parameters) for optimal accuracy
- **Available Models**: tiny, base, small, medium, large
- **Models are cached** for faster subsequent loads


## 🔧 Troubleshooting

### Common Issues

1. **Audio recording not working**
   - Ensure microphone permissions are granted
   - Check if microphone is properly connected
   - Try refreshing the browser page
   - Verify system audio settings

2. **Whisper model download issues**
   - Ensure stable internet connection
   - The model downloads automatically on first use
   - Check available disk space (models can be 1GB+)

3. **FFmpeg not found error**
   ```bash
   # macOS
   brew install ffmpeg
   
   # Ubuntu/Debian
   sudo apt-get install ffmpeg
   
   # Windows
   # Download from https://ffmpeg.org/download.html
   ```

4. **PyAudio installation issues (Windows)**
   ```bash
   pip install pipwin
   pipwin install pyaudio
   ```

5. **PyAudio installation issues (macOS)**
   ```bash
   brew install portaudio
   pip install pyaudio
   ```

### Performance Tips

- Use a quiet environment for better transcription accuracy
- Speak clearly and at a normal pace
- Keep the microphone close to your mouth
- Higher sample rates provide better quality but use more resources
- The "small" model provides good balance of accuracy and speed

## 🎯 Next Steps

This MVP provides the foundation for a voice-to-voice AI assistant. Future enhancements could include:

- **Text-to-Speech**: Convert AI responses back to speech
- **AI Integration**: Connect to language models for intelligent responses
- **Real-time Processing**: Stream audio for continuous conversation
- **Voice Activity Detection**: Automatic start/stop recording
- **Audio Visualization**: Real-time audio waveform display
- **Advanced Audio Processing**: Noise cancellation, echo removal
- **Multi-user Support**: Handle multiple simultaneous users
- **API Integration**: RESTful API for external applications

## 🧪 Testing

Run the setup verification script to ensure everything is working:

```bash
python test_setup.py
```

This will test:
- Package imports
- Whisper model loading
- Audio device detection

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for the Whisper model
- Streamlit for the web framework
- The open-source community for audio processing libraries
- Contributors and users of this project

## 📊 Performance Metrics

- **Transcription Accuracy**: Improved with audio preprocessing
- **Processing Speed**: Optimized with modular architecture
- **Memory Usage**: Efficient with proper cleanup
- **User Experience**: Enhanced with better error handling and feedback 