import unittest
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock
from app.models.requirement_spec import RequirementSpec
from app.models.architecture import Architecture, Service, ADR, FailureMode
from app.engines.architecture_generator import ArchitectureGenerator
from app.engines.failure_mode_mapper import FailureModeMapper
from app.engines.hybrid_reasoner import FinalArchitectureRecommendation

class TestWeek5(unittest.IsolatedAsyncioTestCase):
    """
    Test suite for Week 5 deliverables: Architecture Generation & Failures.
    """

    def setUp(self):
        self.spec = RequirementSpec(project_name="TestApp", domain="microservices", team_size=2)
        self.recommendation = FinalArchitectureRecommendation(
            tech_stack={"api_framework": "FastAPI", "database": "PostgreSQL"},
            deployment_target="Render",
            rationale="Initial design.",
            risks_identified=[],
            confidence=0.9
        )

    # --- Architecture Generator Tests ---

    @patch("app.engines.architecture_generator.httpx.AsyncClient.post")
    async def test_architecture_generator_mock(self, mock_post):
        # Mock LLM decomposition response
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = {
            "choices": [{
                "message": {
                    "content": """{
                        "services": [
                            {"id": "auth", "name": "Auth", "description": "X", "stack": "FastAPI"},
                            {"id": "order", "name": "Order", "description": "Y", "stack": "FastAPI", "dependencies": ["auth"]}
                        ]
                    }"""
                }
            }]
        }
        mock_post.return_value = mock_resp
        
        generator = ArchitectureGenerator()
        generator.api_key = "fake_key"
        
        arch = await generator.generate("proj_123", self.spec, self.recommendation)
        
        self.assertEqual(len(arch.services), 2)
        self.assertEqual(arch.services[0].id, "auth")
        self.assertEqual(arch.services[1].dependencies[0], "auth")
        self.assertGreater(len(arch.adrs), 0)
        self.assertGreaterEqual(arch.estimated_effort_weeks, 1)

    # --- Failure Mode Mapper Tests ---

    def test_failure_mode_mapper(self):
        mapper = FailureModeMapper()
        
        # Test Microservices Failures
        arch_ms = Architecture(
            project_id="ms_1", project_name="MS", domain="microservices",
            tech_stack={}, services=[Service(id="s1", name="S1", description="D", stack="S")],
            rationale="R"
        )
        failures = mapper.map_failures(arch_ms)
        self.assertEqual(len(failures), 3)
        self.assertEqual(failures[0].service_id, "s1")
        self.assertIn("Database", failures[1].mode or "") 
        
        # Test AI-Native Failures
        arch_ai = Architecture(
            project_id="ai_1", project_name="AI", domain="ai_native",
            tech_stack={}, services=[Service(id="agent", name="Agent", description="D", stack="S")],
            rationale="R"
        )
        failures = mapper.map_failures(arch_ai)
        self.assertEqual(len(failures), 3)
        self.assertIn("Model Hallucination", [f.mode for f in failures])

if __name__ == "__main__":
    unittest.main()
