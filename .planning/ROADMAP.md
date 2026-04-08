# OpenEnv Grading System Roadmap

## Project Overview

**Core Value:** Build an OpenEnv grading system that scores agent performance across 3 tasks with deterministic, reproducible results (0.0-1.0 range).

**Deliverables:**
- `app/openenv/graders.py` - Three grading functions
- `app/openenv/test_cases.py` - Test cases for each task
- `app/main.py` - `/reset` and `/step` endpoints wired up

---

## Phases

- [ ] **Phase 1: Graders** - Create graders.py with grade_task_1, grade_task_2, grade_task_3
- [ ] **Phase 2: Test Cases** - Create test_cases.py with 2+ test cases per task
- [ ] **Phase 3: API Endpoints** - Update main.py with /reset and /step endpoints
- [ ] **Phase 4: Integration Testing** - End-to-end testing of the grading system

---

## Phase Details

### Phase 1: Graders

**Goal:** Agent performance can be objectively scored on all 3 tasks

**Depends on:** Nothing (first phase)

**Requirements:** GRAD-01, GRAD-02, GRAD-03

**Success Criteria** (what must be TRUE):
1. `grade_task_1()` returns a float between 0.0 and 1.0
2. `grade_task_2()` returns a float between 0.0 and 1.0
3. `grade_task_3()` returns a float between 0.0 and 1.0
4. Same agent output produces same score on multiple calls (deterministic)
5. Each grader accepts task-specific input and ground truth

**Plans:** TBD

---

### Phase 2: Test Cases

**Goal:** Graders are validated with known inputs and expected outputs

**Depends on:** Phase 1

**Requirements:** TEST-01, TEST-02, TEST-03

**Success Criteria** (what must be TRUE):
1. At least 2 test cases exist for task 1 with known expected scores
2. At least 2 test cases exist for task 2 with known expected scores
3. At least 2 test cases exist for task 3 with known expected scores
4. All test cases pass when run with `pytest`
5. Test cases cover edge cases (e.g., perfect score, zero score, partial credit)

**Plans:** TBD

---

### Phase 3: API Endpoints

**Goal:** Grading system is accessible via HTTP POST endpoints

**Depends on:** Phase 1, Phase 2

**Requirements:** API-01, API-02

**Success Criteria** (what must be TRUE):
1. POST `/reset` with `task_id` returns initial observation for that task
2. POST `/step` with `action` returns observation, reward, done flag, and info
3. `/reset` fails gracefully with invalid task_id (400 response)
4. `/step` fails gracefully with invalid action (400 response)
5. Environment state persists correctly between calls

**Plans:** TBD

---

### Phase 4: Integration Testing

**Goal:** Full grading workflow works end-to-end

**Depends on:** Phase 3

**Requirements:** INT-01, INT-02

**Success Criteria** (what must be TRUE):
1. Complete episode (reset → step × N → final score) works without errors
2. Grading scores match expected values from test cases
3. All 3 tasks can be run through the API workflow
4. No memory leaks or state corruption across multiple episodes

**Plans:** TBD

---

## Progress Table

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Graders | 0/5 | Not started | - |
| 2. Test Cases | 0/5 | Not started | - |
| 3. API Endpoints | 0/5 | Not started | - |
| 4. Integration Testing | 0/4 | Not started | - |

---

## Requirements Traceability

| Requirement | Phase | Description |
|-------------|-------|-------------|
| GRAD-01 | Phase 1 | `grade_task_1()` returns 0.0-1.0 score |
| GRAD-02 | Phase 1 | `grade_task_2()` returns 0.0-1.0 score |
| GRAD-03 | Phase 1 | `grade_task_3()` returns 0.0-1.0 score |
| TEST-01 | Phase 2 | 2+ test cases for task 1 |
| TEST-02 | Phase 2 | 2+ test cases for task 2 |
| TEST-03 | Phase 2 | 2+ test cases for task 3 |
| API-01 | Phase 3 | `/reset` endpoint functional |
| API-02 | Phase 3 | `/step` endpoint functional |
| INT-01 | Phase 4 | Full episode workflow works |
| INT-02 | Phase 4 | Scores match expected values |

**Coverage:** 10/10 requirements mapped ✓

---

## Notes

- Graders must be deterministic: same input → same output every time
- Scores must be meaningful (not always 0.5 or 1.0)
- OpenEnv spec compliance required for final submission
