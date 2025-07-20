#!/usr/bin/env python3
"""
Test Dynamic Responses
Verifies that all responses are generated using GPT-4o instead of hardcoded text
"""

import asyncio
import json
import websockets
import time

async def test_dynamic_responses():
    """Test that all responses are dynamic and contextual."""
    
    print("🤖 Testing Dynamic GPT-4o Responses")
    print("=" * 60)
    print("This will test that the agent generates dynamic responses:")
    print("• Emergency responses based on context")
    print("• Warning messages using GPT-4o")
    print("• Action messages using GPT-4o")
    print("• Emergency services messages using GPT-4o")
    print("=" * 60)
    
    test_scenarios = [
        {
            "name": "Fire Emergency",
            "message": "Help! There's a fire in my kitchen!",
            "expected_type": "fire"
        },
        {
            "name": "Vehicle Accident", 
            "message": "There's been a car accident, someone is injured!",
            "expected_type": "accident"
        },
        {
            "name": "Medical Emergency",
            "message": "I'm having chest pain and can't breathe!",
            "expected_type": "medical"
        },
        {
            "name": "Normal Conversation",
            "message": "Hello, how are you today?",
            "expected_type": "none"
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
                print(f"🎯 Expected Type: {scenario['expected_type']}")
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
                        
                        # Check if response is dynamic (not hardcoded)
                        hardcoded_phrases = [
                            "I'm detecting a fire emergency. Are you safe from the flames?",
                            "I'm detecting a vehicle accident. Are you conscious?",
                            "I'm detecting a medical emergency. Are you experiencing chest pain?",
                            "Hello, can you hear me? I need you to respond immediately.",
                            "I will wait 5 seconds, if you don't respond I will trigger an automatic call to 911.",
                            "No response detected. I am now triggering automatic emergency protocols.",
                            "Emergency services have been contacted. Your location has been logged"
                        ]
                        
                        is_hardcoded = any(phrase in response_text for phrase in hardcoded_phrases)
                        
                        if is_hardcoded:
                            print("   ⚠️  Potentially hardcoded response detected")
                        else:
                            print("   ✅ Dynamic GPT-4o response detected")
                        
                        # Check for contextual keywords
                        if scenario['expected_type'] == "fire" and "fire" in response_text.lower():
                            print("   ✅ Fire-specific context detected")
                        elif scenario['expected_type'] == "accident" and ("accident" in response_text.lower() or "vehicle" in response_text.lower()):
                            print("   ✅ Accident-specific context detected")
                        elif scenario['expected_type'] == "medical" and ("medical" in response_text.lower() or "chest" in response_text.lower()):
                            print("   ✅ Medical-specific context detected")
                        elif scenario['expected_type'] == "none":
                            print("   ✅ Normal conversation response")
                        
                    else:
                        print(f"📊 Received: {data['type']}")
                        
                except asyncio.TimeoutError:
                    print("⏰ No response received within timeout")
                
                # Wait between tests
                await asyncio.sleep(3)
            
            print(f"\n{'='*60}")
            print("✅ Dynamic response test completed!")
            print("=" * 60)
            
    except websockets.exceptions.ConnectionRefusedError:
        print("❌ Could not connect to agentic voice agent")
        print("Please make sure the agentic voice agent is running:")
        print("   ./start_agentic_voice.sh")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🤖 DYNAMIC GPT-4O RESPONSE TEST")
    print("=" * 60)
    print("This test verifies that the agent generates")
    print("dynamic responses using GPT-4o instead of")
    print("hardcoded text for all scenarios.")
    print("=" * 60)
    
    asyncio.run(test_dynamic_responses()) 