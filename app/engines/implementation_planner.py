import structlog
import json
from typing import List, Dict, Set, Optional
from collections import defaultdict, deque
from app.models.schemas import Architecture, Phase, Service
from app.engines.llm_client import call_llm

logger = structlog.get_logger("architect_agent.implementation_planner")

CRITICAL_SERVICES = {"auth", "gateway", "api-gateway", "api_gateway"}
AUTH_SERVICES = {"auth", "authentication", "user-auth", "auth-service"}

PHASE_DEFAULTS = {
    "auth": {"name": "Authentication & Authorization", "duration": 3, "priority": "critical"},
    "gateway": {"name": "API Gateway Setup", "duration": 2, "priority": "critical"},
    "core": {"name": "Core Services", "duration": 4, "priority": "high"},
    "integration": {"name": "Service Integration", "duration": 3, "priority": "high"},
    "data": {"name": "Data Layer", "duration": 2, "priority": "medium"},
    "monitoring": {"name": "Observability & Monitoring", "duration": 1, "priority": "medium"},
    "default": {"name": "Phase", "duration": 2, "priority": "high"},
}


def build_dependency_graph(services: List[Service]) -> Dict[str, List[str]]:
    graph = defaultdict(list)
    for s in services:
        for dep in s.dependencies:
            graph[dep].append(s.id)
    return graph


def compute_in_degrees(services: List[Service]) -> Dict[str, int]:
    in_degrees = {s.id: 0 for s in services}
    for s in services:
        for dep in s.dependencies:
            if dep in in_degrees:
                in_degrees[s.id] += 1
    return in_degrees


def get_service_priority(service_id: str) -> str:
    service_lower = service_id.lower()
    if any(cs in service_lower for cs in ["auth", "user", "identity"]):
        return "critical"
    if any(cs in service_lower for cs in ["gateway", "api"]):
        return "critical"
    if any(cs in service_lower for cs in ["payment", "billing", "transaction"]):
        return "high"
    return "high"


def get_phase_defaults(service_ids: List[str], phase_num: int, architecture: Architecture) -> Dict:
    services_lower = [s.lower() for s in service_ids]
    
    if phase_num == 1 and any(cs in " ".join(services_lower) for cs in ["auth", "user"]):
        return PHASE_DEFAULTS["auth"]
    
    if any(cs in " ".join(services_lower) for cs in ["gateway", "api", "entry"]):
        return PHASE_DEFAULTS["gateway"]
    
    if any(cs in " ".join(services_lower) for cs in ["data", "db", "storage", "cache"]):
        return PHASE_DEFAULTS["data"]
    
    if any(cs in " ".join(services_lower) for cs in ["monitor", "log", "metric", "observe"]):
        return PHASE_DEFAULTS["monitoring"]
    
    if len(service_ids) > 3:
        return PHASE_DEFAULTS["core"]
    
    base = PHASE_DEFAULTS["default"].copy()
    base["name"] = f"Phase {phase_num}"
    base["duration"] = min(4, max(1, len(service_ids)))
    return base


async def plan(architecture: Architecture) -> List[Phase]:
    logger.info("planning_implementation_start", services=len(architecture.services))
    
    services = architecture.services
    if not services:
        return []
        
    in_degrees = compute_in_degrees(services)
    graph = build_dependency_graph(services)
    
    queue = deque([s_id for s_id, deg in in_degrees.items() if deg == 0])
    
    grouped_phases: List[List[str]] = []
    
    while queue:
        level_size = len(queue)
        current_level = []
        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node)
            for neighbor in graph[node]:
                in_degrees[neighbor] -= 1
                if in_degrees[neighbor] == 0:
                    queue.append(neighbor)
        if current_level:
            grouped_phases.append(current_level)
            
    processed = sum(len(lvl) for lvl in grouped_phases)
    if processed != len(services):
        logger.warning("circular_dependency_detected", processed=processed, total=len(services))
        remaining = [s.id for s in services if in_degrees[s.id] > 0]
        if remaining:
            grouped_phases.append(remaining)
            
    phases: List[Phase] = []
    
    for idx, service_ids in enumerate(grouped_phases):
        phase_num = idx + 1
        
        prompt = f"""
        You are planning Phase {phase_num} of a {architecture.domain} system.
        Services to build this phase: {service_ids}
        Overall Architecture Tech Stack: {json.dumps(architecture.tech_stack)}
        Project: {architecture.project_name}
        
        Write a concise, actionable markdown spec for the developers working on this phase.
        Include: specific tasks, acceptance criteria, and technical notes.
        Return ONLY valid JSON like:
        {{"spec_text": "...", "duration_weeks": 2, "name": "Phase Name"}}
        """
        
        defaults = get_phase_defaults(service_ids, phase_num, architecture)
        safe_name = defaults["name"]
        safe_spec = f"# {safe_name}\n\n## Services\n{', '.join(service_ids)}"
        safe_duration = defaults["duration"]
        
        try:
            raw_res = await call_llm(
                system_prompt="Return strictly valid JSON for the phase spec.",
                user_prompt=prompt,
                response_format={"type": "json_object"}
            )
            data = json.loads(raw_res)
            safe_name = data.get("name", safe_name)
            safe_spec = data.get("spec_text", safe_spec)
            safe_duration = max(1, min(8, int(data.get("duration_weeks", safe_duration))))
        except Exception as e:
            logger.error("phase_llm_spec_generation_failed", error=str(e), phase=phase_num)
            
        all_priorities = [get_service_priority(sid) for sid in service_ids]
        phase_priority = "critical" if "critical" in all_priorities else "high"
        
        phase = Phase(
            phase_number=phase_num,
            name=safe_name,
            services_to_build=service_ids,
            dependencies=[i for i in range(1, phase_num)] if phase_num > 1 else [],
            can_parallelize=len(service_ids) > 1,
            priority=phase_priority,
            duration_weeks=safe_duration,
            spec_text=safe_spec
        )
        phases.append(phase)
        
    logger.info("planning_implementation_complete", total_phases=len(phases))
    return phases
