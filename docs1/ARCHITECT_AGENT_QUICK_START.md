# 🏛️ ARCHITECT AGENT — Executive Summary & Quick Start

**Status:** Ready to Build  
**Timeline:** 12 weeks to full product + OpenEnv submission  
**Team:** You (solo, using Claude Code)  
**Goal:** Ship the first AI system architect, fill the empty architectural layer  

---

## 📌 What You're Building

An AI system architect that:
1. **Takes natural language requirements** → produces production-ready system architecture
2. **Thinks hybrid**: Fast pattern-match (instant) + deep reasoning on risky decisions (Claude Sonnet 4)
3. **Stores everything in Supabase** with pgvector for semantic search
4. **Dispatches to any agent via MCP** (Claude Code, Cursor, Codex, etc.)
5. **Submits 3 graded tasks to OpenEnv** hackathon

**Why this matters:**
- Every startup building multi-agent systems needs this
- No product exists in the "architectural AI" layer (completely empty)
- You're first to market
- 10x value multiplier for all downstream coding agents

---

## 🎯 What You're Delivering

### Full Product (Weeks 1-10)
- ✅ Core design engine (requirements → architecture)
- ✅ Hybrid reasoning (fast + deep thinking)
- ✅ 12 specialized engines (parser, classifier, matcher, reasoner, generator, etc.)
- ✅ Supabase storage + pgvector semantic search
- ✅ MCP dispatcher (send specs to any agent)
- ✅ Coherence checker (validate service integration)
- ✅ React UI dashboard
- ✅ API server (FastAPI)

### OpenEnv Submission (Weeks 8-12)
- ✅ 3 graded tasks:
  - Task 1 (Easy): Tech stack recommendation
  - Task 2 (Medium): Anti-pattern detection
  - Task 3 (Hard): Full system design + integration validation
- ✅ Docker containerization
- ✅ Hugging Face Space deployment
- ✅ Complete documentation

---

## 🛠️ Tech Stack (Locked In)

```
Frontend:      React 18 + TypeScript + Tailwind CSS + Shadcn/ui
Backend:       Python 3.11 + FastAPI + Pydantic v2
Database:      Supabase (PostgreSQL + pgvector + Vault)
AI/LLM:        OpenAI API (Claude Sonnet 4 for extended thinking)
Agent Dispatch: MCP Protocol (universal compatibility)
Deployment:    Docker + Hugging Face Spaces
CI/CD:         GitHub Actions
Development:   Claude Code (dogfooding) + Local FastAPI + React dev server
```

---

## 📋 Key Design Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Reasoning | Hybrid (fast + deep) | Fast pattern-match for 90% + reserve Claude tokens for truly novel decisions |
| Domain Support | All three (ambitious) | Makes OpenEnv stronger; can narrow if needed |
| Agent Dispatch | MCP Protocol | Universal; works with any agent |
| Vector DB | pgvector in Supabase | All-in-one; you know Supabase well |
| Grading | Deterministic rules | Repeatable; perfect for OpenEnv competitions |
| Deployment | HF Spaces | OpenEnv requirement; Docker makes it portable |

---

## 📅 12-Week Roadmap

### Phase 1: Foundation & Core Engine (Weeks 1-4)
**Deliverable:** CLI that takes requirements → recommends tech stack instantly

**Week 1-2:**
- [ ] Bootstrap FastAPI + React projects
- [ ] Set up Supabase (postgres + pgvector + vault)
- [ ] Build RequirementParser (NL → structured spec)
- [ ] Build DomainClassifier (detect domain)

**Week 3-4:**
- [ ] Build PatternRetriever (search pgvector)
- [ ] Build FastPatternMatcher (rule-based recommendations)
- [ ] Build RiskyDecisionDetector
- [ ] Test on 5 real project specs

**Deliverable Check:** 
```bash
curl -X POST http://localhost:8000/design -d '{...}'
# Returns: TechStackRecommendation in <1 second
```

---

### Phase 2: Deep Reasoning & Architecture Generation (Weeks 5-8)
**Deliverable:** Full `/design` endpoint that produces production-ready architectures

**Week 5-6:**
- [ ] Build HybridReasoner (fast path + Sonnet 4 extended thinking)
- [ ] Integrate OpenAI API (cache credentials in Supabase Vault)
- [ ] Tune prompt engineering
- [ ] Test on 10 project specs

**Week 7-8:**
- [ ] Build ArchitectureGenerator (service map, ADRs, data flows)
- [ ] Build FailureModeMapper (identify risks)
- [ ] Build ImplementationPlanner (topological sort → phases)
- [ ] Build VectorEmbedder (store in pgvector)

**Deliverable Check:**
```bash
curl -X POST http://localhost:8000/design -d '{...}'
# Returns: Full Architecture with services, ADRs, failure modes, phases
```

---

### Phase 3: Agent Dispatch & OpenEnv (Weeks 9-10)
**Deliverable:** OpenEnv-compliant environment with 3 graded tasks

**Week 9:**
- [ ] Build MCPDispatcher (send phase specs via MCP)
- [ ] Build CoherenceChecker (validate service integration)
- [ ] Build `/dispatch` endpoint with task tracking

**Week 10:**
- [ ] Implement 3 OpenEnv tasks + graders
- [ ] Implement `/reset`, `/step`, `/baseline`, `/tasks` endpoints
- [ ] Create test cases for each task
- [ ] Deploy to Hugging Face Spaces

**Deliverable Check:**
```bash
# Task 1: Easy
curl -X POST http://localhost:7860/reset -d '{"task_id": "task_stack_recommendation"}'
curl -X POST http://localhost:7860/step -d '{"action_type": "recommend_stack", ...}'

# Task 2: Medium
curl -X POST http://localhost:7860/reset -d '{"task_id": "task_anti_pattern_detection"}'

# Task 3: Hard
curl -X POST http://localhost:7860/reset -d '{"task_id": "task_full_design_integration"}'

# Baseline inference
curl http://localhost:7860/baseline
# Returns: {"task_stack_recommendation": 0.75, "task_anti_pattern_detection": 0.65, ...}
```

---

### Phase 4: UI & Polish (Weeks 11-12)
**Deliverable:** Full product ready for OpenEnv submission + external users

**Week 11:**
- [ ] Build React dashboard
  - [ ] Requirements input form
  - [ ] Architecture viewer (Mermaid diagrams)
  - [ ] ADR list display
  - [ ] Failure modes display
  - [ ] Phase board (Kanban)
  - [ ] Dispatch panel (agent status)

**Week 12:**
- [ ] Write comprehensive README
- [ ] Document API endpoints
- [ ] Create examples & tutorials
- [ ] Record demo video
- [ ] Submit to OpenEnv
- [ ] Deploy to production

---

## 🎯 OpenEnv Submission (3 Tasks)

### Task 1: Tech Stack Recommendation (Easy)
**Input:** Project requirements (team size, budget, scale, etc.)  
**Output:** Recommended tech stack (5 components)  
**Grader:** Fuzzy match to expert ground truth  
**Baseline Expected Score:** 0.75  

**Test Case Example:**
```json
{
  "domain": "microservices",
  "team_size": 2,
  "budget_usd": 5000,
  "expected_users": 10000,
  "latency_requirement_ms": 500
}

Expected output: {
  "api_framework": "fastapi",
  "database": "postgresql",
  "cache_layer": "redis",
  "message_queue": "none",
  "monitoring": "prometheus"
}
```

---

### Task 2: Anti-Pattern Detection (Medium)
**Input:** Architecture description + service dependency graph  
**Output:** List of detected anti-patterns  
**Grader:** % of injected anti-patterns found (0.0-1.0)  
**Baseline Expected Score:** 0.65  

**Anti-Patterns to Detect:**
- Circular dependencies
- Polyglot persistence mismatch
- Single points of failure
- N+1 query patterns
- Tight coupling (shared DB across services)

**Test Case Example:**
```json
{
  "services": ["auth", "product", "recommendation", "cart", "order"],
  "dependencies": {
    "auth": [],
    "product": ["recommendation"],
    "recommendation": ["product"],  // ← CIRCULAR!
    "cart": ["product"],
    "order": ["auth", "cart"]
  },
  "databases": {
    "auth": "postgresql",
    "product": "postgresql",
    "recommendation": "mongodb",  // ← MISMATCH
    "cart": "redis",
    "order": "postgresql"
  }
}

Ground truth injected patterns:
1. Circular: product → recommendation → product
2. Mismatch: cart (Redis, no ACID) + order (needs ACID) must be transactional
3. SPOF: auth service is critical path
```

---

### Task 3: Full Design with Integration (Hard)
**Input:** Natural language project requirements  
**Output:** Full Architecture + validated service integration  
**Grader:** Composite (sensibility 30% + decomposition 20% + integration 40% + failures 10%)  
**Baseline Expected Score:** 0.45  

**Test Case Example:**
```
Requirements: "Build AI-powered recommendation engine for e-commerce. 
100k users, <500ms latency, real-time inventory sync, async model 
retraining, PII compliant (GDPR)."

Domain: ai_native

Expected output:
- Service map: API Gateway → Product Service → Recommendation Service → Vector DB
- Tech stack: FastAPI, PostgreSQL, pgvector, Celery, etc.
- ADRs: Why recommendation is separate, why pgvector, etc.
- Failure modes: What if Vector DB is down? What if model training fails?
- Phases: Phase 1 (Auth, Product), Phase 2 (Recommendation), etc.

Grader checks:
- Does design make sense for requirements?
- Are services appropriately decomposed?
- Do service APIs actually match?
- Are failure modes identified?
```

---

## 🚀 How to Start Today

### Step 1: Clone & Setup (30 minutes)
```bash
git clone https://github.com/YOUR-USERNAME/architect-agent
cd architect-agent

# Create Python venv
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn pydantic httpx openai supabase-py python-dotenv

# Create React app
npx create-vite@latest frontend --template react-ts
cd frontend
npm install -D tailwindcss postcss autoprefixer
npm install zustand @tanstack/react-query mermaid shadcn-ui

# Back to root
cd ..

# Create .env file
cat > .env << EOF
OPENAI_API_KEY=sk-...
SUPABASE_URL=https://....supabase.co
SUPABASE_KEY=eyJ...
EOF
```

### Step 2: Bootstrap FastAPI (1 hour)
Use **Claude Code Prompt 1: FastAPI Backend Scaffolding**

Copy the prompt from `CLAUDE_CODE_BUILD_PROMPTS.md` into Claude Code:
```
Claude Code → "Create a production-ready FastAPI backend..."
```

Output: `app/main.py` with full FastAPI setup

Test:
```bash
python -m uvicorn app.main:app --reload
# Visit http://localhost:8000/docs
```

### Step 3: Define Models (1 hour)
Use **Claude Code Prompt 2: Pydantic Models**

Output: `app/models/schemas.py` with all data structures

### Step 4: Build Requirements Parser (2 hours)
Use **Claude Code Prompt 3: Requirements Parser Engine**

Output: `app/engines/requirement_parser.py`

Test:
```bash
python -c "
from app.engines.requirement_parser import parse
import asyncio

spec = asyncio.run(parse('We are 2 engineers building an AI recommendation engine...'))
print(spec)
"
```

### Step 5: Repeat for Each Engine (2 hours each)
Use prompts 4-14 in order. Each is independent; you can parallelize.

```
Week 1: Prompts 1-2 (scaffolding + models)
Week 1-2: Prompts 3-7 (parsing, classification, retrieval)
Week 2-3: Prompts 8-12 (reasoning, generation, dispatch)
Week 3: Prompt 13-14 (coherence, graders)
```

---

## 📊 How to Validate Progress

**After Week 2:** Fast path works
```bash
curl -X POST http://localhost:8000/design \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "E-commerce",
    "requirements_text": "2 engineers, $5k budget, 10k users..."
  }'

# Should return in <1 second with tech stack recommendation
```

**After Week 4:** Architecture generation works
```bash
curl -X POST http://localhost:8000/design \
  -H "Content-Type: application/json" \
  -d '{...}'

# Should return full Architecture with services, ADRs, failure modes, phases
# Latency: 10-30 seconds (with Sonnet 4 thinking)
```

**After Week 8:** Agent dispatch works
```bash
curl -X POST http://localhost:8000/dispatch \
  -H "Content-Type: application/json" \
  -d '{
    "architecture_id": "arch_123",
    "phase_number": 1,
    "mcp_agent_url": "http://agent-service/mcp"
  }'

# Should return task_id + status polling endpoint
```

**After Week 10:** OpenEnv tasks work
```bash
curl -X POST http://localhost:7860/reset -d '{"task_id": "task_stack_recommendation"}'
curl -X POST http://localhost:7860/step -d '{...}'
curl http://localhost:7860/baseline

# Should return scores for all 3 tasks, average baseline 0.60-0.70
```

---

## 🎓 Learning Path (If New to Architecture)

If you're unfamiliar with system design, study these first:

1. **Microservices patterns** (3 hours)
   - Read: "Building Microservices" by Newman (chapters 1-3)
   - Watch: "Microservices Architecture" (YouTube)

2. **AI-native systems** (2 hours)
   - Read: Your own OpenEnv ideas doc (Idea #7)
   - Study: Multi-agent orchestration patterns

3. **Data pipeline design** (2 hours)
   - Read: "Fundamentals of Data Engineering" (chapters 1-2)
   - Watch: Airflow tutorial

4. **Failure modes** (1 hour)
   - Read: "Release It!" by Michael Nygard (chapter 1)

**Total:** ~8 hours of reading. Then you're ready to build.

---

## 💡 Key Insights for Success

### 1. Fast Path Matters
Most requirements fit known patterns. Make that instant (<1s).
Deep thinking is for the 10% of novel decisions.
This hybrid approach means 10x better UX.

### 2. Determinism is Critical
For OpenEnv grading: same input must always produce same output.
No randomness. No "let's try a different temperature this time."
Encode everything into rules or Claude-determined templates.

### 3. Vector Search is Your Superpower
pgvector lets you find "similar architectures from the past."
This is 10x better than just rules.
Invest time in high-quality embeddings.

### 4. MCP Protocol is Key
Dispatch to ANY agent via standard protocol.
Claude Code, Cursor, Codex, custom agents — all work.
This makes you the hub of multi-agent workflows.

### 5. OpenEnv is Not the End
Winning OpenEnv opens doors.
Real product: paid SaaS for startups building multi-agent systems.
Pricing: Free (MVP) → $49/mo (Pro) → Enterprise.

---

## 🔄 Weekly Checklist

### Week 1 Checklist
- [ ] GitHub repo created
- [ ] FastAPI scaffolded
- [ ] Supabase setup (postgres + pgvector + vault)
- [ ] Requirements parser working
- [ ] Domain classifier working
- [ ] 5 test cases passing

### Week 2 Checklist
- [ ] Pattern retriever searching pgvector
- [ ] Fast pattern matcher working
- [ ] Risky decision detector working
- [ ] CLI test harness complete
- [ ] Latency targets met (<1s fast path)

### Week 3-4 Checklist
- [ ] Hybrid reasoner routing to Claude Sonnet 4
- [ ] Architecture generator producing valid output
- [ ] Failure mode mapper working
- [ ] Implementation planner creating phases
- [ ] Vector embedder storing in pgvector
- [ ] 10 real-world test cases passing

### Week 5-8 Checklist
- [ ] MCP dispatcher sending phase specs
- [ ] Coherence checker validating integration
- [ ] All 12 engines production-ready
- [ ] API spec complete (OpenAPI YAML)
- [ ] Docker builds and runs
- [ ] Performance benchmarks meeting targets

### Week 9-10 Checklist
- [ ] 3 OpenEnv tasks implemented
- [ ] Graders working deterministically
- [ ] `/reset`, `/step`, `/baseline`, `/tasks` endpoints
- [ ] Test cases created for each task
- [ ] Baseline inference reproducible
- [ ] Hugging Face Space deployed

### Week 11-12 Checklist
- [ ] React dashboard complete and polished
- [ ] README comprehensive
- [ ] Examples & tutorials written
- [ ] Demo video recorded
- [ ] OpenEnv submission ready
- [ ] Deployed to production

---

## 🚨 Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| **OpenAI API costs** | Budget $200/month; use caching + Claude token counters |
| **pgvector performance** | Index properly; test with 1000+ embeddings early |
| **MCP agent timeouts** | Set realistic timeouts (60 min); implement retries |
| **Scope creep** | Lock features; ruthlessly cut anything not essential for MVP |
| **OpenEnv evaluation bias** | Ensure graders are deterministic; test on 50+ cases |
| **Coherence checking is hard** | Start simple (API contracts only); expand later |

---

## 📞 Support & Resources

**When stuck:**
1. Check the detailed blueprint: `ARCHITECT_AGENT_COMPLETE_BLUEPRINT.md`
2. Check the Claude Code prompts: `CLAUDE_CODE_BUILD_PROMPTS.md`
3. Ask Claude Code directly (it's helping you build)
4. Reference OpenEnv documentation: https://github.com/huggingface/openenv

**Key docs to bookmark:**
- OpenAI API: https://platform.openai.com/docs
- Supabase: https://supabase.com/docs
- FastAPI: https://fastapi.tiangolo.com
- Pydantic: https://docs.pydantic.dev
- MCP Protocol: https://github.com/anthropics/mcp

---

## 🏆 Success Looks Like

**Week 4:** You have a CLI that takes requirements → recommends tech stack instantly.  
**Week 8:** You have a full API that designs complete architectures with Sonnet 4 thinking.  
**Week 10:** You have 3 graded OpenEnv tasks deployed to Hugging Face Space.  
**Week 12:** You have a polished, production-ready product ready to submit.  

**OpenEnv submission: 75-85 score expected** (first product in this layer, novel approach)

**Post-hackathon:** Launch paid beta with 10 startup customers → validate product-market fit → raise if needed

---

## 🚀 Ready to Ship

You have everything you need:
- ✅ Complete system design
- ✅ 14 Claude Code prompts (copy-paste ready)
- ✅ OpenEnv task specs
- ✅ 12-week roadmap
- ✅ Risk mitigations
- ✅ Success metrics

**Next step: Create the GitHub repo and run Claude Code Prompt 1.**

**Go build.** 🏛️
