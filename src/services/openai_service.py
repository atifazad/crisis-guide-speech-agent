#!/usr/bin/env python3
"""
OpenAI Service
Handles all OpenAI API interactions including GPT-4o responses
"""

import logging
import openai
from typing import Optional, List, Dict, Any
from config import Config

logger = logging.getLogger(__name__)

class OpenAIService:
    """Service for handling OpenAI API interactions."""
    
    def __init__(self):
        """Initialize the OpenAI service."""
        self.client = openai.OpenAI(api_key=Config.get_api_key())
        self.model = Config.get_model()
        self.max_tokens = Config.get_max_tokens()
        self.temperature = Config.get_temperature()
        logger.info(f"OpenAI service initialized with model: {self.model}")
    
    def create_chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> Optional[str]:
        """
        Create a chat completion using OpenAI API.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            max_tokens: Maximum tokens for response (uses config default if None)
            temperature: Temperature for response (uses config default if None)
            
        Returns:
            Response text or None if error
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens or self.max_tokens,
                temperature=temperature or self.temperature
            )
            
            response_text = response.choices[0].message.content
            logger.info(f"Generated OpenAI response with {len(response_text)} characters")
            return response_text
            
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return None
    
    def get_agentic_response(self, user_message: str, system_prompt: str) -> str:
        """
        Get an agentic response using a custom system prompt.
        
        Args:
            user_message: The user's message
            system_prompt: Custom system prompt to use
            
        Returns:
            Response text or fallback message
        """
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
            
            response = self.create_chat_completion(messages)
            
            if response:
                return response
            else:
                return "I'm here to help. Can you tell me what's happening?"
                
        except Exception as e:
            logger.error(f"Agentic response error: {str(e)}")
            return "I'm here to help. Can you tell me what's happening?"
    
    def get_default_agentic_response(self, user_message: str) -> str:
        """
        Get an agentic response using the default system prompt.
        
        Args:
            user_message: The user's message
            
        Returns:
            Response text or fallback message
        """
        system_prompt = """You are an agentic AI assistant that takes initiative and leads conversations.

CORE BEHAVIORS:
- Take initiative and lead conversations proactively
- Ask specific, relevant questions based on the situation
- Provide clear, actionable guidance
- Stay calm and reassuring in emergencies
- Escalate appropriately when needed

CONVERSATION STYLE:
- Be direct and authoritative but caring
- Use simple, clear language suitable for voice
- Avoid complex explanations
- Focus on immediate needs and safety
- Provide step-by-step guidance when appropriate

RESPONSE GUIDELINES:
- Be proactive and take initiative
- Ask relevant questions to assess the situation
- Provide clear, actionable steps
- Stay calm and reassuring
- Use natural, conversational language
- Keep responses concise for voice interaction

Respond as the agentic assistant:"""
        
        return self.get_agentic_response(user_message, system_prompt)
    
    def validate_api_key(self) -> bool:
        """
        Validate that the OpenAI API key is working.
        
        Returns:
            True if API key is valid, False otherwise
        """
        try:
            # Try a simple completion to test the API key
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            return True
        except Exception as e:
            logger.error(f"OpenAI API key validation failed: {str(e)}")
            return False 