"""
OpenAI configuration for the Voice-to-Voice AI Assistant.
Provides access to OpenAI API key from environment variables.
"""

from .env_config import EnvConfig

def get_openai_api_key() -> str:
    """
    Get the OpenAI API key from environment variables.
    
    Returns:
        OpenAI API key string
    """
    return EnvConfig.OPENAI_API_KEY

def is_openai_configured() -> bool:
    """
    Check if OpenAI API key is configured.
    
    Returns:
        True if API key is set, False otherwise
    """
    return bool(EnvConfig.OPENAI_API_KEY) 