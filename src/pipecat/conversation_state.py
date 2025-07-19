"""
Conversation state management for crisis response system.
Tracks real-time conversation flow and manages agentic behavior.
"""

import asyncio
import time
import logging
from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class ConversationState(Enum):
    """Enumeration of conversation states."""
    IDLE = "idle"
    LISTENING = "listening"
    PROCESSING = "processing"
    SPEAKING = "speaking"
    ESCALATING = "escalating"
    EMERGENCY = "emergency"

class UrgencyLevel(Enum):
    """Enumeration of urgency levels."""
    NORMAL = "normal"
    URGENT = "urgent"
    EMERGENCY = "emergency"

@dataclass
class ConversationTurn:
    """Represents a single conversation turn."""
    timestamp: datetime
    user_input: str
    ai_response: str
    urgency_level: UrgencyLevel
    processing_time: float

class ConversationStateManager:
    """Manages conversation state and agentic behavior."""
    
    def __init__(self):
        """Initialize conversation state manager."""
        self.current_state = ConversationState.IDLE
        self.current_urgency = UrgencyLevel.NORMAL
        self.conversation_history: List[ConversationTurn] = []
        self.last_user_activity = None
        self.last_ai_response = None
        self.escalation_timer = None
        self.timeout_threshold = 5.0  # seconds
        self.escalation_threshold = 10.0  # seconds
        
    def update_user_activity(self):
        """Update timestamp of last user activity."""
        self.last_user_activity = datetime.now()
        self.current_state = ConversationState.LISTENING
        
    def update_ai_response(self, response: str, urgency: UrgencyLevel = UrgencyLevel.NORMAL):
        """Update AI response and state."""
        self.last_ai_response = datetime.now()
        self.current_state = ConversationState.SPEAKING
        self.current_urgency = urgency
        
        # Add to conversation history
        if self.conversation_history:
            last_turn = self.conversation_history[-1]
            last_turn.ai_response = response
            last_turn.urgency_level = urgency
            last_turn.processing_time = (datetime.now() - last_turn.timestamp).total_seconds()
        
    def add_user_input(self, user_input: str):
        """Add user input to conversation."""
        self.update_user_activity()
        
        # Create new conversation turn
        turn = ConversationTurn(
            timestamp=datetime.now(),
            user_input=user_input,
            ai_response="",
            urgency_level=self.current_urgency,
            processing_time=0.0
        )
        self.conversation_history.append(turn)
        
    def get_conversation_summary(self) -> Dict[str, Any]:
        """
        Get summary of current conversation.
        
        Returns:
            Dictionary with conversation summary
        """
        return {
            "current_state": self.current_state.value,
            "current_urgency": self.current_urgency.value,
            "total_turns": len(self.conversation_history),
            "last_user_activity": self.last_user_activity.isoformat() if self.last_user_activity else None,
            "last_ai_response": self.last_ai_response.isoformat() if self.last_ai_response else None,
            "time_since_user_activity": self.get_time_since_user_activity(),
            "time_since_ai_response": self.get_time_since_ai_response()
        }
    
    def get_time_since_user_activity(self) -> Optional[float]:
        """Get time since last user activity in seconds."""
        if self.last_user_activity:
            return (datetime.now() - self.last_user_activity).total_seconds()
        return None
    
    def get_time_since_ai_response(self) -> Optional[float]:
        """Get time since last AI response in seconds."""
        if self.last_ai_response:
            return (datetime.now() - self.last_ai_response).total_seconds()
        return None
    
    def should_escalate(self) -> bool:
        """
        Check if conversation should escalate due to lack of response.
        
        Returns:
            True if escalation is needed, False otherwise
        """
        time_since_activity = self.get_time_since_user_activity()
        if time_since_activity and time_since_activity > self.escalation_threshold:
            return True
        return False
    
    def should_timeout(self) -> bool:
        """
        Check if conversation should timeout.
        
        Returns:
            True if timeout is needed, False otherwise
        """
        time_since_activity = self.get_time_since_user_activity()
        if time_since_activity and time_since_activity > self.timeout_threshold:
            return True
        return False
    
    def get_escalation_message(self) -> str:
        """
        Get escalation message based on current state.
        
        Returns:
            Escalation message
        """
        if self.current_urgency == UrgencyLevel.EMERGENCY:
            return "I will call 911 immediately. Please stay on the line."
        elif self.current_urgency == UrgencyLevel.URGENT:
            return "I will wait 5 more seconds, then call emergency services."
        else:
            return "Hello, can you hear me? Please respond if you need help."
    
    def escalate_urgency(self):
        """Escalate the urgency level."""
        if self.current_urgency == UrgencyLevel.NORMAL:
            self.current_urgency = UrgencyLevel.URGENT
        elif self.current_urgency == UrgencyLevel.URGENT:
            self.current_urgency = UrgencyLevel.EMERGENCY
        
        self.current_state = ConversationState.ESCALATING
    
    def reset_conversation(self):
        """Reset conversation state."""
        self.current_state = ConversationState.IDLE
        self.current_urgency = UrgencyLevel.NORMAL
        self.last_user_activity = None
        self.last_ai_response = None
        self.escalation_timer = None
    
    def get_recent_context(self, turns: int = 5) -> List[Dict[str, str]]:
        """
        Get recent conversation context for AI processing.
        
        Args:
            turns: Number of recent turns to include
            
        Returns:
            List of conversation turns as dictionaries
        """
        recent_turns = self.conversation_history[-turns:] if self.conversation_history else []
        
        context = []
        for turn in recent_turns:
            context.append({
                "role": "user",
                "content": turn.user_input
            })
            if turn.ai_response:
                context.append({
                    "role": "assistant", 
                    "content": turn.ai_response
                })
        
        return context 