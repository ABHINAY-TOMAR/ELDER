from typing import Any, Dict, List, Tuple

from app.models.architecture import Architecture
from app.models.schemas import Action, Observation, OpenEnvState, OpenEnvTask, Reward
from app.openenv.graders import EPSILON, OpenEnvGraders
from app.openenv.test_cases import TEST_CASES


class OpenEnvInterface:
    """Deterministic OpenEnv runtime with strict 3-task support."""

    TASKS: List[OpenEnvTask] = [
        OpenEnvTask(
            id="task_stack_recommendation",
            name="Tech Stack Recommendation",
            difficulty="Easy",
            description="Recommend a fit-for-purpose stack from structured requirements.",
        ),
        OpenEnvTask(
            id="task_anti_pattern_detection",
            name="Architectural Anti-Pattern Detection",
            difficulty="Medium",
            description="Identify architectural anti-patterns with partial-credit coverage.",
        ),
        OpenEnvTask(
            id="task_full_design_integration",
            name="Full Architecture Design",
            difficulty="Hard",
            description="Produce a full architecture and satisfy required service, integration, and failure constraints.",
        ),
    ]

    def __init__(self) -> None:
        self.graders = OpenEnvGraders()
        self._task_map: Dict[str, OpenEnvTask] = {task.id: task for task in self.TASKS}
        self._active_task_id: str | None = None
        self._attempts: Dict[str, int] = {task.id: 0 for task in self.TASKS}
        self._best_scores: Dict[str, float] = {task.id: EPSILON for task in self.TASKS}

    def get_available_tasks(self) -> List[OpenEnvTask]:
        # Compliance guard: the environment must expose exactly 3 tasks.
        return list(self.TASKS)

    def state(self) -> OpenEnvState:
        return OpenEnvState(
            tasks=self.get_available_tasks(),
            active_task_id=self._active_task_id,
            attempts_by_task=dict(self._attempts),
            best_score_by_task=dict(self._best_scores),
        )

    async def reset(self, task_id: str) -> Observation:
        if task_id not in self._task_map:
            raise ValueError(f"Unknown task_id: {task_id}")

        self._active_task_id = task_id
        self._attempts[task_id] = 0
        self._best_scores[task_id] = EPSILON

        return Observation(
            task_id=task_id,
            message="Task reset complete. Submit an action payload to receive incremental reward.",
            attempt=0,
            best_score=self._best_scores[task_id],
            done=False,
        )

    async def step(self, action: Action) -> Reward:
        task_id = action.task_id
        if task_id not in self._task_map:
            raise ValueError(f"Unknown task_id: {task_id}")

        if self._active_task_id != task_id:
            await self.reset(task_id)

        score, evidence = self._score_action(task_id, action.payload)

        self._attempts[task_id] += 1
        previous_best = self._best_scores[task_id]
        delta = max(0.0, score - previous_best)
        self._best_scores[task_id] = max(previous_best, score)

        shaped = min(1.0 - EPSILON, max(EPSILON, (0.85 * delta) + (0.15 * score)))
        done = self._best_scores[task_id] >= 0.95

        observation = Observation(
            task_id=task_id,
            message=f"Scored {score:.4f}. {evidence}",
            attempt=self._attempts[task_id],
            best_score=self._best_scores[task_id],
            done=done,
        )

        return Reward(
            task_id=task_id,
            score=score,
            delta=delta,
            reward=shaped,
            done=done,
            observation=observation,
        )

    def _score_action(self, task_id: str, payload: Dict[str, Any]) -> Tuple[float, str]:
        test_case = TEST_CASES[task_id][0]

        if task_id == "task_stack_recommendation":
            score = self.graders.grade_tech_stack(payload, test_case.get("ground_truth", {}))
            return score, "Compared stack recommendation against weighted ground truth fields."

        if task_id == "task_anti_pattern_detection":
            findings = payload.get("findings") or payload.get("patterns") or []
            if isinstance(findings, str):
                findings = [findings]
            score = self.graders.grade_anti_patterns(findings, test_case.get("ground_truth_patterns", {}))
            return score, "Matched findings against task-specific keyword bundles."

        try:
            architecture = Architecture(**payload)
            score = self.graders.grade_full_design(architecture, test_case.get("ground_truth_requirements", {}))
            return score, "Evaluated service, integration, and failure-mode coverage."
        except Exception:
            return EPSILON, "Payload did not match architecture schema; minimal effort credit applied."
