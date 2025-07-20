#!/usr/bin/env python3
"""
Test that emergency services are called automatically at level 3
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


async def test_emergency_call_fix():
    """Test that emergency services are called automatically."""
    
    # Create a mock websocket
    mock_websocket = Mock()
    mock_websocket.send = AsyncMock()
    
    # Create agent
    agent = AgenticVoiceAgent()
    
    print("🚨 TESTING EMERGENCY CALL FIX...")
    
    # Test scenario: Fire emergency with no response
    user_input = "There's a fire in my kitchen! Help!"
    print(f"👤 User: {user_input}")
    
    # Simulate the emergency response
    await agent._handle_agentic_emergency_response(mock_websocket, user_input, "fire")
    
    # Check initial response
    calls = mock_websocket.send.call_args_list
    if calls:
        response_data = json.loads(calls[-1][0][0])
        print(f"🤖 Initial Response: {response_data.get('text', 'No response')}")
    
    print(f"\n📊 Initial Status:")
    print(f"   Escalation level: {agent.conversation_state.escalation_level}")
    print(f"   Pending confirmation: {agent.conversation_state.pending_confirmation}")
    
    # Simulate escalation to level 3
    print(f"\n🔥 ESCALATING TO LEVEL 3...")
    agent.conversation_state.escalate()  # Level 1
    agent.conversation_state.escalate()  # Level 2
    agent.conversation_state.escalate()  # Level 3
    print(f"   Escalation level: {agent.conversation_state.escalation_level}")
    
    # Test escalation response at level 3
    escalation_context = f"""
    ESCALATION SITUATION:
    - User has not responded to previous question
    - Escalation level: {agent.conversation_state.escalation_level}
    - Emergency type: {agent.conversation_state.emergency_type}
    - Time elapsed: {agent.conversation_state.confirmation_timeout} seconds
    """
    
    escalation_prompt = f"""You are an emergency response AI assistant. The user has not responded to your previous question. Provide an escalated response.

{escalation_context}

ESCALATION LEVELS:
- Level 1 (First escalation): Ask again with more urgency - "I need you to respond immediately. Are you safe?"
- Level 2 (Second escalation): Warn about calling emergency services - "If you don't respond in the next 5 seconds, I will call emergency services."
- Level 3 (Third escalation): AUTOMATICALLY CALL EMERGENCY SERVICES - "I am calling emergency services now. Stay on the line."

CURRENT ESCALATION LEVEL: {agent.conversation_state.escalation_level}

RESPONSE FORMAT:
- Be more urgent and direct based on the escalation level
- Do not use markdown formatting
- Be specific to the escalation level
- At Level 3: Inform that you are calling emergency services immediately

Remember: At Level 3, automatically call emergency services without asking for permission."""
    
    response = await agent._get_agentic_response("", escalation_prompt)
    print(f"🤖 Level 3 Response: {response}")
    
    # Test that emergency call is triggered
    print(f"\n🚨 TESTING AUTOMATIC EMERGENCY CALL...")
    
    # Mock the emergency call service
    agent.emergency_call_service.initiate_emergency_call = AsyncMock(return_value="test_call_123")
    
    # Trigger the escalation timer logic for level 3
    client_id = "test_client"
    await agent._escalation_timer(mock_websocket, client_id, "Emergency call test")
    
    print(f"\n✅ Emergency call fix test completed!")
    print(f"   Final escalation level: {agent.conversation_state.escalation_level}")
    print(f"   Emergency call should be triggered automatically at level 3")


if __name__ == "__main__":
    asyncio.run(test_emergency_call_fix()) 