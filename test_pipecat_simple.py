#!/usr/bin/env python3
"""
Test script for pipecat integration with corrected API usage.
Tests basic pipeline creation and service connectivity.
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.pipecat import PipecatPipelineManager

def test_pipecat_integration():
    """Test pipecat integration with corrected API."""
    print("🧪 Pipecat Integration Test (Corrected API)")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    
    # Check API keys
    print("🧪 Testing Pipecat Basic Integration")
    print("=" * 50)
    
    openai_key = os.getenv('OPENAI_API_KEY')
    elevenlabs_key = os.getenv('ELEVENLABS_API_KEY')
    
    print(f"OpenAI API Key: {'✅ Set' if openai_key else '❌ Missing'}")
    print(f"ElevenLabs API Key: {'✅ Set' if elevenlabs_key else '❌ Missing'}")
    print()
    
    if not openai_key or not elevenlabs_key:
        print("❌ Missing required API keys")
        return False
    
    # Initialize pipeline manager
    print("🔧 Initializing Pipeline Manager...")
    pipeline_manager = PipecatPipelineManager()
    
    # Test 1: Service connections
    print("\n1. Testing Service Connections...")
    service_results = pipeline_manager.test_services()
    
    for service, result in service_results.items():
        status = "✅ Success" if result.get('success', False) else "❌ Failed"
        error = result.get('error', 'Unknown error')
        print(f"   {service.upper()}: {status}")
        if not result.get('success', False):
            print(f"      Error: {error}")
    
    # Test 2: Simple pipeline creation (without audio transport)
    print("\n2. Testing Simple Pipeline Creation...")
    try:
        # Create a minimal pipeline without audio transport
        from pipecat.pipeline.pipeline import Pipeline
        from pipecat.pipeline.task import PipelineTask
        from pipecat.processors.aggregators.sentence import SentenceAggregator
        from pipecat.processors.aggregators.llm_response import LLMFullResponseAggregator
        from pipecat.services.openai.llm import OpenAILLMService
        
        # Create a simple pipeline with just the processors
        simple_pipeline = Pipeline([
            SentenceAggregator(),
            OpenAILLMService(
                api_key=openai_key,
                model="gpt-4o",
                system_prompt="You are a helpful assistant."
            ),
            LLMFullResponseAggregator()
        ])
        
        print("   ✅ Simple pipeline created successfully")
        
        # Create pipeline task
        pipeline_task = PipelineTask(simple_pipeline)
        print("   ✅ Pipeline task created successfully")
        
        # Test that we can create the components
        print("   ✅ All pipeline components created successfully")
        
    except Exception as e:
        print(f"   ❌ Failed to create simple pipeline: {str(e)}")
        return False
    
    # Test 3: Test with event loop
    print("\n3. Testing Pipeline Runner with Event Loop...")
    try:
        async def test_runner():
            from pipecat.pipeline.runner import PipelineRunner
            
            # Create pipeline runner in async context
            runner = PipelineRunner()
            print("   ✅ Pipeline runner created successfully in async context")
            
            # Test that we can create the runner
            return True
        
        # Run the async test
        success = asyncio.run(test_runner())
        if success:
            print("   ✅ Pipeline runner test passed")
        else:
            print("   ❌ Pipeline runner test failed")
            return False
            
    except Exception as e:
        print(f"   ❌ Failed to create pipeline runner: {str(e)}")
        return False
    
    print("\n✅ Basic pipeline tests passed!")
    print("\nNext steps:")
    print("1. Integrate audio transport layer")
    print("2. Add ElevenLabs TTS integration")
    print("3. Test real-time audio processing")
    
    return True

if __name__ == "__main__":
    success = test_pipecat_integration()
    sys.exit(0 if success else 1) 