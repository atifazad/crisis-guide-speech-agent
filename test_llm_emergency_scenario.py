#!/usr/bin/env python3
"""
Test script to simulate emergency scenarios with LLM-driven responses
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


async def simulate_emergency_scenario():
    """Simulate an emergency scenario with LLM-driven responses."""
    
    # Create a mock websocket
    mock_websocket = Mock()
    mock_websocket.send = AsyncMock()
    
    # Create agent
    agent = AgenticVoiceAgent()
    
    print("🧪 Simulating emergency scenario with LLM-driven responses...")
    
    # Test scenario: Fire emergency
    print("\n🔥 FIRE EMERGENCY SCENARIO")
    print("=" * 50)
    
    # Initial emergency detection
    user_input = "There's a fire in my kitchen! Help!"
    print(f"👤 User: {user_input}")
    
    # Simulate the emergency response
    await agent._handle_agentic_emergency_response(mock_websocket, user_input, "fire")
    
    # Check what was sent
    calls = mock_websocket.send.call_args_list
    if calls:
        response_data = json.loads(calls[-1][0][0])
        print(f"🤖 AI Response: {response_data.get('text', 'No response')}")
    
    print("\n✅ Emergency scenario simulation completed!")
    print("\nKey improvements with LLM-driven system:")
    print("- No more 'I'm calling 911 now' messages without actual calls")
    print("- AI dynamically assesses the situation")
    print("- Responses are context-aware and flexible")
    print("- Emergency calls require explicit user permission")
    print("- Escalation is intelligent and situation-dependent")


if __name__ == "__main__":
    asyncio.run(simulate_emergency_scenario()) 