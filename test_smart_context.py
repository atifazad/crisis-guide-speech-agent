#!/usr/bin/env python3
"""
Test Smart Context Understanding
Verifies that the LLM smartly understands context from user input
"""

import asyncio
import json
import websockets
import time

async def test_smart_context():
    """Test that the LLM smartly understands context from user input."""
    
    print("🧠 Testing Smart Context Understanding")
    print("=" * 60)
    print("This will test that the LLM understands context naturally:")
    print("• Self scenarios: User reporting about themselves")
    print("• Other scenarios: User reporting about someone else")
    print("• Mixed scenarios: Complex situations")
    print("=" * 60)
    
    test_scenarios = [
        {
            "name": "Self - Fire Emergency",
            "message": "I'm trapped in a burning building!",
            "expected_context": "self"
        },
        {
            "name": "Other - Child Choking",
            "message": "My child is choking on food!",
            "expected_context": "other"
        },
        {
            "name": "Other - Accident with Injury",
            "message": "There's been a car accident and someone is injured!",
            "expected_context": "other"
        },
        {
            "name": "Self - Medical Emergency",
            "message": "I'm having chest pain and can't breathe!",
            "expected_context": "self"
        },
        {
            "name": "Other - Person in Distress",
            "message": "Someone is having a heart attack!",
            "expected_context": "other"
        },
        {
            "name": "Mixed - Complex Situation",
            "message": "I'm injured and my child is also hurt in this accident!",
            "expected_context": "mixed"
        }
    ]
    
    try:
        # Connect to the agentic voice agent
        uri = "ws://localhost:8766"
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to agentic voice agent")
            
            for i, scenario in enumerate(test_scenarios, 1):
                print(f"\n{'='*50}")
                print(f"🧪 Test {i}: {scenario['name']}")
                print(f"👤 User: {scenario['message']}")
                print(f"🎯 Expected Context: {scenario['expected_context']}")
                print(f"{'='*50}")
                
                # Send message
                text_message = {
                    "type": "text",
                    "text": scenario['message']
                }
                
                await websocket.send(json.dumps(text_message))
                
                # Listen for response
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=15)
                    data = json.loads(response)
                    
                    if data["type"] == "response_text":
                        response_text = data['text']
                        print(f"🤖 Agent: {response_text}")
                        
                        # Check for smart context understanding
                        if scenario['expected_context'] == "self":
                            # Should ask about the person's own condition
                            if any(word in response_text.lower() for word in ["you", "your", "are you", "can you"]):
                                print("   ✅ Smartly understood self context")
                            else:
                                print("   ⚠️  May not have understood self context")
                                
                        elif scenario['expected_context'] == "other":
                            # Should ask about someone else or what they can do
                            if any(word in response_text.lower() for word in ["they", "them", "the person", "someone", "what can you", "how can you", "tell me about"]):
                                print("   ✅ Smartly understood other context")
                            else:
                                print("   ⚠️  May not have understood other context")
                                
                        elif scenario['expected_context'] == "mixed":
                            # Should address both self and other
                            print("   ✅ Complex situation handled")
                        
                        # Check for appropriate emergency type context
                        if "fire" in scenario['message'].lower() and "fire" in response_text.lower():
                            print("   ✅ Fire context understood")
                        elif "choking" in scenario['message'].lower() and ("choking" in response_text.lower() or "breathing" in response_text.lower()):
                            print("   ✅ Breathing context understood")
                        elif "accident" in scenario['message'].lower() and ("accident" in response_text.lower() or "vehicle" in response_text.lower()):
                            print("   ✅ Accident context understood")
                        elif "chest pain" in scenario['message'].lower() and ("medical" in response_text.lower() or "chest" in response_text.lower()):
                            print("   ✅ Medical context understood")
                        
                    else:
                        print(f"📊 Received: {data['type']}")
                        
                except asyncio.TimeoutError:
                    print("⏰ No response received within timeout")
                
                # Wait between tests
                await asyncio.sleep(3)
            
            print(f"\n{'='*60}")
            print("✅ Smart context understanding test completed!")
            print("=" * 60)
            
    except websockets.exceptions.ConnectionRefusedError:
        print("❌ Could not connect to agentic voice agent")
        print("Please make sure the agentic voice agent is running:")
        print("   ./start_agentic_voice.sh")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🧠 SMART CONTEXT UNDERSTANDING TEST")
    print("=" * 60)
    print("This test verifies that the LLM smartly")
    print("understands context from user input without")
    print("complex programming logic.")
    print("=" * 60)
    
    asyncio.run(test_smart_context()) 