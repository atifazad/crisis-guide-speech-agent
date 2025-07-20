#!/usr/bin/env python3
"""
Test escalation levels with different responses
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


async def test_escalation_levels():
    """Test different escalation levels."""
    
    # Create a mock websocket
    mock_websocket = Mock()
    mock_websocket.send = AsyncMock()
    
    # Create agent
    agent = AgenticVoiceAgent()
    
    print("🚨 TESTING ESCALATION LEVELS...")
    
    # Test scenario: Fire emergency
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
    
    # Test escalation level 1
    print(f"\n🔥 ESCALATION LEVEL 1")
    agent.conversation_state.escalate()
    print(f"   Escalation level: {agent.conversation_state.escalation_level}")
    
    escalation_context = f"""
    ESCALATION SITUATION:
    - User has not responded to previous question
    - Escalation level: {agent.conversation_state.escalation_level}
    - Emergency type: {agent.conversation_state.emergency_type}
    - Time elapsed: {agent.conversation_state.confirmation_timeout} seconds
    
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
- Level 3 (Third escalation): Ask for permission to call - "I need to call emergency services now. Do you give me permission to make the call?"

CURRENT ESCALATION LEVEL: {agent.conversation_state.escalation_level}

RESPONSE FORMAT:
- Be more urgent and direct based on the escalation level
- Do not use markdown formatting
- Be specific to the escalation level

Remember: Be urgent but don't actually call emergency services until you get explicit permission."""
    
    response = await agent._get_agentic_response("", escalation_prompt)
    print(f"🤖 Level 1 Response: {response}")
    
    # Test escalation level 2
    print(f"\n🔥 ESCALATION LEVEL 2")
    agent.conversation_state.escalate()
    print(f"   Escalation level: {agent.conversation_state.escalation_level}")
    
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
- Level 3 (Third escalation): Ask for permission to call - "I need to call emergency services now. Do you give me permission to make the call?"

CURRENT ESCALATION LEVEL: {agent.conversation_state.escalation_level}

RESPONSE FORMAT:
- Be more urgent and direct based on the escalation level
- Do not use markdown formatting
- Be specific to the escalation level

Remember: Be urgent but don't actually call emergency services until you get explicit permission."""
    
    response = await agent._get_agentic_response("", escalation_prompt)
    print(f"🤖 Level 2 Response: {response}")
    
    # Test escalation level 3
    print(f"\n🔥 ESCALATION LEVEL 3")
    agent.conversation_state.escalate()
    print(f"   Escalation level: {agent.conversation_state.escalation_level}")
    
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
- Level 3 (Third escalation): Ask for permission to call - "I need to call emergency services now. Do you give me permission to make the call?"

CURRENT ESCALATION LEVEL: {agent.conversation_state.escalation_level}

RESPONSE FORMAT:
- Be more urgent and direct based on the escalation level
- Do not use markdown formatting
- Be specific to the escalation level

Remember: Be urgent but don't actually call emergency services until you get explicit permission."""
    
    response = await agent._get_agentic_response("", escalation_prompt)
    print(f"🤖 Level 3 Response: {response}")
    
    print(f"\n✅ Escalation levels test completed!")
    print(f"   Final escalation level: {agent.conversation_state.escalation_level}")


if __name__ == "__main__":
    asyncio.run(test_escalation_levels()) 