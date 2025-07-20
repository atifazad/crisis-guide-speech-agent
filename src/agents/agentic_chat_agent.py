#!/usr/bin/env python3
"""
Minimal AgenticChatAgent for the agentic voice agent
"""

import logging
from src.services.openai_service import OpenAIService

logger = logging.getLogger(__name__)

class AgenticChatAgent:
    """Minimal agentic chat agent for voice interactions."""
    
    def __init__(self):
        """Initialize the agentic chat agent."""
        self.openai_service = OpenAIService()
        logger.info("Agentic chat agent initialized with OpenAI service")
    
    def get_agentic_response(self, user_message: str) -> str:
        """Get an agentic response to user input."""
        return self.openai_service.get_default_agentic_response(user_message) 