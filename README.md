# Voice-to-Voice AI Assistant

A modern, web-based voice-to-voice AI assistant built with Python, featuring real-time speech input and Google Whisper integration for accurate speech-to-text conversion.

## 🚀 Features

- **Real-time Speech Input**: Record audio directly through your browser
- **Google Whisper Integration**: High-quality speech-to-text conversion
- **Modern Web Interface**: Built with Streamlit for a beautiful, responsive UI
- **Customizable Settings**: Adjust recording duration and sample rate
- **Audio Statistics**: Word and character count for transcribed text
- **Cross-platform**: Works on Windows, macOS, and Linux

## 🛠️ Technology Stack

- **Python 3.8+**
- **Streamlit**: Web interface framework
- **OpenAI Whisper**: Speech-to-text conversion
- **SoundDevice**: Audio recording and playback
- **NumPy & SciPy**: Audio processing
- **PyAudio**: Audio I/O operations

## 📋 Prerequisites

- Python 3.8 or higher
- Microphone access
- Internet connection (for initial Whisper model download)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd crisis-guide-speech-agent
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
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
   - Click the "🎤 Start Recording" button
   - Speak clearly into your microphone
   - Wait for the transcription to complete
   - View the transcribed text in the results panel

## ⚙️ Configuration

### Recording Settings (Sidebar)
- **Recording Duration**: 3-15 seconds (default: 5)
- **Sample Rate**: 8000, 16000, or 44100 Hz (default: 16000)

### Whisper Model
- Currently using the "base" model for optimal performance
- Models are cached for faster subsequent loads

## 📁 Project Structure

```
crisis-guide-speech-agent/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
└── .gitignore         # Git ignore file
```

## 🔧 Troubleshooting

### Common Issues

1. **Audio recording not working**
   - Ensure microphone permissions are granted
   - Check if microphone is properly connected
   - Try refreshing the browser page

2. **Whisper model download issues**
   - Ensure stable internet connection
   - The model downloads automatically on first use
   - Check available disk space

3. **PyAudio installation issues (Windows)**
   ```bash
   pip install pipwin
   pipwin install pyaudio
   ```

4. **PyAudio installation issues (macOS)**
   ```bash
   brew install portaudio
   pip install pyaudio
   ```

### Performance Tips

- Use a quiet environment for better transcription accuracy
- Speak clearly and at a normal pace
- Keep the microphone close to your mouth
- Higher sample rates provide better quality but use more resources

## 🎯 Next Steps

This MVP provides the foundation for a voice-to-voice AI assistant. Future enhancements could include:

- **Text-to-Speech**: Convert AI responses back to speech
- **AI Integration**: Connect to language models for intelligent responses
- **Real-time Processing**: Stream audio for continuous conversation
- **Multi-language Support**: Support for multiple languages
- **Voice Activity Detection**: Automatic start/stop recording
- **Audio Visualization**: Real-time audio waveform display

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