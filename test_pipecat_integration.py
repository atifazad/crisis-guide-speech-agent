#!/usr/bin/env python3
"""
Test script for pipecat integration.
Tests the real-time audio pipeline with crisis response capabilities.
"""

import asyncio
import os
import sys
import time
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.pipecat import PipecatPipelineManager

def test_pipecat_services():
    """Test pipecat services without starting the pipeline."""
    print("🔧 Testing Pipecat Services")
    print("=" * 50)
    
    # Load environment
    load_dotenv()
    
    # Initialize pipeline manager
    pipeline_manager = PipecatPipelineManager()
    
    # Test service connections
    print("\n1. Testing Service Connections...")
    service_results = pipeline_manager.test_services()
    
    for service, result in service_results.items():
        status = "✅ Success" if result.get('success', False) else "❌ Failed"
        print(f"   {service.upper()}: {status}")
        if not result.get('success', False):
            print(f"      Error: {result.get('error', 'Unknown error')}")
    
    # Test pipeline creation
    print("\n2. Testing Pipeline Creation...")
    pipeline_created = pipeline_manager.create_pipeline()
    print(f"   Pipeline Creation: {'✅ Success' if pipeline_created else '❌ Failed'}")
    
    # Test pipeline status
    print("\n3. Testing Pipeline Status...")
    status = pipeline_manager.get_pipeline_status()
    print(f"   Pipeline Created: {'✅ Yes' if status['pipeline_created'] else '❌ No'}")
    print(f"   Runner Active: {'✅ Yes' if status['runner_active'] else '❌ No'}")
    print(f"   Is Running: {'✅ Yes' if status['is_running'] else '❌ No'}")
    
    # Test conversation state
    print("\n4. Testing Conversation State...")
    conv_summary = status['conversation']
    print(f"   Current State: {conv_summary['current_state']}")
    print(f"   Current Urgency: {conv_summary['current_urgency']}")
    print(f"   Total Turns: {conv_summary['total_turns']}")
    
    return pipeline_manager

async def test_pipecat_pipeline():
    """Test the full pipecat pipeline."""
    print("\n🚀 Testing Pipecat Pipeline")
    print("=" * 50)
    
    # Load environment
    load_dotenv()
    
    # Initialize pipeline manager
    pipeline_manager = PipecatPipelineManager()
    
    # Set up callbacks
    def on_user_input(text):
        print(f"👤 User Input: {text}")
    
    def on_ai_response(text, urgency):
        print(f"🤖 AI Response ({urgency}): {text}")
    
    def on_escalation(message):
        print(f"🚨 ESCALATION: {message}")
    
    pipeline_manager.set_callbacks(
        on_user_input=on_user_input,
        on_ai_response=on_ai_response,
        on_escalation=on_escalation
    )
    
    # Test pipeline creation
    print("\n1. Creating Pipeline...")
    if not pipeline_manager.create_pipeline():
        print("❌ Failed to create pipeline")
        return False
    
    print("✅ Pipeline created successfully")
    
    # Test pipeline start (brief test)
    print("\n2. Testing Pipeline Start (5 seconds)...")
    try:
        # Start pipeline
        started = await pipeline_manager.start_pipeline()
        if started:
            print("✅ Pipeline started successfully")
            print("   Listening for 5 seconds...")
            
            # Run for 5 seconds
            await asyncio.sleep(5)
            
            # Stop pipeline
            await pipeline_manager.stop_pipeline()
            print("✅ Pipeline stopped successfully")
            
        else:
            print("❌ Failed to start pipeline")
            return False
            
    except Exception as e:
        print(f"❌ Error during pipeline test: {str(e)}")
        return False
    
    return True

def main():
    """Main test function."""
    print("🧪 Pipecat Integration Test")
    print("=" * 60)
    
    # Test services first
    pipeline_manager = test_pipecat_services()
    
    # Ask user if they want to test the full pipeline
    print("\n" + "=" * 60)
    print("Next Steps:")
    print("1. The pipecat services have been tested")
    print("2. You can now test the full pipeline with real-time audio")
    print("3. The pipeline will use your microphone and speakers")
    
    response = input("\nDo you want to test the full pipeline? (y/n): ").lower().strip()
    
    if response == 'y':
        print("\n🚀 Starting full pipeline test...")
        print("⚠️  This will use your microphone and speakers")
        print("⚠️  Speak clearly when prompted")
        
        # Run the async pipeline test
        asyncio.run(test_pipecat_pipeline())
    else:
        print("\n✅ Service testing complete!")
        print("You can run the full pipeline test later with:")
        print("python test_pipecat_integration.py")

if __name__ == "__main__":
    main() 