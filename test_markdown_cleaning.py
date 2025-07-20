#!/usr/bin/env python3
"""
Test Markdown Cleaning
Verifies that markdown formatting is removed from agent responses
"""

import asyncio
import json
import websockets
import time

async def test_markdown_cleaning():
    """Test that markdown formatting is cleaned from responses."""
    
    print("🧹 Testing Markdown Cleaning")
    print("=" * 50)
    print("This will test that the agent removes markdown formatting:")
    print("• **bold** text → bold text")
    print("• *italic* text → italic text")
    print("• `code` text → code text")
    print("=" * 50)
    
    test_messages = [
        "Hello, this is a normal message",
        "Can you help me with something?",
        "I need assistance with a problem"
    ]
    
    try:
        # Connect to the agentic voice agent
        uri = "ws://localhost:8766"
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to agentic voice agent")
            
            for i, message in enumerate(test_messages, 1):
                print(f"\n{'='*40}")
                print(f"🧪 Test {i}: Normal conversation")
                print(f"👤 User: {message}")
                print(f"{'='*40}")
                
                # Send message
                text_message = {
                    "type": "text",
                    "text": message
                }
                
                await websocket.send(json.dumps(text_message))
                
                # Listen for response
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=10)
                    data = json.loads(response)
                    
                    if data["type"] == "response_text":
                        response_text = data['text']
                        print(f"🤖 Agent: {response_text}")
                        
                        # Check for markdown characters
                        if "**" in response_text or "*" in response_text or "`" in response_text:
                            print("   ❌ Markdown formatting detected in response!")
                            print(f"   Raw response: {repr(response_text)}")
                        else:
                            print("   ✅ No markdown formatting detected")
                    else:
                        print(f"📊 Received: {data['type']}")
                        
                except asyncio.TimeoutError:
                    print("⏰ No response received within timeout")
                
                # Wait between tests
                await asyncio.sleep(2)
            
            print(f"\n{'='*50}")
            print("✅ Markdown cleaning test completed!")
            print("=" * 50)
            
    except websockets.exceptions.ConnectionRefusedError:
        print("❌ Could not connect to agentic voice agent")
        print("Please make sure the agentic voice agent is running:")
        print("   ./start_agentic_voice.sh")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🧹 MARKDOWN CLEANING TEST")
    print("=" * 50)
    print("This test verifies that the agent removes")
    print("markdown formatting from responses before")
    print("sending them to text-to-speech.")
    print("=" * 50)
    
    asyncio.run(test_markdown_cleaning()) 