"""
Configuration file for the Text Chat Agent
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the chat agent."""
    
    # OpenAI API Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Model Configuration
    DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
    MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
    TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    
    # ElevenLabs Configuration
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
    ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")
    ELEVENLABS_BASE_URL = os.getenv("ELEVENLABS_BASE_URL", "https://api.elevenlabs.io/v1")
    
    # Whisper Configuration
    WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")
    WHISPER_LANGUAGE = os.getenv("WHISPER_LANGUAGE", "en")
    
    # Server Configuration
    WEBSOCKET_PORT = int(os.getenv("WEBSOCKET_PORT", "8766"))
    WEB_UI_PORT = int(os.getenv("WEB_UI_PORT", "8001"))
    
    # Emergency Configuration
    EMERGENCY_ESCALATION_DELAY = int(os.getenv("EMERGENCY_ESCALATION_DELAY", "5"))
    MAX_SILENCE_COUNT = int(os.getenv("MAX_SILENCE_COUNT", "3"))
    PROACTIVE_CHECK_INTERVAL = int(os.getenv("PROACTIVE_CHECK_INTERVAL", "2"))

    # Twilio Configuration
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
    EMERGENCY_CALL_ENABLED = os.getenv("EMERGENCY_CALL_ENABLED", "false").lower() == "true"
    EMERGENCY_TARGET_PHONE = os.getenv("EMERGENCY_TARGET_PHONE", "+1234567890")  # Your phone number

    # ACI.dev Configuration
    ACI_API_KEY = os.getenv("ACI_API_KEY")
    ACI_LINKED_ACCOUNT_OWNER_ID = os.getenv("ACI_LINKED_ACCOUNT_OWNER_ID")
    ACI_ENABLED = os.getenv("ACI_ENABLED", "false").lower() == "true"
    
    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "chat_agent.log")
    
    # File Configuration
    CONVERSATION_DIR = os.getenv("CONVERSATION_DIR", "conversations")
    
    @classmethod
    def get_api_key(cls) -> str:
        """Get the OpenAI API key from environment or config."""
        # First try to get from environment variable
        env_key = os.getenv("OPENAI_API_KEY")
        if env_key:
            return env_key
        
        # Fall back to config
        return cls.OPENAI_API_KEY
    
    @classmethod
    def get_model(cls) -> str:
        """Get the model to use."""
        return os.getenv("OPENAI_MODEL", cls.DEFAULT_MODEL)
    
    @classmethod
    def get_max_tokens(cls) -> int:
        """Get the maximum tokens for responses."""
        return int(os.getenv("OPENAI_MAX_TOKENS", cls.MAX_TOKENS))
    
    @classmethod
    def get_temperature(cls) -> float:
        """Get the temperature for responses."""
        return float(os.getenv("OPENAI_TEMPERATURE", cls.TEMPERATURE))
    
    @classmethod
    def get_elevenlabs_api_key(cls) -> str:
        """Get the ElevenLabs API key."""
        return os.getenv("ELEVENLABS_API_KEY", cls.ELEVENLABS_API_KEY)
    
    @classmethod
    def get_elevenlabs_voice_id(cls) -> str:
        """Get the ElevenLabs voice ID."""
        return os.getenv("ELEVENLABS_VOICE_ID", cls.ELEVENLABS_VOICE_ID)
    
    @classmethod
    def get_elevenlabs_base_url(cls) -> str:
        """Get the ElevenLabs base URL."""
        return os.getenv("ELEVENLABS_BASE_URL", cls.ELEVENLABS_BASE_URL)
    
    @classmethod
    def get_whisper_model(cls) -> str:
        """Get the Whisper model to use."""
        return os.getenv("WHISPER_MODEL", cls.WHISPER_MODEL)
    
    @classmethod
    def get_whisper_language(cls) -> str:
        """Get the Whisper language."""
        return os.getenv("WHISPER_LANGUAGE", cls.WHISPER_LANGUAGE)
    
    @classmethod
    def get_websocket_port(cls) -> int:
        """Get the WebSocket server port."""
        return int(os.getenv("WEBSOCKET_PORT", cls.WEBSOCKET_PORT))
    
    @classmethod
    def get_web_ui_port(cls) -> int:
        """Get the Web UI server port."""
        return int(os.getenv("WEB_UI_PORT", cls.WEB_UI_PORT))
    
    @classmethod
    def get_emergency_escalation_delay(cls) -> int:
        """Get the emergency escalation delay in seconds."""
        return int(os.getenv("EMERGENCY_ESCALATION_DELAY", cls.EMERGENCY_ESCALATION_DELAY))
    
    @classmethod
    def get_max_silence_count(cls) -> int:
        """Get the maximum silence count before action."""
        return int(os.getenv("MAX_SILENCE_COUNT", cls.MAX_SILENCE_COUNT))
    
    @classmethod
    def get_proactive_check_interval(cls) -> int:
        """Get the proactive check interval in seconds."""
        return int(os.getenv("PROACTIVE_CHECK_INTERVAL", cls.PROACTIVE_CHECK_INTERVAL))
    
    @classmethod
    def get_twilio_account_sid(cls) -> str:
        """Get the Twilio account SID."""
        return os.getenv("TWILIO_ACCOUNT_SID", cls.TWILIO_ACCOUNT_SID)
    
    @classmethod
    def get_twilio_auth_token(cls) -> str:
        """Get the Twilio auth token."""
        return os.getenv("TWILIO_AUTH_TOKEN", cls.TWILIO_AUTH_TOKEN)
    
    @classmethod
    def get_twilio_phone_number(cls) -> str:
        """Get the Twilio phone number."""
        return os.getenv("TWILIO_PHONE_NUMBER", cls.TWILIO_PHONE_NUMBER)
    
    @classmethod
    def get_emergency_call_enabled(cls) -> bool:
        """Get whether emergency calls are enabled."""
        return os.getenv("EMERGENCY_CALL_ENABLED", "false").lower() == "true"
    
    @classmethod
    def get_emergency_target_phone(cls) -> str:
        """Get the target phone number for emergency calls."""
        return os.getenv("EMERGENCY_TARGET_PHONE", cls.EMERGENCY_TARGET_PHONE)
    
    @classmethod
    def get_aci_api_key(cls) -> str:
        """Get the ACI.dev API key."""
        return os.getenv("ACI_API_KEY", cls.ACI_API_KEY)
    
    @classmethod
    def get_aci_linked_account_owner_id(cls) -> str:
        """Get the ACI.dev linked account owner ID."""
        return os.getenv("ACI_LINKED_ACCOUNT_OWNER_ID", cls.ACI_LINKED_ACCOUNT_OWNER_ID)
    
    @classmethod
    def get_aci_enabled(cls) -> bool:
        """Get whether ACI.dev is enabled."""
        return os.getenv("ACI_ENABLED", "false").lower() == "true"
    
    @classmethod
    def setup_conversation_dir(cls):
        """Create the conversations directory if it doesn't exist."""
        if not os.path.exists(cls.CONVERSATION_DIR):
            os.makedirs(cls.CONVERSATION_DIR)
            print(f"📁 Created conversations directory: {cls.CONVERSATION_DIR}")
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate that all required configuration is present."""
        required_keys = [
            "OPENAI_API_KEY",
            "ELEVENLABS_API_KEY"
        ]
        
        # Add Twilio keys if emergency calls are enabled
        if cls.get_emergency_call_enabled():
            required_keys.extend([
                "TWILIO_ACCOUNT_SID",
                "TWILIO_AUTH_TOKEN",
                "TWILIO_PHONE_NUMBER"
            ])
        
        # Add ACI.dev keys if ACI.dev is enabled
        if cls.get_aci_enabled():
            required_keys.extend([
                "ACI_API_KEY",
                "ACI_LINKED_ACCOUNT_OWNER_ID"
            ])
        
        missing_keys = []
        for key in required_keys:
            if not os.getenv(key) and not getattr(cls, key, None):
                missing_keys.append(key)
        
        if missing_keys:
            print(f"❌ Missing required environment variables: {', '.join(missing_keys)}")
            print("Please set these variables in your .env file or environment")
            return False
        
        print("✅ Configuration validation passed")
        return True 