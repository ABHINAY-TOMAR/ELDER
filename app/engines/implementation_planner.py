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

COMPLEXITY_MULTIPLIERS = {
    "low": 1.0,
    "medium": 1.5,
    "high": 2.0,
    "critical": 2.5
}

SERVICE_COMPLEXITY = {
    "auth": "high",
    "payment": "critical",
    "billing": "high",
    "transaction": "critical",
    "order": "medium",
    "inventory": "medium",
    "product": "low",
    "user": "medium",
    "notification": "low",
    "email": "low",
    "sms": "low",
    "analytics": "medium",
    "search": "high",
    "recommendation": "critical",
    "ai": "critical",
    "ml": "critical",
    "gateway": "medium",
    "api": "medium",
    "cache": "low",
    "database": "medium",
    "queue": "medium",
    "stream": "high",
    "websocket": "medium",
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


def estimate_service_complexity(service_ids: List[str]) -> str:
    max_complexity = "low"
    for sid in service_ids:
        sid_lower = sid.lower()
        for key, complexity in SERVICE_COMPLEXITY.items():
            if key in sid_lower:
                if complexity == "critical":
                    return "critical"
                elif complexity == "high" and max_complexity != "critical":
                    max_complexity = "high"
                elif complexity == "medium" and max_complexity in ["low"]:
                    max_complexity = "medium"
    return max_complexity


def estimate_phase_duration(service_ids: List[str], phase_num: int, architecture: Architecture) -> int:
    base_duration = len(service_ids)
    complexity = estimate_service_complexity(service_ids)
    multiplier = COMPLEXITY_MULTIPLIERS.get(complexity, 1.0)
    
    duration = int(base_duration * multiplier)
    
    domain_adjustments = {
        "microservices": 1.2,
        "ai_native": 1.5,
        "data_pipeline": 1.3,
    }
    domain_mult = domain_adjustments.get(architecture.domain, 1.0)
    duration = int(duration * domain_mult)
    
    return max(1, min(8, duration))


def generate_fallback_spec(service_ids: List[str], phase_num: int, architecture: Architecture, defaults: Dict) -> str:
    complexity = estimate_service_complexity(service_ids)
    
    tasks = []
    for sid in service_ids:
        sid_lower = sid.lower()
        if "auth" in sid_lower:
            tasks.extend(["Implement authentication endpoints", "Add JWT token handling", "Set up OAuth2 flows"])
        elif "gateway" in sid_lower or "api" in sid_lower:
            tasks.extend(["Configure routing rules", "Set up rate limiting", "Add request validation"])
        elif "payment" in sid_lower or "billing" in sid_lower:
            tasks.extend(["Integrate payment gateway", "Handle webhooks", "Implement retry logic"])
        elif "notification" in sid_lower or "email" in sid_lower:
            tasks.extend(["Set up notification templates", "Configure delivery providers", "Add queue processing"])
        elif "analytics" in sid_lower or "report" in sid_lower:
            tasks.extend(["Design data models", "Create aggregation queries", "Build visualization endpoints"])
        elif "ai" in sid_lower or "ml" in sid_lower or "model" in sid_lower:
            tasks.extend(["Set up model endpoints", "Configure inference pipeline", "Add monitoring"])
        else:
            tasks.extend([f"Implement {sid} core logic", f"Add {sid} API endpoints", f"Write {sid} tests"])
    
    spec = f"""# {defaults['name']}

## Overview
Phase {phase_num} implementation for the {architecture.project_name} project.

## Services
{', '.join(service_ids)}

## Tasks
"""
    for i, task in enumerate(tasks, 1):
        spec += f"{i}. {task}\n"
    
    spec += f"""
## Acceptance Criteria
- All services compile and pass unit tests
- API endpoints return expected responses
- Integration with dependent services verified

## Technical Notes
- Complexity: {complexity}
- Domain: {architecture.domain}
"""
    return spec


def get_phase_defaults(service_ids: List[str], phase_num: int, architecture: Architecture) -> Dict:
    services_lower = [s.lower() for s in service_ids]
    combined = " ".join(services_lower)
    
    if phase_num == 1 and any(cs in combined for cs in ["auth", "user", "identity"]):
        return PHASE_DEFAULTS["auth"]
    
    if any(cs in combined for cs in ["gateway", "api", "entry"]):
        return PHASE_DEFAULTS["gateway"]
    
    if any(cs in combined for cs in ["data", "db", "storage"]):
        return PHASE_DEFAULTS["data"]
    
    if any(cs in combined for cs in ["monitor", "log", "metric", "observe"]):
        return PHASE_DEFAULTS["monitoring"]
    
    if any(cs in combined for cs in ["payment", "transaction", "billing"]):
        return PHASE_DEFAULTS["integration"]
    
    if len(service_ids) > 3:
        return PHASE_DEFAULTS["core"]
    
    base = PHASE_DEFAULTS["default"].copy()
    base["name"] = f"Phase {phase_num}"
    base["duration"] = estimate_phase_duration(service_ids, phase_num, architecture)
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
        safe_duration = defaults["duration"]
        safe_spec = generate_fallback_spec(service_ids, phase_num, architecture, defaults)
        
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
            safe_spec = generate_fallback_spec(service_ids, phase_num, architecture, defaults)
            logger.info("using_enhanced_fallback_spec", phase=phase_num)
            
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
