"""
Crisis-specific UI components for the Voice-to-Voice AI Assistant.
Provides immediate crisis response interface with minimal complexity.
"""

import streamlit as st
from typing import Optional, Dict, Any
from src.config.openai_config import get_openai_api_key, is_openai_configured

class CrisisComponents:
    """Crisis-specific UI components."""
    
    @staticmethod
    def render_crisis_mode_button() -> bool:
        """
        Render the main crisis mode button.
        
        Returns:
            True if crisis mode is activated, False otherwise
        """
        # Large, prominent crisis mode button
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            crisis_activated = st.button(
                "🚨 CRISIS MODE",
                type="primary",
                use_container_width=True,
                help="Click for immediate crisis assistance"
            )
        
        return crisis_activated
    
    @staticmethod
    def render_crisis_active_header():
        """Render header when crisis mode is active."""
        st.markdown("---")
        st.markdown("### 🚨 CRISIS MODE ACTIVE")
        st.markdown("*I'm here to help. What's happening?*")
        st.markdown("---")
    
    @staticmethod
    def render_emergency_911_button():
        """Render the emergency 911 call button."""
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("📞 CALL 911", type="secondary", use_container_width=True):
                st.error("🚨 EMERGENCY: 911 would be called here")
                st.info("In production, this would trigger emergency services")
    
    @staticmethod
    def render_ai_response_area(response: Optional[str] = None):
        """
        Render the AI response display area.
        
        Args:
            response: The AI-generated response to display
        """
        st.markdown("### 🤖 AI Response")
        
        if response:
            st.markdown(response)
            
            # Copy button for the response
            if st.button("📋 Copy Response", type="secondary"):
                st.success("Response copied to clipboard!")
        else:
            st.info("AI response will appear here...")
    
    @staticmethod
    def render_crisis_input():
        """
        Render crisis input area for manual text entry.
        
        Returns:
            User input text or None
        """
        st.markdown("### 📝 Describe the Emergency")
        
        # Text input for crisis description
        crisis_text = st.text_area(
            "What's happening? Describe the emergency:",
            placeholder="e.g., There's a fire in my kitchen, I need help...",
            height=100
        )
        
        # Generate response button
        if st.button("🚨 Get Help Now", type="primary"):
            return crisis_text
        
        return None
    
    @staticmethod
    def render_api_status():
        """Render OpenAI API connection status."""
        st.sidebar.markdown("### 🔧 API Status")
        
        if is_openai_configured():
            st.sidebar.success("✅ OpenAI API: Connected")
        else:
            st.sidebar.error("❌ OpenAI API: Not configured")
            st.sidebar.info("Add OPENAI_API_KEY to .env file")
    
    @staticmethod
    def render_test_scenarios():
        """Render quick test scenario buttons."""
        st.markdown("### 🧪 Quick Test Scenarios")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔥 Fire Emergency"):
                return "There's a fire in my house, what should I do?"
            
            if st.button("🏥 Medical Emergency"):
                return "Someone is having chest pain, help!"
        
        with col2:
            if st.button("🚨 Safety Concern"):
                return "I think someone is trying to break into my house"
            
            if st.button("🌪️ Natural Disaster"):
                return "There's a tornado warning, what should I do?"
        
        return None 