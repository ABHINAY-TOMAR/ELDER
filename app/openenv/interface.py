import logging
import json
import os
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
from app.openenv.graders import OpenEnvGraders

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenEnvTask(BaseModel):
    id: str
    name: str
    description: str
    initial_state: Dict[str, Any]

class ResetRequest(BaseModel):
    task_id: str

class StepRequest(BaseModel):
    task_id: str
    instance_id: str
    action: Dict[str, Any]

class StepResponse(BaseModel):
    observation: str
    reward: float
    done: bool
    info: Dict[str, Any]

class OpenEnvInterface:
    """
    Standard interface for OpenEnv task orchestration.
    """

    def __init__(self):
        self.graders = OpenEnvGraders()
        self.test_cases_dir = "data/openenv_test_cases"

    def get_available_tasks(self) -> List[Dict[str, str]]:
        return [
            {"id": "tech_stack", "name": "Tech Stack Recommendation"},
            {"id": "anti_pattern", "name": "Anti-Pattern Detection"},
            {"id": "full_design", "name": "Full Architecture Design"}
        ]

    async def reset(self, task_id: str) -> Dict[str, Any]:
        """Initialize a task instance."""
        # Load ground truth from file
        case_path = os.path.join(self.test_cases_dir, f"{task_id}_cases.json")
        if not os.path.exists(case_path):
            logger.error(f"Test cases for {task_id} not found.")
            return {"error": "Task not found"}
            
        with open(case_path, "r") as f:
            cases = json.load(f)
            
        # Return the first case as initial state
        return cases[0]["input"]

    async def step(self, task_id: str, action: Dict[str, Any]) -> StepResponse:
        """Execute an action and return reward."""
        # Load ground truth
        case_path = os.path.join(self.test_cases_dir, f"{task_id}_cases.json")
        with open(case_path, "r") as f:
            cases = json.load(f)
            truth = cases[0]["output"]

        reward = 0.0
        if task_id == "tech_stack":
            reward = self.graders.grade_tech_stack(action, truth)
        elif task_id == "anti_pattern":
            reward = self.graders.grade_anti_patterns(action.get("findings", []), truth)
        elif task_id == "full_design":
            # For simplicity in the mockup, we assume action is an Architecture-like dict
            from app.models.architecture import Architecture
            try:
                arch = Architecture(**action)
                reward = self.graders.grade_full_design(arch, truth)
            except:
                reward = 0.1 # Minimal reward for effort but failed schema

        return StepResponse(
            observation="Action processed and graded.",
            reward=reward,
            done=True,
            info={"score_breakdown": {"raw_reward": reward}}
        )
