"""
OpenEnv Graders for AI System Architecture Design Tasks.
Deterministic grading functions for evaluating agent outputs against ground truth.
"""

from typing import Dict, List, Any, Optional
from app.models.schemas import Architecture, Service, ADR, FailureMode, DataFlow


def fuzzy_match(agent_val: str, truth_val: str) -> float:
    """
    Fuzzy matching for similar technology products.
    Handles common synonyms and variations.
    """
    agent_val, truth_val = agent_val.lower().strip(), truth_val.lower().strip()
    
    if not agent_val or not truth_val:
        return 0.0
    
    if agent_val == truth_val:
        return 1.0
    
    if agent_val in truth_val or truth_val in agent_val:
        return 1.0
    
    synonyms = [
        {"postgresql", "postgres", "pg"},
        {"milvus", "zilliz", "weaviate", "pinecone"},
        {"redis", "memcached", "redislite"},
        {"rabbitmq", "amqp", "activemq"},
        {"kafka", "confluent", "msk"},
        {"prometheus", "grafana", "datadog"},
        {"fastapi", "starlette", "flask", "django"},
        {"express", "nodejs", "nestjs", "koa"},
        {"supabase", "firebase", "realm"},
        {"mongodb", "mongo"},
        {"airflow", "Prefect", "Dagster"},
        {"kubernetes", "k8s", "eks", "gke"},
    ]
    
    for syn_set in synonyms:
        if agent_val in syn_set and truth_val in syn_set:
            return 1.0
    
    return 0.0


PATTERN_KEYWORDS = {
    "circular_dependency": ["circular", "cycle", "loop", "cyclic"],
    "single_point_of_failure": ["single point", "spof", "bottleneck", "redundancy", "critical"],
    "polyglot_persistence_issue": ["polyglot", "persistence", "transaction", "acid", "redis"],
    "tight_coupling": ["tight", "coupling", "coupled", "monolith", "shared"],
    "shared_database": ["shared database", "shared schema", "coupling", "bottleneck"],
    "n_plus_1_query": ["n+1", "n plus 1", "query", "inefficient", "loop"],
    "unencrypted_pii": ["encryption", "gdpr", "hipaa", "pii", "plaintext", "unencrypted"],
    "spof": ["single point", "spof", "bottleneck", "redundancy"],
}


def get_keywords_for_pattern(pattern_name: str) -> List[str]:
    """Get keywords for detecting anti-patterns."""
    return PATTERN_KEYWORDS.get(pattern_name, [pattern_name])


def grade_task_1(
    agent_recommendation: Dict[str, str],
    ground_truth: Dict[str, str]
) -> float:
    """
    Grade Task 1: Tech Stack Recommendation.
    
    Score based on how well agent recommendation matches expert ground truth.
    
    Components (5 total, 0.2 weight each):
    - api_framework
    - database
    - cache_layer
    - message_queue
    - monitoring
    
    Returns:
        float: Score between 0.0 and 1.0
    """
    if not ground_truth:
        return 0.0
    
    components = [
        ("api_framework", 0.2),
        ("database", 0.2),
        ("cache_layer", 0.2),
        ("message_queue", 0.2),
        ("monitoring", 0.2),
    ]
    
    score = 0.0
    for component, weight in components:
        agent_val = agent_recommendation.get(component, "").lower().strip()
        truth_val = ground_truth.get(component, "").lower().strip()
        
        if agent_val == truth_val:
            similarity = 1.0
        else:
            similarity = fuzzy_match(agent_val, truth_val)
        
        score += weight * similarity
    
    return min(1.0, max(0.0, score))


def grade_task_2(
    agent_findings: str | list[str],
    ground_truth_patterns: Dict[str, Dict]
) -> float:
    """
    Grade anti-pattern detection.
    
    Score: % of injected anti-patterns correctly identified.
    
    Full score (1.0): Found all anti-patterns
    Partial credit: Found 2/3 (0.67), 1/3 (0.33), 0/3 (0.0)
    
    Returns:
        float: Score between 0.0 and 1.0
    """
    if not ground_truth_patterns:
        return 0.0
    
    if not agent_findings:
        return 0.0
    
    # Convert list to string if needed
    if isinstance(agent_findings, list):
        agent_findings_lower = " ".join(str(f).lower() for f in agent_findings)
    else:
        agent_findings_lower = str(agent_findings).lower()
    found_count = 0
    
    for pattern_name, pattern_info in ground_truth_patterns.items():
        keywords = get_keywords_for_pattern(pattern_name)
        
        if any(keyword.lower() in agent_findings_lower for keyword in keywords):
            found_count += 1
    
    return found_count / len(ground_truth_patterns)


def evaluate_sensibility(arch: Dict | Architecture, requirements: Dict) -> float:
    """
    Evaluate if architecture design makes sense for the requirements.
    
    Checks:
    - Latency requirement → caching strategy present
    - Scale requirement → horizontal scaling support
    - PII requirement → encryption/security present
    - Monitoring present
    """
    score = 0.0
    
    # Handle both dict and Architecture object
    if isinstance(arch, dict):
        tech_stack = arch.get("tech_stack", {})
        services = arch.get("services", [])
    else:
        tech_stack = getattr(arch, "tech_stack", {})
        services = getattr(arch, "services", [])
    
    tech_stack_str = " ".join(str(v) for v in tech_stack.values()).lower() if isinstance(tech_stack, dict) else str(tech_stack).lower()
    
    if requirements.get("latency_ms"):
        if "cache" in tech_stack_str or "redis" in tech_stack_str:
            score += 0.25
    
    if requirements.get("scale"):
        if "horizontal" in tech_stack_str or "scale" in tech_stack_str or "replica" in tech_stack_str:
            score += 0.25
    
    if requirements.get("pii"):
        if any(kw in tech_stack_str for kw in ["encrypt", "security", "auth", "jwt"]):
            score += 0.25
    
    if tech_stack.get("monitoring") if isinstance(tech_stack, dict) else False or "monitoring" in tech_stack_str:
        score += 0.25
    
    return score


def evaluate_decomposition(services: List[Service] | List[Dict]) -> float:
    """
    Evaluate service decomposition quality.
    
    - Too few services (< 2): 0.0 (underdeveloped)
    - 2-3 services: 0.6 (reasonable for small projects)
    - 4-8 services: 1.0 (ideal range)
    - 9-15 services: 0.8 (a bit much, but acceptable)
    - > 15 services: 0.4 (over-engineered)
    """
    if not services:
        return 0.0
    service_count = len(services)
    
    if service_count < 2:
        return 0.0
    elif service_count < 4:
        return 0.6
    elif service_count <= 8:
        return 1.0
    elif service_count <= 15:
        return 0.8
    else:
        return 0.4


def evaluate_integration(arch: Dict | Architecture) -> float:
    """
    Evaluate integration correctness.
    
    Check that all service dependencies are resolvable and that
    data flows are properly defined.
    """
    # Handle both dict and Architecture object
    if isinstance(arch, dict):
        services = arch.get("services", [])
    else:
        services = getattr(arch, "services", [])
    
    if not services:
        return 0.0
    
    integration_score = 0.0
    total_pairs = 0
    
    # Get service IDs (handle both dict and object)
    if services and isinstance(services[0], dict):
        service_ids = {s.get("id") for s in services}
        for service_a in services:
            for dep_id in service_a.get("dependencies", []):
                if dep_id in service_ids:
                    integration_score += 1.0
                total_pairs += 1
    else:
        service_ids = {s.id for s in services}
        for service_a in services:
            for dep_id in service_a.dependencies:
                if dep_id in service_ids:
                    integration_score += 1.0
                total_pairs += 1
    
    if total_pairs == 0:
        return 1.0
    
    return integration_score / total_pairs


def evaluate_failure_coverage(arch: Dict | Architecture) -> float:
    """
    Evaluate failure mode coverage.
    
    Score based on percentage of services with identified failure modes.
    """
    # Handle both dict and Architecture object
    if isinstance(arch, dict):
        services = arch.get("services", [])
        failure_modes = arch.get("failure_modes", {})
    else:
        services = getattr(arch, "services", [])
        failure_modes = getattr(arch, "failure_modes", {})
    
    if not services:
        return 0.0
    
    if not failure_modes:
        return 0.0
    
    # Count services with failure modes
    if isinstance(services, list) and len(services) > 0:
        if isinstance(services[0], dict):
            # List of dicts
            services_with_failures = len([
                s for s in services
                if s.get("id") in failure_modes and failure_modes[s.get("id")]
            ])
        else:
            # List of Service objects
            services_with_failures = len([
                s for s in services
                if s.id in failure_modes and failure_modes[s.id]
            ])
    else:
        services_with_failures = 0
    
    return services_with_failures / len(services) if services else 0.0


def grade_task_3(
    architecture: Dict | Architecture,
    ground_truth_requirements: Dict
) -> float:
    """
    Grade Task 3: Full Design with Integration Validation.
    
    Composite score:
    - Architecture sensibility (30%): Does design make sense?
    - Service decomposition (20%): Good service granularity?
    - Integration correctness (40%): Do services actually integrate?
    - Failure modes coverage (10%): Are failure modes covered?
    
    Returns:
        float: Score between 0.0 and 1.0
    """
    # Handle both dict and Architecture object
    if isinstance(architecture, dict):
        services = architecture.get("services", [])
    else:
        services = getattr(architecture, "services", [])
    
    score = 0.0
    
    sensibility = evaluate_sensibility(architecture, ground_truth_requirements)
    score += 0.3 * sensibility
    
    decomposition = evaluate_decomposition(services)
    score += 0.2 * decomposition
    
    integration = evaluate_integration(architecture)
    score += 0.4 * integration
    
    failures = evaluate_failure_coverage(architecture)
    score += 0.1 * failures
    
    return min(1.0, max(0.0, score))


def grade_task_3_from_dict(
    architecture_dict: Dict[str, Any],
    ground_truth_requirements: Dict
) -> float:
    """
    Grade Task 3 from dictionary input (when Architecture model parsing might fail).
    
    Falls back to heuristic scoring based on dict keys present.
    """
    if not architecture_dict:
        return 0.0
    
    score = 0.0
    
    services = architecture_dict.get("services", [])
    tech_stack = architecture_dict.get("tech_stack", {})
    
    if isinstance(services, list) and len(services) > 0:
        score += 0.2 * evaluate_decomposition(services)
    
    if tech_stack:
        score += 0.1
    
    if architecture_dict.get("adrs"):
        score += 0.1
    
    if architecture_dict.get("data_flows"):
        score += 0.2
    
    if architecture_dict.get("failure_modes"):
        score += 0.1
    
    return min(1.0, max(0.0, score))


def get_grade_breakdown_task_1(
    agent_recommendation: Dict[str, str],
    ground_truth: Dict[str, str]
) -> Dict[str, float]:
    """Get detailed breakdown for Task 1 grading."""
    components = ["api_framework", "database", "cache_layer", "message_queue", "monitoring"]
    breakdown = {}
    total = 0.0
    
    for component in components:
        agent_val = agent_recommendation.get(component, "").lower().strip()
        truth_val = ground_truth.get(component, "").lower().strip()
        
        if agent_val == truth_val:
            similarity = 1.0
        else:
            similarity = fuzzy_match(agent_val, truth_val)
        
        breakdown[component] = similarity
        total += similarity
    
    breakdown["total"] = min(1.0, max(0.0, total))
    return breakdown


def get_grade_breakdown_task_3(
    architecture: Architecture,
    ground_truth_requirements: Dict
) -> Dict[str, float]:
    """Get detailed breakdown for Task 3 grading."""
    return {
        "sensibility": evaluate_sensibility(architecture, ground_truth_requirements),
        "decomposition": evaluate_decomposition(architecture.services),
        "integration": evaluate_integration(architecture),
        "failure_coverage": evaluate_failure_coverage(architecture)
    }
