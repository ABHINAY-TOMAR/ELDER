import asyncio
import httpx
import structlog
from datetime import datetime
from pydantic import BaseModel
from typing import Dict, Any, List

from app.models.schemas import Phase, Architecture

logger = structlog.get_logger("architect_agent.mcp_dispatcher")

class DispatchError(Exception):
    pass

class DispatchResult(BaseModel):
    task_id: str
    status: str
    output_repo: str = ""
    validation_errors: List[str] = []

class MCPDispatcher:
    def __init__(self):
        self.headers = {"Content-Type": "application/json"}

    async def create_task(self, phase: Phase, mcp_url: str, architecture: Architecture) -> str:
        task_id = f"{architecture.project_id}-phase-{phase.phase_number}"
        
        payload = {
            "jsonrpc": "2.0",
            "id": task_id,
            "method": "tasks/create",
            "params": {
                "task_id": task_id,
                "title": phase.name,
                "spec": phase.spec_text,
                "deadline": "2026-12-31T00:00:00Z", # arbitrary future
                "requirements": architecture.tech_stack
            }
        }
        
        logger.info("mcp_create_task_request", task_id=task_id, mcp_url=mcp_url)
        async with httpx.AsyncClient() as client:
            res = await client.post(f"{mcp_url}/mcp", json=payload, headers=self.headers, timeout=10.0)
            res.raise_for_status()
            # typically {"jsonrpc": "2.0", "id": "...", "result": {"status": "created"}}
            return task_id

    async def check_status(self, task_id: str, mcp_url: str) -> Dict[str, Any]:
        payload = {
            "jsonrpc": "2.0",
            "id": f"status_{task_id}",
            "method": "tasks/status",
            "params": {"task_id": task_id}
        }
        async with httpx.AsyncClient() as client:
            res = await client.post(f"{mcp_url}/mcp", json=payload, headers=self.headers, timeout=10.0)
            res.raise_for_status()
            data = res.json()
            if "error" in data:
                raise DispatchError(data["error"])
            return data.get("result", {"state": "unknown"})

    async def get_result(self, task_id: str, mcp_url: str) -> Dict[str, Any]:
        payload = {
            "jsonrpc": "2.0",
            "id": f"result_{task_id}",
            "method": "tasks/result",
            "params": {"task_id": task_id}
        }
        async with httpx.AsyncClient() as client:
            res = await client.post(f"{mcp_url}/mcp", json=payload, headers=self.headers, timeout=10.0)
            res.raise_for_status()
            return res.json().get("result", {})

    async def validate_output(self, result: Dict[str, Any], phase: Phase, architecture: Architecture):
        # Stub for validating the output repository.
        class ValidationStub:
            def __init__(self):
                self.errors = []
        return ValidationStub()

    async def poll_until_complete(self, task_id: str, mcp_url: str, timeout_minutes: int = 60) -> Dict[str, Any]:
        logger.info("mcp_polling_started", task_id=task_id)
        start = datetime.now()
        
        while (datetime.now() - start).total_seconds() < timeout_minutes * 60:
            try:
                status = await self.check_status(task_id, mcp_url)
                state = status.get("state")
                
                if state == "completed":
                    logger.info("mcp_task_completed", task_id=task_id)
                    return await self.get_result(task_id, mcp_url)
                elif state == "failed":
                    logger.error("mcp_task_failed", task_id=task_id, error=status.get("error"))
                    raise DispatchError(status.get("error"))
            except Exception as e:
                logger.warning("mcp_polling_error", error=str(e))
                
            await asyncio.sleep(30)
            
        raise TimeoutError(f"Task {task_id} did not complete within timeout.")

    async def dispatch(self, phase: Phase, mcp_agent_url: str, architecture: Architecture) -> DispatchResult:
        logger.info("mcp_dispatch_start", phase=phase.phase_number)
        
        try:
            task_id = await self.create_task(phase, mcp_agent_url, architecture)
            result = await self.poll_until_complete(task_id, mcp_agent_url)
            validation = await self.validate_output(result, phase, architecture)
            
            summary = DispatchResult(
                task_id=task_id,
                status="completed",
                output_repo=result.get("output_repo", ""),
                validation_errors=validation.errors
            )
            return summary
            
        except Exception as e:
            logger.error("mcp_dispatch_failed", error=str(e), phase=phase.phase_number)
            return DispatchResult(
                task_id=f"{architecture.project_id}-phase-{phase.phase_number}",
                status="failed",
                validation_errors=[str(e)]
            )
