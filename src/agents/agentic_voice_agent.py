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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        """Get the next step in the emergency protocol."""
        if self.emergency_type == "fire":
            return self._get_fire_protocol_step()
        elif self.emergency_type == "medical":
            return self._get_medical_protocol_step()
        elif self.emergency_type == "danger":
            return self._get_danger_protocol_step()
        else:
            return self._get_general_emergency_step()
    
    def _get_fire_protocol_step(self) -> dict:
        """Get fire emergency protocol steps."""
        steps = {
            1: {
                "action": "immediate_safety",
                "message": "I understand there's a fire. First, are you and everyone else safely out of the building?",
                "confirmation_required": True,
                "timeout": 10,
                "escalation": "If you don't respond in 10 seconds, I'll assume you need immediate help and call 911."
            },
            2: {
                "action": "location_confirmation",
                "message": "Good. Now, what's your exact location? I need your address to send help.",
                "confirmation_required": True,
                "timeout": 15,
                "escalation": "I need your location to send firefighters. Please provide your address."
            },
            3: {
                "action": "fire_details",
                "message": "Can you tell me: Is the fire contained to one room, or has it spread? Are there any people still inside?",
                "confirmation_required": True,
                "timeout": 20,
                "escalation": "This information is critical for emergency responders."
            },
            4: {
                "action": "call_emergency",
                "message": "I'm calling 911 now. Stay on the line and follow my instructions.",
                "confirmation_required": False,
                "timeout": 5,
                "escalation": "Emergency services are being contacted."
            }
        }
        return steps.get(self.current_step, {"action": "complete", "message": "Emergency protocol complete."})
    
    def _get_medical_protocol_step(self) -> dict:
        """Get medical emergency protocol steps."""
        steps = {
            1: {
                "action": "consciousness_check",
                "message": "I understand there's a medical emergency. First, is the person conscious and breathing?",
                "confirmation_required": True,
                "timeout": 10,
                "escalation": "If you don't respond, I'll call 911 immediately."
            },
            2: {
                "action": "symptoms_assessment",
                "message": "What are the main symptoms? Chest pain, difficulty breathing, bleeding, or something else?",
                "confirmation_required": True,
                "timeout": 15,
                "escalation": "I need to know the symptoms to provide appropriate help."
            },
            3: {
                "action": "location_confirmation",
                "message": "What's your exact location? I need your address for emergency services.",
                "confirmation_required": True,
                "timeout": 15,
                "escalation": "Location is critical for emergency response."
            },
            4: {
                "action": "call_emergency",
                "message": "I'm calling 911 now. Stay with the person and follow my instructions.",
                "confirmation_required": False,
                "timeout": 5,
                "escalation": "Emergency services are being contacted."
            }
        }
        return steps.get(self.current_step, {"action": "complete", "message": "Emergency protocol complete."})
    
    def _get_danger_protocol_step(self) -> dict:
        """Get danger/threat protocol steps."""
        steps = {
            1: {
                "action": "immediate_safety",
                "message": "I understand you feel in danger. Are you in a safe location right now?",
                "confirmation_required": True,
                "timeout": 10,
                "escalation": "If you don't respond, I'll assume you need immediate help."
            },
            2: {
                "action": "threat_assessment",
                "message": "Can you tell me what's happening? Are you alone, or is someone with you?",
                "confirmation_required": True,
                "timeout": 15,
                "escalation": "I need to understand the situation to help you."
            },
            3: {
                "action": "location_confirmation",
                "message": "What's your exact location? I need your address to send help if needed.",
                "confirmation_required": True,
                "timeout": 15,
                "escalation": "Location is important for your safety."
            },
            4: {
                "action": "call_emergency",
                "message": "I'm calling 911 now. Stay on the line and I'll guide you through this.",
                "confirmation_required": False,
                "timeout": 5,
                "escalation": "Emergency services are being contacted."
            }
        }
        return steps.get(self.current_step, {"action": "complete", "message": "Emergency protocol complete."})
    
    def _get_general_emergency_step(self) -> dict:
        """Get general emergency protocol steps."""
        steps = {
            1: {
                "action": "safety_check",
                "message": "I understand there's an emergency. Are you safe right now?",
                "confirmation_required": True,
                "timeout": 10,
                "escalation": "If you don't respond, I'll call 911 immediately."
            },
            2: {
                "action": "situation_assessment",
                "message": "Can you tell me what's happening? I need to understand the situation.",
                "confirmation_required": True,
                "timeout": 15,
                "escalation": "I need more information to help you properly."
            },
            3: {
                "action": "location_confirmation",
                "message": "What's your exact location? I need your address for emergency services.",
                "confirmation_required": True,
                "timeout": 15,
                "escalation": "Location is critical for emergency response."
            },
            4: {
                "action": "call_emergency",
                "message": "I'm calling 911 now. Stay on the line and follow my instructions.",
                "confirmation_required": False,
                "timeout": 5,
                "escalation": "Emergency services are being contacted."
            }
        }
        return steps.get(self.current_step, {"action": "complete", "message": "Emergency protocol complete."})
    
    def confirm_step(self):
        """Mark current step as confirmed and move to next."""
        self.steps_completed.append(self.current_step)
        self.current_step += 1
        self.pending_confirmation = False
        self.confirmation_timeout = 0
        
    def escalate(self):
        """Increase escalation level and potentially skip steps."""
        self.escalation_level += 1
        if self.escalation_level >= 2:
            # Skip to emergency call
            self.current_step = 4
        self.pending_confirmation = False

# Audio processing is now handled by individual services
# AgenticAudioProcessor has been replaced with:
# - WhisperService for transcription
# - ElevenLabsService for text-to-speech

class AgenticVoiceAgent:
    """Agentic voice agent that takes complete control of conversations."""
    
    def __init__(self):
        self.chat_agent = AgenticChatAgent()
        self.openai_service = OpenAIService()
        self.elevenlabs_service = ElevenLabsService()
        self.whisper_service = WhisperService()
        self.voice_state = AgenticVoiceState()
        self.conversation_state = AgenticConversationState()
        self.active_connections: Dict[str, WebSocketServerProtocol] = {}
        self.proactive_tasks: Dict[str, asyncio.Task] = {}
        self.escalation_tasks: Dict[str, asyncio.Task] = {}
        logger.info("Agentic voice agent initialized with services")
    
    def _detect_emergency(self, text: str) -> tuple[bool, str]:
        """Detect if user input contains emergency keywords and categorize the emergency type."""
        text_lower = text.lower()
        
        # Fire-related keywords
        fire_keywords = ["fire", "burning", "smoke", "flame", "blaze"]
        if any(keyword in text_lower for keyword in fire_keywords):
            return True, "fire"
        
        # Medical emergency keywords
        medical_keywords = ["heart", "chest pain", "cardiac", "breathing", "choking", "asthma", 
                          "injury", "hurt", "bleeding", "broken", "fracture", "unconscious", 
                          "not breathing", "medical emergency"]
        if any(keyword in text_lower for keyword in medical_keywords):
            return True, "medical"
        
        # Danger/threat keywords
        danger_keywords = ["danger", "threat", "someone behind", "following", "attack", "intruder", 
                         "unsafe", "scared", "fear", "help", "emergency", "crisis"]
        if any(keyword in text_lower for keyword in danger_keywords):
            return True, "danger"
        
        # General emergency keywords
        general_keywords = ["accident", "crash", "collision", "car", "vehicle", "emergency", "help"]
        if any(keyword in text_lower for keyword in general_keywords):
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
            if self.conversation_state.current_step > 0:
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
        """Handle emergency response with step-by-step protocol."""
        
        # Start emergency protocol if not already started
        if self.conversation_state.current_step == 0:
            self.conversation_state.start_emergency_protocol(emergency_type)
            logger.info(f"Starting {emergency_type} emergency protocol")
        
        # Get current step
        current_step = self.conversation_state.get_next_step()
        
        if current_step["action"] == "complete":
            # Protocol complete, provide final guidance
            response = "Emergency protocol complete. Help is on the way. Stay on the line and follow emergency responder instructions."
            await self._send_response(websocket, response)
            return
        
        # Check if user provided confirmation for previous step
        if self.conversation_state.pending_confirmation:
            if self._is_positive_confirmation(user_input):
                self.conversation_state.confirm_step()
                logger.info(f"Step {self.conversation_state.current_step - 1} confirmed, moving to step {self.conversation_state.current_step}")
            else:
                # User didn't confirm, ask again with more urgency
                response = f"I need you to confirm this. {current_step['message']}"
                await self._send_response(websocket, response)
                return
        
        # Send current step message
        response = current_step["message"]
        await self._send_response(websocket, response)
        
        # Set up confirmation timeout if required
        if current_step["confirmation_required"]:
            self.conversation_state.pending_confirmation = True
            self.conversation_state.confirmation_timeout = current_step["timeout"]
            
            # Start escalation timer
            client_id = self._get_client_id(websocket)
            if client_id in self.escalation_tasks:
                self.escalation_tasks[client_id].cancel()
            
            self.escalation_tasks[client_id] = asyncio.create_task(
                self._escalation_timer(websocket, client_id, current_step["escalation"])
            )
    
    def _is_positive_confirmation(self, user_input: str) -> bool:
        """Check if user input is a positive confirmation."""
        text_lower = user_input.lower()
        positive_words = ["yes", "yeah", "yep", "sure", "okay", "ok", "correct", "right", "true", "confirmed"]
        return any(word in text_lower for word in positive_words)
    
    async def _escalation_timer(self, websocket: WebSocketServerProtocol, client_id: str, escalation_message: str):
        """Timer for escalation when user doesn't respond."""
        try:
            await asyncio.sleep(self.conversation_state.confirmation_timeout)
            
            # If still pending confirmation, escalate
            if self.conversation_state.pending_confirmation:
                logger.warning(f"Escalating for client {client_id} - no confirmation received")
                self.conversation_state.escalate()
                
                response = escalation_message
                await self._send_response(websocket, response)
                
                # If escalated to emergency call, simulate the call
                if self.conversation_state.current_step >= 4:
                    await self._simulate_emergency_call(websocket)
                    
        except asyncio.CancelledError:
            # Timer was cancelled (user responded)
            pass
    
    async def _simulate_emergency_call(self, websocket: WebSocketServerProtocol):
        """Simulate calling emergency services."""
        response = "Calling 911 now. Emergency services are being contacted. Stay on the line."
        await self._send_response(websocket, response)
        
        # Simulate call delay
        await asyncio.sleep(2)
        
        response = "911 has been contacted. Emergency responders are on their way. Please stay on the line and follow their instructions when they arrive."
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