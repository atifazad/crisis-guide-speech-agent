"""
Configuration validator for the Voice-to-Voice AI Assistant.
Validates OpenAI API key configuration.
"""

import streamlit as st
from typing import Dict, Any, List
from .env_config import EnvConfig

class ConfigValidator:
    """Validates application configuration and displays issues to users."""
    
    @staticmethod
    def validate_and_display_issues() -> bool:
        """
        Validate configuration and display any issues in the Streamlit UI.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        issues = EnvConfig.validate_config()
        
        if issues:
            st.error("⚠️ Configuration Issues Found")
            
            for setting, message in issues.items():
                st.error(f"**{setting}**: {message}")
            
            st.info("💡 **How to fix:**")
            st.info("1. Copy `env.example` to `.env`")
            st.info("2. Add your OpenAI API key to the `.env` file")
            st.info("3. Restart the application")
            
            return False
        
        return True
    
    @staticmethod
    def display_config_summary():
        """Display a summary of the current configuration."""
        config = EnvConfig.get_config_summary()
        
        st.sidebar.header("🔧 Configuration")
        
        # OpenAI API Key status
        if config["openai_api_key_set"]:
            st.sidebar.success("✅ OpenAI API Key: Configured")
        else:
            st.sidebar.error("❌ OpenAI API Key: Not configured")
    
    @staticmethod
    def get_missing_required_vars() -> List[str]:
        """
        Get list of missing required environment variables.
        
        Returns:
            List of missing required variable names
        """
        missing = []
        
        if not EnvConfig.OPENAI_API_KEY:
            missing.append("OPENAI_API_KEY")
        
        return missing
    
    @staticmethod
    def is_fully_configured() -> bool:
        """
        Check if all required configuration is present.
        
        Returns:
            True if fully configured, False otherwise
        """
        return len(ConfigValidator.get_missing_required_vars()) == 0 