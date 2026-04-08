# Graders Verification Report

**File:** `app/openenv/graders.py`
**Date:** 2026-04-07
**Status:** ISSUES FOUND

---

## Summary

| Check | Status |
|-------|--------|
| Task 1: 5 components with fuzzy matching, weights sum to 1.0 | ✅ PASS |
| Task 2: Anti-pattern detection via keyword matching | ❌ FAIL |
| Task 3: Composite formula (30%+20%+40%+10% = 100%) | ✅ PASS |
| All graders return 0.0-1.0 scores | ✅ PASS |
| Deterministic (no randomness) | ✅ PASS |

**Overall:** 4/5 checks pass. One blocker found.

---

## Detailed Findings

### ✅ Task 1 Grader (grade_task_1) - PASS

**Components verified:**
| Component | Weight | Status |
|-----------|--------|--------|
| api_framework | 0.2 | ✅ |
| database | 0.2 | ✅ |
| cache_layer | 0.2 | ✅ |
| message_queue | 0.2 | ✅ |
| monitoring | 0.2 | ✅ |
| **Total** | **1.0** | ✅ |

**Fuzzy matching:** Implemented via `fuzzy_match()` function (lines 10-45). Handles:
- Exact match → 1.0
- Substring containment → 1.0
- 12 synonym groups (PostgreSQL, Redis, Kafka, etc.)

**Score bounds:** Returns `min(1.0, max(0.0, score))` ✅

---

### ❌ Task 2 Grader (grade_task_2) - FAIL

**Issue:** Grader ignores per-test-case keywords from `ground_truth_patterns`

**Current behavior:**
```python
def grade_task_2(agent_findings: str, ground_truth_patterns: Dict[str, Dict]) -> float:
    for pattern_name, pattern_info in ground_truth_patterns.items():
        keywords = get_keywords_for_pattern(pattern_name)  # Uses HARDCODED mapping
```

The `get_keywords_for_pattern()` function uses a static dictionary (lines 48-60), but each test case defines its own keywords:

**Example from test_cases.py (lines 78-82):**
```python
"circular_dependency": {
    "severity": "critical",
    "description": "...",
    "keywords": ["circular", "cycle", "loop", "product → recommendation", "recommendation → product"]
}
```

**Problem:** The test case includes specific direction keywords (`"product → recommendation"`, `"recommendation → product"`), but the grader's hardcoded mapping only contains:
```python
"circular_dependency": ["circular", "cycle", "loop", "cyclic"]
```

**Impact:** 
- An agent that correctly identifies the circular dependency direction would NOT get full credit
- The grader cannot use test-specific keyword hints
- Poor alignment between test definition and grading logic

**Fix required:** Use `pattern_info.get("keywords", get_keywords_for_pattern(pattern_name))` instead of always using the hardcoded mapping.

---

### ✅ Task 3 Grader (grade_task_3) - PASS

**Composite formula verified:**
```python
sensibility     = evaluate_sensibility(...)      * 0.30
decomposition   = evaluate_decomposition(...)   * 0.20
integration     = evaluate_integration(...)     * 0.40
failures        = evaluate_failure_coverage(...) * 0.10
# Total: 0.30 + 0.20 + 0.40 + 0.10 = 1.0 ✅
```

**Component breakdown:**
| Component | Weight | Function |
|-----------|--------|----------|
| Architecture sensibility | 30% | `evaluate_sensibility()` |
| Service decomposition | 20% | `evaluate_decomposition()` |
| Integration correctness | 40% | `evaluate_integration()` |
| Failure modes coverage | 10% | `evaluate_failure_coverage()` |

**Score bounds:** Returns `min(1.0, max(0.0, score))` ✅

---

### ✅ Score Bounds - PASS

All graders properly clamp output:

| Function | Clamping | Line |
|----------|----------|------|
| `grade_task_1` | `min(1.0, max(0.0, score))` | 105 |
| `grade_task_2` | `found_count / len(patterns)` (naturally 0-1) | 138 |
| `grade_task_3` | `min(1.0, max(0.0, score))` | 274 |

---

### ✅ Determinism - PASS

**No random sources found:**
- No `random.*` calls in grader functions
- No time-based calculations
- All operations are pure function of inputs
- Exception: `get_random_test_case()` uses `random.choice()` but is NOT a grader function

---

## Issues

### Blocker #1: Task 2 ignores test-specific keywords

**Dimension:** Requirement Coverage
**Severity:** Blocker
**Description:** `grade_task_2()` uses hardcoded keyword mapping from `get_keywords_for_pattern()` instead of using keywords defined in each test case's `ground_truth_patterns`

**Evidence:**
- `test_cases.py` lines 78-92 define per-test keywords including direction-specific terms
- `graders.py` line 133 calls `get_keywords_for_pattern(pattern_name)` which ignores `pattern_info["keywords"]`
- Test case keyword `"product → recommendation"` not checked by grader

**Fix hint:** Change line 133 from:
```python
keywords = get_keywords_for_pattern(pattern_name)
```
to:
```python
keywords = pattern_info.get("keywords") or get_keywords_for_pattern(pattern_name)
```

This preserves fallback to hardcoded mapping while prioritizing test-specific keywords.

---

## Verification Checklist

- [x] Task 1: 5 components present
- [x] Task 1: Each weight is 0.2
- [x] Task 1: Total weight = 1.0
- [x] Task 1: Fuzzy matching implemented
- [x] Task 2: Uses keyword matching
- [x] Task 2: Keyword source verified (ISSUE FOUND)
- [x] Task 3: Sensibility 30%
- [x] Task 3: Decomposition 20%
- [x] Task 3: Integration 40%
- [x] Task 3: Failure coverage 10%
- [x] Task 3: Weights sum to 100%
- [x] All graders clamp 0.0-1.0
- [x] No random calls in graders
