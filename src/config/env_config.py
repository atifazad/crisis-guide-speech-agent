"""
Environment configuration loader for the Voice-to-Voice AI Assistant.
Loads OpenAI API key from environment variables.
"""

import os
from typing import Any, Dict, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_env_var(key: str, default: Any = None, var_type: type = str) -> Any:
    """
    Get environment variable with type conversion and default value.
    
    Args:
        key: Environment variable name
        default: Default value if environment variable is not set
        var_type: Type to convert the value to (str, int, float, bool)
    
    Returns:
        Environment variable value converted to specified type
    """
    value = os.getenv(key, default)
    
    if value is None:
        return default
    
    # Type conversion
    if var_type == bool:
        if isinstance(value, str):
            return value.lower() in ('true', '1', 'yes', 'on')
        return bool(value)
    elif var_type == int:
        return int(value)
    elif var_type == float:
        return float(value)
    else:
        return str(value)

class EnvConfig:
    """Environment configuration class with OpenAI API key."""
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = get_env_var("OPENAI_API_KEY", "")
    
    @classmethod
    def validate_config(cls) -> Dict[str, Any]:
        """
        Validate the configuration and return any issues.
        
        Returns:
            Dictionary with validation results
        """
        issues = {}
        
        # Check required settings
        if not cls.OPENAI_API_KEY:
            issues["OPENAI_API_KEY"] = "OpenAI API key is required"
        
        return issues
    
    @classmethod
    def get_config_summary(cls) -> Dict[str, Any]:
        """
        Get a summary of the current configuration.
        
        Returns:
            Dictionary with configuration summary
        """
        return {
            "openai_api_key_set": bool(cls.OPENAI_API_KEY),
        } 