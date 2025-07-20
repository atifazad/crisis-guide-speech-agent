#!/usr/bin/env python3
"""
Emergency Call Service - Integrates Twilio and ACI.dev for emergency calling
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmergencyCallData:
    """Data structure for emergency call information."""
    
    def __init__(self, emergency_type: str, location: str, situation: str, user_phone: str = None):
        self.emergency_type = emergency_type
        self.location = location
        self.situation = situation
        self.user_phone = user_phone
        self.timestamp = datetime.now()
        self.call_id = None
        self.status = "pending"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for logging."""
        return {
            "emergency_type": self.emergency_type,
            "location": self.location,
            "situation": self.situation,
            "user_phone": self.user_phone,
            "timestamp": self.timestamp.isoformat(),
            "call_id": self.call_id,
            "status": self.status
        }

class EmergencyCallService:
    """Service for handling emergency calls with Twilio and ACI.dev integration."""
    
    def __init__(self):
        self.twilio_client = None
        self.aci_client = None
        self.active_calls = {}
        self.emergency_logs = []
        
        # Initialize Twilio if enabled
        if Config.get_emergency_call_enabled():
            self._init_twilio()
        
        # Initialize ACI.dev if enabled
        if Config.get_aci_enabled():
            self._init_aci()
    
    def _init_twilio(self):
        """Initialize Twilio client."""
        try:
            from twilio.rest import Client
            account_sid = Config.get_twilio_account_sid()
            auth_token = Config.get_twilio_auth_token()
            
            if account_sid and auth_token:
                self.twilio_client = Client(account_sid, auth_token)
                logger.info("✅ Twilio client initialized successfully")
            else:
                logger.warning("⚠️ Twilio credentials not provided")
        except ImportError:
            logger.error("❌ Twilio package not installed. Run: pip install twilio")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Twilio: {str(e)}")
    
    def _init_aci(self):
        """Initialize ACI.dev client."""
        try:
            # ACI.dev integration would go here
            # For now, we'll simulate the ACI.dev functionality
            logger.info("✅ ACI.dev client initialized (simulated)")
        except Exception as e:
            logger.error(f"❌ Failed to initialize ACI.dev: {str(e)}")
    
    async def initiate_emergency_call(self, emergency_data: EmergencyCallData) -> Optional[str]:
        """Initiate emergency call using Twilio."""
        if not Config.get_emergency_call_enabled():
            logger.warning("⚠️ Emergency calls are disabled")
            return None
        
        if not self.twilio_client:
            logger.error("❌ Twilio client not initialized")
            return None
        
        try:
            # Use target phone number instead of 911
            target_phone = Config.get_emergency_target_phone()
            
            # Create call message
            call_message = self._create_emergency_call_message(emergency_data)
            
            # Create emergency message TwiML
            emergency_twiml = f'''<Response>
                <Say>This is an emergency call from your AI assistant. Emergency type: {emergency_data.emergency_type}. Location: {emergency_data.location}. Situation: {emergency_data.situation}. Please stay on the line for guidance.</Say>
                <Pause length="2"/>
                <Say>Emergency services have been notified. Please provide additional details if needed.</Say>
            </Response>'''
            
            # Initiate call via Twilio with direct TwiML
            call = self.twilio_client.calls.create(
                twiml=emergency_twiml,
                to=target_phone,
                from_=Config.get_twilio_phone_number()
            )
            
            emergency_data.call_id = call.sid
            emergency_data.status = "initiated"
            
            # Store active call
            self.active_calls[call.sid] = emergency_data
            
            # Log emergency call
            self._log_emergency_call(emergency_data)
            
            logger.info(f"🚨 Emergency call initiated: {call.sid}")
            return call.sid
            
        except Exception as e:
            logger.error(f"❌ Failed to initiate emergency call: {str(e)}")
            return None
    
    def _create_emergency_call_message(self, emergency_data: EmergencyCallData) -> str:
        """Create emergency call message."""
        message = f"EMERGENCY CALL - {emergency_data.emergency_type.upper()}\n\n"
        message += f"Location: {emergency_data.location}\n"
        message += f"Situation: {emergency_data.situation}\n"
        message += f"Time: {emergency_data.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        message += "This is an automated emergency call from the Crisis Guide Speech Agent."
        return message
    
    async def get_call_status(self, call_id: str) -> Optional[Dict[str, Any]]:
        """Get the status and details of an emergency call."""
        if not self.twilio_client:
            return None
        
        try:
            call = self.twilio_client.calls(call_id).fetch()
            return {
                "status": call.status,
                "duration": getattr(call, 'duration', None),
                "direction": getattr(call, 'direction', None),
                "price": getattr(call, 'price', None),
                "price_unit": getattr(call, 'price_unit', None)
            }
        except Exception as e:
            logger.error(f"❌ Failed to get call status: {str(e)}")
            return None
    
    async def wait_for_call_completion(self, call_id: str, timeout: int = 60) -> Optional[Dict[str, Any]]:
        """Wait for call to complete or fail with timeout."""
        if not self.twilio_client:
            return None
        
        try:
            check_interval = 2  # Check every 2 seconds
            elapsed_time = 0
            
            while elapsed_time < timeout:
                await asyncio.sleep(check_interval)
                elapsed_time += check_interval
                
                call_details = await self.get_call_status(call_id)
                if not call_details:
                    continue
                
                current_status = call_details["status"]
                logger.info(f"⏱️  {elapsed_time}s - Call {call_id} status: {current_status}")
                
                # Check if call is complete or failed
                if current_status in ["completed", "busy", "failed", "no-answer", "canceled"]:
                    logger.info(f"📊 Call {call_id} ended with status: {current_status}")
                    return call_details
            
            logger.warning(f"⏰ Timeout reached for call {call_id}")
            return await self.get_call_status(call_id)
            
        except Exception as e:
            logger.error(f"❌ Error monitoring call {call_id}: {str(e)}")
            return None
    
    async def end_call(self, call_id: str) -> bool:
        """End an emergency call."""
        if not self.twilio_client:
            return False
        
        try:
            call = self.twilio_client.calls(call_id).update(status='completed')
            logger.info(f"✅ Emergency call ended: {call_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to end call: {str(e)}")
            return False
    
    def _log_emergency_call(self, emergency_data: EmergencyCallData):
        """Log emergency call for compliance."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "call_id": emergency_data.call_id,
            "emergency_type": emergency_data.emergency_type,
            "location": emergency_data.location,
            "situation": emergency_data.situation,
            "status": emergency_data.status
        }
        
        self.emergency_logs.append(log_entry)
        
        # Console logging
        logger.info(f"📝 EMERGENCY CALL LOGGED:")
        logger.info(f"   📞 Call ID: {emergency_data.call_id}")
        logger.info(f"   🚨 Type: {emergency_data.emergency_type}")
        logger.info(f"   📍 Location: {emergency_data.location}")
        logger.info(f"   📋 Situation: {emergency_data.situation}")
        logger.info(f"   📊 Status: {emergency_data.status}")
        
        # Save to file
        try:
            with open("emergency_calls.log", "a") as f:
                json.dump(log_entry, f)
                f.write("\n")
            logger.info(f"💾 Emergency call saved to emergency_calls.log")
        except Exception as e:
            logger.error(f"❌ Failed to log emergency call: {str(e)}")
    
    async def simulate_emergency_call(self, emergency_data: EmergencyCallData) -> str:
        """Simulate emergency call for testing purposes."""
        call_id = f"sim_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        emergency_data.call_id = call_id
        emergency_data.status = "simulated"
        
        # Store active call
        self.active_calls[call_id] = emergency_data
        
        # Log emergency call
        self._log_emergency_call(emergency_data)
        
        logger.info(f"🚨 Simulated emergency call: {call_id}")
        return call_id
    
    async def get_emergency_call_summary(self, call_id: str) -> Optional[Dict[str, Any]]:
        """Get summary of emergency call."""
        if call_id in self.active_calls:
            emergency_data = self.active_calls[call_id]
            return emergency_data.to_dict()
        return None
    
    async def list_active_calls(self) -> Dict[str, EmergencyCallData]:
        """Get list of active emergency calls."""
        return self.active_calls.copy()
    
    async def cleanup_old_calls(self):
        """Clean up old emergency calls."""
        current_time = datetime.now()
        calls_to_remove = []
        
        for call_id, emergency_data in self.active_calls.items():
            # Remove calls older than 1 hour
            if (current_time - emergency_data.timestamp).total_seconds() > 3600:
                calls_to_remove.append(call_id)
        
        for call_id in calls_to_remove:
            del self.active_calls[call_id]
            logger.info(f"🧹 Cleaned up old emergency call: {call_id}")

class ACIDevService:
    """ACI.dev integration service for enhanced emergency features."""
    
    def __init__(self):
        self.api_key = Config.get_aci_api_key()
        self.linked_account_owner_id = Config.get_aci_linked_account_owner_id()
        self.enabled = Config.get_aci_enabled()
    
    async def log_emergency_to_notion(self, emergency_data: EmergencyCallData):
        """Log emergency to Notion via ACI.dev."""
        if not self.enabled:
            logger.warning("⚠️ ACI.dev not enabled")
            return False
        
        try:
            # This would use ACI.dev's Notion integration
            # For now, we'll simulate the functionality
            logger.info(f"📝 Logging emergency to Notion via ACI.dev: {emergency_data.emergency_type}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to log to Notion: {str(e)}")
            return False
    
    async def send_emergency_sms(self, emergency_data: EmergencyCallData):
        """Send emergency SMS via ACI.dev."""
        if not self.enabled:
            logger.warning("⚠️ ACI.dev not enabled")
            return False
        
        try:
            # This would use ACI.dev's SMS integration
            # For now, we'll simulate the functionality
            logger.info(f"📱 Sending emergency SMS via ACI.dev: {emergency_data.emergency_type}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to send SMS: {str(e)}")
            return False
    
    async def create_emergency_document(self, emergency_data: EmergencyCallData):
        """Create emergency document via ACI.dev."""
        if not self.enabled:
            logger.warning("⚠️ ACI.dev not enabled")
            return False
        
        try:
            # This would use ACI.dev's Google Docs integration
            # For now, we'll simulate the functionality
            logger.info(f"📄 Creating emergency document via ACI.dev: {emergency_data.emergency_type}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to create document: {str(e)}")
            return False 