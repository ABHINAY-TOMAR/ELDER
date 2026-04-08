import unittest
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock
from app.models.requirement_spec import RequirementSpec
from app.engines.requirement_parser import RequirementParser
from app.engines.domain_classifier import DomainClassifier
from app.engines.fast_pattern_matcher import FastPatternMatcher
from app.engines.model_selector import ModelSelector

class TestWeek2(unittest.IsolatedAsyncioTestCase):
    """
    Test suite for Week 2 deliverables: Core Reasoning Engines.
    """

    # --- Requirement Parser Tests ---

    @patch("app.engines.requirement_parser.httpx.AsyncClient.post")
    async def test_requirement_parser_mock(self, mock_post):
        # Mock OpenAI response
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = {
            "choices": [{
                "message": {
                    "content": """{
                        "project_name": "TestAI",
                        "domain": "ai_native",
                        "team_size": 2,
                        "budget_usd": 10000,
                        "expected_users": 50000,
                        "latency_requirement_ms": 300,
                        "data_sensitivity": "pii",
                        "deployment_target": "cloud",
                        "constraints": ["must use AWS"],
                        "timeline_weeks": 12,
                        "extracted_features": ["agentic search", "RAG"]
                    }"""
                }
            }],
            "usage": {"prompt_tokens": 100, "completion_tokens": 200}
        }
        mock_post.return_value = mock_resp
        
        parser = RequirementParser()
        parser.api_key = "fake_key"
        
        spec = await parser.parse("We are 2 engineers building TestAI using RAG and agents on AWS with 10k budget.")
        
        self.assertEqual(spec.project_name, "TestAI")
        self.assertEqual(spec.domain, "ai_native")
        self.assertEqual(spec.team_size, 2)
        self.assertIn("RAG", spec.extracted_features)

    # --- Domain Classifier Tests ---

    def test_domain_classifier(self):
        classifier = DomainClassifier()
        
        # Test AI signals
        spec_ai = RequirementSpec(project_name="AI Bot", extracted_features=["LLM", "agent", "RAG"])
        result = classifier.classify(spec_ai)
        self.assertEqual(result.primary_domain, "ai_native")
        self.assertGreater(result.confidence, 0.6)

        # Test Microservices signals
        spec_ms = RequirementSpec(project_name="Store", extracted_features=["REST API", "CRUD", "Dashboard"])
        result = classifier.classify(spec_ms)
        self.assertEqual(result.primary_domain, "microservices")

        # Test Data Pipeline signals
        spec_data = RequirementSpec(project_name="Analyzer", extracted_features=["ETL", "Spark", "Streaming"])
        result = classifier.classify(spec_data)
        self.assertEqual(result.primary_domain, "data_pipeline")

    # --- Fast Pattern Matcher Tests ---

    def test_fast_pattern_matcher(self):
        matcher = FastPatternMatcher()
        
        # Test standard match
        spec = RequirementSpec(
            project_name="Lean Startup", 
            domain="microservices", 
            team_size=1, 
            budget_usd=1000
        )
        rec, risks = matcher.match(spec)
        
        self.assertEqual(rec.tech_stack["database"], "Supabase or PostgreSQL")
        self.assertEqual(len(risks), 0)

        # Test risky match (high scale + PII)
        spec_risky = RequirementSpec(
            project_name="Big Bank", 
            domain="microservices", 
            team_size=10, 
            expected_users=1_000_000,
            data_sensitivity="pii"
        )
        rec, risks = matcher.match(spec_risky)
        
        # Should have scaling and security risks
        risk_types = [r.decision_type for r in risks]
        self.assertIn("scaling", risk_types)
        self.assertIn("security", risk_types)

    # --- Model Selector Tests ---

    def test_model_selector(self):
        selector = ModelSelector()
        
        # High complexity + budget -> Sonnet
        model = selector.select(complexity="high", budget_remaining_usd=10.0)
        self.assertEqual(model, "claude-3-5-sonnet")

        # Low complexity -> Haiku
        model = selector.select(complexity="low", budget_remaining_usd=10.0)
        self.assertEqual(model, "claude-3-5-haiku")

        # High complexity but NO budget -> Haiku
        model = selector.select(complexity="high", budget_remaining_usd=0.1)
        self.assertEqual(model, "claude-3-5-haiku")

        # Risky task -> Sonnet
        model = selector.select(complexity="medium", budget_remaining_usd=5.0, is_risky=True)
        self.assertEqual(model, "claude-3-5-sonnet")

if __name__ == "__main__":
    unittest.main()
