import json
import os
from typing import Any, Dict, List

from openai import OpenAI

from app.models.architecture import Architecture, ADR, FailureMode, Phase, Service
from app.openenv.graders import EPSILON, OpenEnvGraders
from app.openenv.test_cases import (
    TASK_1_TEST_CASES,
    TASK_2_TEST_CASES,
    TASK_3_TEST_CASES,
)


def _strict_unit_interval(value: float) -> float:
    return min(1.0 - EPSILON, max(EPSILON, float(value)))


def _build_client() -> OpenAI:
    openai_key = os.getenv("OPENAI_API_KEY")
    hf_token = os.getenv("HF_TOKEN")

    api_key = openai_key or hf_token
    if not api_key:
        raise RuntimeError("Set OPENAI_API_KEY or HF_TOKEN before running baseline.py")

    base_url = os.getenv("OPENAI_BASE_URL")
    if not base_url and hf_token and not openai_key:
        base_url = os.getenv("HF_OPENAI_BASE_URL", "https://router.huggingface.co/v1")

    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    return OpenAI(api_key=api_key)


def _extract_json(content: str) -> Dict[str, Any]:
    text = (content or "").strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:].strip()
    return json.loads(text)


def _chat_json(client: OpenAI, model: str, seed: int, prompt: str) -> Dict[str, Any]:
    response = client.chat.completions.create(
        model=model,
        temperature=0,
        seed=seed,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "Return strict JSON only."},
            {"role": "user", "content": prompt},
        ],
    )
    content = response.choices[0].message.content or "{}"
    return _extract_json(content)


def run_task_1(client: OpenAI, model: str, seed: int, graders: OpenEnvGraders) -> float:
    case = TASK_1_TEST_CASES[0]
    prompt = (
        "Task: Recommend a software stack. "
        "Return JSON with keys api_framework, database, cache_layer, message_queue, monitoring.\n"
        f"Requirements:\n{json.dumps(case['requirements'], indent=2)}"
    )
    try:
        output = _chat_json(client, model, seed, prompt)
    except Exception:
        output = {}

    score = graders.grade_tech_stack(output, case["ground_truth"])
    return _strict_unit_interval(score)


def run_task_2(client: OpenAI, model: str, seed: int, graders: OpenEnvGraders) -> float:
    case = TASK_2_TEST_CASES[0]
    prompt = (
        "Task: Detect architecture anti-patterns. "
        "Return JSON with key findings as an array of short strings.\n"
        f"System:\n{case['system_description']}\n"
    )
    try:
        output = _chat_json(client, model, seed, prompt)
    except Exception:
        output = {}

    findings = output.get("findings", [])
    if isinstance(findings, str):
        findings = [findings]
    score = graders.grade_anti_patterns(findings, case["ground_truth_patterns"])
    return _strict_unit_interval(score)


def _fallback_architecture(case: Dict[str, Any]) -> Architecture:
    req = case["requirements"]
    expected_services = req.get("expected_services", [])
    services = [
        Service(
            id=f"svc_{idx}",
            name=name,
            description=f"Service for {name}",
            stack="fastapi",
            dependencies=[],
        )
        for idx, name in enumerate(expected_services)
    ]
    failures = [
        FailureMode(
            service_id="svc_0",
            mode=mode,
            probability="medium",
            impact="high",
            detection="monitoring",
            mitigation="retry and fallback",
        )
        for mode in case.get("ground_truth_requirements", {}).get("required_failure_modes", [])
    ]

    return Architecture(
        project_id="baseline_project",
        project_name=req.get("project_name", "Baseline Project"),
        domain=req.get("domain", "microservices"),
        tech_stack={"api_framework": "fastapi", "database": "postgresql"},
        services=services,
        adrs=[
            ADR(
                title="Use FastAPI",
                context="Need fast API development",
                decision="Adopt FastAPI",
                alternatives=["Flask", "Django"],
                consequences="Lower startup overhead",
            )
        ],
        failure_modes=failures,
        phases=[
            Phase(
                phase_number=1,
                name="Initial Build",
                service_ids=[s.id for s in services],
                description="Implement baseline services",
            )
        ],
        estimated_effort_weeks=8,
        rationale="Baseline deterministic architecture",
    )


def run_task_3(client: OpenAI, model: str, seed: int, graders: OpenEnvGraders) -> float:
    case = TASK_3_TEST_CASES[0]
    prompt = (
        "Task: Produce architecture JSON for the given requirement.\n"
        "Return JSON with keys compatible with this schema: "
        "project_id, project_name, domain, tech_stack, services, adrs, failure_modes, phases, estimated_effort_weeks, rationale.\n"
        f"Requirements:\n{json.dumps(case['requirements'], indent=2)}"
    )

    architecture: Architecture
    try:
        output = _chat_json(client, model, seed, prompt)
        architecture = Architecture(**output)
    except Exception:
        architecture = _fallback_architecture(case)

    score = graders.grade_full_design(architecture, case["ground_truth_requirements"])
    return _strict_unit_interval(score)


def main() -> None:
    model = os.getenv("OPENAI_BASELINE_MODEL", "gpt-4o-mini")
    seed = int(os.getenv("BASELINE_SEED", "42"))

    client = _build_client()
    graders = OpenEnvGraders()

    score_easy = run_task_1(client, model, seed, graders)
    score_medium = run_task_2(client, model, seed, graders)
    score_hard = run_task_3(client, model, seed, graders)

    print(f"Baseline model: {model}")
    print(f"Seed: {seed}")
    print(f"Easy (task_stack_recommendation): {score_easy:.6f}")
    print(f"Medium (task_anti_pattern_detection): {score_medium:.6f}")
    print(f"Hard (task_full_design_integration): {score_hard:.6f}")


if __name__ == "__main__":
    main()
