# 🛠️ ARCHITECT AGENT — Claude Code Build Prompts

**How to use:** Copy each prompt into Claude Code, adjust for your context, and run.

---

## 🚀 Prompt 1: FastAPI Backend Scaffolding & Main API

**File to create:** `app/main.py`

```
Create a production-ready FastAPI backend for the Architect Agent system.

REQUIREMENTS:
1. Base FastAPI app with proper logging and error handling
2. CORS enabled for React frontend
3. Environment variable loading (OPENAI_API_KEY, SUPABASE_URL, etc.)
4. Health check endpoint: GET /health
5. Structured logging with JSON output
6. Global exception handler for proper HTTP error responses
7. Request/response logging middleware

PROJECT STRUCTURE:
- app/main.py (this file - entry point)
- app/api/ (endpoints will go here)
- app/engines/ (reasoning engines)
- app/models/ (Pydantic models)
- app/database/ (Supabase integration)
- app/config.py (settings)

TECH STACK:
- FastAPI with async/await throughout
- Python 3.11+
- httpx for async HTTP calls
- python-dotenv for environment variables
- structlog for structured logging

CODE STYLE:
- Type hints everywhere
- Comprehensive docstrings
- Async-first (async def, await)
- Proper error handling with context

Include:
- startup/shutdown events
- dependency injection setup
- CORS middleware configuration
- Request ID tracking for logging
- Example usage comments

Make it production-ready but keep it simple. No over-engineering.
```

---

## 🎯 Prompt 2: Pydantic Models & Data Schemas

**File to create:** `app/models/schemas.py`

```
Create comprehensive Pydantic v2 models for the Architect Agent.

These models represent the core data structures flowing through the system.

MODELS TO DEFINE:

1. INPUT MODELS
   - RequirementInput (user provides project description)
   - ReviewRequest (user uploads architecture for critique)
   - DispatchRequest (trigger agent dispatch)

2. CORE DATA MODELS
   - RequirementSpec (parsed requirements)
   - Service (individual microservice/component)
   - ServiceMap (collection of services + dependencies)
   - DataFlow (how data moves between services)
   - ADR (Architecture Decision Record)
   - FailureMode (identified risk + mitigation)
   - TechStackRecommendation (recommended technologies)
   - Phase (implementation phase)
   - Architecture (complete system design)

3. RESPONSE MODELS
   - ArchitectureResponse (what /design endpoint returns)
   - ReviewResponse (what /review endpoint returns)
   - DispatchResponse (what /dispatch endpoint returns)
   - StatusResponse (what /status endpoint returns)
   - ErrorResponse (standard error format)

4. OPENENV-SPECIFIC MODELS
   - TaskResetRequest / TaskResetResponse
   - TaskStepRequest / TaskStepResponse
   - TaskStatusResponse
   - RewardSignal (0.0-1.0 score)

5. DATABASE MODELS
   - ProjectDB (database record)
   - RequirementDB (stored requirement)
   - ArchitectureDB (stored architecture)
   - TaskAssignmentDB (phase assignment record)

REQUIREMENTS:
- Use Pydantic v2 syntax (field_validator, ConfigDict)
- Add examples for each model (model_config with json_schema_extra)
- Add field descriptions (Field(description="..."))
- Use Literal types for enums
- Validate constraints (e.g., users > 0, budget >= 0)
- Include proper JSON schema generation
- Make models as strict as possible (validate early)

TYPE DEFINITIONS:
- Enum: domain (microservices, ai_native, data_pipeline)
- Enum: data_sensitivity (public, internal, pii)
- Enum: deployment_target (cloud, on_prem, hybrid)
- Enum: task_status (pending, dispatched, in_progress, completed, failed)

EXAMPLE MODEL STRUCTURE:
class Architecture(BaseModel):
    project_id: str = Field(description="Unique project identifier")
    project_name: str = Field(description="Human-readable project name")
    domain: Literal["microservices", "ai_native", "data_pipeline"] = Field(description="Primary domain")
    services: List[Service] = Field(description="List of services to build")
    tech_stack: Dict[str, str] = Field(description="Recommended technologies")
    adrs: List[ADR] = Field(description="Architectural decision records")
    failure_modes: Dict[str, List[FailureMode]] = Field(description="Identified risks")
    implementation_phases: List[Phase] = Field(description="Ordered phases")
    estimated_effort_weeks: int = Field(description="Total effort", ge=1, le=52)
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "project_id": "proj_123",
            "project_name": "E-commerce Platform",
            ...
        }
    })

Be comprehensive. Include every data structure the system uses.
Include validators for complex logic (e.g., circular dependency detection).
```

---

## 📝 Prompt 3: Requirements Parser Engine

**File to create:** `app/engines/requirement_parser.py`

```
Implement the RequirementParser engine.

FUNCTIONALITY:
Takes raw natural language requirement text (typically 200-500 words)
and extracts structured information into a RequirementSpec.

PARSING STRATEGY:
1. First pass: Use Claude API (no full reasoning needed) to extract key facts
2. Second pass: Validate extracted values against constraints
3. Third pass: Fill in defaults and infer missing values

KEY FIELDS TO EXTRACT:
- team_size (number of engineers)
- budget_usd (monthly or total)
- expected_users (at launch and at scale)
- latency_requirement_ms (p99 latency target)
- data_sensitivity (whether handling PII, payment data, etc.)
- deployment_target (cloud, on-prem, or hybrid)
- timeline_weeks (when they need to ship)
- key_features (["recommendations", "real-time", "offline-first", etc.])
- constraints (["must use AWS", "team knows Python", "GDPR compliance", etc.])

IMPLEMENTATION:
1. Create async function: async def parse(text: str) -> RequirementSpec
2. Use Claude API with a simple prompt (not extended thinking)
3. Extract JSON from Claude response
4. Validate with Pydantic model
5. Fill in defaults if fields are missing
6. Return RequirementSpec

ERROR HANDLING:
- If Claude can't parse, return RequirementSpec with defaults + warnings
- If validation fails, raise ValueError with helpful message
- Include confidence scores for each extracted field

EXAMPLE WORKFLOW:
Input: "We're 2 engineers building an AI-powered recommendation engine. 
We have $10k/month budget and expect 100k users in 6 months. 
Need <500ms latency. Using AWS only. GDPR compliant."

Output: RequirementSpec(
  team_size=2,
  budget_usd=10000,
  expected_users=100000,
  latency_requirement_ms=500,
  data_sensitivity="pii",
  deployment_target="cloud",
  timeline_weeks=26,
  key_features=["recommendations", "real-time"],
  constraints=["must use AWS", "GDPR compliant"]
)

CONSTRAINTS:
- No extended thinking (fast, < 1s per request)
- Use text-davinci-003 or gpt-3.5-turbo for speed
- Cache the parser prompt if possible
- Handle edge cases gracefully

Include:
- Full docstrings with type hints
- Unit tests with 5+ example inputs
- Integration test with actual Claude API
- Logging statements for debugging
```

---

## 🏗️ Prompt 4: Domain Classifier

**File to create:** `app/engines/domain_classifier.py`

```
Implement the DomainClassifier engine.

FUNCTIONALITY:
Analyzes a RequirementSpec and determines which domain(s) it belongs to:
- microservices (REST APIs, service-oriented, traditional SaaS)
- ai_native (agents, multi-agent orchestration, RAG, agentic workflows)
- data_pipeline (ETL, batch processing, streaming, analytics)

CLASSIFIER LOGIC:
Analyze for domain keywords and patterns:

MICROSERVICES SIGNALS:
- Keywords: "API", "microservice", "REST", "gRPC", "service mesh"
- Feature pattern: CRUD, real-time sync, multi-user
- Tech preference: Kubernetes, Docker, traditional web frameworks

AI_NATIVE SIGNALS:
- Keywords: "agent", "agentic", "orchestration", "LLM", "RAG"
- Feature pattern: autonomous decision-making, reasoning, multi-step workflows
- Tech preference: vector DB, LLM APIs, memory systems

DATA_PIPELINE SIGNALS:
- Keywords: "ETL", "pipeline", "streaming", "batch", "analytics", "warehouse"
- Feature pattern: data transformation, aggregation, scheduled jobs
- Tech preference: Airflow, Spark, Kafka, data warehouse

DOMAIN CLASSIFICATION RULES:
1. Rule 1: If "agent" in features OR "agent" in team_skills → ai_native (high confidence)
2. Rule 2: If "streaming" or "ETL" in features → data_pipeline (high confidence)
3. Rule 3: If API/REST-heavy with multi-service decomposition → microservices
4. Rule 4: If unclear, default to microservices (most common)

MULTI-DOMAIN SUPPORT:
Some systems span multiple domains. Return:
- primary_domain: str (highest confidence)
- secondary_domains: List[str] (lower confidence)
- confidence: float (0.0-1.0 on primary)
- reasoning: str (explain why)

IMPLEMENTATION:
async def classify(spec: RequirementSpec) -> DomainClassification:
    # Keyword-based classification
    # Score each domain
    # Return ranked result

Include:
- Rule-based logic (no LLM needed for speed)
- Confidence scoring
- Full docstrings
- Unit tests covering all 3 domains + edge cases
- Integration test
- Example outputs for each domain

Keep it fast (<100ms). This runs on every request.
```

---

## 🔍 Prompt 5: Pattern Retriever (pgvector)

**File to create:** `app/engines/pattern_retriever.py`

```
Implement the PatternRetriever using pgvector for semantic search.

FUNCTIONALITY:
Given a RequirementSpec, search past architectures for similar projects.
Use vector similarity to find designs that solved similar problems.

WORKFLOW:
1. Convert RequirementSpec to embedding vector
2. Query pgvector in Supabase for top-5 similar architectures
3. Return architectures with similarity scores
4. Extract key patterns: tech stack, service count, failure modes, etc.

VECTOR EMBEDDING STRATEGY:
Use OpenAI text-embedding-3-small (fast, cheap):
- Embed the requirement text: project description + domain + team size + budget
- Store alongside each architecture in database
- Use cosine similarity for matching

DATABASE QUERIES:
- Supabase PostgreSQL with pgvector extension
- Table: architecture_embeddings
- Query: SELECT * FROM architecture_embeddings 
          WHERE 1 - (embedding <=> req_embedding) > 0.75
          ORDER BY similarity DESC LIMIT 5

CACHING:
Cache embeddings of past architectures (they don't change often).
Only embed new requirements.

IMPLEMENTATION:
async def retrieve_similar(spec: RequirementSpec) -> List[SimilarArchitecture]:
    # Embed the requirement
    # Query pgvector
    # Return similar architectures with reasoning

Include:
- Supabase client initialization
- Embedding function (use OpenAI API)
- SQL query construction
- Result parsing
- Error handling for database errors
- Logging for debugging
- Unit tests with mock database
- Integration test with real Supabase

PERFORMANCE:
- Should be <500ms including embedding
- Cache embeddings aggressively
- Use indexes on pgvector for speed

Return structure:
class SimilarArchitecture(BaseModel):
    project_id: str
    similarity_score: float (0.0-1.0)
    tech_stack: Dict[str, str]
    services: List[str]
    lessons_learned: str
    anti_patterns_avoided: List[str]
```

---

## ⚡ Prompt 6: Fast Pattern Matcher

**File to create:** `app/engines/fast_pattern_matcher.py`

```
Implement FastPatternMatcher for instant tech stack recommendations.

FUNCTIONALITY:
Given a RequirementSpec, instantly recommend a tech stack using rules.
No LLM, no vector search — pure rule-based matching.
Latency target: <100ms.

RULE SYSTEM:
Define rules as: IF (conditions) THEN (recommendation)

EXAMPLE RULES (implement 20+):

# Microservices domain
Rule 1: IF domain == "microservices" AND team_size == 1-2 AND budget < 5k
        THEN api_framework="FastAPI" OR "Express"
             database="PostgreSQL"
             cache="Redis"
             message_queue="none" (use polling instead)
             monitoring="prometheus"
             confidence=0.95

Rule 2: IF domain == "microservices" AND team_size >= 10 AND expected_users > 1M
        THEN api_framework="Go" OR "Java"
             database="PostgreSQL"
             cache="Redis"
             message_queue="Kafka"
             monitoring="Datadog"
             confidence=0.90

# AI-Native domain
Rule 3: IF domain == "ai_native" AND team_size == 1 AND budget < 2k
        THEN api_framework="FastAPI"
             database="Supabase"
             cache="none"
             vector_db="pgvector"
             monitoring="none" (basic stdout logging)
             confidence=0.95

Rule 4: IF domain == "ai_native" AND team_size >= 3 AND budget >= 10k
        THEN api_framework="FastAPI"
             database="PostgreSQL"
             cache="Redis"
             vector_db="Weaviate" OR "Milvus"
             message_queue="Celery" OR "RabbitMQ"
             monitoring="Prometheus"
             confidence=0.90

# Data Pipeline domain
Rule 5: IF domain == "data_pipeline" AND expected_users > 1M
        THEN orchestration="Airflow"
             processing="Spark"
             storage="S3"
             warehouse="BigQuery" OR "Snowflake"
             confidence=0.90

RISKY DECISION DETECTION:
Flag decisions that shouldn't be templated:
- IF data_sensitivity == "pii" AND no_security_mention THEN risky_decision="security"
- IF expected_users > 10M AND no_scaling_mention THEN risky_decision="scaling"
- IF latency < 100ms THEN risky_decision="performance"

IMPLEMENTATION:
def match(spec: RequirementSpec) -> (StackRecommendation, List[RiskyDecision]):
    score = evaluate_rules(spec)
    best_match = select_best_rule(score)
    risky = detect_risky(spec, best_match)
    return StackRecommendation(...), risky

STRUCTURE:
class Rule(BaseModel):
    id: str
    conditions: Dict (e.g., domain, team_size ranges, budget ranges)
    recommendation: Dict
    confidence: float
    priority: int

database = [Rule(...), Rule(...), ...]

def evaluate_rules(spec) -> List[Tuple[Rule, float]]:
    # Score each rule
    # Return sorted by score

Include:
- 20+ rules across all domains
- Rule prioritization (high priority rules first)
- Tie-breaking logic (multiple rules match with same score)
- Full test coverage (every rule tested)
- Performance benchmarks (<100ms)
- Explanations for each recommendation

Keep it deterministic. Same input = same output. No randomness.
```

---

## 🤔 Prompt 7: Risky Decision Detector

**File to create:** `app/engines/risky_decision_detector.py`

```
Implement RiskyDecisionDetector.

FUNCTIONALITY:
Identifies architectural choices that shouldn't be templated.
These are decisions that need deeper reasoning (Claude Sonnet 4 extended thinking).

PATTERNS TO DETECT:

1. UNUSUAL SCALE:
   - If expected_users > 10M AND no scaling_strategy mentioned → risky
   - If latency_requirement < 100ms AND no caching_strategy mentioned → risky
   - If data volume > 100GB AND no sharding_strategy mentioned → risky

2. SECURITY & COMPLIANCE:
   - If data_sensitivity == "pii" AND not GDPR/HIPAA mentioned → risky
   - If payment_processing needed AND no encryption_strategy → risky

3. NOVEL DOMAIN COMBINATIONS:
   - IF ai_native + real-time + streaming → risky (complex)
   - IF multi-region deployment + low budget → risky (expensive)

4. TECHNOLOGY MISMATCH:
   - IF team_size == 1 AND architecture_is_complex → risky
   - IF timeline < 4 weeks AND high_complexity_features → risky

5. MISSING CRITICAL INFO:
   - IF reliability_requirement == "critical" AND no_DR_strategy → risky
   - IF data_sensitivity == "pii" AND no_data_retention_policy → risky

IMPLEMENTATION:
def detect(spec: RequirementSpec, fast_recommendation: StackRecommendation) -> List[RiskyDecision]:
    risky_decisions = []
    
    # Check each pattern
    for pattern in RISKY_PATTERNS:
        if pattern.matches(spec, fast_recommendation):
            risky_decisions.append(RiskyDecision(
                decision_type=pattern.type,
                reason=pattern.reason(spec),
                impact="high",  # or "medium" / "low"
                why_needs_deep_thinking=pattern.rationale
            ))
    
    return risky_decisions

class RiskyDecision(BaseModel):
    decision_type: str  # "scaling", "security", "performance", etc.
    reason: str  # Specific to this project
    impact: Literal["high", "medium", "low"]
    why_needs_deep_thinking: str

Include:
- 15+ risk patterns
- Scoring system for risk level
- Clear explanations for why decision is risky
- Full test coverage
- Integration with fast matcher
- Logging for what was flagged as risky

Keep it fast (<100ms). This runs before expensive deep thinking.
```

---

## 🧠 Prompt 8: Hybrid Reasoner (Extended Thinking)

**File to create:** `app/engines/hybrid_reasoner.py`

```
Implement HybridReasoner for fast + deep architecture reasoning.

FUNCTIONALITY:
- Fast path: Return fast recommendation immediately if no risky decisions
- Deep path: For each risky decision, use Claude Sonnet 4 extended thinking
- Merge path: Combine fast + deep reasoning into final recommendation

CLAUDE SONNET 4 INTEGRATION:
- Model: claude-sonnet-4-20250514
- Use budget_tokens=5000-10000 for extended thinking
- Temperature=0.5 (balance creativity + consistency)
- Cache API key in Supabase Vault

HYBRID REASONING WORKFLOW:

def hybrid_reason(
    spec: RequirementSpec,
    fast_rec: StackRecommendation,
    risky_decisions: List[RiskyDecision]
) -> FinalArchitectureRecommendation:
    
    if not risky_decisions:
        # No risky decisions; return fast recommendation immediately
        return FinalArchitectureRecommendation.from_fast(fast_rec)
    
    # Deep think on risky decisions
    deep_thoughts = []
    for decision in risky_decisions:
        thinking_prompt = f"""
        Project: {spec.project_name}
        Requirement: {spec}
        
        Proposed tech stack: {fast_rec.tech_stack}
        
        Risky decision to revisit: {decision.decision_type}
        Reason it's risky: {decision.reason}
        
        Please think deeply about:
        1. Why the fast recommendation might fail
        2. Alternative approaches
        3. Pros/cons of each approach
        4. Recommendation on whether to stick with fast choice or pivot
        """
        
        response = await sonnet_extended_thinking(thinking_prompt)
        deep_thoughts.append((decision.decision_type, response))
    
    # Merge fast + deep
    final_recommendation = merge_recommendations(fast_rec, deep_thoughts)
    return final_recommendation

IMPLEMENTATION:
async def hybrid_reason(...) -> FinalArchitectureRecommendation

Include:
- OpenAI API integration with error handling
- Extended thinking prompt engineering
- Response parsing (extract JSON from thinking output)
- Caching strategy (don't re-think same decision)
- Timeout handling (fallback to fast if Sonnet is slow)
- Logging at each stage
- Unit tests with mocked Claude responses
- Integration tests with real API

PROMPT ENGINEERING:
Write thoughtful prompts that guide Claude to:
- Consider edge cases
- Think about failure modes
- Challenge assumptions
- Propose alternatives
- Be specific to this project

RESPONSE PARSING:
Claude will return structured thinking + recommendation.
Parse carefully to extract:
- Alternative tech stack suggestions
- Risk assessments
- Mitigation strategies
- Confidence level

CACHING:
Cache extended thinking responses in Supabase.
If same risky decision seen before, reuse cached reasoning.

PERFORMANCE:
- Fast path: < 100ms (no API calls)
- Deep path: 10-30s per risky decision (Sonnet 4 + thinking)
- Total: < 2 minutes for typical project

Make sure the deep reasoning actually improves on fast recommendation.
If it doesn't, bias toward fast (simpler is better).
```

---

## 🏛️ Prompt 9: Architecture Generator

**File to create:** `app/engines/architecture_generator.py`

```
Implement ArchitectureGenerator.

FUNCTIONALITY:
Takes hybrid reasoner output → produces full architecture with:
- Service map (services + dependencies)
- Data flows (how data moves)
- Tech stack (with rationale for each choice)
- ADRs (Architecture Decision Records)
- Estimated effort

ARCHITECTURE GENERATION PROCESS:

1. SERVICE DECOMPOSITION:
   - Based on domain + features, identify services to build
   - Use Claude API (fast, no extended thinking) to flesh out service descriptions
   - Return: List[Service]

2. DEPENDENCY GRAPH:
   - Build directed graph of service dependencies
   - Check for circular dependencies (should not exist)
   - Identify single points of failure
   - Return: DependencyGraph

3. DATA FLOWS:
   - For each service pair, define: "How does A talk to B?"
   - Synchronous (REST, gRPC)? Asynchronous (message queue)?
   - What data format? (JSON, Protobuf?)
   - Return: List[DataFlow]

4. ADRs (Architecture Decision Records):
   - For each major tech choice, explain:
     - What was chosen
     - What was rejected
     - Why this choice was better
     - Implications
   - Return: List[ADR]

5. TECH STACK RATIONALE:
   - Explain why each technology was chosen
   - Include alternatives considered
   - Document assumptions

6. EFFORT ESTIMATION:
   - Estimate weeks to build based on:
     - Service count
     - Team size
     - Complexity
   - Return: estimated_effort_weeks

IMPLEMENTATION:
async def generate(hybrid_recommendation: HybridRecommendation) -> Architecture:
    # Decompose into services
    services = await decompose_services(hybrid_recommendation)
    
    # Build dependency graph
    deps = build_dependency_graph(services)
    
    # Generate data flows
    flows = generate_data_flows(services, deps)
    
    # Generate ADRs
    adrs = await generate_adrs(hybrid_recommendation)
    
    # Estimate effort
    effort = estimate_effort(services, team_size)
    
    return Architecture(
        services=services,
        dependencies=deps,
        data_flows=flows,
        adrs=adrs,
        tech_stack=hybrid_recommendation.tech_stack,
        estimated_effort_weeks=effort
    )

VALIDATION:
- No circular dependencies (DAG check)
- All service dependencies are resolvable
- Tech stack is internally consistent
- Effort estimate is reasonable (1-52 weeks)

Include:
- Full docstrings
- Type hints
- Error handling (invalid graphs, etc.)
- Unit tests (mock services, dependencies)
- Integration tests
- Examples for each domain (microservices, ai_native, data_pipeline)

SERVICE TEMPLATES:
For each domain, pre-define common services:

Microservices:
- API Gateway
- Auth Service
- Business Logic Services (Product, Order, Payment, etc.)
- Database Layer
- Cache Layer
- Message Queue (optional)

AI-Native:
- API Gateway
- Auth Service
- LLM Interface Layer
- Vector DB Layer
- Memory/Reasoning Layer
- Async Job Queue

Data Pipeline:
- Data Ingestion
- Transformation/Processing
- Storage/Warehouse
- Monitoring/Alerting

Be specific and actionable. Each service should be ready to hand off to a coder.
```

---

## ⚠️ Prompt 10: Failure Mode Mapper

**File to create:** `app/engines/failure_mode_mapper.py`

```
Implement FailureModeMapper.

FUNCTIONALITY:
For each service in the architecture, identify top 3 failure modes.
For each failure mode, propose: detection strategy, mitigation strategy, fallback.

FAILURE MODE TAXONOMY:

For MICROSERVICES:
1. Service crash / unavailability
   - Mitigation: Health checks, auto-restart, replicas
   - Detection: /health endpoint returns 5xx
   - Fallback: Fallback to cached response or degraded mode

2. Network latency / timeout
   - Mitigation: Async processing, circuit breaker
   - Detection: Response time > threshold
   - Fallback: Retry with exponential backoff

3. Database connection exhaustion
   - Mitigation: Connection pooling, query optimization
   - Detection: Too many connections > limit
   - Fallback: Queue requests, wait for connection release

For AI-NATIVE:
1. Model inference timeout / hallucination
   - Mitigation: Inference timeout, validity checks
   - Detection: Response time > timeout OR confidence < threshold
   - Fallback: Fallback to simpler model, return previous cached response

2. Vector DB unavailability
   - Mitigation: Replicas, backup vector DB
   - Detection: Connection error to vector DB
   - Fallback: Return generic recommendations, no personalization

3. Token rate limit (API quota)
   - Mitigation: Rate limiting, queue system, batching
   - Detection: Rate limit error from OpenAI API
   - Fallback: Serve cached embeddings, delay non-critical requests

For DATA-PIPELINE:
1. Job failure / incomplete processing
   - Mitigation: Checkpointing, retries
   - Detection: Job did not complete within expected time
   - Fallback: Restart from last checkpoint, alert ops

2. Data quality issue (garbage in, garbage out)
   - Mitigation: Input validation, schema enforcement
   - Detection: Anomaly detection on data distribution
   - Fallback: Quarantine bad batch, investigate

3. Storage quota exceeded
   - Mitigation: Data archival, compression
   - Detection: Storage usage > 90% threshold
   - Fallback: Pause ingestion, archive old data

IMPLEMENTATION:
async def map_failure_modes(architecture: Architecture) -> Dict[str, List[FailureMode]]:
    modes_by_service = {}
    
    for service in architecture.services:
        modes = identify_failure_modes(service, architecture.domain)
        modes_by_service[service.id] = modes
    
    return modes_by_service

class FailureMode(BaseModel):
    mode: str  # "service crash", "timeout", etc.
    probability: Literal["high", "medium", "low"]
    impact: str  # "all requests fail", "slower response", etc.
    detection_strategy: str  # "health check endpoint", "timeout trigger", etc.
    mitigation_strategy: str  # "auto-restart", "circuit breaker", etc.
    fallback_strategy: str  # "cached response", "degraded mode", etc.
    owner: str  # which team owns monitoring this?
    severity: Literal["critical", "high", "medium"]

DOMAIN-AWARE ANALYSIS:
- Use domain classification to determine relevant failure modes
- Customize to specific tech stack (e.g., PostgreSQL-specific failures)
- Consider dependencies (if service A fails, what happens to B?)

Include:
- Comprehensive failure mode catalog
- Domain-specific identification logic
- Severity scoring
- Mitigation effectiveness rating
- Full test coverage
- Logging for transparency

Output should be actionable — a team can read it and say "yes, we need to handle that."
```

---

## 📋 Prompt 11: Implementation Planner

**File to create:** `app/engines/implementation_planner.py`

```
Implement ImplementationPlanner.

FUNCTIONALITY:
Breaks architecture into ordered implementation phases.
Respects dependencies, identifies parallelization opportunities, prioritizes critical path.

PHASING STRATEGY:

Phase 1: Foundations (always first)
- Infrastructure setup (deployment, monitoring, secrets management)
- Shared libraries (auth utilities, logging, error handling)
- Database setup

Phase 2: Critical path (what must work first)
- Services with no dependencies (or only depend on shared infra)
- Core business logic

Phase 3: Integrations (build on phase 2)
- Services that depend on phase 2 services

Phase 4: Advanced features (if time permits)
- Caching, monitoring, advanced scaling features

DEPENDENCY ANALYSIS:
- Build DAG of service dependencies
- Topological sort
- Identify longest critical path
- Find services that can be built in parallel

EXAMPLE:
Services: API Gateway, Auth, Product, Cart, Order, Payment
Dependencies:
  - Product → (nothing)
  - Cart → Product
  - Order → Cart, Auth
  - Payment → Order, Auth
  - API Gateway → (Product, Cart, Order, Payment, Auth)

Optimal phasing:
  Phase 1: Auth, Product (both have no dependencies)
  Phase 2: Cart (depends on Product from Phase 1)
  Phase 3: Order, Payment (both depend on previous phases)
  Phase 4: API Gateway (integrator, depends on everything)

PARALLELIZATION:
- Phase 1 services can be built in parallel
- Phase 2 services can be built in parallel (after Phase 1 done)
- Etc.

SPEC GENERATION:
Each phase gets a specification that's ready to hand to a developer:
- List of services to build
- Dependencies (what must be done first)
- API contracts (what each service must expose)
- Database schema (tables, relationships)
- Example requests/responses
- Error handling requirements

IMPLEMENTATION:
async def plan(architecture: Architecture) -> List[Phase]:
    # Build dependency graph
    deps = build_dependency_graph(architecture.services)
    
    # Topological sort
    sorted_services = topological_sort(deps)
    
    # Group into phases
    phases = group_into_phases(sorted_services, deps)
    
    # Generate specs for each phase
    for phase in phases:
        phase.spec_text = generate_phase_spec(phase, architecture)
    
    return phases

class Phase(BaseModel):
    phase_number: int
    name: str
    services_to_build: List[str]
    dependencies: List[int]  # which previous phases must complete first
    can_parallelize: bool  # can services within this phase be built in parallel
    priority: Literal["critical", "high", "medium"]
    duration_weeks: int  # estimated effort
    spec_text: str  # markdown spec ready for developer

SPEC CONTENT:
Each phase spec should include:
1. Overview: What's being built in this phase
2. Services: List of services with brief descriptions
3. Dependencies: What from previous phases is needed
4. API Contracts: OpenAPI spec (if REST) or proto file (if gRPC)
5. Database Schema: SQL DDL statements
6. Configuration: Environment variables, feature flags
7. Testing: Unit test requirements, integration test scenarios
8. Success Criteria: How to know this phase is done

Include:
- DAG validation (no cycles)
- Parallelization detection
- Critical path analysis
- Effort estimation per phase
- Full test coverage
- Examples

Phases should be actionable. A developer should be able to pick up a phase spec and start coding immediately.
```

---

## 🤖 Prompt 12: MCP Dispatcher

**File to create:** `app/engines/mcp_dispatcher.py`

```
Implement MCPDispatcher for sending phase specs to agents via MCP protocol.

FUNCTIONALITY:
Sends structured phase specifications to any agent via MCP (Model Context Protocol).
Tracks task status, collects outputs, handles retries.

MCP PROTOCOL BASICS:
- JSON-RPC 2.0 over HTTP
- Request: {"jsonrpc": "2.0", "id": ..., "method": "...", "params": {...}}
- Response: {"jsonrpc": "2.0", "id": ..., "result": {...}} or {"error": {...}}

DISPATCHER FLOW:

1. CREATE TASK:
   POST to mcp_agent_url/mcp
   {
     "jsonrpc": "2.0",
     "id": "task_123",
     "method": "tasks/create",
     "params": {
       "task_id": "arch-phase-1",
       "title": "Build Auth Service",
       "spec": "Full markdown spec...",
       "deadline": "2026-04-15T00:00:00Z",
       "requirements": {
         "language": "python",
         "framework": "fastapi",
         "database": "postgresql"
       }
     }
   }

2. POLL STATUS:
   Every 30s, check status:
   {
     "jsonrpc": "2.0",
     "id": "status_123",
     "method": "tasks/status",
     "params": {"task_id": "arch-phase-1"}
   }

3. GET RESULT:
   When completed:
   {
     "jsonrpc": "2.0",
     "id": "result_123",
     "method": "tasks/result",
     "params": {"task_id": "arch-phase-1"}
   }

IMPLEMENTATION:
class MCPDispatcher:
    async def dispatch(
        self,
        phase: Phase,
        mcp_agent_url: str,
        architecture: Architecture
    ) -> DispatchResult:
        # Create task via MCP
        task_id = await self.create_task(phase, mcp_agent_url, architecture)
        
        # Poll for completion
        result = await self.poll_until_complete(task_id, mcp_agent_url)
        
        # Validate output
        validation = await self.validate_output(result, phase, architecture)
        
        return DispatchResult(
            task_id=task_id,
            status="completed" or "failed",
            output_repo=result.get("output_repo"),
            validation_errors=validation.errors
        )

ASYNC POLLING:
async def poll_until_complete(self, task_id, mcp_url, timeout_minutes=60):
    start = datetime.now()
    while (datetime.now() - start).total_seconds() < timeout_minutes * 60:
        status = await self.check_status(task_id, mcp_url)
        
        if status.state == "completed":
            return await self.get_result(task_id, mcp_url)
        elif status.state == "failed":
            raise DispatchError(status.error)
        
        await asyncio.sleep(30)  # Check every 30 seconds
    
    raise TimeoutError(f"Task {task_id} did not complete within {timeout_minutes} minutes")

OUTPUT VALIDATION:
After agent completes, validate:
1. Repository URL is valid (GitHub/HF/etc.)
2. Code exists (clone and check)
3. Files are expected (openapi.yaml, requirements.txt, etc.)
4. Code compiles/imports without error
5. Database schema matches specification
6. API contracts match specification

DATABASE INTEGRATION:
Store in task_assignments table:
- task_id
- phase_number
- status (pending, dispatched, in_progress, completed, failed)
- output_repo_url
- validation_errors
- created_at, completed_at

Include:
- Full docstrings
- Error handling (network timeouts, agent errors)
- Retry logic (exponential backoff)
- Logging at each step
- Unit tests with mock MCP endpoints
- Integration tests with real agents (if possible)

CONFIGURATION:
Support multiple agent backends:
- Claude Code (via MCP server)
- Cursor (via MCP adapter)
- Codex (via MCP adapter)
- Custom agents (any MCP-compliant endpoint)

Be robust. Network calls can fail. Handle timeouts, connection errors, invalid responses gracefully.
```

---

## ✅ Prompt 13: Coherence Checker

**File to create:** `app/engines/coherence_checker.py`

```
Implement CoherenceChecker for validating service integration.

FUNCTIONALITY:
After agents complete phases, validate that generated services actually integrate:
1. API contracts match (what A calls on B matches what B provides)
2. Database schemas are compatible
3. Naming conventions are consistent
4. Message formats align

COHERENCE CHECKS:

1. API CONTRACT MATCHING:
   For each service dependency A → B:
   - Get A's OpenAPI spec or interface definition
   - Get B's OpenAPI spec or interface definition
   - Match endpoints that A calls on B
   - Verify request/response schemas match
   - Error if A expects endpoint that B doesn't provide

   Example:
   - A calls: POST /products?query=<str>
   - B provides: POST /products/search?q=<str>
   - Mismatch: query parameter name differs (query vs q)

2. DATABASE SCHEMA ALIGNMENT:
   For services sharing database tables:
   - Get schema from each service's migration files
   - Ensure column definitions match
   - Ensure constraints (primary key, foreign key) align
   - Error if A treats column as TEXT but B treats as INT

3. MESSAGE FORMAT CONSISTENCY:
   For async communication (message queues):
   - Get schema for messages produced by A
   - Get schema for messages consumed by B
   - Verify compatibility (if A produces JSON, B can parse it)
   - Check required fields align

4. NAMING CONVENTIONS:
   Check all services follow conventions:
   - Service names: snake_case (auth_service, product_service)
   - Database tables: plural snake_case (users, products)
   - API endpoints: kebab-case (/get-products, /create-order)
   - Environment variables: UPPER_SNAKE_CASE

IMPLEMENTATION:
async def check_coherence(
    phase_outputs: List[DispatchResult],
    architecture: Architecture
) -> CoherenceCheckResult:
    
    issues = []
    
    # Check 1: API contracts
    for service_pair in get_service_dependencies(architecture):
        api_issues = await check_api_contracts(
            service_pair.consumer,
            service_pair.provider,
            phase_outputs
        )
        issues.extend(api_issues)
    
    # Check 2: Database schemas
    for shared_table in get_shared_tables(architecture):
        schema_issues = await check_database_schemas(
            shared_table,
            phase_outputs
        )
        issues.extend(schema_issues)
    
    # Check 3: Message formats
    for message_flow in get_async_flows(architecture):
        message_issues = await check_message_formats(
            message_flow.producer,
            message_flow.consumer,
            phase_outputs
        )
        issues.extend(message_issues)
    
    # Check 4: Naming
    naming_issues = check_naming_conventions(phase_outputs)
    issues.extend(naming_issues)
    
    return CoherenceCheckResult(
        passed=len(issues) == 0,
        issues=issues,
        integration_score=calculate_score(issues)
    )

class CoherenceCheckResult(BaseModel):
    passed: bool
    issues: List[CoherenceIssue]
    warnings: List[str]
    integration_score: float  # 0.0-1.0
    affected_service_pairs: List[Tuple[str, str]]
    recommendation: str  # "Fix all issues", "Minor fixes needed", etc.

class CoherenceIssue(BaseModel):
    type: Literal["api_mismatch", "schema_mismatch", "message_mismatch", "naming"]
    severity: Literal["critical", "high", "medium", "low"]
    services_affected: List[str]
    description: str
    suggested_fix: str

HELPERS:

Helper: extract_openapi_spec(service_code: str) -> Dict:
    # Parse Python/Node code, extract FastAPI/Express routes
    # Return OpenAPI schema

Helper: extract_database_schema(migration_files: List[str]) -> Dict:
    # Parse SQL migrations
    # Return schema

Helper: extract_message_schema(producer_code: str, message_type: str) -> Dict:
    # Parse message definitions (Pydantic, TypeScript, etc.)
    # Return schema

Include:
- API spec parsing (FastAPI, Express, etc.)
- Database migration parsing (Alembic, Sequelize, etc.)
- Message schema parsing (JSON Schema, Protobuf)
- Detailed issue reporting
- Suggested fixes
- Full test coverage
- Integration tests

This is critical for ensuring multi-agent outputs actually work together.
Be thorough and helpful with suggestions.
```

---

## 📊 Prompt 14: OpenEnv Graders

**File to create:** `app/openenv/graders.py`

```
Implement the 3 OpenEnv graders for task evaluation.

TASK 1: STACK RECOMMENDATION GRADER
def grade_task_1(
    agent_recommendation: Dict[str, str],
    ground_truth: Dict[str, str]
) -> float:
    """
    Score: How well agent recommendation matches expert ground truth.
    
    Components to match: api_framework, database, cache_layer, 
                         message_queue, monitoring (5 total)
    
    Scoring:
    - 5/5 exact match: 1.0
    - 4/5 match: 0.8
    - 3/5 match: 0.6
    - 2/5 match: 0.4
    - 1/5 match: 0.2
    - 0/5 match: 0.0
    
    Use fuzzy matching for similar products:
    - "postgresql" ~ "postgres" ✓
    - "fastapi" ~ "starlette" ✗
    - "rabbitmq" ~ "amqp" ✗
    """
    
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

TASK 2: ANTI-PATTERN DETECTION GRADER
def grade_task_2(
    agent_findings: List[str],
    ground_truth_patterns: Dict[str, Dict]
) -> float:
    """
    Score: % of injected anti-patterns correctly identified.
    
    Scoring:
    - Found all patterns: 1.0
    - Found 2/3: 0.67
    - Found 1/3: 0.33
    - Found 0/3: 0.0
    
    Use keyword matching to detect if agent found each pattern.
    """
    
    found_count = 0
    
    for pattern_name, pattern_info in ground_truth_patterns.items():
        keywords = get_keywords_for_pattern(pattern_name)
        
        # Check if agent mentioned this pattern
        if any(
            keyword.lower() in agent_findings.lower()
            for keyword in keywords
        ):
            found_count += 1
    
    return found_count / len(ground_truth_patterns) if ground_truth_patterns else 0.0

TASK 3: FULL DESIGN INTEGRATION GRADER
def grade_task_3(
    architecture: Architecture,
    ground_truth_requirements: Dict
) -> float:
    """
    Composite score: 
    - Sensibility (30%): Does design make sense?
    - Decomposition (20%): Good service granularity?
    - Integration (40%): Do services actually integrate?
    - Failures (10%): Are failure modes covered?
    
    Total: 0.0-1.0
    """
    
    score = 0.0
    
    # 30% - Sensibility
    sensibility = evaluate_sensibility(architecture, ground_truth_requirements)
    score += 0.3 * sensibility
    
    # 20% - Decomposition quality
    decomposition = evaluate_decomposition(architecture.services)
    score += 0.2 * decomposition
    
    # 40% - Integration correctness
    integration = evaluate_integration(architecture)
    score += 0.4 * integration
    
    # 10% - Failure modes coverage
    failures = evaluate_failure_coverage(architecture)
    score += 0.1 * failures
    
    return min(1.0, max(0.0, score))

def evaluate_sensibility(arch: Architecture, requirements: Dict) -> float:
    # Does architecture match requirements?
    # - Latency req → caching strategy?
    # - Scale req → horizontal scaling support?
    # - Compliance req → encryption/auth?
    
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

def evaluate_decomposition(services: List[Service]) -> float:
    # Too few services: 0.3 (underdeveloped)
    # Too many services: 0.4 (over-engineered)
    # Just right: 1.0
    
    service_count = len(services)
    
    if service_count < 2:
        return 0.0  # Too simple
    elif service_count < 4:
        return 0.6  # Reasonable for small projects
    elif service_count <= 8:
        return 1.0  # Ideal range
    elif service_count <= 15:
        return 0.8  # A bit much, but okay
    else:
        return 0.4  # Way over-engineered

def evaluate_integration(arch: Architecture) -> float:
    # Check: Do all service pairs have defined APIs?
    integration_score = 0.0
    total_pairs = 0
    
    for service_a in arch.services:
        for dep_id in service_a.dependencies:
            service_b = find_service(arch.services, dep_id)
            
            api_match = validate_api_contract(service_a, service_b)
            schema_match = validate_schema_alignment(service_a, service_b)
            
            pair_score = (api_match + schema_match) / 2
            integration_score += pair_score
            total_pairs += 1
    
    if total_pairs == 0:
        return 1.0  # No dependencies = trivially integrated
    
    return integration_score / total_pairs

def evaluate_failure_coverage(arch: Architecture) -> float:
    # Does architecture identify failure modes?
    
    if not arch.failure_modes:
        return 0.0  # No failure modes = risk!
    
    # Check each service has >= 1 failure mode
    services_with_failures = len([
        s for s in arch.services
        if s.id in arch.failure_modes and arch.failure_modes[s.id]
    ])
    
    coverage = services_with_failures / len(arch.services)
    return coverage

Include:
- All 3 grader functions fully implemented
- Helper functions for scoring
- Test cases (ground truths) for each grader
- Scoring logic documentation
- Example inputs/outputs
- Unit tests for each grader
- Integration tests

Graders must be:
- DETERMINISTIC (same input → same output)
- REPRODUCIBLE (no randomness)
- OBJECTIVE (scores don't depend on opinions)
- FAIR (doesn't favor specific tech stacks)
```

---

## 🚀 Next Steps

**When you're ready to build:**

1. **Copy each prompt into Claude Code**
2. **Adjust paths/imports** for your project structure
3. **Run the build** (Claude Code will handle it)
4. **Test locally** with provided test cases
5. **Iterate** based on results

**Build order:**
1. Prompt 1: FastAPI scaffolding
2. Prompt 2: Pydantic models
3. Prompt 3: Requirements parser
4. Prompt 4: Domain classifier
5. Prompt 5-14: Engines in parallel (they're independent)

**Quality gates:**
- All tests pass
- Type hints everywhere
- Docstrings on all functions
- <100ms for fast path
- <30s for deep thinking path

Let me know when you're ready to start and I'll guide you through the first phase! 🚀
