"""
Refactored main application for the Voice-to-Voice AI Assistant.
Uses the new modular structure for better maintainability.
Now supports environment variable configuration.
"""

import streamlit as st
from typing import Optional

# Import our modular components
from src.config.constants import AUDIO_SETTINGS, UI_SETTINGS
from src.config.config_validator import ConfigValidator
from src.audio.recorder import AudioRecorder
from src.audio.preprocessor import AudioPreprocessor
from src.transcription.whisper_client import TranscriptionManager
from src.ui.components import UIComponents
from src.ui.crisis_components import CrisisComponents
from src.services.openai_service import OpenAIService
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
    
    # Initialize OpenAI service
    openai_service = OpenAIService()
    
    return audio_recorder, audio_preprocessor, transcription_manager, openai_service

def main():
    """Main application function."""
    # Initialize components
    audio_recorder, audio_preprocessor, transcription_manager, openai_service = initialize_components()
    
    # Render crisis-focused header
    st.title("🚨 Emergency Crisis Response")
    st.markdown("*Voice-activated emergency assistance. Speak clearly and I'll help immediately.*")
    st.markdown("---")
    
    # Display API status in sidebar
    CrisisComponents.render_api_status()
    
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
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Speech Input Section
        st.markdown("#### 🎤 Speak Your Emergency")
        
        if st.button("🎤 Start Recording", type="primary", use_container_width=True):
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
                    with st.spinner("Transcribing your message..."):
                        transcribed_text = transcription_manager.transcribe_with_settings(
                            temp_audio_file,
                            language_name=selected_language
                        )
                    
                    # Clean up temporary file
                    AudioFileManager.cleanup_temp_file(temp_audio_file)
                    
                    if transcribed_text:
                        st.success("✅ Message transcribed!")
                        st.session_state.transcribed_text = transcribed_text
                        st.session_state.audio_processed = True
                        
                        # Always generate crisis response (since this is crisis mode)
                        st.session_state.crisis_detected = True
                        st.session_state.crisis_text = transcribed_text
                    else:
                        st.error("❌ Failed to transcribe audio")
                else:
                    st.error("❌ Failed to save audio file")
            else:
                st.error("❌ Failed to record audio")
    
    with col2:
        # Crisis Response Section
        st.markdown("#### 🤖 AI Response")
        
        # Show conversation history
        if 'conversation_history' not in st.session_state:
            st.session_state.conversation_history = []
        
        # Display conversation
        for i, (user_msg, ai_msg) in enumerate(st.session_state.conversation_history):
            st.markdown(f"**You:** {user_msg}")
            st.markdown(f"**AI:** {ai_msg}")
            st.markdown("---")
        
        # Handle new crisis response
        if st.session_state.get('crisis_detected', False):
            crisis_text = st.session_state.get('crisis_text', '')
            if crisis_text:
                # Convert conversation history to API format
                conversation_history = []
                for user_msg, ai_msg in st.session_state.conversation_history:
                    conversation_history.append({"role": "user", "content": user_msg})
                    conversation_history.append({"role": "assistant", "content": ai_msg})
                
                with st.spinner("Generating emergency response..."):
                    ai_response = openai_service.generate_crisis_response(crisis_text, conversation_history)
                
                # Add to conversation history
                st.session_state.conversation_history.append((crisis_text, ai_response))
                
                # Clear crisis state
                st.session_state.crisis_detected = False
                st.session_state.crisis_text = ""
                
                # Rerun to show updated conversation
                st.rerun()
    
    # Emergency Controls
    st.markdown("---")
    col_emergency1, col_emergency2, col_emergency3 = st.columns([1, 2, 1])
    
    with col_emergency2:
        if st.button("📞 CALL 911", type="secondary", use_container_width=True):
            st.error("🚨 EMERGENCY: 911 would be called here")
            st.info("In production, this would trigger emergency services")
        
        # Reset conversation for testing
        if st.button("🔄 Reset Conversation", type="secondary", use_container_width=True):
            st.session_state.conversation_history = []
            st.rerun()
    
    # Footer
    UIComponents.render_footer()

if __name__ == "__main__":
    main() 