"""
OpenAI service for crisis response generation using the Responses API.
Handles API calls and response formatting for crisis situations.
"""

import openai
from typing import Optional, Dict, Any, List
from src.config.openai_config import get_openai_api_key, is_openai_configured

class OpenAIService:
    """OpenAI service for crisis response generation using Responses API."""
    
    def __init__(self):
        """Initialize the OpenAI service."""
        self.api_key = get_openai_api_key()
        self.is_configured = is_openai_configured()
        
        if self.is_configured:
            self.client = openai.OpenAI(api_key=self.api_key)
        else:
            self.client = None
    
    def generate_crisis_response(self, crisis_description: str, conversation_history: List[Dict] = None) -> Optional[str]:
        """
        Generate a crisis response using OpenAI Responses API.
        
        Args:
            crisis_description: Description of the crisis situation
            conversation_history: Previous conversation messages for context
            
        Returns:
            AI-generated crisis response or None if error
        """
        if not self.is_configured:
            return "❌ OpenAI API not configured. Please add your API key to the .env file."
        
        try:
            # Prepare messages for the conversation
            messages = []
            
            # Add system message for crisis response behavior
            system_message = {
                "role": "system",
                "content": """You are a crisis response AI assistant. Your role is to provide immediate, 
                clear, and actionable guidance during emergencies. Always prioritize safety first.
                
                Guidelines:
                - Be direct and action-oriented - no unnecessary disclaimers
                - Provide immediate safety instructions
                - Be empathetic and helpful
                - Include emergency numbers when appropriate
                - Ask follow-up questions to assess the situation
                - If life-threatening, emphasize calling 911 immediately
                - Be proactive in asking safety questions
                - If no response is received, escalate to emergency services
                
                Response Style:
                - Start with immediate action steps
                - Be clear and direct
                - Show empathy and concern
                - Provide specific, actionable guidance
                - Ask relevant follow-up questions"""
            }
            messages.append(system_message)
            
            # Add conversation history for context
            if conversation_history:
                messages.extend(conversation_history)
            
            # Prepare crisis-specific input with instructions
            crisis_input = f"""You are a crisis response AI assistant. Be direct, empathetic, and action-oriented. 
            Provide immediate safety instructions without unnecessary disclaimers.
            
            User emergency: {crisis_description}
            
            Respond with clear, actionable steps and show empathy."""
            
            # Generate response using Responses API
            response = self.client.responses.create(
                input=crisis_input,
                model="gpt-4o"
            )
            
            return response.output[0].content[0].text
            
        except Exception as e:
            return f"❌ Error generating response: {str(e)}"
    
    def generate_proactive_question(self, context: str = "", conversation_history: List[Dict] = None) -> Optional[str]:
        """
        Generate a proactive question to assess the situation.
        
        Args:
            context: Previous conversation context
            conversation_history: Previous conversation messages
            
        Returns:
            Proactive question or None if error
        """
        if not self.is_configured:
            return None
        
        try:
            # Prepare messages
            messages = []
            
            # Add system message for proactive questioning
            system_message = {
                "role": "system",
                "content": """You are a crisis response AI. Generate a single, direct question to assess 
                the current situation and ensure the person is safe. Keep it short and actionable.
                Examples: "Can you breathe?", "Are you able to evacuate?", "Are you safe right now?" """
            }
            messages.append(system_message)
            
            # Add conversation history
            if conversation_history:
                messages.extend(conversation_history)
            
            # Prepare proactive question input
            if context:
                question_input = f"""You are a crisis response AI. Generate a single, direct, empathetic question to assess safety.
                
                Context: {context}
                
                Generate one direct safety question:"""
            else:
                question_input = """You are a crisis response AI. Generate a single, direct, empathetic question to assess safety.
                
                Generate one direct safety question:"""
            
            # Generate response
            response = self.client.responses.create(
                input=question_input,
                model="gpt-4o"
            )
            
            return response.output[0].content[0].text
            
        except Exception as e:
            return "Are you safe right now?"
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test the OpenAI API connection.
        
        Returns:
            Dictionary with test results
        """
        if not self.is_configured:
            return {
                "success": False,
                "error": "OpenAI API not configured",
                "message": "Add OPENAI_API_KEY to .env file"
            }
        
        try:
            # Test with a simple response
            response = self.client.responses.create(
                input="Test",
                model="gpt-4o"
            )
            
            return {
                "success": True,
                "message": "OpenAI Responses API connection successful",
                "api": "Responses API"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "OpenAI API connection failed"
            } 