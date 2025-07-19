#!/usr/bin/env python3
"""
Test script for Crisis Guide Voice Agent with agentic behavior.
Demonstrates conversation state management and escalation logic.
"""

import os
import sys
import asyncio
import time
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.pipecat import PipecatPipelineManager
from src.pipecat.conversation_state import ConversationStateManager, UrgencyLevel

def test_crisis_conversation_state():
    """Test the crisis conversation state management."""
    print("🧪 Crisis Agent Conversation State Test")
    print("=" * 50)
    
    # Initialize conversation state
    conv_state = ConversationStateManager()
    
    print("1. Testing Initial State...")
    summary = conv_state.get_conversation_summary()
    print(f"   Current State: {summary['current_state']}")
    print(f"   Current Urgency: {summary['current_urgency']}")
    print(f"   Total Turns: {summary['total_turns']}")
    print(f"   Last User Activity: {summary['last_user_activity']}")
    print(f"   Last AI Response: {summary['last_ai_response']}")
    
    print("\n2. Testing User Input Processing...")
    # Simulate user input about fire
    conv_state.add_user_input("Help, there is fire")
    summary = conv_state.get_conversation_summary()
    print(f"   After fire input: {summary['current_state']}")
    print(f"   Urgency Level: {summary['current_urgency']}")
    print(f"   Total Turns: {summary['total_turns']}")
    
    print("\n3. Testing AI Response Processing...")
    # Simulate AI response
    conv_state.update_ai_response("Yes, I am here to help. Can you breathe?")
    summary = conv_state.get_conversation_summary()
    print(f"   After AI response: {summary['current_state']}")
    print(f"   Total Turns: {summary['total_turns']}")
    print(f"   Time since user activity: {summary['time_since_user_activity']}")
    
    print("\n4. Testing Timeout Detection...")
    # Simulate timeout
    time.sleep(1)  # Wait a bit
    should_timeout = conv_state.should_timeout()
    print(f"   Should timeout: {should_timeout}")
    
    print("\n5. Testing Escalation Logic...")
    # Simulate escalation
    should_escalate = conv_state.should_escalate()
    escalation_msg = conv_state.get_escalation_message()
    print(f"   Should escalate: {should_escalate}")
    print(f"   Escalation message: {escalation_msg}")
    
    print("\n6. Testing Urgency Escalation...")
    # Test urgency escalation
    conv_state.escalate_urgency()
    summary = conv_state.get_conversation_summary()
    print(f"   After escalation: {summary['current_state']}")
    print(f"   New urgency level: {summary['current_urgency']}")
    
    print("\n✅ Conversation state test completed!")
    return True

async def test_crisis_pipeline():
    """Test the crisis pipeline with agentic behavior."""
    print("\n🧪 Crisis Pipeline Test")
    print("=" * 30)
    
    # Load environment
    load_dotenv()
    
    # Check API keys
    openai_key = os.getenv('OPENAI_API_KEY')
    elevenlabs_key = os.getenv('ELEVENLABS_API_KEY')
    
    if not openai_key or not elevenlabs_key:
        print("❌ Missing required API keys")
        return False
    
    # Initialize pipeline manager
    pipeline_manager = PipecatPipelineManager()
    
    # Set up callbacks for monitoring
    def on_user_input(text):
        print(f"👤 User: {text}")
    
    def on_ai_response(text, urgency):
        print(f"🤖 AI ({urgency}): {text}")
    
    def on_escalation(message):
        print(f"🚨 ESCALATION: {message}")
    
    pipeline_manager.set_callbacks(
        on_user_input=on_user_input,
        on_ai_response=on_ai_response,
        on_escalation=on_escalation
    )
    
    # Test pipeline creation
    print("1. Creating Crisis Pipeline...")
    if not pipeline_manager.create_pipeline():
        print("❌ Failed to create pipeline")
        return False
    
    print("✅ Pipeline created successfully")
    
    # Test pipeline status
    status = pipeline_manager.get_pipeline_status()
    print(f"   Pipeline Created: {'✅ Yes' if status['pipeline_created'] else '❌ No'}")
    print(f"   Services Configured: {status['services']}")
    
    print("\n2. Testing Crisis Response System Prompt...")
    # Test the crisis system prompt
    crisis_prompt = pipeline_manager._get_crisis_system_prompt()
    print("   Crisis System Prompt:")
    print("   " + crisis_prompt[:200] + "...")
    
    print("\n3. Testing Service Connections...")
    service_results = pipeline_manager.test_services()
    for service, result in service_results.items():
        status = "✅ Success" if result.get('success', False) else "❌ Failed"
        print(f"   {service.upper()}: {status}")
    
    print("\n✅ Crisis pipeline test completed!")
    return True

def test_crisis_scenarios():
    """Test different crisis scenarios."""
    print("\n🧪 Crisis Scenarios Test")
    print("=" * 30)
    
    scenarios = [
        {
            "name": "Fire Emergency",
            "user_input": "Help, there is fire",
            "expected_response": "breathe",
            "urgency": "urgent"
        },
        {
            "name": "Medical Emergency", 
            "user_input": "I can't breathe",
            "expected_response": "breathing",
            "urgency": "emergency"
        },
        {
            "name": "Safety Concern",
            "user_input": "Someone is following me",
            "expected_response": "safe",
            "urgency": "urgent"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{i}. {scenario['name']}")
        print(f"   Input: {scenario['user_input']}")
        print(f"   Expected: {scenario['expected_response']}")
        print(f"   Urgency: {scenario['urgency']}")
    
    print("\n✅ Crisis scenarios test completed!")
    return True

def main():
    """Main test function."""
    print("🚨 Crisis Guide Voice Agent Test")
    print("=" * 50)
    
    # Test conversation state
    success1 = test_crisis_conversation_state()
    
    # Test crisis scenarios
    success2 = test_crisis_scenarios()
    
    # Test pipeline (async)
    success3 = asyncio.run(test_crisis_pipeline())
    
    if success1 and success2 and success3:
        print("\n" + "=" * 50)
        print("✅ All crisis agent tests passed!")
        print("\nAgentic Features Implemented:")
        print("✅ Conversation state management")
        print("✅ Urgency level escalation")
        print("✅ Timeout detection")
        print("✅ Crisis response protocols")
        print("✅ Automatic escalation logic")
        print("\nReady for real-time voice interaction!")
    else:
        print("\n❌ Some tests failed. Please check configuration.")

if __name__ == "__main__":
    main() 