#!/usr/bin/env python3
"""
Unit tests for AgenticVoiceAgent - Working tests only
"""

import unittest
import asyncio
import json
from unittest.mock import Mock, AsyncMock, patch
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.agents.agentic_voice_agent import AgenticConversationState


class TestAgenticConversationState(unittest.TestCase):
    """Test the AgenticConversationState class."""
    
    def setUp(self):
        self.state = AgenticConversationState()
    
    def test_initial_state(self):
        """Test initial state values."""
        self.assertEqual(self.state.current_step, 0)
        self.assertEqual(self.state.steps_completed, [])
        self.assertFalse(self.state.pending_confirmation)
        self.assertEqual(self.state.escalation_level, 0)
        self.assertTrue(self.state.user_responsive)
        self.assertIsNone(self.state.emergency_type)
    
    def test_start_emergency_protocol(self):
        """Test starting emergency protocol."""
        self.state.start_emergency_protocol("fire")
        self.assertEqual(self.state.emergency_type, "fire")
        self.assertEqual(self.state.current_step, 1)
        self.assertEqual(self.state.steps_completed, [])
        self.assertEqual(self.state.escalation_level, 0)
    
    def test_fire_protocol_steps(self):
        """Test fire emergency protocol steps."""
        self.state.start_emergency_protocol("fire")
        
        # Step 1
        step = self.state.get_next_step()
        self.assertEqual(step["action"], "immediate_safety")
        self.assertTrue(step["confirmation_required"])
        self.assertEqual(step["timeout"], 10)
        
        # Move to step 2
        self.state.current_step = 2
        step = self.state.get_next_step()
        self.assertEqual(step["action"], "location_confirmation")
        self.assertTrue(step["confirmation_required"])
    
    def test_medical_protocol_steps(self):
        """Test medical emergency protocol steps."""
        self.state.start_emergency_protocol("medical")
        
        # Step 1
        step = self.state.get_next_step()
        self.assertEqual(step["action"], "consciousness_check")
        self.assertTrue(step["confirmation_required"])
        
        # Move to step 2
        self.state.current_step = 2
        step = self.state.get_next_step()
        self.assertEqual(step["action"], "symptoms_assessment")
    
    def test_danger_protocol_steps(self):
        """Test danger/threat protocol steps."""
        self.state.start_emergency_protocol("danger")
        
        # Step 1
        step = self.state.get_next_step()
        self.assertEqual(step["action"], "immediate_safety")
        self.assertTrue(step["confirmation_required"])
    
    def test_confirm_step(self):
        """Test step confirmation."""
        self.state.start_emergency_protocol("fire")
        self.state.pending_confirmation = True
        self.state.confirmation_timeout = 10
        
        self.state.confirm_step()
        
        self.assertEqual(self.state.current_step, 2)
        self.assertEqual(self.state.steps_completed, [1])
        self.assertFalse(self.state.pending_confirmation)
        self.assertEqual(self.state.confirmation_timeout, 0)
    
    def test_escalate(self):
        """Test escalation logic."""
        self.state.start_emergency_protocol("fire")
        self.state.pending_confirmation = True
        
        self.state.escalate()
        
        self.assertEqual(self.state.escalation_level, 1)
        self.assertFalse(self.state.pending_confirmation)
        
        # Test escalation to emergency call
        self.state.escalate()
        self.assertEqual(self.state.current_step, 4)


class TestEmergencyProtocols(unittest.TestCase):
    """Test emergency protocol implementations."""
    
    def setUp(self):
        self.state = AgenticConversationState()
    
    def test_fire_protocol_complete_flow(self):
        """Test complete fire emergency protocol flow."""
        self.state.start_emergency_protocol("fire")
        
        # Step 1: Immediate safety
        step = self.state.get_next_step()
        self.assertEqual(step["action"], "immediate_safety")
        self.assertIn("safely out", step["message"])
        
        # Step 2: Location confirmation
        self.state.current_step = 2
        step = self.state.get_next_step()
        self.assertEqual(step["action"], "location_confirmation")
        self.assertIn("address", step["message"])
        
        # Step 3: Fire details
        self.state.current_step = 3
        step = self.state.get_next_step()
        self.assertEqual(step["action"], "fire_details")
        self.assertIn("contained", step["message"])
        
        # Step 4: Call emergency
        self.state.current_step = 4
        step = self.state.get_next_step()
        self.assertEqual(step["action"], "call_emergency")
        self.assertIn("911", step["message"])
    
    def test_medical_protocol_complete_flow(self):
        """Test complete medical emergency protocol flow."""
        self.state.start_emergency_protocol("medical")
        
        # Step 1: Consciousness check
        step = self.state.get_next_step()
        self.assertEqual(step["action"], "consciousness_check")
        self.assertIn("conscious", step["message"])
        
        # Step 2: Symptoms assessment
        self.state.current_step = 2
        step = self.state.get_next_step()
        self.assertEqual(step["action"], "symptoms_assessment")
        self.assertIn("symptoms", step["message"])
        
        # Step 3: Location confirmation
        self.state.current_step = 3
        step = self.state.get_next_step()
        self.assertEqual(step["action"], "location_confirmation")
        self.assertIn("address", step["message"])
        
        # Step 4: Call emergency
        self.state.current_step = 4
        step = self.state.get_next_step()
        self.assertEqual(step["action"], "call_emergency")
        self.assertIn("911", step["message"])
    
    def test_danger_protocol_complete_flow(self):
        """Test complete danger/threat protocol flow."""
        self.state.start_emergency_protocol("danger")
        
        # Step 1: Immediate safety
        step = self.state.get_next_step()
        self.assertEqual(step["action"], "immediate_safety")
        self.assertIn("safe location", step["message"])
        
        # Step 2: Threat assessment
        self.state.current_step = 2
        step = self.state.get_next_step()
        self.assertEqual(step["action"], "threat_assessment")
        self.assertIn("happening", step["message"])
        
        # Step 3: Location confirmation
        self.state.current_step = 3
        step = self.state.get_next_step()
        self.assertEqual(step["action"], "location_confirmation")
        self.assertIn("address", step["message"])
        
        # Step 4: Call emergency
        self.state.current_step = 4
        step = self.state.get_next_step()
        self.assertEqual(step["action"], "call_emergency")
        self.assertIn("911", step["message"])


if __name__ == "__main__":
    unittest.main() 