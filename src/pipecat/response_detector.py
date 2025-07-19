"""
Response detection system for crisis response pipeline.
Monitors for user responses, detects silence, and manages timeouts.
"""

import asyncio
import logging
from typing import Optional, Callable, Dict, Any
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)

class ResponseStatus(Enum):
    """Status of user response detection."""
    WAITING = "waiting"
    RESPONDED = "responded"
    TIMEOUT = "timeout"
    ESCALATING = "escalating"

class ResponseDetector:
    """Monitors for user responses and manages timeouts."""
    
    def __init__(self, 
                 timeout_threshold: float = 5.0,
                 escalation_threshold: float = 10.0,
                 emergency_threshold: float = 15.0):
        """
        Initialize response detector.
        
        Args:
            timeout_threshold: Seconds before first timeout check
            escalation_threshold: Seconds before escalation
            emergency_threshold: Seconds before emergency call
        """
        self.timeout_threshold = timeout_threshold
        self.escalation_threshold = escalation_threshold
        self.emergency_threshold = emergency_threshold
        
        self.current_status = ResponseStatus.WAITING
        self.last_ai_speech_time = None
        self.last_user_response_time = None
        self.is_monitoring = False
        self.monitoring_task = None
        
        # Callbacks
        self.on_timeout: Optional[Callable[[str], None]] = None
        self.on_escalation: Optional[Callable[[str], None]] = None
        self.on_emergency: Optional[Callable[[str], None]] = None
    
    def start_monitoring(self, ai_speech_time: datetime = None):
        """
        Start monitoring for user response.
        
        Args:
            ai_speech_time: When AI finished speaking
        """
        self.last_ai_speech_time = ai_speech_time or datetime.now()
        self.current_status = ResponseStatus.WAITING
        self.is_monitoring = True
        
        # Start monitoring task
        if self.monitoring_task:
            self.monitoring_task.cancel()
        
        self.monitoring_task = asyncio.create_task(self._monitor_response())
        logger.info("Response monitoring started")
    
    def stop_monitoring(self):
        """Stop monitoring for user response."""
        self.is_monitoring = False
        if self.monitoring_task:
            self.monitoring_task.cancel()
            self.monitoring_task = None
        logger.info("Response monitoring stopped")
    
    def user_responded(self, response_time: datetime = None):
        """
        Register that user has responded.
        
        Args:
            response_time: When user responded
        """
        self.last_user_response_time = response_time or datetime.now()
        self.current_status = ResponseStatus.RESPONDED
        self.stop_monitoring()
        logger.info("User response detected")
    
    async def _monitor_response(self):
        """Monitor for user response with timeout escalation (async)."""
        try:
            while self.is_monitoring:
                current_time = datetime.now()
                time_since_ai = (current_time - self.last_ai_speech_time).total_seconds()
                
                # Check for timeout
                if time_since_ai >= self.timeout_threshold and self.current_status == ResponseStatus.WAITING:
                    await self._handle_timeout()
                
                # Check for escalation
                elif time_since_ai >= self.escalation_threshold and self.current_status == ResponseStatus.TIMEOUT:
                    await self._handle_escalation()
                
                # Check for emergency
                elif time_since_ai >= self.emergency_threshold and self.current_status == ResponseStatus.ESCALATING:
                    await self._handle_emergency()
                
                await asyncio.sleep(0.5)  # Check every 500ms
                
        except asyncio.CancelledError:
            logger.info("Response monitoring cancelled")
        except Exception as e:
            logger.error(f"Error in response monitoring: {str(e)}")
    
    async def _handle_timeout(self):
        """Handle first timeout (5 seconds)."""
        self.current_status = ResponseStatus.TIMEOUT
        
        timeout_message = "Hello, can you hear me? Please respond if you need help."
        logger.info(f"Timeout detected: {timeout_message}")
        
        if self.on_timeout:
            self.on_timeout(timeout_message)
    
    async def _handle_escalation(self):
        """Handle escalation (10 seconds)."""
        self.current_status = ResponseStatus.ESCALATING
        
        escalation_message = "I will wait 5 seconds, if you don't respond I will trigger an automatic call to 911."
        logger.info(f"Escalation detected: {escalation_message}")
        
        if self.on_escalation:
            self.on_escalation(escalation_message)
    
    async def _handle_emergency(self):
        """Handle emergency (15 seconds)."""
        self.current_status = ResponseStatus.ESCALATING
        
        emergency_message = "EMERGENCY: Calling 911 now."
        logger.info(f"Emergency detected: {emergency_message}")
        
        if self.on_emergency:
            self.on_emergency(emergency_message)
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current response detection status.
        
        Returns:
            Dictionary with status information
        """
        current_time = datetime.now()
        time_since_ai = (current_time - self.last_ai_speech_time).total_seconds() if self.last_ai_speech_time else None
        
        return {
            "status": self.current_status.value,
            "is_monitoring": self.is_monitoring,
            "time_since_ai_speech": time_since_ai,
            "timeout_threshold": self.timeout_threshold,
            "escalation_threshold": self.escalation_threshold,
            "emergency_threshold": self.emergency_threshold
        }
    
    def set_callbacks(self,
                     on_timeout: Optional[Callable[[str], None]] = None,
                     on_escalation: Optional[Callable[[str], None]] = None,
                     on_emergency: Optional[Callable[[str], None]] = None):
        """
        Set callback functions for response detection events.
        
        Args:
            on_timeout: Callback for timeout events
            on_escalation: Callback for escalation events
            on_emergency: Callback for emergency events
        """
        self.on_timeout = on_timeout
        self.on_escalation = on_escalation
        self.on_emergency = on_emergency 