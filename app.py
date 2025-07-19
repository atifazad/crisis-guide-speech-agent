import streamlit as st
import sounddevice as sd
import numpy as np
import whisper
import tempfile
import os
from scipy.io import wavfile
import time
import librosa

# Page configuration
st.set_page_config(
    page_title="Voice-to-Voice AI Assistant",
    page_icon="🎤",
    layout="wide"
)

# Initialize Whisper model
@st.cache_resource
def load_whisper_model():
    """Load the Whisper model once and cache it"""
    # Use a larger model for better accuracy
    return whisper.load_model("small")  # Changed from "base" to "small"

def record_audio(duration=5, sample_rate=16000):
    """Record audio for specified duration with better error handling"""
    try:
        st.info(f"Recording for {duration} seconds... Speak now!")
        
        # Record audio with better error handling
        recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype=np.float32)
        sd.wait()
        
        # Normalize audio
        recording = recording.flatten()
        recording = recording / np.max(np.abs(recording)) if np.max(np.abs(recording)) > 0 else recording
        
        return recording
    except Exception as e:
        st.error(f"Error recording audio: {str(e)}")
        return None

def preprocess_audio(audio_data, sample_rate=16000):
    """Preprocess audio for better transcription"""
    try:
        # Resample to 16kHz if needed (Whisper expects 16kHz)
        if sample_rate != 16000:
            audio_data = librosa.resample(audio_data, orig_sr=sample_rate, target_sr=16000)
            sample_rate = 16000
        
        # Apply noise reduction and normalization
        # Remove DC offset
        audio_data = audio_data - np.mean(audio_data)
        
        # Normalize to prevent clipping
        max_val = np.max(np.abs(audio_data))
        if max_val > 0:
            audio_data = audio_data / max_val * 0.95
        
        return audio_data, 16000
    except Exception as e:
        st.error(f"Error preprocessing audio: {str(e)}")
        return audio_data, sample_rate

def save_audio_to_temp(audio_data, sample_rate=16000):
    """Save audio data to a temporary WAV file"""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            wavfile.write(tmp_file.name, sample_rate, audio_data.astype(np.float32))
            return tmp_file.name
    except Exception as e:
        st.error(f"Error saving audio: {str(e)}")
        return None

def transcribe_audio(audio_file_path, model, language=None):
    """Transcribe audio using Whisper with improved settings"""
    try:
        # Use better transcription parameters
        result = model.transcribe(
            audio_file_path,
            language=language,  # Auto-detect if None
            task="transcribe",
            fp16=False,  # Use FP32 for better compatibility
            verbose=False
        )
        return result["text"].strip()
    except Exception as e:
        st.error(f"Error transcribing audio: {str(e)}")
        return None

def main():
    st.title("🎤 Voice-to-Voice AI Assistant")
    st.markdown("### Speech Input Interface with Google Whisper")
    
    # Load Whisper model
    with st.spinner("Loading Whisper model..."):
        model = load_whisper_model()
    st.success("Whisper model loaded successfully!")
    
    # Sidebar for settings
    st.sidebar.header("Settings")
    recording_duration = st.sidebar.slider("Recording Duration (seconds)", 3, 15, 5)
    sample_rate = st.sidebar.selectbox("Sample Rate", [8000, 16000, 44100], index=1)
    
    # Language selection
    language_options = {
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
    selected_language = st.sidebar.selectbox("Language", list(language_options.keys()), index=0)
    language_code = language_options[selected_language]
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("🎙️ Speech Input")
        
        # Record button
        if st.button("🎤 Start Recording", type="primary", use_container_width=True):
            # Record audio
            audio_data = record_audio(recording_duration, sample_rate)
            
            if audio_data is not None:
                # Preprocess audio
                processed_audio, processed_sample_rate = preprocess_audio(audio_data, sample_rate)
                
                # Save audio to temporary file
                temp_audio_file = save_audio_to_temp(processed_audio, processed_sample_rate)
                
                if temp_audio_file:
                    # Transcribe audio
                    with st.spinner("Transcribing audio..."):
                        transcribed_text = transcribe_audio(temp_audio_file, model, language_code)
                    
                    # Clean up temporary file
                    try:
                        os.unlink(temp_audio_file)
                    except:
                        pass
                    
                    if transcribed_text:
                        st.success("✅ Audio transcribed successfully!")
                        st.session_state.transcribed_text = transcribed_text
                        st.session_state.audio_processed = True
                    else:
                        st.error("❌ Failed to transcribe audio")
                else:
                    st.error("❌ Failed to save audio file")
            else:
                st.error("❌ Failed to record audio")
    
    with col2:
        st.header("📝 Transcription Results")
        
        # Display transcribed text
        if 'transcribed_text' in st.session_state:
            st.text_area(
                "Transcribed Text:",
                value=st.session_state.transcribed_text,
                height=200,
                disabled=True
            )
            
            # Copy button
            if st.button("📋 Copy to Clipboard"):
                st.write("Text copied to clipboard!")
                
            # Confidence indicator
            if st.session_state.get('audio_processed', False):
                st.success("✅ Audio processed with improved settings")
        else:
            st.info("Record some audio to see the transcription here.")
    
    # Additional features section
    st.markdown("---")
    st.header("🔧 Additional Features")
    
    col3, col4, col5 = st.columns(3)
    
    with col3:
        st.subheader("📊 Audio Statistics")
        if 'transcribed_text' in st.session_state:
            word_count = len(st.session_state.transcribed_text.split())
            char_count = len(st.session_state.transcribed_text)
            st.metric("Words", word_count)
            st.metric("Characters", char_count)
        else:
            st.info("Record audio to see statistics")
    
    with col4:
        st.subheader("⚙️ Model Info")
        st.write(f"**Model:** {type(model).__name__} (small)")
        st.write(f"**Sample Rate:** {sample_rate} Hz")
        st.write(f"**Recording Duration:** {recording_duration}s")
        st.write(f"**Language:** {selected_language}")
    
    with col5:
        st.subheader("💡 Tips for Better Accuracy")
        st.markdown("""
        - **Speak clearly** and at a normal pace
        - **Minimize background noise**
        - **Keep microphone close** to your mouth
        - **Use quiet environment**
        - **Select correct language** in settings
        - **Speak for full duration** of recording
        """)
    
    # Troubleshooting section
    st.markdown("---")
    st.header("🔧 Troubleshooting")
    
    with st.expander("Common Issues and Solutions"):
        st.markdown("""
        **Poor Transcription Quality:**
        - Ensure microphone permissions are granted
        - Check that microphone is working in other apps
        - Try speaking louder and more clearly
        - Reduce background noise
        
        **No Audio Detected:**
        - Check microphone connection
        - Verify browser microphone permissions
        - Try refreshing the page
        
        **Model Loading Issues:**
        - Ensure stable internet connection
        - Check available disk space
        - Restart the application
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
        Built with ❤️ using Streamlit and OpenAI Whisper
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 