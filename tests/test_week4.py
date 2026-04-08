import unittest
import asyncio
import json
from unittest.mock import MagicMock, patch, AsyncMock
from app.models.requirement_spec import RequirementSpec
from app.engines.hybrid_reasoner import HybridReasoner, DeepThought
from app.engines.fast_pattern_matcher import StackRecommendation, RiskyDecision

class TestWeek4(unittest.IsolatedAsyncioTestCase):
    """
    Test suite for Week 4 deliverables: Hybrid Reasoning.
    """

    def setUp(self):
        self.fast_rec = StackRecommendation(
            tech_stack={"database": "PostgreSQL", "cache": "None"},
            deployment_target="Render",
            rationale="Fast",
            confidence=0.95
        )
        self.spec = RequirementSpec(project_name="TestProj", domain="microservices")

    async def test_hybrid_reasoner_fast_path(self):
        # No risks -> returns fast_rec immediately
        reasoner = HybridReasoner()
        result = await reasoner.reason(self.spec, self.fast_rec, [])
        
        self.assertEqual(result.tech_stack["database"], "PostgreSQL")
        self.assertEqual(len(result.deep_reasoning_applied), 0)
        self.assertEqual(result.confidence, 0.95)

    @patch("app.engines.hybrid_reasoner.httpx.AsyncClient.post")
    async def test_hybrid_reasoner_deep_path(self, mock_post):
        # Mock LLM response for a scaling risk
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "decision_type": "scaling",
                        "original_recommendation": "PostgreSQL",
                        "refined_recommendation": "PostgreSQL with Citus sharding",
                        "reasoning": "Need to handle 10M users.",
                        "risk_mitigation": "Horizontal sharding of the user table."
                    })
                }
            }],
            "usage": {"prompt_tokens": 100, "completion_tokens": 100}
        }
        mock_post.return_value = mock_resp
        
        reasoner = HybridReasoner()
        reasoner.api_key = "fake_key"
        
        risk = RiskyDecision(
            decision_type="scaling",
            reason="Too many users",
            impact="high",
            why_needs_deep_thinking="Need sharding strategy"
        )
        
        result = await reasoner.reason(self.spec, self.fast_rec, [risk])
        
        # Verify stack was refined
        self.assertEqual(result.tech_stack["database"], "PostgreSQL with Citus sharding")
        self.assertEqual(len(result.deep_reasoning_applied), 1)
        self.assertEqual(result.deep_reasoning_applied[0].decision_type, "scaling")
        self.assertEqual(result.confidence, 0.9)

if __name__ == "__main__":
    unittest.main()
