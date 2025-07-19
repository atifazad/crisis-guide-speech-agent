"""
Constants and configuration values for the Voice-to-Voice AI Assistant.
"""

# Language options for transcription
LANGUAGE_OPTIONS = {
    "Auto-detect": None,
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese": "zh"
}

# Audio recording settings
AUDIO_SETTINGS = {
    "DEFAULT_SAMPLE_RATE": 16000,
    "DEFAULT_RECORDING_DURATION": 5,
    "SUPPORTED_SAMPLE_RATES": [8000, 16000, 44100],
    "MIN_RECORDING_DURATION": 3,
    "MAX_RECORDING_DURATION": 15,
    "AUDIO_CHANNELS": 1,
    "AUDIO_DTYPE": "float32"
}

# Whisper model settings
WHISPER_SETTINGS = {
    "DEFAULT_MODEL": "small",
    "AVAILABLE_MODELS": ["tiny", "base", "small", "medium", "large"],
    "MODEL_CACHE_DIR": "data/models",
    "FP16_ENABLED": False,  # Use FP32 for better CPU compatibility
    "VERBOSE": False
}

# UI settings
UI_SETTINGS = {
    "PAGE_TITLE": "Voice-to-Voice AI Assistant",
    "PAGE_ICON": "🎤",
    "LAYOUT": "wide",
    "SIDEBAR_TITLE": "Settings",
    "MAIN_TITLE": "🎤 Voice-to-Voice AI Assistant",
    "SUBTITLE": "Speech Input Interface with Google Whisper"
}

# File settings
FILE_SETTINGS = {
    "TEMP_AUDIO_SUFFIX": ".wav",
    "TEMP_AUDIO_PREFIX": "temp_audio_",
    "DELETE_TEMP_FILES": True
}

# Error messages
ERROR_MESSAGES = {
    "AUDIO_RECORDING_FAILED": "Failed to record audio",
    "AUDIO_SAVE_FAILED": "Failed to save audio file",
    "TRANSCRIPTION_FAILED": "Failed to transcribe audio",
    "MODEL_LOAD_FAILED": "Failed to load Whisper model",
    "DEVICE_NOT_FOUND": "No audio input devices found",
    "PREPROCESSING_FAILED": "Failed to preprocess audio"
}

# Success messages
SUCCESS_MESSAGES = {
    "AUDIO_RECORDED": "Audio recorded successfully",
    "AUDIO_TRANSCRIBED": "Audio transcribed successfully",
    "MODEL_LOADED": "Whisper model loaded successfully",
    "AUDIO_PROCESSED": "Audio processed with improved settings"
}

# Tips for better accuracy
ACCURACY_TIPS = [
    "Speak clearly and at a normal pace",
    "Minimize background noise",
    "Keep the microphone close to your mouth",
    "Use quiet environment",
    "Select correct language in settings",
    "Speak for full duration of recording"
]

# Troubleshooting tips
TROUBLESHOOTING_TIPS = {
    "POOR_QUALITY": [
        "Ensure microphone permissions are granted",
        "Check that microphone is working in other apps",
        "Try speaking louder and more clearly",
        "Reduce background noise"
    ],
    "NO_AUDIO": [
        "Check microphone connection",
        "Verify browser microphone permissions",
        "Try refreshing the page"
    ],
    "MODEL_ISSUES": [
        "Ensure stable internet connection",
        "Check available disk space",
        "Restart the application"
    ]
} 