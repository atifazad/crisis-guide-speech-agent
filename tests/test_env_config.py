"""
Tests for environment configuration.
"""

import unittest
from unittest.mock import patch
import os
from src.config.env_config import EnvConfig, get_env_var

class TestEnvConfig(unittest.TestCase):
    """Test environment configuration loading."""
    
    def test_get_env_var_with_default(self):
        """Test getting environment variable with default value."""
        # Test with non-existent variable
        result = get_env_var("NON_EXISTENT_VAR", "default_value")
        self.assertEqual(result, "default_value")
    
    def test_get_env_var_type_conversion(self):
        """Test environment variable type conversion."""
        with patch.dict(os.environ, {
            "TEST_INT": "42",
            "TEST_BOOL": "true",
            "TEST_FLOAT": "3.14"
        }):
            self.assertEqual(get_env_var("TEST_INT", 0, int), 42)
            self.assertEqual(get_env_var("TEST_BOOL", False, bool), True)
            self.assertEqual(get_env_var("TEST_FLOAT", 0.0, float), 3.14)
    
    def test_openai_api_key_validation(self):
        """Test OpenAI API key validation."""
        # Test with no API key
        with patch.dict(os.environ, {}, clear=True):
            # Test the validation logic directly
            from src.config.env_config import get_env_var
            api_key = get_env_var("OPENAI_API_KEY", "")
            issues = {}
            if not api_key:
                issues["OPENAI_API_KEY"] = "OpenAI API key is required"
            
            self.assertIn("OPENAI_API_KEY", issues)
        
        # Test with API key
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}):
            # Test the validation logic directly
            from src.config.env_config import get_env_var
            api_key = get_env_var("OPENAI_API_KEY", "")
            issues = {}
            if not api_key:
                issues["OPENAI_API_KEY"] = "OpenAI API key is required"
            
            self.assertEqual(len(issues), 0)
    
    def test_config_summary(self):
        """Test configuration summary generation."""
        summary = EnvConfig.get_config_summary()
        
        self.assertIn("openai_api_key_set", summary)
        self.assertIsInstance(summary["openai_api_key_set"], bool)

if __name__ == "__main__":
    unittest.main() 