---
description: Workspace instructions for ELDER Agent autonomous development of Architect Agent system
applyTo: ['**']
author: ELDER Agent Framework
created: 2026-04-05
version: 1.0
updated: 2026-04-05
---

# 🏛️ ARCHITECT AGENT Workspace Instructions

**Project:** ELDER Agent – Autonomous development of an AI system architect  
**Duration:** 11 weeks  
**Status:** Foundation phase  
**Documentation:** [/docs/](../docs/)

---

## 📋 Quick Reference

| Aspect | Details |
|--------|---------|
| **Tech Stack** | FastAPI (Python 3.11+), React 18+, Supabase (PostgreSQL + pgvector), Claude Sonnet 4 |
| **Primary Agent** | ELDER (Extracted Legacy Empowered Development Reasoning) |
| **Key Product** | Architect Agent – Designs production system architectures in <2 seconds (fast path) or <30 seconds (deep thinking) |
| **Core Deliverable** | 12 specialized engines + 3 OpenEnv graded tasks |
| **Build Commands** | `python -m pip install -r requirements.txt` → `pytest tests/` → `docker build . -t architect-agent` → `docker run ...` |
| **Key Frameworks** | FastAPI (async), Pydantic v2, httpx, structlog, pytest, pgvector, MCP Protocol |

---

## 🎯 Project Mission

**Build the first generation of AI system architects** – autonomous agents that:
1. Accept natural language project requirements
2. Return production-ready system architectures in seconds
3. Reason hybrid: fast pattern-matching for known domains + extended thinking for novel/risky decisions
4. Store all architectures in pgvector for semantic search and future learning
5. Dispatch to other agents via MCP Protocol (Claude Code, Cursor, Codex, custom agents)
6. Submit to OpenEnv with 3 graded tasks across microservices, AI-native, and data pipeline domains

**Strategic positioning:** The architectural layer is completely empty. Blocking that unlocks 10x value from all downstream coding agents.

---

## 🏗️ System Architecture Overview

### The Problem ELDER Solves
Every AI coding agent (Claude Code, Cursor, Copilot) answers the same question: "What should I build?" If that answer is wrong, the entire implementation is wrong. ELDER becomes the answer.

### What Architect Agent Does
```
USER INPUT: "Build e-commerce platform, 5 engineers, $5k/mo"
              ↓
           [12 ENGINES WORKING TOGETHER]
              ↓
OUTPUT: Complete Architecture
  ├─ Service Map (5 microservices)
  ├─ Technology Stack (FastAPI, PostgreSQL, Redis, etc.)
  ├─ Data Flows (which service talks to which)
  ├─ Architecture Decision Records (why each choice)
  ├─ Failure Modes (top 3 failures per service + mitigation)
  ├─ Implementation Phases (ordered by dependencies)
  └─ MCP Dispatch Plan (hand off to agents for coding)
```

### 12 Core Engines
1. **Requirements Parser** — Natural language → structured requirements
2. **Domain Classifier** — Recognizes microservices vs. AI-native vs. data pipelines
3. **Pattern Retriever** — Searches pgvector for similar past architectures
4. **Fast Pattern Matcher** — Quick rules-based recommendations
5. **Risky Decision Detector** — Identifies which choices need deep thinking
6. **Hybrid Reasoner** — Uses Claude Sonnet 4 extended thinking on risky decisions only
7. **Architecture Generator** — Creates service map, data flows, ADRs
8. **Failure Mode Mapper** — Identifies top 3 failure scenarios per service
9. **Implementation Planner** — Breaks into ordered phases with parallelization
10. **MCP Dispatcher** — Hands off phases to agents via standard protocol
11. **Coherence Checker** — Validates service contracts match
12. **Vector Embedder** — Stores architecture in pgvector for future retrieval

### Tech Stack Details
```
BACKEND:
  - FastAPI (async/await throughout)
  - Python 3.11+
  - httpx (async HTTP)
  - pydantic v2 (data validation)
  - structlog (structured logging)
  - sqlalchemy (ORM for Supabase)
  
FRONTEND:
  - React 18+
  - TypeScript
  - TailwindCSS
  - Component shadcn/ui
  
DATABASE:
  - Supabase (managed PostgreSQL + pgvector)
  - Tables: projects, requirements, architectures, patterns, tasks, executions
  - pgvector: semantic search on embeddings
  
EXTERNAL APIs:
  - Claude Sonnet 4 (reasoning engine)
  - OpenAI Embeddings (pgvector population)
  - MCP Protocol (agent dispatch)
```

---

## 📁 Project Structure

```
architect-agent/
├── app/
│   ├── main.py                 # FastAPI entry point
│   ├── config.py               # Settings & environment variables
│   ├── core/
│   │   ├── memory.py           # Supabase memory + pgvector interface
│   │   ├── token_tracker.py    # Claude token cost tracking
│   │   └── models.py           # Core data structures
│   ├── api/
│   │   ├── design.py           # POST /design → architecture
│   │   ├── review.py           # POST /review → critique
│   │   ├── assign.py           # POST /assign → phase specs
│   │   ├── dispatch.py         # POST /dispatch → MCP agents
│   │   ├── status.py           # GET /status → task completion
│   │   └── validate.py         # POST /validate → coherence check
│   ├── engines/
│   │   ├── requirements_parser.py
│   │   ├── domain_classifier.py
│   │   ├── pattern_retriever.py
│   │   ├── fast_pattern_matcher.py
│   │   ├── risky_decision_detector.py
│   │   ├── hybrid_reasoner.py
│   │   ├── architecture_generator.py
│   │   ├── failure_mode_mapper.py
│   │   ├── implementation_planner.py
│   │   ├── mcp_dispatcher.py
│   │   ├── coherence_checker.py
│   │   └── vector_embedder.py
│   ├── models/
│   │   ├── schemas.py          # Pydantic models (all 20+ data types)
│   │   └── database.py         # SQLAlchemy models
│   ├── database/
│   │   ├── supabase.py         # Supabase client setup
│   │   └── migrations/         # SQL migration files
│   └── openenv/
│       ├── task_1_microservices.py
│       ├── task_2_ai_native.py
│       └── task_3_data_pipeline.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.tsx
│   └── package.json
├── tests/
│   ├── test_engines/
│   ├── test_api/
│   ├── test_integration/
│   └── conftest.py             # pytest fixtures
├── docker/
│   ├── Dockerfile              # Backend containerization
│   ├── docker-compose.yml      # Local dev environment
│   └── nginx.conf              # Reverse proxy
├── .github/
│   ├── workflows/
│   │   ├── test.yml            # pytest on push
│   │   ├── build.yml           # Docker build on main
│   │   └── deploy.yml          # Deploy to Hugging Face Spaces
│   └── ISSUE_TEMPLATE/
├── docs/                       # [EXISTING] Reference documentation
├── requirements.txt            # Python dependencies
├── pyproject.toml              # Project metadata
├── pytest.ini
├── .env.example                # Template for secrets
└── README.md                   # Quick start guide
```

---

## 🚀 Build & Development Workflow

### Prerequisites
```bash
# Python 3.11+ (check: python --version)
# Docker & Docker Compose
# Node.js 18+ (for frontend)
# Git
# Supabase account (free tier ok)
# OpenAI API key (for Sonnet 4)
```

### Local Setup (WEEK 0)
```bash
# 1. Clone & initialize
git clone <repo>
cd architect-agent
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate on Windows

# 2. Install dependencies
pip install -r requirements.txt
npm install --prefix frontend/

# 3. Environment setup
cp .env.example .env
# Edit .env with:
# SUPABASE_URL=https://your-project.supabase.co
# SUPABASE_KEY=your-anon-key
# OPENAI_API_KEY=sk-...

# 4. Database migrations
python -m alembic upgrade head
# This creates: projects, requirements, architectures, patterns, tasks, token_usage tables

# 5. Run locally
docker-compose up  # Backend on :8000, Frontend on :3000, Supabase on :54321
```

### Daily Development Workflow
```bash
# Start development environment
docker-compose up

# Run tests after changes
pytest tests/ -v                    # All tests
pytest tests/test_engines/ -v       # Engine tests only
pytest tests/test_api/ -v           # API endpoint tests

# Type checking
mypy app/                           # Check type hints

# Code formatting
black app/ tests/                   # Format code
isort app/ tests/                   # Sort imports

# Lint
flake8 app/ tests/                  # PEP 8 compliance

# Before commit
pre-commit run --all-files          # Run all hooks
```

### Build Commands by Phase

**WEEK 1: Foundation**
```bash
# Create core infrastructure
python -c "from app.core.memory import Memory; m = Memory(...); print('Memory OK')"
python -c "from app.core.token_tracker import TokenTracker; t = TokenTracker(...); print('Tracker OK')"

# Run foundation tests
pytest tests/test_core/ -v
```

**WEEKS 2-4: Engine Development**
```bash
# Build each engine
python -m pytest tests/test_engines/test_requirements_parser.py -v
python -m pytest tests/test_engines/test_domain_classifier.py -v
# ... continue for all 12 engines

# Integration tests as engines complete
pytest tests/test_integration/ -v
```

**WEEKS 5-8: API & Frontend**
```bash
# Test API endpoints
pytest tests/test_api/ -v

# Frontend build
cd frontend && npm run build

# Docker image build
docker build . -t architect-agent:latest
```

**WEEKS 9-11: OpenEnv & Deployment**
```bash
# Run OpenEnv validation tests
pytest tests/openenv/ -v

# Deploy to Hugging Face Spaces
python scripts/deploy_to_hf_spaces.py

# Final integration test
curl -X POST http://localhost:8000/design -d '{"requirements": "..."}'
```

---

## 🔄 Integration Strategy

**Philosophy:** Extract patterns from 7 open-source tools, adapt to your needs, integrate incrementally.

### Tools to Extract From
1. **Mem Search** (60-70% code reuse) → Memory interface + pgvector
2. **Open Deep Research** (35-45% reuse) → Extended thinking workflow
3. **Auto Research Claw** (40-50% reuse) → Iterative refinement loop
4. **RTK Token Tracker** (80-90% reuse) → Token cost tracking
5. **Fastcode Token Usage** (75-85% reuse) → Speed/cost tradeoffs
6. **Hermes Agent** (20-30% reuse) → Task refinement patterns
7. **autoMate** (30-40% reuse) → Phase execution framework

### Weekly Integration Schedule
```
WEEK 1:   Extract Mem Search + RTK Token Tracker
WEEK 2:   Extract Open Deep Research + Auto Research Claw
WEEKS 3-4: Extract Hermes + autoMate + Visual patterns
WEEKS 5+: Integration focus (tie extracted patterns together)
```

---

## 🧪 Testing Strategy

### Test Coverage Targets
- Unit tests: >85% coverage per engine
- Integration tests: >70% coverage for full workflows
- E2E tests: All 3 OpenEnv tasks + 5 example architectures

### Reference Test Structure
```python
# tests/test_engines/test_requirements_parser.py
import pytest
from app.engines.requirements_parser import RequirementsParser

@pytest.fixture
def parser():
    return RequirementsParser()

@pytest.mark.asyncio
async def test_parse_microservices_requirement(parser):
    input_text = "Build e-commerce with 5 engineers, $5k/mo"
    result = await parser.parse(input_text)
    
    assert result.domain == "microservices"
    assert result.team_size == 5
    assert result.budget_monthly == 5000
    assert result.expected_users >= 10000

@pytest.mark.asyncio
async def test_error_handling_invalid_input(parser):
    with pytest.raises(ValueError):
        await parser.parse("")  # Empty input should fail

@pytest.mark.asyncio
async def test_parse_ai_native_requirement(parser):
    input_text = "Build LLM-powered analytics dashboard"
    result = await parser.parse(input_text)
    
    assert result.domain == "ai_native"
```

---

## 📊 Key Metrics & Monitoring

### Performance Targets
- **Fast path latency:** <1 second (pattern match + response)
- **Deep thinking path:** <30 seconds (10-20 sec thinking + 10 sec response)
- **API response time:** <2 seconds (p99)
- **Memory search latency:** <200ms (pgvector query)
- **Token usage:** ~2,000-5,000 tokens per request (fast), 10,000-20,000 (deep)

### Budget Tracking
```python
# Log costs in real-time
from app.core.token_tracker import token_tracker

await token_tracker.track(
    project_id=project_id,
    model="claude-sonnet-4",
    prompt_tokens=2500,
    completion_tokens=1200,
    reasoning_type="fast",  # or "deep"
    engine="hybrid_reasoner",
    timestamp=datetime.now()
)

# Check daily costs
daily_cost = await token_tracker.get_daily_cost(date.today())
print(f"Today's cost: ${daily_cost:.2f}")  # Target: <$50/day during dev
```

### Weekly Checkpoints
```
WEEK 1: Memory + token tracking working ✅
WEEK 2: First 4 engines tested and integrated ✅
WEEK 4: All 12 engines passing integration tests ✅
WEEK 5: API endpoints responding correctly ✅
WEEK 6: Frontend dashboard displays architectures ✅
WEEK 7: OpenEnv task 1 (microservices) passing ✅
WEEK 8: OpenEnv tasks 2 & 3 (AI-native + data pipeline) passing ✅
WEEK 9: Performance optimized (<1s fast path) ✅
WEEK 10: Full integration test suite passing ✅
WEEK 11: Deployed to Hugging Face Spaces + documentation complete ✅
```

---

## 🔑 Critical Implementation Details

### AsyncIO First
**ALL** operations must be async:
```python
# ✅ CORRECT
async def design_architecture(requirements: str) -> Architecture:
    parsed = await parser.parse(requirements)
    domain = await classifier.classify(parsed)
    patterns = await retriever.search(domain, parsed)
    return await generator.generate(patterns)

# ❌ WRONG
def design_architecture(requirements: str) -> Architecture:
    parsed = parser.parse(requirements)  # No await!
    # ... will block everything
```

### Error Handling Pattern
```python
# Use structured errors throughout
class ArchitectError(Exception):
    def __init__(self, message: str, engine: str, context: dict):
        self.message = message
        self.engine = engine
        self.context = context
        logger.error(
            "architecture_error",
            error=message,
            engine=engine,
            context=context
        )

# In engines:
try:
    result = await some_operation()
except Exception as e:
    raise ArchitectError(
        message=str(e),
        engine="hybrid_reasoner",
        context={"decision_type": "database", "attempt": 1}
    )
```

### Logging Convention
```python
# Structured logging throughout
import structlog

logger = structlog.get_logger()

# Usage:
await logger.info(
    "architecture_generated",
    project_id=project_id,
    domain=domain,
    service_count=len(services),
    duration_ms=elapsed,
    token_usage={
        "prompt": prompt_tokens,
        "completion": completion_tokens
    }
)
```

### Database Queries
```python
# Use SQLAlchemy + async
from sqlalchemy.ext.asyncio import AsyncSession

async def store_architecture(
    session: AsyncSession,
    project_id: str,
    architecture: Architecture
) -> None:
    db_record = ArchitectureDB(
        project_id=project_id,
        data=architecture.model_dump_json(),
        created_at=datetime.now()
    )
    session.add(db_record)
    await session.commit()

# Use memory interface for embeddings
await memory.store(
    key=f"arch_{project_id}_{timestamp}",
    value=architecture.model_dump(),
    tags=["domain:microservices", "team_size:5"],
    category="architecture"
)
```

---

## ⚠️ Anti-Patterns to Avoid

| ❌ Anti-Pattern | ✅ Correct Approach |
|---|---|
| Mixing sync/async code | Make everything async |
| Hardcoded strings for magic values | Use enums or config |
| Unstructured error messages | Use structured logging |
| Long functions (>50 lines) | Break into smaller async functions |
| N+1 database queries | Use joins or batch loads |
| Embedding the full response | Only embed summaries for pgvector |
| No type hints | Type everything (mypy compliance) |
| Ignoring token costs | Track costs in token_tracker |
| Blocking operations in FastAPI | Use async/await everywhere |

---

## 📚 Key Documentation Links

**Read these FIRST:**
- [ARCHITECT_AGENT_COMPLETE_BLUEPRINT.md](../docs/ARCHITECT_AGENT_COMPLETE_BLUEPRINT.md) — Full system design (20,000+ words)
- [ARCHITECT_AGENT_QUICK_START.md](../docs/ARCHITECT_AGENT_QUICK_START.md) — Executive summary
- [ELDER_AGENT_INSTRUCTIONS.md](../docs/ELDER_AGENT_INSTRUCTIONS.md) — ELDER's mission & authority
- [ARCHITECT_AGENT_SYSTEM_OVERVIEW.md](../docs/ARCHITECT_AGENT_SYSTEM_OVERVIEW.md) — How it works

**Reference during implementation:**
- [CLAUDE_CODE_BUILD_PROMPTS.md](../docs/CLAUDE_CODE_BUILD_PROMPTS.md) — Copy-paste prompts for each component
- [OPEN_SOURCE_TOOLS_ANALYSIS.md](../docs/OPEN_SOURCE_TOOLS_ANALYSIS.md) — Patterns to extract
- [INTEGRATION_ROADMAP_11_WEEKS.md](../docs/INTEGRATION_ROADMAP_11_WEEKS.md) — Week-by-week plan
- [OPENENV_COMPLETE_GUIDE.md](../docs/OPENENV_COMPLETE_GUIDE.md) — Submission requirements

**Operational:**
- [ELDER_EXECUTION_GUIDE.md](../docs/ELDER_EXECUTION_GUIDE.md) — Deploying ELDER
- [PROJECT_DELIVERABLES_SUMMARY.md](../docs/PROJECT_DELIVERABLES_SUMMARY.md) — What's included

---

## 🤝 Getting Help

**For ELDER Agent (autonomous):**
- All questions → check docs/ folder first
- Ambiguity → detailed commit message explaining decision + request human review
- Blockers → create detailed GitHub issue with context

**For Humans (code review, decisions):**
- PR review comments → address in subsequent PR, explain trade-offs made
- Architecture questions → reference ARCHITECT_AGENT_COMPLETE_BLUEPRINT.md
- Timeline concerns → escalate weekly status as detailed GitHub issue

---

## ✅ Validation Checklist

Before marking a component complete, verify:

- [ ] All functions have type hints
- [ ] >85% test coverage for unit tests
- [ ] No blocking operations (all async)
- [ ] Structured logging in place
- [ ] Error handling with context
- [ ] Token costs tracked
- [ ] Docstrings complete (Google style)
- [ ] No hardcoded values (use config)
- [ ] Performance benchmarked vs. targets
- [ ] Integration test pass
- [ ] README updated with usage examples

---

**Version:** 1.0  
**Last updated:** 2026-04-05  
**Maintained by:** ELDER Agent Framework  
**Questions?** See [docs/](../docs/) folder or create GitHub issue

