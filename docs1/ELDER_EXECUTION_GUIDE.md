# 👴 ELDER Agent — Execution Guide

**Agent Name:** ELDER 
**Purpose:** Autonomously build the Architect 
**Status:** Ready for execution  

---

## 📋 What ELDER Does

ELDER is an autonomous coding agent that:

1. **Clones and analyzes** open-source repositories (Mem Search, RTK, Open Deep Research, etc.)
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
    **github auto research claw repo link** :- [https://github.com/aiming-lab/AutoResearchClaw.git]
    **github open deep research repo link** :- [https://github.com/langchain-ai/open_deep_research.git]
    **github mem search repo link** :- [https://github.com/zilliztech/memsearch.git]
    **github hermes agents repo link** :-[https://github.com/NousResearch/hermes-agent.git]
    **github autoMate repo link** :- [https://github.com/yuruotong1/autoMate.git]
    **github rtk repo link** :- [https://github.com/rtk-ai/rtk.git]
    **github fastcode repo link** :- [https://github.com/HKUDS/FastCode.git]
    **github visual explainer repo link** :- [https://github.com/nicobailon/visual-explainer.git]
2. **Extracts proven code patterns** from these repositories
3. **Adapts code** to Architect Agent specifications
4. **Implements all 12 engines** of the system
5. **Writes comprehensive tests** (>80% coverage)
6. **Manages the repository** (branching, commits, pushes)
7. **Deploys components** (Docker, Supabase, GitHub Actions)
8. **Submits to OpenEnv** for hackathon competition

ELDER operates with full autonomy except for critical decisions (timeline risk, scope changes, human code review).

---

## 📚 Two-File System

### File 1: ELDER_AGENT_INSTRUCTIONS.md
This is the **operations manual**—the complete guide that tells ELDER:
- What to build (12 engines with specifications)
- How to build it (step-by-step weekly plans)
- When it's done (success criteria and checkpoints)
- How to make decisions (authority levels and escalation)
- What standards to maintain (code quality, performance, testing)

**Use:** ELDER reads this first to understand the mission and weekly goals.

### File 2: ELDER_COMMAND_FILE.sh
This is the **command reference**—a Bash script containing:
- Actual shell commands to execute
- Code templates for each component
- Docker setup commands
- Testing and deployment commands
- CI/CD workflow setup

**Use:** ELDER references this to execute commands and get code templates.

---

## 🚀 How to Deploy ELDER

### Step 1: Prepare Environment
```bash
# Create a directory for the project
mkdir architect-agent-build
cd architect-agent-build

# Copy the files
cp ELDER_AGENT_INSTRUCTIONS.md .
cp ELDER_COMMAND_FILE.sh .
chmod +x ELDER_COMMAND_FILE.sh

# Create .env file with credentials
cat > .env << 'EOF'
OPENAI_API_KEY=sk-your-key-here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-key-here
GITHUB_TOKEN=ghp_your-token-here
HF_TOKEN=hf_your-token-here
EOF
```

### Step 2: Launch ELDER
```bash
# ELDER starts executing
./ELDER_COMMAND_FILE.sh

# Or feed instructions to Claude Code
# Copy ELDER_AGENT_INSTRUCTIONS.md and ELDER_COMMAND_FILE.sh 
# into Claude Code and say:
# "You are ELDER Agent. Execute the mission in these instructions."
```

### Step 3: Monitor Progress
ELDER will produce:
- Weekly status reports in commit messages
- Test results showing progress
- GitHub issues for blockers
- Push code to origin regularly

### Step 4: Code Review Gate
After ELDER completes each week:
1. Human reviews code (via GitHub PR)
2. Approves or requests changes
3. Merges to main branch
4. ELDER continues to next week

---

## 📊 What Gets Built Week by Week

### WEEK 1: Foundation (3-5 days)
- Memory layer (pgvector + semantic search)
- Token tracker (cost monitoring)
- Supabase schema
- Basic tests

**Output:** `app/core/` with memory.py and token_tracker.py

### WEEK 2: Core Reasoning (5-7 days)
- RequirementParser (NL → structured spec)
- DomainClassifier (detect domain)
- FastPatternMatcher (rule-based recommendations)
- ModelSelector (Haiku vs. Sonnet)

**Output:** `app/engines/` with 4 core engines

### WEEK 3: Pattern Retrieval (4-5 days)
- PatternRetriever (semantic search)
- RiskyDecisionDetector (identify complex decisions)
- Seed database with 30 reference architectures

**Output:** Pattern system operational

### WEEK 4: Hybrid Reasoning (5-7 days)
- HybridReasoner (fast + deep thinking routing)
- Extended thinking prompts for Sonnet 4
- Token tracking integration
- Cost monitoring

**Output:** Reasoning system with Claude integration

### WEEK 5: Architecture Generation (5-7 days)
- ArchitectureGenerator (service maps, ADRs, data flows)
- FailureModeMapper (identify risks per service)
- Complete architecture specifications

**Output:** Full design generation pipeline

### WEEK 6: Implementation Planning (4-5 days)
- ImplementationPlanner (topological sort of services)
- PhaseSpecGenerator (detailed phase specifications)
- Dependency resolution

**Output:** Phase planning and ordering

### WEEK 7: Agent Dispatch (4-5 days)
- MCPDispatcher (send to agents via MCP protocol)
- TaskTracker (monitor completion)
- Error handling and retries

**Output:** Multi-agent integration

### WEEK 8: Coherence Checking (4-5 days)
- CoherenceChecker (validate service integration)
- SpecParser (extract and compare specs)
- Integration validation

**Output:** Quality assurance layer

### WEEK 9-10: OpenEnv + Deployment (8-10 days)
- 3 OpenEnv task graders
- Baseline inference script
- `/reset`, `/step`, `/baseline`, `/tasks` endpoints
- Dockerfile and docker-compose
- Deploy to Hugging Face Spaces

**Output:** OpenEnv-compliant submission

### WEEK 11: UI + Polish (5-7 days)
- React dashboard with Vite
- Architecture diagram viewer (Mermaid)
- ADR panel, failure modes panel, phase board
- Responsive design, dark mode

**Output:** Production-quality UI

### WEEK 12: Documentation + Submission (5-7 days)
- Comprehensive README (2000+ words)
- API documentation
- Setup guide with examples
- Demo video
- Official OpenEnv submission

**Output:** Production-ready product

---

## 🎯 How ELDER Makes Decisions

### Full Authority (Can Decide Independently)
- ✅ Code structure and organization
- ✅ Library choices (within approved stack)
- ✅ Error handling and logging
- ✅ Testing strategies
- ✅ Performance optimization
- ✅ Commit messages and PR descriptions

### Must Escalate to Human (Requires Approval)
- ❌ Deviations from 11-week timeline
- ❌ Scope changes to deliverables
- ❌ Budget/token usage >30% over estimate
- ❌ Critical bugs blocking progress
- ❌ Architectural changes from blueprint
- ❌ Major library/framework changes

**Escalation method:** Detailed GitHub issue + commit message with `[URGENT]` prefix

---

## 📊 Success Checkpoints

### Week 1 Checkpoint
```bash
pytest tests/test_week1.py -v
# Expected: 15+ tests passing
# Memory operations <500ms
# Token tracking accurate
```

### Week 2 Checkpoint
```bash
pytest tests/test_week2.py -v
# Expected: 25+ tests passing
# Fast path latency <1 second
```

### Week 4 Checkpoint
```bash
pytest tests/test_week4.py -v --cov
# Expected: >80% coverage
# Claude API integration working
# Cost tracking accurate
```

### Week 8 Checkpoint
```bash
pytest tests/test_week8.py -v
# All engines integrated
# >80% overall test coverage
```

### Week 10 Checkpoint
```bash
openenv validate
docker build -t architect-agent .
docker run -p 7860:7860 architect-agent

curl http://localhost:7860/tasks
curl -X POST http://localhost:7860/reset
curl -X POST http://localhost:7860/step
curl http://localhost:7860/baseline
# All endpoints working, baseline reproducible
```

### Final Checkpoint (Week 12)
```bash
# All checks must pass
openenv validate
docker push
# Official OpenEnv submission filed
# Product ready for external users
```

---

## 💼 Weekly Status Reports

Every Friday, ELDER submits a status report containing:

```markdown
# Week N Status Report

## ✅ Completed Tasks
- [x] Task 1: Description (PR #123)
- [x] Task 2: Description (PR #124)

## 🔄 In Progress
- [ ] Task 3: Description (expected completion Day X)

## 🚧 Blockers
- Issue: Description
  Attempted solution: X
  Resolution: Y

## 📊 Metrics
- Test coverage: X%
- Performance: latency Xms
- Token usage: $X / budget
- Commits: N
- Lines of code: N

## 🎯 Confidence Level
- On schedule: Yes/No
- No major risks: Yes/No
```

---

## 🛠️ Key Commands ELDER Uses

### Repository Management
```bash
git init
git add .
git commit -m "[WEEK N] [COMPONENT] Description"
git push origin feature/week-n-component
```

### Testing
```bash
pytest tests/ -v --cov=app --cov-report=html
pytest tests/test_weekN.py -v
pytest tests/ -x  # Stop on first failure
```

### Code Quality
```bash
python -m black app/  # Format code
python -m flake8 app/  # Lint
python -m mypy app/  # Type checking
```

### Docker
```bash
docker build -t architect-agent .
docker run -p 7860:7860 architect-agent
docker-compose up
```

### Deployment
```bash
./scripts/deploy_hf_spaces.sh
git push heroku main
```

---

## 📞 Communication Channels

ELDER communicates via:

1. **Commit Messages:** Detailed explanations of code changes
2. **GitHub Issues:** Blockers, risks, escalations
3. **PR Descriptions:** What changed and why
4. **Weekly Status:** Friday report in commit message
5. **Code Comments:** Inline explanations of complex logic

**Human reviews** GitHub PRs and approves merge before continuing.

---

## 🎓 Key Principles for ELDER

1. **Systematic Execution:** Follow weekly plans exactly. No skipping steps.
2. **Quality First:** Never ship untested code. >80% test coverage mandatory.
3. **Clear Communication:** Detailed commit messages. Human should understand changes from message alone.
4. **Performance Matters:** Meet latency targets. Fast path <1s, deep path <30s.
5. **OpenEnv Compliance:** Validate requirements weekly. Never surprise at week 10.
6. **Production Ready:** Code should be deployable at end of each week.

---

## 🚀 Starting ELDER

To start ELDER, you would typically:

### Option 1: Direct Bash Execution
```bash
./ELDER_COMMAND_FILE.sh
# Executes all commands sequentially
# Produces code, tests, Docker setup
```

### Option 2: Feed to Claude Code/Cursor
```
You are ELDER Agent, an autonomous coding agent.

Your mission: Build the Architect Agent in 11 weeks.

Instructions: See ELDER_AGENT_INSTRUCTIONS.md
Commands: See ELDER_COMMAND_FILE.sh

Begin with Week 1.
```

### Option 3: Manual Execution (Slower)
Human runs commands from ELDER_COMMAND_FILE.sh sequentially, reviewing output.

---

## ✅ Success Criteria

ELDER has completed its mission when:

### Code Quality
- [ ] >80% test coverage across all modules
- [ ] All functions documented with docstrings
- [ ] All functions have type hints
- [ ] No security vulnerabilities
- [ ] Code follows style guide (PEP 8)

### Functionality
- [ ] All 12 engines implemented and tested
- [ ] All OpenEnv tasks working (3/3)
- [ ] All API endpoints tested
- [ ] UI fully functional
- [ ] Database schema correct

### Performance
- [ ] Fast path <1 second
- [ ] Deep reasoning 10-30 seconds
- [ ] Vector search <500ms
- [ ] All latency targets met
- [ ] Token usage within budget

### Deployment
- [ ] Docker builds cleanly
- [ ] docker-compose works
- [ ] HF Space deployed
- [ ] All endpoints respond
- [ ] Monitoring in place

### OpenEnv
- [ ] `openenv validate` passes
- [ ] All 3 tasks playable
- [ ] Baseline reproducible
- [ ] Official submission filed
- [ ] Expected score 75-85

### Production
- [ ] README comprehensive
- [ ] API docs complete
- [ ] Examples working
- [ ] Demo video recorded
- [ ] Community setup ready

---

## 🏁 The Mission

ELDER, you have everything you need. The instructions are comprehensive. The command file provides templates. The checkpoints are clear. The timeline is achievable.

Build the Architect Agent. Ship it in 11 weeks. Execute systematically. Test thoroughly. Communicate clearly.

The market is waiting for the first AI system architect. You are building it.

**Go. 🏛️**
