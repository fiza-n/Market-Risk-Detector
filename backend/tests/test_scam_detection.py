"""
Unit tests for the Scam Detection module (Person C Scope)
"""

import sys
import unittest
from unittest.mock import patch, MagicMock

# Ensure config environment is mocked or pre-configured
from config import Config
Config.GEMINI_API_KEY = "mock-api-key"

from scam_detection.groq_client import analyze_scam_patterns
from scam_detection.feedback_loop import get_recent_correction_hints

class TestScamDetection(unittest.TestCase):

    @patch("scam_detection.groq_client.genai.Client")
    def test_high_risk_listing(self, mock_client_class):
        # 1. A listing containing "pay via JazzCash before delivery, urgent, leaving country"
        # should score high (>60) and include an advance-payment flag.
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.text = (
            '{"scam_score": 90, '
            '"scam_flags": ["Advance payment requested via JazzCash", "High pressure urgency"], '
            '"tip": "Avoid this listing. Insist on cash on delivery after inspection."}'
        )
        mock_client.models.generate_content.return_value = mock_response

        title = "iPhone 13 Urgent Sale Leaving Country"
        description = "Need to sell urgently because I am leaving the country tomorrow. Price is very low. Pay via JazzCash before delivery."
        seller_info = "WhatsApp only"

        result = analyze_scam_patterns(title, description, seller_info)
        
        self.assertGreater(result["scam_score"], 60)
        self.assertTrue(any("advance payment" in flag.lower() or "pay" in flag.lower() for flag in result["scam_flags"]))
        self.assertEqual(result["scam_score"], 90)
        self.assertEqual(len(result["scam_flags"]), 2)

    @patch("scam_detection.groq_client.genai.Client")
    def test_low_risk_listing(self, mock_client_class):
        # 2. A plain, detail-rich listing with no pressure language scores low (<30).
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.text = (
            '{"scam_score": 10, '
            '"scam_flags": [], '
            '"tip": "Safe to proceed. Standard inspection recommended."}'
        )
        mock_client.models.generate_content.return_value = mock_response

        title = "Original Solid Wood Dining Table"
        description = "Solid sheesham wood dining table with 6 matching chairs. Very minor scratches, overall 9/10 condition. Inspect in person in Gulberg, Lahore. Payment mode: cash on delivery or bank transfer after inspection."
        seller_info = "Lahore resident since 10 years"

        result = analyze_scam_patterns(title, description, seller_info)
        
        self.assertLess(result["scam_score"], 30)
        self.assertEqual(len(result["scam_flags"]), 0)

    @patch("scam_detection.groq_client.genai.Client")
    def test_response_contract_types(self, mock_client_class):
        # 3. analyze_scam_patterns returns a dict matching the exact keys/types in the contract.
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        
        # Test float score coercion and flag string coercion
        mock_response = MagicMock()
        mock_response.text = (
            '{"scam_score": 45.6, '
            '"scam_flags": ["flag1", 123], '
            '"tip": "be careful"}'
        )
        mock_client.models.generate_content.return_value = mock_response

        result = analyze_scam_patterns("Test title", "Test description", None)
        
        self.assertIsInstance(result, dict)
        self.assertIn("scam_score", result)
        self.assertIn("scam_flags", result)
        self.assertIn("tip", result)
        self.assertIn("raw_llm_response", result)
        
        self.assertIsInstance(result["scam_score"], int)
        self.assertEqual(result["scam_score"], 46) # Float rounded to nearest int
        
        self.assertIsInstance(result["scam_flags"], list)
        self.assertEqual(result["scam_flags"], ["flag1", "123"]) # All elements coerced to strings
        
        self.assertIsInstance(result["tip"], str)
        self.assertEqual(result["tip"], "be careful")
        self.assertIsInstance(result["raw_llm_response"], str)

    @patch("scam_detection.groq_client.genai.Client")
    def test_malformed_non_json_raises(self, mock_client_class):
        # 4. Malformed/non-JSON model output causes the function to raise, not return a silently broken dict.
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.text = "NOT VALID JSON"
        mock_client.models.generate_content.return_value = mock_response

        # Should raise an error after retrying twice
        with self.assertRaises(RuntimeError):
            analyze_scam_patterns("Test", "Test", None)
            
        # Ensure generate_content was called twice (initial + 1 retry)
        self.assertEqual(mock_client.models.generate_content.call_count, 2)

    def test_feedback_loop_import_failure(self):
        # 5a. get_recent_correction_hints returns "" without raising when the db import fails.
        with patch.dict("sys.modules", {"db": None}):
            hints = get_recent_correction_hints()
            self.assertEqual(hints, "")

    @patch("db.db", None)
    def test_feedback_loop_db_none(self):
        # 5b. get_recent_correction_hints returns "" without raising when db.db is None.
        hints = get_recent_correction_hints()
        self.assertEqual(hints, "")

    @patch("db.db")
    def test_feedback_loop_success_parsing(self, mock_db):
        # Positive path: ensure database entries are retrieved and parsed correctly
        mock_cursor = MagicMock()
        mock_cursor.sort.return_value.limit.return_value = [
            {
                "input": {
                    "title": "Bad Phone",
                    "description": "send token money"
                },
                "scam_analysis": {
                    "scam_score": 75,
                    "scam_flags": ["Token money"],
                    "tip": "Do not pay"
                },
                "created_at": "2026-08-24T12:00:00"
            }
        ]
        mock_db.submissions.find.return_value = mock_cursor

        hints = get_recent_correction_hints()
        self.assertIn("Bad Phone", hints)
        self.assertIn("send token money", hints)
        self.assertIn("Score=75", hints)

if __name__ == "__main__":
    unittest.main()
