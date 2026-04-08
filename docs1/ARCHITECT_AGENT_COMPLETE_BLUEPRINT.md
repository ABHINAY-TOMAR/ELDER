# 🏛️ ARCHITECT AGENT — Complete Blueprint

**Status:** Full Product + OpenEnv Submission  
**Timeline:** 12 weeks  
**Tech Stack:** Python (FastAPI) + React + Supabase (pgvector)  
**Specialization:** All three domains (Microservices, AI-Native, Data Pipelines) with adaptive scope  
**Dispatch:** MCP Protocol (universal agent compatibility)

---

## 📊 Executive Summary

### What You're Building

An AI system architect that operates at the **design layer, not the code layer**:

1. **Takes natural language requirements** → produces production-ready architecture
2. **Reasons hybrid**: Fast pattern-match for known domains + deep thinking for novel/risky decisions
3. **Stores everything in Supabase** with pgvector for semantic search of past architectures
4. **Dispatches to any agent via MCP** (Claude Code, Cursor, Codex, custom agents)
5. **Submits to OpenEnv** with 3 graded tasks across all domains

### Why This Wins

- **First product in the architectural AI layer** (completely empty space)
- **Blocks 10x value from all downstream coding agents** (they build the right thing)
- **OpenEnv positions you** as the system design specialist
- **MCP dispatch** makes you the hub for multi-agent workflows

---

## 🏗️ Part 1: System Architecture

### 1.1 High-Level Data Flow

```
USER REQUIREMENTS (natural language)
        ↓
    [REQUIREMENTS PARSER]
        ↓
    [DOMAIN CLASSIFIER] → microservices? AI-native? data pipeline?
        ↓
    [PATTERN RETRIEVER] → search pgvector for similar past architectures
        ↓
    [FAST PATTERN MATCHER] → recommend stack immediately
        ↓
    [RISKY DECISION DETECTOR] → Which choices need deep thinking?
        ↓
    [HYBRID REASONER] → extended thinking on risky ones only
        ↓
    [ARCHITECTURE GENERATOR] → service map, data flows, ADRs
        ↓
    [FAILURE MODE MAPPER] → identify top 3 failure modes per service
        ↓
    [IMPLEMENTATION PLANNER] → break into ordered phases
        ↓
    [MCP DISPATCHER] → hand off to agents via standard protocol
        ↓
    [COHERENCE CHECKER] → validate service contracts match
        ↓
    [VECTOR EMBEDDER] → store in pgvector for future retrieval
        ↓
    OUTPUT: Full architecture + dispatch plan + monitoring
```

### 1.2 Service Map

```
┌─────────────────────────────────────────────────────────────┐
│                    ARCHITECT AGENT PLATFORM                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [Frontend Layer] ──────────────────────────────────────────│
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐     │
│  │   React UI   │   │  Requirements│   │  Architecture│     │
│  │  Dashboard   │   │   Input Form │   │  Viewer      │     │
│  └──────────────┘   └──────────────┘   └──────────────┘     │
│         ↑                   ↑                    ↑          │
│─────────┼───────────────────┼────────────────────┼──────────│
│         │                   │                    │          │
│  [API Layer - FastAPI] ────────────────────────│            │
│  ┌──────────────────────────────────────────────┐           │
│  │  /design          POST requirements → arch   │           │
│  │  /review          POST arch → critique       │           │
│  │  /assign          POST arch → phase specs    │           │
│  │  /dispatch        POST phase → MCP agents    │           │
│  │  /status          GET task_id → completion   │           │
│  │  /validate        POST services → coherence  │           │
│  └──────────────────────────────────────────────┘           │
│         │                   │                    │          │
│─────────┼───────────────────┼────────────────────┼──────────│
│         │                   │                    │          │
│  [Engine Layer] ────────────────────────────────────────────│
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │Requirements  │  │Domain        │  │Pattern       │       │
│  │Parser        │  │Classifier    │  │Retriever     │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │Fast Pattern  │  │Risky Decision│  │Hybrid        │       │
│  │Matcher       │  │Detector      │  │Reasoner      │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │Architecture  │  │Failure Mode  │  │Implementation│       │
│  │Generator     │  │Mapper        │  │Planner       │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │MCP Dispatcher│  │Coherence     │  │Vector        │       │
│  │              │  │Checker       │  │Embedder      │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│         │                   │                    │          │
│─────────┼───────────────────┼────────────────────┼──────────│
│         │                   │                    │          │
│  [Data Layer - Supabase] ───────────────────────────────────│
│  ┌──────────────────────────────────────────────┐           │
│  │ PostgreSQL Tables:                           │           │
│  │  - projects                                  │           │
│  │  - requirements_submitted                    │           │
│  │  - architectures_generated                   │           │
│  │  - task_assignments (phases)                 │           │
│  │  - agent_execution_traces                    │           │
│  │  - pattern_templates                         │           │
│  │                                              │           │
│  │ pgvector Collections:                        │           │
│  │  - architecture_embeddings (semantic search) │           │
│  │  - pattern_templates_embeddings              │           │
│  │  - design_decisions_embeddings               │           │
│  │                                              │           │
│  │ Vault (Secrets):                             │           │
│  │  - OPENAI_API_KEY (for Sonnet 4)             │           │
│  │  - MCP_AGENT_CREDENTIALS                     │           │
│  └──────────────────────────────────────────────┘           │
│         │                   │                    │          │
│─────────┼───────────────────┼────────────────────┼──────────│
│         │                   │                    │          │
│  [External Integrations] ───────────────────────────────────│
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │OpenAI API    │  │MCP Protocol  │  │Claude Code / │       │
│  │(Sonnet 4)    │  │Dispatcher    │  │Cursor / etc. │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 1.3 Core Components Detail

#### Component 1: Requirements Parser

```python
# Input: Natural language requirement
# Output: Structured RequirementSpec

class RequirementSpec(BaseModel):
    project_name: str
    domain: Literal["microservices", "ai_native", "data_pipeline"]
    team_size: int
    budget_usd: int
    expected_users: int
    latency_requirement_ms: int
    data_sensitivity: Literal["public", "internal", "pii"]
    deployment_target: Literal["cloud", "on_prem", "hybrid"]
    constraints: List[str]  # "must use AWS", "team knows Node.js", etc.
    timeline_weeks: int
    extracted_features: List[str]  # ["recommendations", "real-time", "batch"]
```

#### Component 2: Domain Classifier

```python
# Determines which domain classifier to use
# Checks for keywords:
#   "agent", "orchestration", "agentic" → ai_native
#   "microservices", "REST API", "service mesh" → microservices
#   "ETL", "pipeline", "streaming", "batch" → data_pipeline
#   Hybrid: multi-domain if multiple keywords present

class DomainClassification(BaseModel):
    primary_domain: str
    secondary_domains: List[str]
    confidence: float
    reasoning: str
```

#### Component 3: Pattern Retriever (pgvector)

```python
# Search past architectures for similar requirements
# Embed requirement → find top-5 similar past architectures
# Return: design decisions, tech stack, anti-patterns to avoid

# Supabase query:
SELECT 
  id, 
  architecture_name,
  tech_stack,
  services,
  similarity
FROM architecture_embeddings
WHERE 1 - (embedding <=> requirement_embedding) > 0.7
ORDER BY similarity DESC
LIMIT 5;
```

#### Component 4: Fast Pattern Matcher

```python
# Rule-based matching for known patterns
# Examples:
#   IF domain == "ai_native" AND team_size < 5 AND budget < 10k:
#       RECOMMEND = "Claude Code + Supabase + pgvector (all-in-one)"
#   
#   IF domain == "microservices" AND users > 1M AND latency < 100ms:
#       RECOMMEND = "Kubernetes + gRPC + event-driven"
#       RISKY_DECISION = "scaling strategy" (flag for deep thinking)
#
#   IF domain == "data_pipeline" AND data_sensitivity == "pii":
#       RECOMMEND = "Airflow + encryption at rest/transit"
#       RISKY_DECISION = "data governance" (flag for deep thinking)

class StackRecommendation(BaseModel):
    tech_stack: Dict[str, str]  # "api_framework": "fastapi", etc.
    deployment_target: str
    rationale: str
    risky_decisions: List[str]  # which need deep thinking
```

#### Component 5: Risky Decision Detector

```python
# Identifies decisions that shouldn't be templated
# Examples:
#   - Database choice when requirements are unusual
#   - Security strategy for PII data
#   - Scaling architecture at very high scale (>10M users)
#   - Novel domain combinations
#   - Tight SLA requirements
#   - Regulatory constraints (HIPAA, GDPR, etc.)

class RiskyDecision(BaseModel):
    decision_type: str  # "database_choice", "security_model", etc.
    reason: str
    impact: Literal["high", "medium", "low"]
    why_needs_deep_thinking: str
```

#### Component 6: Hybrid Reasoner

```python
# Fast path: pattern match
# Slow path: Claude Sonnet 4 with extended thinking on risky decisions only

# Pseudocode:
def hybrid_reason(requirement_spec, fast_recommendation, risky_decisions):
    if len(risky_decisions) == 0:
        return fast_recommendation  # instant
    
    # Only spend tokens on risky decisions
    thinking_prompt = f"""
    Given these requirements:
    {requirement_spec}
    
    Initial fast recommendation:
    {fast_recommendation}
    
    Risky decisions that need deeper analysis:
    {risky_decisions}
    
    Please think deeply about why the fast recommendation
    might fail and propose alternatives.
    """
    
    # Use Sonnet 4 extended thinking (budget_tokens=5000-10000)
    response = sonnet_extended_thinking(thinking_prompt)
    
    return merge_fast_and_deep(fast_recommendation, response)
```

#### Component 7: Architecture Generator

```python
# Output structure
class Architecture(BaseModel):
    project_name: str
    service_map: ServiceMap
    data_flows: List[DataFlow]
    tech_stack: Dict[str, str]
    adrs: List[ADR]  # Architecture Decision Records
    failure_modes: Dict[str, FailureMode]  # per service
    implementation_phases: List[Phase]
    dependencies: DependencyGraph
    estimated_effort_weeks: int
    risk_assessment: str

class ServiceMap(BaseModel):
    services: List[Service]
    external_integrations: List[str]
    
class Service(BaseModel):
    id: str
    name: str
    domain: str  # auth, product, recommendation, etc.
    technology: str  # "Python/FastAPI", "Node/Express", etc.
    responsibilities: List[str]
    dependencies: List[str]  # other service IDs
    database: str
    scaling_strategy: str

class ADR(BaseModel):
    id: str  # ADR-001, ADR-002, etc.
    title: str  # "Use PostgreSQL over MongoDB"
    chosen: str
    rejected: List[str]
    reasoning: str
    implications: str

class FailureMode(BaseModel):
    service_id: str
    mode: str  # "service crash", "database unavailable", etc.
    probability: Literal["high", "medium", "low"]
    impact: str
    mitigation: str
    detection_strategy: str
```

#### Component 8: Failure Mode Mapper

```python
# For each service, identify top 3 failure modes
# Based on domain knowledge + LLM reasoning

class FailureModeAnalysis(BaseModel):
    service_id: str
    failure_modes: List[FailureMode]
    
def map_failure_modes(services, domain):
    # Domain-specific failure patterns:
    
    # Microservices:
    #   1. Service crash / unavailability
    #   2. Network latency / timeout
    #   3. Database connection pooling exhaustion
    
    # AI-Native:
    #   1. Model inference timeout / hallucination
    #   2. Vector DB unavailability
    #   3. Token rate limit (API quota)
    
    # Data Pipeline:
    #   1. Job failure / incomplete processing
    #   2. Data quality issue (garbage in, garbage out)
    #   3. Storage quota exceeded
```

#### Component 9: Implementation Planner

```python
# Break architecture into ordered phases
# Respects: dependencies, parallelization, risk ordering

class Phase(BaseModel):
    phase_number: int
    name: str
    duration_weeks: int
    services_to_build: List[str]
    dependencies: List[int]  # previous phase IDs
    can_parallelize: bool
    priority: Literal["critical", "high", "medium"]
    spec_for_agent: str  # ready to hand off to MCP dispatcher

def plan_phases(architecture):
    # Topological sort of services by dependencies
    # Group independent services into same phase
    # Prioritize: auth → core business logic → advanced features
    
    phases = []
    for service_group in topological_sort(architecture.services):
        phase = Phase(
            phase_number=len(phases) + 1,
            services_to_build=service_group,
            spec_for_agent=generate_spec(service_group, architecture)
        )
        phases.append(phase)
    
    return phases
```

#### Component 10: MCP Dispatcher

```python
# Sends phase specs to any agent via MCP protocol
# Unified interface for Claude Code, Cursor, Codex, custom agents

class MCPDispatch(BaseModel):
    task_id: str
    phase_number: int
    services: List[str]
    spec: str  # markdown spec
    openapi_schema: Dict  # if applicable
    database_schema: str
    deadline: datetime
    mcp_server_url: str  # where to find the agent

# MCP Protocol message:
{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tasks/create",
    "params": {
        "task_id": "arch-phase-1",
        "title": "Build Auth Service",
        "spec": "...",
        "deadline": "2026-04-15T00:00:00Z"
    }
}

# Agent responds via MCP:
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "task_id": "arch-phase-1",
        "status": "completed",
        "output": "github_repo_url",
        "services_implemented": ["auth_service"]
    }
}
```

#### Component 11: Coherence Checker

```python
# Validates that services actually integrate correctly
# Checks: API contracts, database schemas, naming conventions

class CoherenceCheck(BaseModel):
    passed: bool
    issues: List[str]
    warnings: List[str]
    service_compatibility: Dict[str, bool]  # per service pair

def check_coherence(phase_outputs):
    issues = []
    
    # Check 1: API contract matching
    for service_pair in phase_outputs.service_pairs():
        if not contracts_match(service_pair.api_consumer, service_pair.api_provider):
            issues.append(f"API mismatch: {service_pair}")
    
    # Check 2: Database schema consistency
    for shared_table in find_shared_tables(phase_outputs.databases):
        if not schemas_match(shared_table):
            issues.append(f"Schema mismatch: {shared_table}")
    
    # Check 3: Naming conventions
    for service in phase_outputs.services:
        if not follows_naming_convention(service.name):
            issues.append(f"Naming violation: {service.name}")
    
    return CoherenceCheck(
        passed=len(issues) == 0,
        issues=issues
    )
```

#### Component 12: Vector Embedder

```python
# Embeds architecture → stores in pgvector
# Makes it searchable for future projects

def embed_and_store(architecture: Architecture):
    # Embed: project description + services + tech stack
    text_to_embed = f"""
    Project: {architecture.project_name}
    Domain: {architecture.domain}
    Services: {[s.name for s in architecture.services]}
    Stack: {architecture.tech_stack}
    Key decisions: {[adr.title for adr in architecture.adrs]}
    """
    
    embedding = openai.embeddings.create(
        input=text_to_embed,
        model="text-embedding-3-small"
    ).data[0].embedding
    
    supabase.table("architecture_embeddings").insert({
        "project_id": architecture.project_id,
        "embedding": embedding,
        "architecture": architecture.model_dump(),
        "created_at": datetime.now()
    })
```

---

## 📊 Part 2: OpenEnv Integration (3 Graded Tasks)

### 2.1 OpenEnv Task Framework

Your environment will be deployed as a **Hugging Face Space** with 3 graded tasks across all domains.

```yaml
# openenv.yaml
name: "Architect Agent"
description: "AI system architect that designs microservices, AI-native, and data pipeline systems"
version: "1.0.0"
domains:
  - microservices
  - ai_native
  - data_pipeline

tasks:
  - id: "task_stack_recommendation"
    name: "Tech Stack Recommendation"
    difficulty: "easy"
    domain: "all"
    
  - id: "task_anti_pattern_detection"
    name: "Architectural Anti-Pattern Detection"
    difficulty: "medium"
    domain: "all"
    
  - id: "task_full_design_integration"
    name: "Full System Design with Integration Validation"
    difficulty: "hard"
    domain: "all"
```

### 2.2 Task 1: Tech Stack Recommendation (Easy)

**Objective:** Given project requirements, recommend an optimal tech stack.

**What the grader receives:**

```python
@dataclass
class Task1Input:
    project_name: str
    domain: Literal["microservices", "ai_native", "data_pipeline"]
    team_size: int
    budget_usd: int
    expected_users: int
    latency_requirement_ms: int
    data_sensitivity: Literal["public", "internal", "pii"]
    deployment_target: Literal["cloud", "on_prem", "hybrid"]
    timeline_weeks: int
```

**Grader Logic:**

```python
def grade_task_1(agent_recommendation: Dict[str, str], ground_truth: Dict[str, str]) -> float:
    """
    Score based on how well agent recommendation matches expert ground truth.
    
    Scoring:
    - Exact match on all 5 core components: 1.0
    - 4/5 match: 0.8
    - 3/5 match: 0.6
    - 2/5 match: 0.4
    - 1/5 match: 0.2
    - 0/5 match: 0.0
    
    Core components: API framework, DB, Cache, Message Queue, Monitoring
    """
    
    components = [
        ("api_framework", 0.2),      # FastAPI, Express, Django, etc.
        ("database", 0.2),           # PostgreSQL, MongoDB, etc.
        ("cache_layer", 0.2),        # Redis, Memcached, etc.
        ("message_queue", 0.2),      # RabbitMQ, Kafka, SQS, etc.
        ("monitoring", 0.2),         # Prometheus, DataDog, etc.
    ]
    
    score = 0.0
    for component, weight in components:
        agent_value = agent_recommendation.get(component, "").lower()
        ground_truth_value = ground_truth.get(component, "").lower()
        
        # Fuzzy matching for similar products
        similarity = fuzzy_match(agent_value, ground_truth_value)
        score += weight * similarity
    
    return score

# Example ground truths:
GROUND_TRUTHS = {
    "domain=microservices, team=2, budget=5k": {
        "api_framework": "fastapi",
        "database": "postgresql",
        "cache_layer": "redis",
        "message_queue": "rabbitmq",
        "monitoring": "prometheus"
    },
    "domain=ai_native, team=1, budget=2k": {
        "api_framework": "fastapi",
        "database": "supabase",
        "cache_layer": "redis",
        "message_queue": "none",
        "monitoring": "basic"
    },
    "domain=data_pipeline, team=3, budget=10k": {
        "api_framework": "none",
        "database": "postgresql",
        "cache_layer": "none",
        "message_queue": "kafka",
        "monitoring": "airflow-ui"
    }
}
```

**Baseline Expected Score:** 0.75 (Sonnet 4 should get most recommendations right)

**How to test locally:**

```bash
curl -X POST http://localhost:7860/step \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "task_stack_recommendation",
    "action_type": "recommend_stack",
    "requirements": {
      "domain": "microservices",
      "team_size": 2,
      "budget_usd": 5000,
      "expected_users": 10000,
      ...
    }
  }'
```

---

### 2.3 Task 2: Anti-Pattern Detection (Medium)

**Objective:** Identify architectural anti-patterns in a given system.

**What the grader receives:**

```python
@dataclass
class Task2Input:
    system_description: str  # "We have 5 services, Auth, Product, Rec, Cart, Order"
    service_map: Dict[str, List[str]]  # "auth": ["product", "order"]
    database_choices: Dict[str, str]  # "auth": "mongodb", "cart": "redis", etc.
    communication_pattern: str  # "rest" or "event_driven" or "mixed"
    scalability_requirements: str  # "1M users", "100k users", etc.
```

**Injected Anti-Patterns (ground truth):**

```python
# 3 carefully crafted anti-patterns per test case
INJECTED_PATTERNS = {
    "test_case_1": {
        "circular_dependency": {
            "services": ["auth", "product"],  # auth → product → auth
            "severity": "critical",
            "description": "Circular dependency creates deployment ordering problem"
        },
        "polyglot_persistence_mismatch": {
            "services": ["cart", "order"],  # cart uses Redis, order expects ACID
            "severity": "high",
            "description": "Cart uses Redis (no transactions), Order needs ACID guarantees"
        },
        "single_point_of_failure": {
            "service": "auth",
            "description": "Every service depends on auth; if it goes down, entire system fails"
        }
    }
}
```

**Grader Logic:**

```python
def grade_task_2(agent_findings: List[str], ground_truth_patterns: Dict) -> float:
    """
    Score: % of injected anti-patterns correctly identified
    
    Full score (1.0): Found all 3 anti-patterns
    Partial credit: Found 2/3 (0.67), 1/3 (0.33), 0/3 (0.0)
    """
    
    found_count = 0
    for pattern_name, pattern_details in ground_truth_patterns.items():
        # Check if agent mentioned this pattern type
        if any(keyword in agent_findings for keyword in pattern_keywords(pattern_name)):
            found_count += 1
    
    score = found_count / len(ground_truth_patterns)
    return score

def pattern_keywords(pattern_type: str) -> List[str]:
    keywords = {
        "circular_dependency": ["circular", "cycle", "dependency loop", "auth → product → auth"],
        "polyglot_persistence_mismatch": ["polyglot", "persistence", "transaction", "ACID mismatch"],
        "single_point_of_failure": ["single point", "failure", "bottleneck", "all depend on auth"],
        "n_plus_1_query": ["n+1", "query", "inefficient", "loop within loop"],
        "tight_coupling": ["tight", "coupling", "shared database", "monolith"],
    }
    return keywords.get(pattern_type, [])
```

**Baseline Expected Score:** 0.65 (medium difficulty; requires reasoning about system interactions)

**Test Case Example:**

```python
test_case = {
    "service_map": {
        "auth": ["product", "order", "cart"],
        "product": ["recommendation"],
        "recommendation": ["product"],  # ← circular!
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
        "circular_dependency": {
            "description": "product → recommendation → product creates deployment ordering problem"
        },
        "polyglot_persistence_issue": {
            "description": "cart (Redis) and order (PostgreSQL) need to be transactional together"
        },
        "single_point_of_failure": {
            "description": "auth service is critical path; if down, entire system fails"
        }
    }
}
```

---

### 2.4 Task 3: Full Design with Integration Validation (Hard)

**Objective:** Design a complete system AND validate that produced service specs actually integrate.

**What the grader receives:**

```python
@dataclass
class Task3Input:
    requirements: str  # "Build recommendation engine for e-commerce with 100k users, <500ms latency"
    domain: str  # "ai_native" or "microservices"
    constraints: List[str]  # "must use PostgreSQL", "async processing required"
```

**Grader Logic:**

```python
def grade_task_3(
    architecture: Architecture,
    generated_specs: Dict[str, PhaseSpec],
    integration_test_results: Dict[str, bool]
) -> float:
    """
    Composite score:
    - Architecture sensibility (30%): Does design make sense for domain?
    - Service count/decomposition (20%): Appropriate granularity?
    - Integration correctness (40%): Do APIs/schemas actually match?
    - Failure modes coverage (10%): Are failure modes identified?
    
    Total: 1.0
    """
    
    score = 0.0
    
    # 30% - Architecture sensibility
    sensibility = evaluate_sensibility(architecture, input_requirements)
    score += 0.3 * sensibility
    
    # 20% - Service decomposition
    decomposition_quality = evaluate_decomposition(architecture.services)
    score += 0.2 * decomposition_quality
    
    # 40% - Integration correctness
    integration_score = 0.0
    total_integrations = 0
    
    for service_a_id, service_a in architecture.services.items():
        for dependency_id in service_a.dependencies:
            service_b = architecture.services[dependency_id]
            
            # Check: do their API contracts match?
            api_match = validate_api_contract(service_a, service_b)
            
            # Check: do their database schemas align (if shared)?
            schema_match = validate_schema_alignment(service_a, service_b)
            
            # Check: are message formats compatible?
            message_match = validate_message_format(service_a, service_b)
            
            integration_score += (api_match + schema_match + message_match) / 3
            total_integrations += 1
    
    if total_integrations > 0:
        integration_score /= total_integrations
    
    score += 0.4 * integration_score
    
    # 10% - Failure modes
    failure_coverage = evaluate_failure_mode_coverage(architecture)
    score += 0.1 * failure_coverage
    
    return min(1.0, max(0.0, score))
```

**Test Case Example:**

```python
test_case_hard = {
    "requirements": """
    Build an AI-powered recommendation engine for e-commerce.
    Requirements:
    - 100,000 users
    - Personalized product recommendations in <500ms
    - Real-time inventory sync
    - Async model retraining daily
    - PII compliance (credit card handling)
    """,
    "domain": "ai_native",
    "constraints": [
        "must use vector database for embeddings",
        "payment processing must be PCI-DSS compliant",
        "async processing for model training"
    ]
}

# What the grader checks:
# 1. Architecture sensibility:
#    - Does it have: API Gateway? Auth? Product Service? Recommendation Engine? 
#      Vector DB? Payment Service? Job Queue?
#    - Are they appropriately decomposed? (Not monolith, not over-engineered)
# 
# 2. Service integration:
#    - Does Recommendation Engine output match Product Service input format?
#    - Does Payment Service expect Auth to return JWT tokens?
#    - Do async job queues have proper retry logic?
#    - Are latency targets achievable with proposed tech stack?
# 
# 3. Failure modes:
#    - If Vector DB goes down, does architecture have fallback?
#    - If payment service is down, does recommendation still work?
```

**Baseline Expected Score:** 0.45 (Hard; requires end-to-end reasoning + validation)

---

### 2.5 OpenEnv Evaluation Criteria Alignment

Your submission will be scored across OpenEnv's 5 criteria:


| Criterion                     | Weight | How Architect Excels                                                                                               |
| ----------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------ |
| **Real-world utility**        | 30%    | Architecture design is THE most expensive mistake startups make. This directly addresses it.                       |
| **Task & grader quality**     | 25%    | 3 tasks progress from easy (pattern match) → hard (full integration). Graders are deterministic & objective.       |
| **Environment design**        | 20%    | Clean state management (requirements → architecture). Non-sparse rewards (partial credit for partial correctness). |
| **Code quality & compliance** | 15%    | FastAPI + pgvector + MCP protocol = production-grade. Full OpenEnv spec compliance.                                |
| **Creativity & novelty**      | 10%    | First AI system architect (filling empty layer). Novel use of pgvector for architecture similarity.                |


**Expected OpenEnv Score:** 75-85 (assuming solid execution)

---

## 🛠️ Part 3: Tech Stack & Architecture

### 3.1 Complete Tech Stack

```
┌─────────────────────────────────────────────────────────┐
│                    TECH STACK                            │
├─────────────────────────────────────────────────────────┤
│
│ FRONTEND
│ ├─ React 18 (vite bundler)
│ ├─ TypeScript
│ ├─ Tailwind CSS + Shadcn/ui
│ ├─ Zustand (state management)
│ ├─ React Query (server state)
│ └─ Mermaid.js (architecture diagram rendering)
│
│ BACKEND
│ ├─ Python 3.11+
│ ├─ FastAPI (async API framework)
│ ├─ Pydantic v2 (validation)
│ ├─ httpx (async HTTP client)
│ ├─ openai (Sonnet 4 API)
│ └─ supabase-py (Supabase client)
│
│ DATABASE
│ ├─ Supabase (managed PostgreSQL)
│ ├─ pgvector extension (vector search)
│ ├─ PostgRES functions (stored procedures)
│ └─ Vault (secrets management)
│
│ INTEGRATIONS
│ ├─ OpenAI API (Sonnet 4 extended thinking)
│ ├─ MCP Protocol (agent dispatch)
│ ├─ Hugging Face Spaces (deployment)
│ └─ GitHub (for pattern storage)
│
│ DEVOPS
│ ├─ Docker (containerization)
│ ├─ Docker Compose (local dev)
│ ├─ GitHub Actions (CI/CD)
│ └─ Supabase CLI (local DB dev)
│
└─────────────────────────────────────────────────────────┘
```

### 3.2 Database Schema (Supabase)

```sql
-- Projects
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id),
    name TEXT NOT NULL,
    description TEXT,
    domain TEXT NOT NULL, -- 'microservices', 'ai_native', 'data_pipeline'
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Requirements submitted
CREATE TABLE requirements_submitted (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    raw_input TEXT NOT NULL,
    parsed_spec JSONB NOT NULL, -- RequirementSpec
    domain TEXT NOT NULL,
    team_size INTEGER,
    budget_usd INTEGER,
    expected_users INTEGER,
    latency_requirement_ms INTEGER,
    data_sensitivity TEXT,
    deployment_target TEXT,
    timeline_weeks INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Generated architectures
CREATE TABLE architectures_generated (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    requirement_id UUID NOT NULL REFERENCES requirements_submitted(id),
    architecture JSONB NOT NULL, -- Full Architecture object
    tech_stack JSONB NOT NULL,
    service_map JSONB NOT NULL,
    adrs JSONB NOT NULL,
    failure_modes JSONB NOT NULL,
    implementation_phases JSONB NOT NULL,
    embedding vector(1536), -- pgvector
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create vector similarity search index
CREATE INDEX ON architectures_generated USING ivfflat (embedding vector_cosine_ops);

-- Task assignments (implementation phases)
CREATE TABLE task_assignments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    architecture_id UUID NOT NULL REFERENCES architectures_generated(id) ON DELETE CASCADE,
    phase_number INTEGER NOT NULL,
    services_to_build TEXT[] NOT NULL,
    spec_text TEXT NOT NULL,
    mcp_agent_url TEXT,
    status TEXT DEFAULT 'pending', -- 'pending', 'dispatched', 'in_progress', 'completed', 'failed'
    assigned_at TIMESTAMP,
    completed_at TIMESTAMP,
    output_repo_url TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Agent execution traces
CREATE TABLE agent_execution_traces (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_assignment_id UUID NOT NULL REFERENCES task_assignments(id) ON DELETE CASCADE,
    mcp_request JSONB NOT NULL,
    mcp_response JSONB NOT NULL,
    status_code INTEGER,
    error_message TEXT,
    execution_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Pattern templates (microservices, ai_native, data_pipeline, etc.)
CREATE TABLE pattern_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    domain TEXT NOT NULL,
    template_name TEXT NOT NULL, -- 'monolith', 'microservices', 'event_driven', etc.
    description TEXT,
    service_blueprint JSONB NOT NULL,
    tech_stack JSONB NOT NULL,
    deployment_instructions TEXT,
    embedding vector(1536), -- pgvector
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX ON pattern_templates USING ivfflat (embedding vector_cosine_ops);

-- Evaluation graders (for OpenEnv tasks)
CREATE TABLE evaluation_graders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id TEXT NOT NULL, -- 'task_stack_recommendation', etc.
    grader_code TEXT NOT NULL, -- Python function
    ground_truth_cases JSONB NOT NULL, -- test cases
    created_at TIMESTAMP DEFAULT NOW()
);

-- OpenEnv task results
CREATE TABLE openenv_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id TEXT NOT NULL,
    attempt_number INTEGER,
    agent_output JSONB NOT NULL,
    grader_score FLOAT NOT NULL,
    grader_feedback TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 3.3 API Spec (FastAPI)

```python
# File: app/api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import logging

app = FastAPI(title="Architect Agent API", version="1.0.0")
logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────
# MODELS
# ──────────────────────────────────────────────────────────

class RequirementInput(BaseModel):
    project_name: str
    requirements_text: str
    domain: Optional[str] = None  # auto-detected if not provided

class ArchitectureResponse(BaseModel):
    project_id: str
    architecture: Dict
    tech_stack: Dict
    service_map: Dict
    adrs: List[Dict]
    failure_modes: Dict
    implementation_phases: List[Dict]
    estimated_effort_weeks: int

class DispatchRequest(BaseModel):
    architecture_id: str
    phase_number: int
    mcp_agent_url: str

class StatusResponse(BaseModel):
    task_id: str
    status: str  # 'pending', 'in_progress', 'completed'
    output_repo: Optional[str]
    error: Optional[str]

# ──────────────────────────────────────────────────────────
# ENDPOINTS
# ──────────────────────────────────────────────────────────

@app.post("/design")
async def design_architecture(req: RequirementInput) -> ArchitectureResponse:
    """
    POST /design
    Takes natural language requirements → returns full architecture.
    """
    logger.info(f"Designing architecture for: {req.project_name}")
    
    # 1. Parse requirements
    parsed = await requirement_parser.parse(req.requirements_text)
    
    # 2. Classify domain
    if not req.domain:
        domain_result = await domain_classifier.classify(parsed)
        req.domain = domain_result.primary_domain
    
    # 3. Retrieve similar past architectures
    similar = await pattern_retriever.search(parsed)
    
    # 4. Fast pattern matching
    fast_recommendation = await fast_pattern_matcher.match(parsed)
    
    # 5. Detect risky decisions
    risky = await risky_decision_detector.detect(fast_recommendation)
    
    # 6. Hybrid reasoning (fast + deep)
    final_recommendation = await hybrid_reasoner.reason(
        parsed, fast_recommendation, risky
    )
    
    # 7. Generate full architecture
    architecture = await architecture_generator.generate(final_recommendation)
    
    # 8. Map failure modes
    architecture.failure_modes = await failure_mode_mapper.map(architecture)
    
    # 9. Create implementation plan
    architecture.implementation_phases = await implementation_planner.plan(architecture)
    
    # 10. Embed and store
    await vector_embedder.embed_and_store(architecture)
    
    return ArchitectureResponse(
        project_id=architecture.project_id,
        architecture=architecture.model_dump(),
        tech_stack=architecture.tech_stack,
        service_map=architecture.service_map.model_dump(),
        adrs=[adr.model_dump() for adr in architecture.adrs],
        failure_modes=architecture.failure_modes,
        implementation_phases=[p.model_dump() for p in architecture.implementation_phases],
        estimated_effort_weeks=architecture.estimated_effort_weeks
    )

@app.post("/review")
async def review_architecture(architecture: Dict) -> Dict:
    """
    POST /review
    Upload existing architecture → get critique & improvements.
    """
    logger.info("Reviewing submitted architecture")
    
    # Analyze for anti-patterns, over-engineering, missing pieces
    critique = await architecture_reviewer.review(architecture)
    
    return {
        "issues_found": critique.issues,
        "improvements": critique.improvements,
        "risk_assessment": critique.risk_assessment,
        "estimated_refactor_effort_weeks": critique.refactor_effort_weeks
    }

@app.post("/assign")
async def assign_agents(architecture_id: str) -> Dict:
    """
    POST /assign
    Takes architecture → produces phase specs ready to hand off to agents.
    """
    logger.info(f"Creating phase specs for architecture: {architecture_id}")
    
    architecture = await db.fetch_architecture(architecture_id)
    phases = await implementation_planner.plan(architecture)
    
    phase_specs = []
    for phase in phases:
        spec = {
            "phase_number": phase.phase_number,
            "services": phase.services_to_build,
            "dependencies": phase.dependencies,
            "spec_text": phase.spec_for_agent,
            "can_parallelize": phase.can_parallelize,
            "duration_weeks": phase.duration_weeks,
            "priority": phase.priority
        }
        phase_specs.append(spec)
    
    return {
        "architecture_id": architecture_id,
        "phases": phase_specs,
        "total_phases": len(phases),
        "parallelizable_phases": sum(1 for p in phases if p.can_parallelize)
    }

@app.post("/dispatch")
async def dispatch_to_agent(req: DispatchRequest) -> Dict:
    """
    POST /dispatch
    Sends phase spec to agent via MCP protocol.
    Tracks task and returns status endpoint.
    """
    logger.info(f"Dispatching phase {req.phase_number} to {req.mcp_agent_url}")
    
    # Get phase spec
    phase = await db.fetch_phase(req.architecture_id, req.phase_number)
    
    # Create MCP dispatch message
    mcp_message = {
        "jsonrpc": "2.0",
        "id": phase.id,
        "method": "tasks/create",
        "params": {
            "task_id": f"arch-phase-{req.phase_number}",
            "title": f"Build Phase {req.phase_number}: {', '.join(phase.services_to_build)}",
            "spec": phase.spec_text,
            "deadline": calculate_deadline(phase.duration_weeks)
        }
    }
    
    # Send via MCP
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{req.mcp_agent_url}/mcp",
            json=mcp_message,
            timeout=30.0
        )
        response.raise_for_status()
    
    # Track in database
    task_id = f"arch-phase-{req.phase_number}"
    await db.create_task_assignment(
        architecture_id=req.architecture_id,
        phase_number=req.phase_number,
        task_id=task_id,
        mcp_agent_url=req.mcp_agent_url,
        status="dispatched"
    )
    
    return {
        "task_id": task_id,
        "status": "dispatched",
        "status_url": f"/status/{task_id}"
    }

@app.get("/status/{task_id}")
async def get_status(task_id: str) -> StatusResponse:
    """
    GET /status/{task_id}
    Polls task completion via MCP.
    """
    logger.info(f"Checking status of task: {task_id}")
    
    assignment = await db.fetch_task_assignment(task_id)
    
    if assignment.status == "completed":
        return StatusResponse(
            task_id=task_id,
            status="completed",
            output_repo=assignment.output_repo_url
        )
    elif assignment.status == "failed":
        return StatusResponse(
            task_id=task_id,
            status="failed",
            error=assignment.error_message
        )
    else:
        return StatusResponse(
            task_id=task_id,
            status=assignment.status
        )

@app.post("/validate")
async def validate_coherence(architecture_id: str, phase_outputs: List[Dict]) -> Dict:
    """
    POST /validate
    Validates that generated services actually integrate correctly.
    """
    logger.info(f"Validating coherence for architecture: {architecture_id}")
    
    coherence_result = await coherence_checker.check(phase_outputs)
    
    return {
        "passed": coherence_result.passed,
        "issues": coherence_result.issues,
        "warnings": coherence_result.warnings,
        "integration_score": coherence_result.integration_score
    }

# ──────────────────────────────────────────────────────────
# OPENENV ENDPOINTS (for hackathon submission)
# ──────────────────────────────────────────────────────────

@app.post("/reset")
async def reset(task_id: str) -> Dict:
    """
    OpenEnv interface: /reset
    Initializes a fresh task environment.
    """
    if task_id == "task_stack_recommendation":
        test_case = random_test_case(task_id)
    elif task_id == "task_anti_pattern_detection":
        test_case = random_test_case(task_id)
    elif task_id == "task_full_design_integration":
        test_case = random_test_case(task_id)
    
    task_instance_id = str(uuid.uuid4())
    
    await db.create_task_instance(
        task_id=task_id,
        instance_id=task_instance_id,
        test_case=test_case
    )
    
    return {
        "task_id": task_id,
        "instance_id": task_instance_id,
        "state": test_case
    }

@app.post("/step")
async def step(instance_id: str, action: Dict) -> Dict:
    """
    OpenEnv interface: /step
    Agent takes action, receive observation + reward.
    """
    task_instance = await db.fetch_task_instance(instance_id)
    
    if task_instance.task_id == "task_stack_recommendation":
        # Agent recommends stack
        agent_stack = action.get("tech_stack")
        
        # Grade it
        score = grader_task_1(agent_stack, task_instance.ground_truth)
        
        return {
            "observation": None,
            "reward": {"score": score},
            "done": True,
            "info": {"grader_feedback": f"Stack recommendation: {score:.2f}"}
        }
    
    elif task_instance.task_id == "task_anti_pattern_detection":
        # Agent identifies anti-patterns
        agent_findings = action.get("anti_patterns", [])
        
        # Grade it
        score = grader_task_2(agent_findings, task_instance.ground_truth)
        
        return {
            "observation": None,
            "reward": {"score": score},
            "done": True,
            "info": {"grader_feedback": f"Anti-pattern detection: {score:.2f}"}
        }
    
    elif task_instance.task_id == "task_full_design_integration":
        # Agent produces full architecture
        architecture = action.get("architecture")
        
        # Grade it
        score = grader_task_3(architecture, task_instance.ground_truth)
        
        return {
            "observation": None,
            "reward": {"score": score},
            "done": True,
            "info": {"grader_feedback": f"Full design integration: {score:.2f}"}
        }

@app.get("/baseline")
async def baseline_inference() -> Dict:
    """
    OpenEnv interface: /baseline
    Runs Sonnet 4 baseline against all 3 tasks, returns scores.
    """
    logger.info("Running baseline inference on all tasks")
    
    scores = {}
    
    for task_id in ["task_stack_recommendation", "task_anti_pattern_detection", "task_full_design_integration"]:
        # Run 3 times, average
        trial_scores = []
        for trial in range(3):
            instance = await reset(task_id)
            
            # Baseline agent action
            baseline_action = await baseline_agent.act(task_id, instance["state"])
            
            # Step
            result = await step(instance["instance_id"], baseline_action)
            
            trial_scores.append(result["reward"]["score"])
        
        scores[task_id] = {
            "scores": trial_scores,
            "average": sum(trial_scores) / len(trial_scores),
            "std_dev": calculate_std_dev(trial_scores)
        }
    
    return scores

@app.get("/tasks")
async def list_tasks() -> Dict:
    """
    OpenEnv interface: /tasks
    Returns available tasks and action schema.
    """
    return {
        "tasks": [
            {
                "id": "task_stack_recommendation",
                "name": "Tech Stack Recommendation",
                "difficulty": "easy",
                "action_schema": {
                    "tech_stack": {
                        "api_framework": "string",
                        "database": "string",
                        "cache_layer": "string",
                        "message_queue": "string",
                        "monitoring": "string"
                    }
                }
            },
            {
                "id": "task_anti_pattern_detection",
                "name": "Anti-Pattern Detection",
                "difficulty": "medium",
                "action_schema": {
                    "anti_patterns": ["list of detected pattern names"]
                }
            },
            {
                "id": "task_full_design_integration",
                "name": "Full System Design with Integration",
                "difficulty": "hard",
                "action_schema": {
                    "architecture": "full Architecture JSON object"
                }
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
```

---

## 📅 Part 4: Implementation Roadmap (12 Weeks)

### Phase 1: Foundation & Core Engine (Weeks 1-4)

**Week 1-2: Setup & Requirements Parser**

- Bootstrap FastAPI project + React frontend
- Set up Supabase (postgres + pgvector + vault)
- Implement `RequirementParser` (NL → structured spec)
- Implement `DomainClassifier` (detect microservices vs ai_native vs data_pipeline)
- Unit tests for parser

**Week 3-4: Pattern Retrieval & Fast Matching**

- Implement `PatternRetriever` (search pgvector for similar architectures)
- Build pattern template library (microservices, ai_native, data_pipeline, monolith, event_driven)
- Implement `FastPatternMatcher` (rule-based stack recommendations)
- Implement `RiskyDecisionDetector` (which choices need deep thinking)
- Integration tests

**Deliverable:** CLI tool that takes requirements → recommends tech stack instantly (latency <1s)

---

### Phase 2: Deep Reasoning & Architecture Generation (Weeks 5-8)

**Week 5-6: Hybrid Reasoner**

- Implement `HybridReasoner` (fast path + Sonnet 4 extended thinking on risky decisions)
- Integrate with OpenAI API (cached credentials in Supabase Vault)
- Tune prompt engineering for architecture reasoning
- Test on 10 real project specs

**Week 7-8: Architecture Generator + Failure Mode Mapper**

- Implement `ArchitectureGenerator` (produce service map, data flows, ADRs)
- Implement `FailureModeMapper` (identify top 3 failure modes per service)
- Implement `ImplementationPlanner` (break into phases, topological sort)
- Implement `VectorEmbedder` (embed + store in pgvector)

**Deliverable:** Full `/design` endpoint that produces production-ready architectures

---

### Phase 3: Agent Dispatch & Integration (Weeks 9-10)

**Week 9: MCP Dispatcher & Coherence Checker**

- Implement `MCPDispatcher` (send phase specs via MCP protocol)
- Implement `CoherenceChecker` (validate service contracts match)
- Implement `/dispatch` endpoint with task tracking
- Test dispatch to mock agent

**Week 10: OpenEnv Integration**

- Implement 3 OpenEnv tasks (stack recommendation, anti-pattern detection, full design)
- Implement graders for all 3 tasks
- Implement `/reset`, `/step`, `/baseline`, `/tasks` endpoints
- Create test cases for each task
- Deploy to Hugging Face Spaces

**Deliverable:** OpenEnv-compliant environment with 3 graded tasks

---

### Phase 4: UI & Polish (Weeks 11-12)

**Week 11: React Dashboard**

- Build requirements input form
- Build architecture viewer (Mermaid diagram rendering)
- Build ADR list display
- Build failure modes display
- Build phase board (Kanban for implementation phases)
- Implement dispatch panel (assign agents, track status)

**Week 12: Documentation & Submission**

- Write comprehensive README
- Document API endpoints
- Create examples & tutorials
- Record demo video
- Submit to OpenEnv
- Deploy to production

**Deliverable:** Full product ready for OpenEnv hackathon

---

## 🎯 Part 5: OpenEnv Submission Checklist

### Pre-Submission (All must pass or DQ)

- HF Space deploys and responds to HTTP
- `openenv validate` passes
- Docker builds cleanly (`docker build .`)
- Baseline inference script runs (`python inference.py`)
- 3 tasks with graders enumerated
- `/reset`, `/step`, `/baseline`, `/tasks` endpoints work
- Graders return 0.0–1.0 scores
- No hardcoded secrets in repo
- Task is NOT a game/toy (real-world system architecture)

### Documentation

- README explains the task
- Motivation section included
- Action/observation JSON examples
- Task descriptions (easy, medium, hard)
- Setup & usage instructions
- Baseline scores documented
- openenv.yaml with metadata

### Testing

- Manual test: 5 real project specs
- Automated test: all 3 tasks grade correctly
- Integration test: agent dispatch → outputs → coherence check
- Variance test: baseline inference runs 3x, scores don't vary >10%

---

## 💻 Part 6: Claude Code Prompts (Build It Yourself)

### Prompt 1: FastAPI Backend Scaffolding

```
Create a FastAPI backend for the Architect Agent with:
1. POST /design endpoint that takes RequirementInput
2. POST /review endpoint
3. POST /assign endpoint
4. POST /dispatch endpoint
5. GET /status/{task_id} endpoint
6. Pydantic models for all inputs/outputs
7. Async throughout
8. Error handling with proper HTTP status codes

Use SQLAlchemy ORM for Supabase (PostgreSQL).
Structure: app/main.py, app/api.py, app/models.py, app/schemas.py

Include docstrings and type hints.
```

### Prompt 2: Requirements Parser

```
Implement RequirementParser in Python that:
1. Takes natural language text (max 1000 chars)
2. Extracts: team_size, budget_usd, expected_users, latency_requirement_ms, 
   data_sensitivity, deployment_target, timeline_weeks
3. Identifies domain hints ("agent", "microservice", "pipeline", etc.)
4. Returns RequirementSpec dataclass

Use Claude API for initial parsing, then validate with rules.
Include unit tests with 10 example inputs.
```

### Prompt 3: Fast Pattern Matcher

```
Create FastPatternMatcher that:
1. Given a RequirementSpec, recommends tech stack
2. Rules-based: IF domain == "ai_native" AND team_size < 5, THEN recommend "FastAPI + Supabase + pgvector"
3. Returns StackRecommendation with rationale + risky_decisions list

Implement rules for:
- Microservices (low/medium/high scale)
- AI-Native (small team, large scale, high complexity)
- Data Pipelines (batch, streaming, hybrid)

Include 20+ rules, with test coverage.
```

### Prompt 4: Hybrid Reasoner

```
Implement HybridReasoner that:
1. Takes fast recommendation + risky decisions list
2. For each risky decision, calls Claude Sonnet 4 with extended thinking
3. Merges deep reasoning with fast recommendation
4. Returns final Architecture spec

Use openai.ChatCompletion with:
- model="claude-sonnet-4-20250514"
- temperature=0.5
- max_tokens=8000 (for extended thinking)

Cache API credentials in Supabase Vault.
Include retry logic and timeout handling.
```

### Prompt 5: Architecture Generator

```
Create ArchitectureGenerator that produces:
1. ServiceMap (list of services with dependencies)
2. DataFlows (how data moves between services)
3. ADRs (Architecture Decision Records)
4. TechStack choices with rationale
5. EstimatedEffortWeeks

Input: HybridReasoner output + RequirementSpec
Output: Full Architecture object (Pydantic model)

Use Claude to flesh out service descriptions based on requirements.
Include templates for different domains.
```

### Prompt 6: OpenEnv Tasks & Graders

```
Implement 3 graders for OpenEnv tasks:

1. grade_task_1_stack_recommendation(agent_recommendation, ground_truth) -> float
   - Fuzzy match on 5 components
   - Score 0.0-1.0

2. grade_task_2_anti_pattern_detection(agent_findings, injected_patterns) -> float
   - Count matching anti-patterns
   - Partial credit per finding

3. grade_task_3_full_design_integration(architecture, integration_tests) -> float
   - Composite: sensibility (30%) + decomposition (20%) + integration (40%) + failures (10%)

Include test cases and expected scores.
```

---

## 🚀 Part 7: Key Decisions Made


| Decision             | Choice               | Rationale                                                               |
| -------------------- | -------------------- | ----------------------------------------------------------------------- |
| **Backend Language** | Python (FastAPI)     | You prefer it; cleaner async than Node; better for AI/ML integration    |
| **Database**         | Supabase (pgvector)  | All-in-one: postgres + vector search + vault; you know it               |
| **Agent Dispatch**   | MCP protocol         | Universal; works with any agent (Claude Code, Cursor, Codex, custom)    |
| **Reasoning**        | Hybrid (fast + deep) | Fast pattern match for 90% of cases; reserve tokens for novel decisions |
| **Domain Coverage**  | All three            | Ambitious; makes OpenEnv submission stronger; can be narrowed if needed |
| **Deployment**       | HF Spaces            | OpenEnv requirement; Docker makes it portable                           |
| **Frontend**         | React + Shadcn/ui    | Your style (EduCore); fast to build; polished                           |
| **Grading**          | Deterministic rules  | Repeatable; no randomness; perfect for OpenEnv                          |


---

## 📊 Expected Metrics

### Performance

- `**/design` latency:** <3s (fast path) to <30s (with deep thinking)
- **Vector search:** <100ms (pgvector similarity)
- **Baseline inference:** ~5-10 minutes per full run (all 3 tasks)
- **MCP dispatch:** <1s (HTTP call to agent)

### Quality

- **OpenEnv scores:** 75-85 (if execution is solid)
- **Real-world validation:** 5+ actual startup projects tested
- **Code coverage:** >80% on critical paths

### Business

- **TAM:** Every startup building multi-agent systems (thousands/year)
- **Pricing model:** Free (MVP) → $49/mo (Pro) → Enterprise
- **Competitive advantage:** First product in the architectural AI layer

---

## 🎯 Success Criteria

By end of 12 weeks:

✅ **OpenEnv submission complete** with 3 graded tasks  
✅ **Full-featured product** with UI + dispatch + integration  
✅ **All-three-domains** support (microservices, AI-native, data pipelines)  
✅ **Production-ready code** (FastAPI + pgvector + MCP)  
✅ **Comprehensive docs** (README, API spec, examples)  
✅ **Validated on real projects** (5+ test cases)  
✅ **Baseline inference** reproducible and working  
✅ **Ready to take external users** after submission  

---

## 🔄 Next Steps (Starting Today)

**Week 1:**

1. Create GitHub repo: `architect-agent`
2. Bootstrap FastAPI project
3. Set up Supabase (postgres + pgvector)
4. Create requirements parser
5. Test with 10 real project specs

**Use Claude Code to build each component.**  
**I'll provide specific build prompts when you're ready.**

---

**Ready to start building? Let's ship this.** 🚀