"""
Refactored main application for the Voice-to-Voice AI Assistant.
Uses the new modular structure for better maintainability.
"""

import streamlit as st
from typing import Optional

# Import our modular components
from src.config.constants import AUDIO_SETTINGS, UI_SETTINGS
from src.audio.recorder import AudioRecorder
from src.audio.preprocessor import AudioPreprocessor
from src.transcription.whisper_client import TranscriptionManager
from src.ui.components import UIComponents
from src.utils.file_utils import AudioFileManager
from src.utils.error_handler import ErrorHandler

# Page configuration
st.set_page_config(
    page_title=UI_SETTINGS["PAGE_TITLE"],
    page_icon=UI_SETTINGS["PAGE_ICON"],
    layout=UI_SETTINGS["LAYOUT"]
)

def initialize_components():
    """Initialize all application components."""
    # Initialize audio components
    audio_recorder = AudioRecorder()
    audio_preprocessor = AudioPreprocessor()
    
    # Initialize transcription component
    transcription_manager = TranscriptionManager()
    
    return audio_recorder, audio_preprocessor, transcription_manager

def main():
    """Main application function."""
    # Initialize components
    audio_recorder, audio_preprocessor, transcription_manager = initialize_components()
    
    # Render header
    UIComponents.render_header()
    
    # Get device information
    device_info = audio_recorder.get_device_info()
    
    # Render sidebar settings
    recording_duration, sample_rate, selected_language = UIComponents.render_sidebar_settings(
        recording_duration=AUDIO_SETTINGS["DEFAULT_RECORDING_DURATION"],
        sample_rate=AUDIO_SETTINGS["DEFAULT_SAMPLE_RATE"],
        language_options=transcription_manager.get_language_options(),
        selected_language="Auto-detect"
    )
    
    # Validate recording settings
    if not audio_recorder.validate_recording_settings(recording_duration, sample_rate):
        st.stop()
    
    # Main content area
    col1, col2 = UIComponents.create_columns(2)
    
    with col1:
        # Recording section
        if UIComponents.render_recording_section():
            # Record audio
            audio_data = audio_recorder.record_audio(
                duration=recording_duration,
                sample_rate=sample_rate
            )
            
            if audio_data is not None:
                # Preprocess audio
                processed_audio, processed_sample_rate = audio_preprocessor.preprocess_audio(
                    audio_data, sample_rate
                )
                
                # Save audio to temporary file
                temp_audio_file = AudioFileManager.save_audio_to_temp(
                    processed_audio, processed_sample_rate
                )
                
                if temp_audio_file:
                    # Transcribe audio
                    UIComponents.render_processing_status("Transcribing audio...")
                    transcribed_text = transcription_manager.transcribe_with_settings(
                        temp_audio_file,
                        language_name=selected_language
                    )
                    
                    # Clean up temporary file
                    AudioFileManager.cleanup_temp_file(temp_audio_file)
                    
                    if transcribed_text:
                        UIComponents.render_success_message("Audio transcribed successfully!")
                        st.session_state.transcribed_text = transcribed_text
                        st.session_state.audio_processed = True
                    else:
                        UIComponents.render_error_message("Failed to transcribe audio")
                else:
                    UIComponents.render_error_message("Failed to save audio file")
            else:
                UIComponents.render_error_message("Failed to record audio")
    
    with col2:
        # Transcription results
        transcribed_text = st.session_state.get('transcribed_text', None)
        UIComponents.render_transcription_results(transcribed_text)
    
    # Additional features section
    UIComponents.render_separator()
    st.header("🔧 Additional Features")
    
    col3, col4, col5 = UIComponents.create_columns(3)
    
    with col3:
        # Audio statistics
        UIComponents.render_audio_statistics(transcribed_text)
    
    with col4:
        # Model information
        model_info = transcription_manager.get_model_info()
        UIComponents.render_model_info(model_info, sample_rate, recording_duration)
    
    with col5:
        # Accuracy tips
        UIComponents.render_accuracy_tips()
    
    # Troubleshooting section
    UIComponents.render_troubleshooting()
    
    # Footer
    UIComponents.render_footer()

if __name__ == "__main__":
    main() 