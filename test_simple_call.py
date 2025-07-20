#!/usr/bin/env python3
"""
Simple Twilio call test without webhooks
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config import Config
from twilio.rest import Client

async def test_simple_call():
    """Test a simple Twilio call without webhooks."""
    print("📞 Testing Simple Twilio Call")
    print("=" * 40)
    
    # Initialize Twilio client
    client = Client(Config.get_twilio_account_sid(), Config.get_twilio_auth_token())
    
    try:
        # Make a simple call with TwiML
        call = client.calls.create(
            twiml='<Response><Say>This is a test call from your emergency system. If you receive this call, the Twilio integration is working correctly.</Say></Response>',
            to=Config.get_emergency_target_phone(),
            from_=Config.get_twilio_phone_number()
        )
        
        print(f"✅ Call initiated: {call.sid}")
        print(f"📱 To: {Config.get_emergency_target_phone()}")
        print(f"📞 From: {Config.get_twilio_phone_number()}")
        print(f"📊 Initial Status: {call.status}")
        print()
        print("⏳ Monitoring call status...")
        
        # Monitor call status until it's complete or failed
        max_wait_time = 60  # Maximum 60 seconds
        check_interval = 2   # Check every 2 seconds
        elapsed_time = 0
        
        while elapsed_time < max_wait_time:
            await asyncio.sleep(check_interval)
            elapsed_time += check_interval
            
            # Get current call status
            call_status = client.calls(call.sid).fetch()
            current_status = call_status.status
            
            print(f"⏱️  {elapsed_time}s - Status: {current_status}")
            
            # Check if call is complete or failed
            if current_status in ["completed", "busy", "failed", "no-answer", "canceled"]:
                print()
                if current_status == "completed":
                    print("✅ Call completed successfully!")
                    print(f"📊 Duration: {call_status.duration} seconds")
                elif current_status == "busy":
                    print("❌ Call failed - phone busy or unreachable")
                elif current_status == "failed":
                    print("❌ Call failed - check Twilio account status")
                elif current_status == "no-answer":
                    print("❌ Call failed - no answer")
                elif current_status == "canceled":
                    print("❌ Call was canceled")
                else:
                    print(f"❌ Call ended with status: {current_status}")
                break
            elif current_status == "ringing":
                print("📞 Phone is ringing...")
            elif current_status == "in-progress":
                print("📞 Call is in progress...")
            elif current_status == "queued":
                print("⏳ Call is queued...")
            else:
                print(f"📊 Call status: {current_status}")
        else:
            print()
            print("⏰ Timeout reached - call monitoring stopped")
            print(f"📊 Final status: {call_status.status}")
            
    except Exception as e:
        print(f"❌ Error making call: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_simple_call()) 