import unittest
import asyncio
from app.openenv.interface import OpenEnvInterface

class TestOpenEnvSubmission(unittest.IsolatedAsyncioTestCase):
    """
    Test suite for Weeks 9-10: OpenEnv Integration.
    """

    def setUp(self):
        self.interface = OpenEnvInterface()

    async def test_openenv_reset(self):
        # Reset should load the first case
        state = await self.interface.reset("tech_stack")
        self.assertEqual(state["project_name"], "Ecommerce")

    async def test_openenv_step_tech_stack(self):
        # Action matches ground truth
        action = {
            "api_framework": "FastAPI",
            "database": "PostgreSQL",
            "cache": "Redis",
            "message_queue": "RabbitMQ"
        }
        resp = await self.interface.step("tech_stack", action)
        self.assertEqual(resp.reward, 1.0)
        self.assertTrue(resp.done)

    async def test_openenv_step_anti_pattern(self):
        # Action matches 2 of 3 patterns
        action = {"findings": ["Shared Database", "Missing API Gateway"]}
        resp = await self.interface.step("anti_pattern", action)
        # 2/3 = 0.666...
        self.assertAlmostEqual(resp.reward, 0.666, places=2)

if __name__ == "__main__":
    unittest.main()
