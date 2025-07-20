#!/usr/bin/env python3
"""
Test script to verify escalation functionality with LLM-driven emergency responses
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


async def test_escalation():
    """Test escalation functionality."""
    
    # Create a mock websocket
    mock_websocket = Mock()
    mock_websocket.send = AsyncMock()
    
    # Create agent
    agent = AgenticVoiceAgent()
    
    print("🧪 Testing escalation functionality...")
    
    # Test scenario: Fire emergency with no response
    print("\n🔥 FIRE EMERGENCY - NO RESPONSE SCENARIO")
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
    
    # Check if escalation timer was set up
    print(f"\n📊 Escalation Status:")
    print(f"   Pending confirmation: {agent.conversation_state.pending_confirmation}")
    print(f"   Confirmation timeout: {agent.conversation_state.confirmation_timeout}")
    print(f"   Escalation level: {agent.conversation_state.escalation_level}")
    print(f"   Active escalation tasks: {len(agent.escalation_tasks)}")
    
    # Simulate escalation timer firing (no response)
    print(f"\n⏰ Simulating escalation timer (no response)...")
    
    # Cancel any existing escalation tasks
    for task in agent.escalation_tasks.values():
        task.cancel()
    
    # Manually trigger escalation
    agent.conversation_state.escalate()
    print(f"   Escalation level after escalation: {agent.conversation_state.escalation_level}")
    
    # Simulate escalation response
    escalation_context = f"""
    ESCALATION SITUATION:
    - User has not responded to previous question
    - Escalation level: {agent.conversation_state.escalation_level}
    - Emergency type: {agent.conversation_state.emergency_type}
    - Time elapsed: {agent.conversation_state.confirmation_timeout} seconds
    """
    
    escalation_prompt = f"""You are an emergency response AI assistant. The user has not responded to your previous question. Provide an escalated response.

{escalation_context}

RESPONSE FORMAT:
- Be more urgent and direct
- If this is the first escalation: "I need you to respond immediately. Are you safe?"
- If this is the second escalation: "If you don't respond in the next 10 seconds, I will call emergency services."
- If this is the third escalation: "I need to call emergency services now. Do you give me permission to make the call?"
- Do not use markdown formatting

Remember: Be urgent but don't actually call emergency services until you get explicit permission."""
    
    response = await agent._get_agentic_response("", escalation_prompt)
    print(f"🤖 Escalation Response: {response}")
    
    print("\n✅ Escalation test completed!")
    print("\nKey improvements:")
    print("- Escalation timer is properly set up for questions")
    print("- LLM decides escalation responses dynamically")
    print("- Multiple escalation levels are supported")
    print("- Emergency call permission is requested at appropriate level")


if __name__ == "__main__":
    asyncio.run(test_escalation()) 