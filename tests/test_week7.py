import unittest
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock
from app.models.architecture import Phase, Architecture, Service
from app.engines.mcp_dispatcher import MCPDispatcher, DispatchResult, TaskStatus

class TestWeek7(unittest.IsolatedAsyncioTestCase):
    """
    Test suite for Week 7 deliverables: MCP Dispatcher.
    """

    def setUp(self):
        self.phase = Phase(
            phase_number=1, name="Foundation", service_ids=["auth"], 
            description="D", spec_markdown="# Spec"
        )
        self.arch = Architecture(
            project_id="p1", project_name="T", domain="ms", tech_stack={}, 
            services=[Service(id="auth", name="A", description="D", stack="S")],
            rationale="R"
        )

    @patch("app.engines.mcp_dispatcher.httpx.AsyncClient.post")
    async def test_mcp_dispatch_success(self, mock_post):
        # Mock successful dispatch
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp
        
        dispatcher = MCPDispatcher()
        result = await dispatcher.dispatch(self.phase, "http://agent", self.arch)
        
        self.assertEqual(result.status, "dispatched")
        self.assertTrue(result.task_id.startswith("task_"))

    @patch("app.engines.mcp_dispatcher.httpx.AsyncClient.post")
    async def test_mcp_polling_logic(self, mock_post):
        # 1. Mock status poll (completed)
        mock_status_resp = MagicMock()
        mock_status_resp.json.return_value = {
            "jsonrpc": "2.0",
            "result": {"state": "completed", "progress": 100}
        }
        
        # 2. Mock result fetch
        mock_result_resp = MagicMock()
        mock_result_resp.json.return_value = {
            "jsonrpc": "2.0",
            "result": {"output_repo": "https://github.com/test/repo"}
        }
        
        # Configure mock_post to return different responses based on call
        mock_post.side_effect = [mock_status_resp, mock_result_resp]
        
        dispatcher = MCPDispatcher()
        # We manually call poll logic steps to avoid long waits/sleeps in unit test
        status = await dispatcher.check_status("task_1", "http://agent")
        self.assertEqual(status.state, "completed")
        
        result = await dispatcher.get_result("task_1", "http://agent")
        self.assertEqual(result.status, "completed")
        self.assertEqual(result.output_repo_url, "https://github.com/test/repo")

if __name__ == "__main__":
    unittest.main()
