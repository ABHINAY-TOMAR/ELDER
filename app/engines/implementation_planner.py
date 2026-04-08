import structlog
import json
from typing import List, Dict, Set
from collections import defaultdict, deque
from app.models.schemas import Architecture, Phase, Service
from app.engines.llm_client import call_llm

logger = structlog.get_logger("architect_agent.implementation_planner")

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
            if dep in in_degrees: # some robustness
                in_degrees[s.id] += 1
    return in_degrees

async def plan(architecture: Architecture) -> List[Phase]:
    """
    Sort services topologically and groups them into phases.
    Uses LLM to flesh out the spec document for the phases.
    """
    logger.info("planning_implementation_start", services=len(architecture.services))
    
    services = architecture.services
    if not services:
        return []
        
    in_degrees = compute_in_degrees(services)
    graph = build_dependency_graph(services)
    
    # Topological sort (Kahn's algorithm) grouped by levels/phases
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
            
    # Check cycle
    processed = sum(len(lvl) for lvl in grouped_phases)
    if processed != len(services):
        logger.warning("circular_dependency_detected", processed=processed, total=len(services))
        # fallback: dump remaining into the last phase
        remaining = [s.id for s in services if in_degrees[s.id] > 0]
        if remaining:
            grouped_phases.append(remaining)
            
    phases: List[Phase] = []
    
    for idx, service_ids in enumerate(grouped_phases):
        phase_num = idx + 1
        
        # Build spec
        prompt = f"""
        You are planning Phase {phase_num}.
        Services to build this phase: {service_ids}
        Overall Architecture Tech: {json.dumps(architecture.tech_stack)}
        Domain: {architecture.domain}
        
        Write a concise, actionable markdown spec for the developers working on this phase.
        Return ONLY valid JSON like:
        {{"spec_text": "...", "duration_weeks": 2, "name": "Phase Name"}}
        """
        
        safe_name = f"Phase {phase_num}"
        safe_spec = "# Scaffold Phase"
        safe_duration = 2
        
        try:
            raw_res = await call_llm(
                system_prompt="Return strictly valid JSON for the phase spec.",
                user_prompt=prompt,
                response_format={"type": "json_object"}
            )
            data = json.loads(raw_res)
            safe_name = data.get("name", safe_name)
            safe_spec = data.get("spec_text", safe_spec)
            safe_duration = data.get("duration_weeks", 2)
        except Exception as e:
            logger.error("phase_llm_spec_generation_failed", error=str(e), phase=phase_num)
            
        phase = Phase(
            phase_number=phase_num,
            name=safe_name,
            services_to_build=service_ids,
            dependencies=[i for i in range(1, phase_num)] if phase_num > 1 else [],
            can_parallelize=len(service_ids) > 1,
            priority="critical" if phase_num == 1 else "high",
            duration_weeks=safe_duration,
            spec_text=safe_spec
        )
        phases.append(phase)
        
    logger.info("planning_implementation_complete", total_phases=len(phases))
    return phases
