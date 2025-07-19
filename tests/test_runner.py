"""
Test runner for the Voice-to-Voice AI Assistant project.
"""

import unittest
import sys
import os
import time
from io import StringIO

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import all test modules
from tests.test_audio import (
    TestAudioRecorder,
    TestAudioDeviceManager,
    TestAudioPreprocessor
)
from tests.test_transcription import (
    TestWhisperClient,
    TestTranscriptionManager,
    TestTranscriptionIntegration
)
from tests.test_utils import (
    TestErrorHandler,
    TestAudioFileManager,
    TestTempFileContext,
    TestUtilsIntegration
)

from tests.test_config import (
    TestLanguageOptions,
    TestAudioSettings,
    TestWhisperSettings,
    TestUISettings,
    TestFileSettings,
    TestErrorMessages,
    TestSuccessMessages,
    TestAccuracyTips,
    TestTroubleshootingTips,
    TestConfigIntegration
)


def run_all_tests():
    """Run all unit tests and return results."""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        # Audio tests
        TestAudioRecorder,
        TestAudioDeviceManager,
        TestAudioPreprocessor,
        
        # Transcription tests
        TestWhisperClient,
        TestTranscriptionManager,
        TestTranscriptionIntegration,
        
        # Utils tests
        TestErrorHandler,
        TestAudioFileManager,
        TestTempFileContext,
        TestUtilsIntegration,
        

        
        # Config tests
        TestLanguageOptions,
        TestAudioSettings,
        TestWhisperSettings,
        TestUISettings,
        TestFileSettings,
        TestErrorMessages,
        TestSuccessMessages,
        TestAccuracyTips,
        TestTroubleshootingTips,
        TestConfigIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result


def run_specific_test_category(category):
    """Run tests for a specific category."""
    category_map = {
        'audio': [
            TestAudioRecorder,
            TestAudioDeviceManager,
            TestAudioPreprocessor
        ],
        'transcription': [
            TestWhisperClient,
            TestTranscriptionManager,
            TestTranscriptionIntegration
        ],
        'utils': [
            TestErrorHandler,
            TestAudioFileManager,
            TestTempFileContext,
            TestUtilsIntegration
        ],

        'config': [
            TestLanguageOptions,
            TestAudioSettings,
            TestWhisperSettings,
            TestUISettings,
            TestFileSettings,
            TestErrorMessages,
            TestSuccessMessages,
            TestAccuracyTips,
            TestTroubleshootingTips,
            TestConfigIntegration
        ]
    }
    
    if category not in category_map:
        print(f"Unknown category: {category}")
        print("Available categories:", list(category_map.keys()))
        return None
    
    test_suite = unittest.TestSuite()
    for test_class in category_map[category]:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result


def generate_test_report(result):
    """Generate a detailed test report."""
    report = []
    report.append("=" * 60)
    report.append("VOICE-TO-VOICE AI ASSISTANT - TEST REPORT")
    report.append("=" * 60)
    report.append("")
    
    # Summary
    report.append("SUMMARY:")
    report.append(f"  Tests run: {result.testsRun}")
    report.append(f"  Failures: {len(result.failures)}")
    report.append(f"  Errors: {len(result.errors)}")
    report.append(f"  Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    report.append("")
    
    # Calculate success rate
    total_tests = result.testsRun
    failed_tests = len(result.failures) + len(result.errors)
    success_rate = ((total_tests - failed_tests) / total_tests * 100) if total_tests > 0 else 0
    
    report.append(f"SUCCESS RATE: {success_rate:.1f}%")
    report.append("")
    
    # Failures
    if result.failures:
        report.append("FAILURES:")
        for test, traceback in result.failures:
            report.append(f"  {test}")
            report.append(f"    {traceback}")
        report.append("")
    
    # Errors
    if result.errors:
        report.append("ERRORS:")
        for test, traceback in result.errors:
            report.append(f"  {test}")
            report.append(f"    {traceback}")
        report.append("")
    
    # Test coverage by module
    report.append("TEST COVERAGE BY MODULE:")
    modules = {
        'Audio': ['TestAudioRecorder', 'TestAudioDeviceManager', 'TestAudioPreprocessor'],
        'Transcription': ['TestWhisperClient', 'TestTranscriptionManager', 'TestTranscriptionIntegration'],
        'Utils': ['TestErrorHandler', 'TestAudioFileManager', 'TestTempFileContext', 'TestUtilsIntegration'],
        'Config': ['TestLanguageOptions', 'TestAudioSettings', 'TestWhisperSettings', 'TestUISettings', 
                  'TestFileSettings', 'TestErrorMessages', 'TestSuccessMessages', 'TestAccuracyTips', 
                  'TestTroubleshootingTips', 'TestConfigIntegration']
    }
    
    for module, test_classes in modules.items():
        report.append(f"  {module}: {len(test_classes)} test classes")
    
    report.append("")
    report.append("=" * 60)
    
    return "\n".join(report)


def main():
    """Main function to run tests."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Run unit tests for Voice-to-Voice AI Assistant')
    parser.add_argument('--category', '-c', 
                       choices=['audio', 'transcription', 'utils', 'config'],
                       help='Run tests for a specific category')
    parser.add_argument('--report', '-r', action='store_true',
                       help='Generate detailed test report')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    print("Starting test execution...")
    start_time = time.time()
    
    if args.category:
        result = run_specific_test_category(args.category)
        if result is None:
            return 1
    else:
        result = run_all_tests()
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    print(f"\nTest execution completed in {execution_time:.2f} seconds")
    
    if args.report:
        report = generate_test_report(result)
        print(report)
        
        # Save report to file
        with open('test_report.txt', 'w') as f:
            f.write(report)
        print("Detailed report saved to test_report.txt")
    
    # Return appropriate exit code
    if result.failures or result.errors:
        return 1
    else:
        return 0


if __name__ == '__main__':
    sys.exit(main()) 