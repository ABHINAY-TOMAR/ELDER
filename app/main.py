"""
ELDER Application - Main Entry Point

FastAPI application providing OpenEnv grading environment endpoints:
- /reset: Initialize a task session with random test case
- /step: Submit agent action for grading and get response
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Literal
from enum import Enum
import random
import uuid

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from app.openenv.graders import grade_task_1, grade_task_2, grade_task_3
from app.openenv.test_cases import TEST_CASES, get_random_test_case


# =============================================================================
# DATA MODELS
# =============================================================================

class TaskType(str, Enum):
    TASK_1 = "task_1"
    TASK_2 = "task_2"
    TASK_3 = "task_3"


class ActionType(str, Enum):
    # Task 1: Stack Recommendation
    RECOMMEND_STACK = "recommend_stack"
    
    # Task 2: Anti-Pattern Detection
    DETECT_ANTI_PATTERNS = "detect_anti_patterns"
    ANALYZE_ARCHITECTURE = "analyze_architecture"
    
    # Task 3: Full Design
    DESIGN_SYSTEM = "design_system"
    CREATE_SPECS = "create_specs"


@dataclass
class SessionState:
    """Tracks state for an active evaluation session."""
    session_id: str
    task_id: str
    test_case: Dict[str, Any]
    step_count: int = 0
    total_score: float = 0.0
    history: List[Dict[str, Any]] = field(default_factory=list)


# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================

class ResetRequest(BaseModel):
    """Request body for /reset endpoint."""
    task_id: str = Field(
        ..., 
        description="Task ID: 'task_1', 'task_2', or 'task_3'"
    )
    seed: Optional[int] = Field(
        None, 
        description="Optional random seed for reproducibility"
    )


class StepRequest(BaseModel):
    """Request body for /step endpoint."""
    session_id: str = Field(
        ..., 
        description="Session ID from /reset response"
    )
    action_type: str = Field(
        ..., 
        description="Type of action: recommend_stack, detect_anti_patterns, design_system"
    )
    agent_response: Dict[str, Any] = Field(
        ..., 
        description="Agent's response/action to be graded"
    )


class Observation(BaseModel):
    """Observation returned to the agent after each step."""
    session_id: str
    step: int
    task_id: str
    action_type: str
    score: float
    feedback: str
    is_terminal: bool
    info: Dict[str, Any] = Field(default_factory=dict)


class ResetResponse(BaseModel):
    """Response from /reset endpoint."""
    session_id: str
    task_id: str
    task_description: str
    observation: Observation


class StepResponse(BaseModel):
    """Response from /step endpoint."""
    observation: Observation


# =============================================================================
# SESSION STORAGE (in-memory for simplicity)
# =============================================================================

sessions: Dict[str, SessionState] = {}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def create_initial_observation(
    session_id: str,
    task_id: str,
    test_case: Dict[str, Any],
) -> Observation:
    """Create initial observation for a fresh session."""
    return Observation(
        session_id=session_id,
        step=0,
        task_id=task_id,
        action_type="init",
        score=0.0,
        feedback="Session initialized. Ready for agent action.",
        is_terminal=False,
        info={
            "requirements": test_case.get("requirements", {}),
            "system_description": test_case.get("system_description", ""),
            "service_map": test_case.get("service_map", {}),
            "ground_truth_id": test_case.get("id", ""),
        },
    )


def create_terminal_observation(
    session: SessionState,
    action_type: str,
    score: float,
    feedback: str,
    info: Optional[Dict[str, Any]] = None,
) -> Observation:
    """Create terminal observation after grading."""
    return Observation(
        session_id=session.session_id,
        step=session.step_count,
        task_id=session.task_id,
        action_type=action_type,
        score=score,
        feedback=feedback,
        is_terminal=True,
        info=info or {},
    )


def create_step_observation(
    session: SessionState,
    action_type: str,
    score: float,
    feedback: str,
    info: Optional[Dict[str, Any]] = None,
) -> Observation:
    """Create observation for intermediate step."""
    return Observation(
        session_id=session.session_id,
        step=session.step_count,
        task_id=session.task_id,
        action_type=action_type,
        score=score,
        feedback=feedback,
        is_terminal=False,
        info=info or {},
    )


def get_ground_truth(test_case: Dict[str, Any], task_id: str) -> Dict[str, Any]:
    """Extract ground truth from test case based on task type."""
    if task_id == "task_1":
        return test_case.get("ground_truth", {})
    elif task_id == "task_2":
        return test_case.get("ground_truth_patterns", {})
    elif task_id == "task_3":
        return test_case.get("ground_truth", {})
    return {}


# =============================================================================
# GRADE ROUTING
# =============================================================================

def route_and_grade(
    action_type: str,
    agent_response: Dict[str, Any],
    ground_truth: Dict[str, Any],
    test_case: Dict[str, Any],
) -> tuple[float, str, bool, Dict[str, Any]]:
    """
    Route agent action to appropriate grader and return results.
    
    Returns:
        tuple: (score, feedback, is_terminal, info)
    """
    info = {}
    
    # Task 1: Stack Recommendation
    if action_type == "recommend_stack":
        agent_recommendation = agent_response.get("recommendation", {})
        
        # Handle both direct recommendations and nested structure
        if not agent_recommendation:
            agent_recommendation = {
                "api_framework": agent_response.get("api_framework", ""),
                "database": agent_response.get("database", ""),
                "cache_layer": agent_response.get("cache_layer", ""),
                "message_queue": agent_response.get("message_queue", ""),
                "monitoring": agent_response.get("monitoring", ""),
            }
        
        score = grade_task_1(agent_recommendation, ground_truth)
        
        # Generate feedback
        components = ["api_framework", "database", "cache_layer", "message_queue", "monitoring"]
        matched = sum(
            1 for c in components
            if agent_recommendation.get(c, "").lower().strip() == ground_truth.get(c, "").lower().strip()
        )
        
        feedback = f"Stack recommendation scored {score:.2f}. Matched {matched}/5 components exactly."
        
        return score, feedback, True, {
            "score_breakdown": {
                c: {
                    "agent": agent_recommendation.get(c, ""),
                    "ground_truth": ground_truth.get(c, ""),
                    "match": agent_recommendation.get(c, "").lower().strip() == ground_truth.get(c, "").lower().strip()
                }
                for c in components
            }
        }
    
    # Task 2: Anti-Pattern Detection
    elif action_type in ("detect_anti_patterns", "analyze_architecture"):
        agent_findings = agent_response.get("findings", [])
        
        # Handle both findings array and string
        if isinstance(agent_findings, str):
            agent_findings = [agent_findings]
        
        # Also check for findings in a different format
        if not agent_findings:
            agent_findings = [
                agent_response.get("description", ""),
                agent_response.get("anti_patterns", ""),
            ]
        
        score = grade_task_2(agent_findings, ground_truth)
        
        # Generate feedback
        found_patterns = []
        for pattern_name in ground_truth.keys():
            from app.openenv.graders import PATTERN_KEYWORDS
            keywords = PATTERN_KEYWORDS.get(pattern_name, [])
            findings_text = " ".join(agent_findings).lower()
            if any(kw.lower() in findings_text for kw in keywords):
                found_patterns.append(pattern_name)
        
        feedback = f"Anti-pattern detection scored {score:.2f}. Found {len(found_patterns)}/{len(ground_truth)} patterns."
        
        return score, feedback, True, {
            "found_patterns": found_patterns,
            "total_patterns": list(ground_truth.keys()),
        }
    
    # Task 3: Full Design Integration
    elif action_type in ("design_system", "create_specs"):
        architecture = agent_response.get("architecture", agent_response)
        
        # Extract services if nested
        if "services" not in architecture:
            architecture["services"] = agent_response.get("services", [])
        
        score = grade_task_3(architecture, ground_truth.get("requirements", {}))
        
        # Generate feedback
        service_count = len(architecture.get("services", []))
        failure_count = len(architecture.get("failure_modes", {}))
        
        feedback = f"Architecture design scored {score:.2f}. {service_count} services defined, {failure_count} failure modes identified."
        
        return score, feedback, True, {
            "service_count": service_count,
            "failure_mode_count": failure_count,
        }
    
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown action type: {action_type}"
        )


# =============================================================================
# FASTAPI APPLICATION
# =============================================================================

app = FastAPI(
    title="ELDER OpenEnv Grading API",
    description="Environment for evaluating architecture agent performance",
    version="0.1.0",
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "ELDER OpenEnv",
        "version": "0.1.0",
    }


@app.post("/reset", response_model=ResetResponse)
async def reset(request: ResetRequest):
    """
    Initialize a new evaluation session.
    
    Selects a random test case for the given task and returns
    the initial observation.
    """
    # Validate task_id
    if request.task_id not in TEST_CASES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid task_id. Must be one of: {list(TEST_CASES.keys())}"
        )
    
    # Apply seed if provided
    if request.seed is not None:
        random.seed(request.seed)
    
    # Select random test case
    test_case = get_random_test_case(request.task_id)
    if not test_case:
        raise HTTPException(
            status_code=500,
            detail=f"No test cases found for task: {request.task_id}"
        )
    
    # Create session
    session_id = str(uuid.uuid4())
    session = SessionState(
        session_id=session_id,
        task_id=request.task_id,
        test_case=test_case,
    )
    sessions[session_id] = session
    
    # Create observation
    observation = create_initial_observation(
        session_id=session_id,
        task_id=request.task_id,
        test_case=test_case,
    )
    
    return ResetResponse(
        session_id=session_id,
        task_id=request.task_id,
        task_description=test_case.get("description", ""),
        observation=observation,
    )


@app.post("/step", response_model=StepResponse)
async def step(request: StepRequest):
    """
    Submit agent action for grading.
    
    Routes to appropriate grader based on action_type and returns
    score with feedback.
    """
    # Get session
    session = sessions.get(request.session_id)
    if not session:
        raise HTTPException(
            status_code=404,
            detail=f"Session not found: {request.session_id}"
        )
    
    # Increment step counter
    session.step_count += 1
    
    # Get ground truth
    ground_truth = get_ground_truth(session.test_case, session.task_id)
    
    # Route and grade
    try:
        score, feedback, is_terminal, info = route_and_grade(
            action_type=request.action_type,
            agent_response=request.agent_response,
            ground_truth=ground_truth,
            test_case=session.test_case,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Grading error: {str(e)}"
        )
    
    # Update session
    session.total_score += score
    session.history.append({
        "step": session.step_count,
        "action_type": request.action_type,
        "score": score,
        "feedback": feedback,
    })
    
    # Create observation
    if is_terminal:
        observation = create_terminal_observation(
            session=session,
            action_type=request.action_type,
            score=score,
            feedback=feedback,
            info=info,
        )
    else:
        observation = create_step_observation(
            session=session,
            action_type=request.action_type,
            score=score,
            feedback=feedback,
            info=info,
        )
    
    return StepResponse(observation=observation)


@app.get("/session/{session_id}")
async def get_session(session_id: str):
    """Get current state of a session."""
    session = sessions.get(session_id)
    if not session:
        raise HTTPException(
            status_code=404,
            detail=f"Session not found: {session_id}"
        )
    
    return {
        "session_id": session.session_id,
        "task_id": session.task_id,
        "step_count": session.step_count,
        "total_score": session.total_score,
        "history": session.history,
        "test_case_id": session.test_case.get("id", ""),
    }


@app.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """Delete a session."""
    if session_id not in sessions:
        raise HTTPException(
            status_code=404,
            detail=f"Session not found: {session_id}"
        )
    
    del sessions[session_id]
    return {"status": "deleted", "session_id": session_id}


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
