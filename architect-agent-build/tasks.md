# 📋 Architect Agent — Task Tracking

## 🏗️ Phase 1: Foundation & Core Engine (Weeks 1-4)

### Week 1: Foundation + Memory Layer (Current)
- [x] Initialize Project Structure (`app/`, `app/core/`, `tests/`)
- [x] Implement `ArchitectMemory` (with chunking and compaction)
- [x] Implement `ArchitectTokenTracker` (with pricing and stats)
- [ ] Execute Supabase SQL Schema (Tables: `architect_memory`, `token_usage`, RPC: `match_architect_memory`)
- [ ] Fix and Verify Test Suite (`tests/test_week1.py`)
- [ ] Create `docs/memory_layer.md`
- [ ] Create `docs/token_tracking.md`

### Week 2: Core Reasoning Engines
- [ ] Implement `RequirementSpec` Pydantic models
- [ ] Implement `RequirementParser` (NL -> Structured)
- [ ] Implement `DomainClassifier` (detect domain)
- [ ] Implement `FastPatternMatcher` (rule-based)
- [ ] Implement `ModelSelector`
- [ ] Create `tests/test_week2.py`

### Week 3: Pattern Retrieval + Risk Detection
- [ ] Implement `PatternRetriever` (pgvector search)
- [ ] Implement `RiskyDecisionDetector`
- [ ] Seed `data/reference_architectures/` (30 JSON files)
- [ ] Create `tests/test_week3.py`

### Week 4: Hybrid Reasoning + Extended Thinking
- [ ] Implement `HybridReasoner` (fast vs deep routing)
- [ ] Implement OpenAI/Claude Integration with retry logic
- [ ] Create Reasoning Prompts in `app/data/prompts/`
- [ ] Create `tests/test_week4.py`

---

## 🛠️ Bugs & Improvements
- [ ] **Bug:** `unittest` fails to find modules when run from root.
- [ ] **Improvement:** Add automated SQL migration script for Supabase.
- [ ] **Enhancement:** Add more detailed pricing for DeepSeek and o1 models.
- [ ] **Refactor:** Ensure `httpx` clients are reused in `ArchitectMemory`.
