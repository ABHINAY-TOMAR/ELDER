import unittest
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock
from app.models.requirement_spec import RequirementSpec
from app.engines.pattern_retriever import PatternRetriever
from app.engines.risky_decision_detector import RiskyDecisionDetector
from app.engines.fast_pattern_matcher import StackRecommendation

class TestWeek3(unittest.IsolatedAsyncioTestCase):
    """
    Test suite for Week 3 deliverables: Pattern Retrieval and Risk Detection.
    """

    # --- Pattern Retriever Tests ---

    @patch("app.core.memory.ArchitectMemory")
    async def test_pattern_retriever_mock(self, mock_memory_class):
        # Mock memory instance and its search method
        mock_memory = mock_memory_class.return_value
        mock_memory.search = AsyncMock(return_value=[
            {
                "source": "proj_abc",
                "similarity": 0.85,
                "metadata": {
                    "tech_stack": {"db": "Postgres"},
                    "services": ["s1", "s2"],
                    "rationale": "High scale design."
                }
            }
        ])
        
        retriever = PatternRetriever(mock_memory)
        spec = RequirementSpec(project_name="TestProj", domain="microservices")
        
        results = await retriever.retrieve_similar(spec, limit=1)
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].project_id, "proj_abc")
        self.assertEqual(results[0].similarity_score, 0.85)
        self.assertIn("s1", results[0].services)

    # --- Risky Decision Detector Tests ---

    def test_risky_decision_detector(self):
        detector = RiskyDecisionDetector()
        
        # 1. Test Scale Risk
        spec_scale = RequirementSpec(project_name="Huge", expected_users=2_000_000)
        fast_rec = StackRecommendation(
            tech_stack={"db": "Postgres"}, 
            deployment_target="Vercel", 
            rationale="Fast", 
            confidence=0.9
        )
        risks = detector.detect(spec_scale, fast_rec)
        self.assertTrue(any(r.decision_type == "scaling" for r in risks))

        # 2. Test Security Risk
        spec_security = RequirementSpec(project_name="Bank", data_sensitivity="pii", constraints=[])
        risks = detector.detect(spec_security, fast_rec)
        self.assertTrue(any(r.decision_type == "security" for r in risks))

        # 3. Test Conflict Risk
        spec_conflict = RequirementSpec(
            project_name="Conflicted", 
            constraints=["Must use MongoDB"]
        )
        fast_rec_sql = StackRecommendation(
            tech_stack={"database": "PostgreSQL"}, 
            deployment_target="Cloud", 
            rationale="Fast", 
            confidence=0.9
        )
        risks = detector.detect(spec_conflict, fast_rec_sql)
        self.assertTrue(any(r.decision_type == "database" for r in risks))

        # 4. Test Complexity Risk
        spec_complex = RequirementSpec(
            project_name="Solo", 
            team_size=1, 
            extracted_features=["f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9"]
        )
        risks = detector.detect(spec_complex, fast_rec)
        self.assertTrue(any(r.decision_type == "complexity" for r in risks))

if __name__ == "__main__":
    # We need to define AsyncMock if not available (Python < 3.8)
    # But we are on 3.11+ so it's fine.
    from unittest.mock import AsyncMock
    unittest.main()
