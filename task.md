# ELDER Project Task List

**Last Updated:** 2026-04-07
**Status:** MVP Complete - Ready for OpenEnv Submission

---

## 🔴 HIGH PRIORITY

### Backend Issues
- [x] **[FIX-001]** `engines/model_selector.py` - Move `import os` to top of file
- [x] **[FIX-002]** `engines/domain_classifier.py` - Remove dead code
- [x] **[FIX-003-004]** `engines/coherence_checker.py` - Implement stubs
- [x] **[FIX-005]** `engines/mcp_dispatcher.py` - Make deadline configurable
- [x] **[FIX-006]** `engines/tech_research.py` - Add empty list guard
- [x] **[FIX-007]** `engines/deep_thinker.py` - Fix silent exception
- [x] **[FIX-008]** `engines/architecture_generator.py` - Fix type ignores
- [x] **[FIX-010]** `engines/llm_client.py` - Add error handling

### OpenEnv
- [x] **[OE-001]** Add 30 test cases to `openenv/test_cases.py`

### Frontend
- [x] **[FE-001]** Scaffold React app with Vite + TypeScript + Tailwind
- [x] **[FE-002-007]** All 6 React components built

### Deployment
- [x] **[DE-001-002]** Docker and docker-compose

---

## 🟡 MEDIUM PRIORITY

### Backend Fixes
- [x] **[FIX-009]** `engines/implementation_planner.py` - Improved fallbacks

### Database
- [x] **[DB-001-003]** Supabase migrations and seed data

### GitHub Actions
- [x] **[CI-001-003]** test.yml, lint.yml, deploy.yml

---

## 🟢 LOW PRIORITY

### Frontend Polish
- [x] **[FE-008]** Responsive design / mobile support
- [x] **[FE-009]** Dark mode support with toggle
- [x] **[FE-010]** Animations and transitions

### Documentation
- [x] **[DOC-001]** README.md (2000+ words)
- [x] **[DOC-002]** API.md documentation
- [x] **[DOC-003]** SETUP.md local development guide
- [x] **[DOC-004]** 5 worked examples in `examples/`

### OpenSource Integration
- [ ] **[OS-001]** Visual Explainer patterns for Mermaid

### OpenEnv Completion
- [x] **[OE-002]** baseline.py for scoring
- [ ] **[OE-003]** Deploy to Hugging Face Spaces
- [ ] **[OE-004]** Submit to OpenEnv

---

## ✅ COMPLETED

### Backend (14 engines + core)
- [x] All engine modules implemented and fixed
- [x] Core services: memory (pgvector), token_tracker
- [x] Models: All Pydantic schemas with proper types

### OpenEnv
- [x] 3 deterministic graders
- [x] 30 test cases (10 per task)
- [x] baseline.py for comparison

### Frontend
- [x] 6 React components (RequirementInput, ArchitectureViewer, ADRPanel, FailureModesPanel, PhaseBoard, DispatchPanel)
- [x] Dark/light mode toggle
- [x] Responsive design
- [x] Animations

### Infrastructure
- [x] Docker containers
- [x] docker-compose
- [x] CI/CD workflows
- [x] Supabase migrations

### Documentation
- [x] README.md
- [x] API.md
- [x] SETUP.md
- [x] 5 worked examples

---

## 📊 Statistics

| Category | Total | Completed | Remaining |
|----------|-------|-----------|-----------|
| HIGH | 12 | 12 | 0 |
| MEDIUM | 10 | 10 | 0 |
| LOW | 16 | 13 | 3 |
| **TOTAL** | **38** | **35** | **3** |

---

## 🚀 Remaining Tasks

1. **[OS-001]** Visual Explainer patterns (optional enhancement)
2. **[OE-003]** Deploy to HuggingFace Spaces (requires HF account setup)
3. **[OE-004]** Submit to OpenEnv (after deployment)

---

## 🔧 Fixes Applied

1. PATTERN_KEYWORDS export in graders.py
2. RiskyDecision schema with id, affected_component, decision_context
3. Removed duplicate folders (architect-agent-build, _source_repos)
4. 30 test cases (10 per OpenEnv task)
5. Improved implementation_planner.py with complexity-based fallbacks
6. Dark/light mode with persistence
7. Responsive design with mobile menu
8. Light theme Mermaid support
9. Download PNG for architecture diagrams
