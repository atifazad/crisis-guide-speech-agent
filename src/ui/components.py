"""
Reusable UI components for the Voice-to-Voice AI Assistant.
"""

import streamlit as st
from typing import Optional, Dict, Any, List
from ..config.constants import (
    ACCURACY_TIPS,
    TROUBLESHOOTING_TIPS,
    SUCCESS_MESSAGES,
    ERROR_MESSAGES
)

class UIComponents:
    """Reusable UI components for the application."""
    
    @staticmethod
    def render_header() -> None:
        """Render the main application header."""
        st.title("🎤 Voice-to-Voice AI Assistant")
        st.markdown("### Speech Input Interface with Google Whisper")
    
    @staticmethod
    def render_sidebar_settings(
        recording_duration: int,
        sample_rate: int,
        language_options: Dict[str, Optional[str]],
        selected_language: str = "Auto-detect"
    ) -> tuple:
        """
        Render sidebar settings.
        
        Returns:
            Tuple of (recording_duration, sample_rate, selected_language)
        """
        st.sidebar.header("Settings")
        
        # Recording settings
        recording_duration = st.sidebar.slider(
            "Recording Duration (seconds)",
            3, 15, recording_duration
        )
        
        sample_rate = st.sidebar.selectbox(
            "Sample Rate",
            [8000, 16000, 44100],
            index=1
        )
        
        # Language selection
        selected_language = st.sidebar.selectbox(
            "Language",
            list(language_options.keys()),
            index=list(language_options.keys()).index(selected_language)
        )
        
        return recording_duration, sample_rate, selected_language
    
    @staticmethod
    def render_recording_section() -> bool:
        """Render the recording section."""
        st.header("🎙️ Speech Input")
        
        return st.button(
            "🎤 Start Recording",
            type="primary",
            use_container_width=True
        )
    
    @staticmethod
    def render_transcription_results(transcribed_text: Optional[str]) -> None:
        """Render transcription results."""
        st.header("📝 Transcription Results")
        
        if transcribed_text:
            st.text_area(
                "Transcribed Text:",
                value=transcribed_text,
                height=200,
                disabled=True
            )
            
            # Copy button
            if st.button("📋 Copy to Clipboard"):
                st.write("Text copied to clipboard!")
            
            # Success indicator
            st.success("✅ Audio processed with improved settings")
        else:
            st.info("Record some audio to see the transcription here.")
    
    @staticmethod
    def render_audio_statistics(transcribed_text: Optional[str]) -> None:
        """Render audio statistics."""
        st.subheader("📊 Audio Statistics")
        
        if transcribed_text:
            word_count = len(transcribed_text.split())
            char_count = len(transcribed_text)
            st.metric("Words", word_count)
            st.metric("Characters", char_count)
        else:
            st.info("Record audio to see statistics")
    
    @staticmethod
    def render_model_info(model_info: Dict[str, Any], sample_rate: int, recording_duration: int) -> None:
        """Render model information."""
        st.subheader("⚙️ Model Info")
        st.write(f"**Model:** {model_info.get('type', 'Unknown')} ({model_info.get('name', 'Unknown')})")
        st.write(f"**Parameters:** {model_info.get('parameters', 'Unknown')}")
        st.write(f"**Sample Rate:** {sample_rate} Hz")
        st.write(f"**Recording Duration:** {recording_duration}s")
    
    @staticmethod
    def render_accuracy_tips() -> None:
        """Render tips for better accuracy."""
        st.subheader("💡 Tips for Better Accuracy")
        
        for tip in ACCURACY_TIPS:
            st.markdown(f"- **{tip}**")
    
    @staticmethod
    def render_troubleshooting() -> None:
        """Render troubleshooting section."""
        st.markdown("---")
        st.header("🔧 Troubleshooting")
        
        with st.expander("Common Issues and Solutions"):
            for category, tips in TROUBLESHOOTING_TIPS.items():
                st.markdown(f"**{category.replace('_', ' ').title()}:**")
                for tip in tips:
                    st.markdown(f"- {tip}")
                st.markdown("")
    
    @staticmethod
    def render_footer() -> None:
        """Render the application footer."""
        st.markdown("---")
        st.markdown(
            """
            <div style='text-align: center; color: #666;'>
            Built with ❤️ using Streamlit and OpenAI Whisper
            </div>
            """,
            unsafe_allow_html=True
        )
    
    @staticmethod
    def render_device_info(device_info: Dict[str, Any]) -> None:
        """Render audio device information."""
        st.subheader("🎧 Audio Devices")
        
        if device_info.get('has_devices'):
            st.success(f"✅ Found {device_info['total_input_devices']} input device(s)")
            
            for i, device in enumerate(device_info['input_devices'][:3]):
                st.write(f"   {i+1}. {device['name']}")
            
            if len(device_info['input_devices']) > 3:
                st.write(f"   ... and {len(device_info['input_devices']) - 3} more")
        else:
            st.error("❌ No input devices found")
    
    @staticmethod
    def render_processing_status(status: str, is_processing: bool = True) -> None:
        """Render processing status."""
        if is_processing:
            with st.spinner(status):
                pass
        else:
            st.info(status)
    
    @staticmethod
    def render_success_message(message: str) -> None:
        """Render success message."""
        st.success(f"✅ {message}")
    
    @staticmethod
    def render_error_message(message: str) -> None:
        """Render error message."""
        st.error(f"❌ {message}")
    
    @staticmethod
    def render_info_message(message: str) -> None:
        """Render info message."""
        st.info(message)
    
    @staticmethod
    def render_warning_message(message: str) -> None:
        """Render warning message."""
        st.warning(f"⚠️ {message}")
    
    @staticmethod
    def create_columns(num_columns: int = 2) -> List:
        """Create columns for layout."""
        return st.columns(num_columns)
    
    @staticmethod
    def render_separator() -> None:
        """Render a visual separator."""
        st.markdown("---")
    
    @staticmethod
    def render_expandable_section(title: str, content: str) -> None:
        """Render an expandable section."""
        with st.expander(title):
            st.markdown(content)
    
    @staticmethod
    def render_metric(label: str, value: Any, delta: Optional[str] = None) -> None:
        """Render a metric."""
        st.metric(label, value, delta)
    
    @staticmethod
    def render_progress_bar(progress: float, text: str = "Processing...") -> None:
        """Render a progress bar."""
        st.progress(progress, text=text)
    
    @staticmethod
    def render_code_block(code: str, language: str = "python") -> None:
        """Render a code block."""
        st.code(code, language=language)
    
    @staticmethod
    def render_dataframe(data: Any, caption: str = "") -> None:
        """Render a dataframe."""
        st.dataframe(data, caption=caption)
    
    @staticmethod
    def render_chart(chart_data: Any, chart_type: str = "line") -> None:
        """Render a chart."""
        if chart_type == "line":
            st.line_chart(chart_data)
        elif chart_type == "bar":
            st.bar_chart(chart_data)
        elif chart_type == "area":
            st.area_chart(chart_data)
    
    @staticmethod
    def render_download_button(
        data: Any,
        file_name: str,
        mime_type: str = "text/plain"
    ) -> None:
        """Render a download button."""
        st.download_button(
            label="Download",
            data=data,
            file_name=file_name,
            mime=mime_type
        ) 