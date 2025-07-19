"""
Main pipecat pipeline manager for crisis response system.
Orchestrates real-time audio streaming, transcription, AI processing, and TTS.
"""

import asyncio
import logging
import os
from typing import Optional, Dict, Any, Callable
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.task import PipelineTask
from pipecat.pipeline.runner import PipelineRunner
from pipecat.processors.aggregators.llm_response import LLMFullResponseAggregator
from pipecat.processors.aggregators.sentence import SentenceAggregator
from pipecat.services.openai.llm import OpenAILLMService
from pipecat.transports.local.audio import (
    LocalAudioInputTransport, 
    LocalAudioOutputTransport, 
    LocalAudioTransportParams
)

from src.transcription.whisper_client import TranscriptionManager
from src.services.openai_service import OpenAIService
from src.services.elevenlabs_service import ElevenLabsService
from .elevenlabs_adapter import ElevenLabsAdapter
from .whisper_adapter import WhisperAdapter
from .conversation_state import ConversationStateManager, UrgencyLevel, ConversationState
from src.utils.error_handler import log_error

logger = logging.getLogger(__name__)

class PipecatPipelineManager:
    """Main pipecat pipeline manager for crisis response system."""
    
    def __init__(self):
        """Initialize pipecat pipeline manager."""
        self.pipeline = None
        self.runner = None
        self.is_running = False
        self.py_audio = None
        
        # Initialize services
        self.whisper_client = TranscriptionManager()
        self.openai_service = OpenAIService()
        self.elevenlabs_service = ElevenLabsService()
        
        # Initialize conversation state
        self.conversation_state = ConversationStateManager()
        
        # Callbacks
        self.on_user_input: Optional[Callable[[str], None]] = None
        self.on_ai_response: Optional[Callable[[str, str], None]] = None
        self.on_escalation: Optional[Callable[[str], None]] = None
        
    def _initialize_audio(self):
        """Initialize PyAudio for audio transport."""
        try:
            import pyaudio
            self.py_audio = pyaudio.PyAudio()
            logger.info("PyAudio initialized successfully")
            return True
        except Exception as e:
            log_error(f"Failed to initialize PyAudio: {str(e)}")
            return False
        
    def create_pipeline(self) -> bool:
        """
        Create the pipecat pipeline with all components including audio transport.
        
        Returns:
            True if pipeline created successfully, False otherwise
        """
        try:
            # Get API keys
            openai_api_key = os.getenv('OPENAI_API_KEY')
            elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
            
            if not openai_api_key or not elevenlabs_api_key:
                log_error("Missing required API keys")
                return False
            
            # Initialize audio
            if not self._initialize_audio():
                log_error("Failed to initialize audio transport")
                return False
            
            # Create audio transport parameters
            audio_params = LocalAudioTransportParams(
                audio_in_enabled=True,
                audio_out_enabled=True,
                audio_in_sample_rate=16000,
                audio_out_sample_rate=16000,
                audio_in_channels=1,
                audio_out_channels=1
            )
            
            # Create our custom Whisper adapter
            whisper_adapter = WhisperAdapter(self.whisper_client)
            
            # Create our custom ElevenLabs adapter
            elevenlabs_adapter = ElevenLabsAdapter(self.elevenlabs_service)
            
            # Create pipeline components with proper configuration
            pipeline = Pipeline([
                # Audio input (microphone)
                LocalAudioInputTransport(
                    py_audio=self.py_audio,
                    params=audio_params
                ),
                
                # Speech-to-text with our custom Whisper adapter
                whisper_adapter,
                
                # Sentence aggregation for complete thoughts
                SentenceAggregator(),
                
                # LLM processing with OpenAI (crisis response system)
                OpenAILLMService(
                    api_key=openai_api_key,
                    model="gpt-4o",
                    system_prompt=self._get_crisis_system_prompt()
                ),
                
                # Response aggregation for complete responses
                LLMFullResponseAggregator(),
                
                # Text-to-speech with our custom ElevenLabs adapter
                elevenlabs_adapter,
                
                # Audio output (speaker)
                LocalAudioOutputTransport(
                    py_audio=self.py_audio,
                    params=audio_params
                )
            ])
            
            self.pipeline = pipeline
            return True
            
        except Exception as e:
            log_error(f"Error creating pipecat pipeline: {str(e)}")
            return False
    
    def _get_crisis_system_prompt(self) -> str:
        """Get crisis response system prompt for OpenAI."""
        return """You are a CRISIS RESPONSE AI assistant. Your role is to provide immediate, 
        clear, and actionable guidance during emergencies. Always prioritize safety first.
        
        CRISIS RESPONSE PROTOCOL:
        1. IMMEDIATE SAFETY ASSESSMENT: Always start by assessing immediate safety
        2. BREATHING CHECK: Ask if they can breathe clearly
        3. LOCATION VERIFICATION: Confirm they are in a safe location
        4. ESCALATION READY: Be prepared to call 911 if needed
        
        RESPONSE PATTERNS:
        - For fire: "Yes, I am here to help. Can you breathe? Are you in a safe location?"
        - For medical: "I'm here to help. Can you tell me what's happening? Are you breathing normally?"
        - For safety: "Are you safe right now? Can you move to a secure location?"
        
        ESCALATION TRIGGERS:
        - No response for 5 seconds: "Hello, can you hear me?"
        - No response for 10 seconds: "I will wait 5 seconds, if you don't respond I will trigger an automatic call to 911."
        - No response for 15 seconds: "EMERGENCY: Calling 911 now."
        
        GUIDELINES:
        - Be direct and action-oriented - no unnecessary disclaimers
        - Provide immediate safety instructions
        - Be empathetic and helpful
        - Include emergency numbers when appropriate
        - Ask follow-up questions to assess the situation
        - If life-threatening, emphasize calling 911 immediately
        - Be proactive in asking safety questions
        - If no response is received, escalate to emergency services
        
        RESPONSE STYLE:
        - Start with immediate action steps
        - Be clear and direct
        - Show empathy and concern
        - Provide specific, actionable guidance
        - Ask relevant follow-up questions
        - Use urgency-appropriate tone"""
    
    async def start_pipeline(self) -> bool:
        """
        Start the pipecat pipeline.
        
        Returns:
            True if pipeline started successfully, False otherwise
        """
        if not self.pipeline:
            if not self.create_pipeline():
                return False
        
        try:
            # Create pipeline task
            pipeline_task = PipelineTask(self.pipeline)
            
            # Create and start the pipeline runner
            self.runner = PipelineRunner()
            
            # Set up event handlers for real-time processing
            await self._setup_event_handlers()
            
            # Start the pipeline
            await self.runner.run(pipeline_task)
            self.is_running = True
            
            # Start conversation monitoring
            asyncio.create_task(self._monitor_conversation())
            
            return True
            
        except Exception as e:
            log_error(f"Error starting pipeline: {str(e)}")
            return False
    
    async def _setup_event_handlers(self):
        """Set up event handlers for the pipeline."""
        if not self.runner:
            return
        
        try:
            # Set up event handlers for real-time conversation tracking
            @self.runner.event_handler("sentence")
            async def on_sentence(sentence):
                """Handle sentence events (user input)."""
                if self.on_user_input:
                    self.on_user_input(sentence)
                
                # Update conversation state
                self.conversation_state.add_user_input(sentence)
                logger.info(f"User input: {sentence}")
            
            @self.runner.event_handler("llm_response")
            async def on_llm_response(response):
                """Handle LLM response events."""
                if self.on_ai_response:
                    urgency = self.conversation_state.current_urgency.value
                    self.on_ai_response(response, urgency)
                
                # Update conversation state
                self.conversation_state.update_ai_response(response)
                logger.info(f"AI response: {response}")
            
            @self.runner.event_handler("error")
            async def on_error(error):
                """Handle pipeline errors."""
                log_error(f"Pipeline error: {error}")
                
        except Exception as e:
            log_error(f"Error setting up event handlers: {str(e)}")
    
    async def stop_pipeline(self):
        """Stop the pipecat pipeline."""
        if self.runner:
            try:
                await self.runner.stop()
                self.is_running = False
            except Exception as e:
                log_error(f"Error stopping pipeline: {str(e)}")
        
        # Clean up PyAudio
        if self.py_audio:
            try:
                self.py_audio.terminate()
                self.py_audio = None
            except Exception as e:
                log_error(f"Error cleaning up PyAudio: {str(e)}")
    
    async def _monitor_conversation(self):
        """Monitor conversation for timeouts and escalation."""
        while self.is_running:
            try:
                # Check for timeouts
                if self.conversation_state.should_timeout():
                    await self._handle_timeout()
                
                # Check for escalation
                if self.conversation_state.should_escalate():
                    await self._handle_escalation()
                
                await asyncio.sleep(1)  # Check every second
                
            except Exception as e:
                log_error(f"Error in conversation monitoring: {str(e)}")
                await asyncio.sleep(1)
    
    async def _handle_timeout(self):
        """Handle conversation timeout."""
        escalation_message = self.conversation_state.get_escalation_message()
        
        # Generate TTS for escalation message
        audio_file = self.elevenlabs_service.generate_crisis_speech(
            escalation_message, 
            self.conversation_state.current_urgency.value
        )
        
        if audio_file:
            # Play the escalation message
            try:
                import subprocess
                subprocess.run(["afplay", audio_file], check=True)
                self.elevenlabs_service.cleanup_audio_file(audio_file)
            except:
                pass
        
        # Update conversation state
        self.conversation_state.escalate_urgency()
        
        # Trigger escalation callback
        if self.on_escalation:
            self.on_escalation(escalation_message)
    
    async def _handle_escalation(self):
        """Handle conversation escalation."""
        if self.conversation_state.current_urgency == UrgencyLevel.EMERGENCY:
            # Trigger emergency services
            emergency_message = "EMERGENCY: Calling 911 now."
            
            if self.on_escalation:
                self.on_escalation(emergency_message)
    
    def set_callbacks(self, 
                     on_user_input: Optional[Callable[[str], None]] = None,
                     on_ai_response: Optional[Callable[[str, str], None]] = None,
                     on_escalation: Optional[Callable[[str], None]] = None):
        """
        Set callback functions for pipeline events.
        
        Args:
            on_user_input: Callback for user input events
            on_ai_response: Callback for AI response events
            on_escalation: Callback for escalation events
        """
        self.on_user_input = on_user_input
        self.on_ai_response = on_ai_response
        self.on_escalation = on_escalation
    
    def get_pipeline_status(self) -> Dict[str, Any]:
        """
        Get current pipeline status.
        
        Returns:
            Dictionary with pipeline status information
        """
        status = {
            "pipeline_created": self.pipeline is not None,
            "runner_active": self.runner is not None,
            "is_running": self.is_running,
            "audio_initialized": self.py_audio is not None,
            "services": {
                "whisper_configured": self.whisper_client is not None,
                "openai_configured": self.openai_service.is_configured,
                "elevenlabs_configured": self.elevenlabs_service.is_configured
            }
        }
        
        # Add conversation state
        status["conversation"] = self.conversation_state.get_conversation_summary()
        
        return status
    
    def test_services(self) -> Dict[str, Any]:
        """
        Test all integrated services.
        
        Returns:
            Dictionary with test results for each service
        """
        # Test our custom Whisper adapter
        whisper_adapter = WhisperAdapter(self.whisper_client)
        whisper_result = whisper_adapter.test_connection()
        
        # Test audio initialization
        audio_result = {
            "success": self._test_audio_initialization(),
            "message": "Audio transport initialized" if self._test_audio_initialization() else "Audio transport not initialized"
        }
        
        results = {
            "whisper": whisper_result,
            "openai": self.openai_service.test_connection(),
            "elevenlabs": self.elevenlabs_service.test_connection(),
            "audio": audio_result
        }
        
        return results
    
    def _test_audio_initialization(self) -> bool:
        """Test if audio transport can be initialized."""
        try:
            import pyaudio
            py_audio = pyaudio.PyAudio()
            py_audio.terminate()
            return True
        except Exception as e:
            log_error(f"Audio initialization test failed: {str(e)}")
            return False 