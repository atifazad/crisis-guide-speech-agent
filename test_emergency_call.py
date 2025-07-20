#!/usr/bin/env python3
"""
Test script for emergency call functionality
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.services.emergency_call_service import EmergencyCallService, EmergencyCallData, ACIDevService
from config import Config

async def test_emergency_call_service():
    """Test the emergency call service."""
    print("🧪 Testing Emergency Call Service")
    print("=" * 50)
    
    # Test configuration
    print(f"📋 Configuration:")
    print(f"   Emergency calls enabled: {Config.get_emergency_call_enabled()}")
    print(f"   ACI.dev enabled: {Config.get_aci_enabled()}")
    print(f"   Target phone: {Config.get_emergency_target_phone()}")
    print()
    
    # Initialize services
    emergency_service = EmergencyCallService()
    aci_service = ACIDevService()
    
    # Test emergency call data creation
    print("📝 Testing Emergency Call Data Creation")
    emergency_data = EmergencyCallData(
        emergency_type="fire",
        location="123 Test Street, Test City",
        situation="Fire detected in kitchen",
        user_phone="+1234567890"
    )
    
    print(f"   Emergency Type: {emergency_data.emergency_type}")
    print(f"   Location: {emergency_data.location}")
    print(f"   Situation: {emergency_data.situation}")
    print(f"   Timestamp: {emergency_data.timestamp}")
    print()
    
    # Test emergency call initiation
    print("📞 Testing Emergency Call Initiation")
    if Config.get_emergency_call_enabled():
        call_id = await emergency_service.initiate_emergency_call(emergency_data)
        if call_id:
            print(f"   ✅ Emergency call initiated: {call_id}")
            
            # Test call status monitoring with completion wait
            print("📊 Testing Call Status Monitoring (waiting for completion)")
            call_result = await emergency_service.wait_for_call_completion(call_id, timeout=60)
            if call_result:
                print(f"   📊 Final status: {call_result['status']}")
                if call_result.get('duration'):
                    print(f"   ⏱️  Duration: {call_result['duration']} seconds")
                if call_result.get('price'):
                    print(f"   💰 Cost: {call_result['price']} {call_result.get('price_unit', 'USD')}")
            else:
                print("   ❌ Call monitoring failed")
        else:
            print("   ❌ Failed to initiate emergency call")
    else:
        print("   ⚠️ Emergency calls are disabled")
        # Test simulation
        call_id = await emergency_service.simulate_emergency_call(emergency_data)
        print(f"   🎭 Simulated emergency call: {call_id}")
    
    print()
    
    # Test ACI.dev integration
    print("🔗 Testing ACI.dev Integration")
    if Config.get_aci_enabled():
        # Test Notion logging
        notion_result = await aci_service.log_emergency_to_notion(emergency_data)
        print(f"   Notion logging: {'✅' if notion_result else '❌'}")
        
        # Test SMS sending
        sms_result = await aci_service.send_emergency_sms(emergency_data)
        print(f"   SMS sending: {'✅' if sms_result else '❌'}")
        
        # Test document creation
        doc_result = await aci_service.create_emergency_document(emergency_data)
        print(f"   Document creation: {'✅' if doc_result else '❌'}")
    else:
        print("   ⚠️ ACI.dev is disabled")
    
    print()
    
    # Test emergency call summary
    print("📋 Testing Emergency Call Summary")
    summary = await emergency_service.get_emergency_call_summary(call_id)
    if summary:
        print(f"   Call ID: {summary['call_id']}")
        print(f"   Status: {summary['status']}")
        print(f"   Emergency Type: {summary['emergency_type']}")
    else:
        print("   ❌ No call summary available")
    
    print()
    
    # Test active calls listing
    print("📋 Testing Active Calls Listing")
    active_calls = await emergency_service.list_active_calls()
    print(f"   Active calls: {len(active_calls)}")
    for call_id, call_data in active_calls.items():
        print(f"     - {call_id}: {call_data.emergency_type}")
    
    print()
    print("✅ Emergency call service test completed!")

async def test_configuration():
    """Test configuration validation."""
    print("🔧 Testing Configuration")
    print("=" * 30)
    
    if Config.validate_config():
        print("✅ Configuration validation passed")
    else:
        print("❌ Configuration validation failed")
    
    print()

async def main():
    """Run all tests."""
    print("🚨 Emergency Call System Test")
    print("=" * 50)
    print()
    
    await test_configuration()
    await test_emergency_call_service()

if __name__ == "__main__":
    asyncio.run(main()) 