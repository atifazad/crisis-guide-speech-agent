#!/usr/bin/env python3
"""
Test script for LLM-driven emergency response system
"""

import asyncio
import json
from unittest.mock import Mock, AsyncMock
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.agents.agentic_voice_agent import AgenticVoiceAgent, AgenticConversationState


async def test_llm_emergency_response():
    """Test the LLM-driven emergency response system."""
    
    # Create a mock websocket
    mock_websocket = Mock()
    mock_websocket.send = AsyncMock()
    
    # Create agent
    agent = AgenticVoiceAgent()
    
    print("🧪 Testing LLM-driven emergency response system...")
    
    # Test 1: Fire emergency detection
    print("\n1. Testing fire emergency detection...")
    emergency_detected, emergency_type = agent._detect_emergency("There's a fire in my kitchen!")
    print(f"   Emergency detected: {emergency_detected}")
    print(f"   Emergency type: {emergency_type}")
    
    # Test 2: Medical emergency detection
    print("\n2. Testing medical emergency detection...")
    emergency_detected, emergency_type = agent._detect_emergency("My chest hurts and I can't breathe")
    print(f"   Emergency detected: {emergency_detected}")
    print(f"   Emergency type: {emergency_type}")
    
    # Test 3: Danger/threat detection
    print("\n3. Testing danger/threat detection...")
    emergency_detected, emergency_type = agent._detect_emergency("Someone is following me and I'm scared")
    print(f"   Emergency detected: {emergency_detected}")
    print(f"   Emergency type: {emergency_type}")
    
    # Test 4: Positive confirmation detection
    print("\n4. Testing positive confirmation detection...")
    positive_words = ["yes", "yeah", "yep", "sure", "okay", "ok", "correct", "right", "true", "confirmed"]
    for word in positive_words:
        is_positive = agent._is_positive_confirmation(word)
        print(f"   '{word}' -> {is_positive}")
    
    # Test 5: Negative confirmation detection
    print("\n5. Testing negative confirmation detection...")
    negative_words = ["no", "nope", "not", "never", "wrong", "false", "cancel"]
    for word in negative_words:
        is_positive = agent._is_positive_confirmation(word)
        print(f"   '{word}' -> {is_positive}")
    
    # Test 6: Conversation state management
    print("\n6. Testing conversation state management...")
    state = AgenticConversationState()
    print(f"   Initial step: {state.current_step}")
    print(f"   Initial escalation level: {state.escalation_level}")
    
    state.start_emergency_protocol("fire")
    print(f"   After starting fire protocol: {state.current_step}")
    print(f"   Emergency type: {state.emergency_type}")
    
    state.escalate()
    print(f"   After escalation: {state.escalation_level}")
    
    print("\n✅ LLM-driven emergency response system tests completed!")


if __name__ == "__main__":
    asyncio.run(test_llm_emergency_response()) 