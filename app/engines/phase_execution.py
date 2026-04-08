import asyncio
import structlog
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from app.models.schemas import Phase, Architecture
from app.engines.mcp_dispatcher import MCPDispatcher, DispatchResult

logger = structlog.get_logger("architect_agent.phase_execution")

class DependencyError(Exception):
    pass

class PhaseExecutionResult(BaseModel):
    phase_id: int
    status: str  # "completed" or "failed"
    task_results: List[DispatchResult]
    errors: List[str] = []

class PhaseExecutionFramework:
    """
    Implements workflow automation and phase orchestration derived from autoMate logic.
    Handles dependency validation and parallel/sequential execution of phase instructions.
    """
    
    def __init__(self, dispatcher: MCPDispatcher):
        self.dispatcher = dispatcher
        # Simple simulated in-memory store for phase statuses
        # In a real system, this reads from Supabase memory
        self.phase_status_db: Dict[int, str] = {}
        
    async def _validate_dependencies(self, phase: Phase):
        """Validates if all dependent phases have completed."""
        for dep_num in phase.depends_on:
            status = self.phase_status_db.get(dep_num, "pending")
            if status != "completed":
                raise DependencyError(f"Cannot execute Phase {phase.phase_number}. Dependency Phase {dep_num} is not 'completed', current status is '{status}'.")

    async def execute_phase(
        self,
        phase: Phase,
        architecture: Architecture,
        mcp_agent_url: str
    ) -> PhaseExecutionResult:
        """
        Execute an implementation phase by dispatching to the MCP agent.
        """
        logger.info("phase_execution_start", phase_num=phase.phase_number, services=len(phase.services_to_build))
        
        try:
            # 1. Validate dependencies
            await self._validate_dependencies(phase)
        except DependencyError as e:
            logger.error("phase_execution_dependency_error", error=str(e))
            self.phase_status_db[phase.phase_number] = "blocked"
            return PhaseExecutionResult(
                phase_id=phase.phase_number,
                status="blocked",
                task_results=[],
                errors=[str(e)]
            )
            
        self.phase_status_db[phase.phase_number] = "in_progress"
        
        # 2. In a real generalized framework, you'd split tasks by service.
        # Here we map the entire phase spec as a singular dispatch payload to the main MCP Dispatcher.
        # If we had can_parallelize flag mapping to individual services we'd use asyncio.gather
        
        dispatch_results = []
        try:
            # Dispatch
            res = await self.dispatcher.dispatch(phase=phase, mcp_agent_url=mcp_agent_url, architecture=architecture)
            dispatch_results.append(res)
            
            # 3. Track Status
            overall_status = "completed" if all(r.status == "completed" for r in dispatch_results) else "failed"
            self.phase_status_db[phase.phase_number] = overall_status
            
            logger.info("phase_execution_finish", phase_num=phase.phase_number, status=overall_status)
            
            errors = []
            for r in dispatch_results:
                errors.extend(r.validation_errors)
                
            return PhaseExecutionResult(
                phase_id=phase.phase_number,
                status=overall_status,
                task_results=dispatch_results,
                errors=errors
            )
            
        except Exception as e:
            logger.error("phase_execution_dispatch_error", error=str(e))
            self.phase_status_db[phase.phase_number] = "failed"
            return PhaseExecutionResult(
                phase_id=phase.phase_number,
                status="failed",
                task_results=dispatch_results,
                errors=[str(e)]
            )

    def mark_phase_completed_manual(self, phase_number: int):
        """Utility for test runs."""
        self.phase_status_db[phase_number] = "completed"
