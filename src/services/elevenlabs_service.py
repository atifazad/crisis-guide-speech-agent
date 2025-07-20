#!/usr/bin/env python3
"""
ElevenLabs Service
Handles all ElevenLabs API interactions including text-to-speech conversion
"""

import logging
import requests
from typing import Optional, Dict, Any
from config import Config

logger = logging.getLogger(__name__)

class ElevenLabsService:
    """Service for handling ElevenLabs API interactions."""
    
    def __init__(self):
        """Initialize the ElevenLabs service."""
        self.api_key = Config.get_elevenlabs_api_key()
        self.voice_id = Config.get_elevenlabs_voice_id()
        self.base_url = Config.get_elevenlabs_base_url()
        logger.info(f"ElevenLabs service initialized with voice ID: {self.voice_id}")
    
    def text_to_speech(self, text: str, voice_settings: Optional[Dict[str, float]] = None) -> Optional[bytes]:
        """
        Convert text to speech using ElevenLabs API.
        
        Args:
            text: The text to convert to speech
            voice_settings: Optional voice settings (stability, similarity_boost)
            
        Returns:
            Audio data as bytes or None if error
        """
        try:
            url = f"{self.base_url}/text-to-speech/{self.voice_id}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.api_key
            }
            
            # Default voice settings
            if voice_settings is None:
                voice_settings = {
                    "stability": 0.5,
                    "similarity_boost": 0.5
                }
            
            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": voice_settings
            }
            
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                audio_data = response.content
                logger.info(f"Generated TTS audio: {len(audio_data)} bytes")
                return audio_data
            else:
                logger.error(f"ElevenLabs API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"TTS error: {str(e)}")
            return None
    
    def get_available_voices(self) -> Optional[list]:
        """
        Get list of available voices from ElevenLabs.
        
        Returns:
            List of voice dictionaries or None if error
        """
        try:
            url = f"{self.base_url}/voices"
            
            headers = {
                "Accept": "application/json",
                "xi-api-key": self.api_key
            }
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                voices = response.json().get("voices", [])
                logger.info(f"Retrieved {len(voices)} available voices")
                return voices
            else:
                logger.error(f"ElevenLabs voices API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting voices: {str(e)}")
            return None
    
    def validate_api_key(self) -> bool:
        """
        Validate that the ElevenLabs API key is working.
        
        Returns:
            True if API key is valid, False otherwise
        """
        try:
            # Try to get available voices to test the API key
            voices = self.get_available_voices()
            return voices is not None
        except Exception as e:
            logger.error(f"ElevenLabs API key validation failed: {str(e)}")
            return False
    
    def get_voice_info(self, voice_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific voice.
        
        Args:
            voice_id: Voice ID to get info for (uses default if None)
            
        Returns:
            Voice information dictionary or None if error
        """
        try:
            voice_id = voice_id or self.voice_id
            url = f"{self.base_url}/voices/{voice_id}"
            
            headers = {
                "Accept": "application/json",
                "xi-api-key": self.api_key
            }
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                voice_info = response.json()
                logger.info(f"Retrieved voice info for: {voice_info.get('name', 'Unknown')}")
                return voice_info
            else:
                logger.error(f"ElevenLabs voice info API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting voice info: {str(e)}")
            return None 