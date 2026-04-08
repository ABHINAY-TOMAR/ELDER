# OpenEnv Grading System - Requirements Summary

## Overview

This document specifies the OpenEnv interface requirements for the Architect Agent evaluation system. The system implements 3 graded tasks with deterministic, reproducible scoring.

---

## Task 1: Stack Recommendation Grader

**Difficulty:** Easy  
**Domain:** All domains (microservices, ai_native, data_pipeline)

### Grading Logic

The grader compares agent recommendations against expert ground truth for 5 core components:

```python
def grade_task_1(agent_recommendation: Dict[str, str], ground_truth: Dict[str, str]) -> float:
    """
    Scoring:
    - 5/5 exact match: 1.0
    - 4/5 match: 0.8
    - 3/5 match: 0.6
    - 2/5 match: 0.4
    - 1/5 match: 0.2
    - 0/5 match: 0.0
    """
```

### 5 Core Components (20% each)

| Component | Examples | Fuzzy Matching Rules |
|-----------|----------|---------------------|
| `api_framework` | FastAPI, Express, Django | "fastapi" ~ "fastapi" ✓, "starlette" ≠ "fastapi" |
| `database` | PostgreSQL, MongoDB, Supabase | "postgresql" ~ "postgres" ✓ |
| `cache_layer` | Redis, Memcached, none | Exact match required for "none" |
| `message_queue` | RabbitMQ, Kafka, SQS, none | "rabbitmq" ~ "amqp" ✗ (no fuzzy) |
| `monitoring` | Prometheus, DataDog, basic | Exact match required |

### Fuzzy Matching Implementation

```python
def fuzzy_match(agent_val: str, truth_val: str) -> float:
    if agent_val == truth_val:
        return 1.0
    
    # Allow PostgreSQL/postgres equivalence
    if "postgres" in [agent_val, truth_val] and "postgresql" in [agent_val, truth_val]:
        return 1.0
    
    # Otherwise strict match only
    return 0.0
```

### Baseline Expected Score
- **0.75** (Sonnet 4 should match most recommendations correctly)

---

## Task 2: Anti-Pattern Detection Grader

**Difficulty:** Medium  
**Domain:** All domains

### Grading Logic

The grader evaluates how many injected anti-patterns the agent correctly identifies:

```python
def grade_task_2(agent_findings: List[str], ground_truth_patterns: Dict) -> float:
    """
    Scoring:
    - Found all 3 patterns: 1.0
    - Found 2/3: 0.67
    - Found 1/3: 0.33
    - Found 0/3: 0.0
    """
    found_count = sum(1 for pattern in ground_truth_patterns 
                      if any_keyword_found(pattern, agent_findings))
    return found_count / len(ground_truth_patterns)
```

### Keyword Matching

```python
def pattern_keywords(pattern_type: str) -> List[str]:
    return {
        "circular_dependency": ["circular", "cycle", "dependency loop", "auth → product → auth"],
        "polyglot_persistence_mismatch": ["polyglot", "persistence", "transaction", "ACID mismatch"],
        "single_point_of_failure": ["single point", "failure", "bottleneck", "all depend on auth"],
        "n_plus_1_query": ["n+1", "query", "inefficient", "loop within loop"],
        "tight_coupling": ["tight", "coupling", "shared database", "monolith"],
    }.get(pattern_type, [])
```

### Injected Anti-Pattern Examples

```python
{
    "circular_dependency": {
        "services": ["auth", "product"],  # auth → product → auth
        "severity": "critical"
    },
    "polyglot_persistence_mismatch": {
        "services": ["cart", "order"],  # cart uses Redis, order needs ACID
        "severity": "high"
    },
    "single_point_of_failure": {
        "service": "auth",
        "description": "Every service depends on auth"
    }
}
```

### Baseline Expected Score
- **0.65** (requires reasoning about system interactions)

---

## Task 3: Full Design Integration Grader

**Difficulty:** Hard  
**Domain:** All domains

### Grading Logic

Composite score with weighted components:

```python
def grade_task_3(architecture: Architecture, ground_truth: Dict) -> float:
    score = 0.0
    
    # 30% - Architecture sensibility
    score += 0.3 * evaluate_sensibility(architecture, ground_truth)
    
    # 20% - Service decomposition quality
    score += 0.2 * evaluate_decomposition(architecture.services)
    
    # 40% - Integration correctness
    score += 0.4 * evaluate_integration(architecture)
    
    # 10% - Failure modes coverage
    score += 0.1 * evaluate_failure_coverage(architecture)
    
    return min(1.0, max(0.0, score))
```

### Component Breakdown

| Component | Weight | Evaluation Criteria |
|-----------|--------|-------------------|
| **Sensibility** | 30% | Latency → caching, Scale → horizontal scaling, PII → encryption, Monitoring exists |
| **Decomposition** | 20% | 2-3 services = 0.6, 4-8 = 1.0, 9-15 = 0.8, >15 = 0.4 |
| **Integration** | 40% | API contract matching, schema alignment, message format compatibility |
| **Failures** | 10% | % of services with identified failure modes |

### Sensibility Evaluation

```python
def evaluate_sensibility(arch, requirements) -> float:
    score = 0.0
    if requirements.get("latency_ms") and arch.has_caching():
        score += 0.25
    if requirements.get("scale") and arch.is_horizontally_scalable():
        score += 0.25
    if requirements.get("pii") and arch.has_encryption():
        score += 0.25
    if arch.has_monitoring():
        score += 0.25
    return score
```

### Integration Evaluation

```python
def evaluate_integration(arch) -> float:
    integration_score = 0.0
    total_pairs = 0
    
    for service_a in arch.services:
        for dep_id in service_a.dependencies:
            service_b = find_service(arch.services, dep_id)
            api_match = validate_api_contract(service_a, service_b)
            schema_match = validate_schema_alignment(service_a, service_b)
            integration_score += (api_match + schema_match) / 2
            total_pairs += 1
    
    return 1.0 if total_pairs == 0 else integration_score / total_pairs
```

### Baseline Expected Score
- **0.45** (requires end-to-end reasoning + validation)

---

## OpenEnv Response Format

### Standard Response Structure

```python
@dataclass
class OpenEnvResponse:
    observation: Optional[Any]  # Current state (null for terminal step)
    reward: Dict[str, float]   # {"score": 0.0-1.0}
    done: bool                 # True = episode complete
    info: Dict[str, Any]       # {"grader_feedback": str, ...}
```

### Response Examples

**Task 1 Response:**
```python
{
    "observation": None,
    "reward": {"score": 0.8},
    "done": True,
    "info": {"grader_feedback": "Stack recommendation: 0.80"}
}
```

**Task 2 Response:**
```python
{
    "observation": None,
    "reward": {"score": 0.67},
    "done": True,
    "info": {"grader_feedback": "Anti-pattern detection: 0.67"}
}
```

**Task 3 Response:**
```python
{
    "observation": None,
    "reward": {"score": 0.45},
    "done": True,
    "info": {"grader_feedback": "Full design integration: 0.45"}
}
```

---

## /reset Endpoint

**Purpose:** Initialize a fresh task environment with a random test case.

### Endpoint Signature

```python
@app.post("/reset")
async def reset(task_id: str) -> Dict:
```

### Flow

```
task_id → select random test case → initialize session state → return state
```

### Implementation

```python
@app.post("/reset")
async def reset(task_id: str) -> Dict:
    """
    OpenEnv interface: /reset
    Initializes a fresh task environment.
    """
    if task_id == "task_stack_recommendation":
        test_case = random.choice(TASK1_TEST_CASES)
    elif task_id == "task_anti_pattern_detection":
        test_case = random.choice(TASK2_TEST_CASES)
    elif task_id == "task_full_design_integration":
        test_case = random.choice(TASK3_TEST_CASES)
    
    task_instance_id = str(uuid.uuid4())
    
    # Persist session state
    await db.create_task_instance(
        task_id=task_id,
        instance_id=task_instance_id,
        test_case=test_case
    )
    
    return {
        "task_id": task_id,
        "instance_id": task_instance_id,
        "state": test_case  # Initial observation
    }
```

### Test Case Structure

**Task 1 Test Case:**
```python
{
    "project_name": "E-commerce Platform",
    "domain": "microservices",
    "team_size": 2,
    "budget_usd": 5000,
    "expected_users": 10000,
    "latency_requirement_ms": 200,
    "data_sensitivity": "pii",
    "deployment_target": "cloud",
    "timeline_weeks": 12,
    "ground_truth": {
        "api_framework": "fastapi",
        "database": "postgresql",
        "cache_layer": "redis",
        "message_queue": "rabbitmq",
        "monitoring": "prometheus"
    }
}
```

**Task 2 Test Case:**
```python
{
    "service_map": {
        "auth": ["product", "order"],
        "product": ["recommendation"],
        "recommendation": ["product"],  # circular!
        "cart": ["order"],
        "order": ["auth"]
    },
    "databases": {
        "auth": "postgresql",
        "product": "postgresql",
        "recommendation": "mongodb",
        "cart": "redis",
        "order": "postgresql"
    },
    "injected_patterns": {
        "circular_dependency": {...},
        "polyglot_persistence_issue": {...},
        "single_point_of_failure": {...}
    }
}
```

**Task 3 Test Case:**
```python
{
    "requirements": "Build recommendation engine for e-commerce...",
    "domain": "ai_native",
    "constraints": ["must use vector database", "PCI-DSS compliance"],
    "ground_truth": {...}
}
```

---

## /step Endpoint

**Purpose:** Agent takes action, receive observation + reward.

### Endpoint Signature

```python
@app.post("/step")
async def step(instance_id: str, action: Dict) -> Dict:
```

### Flow

```
instance_id + action → fetch session → route to grader → return OpenEnv response
```

### Implementation

```python
@app.post("/step")
async def step(instance_id: str, action: Dict) -> Dict:
    """
    OpenEnv interface: /step
    Agent takes action, receive observation + reward.
    """
    task_instance = await db.fetch_task_instance(instance_id)
    
    if task_instance.task_id == "task_stack_recommendation":
        agent_stack = action.get("tech_stack")
        score = grader_task_1(agent_stack, task_instance.ground_truth)
        
        return {
            "observation": None,
            "reward": {"score": score},
            "done": True,
            "info": {"grader_feedback": f"Stack recommendation: {score:.2f}"}
        }
    
    elif task_instance.task_id == "task_anti_pattern_detection":
        agent_findings = action.get("anti_patterns", [])
        score = grader_task_2(agent_findings, task_instance.ground_truth)
        
        return {
            "observation": None,
            "reward": {"score": score},
            "done": True,
            "info": {"grader_feedback": f"Anti-pattern detection: {score:.2f}"}
        }
    
    elif task_instance.task_id == "task_full_design_integration":
        architecture = action.get("architecture")
        score = grader_task_3(architecture, task_instance.ground_truth)
        
        return {
            "observation": None,
            "reward": {"score": score},
            "done": True,
            "info": {"grader_feedback": f"Full design integration: {score:.2f}"}
        }
```

### Action Schemas

**Task 1 Action:**
```python
{
    "action_type": "recommend_stack",
    "tech_stack": {
        "api_framework": "fastapi",
        "database": "postgresql",
        "cache_layer": "redis",
        "message_queue": "rabbitmq",
        "monitoring": "prometheus"
    }
}
```

**Task 2 Action:**
```python
{
    "action_type": "detect_anti_patterns",
    "anti_patterns": [
        "Circular dependency between product and recommendation services",
        "Cart (Redis) and order (PostgreSQL) have transaction mismatch"
    ]
}
```

**Task 3 Action:**
```python
{
    "action_type": "submit_architecture",
    "architecture": {
        "services": [...],
        "tech_stack": {...},
        "data_flows": [...],
        "failure_modes": {...}
    }
}
```

---

## Grader Requirements

All graders must be:

| Requirement | Description |
|-------------|-------------|
| **Deterministic** | Same input → same output every time |
| **Reproducible** | No randomness in scoring |
| **Objective** | Scores don't depend on opinions |
| **Fair** | Doesn't favor specific tech stacks |

---

## Sources

- ARCHITECT_AGENT_COMPLETE_BLUEPRINT.md (lines 495-856)
- CLAUDE_CODE_BUILD_PROMPTS.md (lines 1221-1428)
