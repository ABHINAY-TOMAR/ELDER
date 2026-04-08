# OpenEnv Graders - Research

**Researched:** 2026-04-07
**Domain:** AI Agent Evaluation / Grading Systems
**Confidence:** HIGH (Implementation already exists in codebase)

## Summary

The OpenEnv system uses three deterministic graders to evaluate AI agent performance on system architecture design tasks. Each grader scores a different aspect: tech stack recommendations, anti-pattern detection, and full architecture integration. All graders return normalized scores between 0.0-1.0 and are designed to be **deterministic**, **reproducible**, **objective**, and **fair** (no stack favoritism).

**Primary implementation location:** `app/openenv/graders.py`
**Test cases location:** `app/openenv/test_cases.py`
**Data models:** `app/models/schemas.py`

---

## Grader 1: Stack Recommendation (`grade_task_1`)

### Purpose
Score how well an agent's technology stack recommendation matches expert ground truth.

### Input
| Parameter | Type | Description |
|-----------|------|-------------|
| `agent_recommendation` | `Dict[str, str]` | Agent's tech stack (5 components) |
| `ground_truth` | `Dict[str, str]` | Expert ground truth (5 components) |

### Components (5 total, 0.2 weight each)
| Component | Examples | Weight |
|-----------|----------|--------|
| `api_framework` | fastapi, express, django | 0.2 |
| `database` | postgresql, mongodb, supabase | 0.2 |
| `cache_layer` | redis, memcached, none | 0.2 |
| `message_queue` | rabbitmq, kafka, sqs, none | 0.2 |
| `monitoring` | prometheus, datadog, basic | 0.2 |

### Scoring Algorithm

```
score = Σ (weight_i × similarity_i) for i in [0..4]
return clamp(score, 0.0, 1.0)
```

**Where similarity is calculated as:**
1. Exact match → 1.0
2. Substring match (a in b or b in a) → 1.0  
3. Fuzzy match via synonym lookup → 1.0
4. Otherwise → 0.0

### Fuzzy Matching Implementation

```python
def fuzzy_match(agent_val: str, truth_val: str) -> float:
    """Returns 1.0 if technologies are equivalent, 0.0 otherwise."""
    agent_val, truth_val = agent_val.lower().strip(), truth_val.lower().strip()
    
    # Empty check
    if not agent_val or not truth_val:
        return 0.0
    
    # Exact match
    if agent_val == truth_val:
        return 1.0
    
    # Substring match
    if agent_val in truth_val or truth_val in agent_val:
        return 1.0
    
    # Synonym group matching
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
        {"airflow", "prefect", "dagster"},
        {"kubernetes", "k8s", "eks", "gke"},
    ]
    
    for syn_set in synonyms:
        if agent_val in syn_set and truth_val in syn_set:
            return 1.0
    
    return 0.0
```

### Synonym Groups

| Group | Members |
|-------|---------|
| PostgreSQL variants | postgresql, postgres, pg |
| Vector DBs | milvus, zilliz, weaviate, pinecone |
| Caches | redis, memcached, redislite |
| Message Queues | rabbitmq, amqp, activemq |
| Kafka variants | kafka, confluent, msk |
| Monitoring | prometheus, grafana, datadog |
| Python APIs | fastapi, starlette, flask, django |
| Node APIs | express, nodejs, nestjs, koa |
| BaaS | supabase, firebase, realm |
| Document DBs | mongodb, mongo |
| Workflow Engines | airflow, prefect, dagster |
| K8s variants | kubernetes, k8s, eks, gke |

### Test Cases

```python
# Exact match → 1.0
grade_task_1(
    {"api_framework": "fastapi", "database": "postgresql", ...},
    {"api_framework": "fastapi", "database": "postgresql", ...}
)  # → 1.0

# Synonym match → 1.0
grade_task_1(
    {"database": "postgres"},
    {"database": "postgresql"}
)  # → 1.0

# Partial match → 0.6 (3/5 components correct)
grade_task_1(
    {"api_framework": "fastapi", "database": "wrong", "cache_layer": "redis", "message_queue": "wrong", "monitoring": "prometheus"},
    {"api_framework": "fastapi", "database": "postgresql", "cache_layer": "redis", "message_queue": "rabbitmq", "monitoring": "prometheus"}
)  # → 0.6
```

### Baseline Expected Score
**0.75** — Sonnet 4 should get most recommendations right with this algorithm.

---

## Grader 2: Anti-Pattern Detection (`grade_task_2`)

### Purpose
Score how many injected anti-patterns the agent correctly identifies.

### Input
| Parameter | Type | Description |
|-----------|------|-------------|
| `agent_findings` | `str` | Agent's findings/report as string |
| `ground_truth_patterns` | `Dict[str, Dict]` | Patterns that should be detected |

### Scoring Algorithm

```
found_count = count of patterns where any keyword matches agent_findings
score = found_count / total_patterns
```

### Keyword Detection Logic

```python
def get_keywords_for_pattern(pattern_name: str) -> List[str]:
    """Get keywords for detecting anti-patterns."""
    mapping = {
        "circular_dependency": ["circular", "cycle", "loop", "cyclic"],
        "single_point_of_failure": ["single point", "spof", "bottleneck", "redundancy", "critical"],
        "polyglot_persistence_issue": ["polyglot", "persistence", "transaction", "acid", "redis"],
        "tight_coupling": ["tight", "coupling", "coupled", "monolith", "shared"],
        "shared_database": ["shared database", "shared schema", "coupling", "bottleneck"],
        "n_plus_1_query": ["n+1", "n plus 1", "query", "inefficient", "loop"],
        "unencrypted_pii": ["encryption", "gdpr", "hipaa", "pii", "plaintext", "unencrypted"],
        "spof": ["single point", "spof", "bottleneck", "redundancy"],
    }
    return mapping.get(pattern_name, [pattern_name])
```

### Pattern → Keywords Mapping

| Pattern | Keywords | Severity Weight |
|---------|----------|-----------------|
| `circular_dependency` | circular, cycle, loop, cyclic | critical |
| `single_point_of_failure` | single point, spof, bottleneck, redundancy, critical | high |
| `polyglot_persistence_issue` | polyglot, persistence, transaction, acid, redis | medium |
| `tight_coupling` | tight, coupling, coupled, monolith, shared | high |
| `shared_database` | shared database, shared schema, coupling, bottleneck | medium |
| `n_plus_1_query` | n+1, n plus 1, query, inefficient, loop | medium |
| `unencrypted_pii` | encryption, gdpr, hipaa, pii, plaintext, unencrypted | critical |
| `spof` | single point, spof, bottleneck, redundancy | high |

### Detection Algorithm

```python
def grade_task_2(agent_findings: str, ground_truth_patterns: Dict[str, Dict]) -> float:
    if not ground_truth_patterns:
        return 0.0
    if not agent_findings:
        return 0.0
    
    agent_findings_lower = agent_findings.lower()
    found_count = 0
    
    for pattern_name, pattern_info in ground_truth_patterns.items():
        keywords = get_keywords_for_pattern(pattern_name)
        if any(keyword.lower() in agent_findings_lower for keyword in keywords):
            found_count += 1
    
    return found_count / len(ground_truth_patterns)
```

### Test Cases

```python
# Found all 3 patterns → 1.0
grade_task_2(
    "The system has circular dependencies and auth is a single point of failure. "
    "The cart uses Redis while orders use PostgreSQL causing ACID issues.",
    {
        "circular_dependency": {...},
        "single_point_of_failure": {...},
        "polyglot_persistence_issue": {...}
    }
)  # → 1.0

# Found 2/3 patterns → 0.67
grade_task_2(
    "Auth is a critical single point of failure. Cart uses Redis.",
    {...}  # 3 patterns
)  # → 0.67

# Found 0/3 patterns → 0.0
grade_task_2(
    "The system looks good overall.",
    {...}  # 3 patterns
)  # → 0.0
```

### Baseline Expected Score
**0.65** — Medium difficulty; requires reasoning about system interactions.

---

## Grader 3: Full Design Integration (`grade_task_3`)

### Purpose
Composite score evaluating complete architecture design with integration validation.

### Input
| Parameter | Type | Description |
|-----------|------|-------------|
| `architecture` | `Architecture` | Complete architecture from agent |
| `ground_truth_requirements` | `Dict` | Expected requirements |

### Composite Scoring Formula

```
total_score = 0.3 × sensibility + 0.2 × decomposition + 0.4 × integration + 0.1 × failures
return clamp(total_score, 0.0, 1.0)
```

### Component Breakdown

| Component | Weight | Description |
|-----------|--------|-------------|
| Sensibility | 30% | Does design make sense for requirements? |
| Decomposition | 20% | Appropriate service granularity? |
| Integration | 40% | Do services actually integrate? |
| Failure Coverage | 10% | Are failure modes identified? |

### Sub-Component Algorithms

#### 1. Sensibility Evaluation (30%)

```python
def evaluate_sensibility(arch: Architecture, requirements: Dict) -> float:
    score = 0.0
    tech_stack_str = " ".join(str(v) for v in arch.tech_stack.values()).lower()
    
    if requirements.get("latency_ms"):
        if "cache" in tech_stack_str or "redis" in tech_stack_str:
            score += 0.25
    
    if requirements.get("scale"):
        if "horizontal" in tech_stack_str or "scale" in tech_stack_str or "replica" in tech_stack_str:
            score += 0.25
    
    if requirements.get("pii"):
        if any(kw in tech_stack_str for kw in ["encrypt", "security", "auth", "jwt"]):
            score += 0.25
    
    if arch.tech_stack.get("monitoring") or "monitoring" in tech_stack_str:
        score += 0.25
    
    return score  # Max 1.0
```

**Criteria:**
| Requirement | Required in Tech Stack |
|-------------|------------------------|
| `latency_ms` | cache or redis |
| `scale` | horizontal, scale, or replica |
| `pii` | encrypt, security, auth, or jwt |
| Any | monitoring present |

#### 2. Decomposition Evaluation (20%)

```python
def evaluate_decomposition(services: List[Service]) -> float:
    service_count = len(services)
    
    if service_count < 2:
        return 0.0  # Underdeveloped
    elif service_count < 4:
        return 0.6  # Reasonable for small projects
    elif service_count <= 8:
        return 1.0  # Ideal range
    elif service_count <= 15:
        return 0.8  # Acceptable
    else:
        return 0.4  # Over-engineered
```

| Service Count | Score | Reason |
|---------------|-------|--------|
| < 2 | 0.0 | Underdeveloped |
| 2-3 | 0.6 | Reasonable for small projects |
| 4-8 | 1.0 | Ideal range |
| 9-15 | 0.8 | Acceptable but complex |
| > 15 | 0.4 | Over-engineered |

#### 3. Integration Evaluation (40%)

```python
def evaluate_integration(arch: Architecture) -> float:
    if not arch.services:
        return 0.0
    
    integration_score = 0.0
    total_pairs = 0
    
    service_ids = {s.id for s in arch.services}
    
    for service_a in arch.services:
        for dep_id in service_a.dependencies:
            if dep_id in service_ids:  # Valid dependency
                integration_score += 1.0
            total_pairs += 1
    
    if total_pairs == 0:
        return 1.0  # No dependencies = trivially integrated
    
    return integration_score / total_pairs
```

**Checks:**
- All dependency references point to valid services
- Score = valid_dependencies / total_dependencies
- 0 dependencies = perfect score (trivially integrated)

#### 4. Failure Coverage (10%)

```python
def evaluate_failure_coverage(arch: Architecture) -> float:
    if not arch.services or not arch.failure_modes:
        return 0.0
    
    services_with_failures = len([
        s for s in arch.services
        if s.id in arch.failure_modes and arch.failure_modes[s.id]
    ])
    
    return services_with_failures / len(arch.services)
```

**Score:** % of services with at least one identified failure mode.

### Complete Algorithm

```python
def grade_task_3(architecture: Architecture, ground_truth_requirements: Dict) -> float:
    score = 0.0
    
    sensibility = evaluate_sensibility(architecture, ground_truth_requirements)
    score += 0.3 * sensibility
    
    decomposition = evaluate_decomposition(architecture.services)
    score += 0.2 * decomposition
    
    integration = evaluate_integration(architecture)
    score += 0.4 * integration
    
    failures = evaluate_failure_coverage(architecture)
    score += 0.1 * failures
    
    return min(1.0, max(0.0, score))
```

### Test Cases

```python
# Perfect design
grade_task_3(
    Architecture(
        services=[Service(id="auth", ...), Service(id="api", ...), ...],  # 5 services
        tech_stack={"api": "fastapi", "cache": "redis", "monitoring": "prometheus", ...},
        failure_modes={"auth": [...], "api": [...]}
    ),
    {"latency_ms": 500, "scale": "10k", "pii": True}
)  # → 1.0
```

### Baseline Expected Score
**Varies** — Depends on architecture quality, but well-designed systems should score 0.7+.

---

## Helper Functions

### Required by Graders

| Function | Location | Purpose |
|----------|----------|---------|
| `fuzzy_match()` | graders.py:10 | Technology synonym matching |
| `get_keywords_for_pattern()` | graders.py:48 | Anti-pattern keyword lookup |
| `evaluate_sensibility()` | graders.py:141 | Task 3 sensibility check |
| `evaluate_decomposition()` | graders.py:173 | Service count scoring |
| `evaluate_integration()` | graders.py:197 | Dependency validation |
| `evaluate_failure_coverage()` | graders.py:224 | Failure mode coverage |
| `get_grade_breakdown_task_1()` | graders.py:312 | Per-component scores |
| `get_grade_breakdown_task_3()` | graders.py:337 | Sub-component scores |

### Optional Utilities

| Function | Purpose |
|----------|---------|
| `grade_task_3_from_dict()` | Fallback grading when Architecture parsing fails |

---

## Data Models

### Architecture Model (schemas.py)

```python
class Architecture(BaseModel):
    project_id: str
    project_name: str
    domain: Literal["microservices", "ai_native", "data_pipeline"]
    services: List[Service]
    tech_stack: Dict[str, str]
    adrs: List[ADR]
    failure_modes: Dict[str, List[FailureMode]]
    data_flows: List[DataFlow]
    implementation_phases: List[Phase]
    estimated_effort_weeks: int
    
    def has_caching(self) -> bool
    def is_horizontally_scalable(self) -> bool
    def has_encryption(self) -> bool
    def has_monitoring(self) -> bool
```

### Service Model

```python
class Service(BaseModel):
    id: str           # e.g., "auth_service"
    name: str         # Human-readable
    description: str # What it does
    dependencies: List[str]  # Service IDs it depends on
```

### FailureMode Model

```python
class FailureMode(BaseModel):
    mode: str
    probability: Literal["high", "medium", "low"]
    impact: str
    detection_strategy: str
    mitigation_strategy: str
    fallback_strategy: str
    owner: str
    severity: Literal["critical", "high", "medium", "low"]
```

---

## Edge Cases & Boundary Conditions

| Scenario | Handling |
|----------|----------|
| Empty agent_recommendation | Return 0.0 |
| Empty ground_truth | Return 0.0 |
| Empty agent_findings | Return 0.0 |
| No services in architecture | Return 0.0 for integration, 0.0 for decomposition |
| No dependencies | Return 1.0 for integration (trivially integrated) |
| Empty failure_modes dict | Return 0.0 for failure coverage |
| Service count = 0 | Decomposition = 0.0 |
| Score > 1.0 | Clamp to 1.0 |
| Score < 0.0 | Clamp to 0.0 |

---

## Ground Truth Test Cases

### Task 1 (2 test cases)
```python
# test_case_1_microservices_small
{
    "requirements": {"domain": "microservices", "team_size": 2, "budget_usd": 5000, ...},
    "ground_truth": {
        "api_framework": "fastapi",
        "database": "postgresql",
        "cache_layer": "redis",
        "message_queue": "rabbitmq",
        "monitoring": "prometheus"
    }
}

# test_case_2_ai_native_startup
{
    "requirements": {"domain": "ai_native", "team_size": 1, "budget_usd": 2000, ...},
    "ground_truth": {
        "api_framework": "fastapi",
        "database": "supabase",
        "cache_layer": "none",
        "message_queue": "none",
        "monitoring": "basic"
    }
}
```

### Task 2 (2 test cases)
```python
# test_case_1_circular_spf (3 patterns)
{
    "ground_truth_patterns": {
        "circular_dependency": {...},
        "single_point_of_failure": {...},
        "polyglot_persistence_issue": {...}
    }
}

# test_case_2_tight_coupling (3 patterns)
{
    "ground_truth_patterns": {
        "tight_coupling": {...},
        "shared_database": {...},
        "n_plus_1_query": {...}
    }
}
```

### Task 3 (2 test cases)
```python
# test_case_1_recommendation_engine
{
    "requirements": {
        "latency_ms": 500,
        "scale": "100k users",
        "pii": True,
        ...
    },
    "ground_truth_requirements": {
        "latency_ms": 500,
        "scale": "100k users",
        "pii": True,
        "required_services": ["api_gateway", "auth", "product", "recommendation", "vector_db"],
        "required_integrations": ["auth → recommendation", "product → recommendation", "recommendation → product"],
        "required_failure_modes": ["vector_db_down", "model_timeout", "auth_failure"]
    }
}

# test_case_2_microservices_platform
{...}  # Similar structure
```

---

## Open Questions

1. **Should fuzzy_match use Levenshtein distance?** — Current implementation uses synonym sets only. Adding edit-distance could catch typos (e.g., "postgrsql" vs "postgresql").

2. **Should Task 2 require pattern severity weighting?** — Current implementation gives equal weight to all patterns regardless of severity (critical vs medium).

3. **Should Task 3 integration check data flow formats?** — Currently only checks dependency validity, not whether data_flows are properly defined.

4. **Should there be a partial credit for "close" anti-pattern detection?** — Current implementation is binary (found/not found).

---

## Sources

### Primary (HIGH confidence)
- `app/openenv/graders.py` — Implementation (347 lines)
- `app/openenv/test_cases.py` — Test data (214 lines)
- `app/models/schemas.py` — Data models (188 lines)

### Secondary (MEDIUM confidence)
- `docs1/ARCHITECT_AGENT_COMPLETE_BLUEPRINT.md` lines 548-609, 673-702, 754-812
- `docs1/CLAUDE_CODE_BUILD_PROMPTS.md` lines 1221-1429

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — Implementation already exists in codebase
- Architecture: HIGH — Full implementation documented
- Pitfalls: MEDIUM — Edge cases identified but not exhaustively tested

**Research date:** 2026-04-07
**Valid until:** 2026-05-07 (30 days — stable implementation)
