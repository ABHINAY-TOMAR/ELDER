import logging
import asyncio
import uuid
import httpx
from datetime import datetime
from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field
from app.models.architecture import Phase, Architecture

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DispatchResult(BaseModel):
    task_id: str
    status: str
    output_repo_url: Optional[str] = None
    error: Optional[str] = None

class TaskStatus(BaseModel):
    task_id: str
    state: Literal["pending", "dispatched", "in_progress", "completed", "failed"]
    progress: int = 0 # 0-100
    error: Optional[str] = None

class MCPDispatcher:
    """
    Communicates with developer agents using the Model Context Protocol (MCP).
    Dispatches implementation tasks and polls for completion.
    """

    def __init__(self, supabase_client: Any = None):
        self.supabase = supabase_client

    async def dispatch(
        self, 
        phase: Phase, 
        mcp_agent_url: str, 
        arch: Architecture
    ) -> DispatchResult:
        """
        Send a phase specification to an agent and track the assignment.
        """
        task_id = f"task_{uuid.uuid4().hex[:8]}"
        logger.info(f"Dispatching phase {phase.phase_number} to {mcp_agent_url} (ID: {task_id})")

        # 1. Store assignment in DB
        if self.supabase:
            try:
                self.supabase.table("task_assignments").insert({
                    "task_id": task_id,
                    "project_id": arch.project_id,
                    "phase_number": phase.phase_number,
                    "status": "dispatched",
                    "agent_url": mcp_agent_url,
                    "created_at": datetime.now().isoformat()
                }).execute()
            except Exception as e:
                logger.error(f"Failed to record assignment: {e}")

        # 2. Call MCP Agent (JSON-RPC 2.0)
        async with httpx.AsyncClient() as client:
            try:
                payload = {
                    "jsonrpc": "2.0",
                    "id": task_id,
                    "method": "tasks/create",
                    "params": {
                        "task_id": task_id,
                        "title": f"Build {arch.project_name} - Phase {phase.phase_number}",
                        "spec": phase.spec_markdown,
                        "requirements": {
                            "domain": arch.domain,
                            "tech_stack": arch.tech_stack
                        }
                    }
                }
                
                response = await client.post(f"{mcp_agent_url}/mcp", json=payload, timeout=10.0)
                response.raise_for_status()
                
                return DispatchResult(task_id=task_id, status="dispatched")
                
            except Exception as e:
                logger.error(f"MCP Dispatch failed: {e}")
                return DispatchResult(task_id=task_id, status="failed", error=str(e))

    async def poll_until_complete(
        self, 
        task_id: str, 
        mcp_agent_url: str, 
        timeout_minutes: int = 60
    ) -> DispatchResult:
        """
        Wait for an agent to finish the task.
        """
        start_time = datetime.now()
        
        while (datetime.now() - start_time).total_seconds() < timeout_minutes * 60:
            status = await self.check_status(task_id, mcp_agent_url)
            
            if status.state == "completed":
                # Get result
                result = await self.get_result(task_id, mcp_agent_url)
                return result
            elif status.state == "failed":
                return DispatchResult(task_id=task_id, status="failed", error=status.error)
            
            # Wait 30s between polls
            await asyncio.sleep(30)
            
        return DispatchResult(task_id=task_id, status="failed", error="Timeout")

    async def check_status(self, task_id: str, mcp_agent_url: str) -> TaskStatus:
        """Query agent for current task state."""
        async with httpx.AsyncClient() as client:
            try:
                payload = {
                    "jsonrpc": "2.0",
                    "id": f"poll_{task_id}",
                    "method": "tasks/status",
                    "params": {"task_id": task_id}
                }
                response = await client.post(f"{mcp_agent_url}/mcp", json=payload)
                data = response.json()
                result = data.get("result", {})
                return TaskStatus(
                    task_id=task_id,
                    state=result.get("state", "failed"),
                    progress=result.get("progress", 0)
                )
            except Exception as e:
                return TaskStatus(task_id=task_id, state="failed", error=str(e))

    async def get_result(self, task_id: str, mcp_agent_url: str) -> DispatchResult:
        """Retrieve final output repo from agent."""
        async with httpx.AsyncClient() as client:
            try:
                payload = {
                    "jsonrpc": "2.0",
                    "id": f"res_{task_id}",
                    "method": "tasks/result",
                    "params": {"task_id": task_id}
                }
                response = await client.post(f"{mcp_agent_url}/mcp", json=payload)
                data = response.json()
                result = data.get("result", {})
                
                output_url = result.get("output_repo")
                
                # Update DB
                if self.supabase:
                    self.supabase.table("task_assignments").update({
                        "status": "completed",
                        "output_repo_url": output_url,
                        "completed_at": datetime.now().isoformat()
                    }).eq("task_id", task_id).execute()
                
                return DispatchResult(task_id=task_id, status="completed", output_repo_url=output_url)
            except Exception as e:
                return DispatchResult(task_id=task_id, status="failed", error=str(e))
