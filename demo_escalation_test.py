#!/usr/bin/env python3
"""
Quick demo test for escalation functionality
"""

import asyncio
import json
from unittest.mock import Mock, AsyncMock
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.agents.agentic_voice_agent import AgenticVoiceAgent


async def demo_escalation():
    """Demo escalation functionality."""
    
    # Create a mock websocket
    mock_websocket = Mock()
    mock_websocket.send = AsyncMock()
    
    # Create agent
    agent = AgenticVoiceAgent()
    
    print("🚨 DEMO: Testing escalation with 5-second timeout...")
    
    # Test scenario: Fire emergency
    user_input = "There's a fire in my kitchen! Help!"
    print(f"👤 User: {user_input}")
    
    # Simulate the emergency response
    await agent._handle_agentic_emergency_response(mock_websocket, user_input, "fire")
    
    # Check what was sent
    calls = mock_websocket.send.call_args_list
    if calls:
        response_data = json.loads(calls[-1][0][0])
        print(f"🤖 AI Response: {response_data.get('text', 'No response')}")
    
    print(f"\n📊 Escalation Status:")
    print(f"   Pending confirmation: {agent.conversation_state.pending_confirmation}")
    print(f"   Confirmation timeout: {agent.conversation_state.confirmation_timeout} seconds")
    print(f"   Escalation level: {agent.conversation_state.escalation_level}")
    print(f"   Active escalation tasks: {len(agent.escalation_tasks)}")
    
    print(f"\n⏰ Waiting for escalation (5 seconds)...")
    
    # Wait for escalation to trigger
    await asyncio.sleep(6)  # Wait slightly longer than the 5-second timeout
    
    print(f"\n📊 After escalation:")
    print(f"   Escalation level: {agent.conversation_state.escalation_level}")
    print(f"   Pending confirmation: {agent.conversation_state.pending_confirmation}")
    
    print(f"\n✅ Demo completed! Escalation should have triggered after 5 seconds.")


if __name__ == "__main__":
    asyncio.run(demo_escalation()) 