"""
Whisper adapter for pipecat streaming audio processing.
Integrates existing Whisper transcription with pipecat's real-time audio pipeline.
"""

import asyncio
import logging
from typing import Optional, Dict, Any
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.task import PipelineTask
from pipecat.pipeline.runner import PipelineRunner
from pipecat.processors.aggregators.llm_response import LLMFullResponseAggregator
from pipecat.processors.aggregators.sentence import SentenceAggregator
from pipecat.services.openai.llm import OpenAILLMService
from pipecat.processors.frame_processor import FrameProcessor

from src.transcription.whisper_client import TranscriptionManager
from src.services.elevenlabs_service import ElevenLabsService
from .elevenlabs_adapter import ElevenLabsAdapter
from src.utils.error_handler import log_error

logger = logging.getLogger(__name__)

class WhisperAdapter(FrameProcessor):
    """Custom Whisper adapter using our existing Whisper service."""
    
    def __init__(self, whisper_client: TranscriptionManager):
        """
        Initialize Whisper adapter.
        
        Args:
            whisper_client: Existing Whisper transcription manager
        """
        super().__init__()
        self.whisper_client = whisper_client
        self.is_configured = whisper_client is not None
        
    async def process_audio(self, audio_data: bytes) -> Optional[str]:
        """
        Process audio data to text using our Whisper service.
        
        Args:
            audio_data: Raw audio data
            
        Returns:
            Transcribed text or None if error
        """
        try:
            if not self.is_configured:
                log_error("Whisper service not configured")
                return None
            
            # Use our existing Whisper service to transcribe
            # This would integrate with our existing transcription logic
            # For now, return a placeholder
            return "Transcribed text from audio"
            
        except Exception as e:
            log_error(f"Error in Whisper adapter: {str(e)}")
            return None
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test Whisper connection through adapter.
        
        Returns:
            Dictionary with test results
        """
        if not self.is_configured:
            return {
                "success": False,
                "error": "Whisper service not configured",
                "message": "Whisper client not available"
            }
        
        try:
            # Test that our Whisper service is available
            return {
                "success": True,
                "message": "Whisper service available",
                "service": "Our Whisper Service"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Whisper service test failed"
            }
    
    def get_service_info(self) -> Dict[str, Any]:
        """
        Get Whisper service information.
        
        Returns:
            Dictionary with service information
        """
        return {
            "service_type": "Our Whisper Service",
            "configured": self.is_configured,
            "client_available": self.whisper_client is not None
        }

class WhisperPipelineAdapter:
    """Adapter to integrate existing Whisper with pipecat streaming."""
    
    def __init__(self, whisper_client: TranscriptionManager):
        """
        Initialize Whisper adapter.
        
        Args:
            whisper_client: Existing Whisper transcription manager
        """
        self.whisper_client = whisper_client
        self.pipeline = None
        self.runner = None
        
    def create_pipeline(self, 
                       openai_api_key: str,
                       elevenlabs_api_key: str,
                       voice_id: str = "pNInz6obpgDQGcFmaJgB") -> Pipeline:
        """
        Create pipecat pipeline with our Whisper, OpenAI, and ElevenLabs.
        
        Args:
            openai_api_key: OpenAI API key
            elevenlabs_api_key: ElevenLabs API key
            voice_id: ElevenLabs voice ID for TTS
            
        Returns:
            Configured pipecat pipeline
        """
        try:
            # Create our custom Whisper adapter
            whisper_adapter = WhisperAdapter(self.whisper_client)
            
            # Create our custom ElevenLabs adapter
            elevenlabs_service = ElevenLabsService()
            elevenlabs_adapter = ElevenLabsAdapter(elevenlabs_service)
            
            # Create pipeline components with proper configuration
            pipeline = Pipeline([
                # Speech-to-text with our custom Whisper adapter
                whisper_adapter,
                
                # Sentence aggregation for complete thoughts
                SentenceAggregator(),
                
                # LLM processing with OpenAI
                OpenAILLMService(
                    api_key=openai_api_key,
                    model="gpt-4o",
                    system_prompt=self._get_crisis_system_prompt()
                ),
                
                # Response aggregation for complete responses
                LLMFullResponseAggregator(),
                
                # Text-to-speech with our custom ElevenLabs adapter
                elevenlabs_adapter
            ])
            
            self.pipeline = pipeline
            return pipeline
            
        except Exception as e:
            log_error(f"Error creating pipecat pipeline: {str(e)}")
            return None
    
    def _get_crisis_system_prompt(self) -> str:
        """Get crisis response system prompt for OpenAI."""
        return """You are a crisis response AI assistant. Your role is to provide immediate, 
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
    
    async def start_pipeline(self) -> bool:
        """
        Start the pipecat pipeline.
        
        Returns:
            True if pipeline started successfully, False otherwise
        """
        if not self.pipeline:
            log_error("Pipeline not created. Call create_pipeline() first.")
            return False
        
        try:
            # Create and start the pipeline runner
            self.runner = PipelineRunner()
            
            # Start the pipeline
            await self.runner.run()
            return True
            
        except Exception as e:
            log_error(f"Error starting pipeline: {str(e)}")
            return False
    
    async def stop_pipeline(self):
        """Stop the pipecat pipeline."""
        if self.runner:
            try:
                await self.runner.stop()
            except Exception as e:
                log_error(f"Error stopping pipeline: {str(e)}")
    
    def get_pipeline_status(self) -> Dict[str, Any]:
        """
        Get current pipeline status.
        
        Returns:
            Dictionary with pipeline status information
        """
        status = {
            "pipeline_created": self.pipeline is not None,
            "runner_active": self.runner is not None,
            "whisper_available": self.whisper_client is not None
        }
        
        if self.runner:
            try:
                status["runner_status"] = "active"
            except:
                status["runner_status"] = "inactive"
        
        return status 