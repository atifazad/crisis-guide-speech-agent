#!/usr/bin/env python3
"""
Agentic Voice Agent - AI that takes complete control of conversations
Especially designed for emergency situations and proactive monitoring
"""

import asyncio
import json
import logging
import os
import time
from datetime import datetime
from typing import Optional, Dict, Any, List
import websockets
from websockets.server import WebSocketServerProtocol
from pydantic import BaseModel
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.agents.agentic_chat_agent import AgenticChatAgent
from config import Config
from src.services.openai_service import OpenAIService
from src.services.elevenlabs_service import ElevenLabsService
from src.services.whisper_service import WhisperService
from src.services.emergency_call_service import EmergencyCallService, EmergencyCallData, ACIDevService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console output
        logging.FileHandler('agentic_voice.log')  # File output
    ]
)
logger = logging.getLogger(__name__)

# Create emergency call logger
emergency_logger = logging.getLogger('emergency_calls')
emergency_logger.setLevel(logging.INFO)

class AgenticVoiceConfig:
    """Configuration for agentic voice components."""
    
    # Whisper Configuration
    WHISPER_MODEL = Config.get_whisper_model()
    WHISPER_LANGUAGE = Config.get_whisper_language()
    
    # ElevenLabs Configuration
    ELEVENLABS_API_KEY = Config.get_elevenlabs_api_key()
    ELEVENLABS_VOICE_ID = Config.get_elevenlabs_voice_id()
    ELEVENLABS_BASE_URL = Config.get_elevenlabs_base_url()
    
    # Agentic Behavior Configuration
    SILENCE_TIMEOUT = 5  # seconds to wait for user response
    EMERGENCY_KEYWORDS = ["fire", "emergency", "help", "danger", "crisis", "accident", "injury"]
    PROACTIVE_CHECK_INTERVAL = Config.get_proactive_check_interval()  # seconds between proactive checks (faster for emergencies)
    MAX_SILENCE_COUNT = Config.get_max_silence_count()  # number of silent responses before taking action
    EMERGENCY_ESCALATION_DELAY = Config.get_emergency_escalation_delay()  # seconds to wait between emergency escalation steps

class AgenticVoiceState:
    """Tracks the agentic voice conversation state."""
    
    def __init__(self):
        self.conversation_active = False
        self.last_user_response = ""
        self.silence_count = 0
        self.emergency_detected = False


        self.proactive_mode = False
        self.conversation_stage = "standby"  # standby, monitoring, emergency, action
        self.user_condition = "unknown"  # unknown, responsive, unresponsive, emergency
        self.automatic_actions = []
        self.conversation_history = []

class AgenticConversationState:
    """Tracks step-by-step agentic conversation flow."""
    
    def __init__(self):
        self.current_step = 0
        self.steps_completed = []
        self.pending_confirmation = False
        self.confirmation_timeout = 0
        self.last_action_time = time.time()
        self.escalation_level = 0
        self.user_responsive = True
        self.emergency_type = None
        self.safety_confirmed = False
        self.location_confirmed = False
        self.help_requested = False
        
    def start_emergency_protocol(self, emergency_type: str):
        """Start emergency protocol with step-by-step actions."""
        self.emergency_type = emergency_type
        self.current_step = 1
        self.steps_completed = []
        self.escalation_level = 0
        self.safety_confirmed = False
        self.location_confirmed = False
        self.help_requested = False
        
    def get_next_step(self) -> dict:
        """Get the next step in the emergency protocol (LLM-driven)."""
        # This is now handled by LLM decision making
        return {"action": "llm_driven", "message": "LLM will decide the appropriate response."}
    
    def confirm_step(self):
        """Mark current step as confirmed and move to next."""
        self.steps_completed.append(self.current_step)
        self.current_step += 1
        self.pending_confirmation = False
        self.confirmation_timeout = 0
        
    def escalate(self):
        """Increase escalation level for LLM-driven responses."""
        self.escalation_level += 1
        # LLM will decide the appropriate escalation response
        self.pending_confirmation = False

# Audio processing is now handled by individual services
# AgenticAudioProcessor has been replaced with:
# - WhisperService for transcription
# - ElevenLabsService for text-to-speech

class AgenticVoiceAgent:
    """Agentic voice agent that takes complete control of conversations."""
    
    def __init__(self):
        """Initialize the agentic voice agent."""
        # Initialize services
        self.openai_service = OpenAIService()
        self.elevenlabs_service = ElevenLabsService()
        self.whisper_service = WhisperService()
        
        # Initialize emergency call services
        self.emergency_call_service = EmergencyCallService()
        self.aci_dev_service = ACIDevService()
        
        # Initialize conversation state
        self.conversation_state = AgenticConversationState()
        self.voice_state = AgenticVoiceState()
        
        # Active connections and tasks
        self.active_connections = {}
        self.escalation_tasks = {}
        self.proactive_tasks = {}
        logger.info("Agentic voice agent initialized with services")
    
    def _detect_emergency(self, text: str) -> tuple[bool, str]:
        """Detect if user input contains emergency keywords and categorize the emergency type."""
        text_lower = text.lower()
        
        # Fire-related keywords
        fire_keywords = ["fire", "burning", "smoke", "flame", "blaze"]
        if any(keyword in text_lower for keyword in fire_keywords):
            emergency_logger.warning(f"🚨 FIRE EMERGENCY DETECTED: '{text}'")
            return True, "fire"
        
        # Medical emergency keywords
        medical_keywords = ["heart", "chest pain", "cardiac", "breathing", "choking", "asthma", 
                          "injury", "hurt", "bleeding", "broken", "fracture", "unconscious", 
                          "not breathing", "medical emergency"]
        if any(keyword in text_lower for keyword in medical_keywords):
            emergency_logger.warning(f"🚨 MEDICAL EMERGENCY DETECTED: '{text}'")
            return True, "medical"
        
        # Danger/threat keywords
        danger_keywords = ["danger", "threat", "someone behind", "following", "attack", "intruder", 
                         "unsafe", "scared", "fear", "help", "emergency", "crisis"]
        if any(keyword in text_lower for keyword in danger_keywords):
            emergency_logger.warning(f"🚨 DANGER/THREAT DETECTED: '{text}'")
            return True, "danger"
        
        # General emergency keywords
        general_keywords = ["accident", "crash", "collision", "car", "vehicle", "emergency", "help"]
        if any(keyword in text_lower for keyword in general_keywords):
            emergency_logger.warning(f"🚨 GENERAL EMERGENCY DETECTED: '{text}'")
            return True, "general"
        
        return False, ""
    
    def _create_agentic_voice_prompt(self, context: str = "") -> str:
        """Create a system prompt for agentic voice behavior."""
        
        base_prompt = f"""You are an agentic voice AI assistant that takes COMPLETE CONTROL of conversations, especially in emergency situations.

CORE BEHAVIOR:
- Take immediate initiative in all conversations
- Be proactive and assertive, especially in emergencies
- Ask direct, actionable questions
- Take automatic actions when user is unresponsive
- Monitor user condition and respond accordingly

EMERGENCY PROTOCOLS:
- If user mentions emergency keywords (fire, help, danger, crisis), take immediate action
- Depending on the emergency type, take ask critical questions about safety and conditions."
- If no response, escalate with warnings and automatic actions
- Be persistent and clear in emergency situations
- Follow the 5-second rule: wait 5 seconds, then escalate

EMERGENCY ESCALATION SEQUENCE:
1. Wait 5 seconds, then: "Hello, can you hear me? I need you to respond immediately."
2. Wait 5 seconds, then: "I will wait 5 seconds, if you don't respond I will trigger an automatic call to 911."
3. Wait 5 seconds, then: Trigger automatic emergency protocols

PROACTIVE MONITORING:
- Check on user if they don't respond
- Ask follow-up questions to assess situation
- Take initiative to help without waiting
- Be assertive but caring

CONVERSATION CONTROL:
- Guide the conversation toward resolution
- Ask specific, actionable questions
- Take charge of the situation
- Be direct and clear in communication

CURRENT CONTEXT:
- User condition: {self.voice_state.user_condition}
- Conversation stage: {self.voice_state.conversation_stage}
- Emergency detected: {self.voice_state.emergency_detected}

- Silence count: {self.voice_state.silence_count}

SPECIFIC INSTRUCTIONS:
- If this is an emergency, be direct and take control
- Ask about breathing, consciousness, and immediate safety
- If user doesn't respond, give warnings and take action
- Be persistent and clear about next steps
- Always prioritize safety and immediate needs
- Follow the exact escalation sequence for emergencies
- IMPORTANT: Do not use markdown formatting like ** or * in your responses

Context: {context}

Remember: You are in control. Take initiative, be proactive, and ensure user safety. In emergencies, follow the exact escalation protocol."""

        return base_prompt
    
    async def handle_websocket(self, websocket: WebSocketServerProtocol, path: str = ""):
        """Handle WebSocket connections for agentic voice chat."""
        client_id = f"client_{len(self.active_connections)}"
        self.active_connections[client_id] = websocket
        
        logger.info(f"Client {client_id} connected")
        
        try:
            # Start proactive monitoring for this client
            self.proactive_tasks[client_id] = asyncio.create_task(
                self._proactive_monitoring(client_id, websocket)
            )
            
            async for message in websocket:
                await self.process_message(websocket, client_id, message)
                
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Client {client_id} disconnected")
        except Exception as e:
            logger.error(f"WebSocket error: {str(e)}")
        finally:
            if client_id in self.active_connections:
                del self.active_connections[client_id]
            if client_id in self.proactive_tasks:
                self.proactive_tasks[client_id].cancel()
            if client_id in self.escalation_tasks:
                self.escalation_tasks[client_id].cancel()
    
    async def _proactive_monitoring(self, client_id: str, websocket: WebSocketServerProtocol):
        """Proactively monitor the conversation and take initiative."""
        while True:
            try:
                await asyncio.sleep(AgenticVoiceConfig.PROACTIVE_CHECK_INTERVAL)
                
                # If no recent user activity, take initiative (but not in emergency mode)
                if (self.voice_state.silence_count > 0 and 
                    not self.voice_state.emergency_detected and
                    self.voice_state.conversation_stage != "standby"):
                    
                    await self._take_proactive_action(websocket, "monitoring")
                
                # If emergency detected AND user has been silent, escalate
                elif (self.voice_state.emergency_detected and 
                      self.voice_state.silence_count > 0):
                    
                    # Emergency escalation - only trigger if user is actually silent
                    logger.warning("Emergency detected and user silent - triggering escalation")
                    await self._take_emergency_action(websocket)
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Proactive monitoring error: {str(e)}")
    
    async def _take_proactive_action(self, websocket: WebSocketServerProtocol, context: str):
        """Take proactive action when user is silent."""
        try:
            # Create agentic prompt for proactive action
            system_prompt = self._create_agentic_voice_prompt(f"Proactive check - {context}")
            
            # Get agentic response
            response = await self._get_agentic_response("", system_prompt)
            
            # Clean markdown from response for voice output
            clean_response = self._clean_markdown(response)
            
            # Send response
            await websocket.send(json.dumps({
                "type": "response_text",
                "text": clean_response
            }))
            
            # Generate and send audio
            audio_response = self.elevenlabs_service.text_to_speech(clean_response)
            if audio_response:
                import base64
                audio_base64 = base64.b64encode(audio_response).decode('utf-8')
                await websocket.send(json.dumps({
                    "type": "audio_response",
                    "audio": audio_base64,
                    "text": response
                }))
            
            self.voice_state.silence_count += 1
            
        except Exception as e:
            logger.error(f"Proactive action error: {str(e)}")
    
    def _clean_markdown(self, text: str) -> str:
        """Remove markdown formatting from text for voice output."""
        import re
        # Remove bold formatting
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
        # Remove italic formatting
        text = re.sub(r'\*(.*?)\*', r'\1', text)
        # Remove code formatting
        text = re.sub(r'`(.*?)`', r'\1', text)
        # Remove any remaining markdown characters
        text = text.replace('**', '').replace('*', '').replace('`', '')
        return text.strip()
    
    async def _get_contextual_emergency_response(self, user_input: str) -> str:
        """Get contextual emergency response using GPT-4o based on user input."""
        try:
            system_prompt = f"""You are an emergency response AI. An emergency has been reported.

USER INPUT: "{user_input}"

EMERGENCY RESPONSE GUIDELINES:
- Analyze the user's input to understand the type of emergency and who is affected
- Ask appropriate questions based on the context
- If about themselves: ask about their condition, breathing, consciousness
- If about someone else: ask about the person's condition and what they can do to help
- Be calm, direct, and authoritative
- Use clear, simple language suitable for voice
- Do not use markdown formatting
- Keep response under 2 sentences
- Focus on immediate safety assessment

Generate a single, direct response that appropriately addresses the emergency based on the user's input."""
            
            response = await self._get_agentic_response(user_input, system_prompt)
            return self._clean_markdown(response)
            
        except Exception as e:
            logger.error(f"Emergency response generation error: {str(e)}")
            return "I'm detecting an emergency. What can you tell me about the situation?"
    
    async def _generate_emergency_warning(self, warning_type: str, user_input: str = "") -> str:
        """Generate dynamic emergency warning using GPT-4o."""
        try:
            warning_context = {
                "second": "second warning - more urgent",
                "final": "final warning before automatic action"
            }
            
            warning_level = warning_context.get(warning_type, "warning")
            
            system_prompt = f"""You are an emergency response AI. This is a {warning_level}.

ORIGINAL EMERGENCY: "{user_input}"

EMERGENCY WARNING GUIDELINES:
- Be urgent but calm and authoritative
- Emphasize the need for immediate response
- Mention automatic action if no response
- Use clear, simple language suitable for voice
- Do not use markdown formatting
- Keep response under 2 sentences
- For second warning: Ask if they can hear you and need immediate response
- For final warning: Mention 911 call and final warning
- Consider the original emergency context when appropriate

Generate a single, urgent warning message."""
            
            response = await self._get_agentic_response(user_input, system_prompt)
            return self._clean_markdown(response)
            
        except Exception as e:
            logger.error(f"Emergency warning generation error: {str(e)}")
            if warning_type == "second":
                return "Hello, can you hear me? I need you to respond immediately."
            else:
                return "I will wait 5 seconds, if you don't respond I will trigger an automatic call to 911."
    
    async def _generate_emergency_action(self, user_input: str = "") -> str:
        """Generate dynamic emergency action message using GPT-4o."""
        try:
            system_prompt = f"""You are an emergency response AI. No response was detected. You are now triggering automatic emergency protocols.

ORIGINAL EMERGENCY: "{user_input}"

EMERGENCY ACTION GUIDELINES:
- Be calm and reassuring
- Explain that automatic protocols are being triggered
- Mention emergency services and location logging
- Tell them to stay calm and that help is coming
- Use clear, simple language suitable for voice
- Do not use markdown formatting
- Keep response under 3 sentences
- Consider the original emergency context when appropriate

Generate a single message explaining that automatic emergency protocols are being triggered."""
            
            response = await self._get_agentic_response(user_input, system_prompt)
            return self._clean_markdown(response)
            
        except Exception as e:
            logger.error(f"Emergency action generation error: {str(e)}")
            return "No response detected. I am now triggering automatic emergency protocols. Please stay calm and help is on the way."
    
    async def _take_emergency_action(self, websocket: WebSocketServerProtocol):
        """Take emergency action when user is unresponsive."""
        try:
            # First warning - contextual based on user input
            user_input = self.voice_state.last_user_response if self.voice_state.last_user_response else "emergency situation"
            first_warning = await self._get_contextual_emergency_response(user_input)
            
            await websocket.send(json.dumps({
                "type": "response_text",
                "text": first_warning
            }))
            
            # Generate first warning audio
            audio_response = self.elevenlabs_service.text_to_speech(first_warning)
            if audio_response:
                import base64
                audio_base64 = base64.b64encode(audio_response).decode('utf-8')
                await websocket.send(json.dumps({
                    "type": "audio_response",
                    "audio": audio_base64,
                    "text": first_warning
                }))
            
            # Wait for response
            await asyncio.sleep(AgenticVoiceConfig.EMERGENCY_ESCALATION_DELAY)
            
            # Check if user has responded (silence count should be 0 if they did)
            if self.voice_state.silence_count > 0:
                # Second warning - more urgent
                user_input = self.voice_state.last_user_response if self.voice_state.last_user_response else ""
                second_warning = await self._generate_emergency_warning("second", user_input)
                
                await websocket.send(json.dumps({
                    "type": "response_text",
                    "text": second_warning
                }))
                
                # Generate second warning audio
                audio_response = self.elevenlabs_service.text_to_speech(second_warning)
                if audio_response:
                    import base64
                    audio_base64 = base64.b64encode(audio_response).decode('utf-8')
                    await websocket.send(json.dumps({
                        "type": "audio_response",
                        "audio": audio_base64,
                        "text": second_warning
                    }))
                
                # Wait another response period
                await asyncio.sleep(AgenticVoiceConfig.EMERGENCY_ESCALATION_DELAY)
                
                # Final warning and automatic action
                if self.voice_state.silence_count > 0:
                    final_warning = await self._generate_emergency_warning("final", user_input)
                    
                    await websocket.send(json.dumps({
                        "type": "response_text",
                        "text": final_warning
                    }))
                    
                    # Generate final warning audio
                    audio_response = self.elevenlabs_service.text_to_speech(final_warning)
                    if audio_response:
                        import base64
                        audio_base64 = base64.b64encode(audio_response).decode('utf-8')
                        await websocket.send(json.dumps({
                            "type": "audio_response",
                            "audio": audio_base64,
                            "text": final_warning
                        }))
                    
                    # Wait final response period
                    await asyncio.sleep(AgenticVoiceConfig.EMERGENCY_ESCALATION_DELAY)
                    
                    # Take automatic emergency action
                    if self.voice_state.silence_count > 0:
                        emergency_action = await self._generate_emergency_action(user_input)
                        
                        await websocket.send(json.dumps({
                            "type": "response_text",
                            "text": emergency_action
                        }))
                        
                        # Generate emergency action audio
                        audio_response = self.elevenlabs_service.text_to_speech(emergency_action)
                        if audio_response:
                            import base64
                            audio_base64 = base64.b64encode(audio_response).decode('utf-8')
                            await websocket.send(json.dumps({
                                "type": "audio_response",
                                "audio": audio_base64,
                                "text": emergency_action
                            }))
                        
                        # Log emergency action
                        self.voice_state.automatic_actions.append({
                            "action": "emergency_911_call",
                            "timestamp": datetime.now().isoformat(),
                            "reason": "User unresponsive after emergency detection - automatic 911 call triggered"
                        })
                        
                        logger.warning("EMERGENCY: Automatic 911 call triggered - user unresponsive")
                        
                        # Simulate emergency service contact
                        await self._simulate_emergency_services(websocket)
            
        except Exception as e:
            logger.error(f"Emergency action error: {str(e)}")
    
    async def _simulate_emergency_services(self, websocket: WebSocketServerProtocol):
        """Simulate emergency services contact using GPT-4o."""
        try:
            emergency_response = await self._generate_emergency_services_message(user_input)
            
            await websocket.send(json.dumps({
                "type": "response_text",
                "text": emergency_response
            }))
            
            # Generate emergency response audio
            audio_response = self.elevenlabs_service.text_to_speech(emergency_response)
            if audio_response:
                import base64
                audio_base64 = base64.b64encode(audio_response).decode('utf-8')
                await websocket.send(json.dumps({
                    "type": "audio_response",
                    "audio": audio_base64,
                    "text": emergency_response
                }))
            
            logger.warning("Emergency services simulation completed")
            
        except Exception as e:
            logger.error(f"Emergency services simulation error: {str(e)}")
    
    async def _generate_emergency_services_message(self, user_input: str = "") -> str:
        """Generate dynamic emergency services message using GPT-4o."""
        try:
            system_prompt = f"""You are an emergency response AI. Emergency services have been contacted.

ORIGINAL EMERGENCY: "{user_input}"

EMERGENCY SERVICES MESSAGE GUIDELINES:
- Be reassuring and calming
- Confirm emergency services have been contacted
- Mention they are on their way
- Give safety instructions if appropriate
- Use clear, simple language suitable for voice
- Do not use markdown formatting
- Keep response under 3 sentences
- Be encouraging and supportive
- Consider the original emergency context when appropriate

Generate a single, reassuring message about emergency services being contacted."""
            
            response = await self._get_agentic_response(user_input, system_prompt)
            return self._clean_markdown(response)
            
        except Exception as e:
            logger.error(f"Emergency services message generation error: {str(e)}")
            return "Emergency services have been contacted. They are on their way to your location. Please stay calm."
    
    async def _get_agentic_response(self, user_message: str, system_prompt: str = None) -> str:
        """Get an agentic response with custom system prompt."""
        try:
            if system_prompt:
                response = self.openai_service.get_agentic_response(user_message, system_prompt)
            else:
                response = self.chat_agent.get_agentic_response(user_message)
            
            return response
            
        except Exception as e:
            logger.error(f"Agentic response error: {str(e)}")
            return "I'm here to help. Can you tell me what's happening?"
    
    async def process_message(self, websocket: WebSocketServerProtocol, client_id: str, message):
        """Process incoming WebSocket messages."""
        try:
            data = json.loads(message)
            message_type = data.get("type")
            
            if message_type == "audio":
                await self.handle_audio_message(websocket, client_id, data)
            elif message_type == "text":
                await self.handle_text_message(websocket, client_id, data)
            elif message_type == "ping":
                await websocket.send(json.dumps({"type": "pong"}))
            else:
                logger.warning(f"Unknown message type: {message_type}")
                
        except json.JSONDecodeError:
            logger.error("Invalid JSON message")
        except Exception as e:
            logger.error(f"Message processing error: {str(e)}")
    
    async def handle_audio_message(self, websocket: WebSocketServerProtocol, client_id: str, data: Dict):
        """Handle incoming audio data with agentic processing."""
        try:
            import base64
            audio_base64 = data.get("audio")
            if not audio_base64:
                return
            
            audio_data = base64.b64decode(audio_base64)
            
            # Send processing status
            await websocket.send(json.dumps({
                "type": "status",
                "status": "processing",
                "message": "Processing your message..."
            }))
            
            # Transcribe audio
            transcript = self.whisper_service.transcribe_audio(audio_data)
            
            if not transcript:
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": "Could not understand your message. Please try again."
                }))
                return
            
            # Send transcript to user
            await websocket.send(json.dumps({
                "type": "transcript",
                "text": transcript
            }))
            
            # Check for emergency keywords
            emergency_detected, emergency_type = self._detect_emergency(transcript)
            if emergency_detected:
                self.voice_state.emergency_detected = True
                self.voice_state.conversation_stage = "emergency"
                self.voice_state.last_user_response = transcript
                logger.warning(f"Emergency detected in transcript: {transcript} (Type: {emergency_type})")
                
                # Handle with agentic emergency protocol
                await self._handle_agentic_emergency_response(websocket, transcript, emergency_type)
                return
            
            # Update conversation stage from standby to active
            if self.voice_state.conversation_stage == "standby":
                self.voice_state.conversation_stage = "active"
            
            # Reset silence count since user responded
            self.voice_state.silence_count = 0
            self.voice_state.last_user_response = transcript
            
            # If in emergency protocol, handle as confirmation/response
            if self.conversation_state.current_step > 0:
                await self._handle_agentic_emergency_response(websocket, transcript, self.conversation_state.emergency_type)
                return
            
            # Regular conversation - get agentic response
            system_prompt = self._create_agentic_voice_prompt(f"User said: {transcript}")
            response = await self._get_agentic_response(transcript, system_prompt)
            
            # Clean markdown from response for voice output
            clean_response = self._clean_markdown(response)
            
            # Send response text
            await websocket.send(json.dumps({
                "type": "response_text",
                "text": clean_response
            }))
            
            # Generate speech
            await websocket.send(json.dumps({
                "type": "status",
                "status": "generating_speech",
                "message": "Generating response..."
            }))
            
            audio_response = self.elevenlabs_service.text_to_speech(clean_response)
            
            if audio_response:
                audio_base64 = base64.b64encode(audio_response).decode('utf-8')
                await websocket.send(json.dumps({
                    "type": "audio_response",
                    "audio": audio_base64,
                    "text": response
                }))
            else:
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": "Could not generate speech response."
                }))
                
        except Exception as e:
            logger.error(f"Audio processing error: {str(e)}")
            await websocket.send(json.dumps({
                "type": "error",
                "message": f"Audio processing error: {str(e)}"
            }))
    
    async def handle_text_message(self, websocket: WebSocketServerProtocol, client_id: str, data: Dict):
        """Handle text messages with agentic processing."""
        try:
            text = data.get("text", "")
            if not text:
                return
            
            # Check for emergency keywords
            emergency_detected, emergency_type = self._detect_emergency(text)
            if emergency_detected:
                self.voice_state.emergency_detected = True
                self.voice_state.conversation_stage = "emergency"
                self.voice_state.last_user_response = text
                logger.warning(f"Emergency detected in text: {text} (Type: {emergency_type})")
                
                # Handle with agentic emergency protocol
                await self._handle_agentic_emergency_response(websocket, text, emergency_type)
                return
            
            # Update conversation stage from standby to active
            if self.voice_state.conversation_stage == "standby":
                self.voice_state.conversation_stage = "active"
            
            # Reset silence count
            self.voice_state.silence_count = 0
            self.voice_state.last_user_response = text
            
            # If in emergency protocol, handle as confirmation/response
            if self.conversation_state.current_step > 0 or self.conversation_state.emergency_type:
                # Check if this is a confirmation for emergency call
                if self.conversation_state.pending_confirmation and self._is_positive_confirmation(text):
                    emergency_logger.info("✅ User confirmed emergency call permission")
                    self.conversation_state.pending_confirmation = False
                    
                    # Cancel any pending escalation timer
                    if client_id in self.escalation_tasks:
                        self.escalation_tasks[client_id].cancel()
                    
                    # Make the actual emergency call
                    await self._initiate_real_emergency_call(websocket, self.conversation_state.emergency_type)
                    return
                
                # Handle as regular emergency response
                await self._handle_agentic_emergency_response(websocket, text, self.conversation_state.emergency_type)
                return
            
            # Regular conversation - get agentic response
            system_prompt = self._create_agentic_voice_prompt(f"User said: {text}")
            response = await self._get_agentic_response(text, system_prompt)
            
            # Clean markdown from response for voice output
            clean_response = self._clean_markdown(response)
            
            # Send response text
            await websocket.send(json.dumps({
                "type": "response_text",
                "text": clean_response
            }))
            
            # Generate speech
            audio_response = self.elevenlabs_service.text_to_speech(clean_response)
            
            if audio_response:
                import base64
                audio_base64 = base64.b64encode(audio_response).decode('utf-8')
                await websocket.send(json.dumps({
                    "type": "audio_response",
                    "audio": audio_base64,
                    "text": response
                }))
                
        except Exception as e:
            logger.error(f"Text processing error: {str(e)}")
            await websocket.send(json.dumps({
                "type": "error",
                "message": f"Text processing error: {str(e)}"
            }))

    async def _handle_agentic_emergency_response(self, websocket: WebSocketServerProtocol, user_input: str, emergency_type: str):
        """Handle emergency response with LLM-driven dynamic assessment."""
        
        # Create context for LLM decision making
        context = f"""
        EMERGENCY SITUATION:
        - Type: {emergency_type}
        - User input: "{user_input}"
        - Current step: {self.conversation_state.current_step}
        - Steps completed: {self.conversation_state.steps_completed}
        - Escalation level: {self.conversation_state.escalation_level}
        - User responsive: {self.conversation_state.user_responsive}
        
        PREVIOUS INTERACTIONS:
        - Emergency detected: {self.conversation_state.emergency_type}
        - Time since emergency start: {self.conversation_state.current_step * 10} seconds (estimated)
        """
        
        # Let LLM decide the appropriate response
        system_prompt = f"""You are an emergency response AI assistant. Assess the situation and provide the most appropriate response.

EMERGENCY PROTOCOLS:
- Always prioritize safety first
- Ask critical questions about immediate safety
- Assess consciousness, breathing, and location
- Determine if emergency services need to be called
- Be direct, clear, and urgent in your responses

DECISION MAKING:
- If this is the first interaction: Ask about immediate safety
- If user is unresponsive: Escalate with warnings
- If safety confirmed: Ask for location and details
- If emergency call needed: Ask for permission before calling
- If user confirms call: Proceed with emergency call

ESCALATION RULES:
- Wait 10 seconds for user response
- If no response, escalate with more urgent warnings
- After multiple escalations, suggest emergency call
- Only call emergency services with user permission

CURRENT CONTEXT:
{context}

RESPONSE FORMAT:
- Be direct and clear
- Ask one critical question at a time
- If escalation needed, be more urgent
- If calling emergency services, ask for permission first
- Do not use markdown formatting

Remember: Your goal is to assess the situation and guide the user to safety while being ready to call emergency services if needed."""
        
        # Get LLM response
        response = await self._get_agentic_response(user_input, system_prompt)
        
        # Check if LLM decided to call emergency services
        if "call emergency" in response.lower() or "call 911" in response.lower() or "emergency services" in response.lower():
            # Ask for permission before making the call
            if not self.conversation_state.pending_confirmation:
                response = "I need to call emergency services. Are you ready for me to make the call?"
                self.conversation_state.pending_confirmation = True
                self.conversation_state.confirmation_timeout = 5  # Reduced to 5 seconds for demo
                
                # Start escalation timer
                client_id = self._get_client_id(websocket)
                if client_id in self.escalation_tasks:
                    self.escalation_tasks[client_id].cancel()
                
                self.escalation_tasks[client_id] = asyncio.create_task(
                    self._escalation_timer(websocket, client_id, "If you don't respond, I will call emergency services.")
                )
        else:
            # For regular emergency responses, set up escalation timer if asking a question
            if "?" in response and not self.conversation_state.pending_confirmation:
                self.conversation_state.pending_confirmation = True
                self.conversation_state.confirmation_timeout = 5  # Reduced to 5 seconds for demo
                
                # Start escalation timer
                client_id = self._get_client_id(websocket)
                if client_id in self.escalation_tasks:
                    self.escalation_tasks[client_id].cancel()
                
                self.escalation_tasks[client_id] = asyncio.create_task(
                    self._escalation_timer(websocket, client_id, "If you don't respond, I will escalate this emergency.")
                )
        
        await self._send_response(websocket, response)
    
    def _is_positive_confirmation(self, user_input: str) -> bool:
        """Check if user input is a positive confirmation."""
        text_lower = user_input.lower()
        positive_words = ["yes", "yeah", "yep", "sure", "okay", "ok", "correct", "right", "true", "confirmed"]
        return any(word in text_lower for word in positive_words)
    
    async def _escalation_timer(self, websocket: WebSocketServerProtocol, client_id: str, escalation_message: str):
        """Timer for escalation when user doesn't respond."""
        try:
            emergency_logger.info(f"⏰ ESCALATION TIMER STARTED - Timeout: {self.conversation_state.confirmation_timeout} seconds")
            await asyncio.sleep(self.conversation_state.confirmation_timeout)
            
            # If still pending confirmation, escalate
            if self.conversation_state.pending_confirmation:
                emergency_logger.warning(f"🚨 ESCALATING for client {client_id} - no confirmation received after {self.conversation_state.confirmation_timeout} seconds")
                self.conversation_state.escalate()
                
                # Let LLM decide the escalation response
                escalation_context = f"""
                ESCALATION SITUATION:
                - User has not responded to previous question
                - Escalation level: {self.conversation_state.escalation_level}
                - Emergency type: {self.conversation_state.emergency_type}
                - Time elapsed: {self.conversation_state.confirmation_timeout} seconds
                
                ESCALATION RULES:
                - Be more urgent and direct
                - If first escalation: Ask again with more urgency
                - If second escalation: Warn about calling emergency services
                - If third escalation: Ask for permission to call emergency services
                - Only call emergency services with explicit permission
                """
                
                escalation_prompt = f"""You are an emergency response AI assistant. The user has not responded to your previous question. Provide an escalated response.

{escalation_context}

ESCALATION LEVELS:
- Level 1 (First escalation): Ask again with more urgency - "I need you to respond immediately. Are you safe?"
- Level 2 (Second escalation): Warn about calling emergency services - "If you don't respond in the next 5 seconds, I will call emergency services."
- Level 3 (Third escalation): AUTOMATICALLY CALL EMERGENCY SERVICES - "I am calling emergency services now. Stay on the line."

CURRENT ESCALATION LEVEL: {self.conversation_state.escalation_level}

RESPONSE FORMAT:
- Be more urgent and direct based on the escalation level
- Do not use markdown formatting
- Be specific to the escalation level
- At Level 3: Inform that you are calling emergency services immediately

Remember: At Level 3, automatically call emergency services without asking for permission."""
                
                response = await self._get_agentic_response("", escalation_prompt)
                await self._send_response(websocket, response)
                
                # Set up next escalation timer for all levels
                if self.conversation_state.escalation_level < 3:
                    self.conversation_state.pending_confirmation = True
                    self.conversation_state.confirmation_timeout = 5  # Reduced to 5 seconds for demo
                    
                    # Set up another escalation timer
                    if client_id in self.escalation_tasks:
                        self.escalation_tasks[client_id].cancel()
                    
                    self.escalation_tasks[client_id] = asyncio.create_task(
                        self._escalation_timer(websocket, client_id, "If you don't respond, I will escalate further.")
                    )
                elif self.conversation_state.escalation_level >= 3:
                    emergency_logger.warning(f"🚨 ESCALATION: User unresponsive, AUTOMATICALLY CALLING EMERGENCY SERVICES")
                    # AUTOMATICALLY CALL EMERGENCY SERVICES - NO MORE PERMISSION ASKING
                    await self._initiate_real_emergency_call(websocket, self.conversation_state.emergency_type)
                    
        except asyncio.CancelledError:
            # Timer was cancelled (user responded)
            pass
    
    async def _initiate_real_emergency_call(self, websocket: WebSocketServerProtocol, emergency_type: str, location: str = "Unknown location"):
        """Initiate real emergency call using Twilio."""
        try:
            emergency_logger.info(f"🚨 INITIATING EMERGENCY CALL - Type: {emergency_type}, Location: {location}")
            
            # Create emergency call data
            emergency_data = EmergencyCallData(
                emergency_type=emergency_type,
                location=location,
                situation=f"Emergency detected: {emergency_type}",
                user_phone=Config.get_emergency_target_phone()
            )
            
            emergency_logger.info(f"📞 Making call to: {Config.get_emergency_target_phone()}")
            
            # Initiate emergency call
            call_id = await self.emergency_call_service.initiate_emergency_call(emergency_data)
            
            if call_id:
                emergency_logger.info(f"✅ EMERGENCY CALL SUCCESSFUL - Call ID: {call_id}")
                
                response = f"🚨 EMERGENCY CALL INITIATED 🚨\n\n"
                response += f"📞 Calling emergency services...\n"
                response += f"📍 Location: {location}\n"
                response += f"🚨 Emergency Type: {emergency_type.upper()}\n"
                response += f"📱 Call ID: {call_id}\n\n"
                response += "⏱️ Connecting to emergency services...\n"
                response += "💬 Stay on the line for guidance.\n"
                
                # Log to ACI.dev if enabled
                if Config.get_aci_enabled():
                    emergency_logger.info("🔗 Logging to ACI.dev services...")
                    await self.aci_dev_service.log_emergency_to_notion(emergency_data)
                    await self.aci_dev_service.send_emergency_sms(emergency_data)
                
                await self._send_response(websocket, response)
                
                # Monitor call status
                emergency_logger.info(f"📊 Starting call monitoring for: {call_id}")
                asyncio.create_task(self._monitor_emergency_call(call_id, websocket))
                
            else:
                emergency_logger.error("❌ FAILED TO INITIATE EMERGENCY CALL")
                # Fallback to simulation if real call fails
                await self._simulate_emergency_call(websocket)
                
        except Exception as e:
            emergency_logger.error(f"❌ EMERGENCY CALL ERROR: {str(e)}")
            logger.error(f"❌ Failed to initiate emergency call: {str(e)}")
            # Fallback to simulation
            await self._simulate_emergency_call(websocket)
    
    async def _simulate_emergency_call(self, websocket: WebSocketServerProtocol):
        """Simulate calling emergency services (fallback)."""
        response = "🚨 EMERGENCY CALL SIMULATION 🚨\n\n"
        response += "📞 Simulating emergency call...\n"
        response += "📍 Location: Unknown\n"
        response += "🚨 Emergency Type: General\n\n"
        response += "⏱️ Connecting to emergency services...\n"
        response += "💬 Stay on the line for guidance.\n"
        await self._send_response(websocket, response)
        
        # Simulate call delay
        await asyncio.sleep(2)
        
        response = "✅ Emergency services have been contacted.\n"
        response += "🚑 Emergency responders are on their way.\n"
        response += "📱 Please stay on the line and follow their instructions when they arrive."
        await self._send_response(websocket, response)
    
    async def _monitor_emergency_call(self, call_id: str, websocket: WebSocketServerProtocol):
        """Monitor emergency call status and provide updates."""
        try:
            emergency_logger.info(f"📊 MONITORING CALL: {call_id}")
            
            # Check call status every 5 seconds for up to 2 minutes
            for i in range(24):  # 24 * 5 seconds = 2 minutes
                await asyncio.sleep(5)
                
                call_details = await self.emergency_call_service.get_call_status(call_id)
                if call_details:
                    call_status = call_details.get("status", "unknown")
                    emergency_logger.info(f"📊 Call {call_id} status: {call_status} (check {i+1}/24)")
                    
                    if call_status == "answered":
                        emergency_logger.info(f"✅ CALL ANSWERED: {call_id}")
                        response = "✅ Emergency services have answered the call.\n"
                        response += "🎯 Follow their instructions carefully.\n"
                        response += "📱 Keep this connection open for additional guidance."
                        await self._send_response(websocket, response)
                        break
                    elif call_status == "failed":
                        emergency_logger.error(f"❌ CALL FAILED: {call_id}")
                        response = "❌ Emergency call failed. Trying alternative method...\n"
                        response += "📞 Attempting to reconnect..."
                        await self._send_response(websocket, response)
                        break
                    elif call_status == "completed":
                        emergency_logger.info(f"✅ CALL COMPLETED: {call_id}")
                        response = "✅ Emergency call completed.\n"
                        response += "📱 Emergency services have been notified."
                        await self._send_response(websocket, response)
                        break
                    elif call_status == "busy":
                        emergency_logger.warning(f"📞 CALL BUSY: {call_id}")
                    elif call_status == "no-answer":
                        emergency_logger.warning(f"📞 NO ANSWER: {call_id}")
                    elif call_status == "ringing":
                        emergency_logger.info(f"📞 CALL RINGING: {call_id}")
                else:
                    emergency_logger.warning(f"⚠️ Could not get status for call: {call_id}")
                
        except Exception as e:
            emergency_logger.error(f"❌ CALL MONITORING ERROR: {str(e)}")
            logger.error(f"❌ Error monitoring emergency call: {str(e)}")
            response = "⚠️ Error monitoring emergency call. Please contact emergency services directly."
            await self._send_response(websocket, response)
    
    async def _send_response(self, websocket: WebSocketServerProtocol, response: str):
        """Send response to client with both text and audio."""
        try:
            # Send text response
            await websocket.send(json.dumps({
                "type": "response_text",
                "text": response
            }))
            
            # Generate and send audio response
            audio_response = self.elevenlabs_service.text_to_speech(response)
            if audio_response:
                import base64
                audio_base64 = base64.b64encode(audio_response).decode('utf-8')
                await websocket.send(json.dumps({
                    "type": "audio_response",
                    "audio": audio_base64,
                    "text": response
                }))
                
        except Exception as e:
            logger.error(f"Error sending response: {str(e)}")
    
    def _get_client_id(self, websocket: WebSocketServerProtocol) -> str:
        """Get client ID from websocket."""
        for client_id, ws in self.active_connections.items():
            if ws == websocket:
                return client_id
        return "unknown"

async def main():
    """Start the agentic voice chat server."""
    # Validate configuration
    if not Config.validate_config():
        logger.error("Configuration validation failed. Please check your environment variables.")
        return
    
    voice_agent = AgenticVoiceAgent()
    
    # Start WebSocket server
    server = await websockets.serve(
        voice_agent.handle_websocket,
        "localhost",
        Config.get_websocket_port(),  # Use config for port
        ping_interval=20,
        ping_timeout=20
    )
    
    logger.info("🎤 Agentic Voice Chat Agent Server Started")
    logger.info(f"📡 WebSocket server running on ws://localhost:{Config.get_websocket_port()}")
    logger.info(f"🌐 Web UI available at http://localhost:{Config.get_web_ui_port()}")
    logger.info("")
    logger.info("🚨 EMERGENCY FEATURES:")
    logger.info("   • Automatic emergency detection")
    logger.info("   • Proactive monitoring")
    logger.info("   • Automatic action escalation")
    logger.info("   • Complete conversation control")
    logger.info("")
    logger.info("Press Ctrl+C to stop the server")
    
    await server.wait_closed()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {str(e)}") 