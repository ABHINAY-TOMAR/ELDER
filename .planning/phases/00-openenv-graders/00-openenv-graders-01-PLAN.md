---
phase: 00-openenv-graders
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - app/openenv/graders.py
  - app/openenv/__init__.py
  - app/openenv/test_graders.py
autonomous: true
requirements: []
must_haves:
  truths:
    - "Graders produce consistent scores for identical inputs"
    - "Task 1 scores based on 5 component fuzzy matches (0.2 each)"
    - "Task 2 identifies anti-patterns via keyword matching"
    - "Task 3 composite score: sensibility 30%, decomposition 20%, integration 40%, failures 10%"
  artifacts:
    - path: "app/openenv/graders.py"
      provides: "All 3 grader functions + helper functions"
      exports: ["grade_task_1", "grade_task_2", "grade_task_3", "fuzzy_match", "get_keywords_for_pattern"]
    - path: "app/openenv/test_graders.py"
      provides: "Test suite verifying determinism"
  key_links:
    - from: "grade_task_1"
      to: "fuzzy_match"
      via: "Component scoring"
    - from: "grade_task_2"
      to: "get_keywords_for_pattern"
      via: "Keyword matching"
    - from: "grade_task_3"
      to: "evaluate_* functions"
      via: "Composite scoring"
---

<objective>
Create the OpenEnv grading system for evaluating AI agent outputs on 3 architecture tasks. Graders must be deterministic, reproducible, and objective.

Purpose: Enable fair, automated evaluation of agent recommendations across stack matching, anti-pattern detection, and full design integration.
Output: `app/openenv/graders.py` with all grading functions
</objective>

<execution_context>
@D:\ELDER\docs1\ARCHITECT_AGENT_COMPLETE_BLUEPRINT.md (lines 528-852 - Task grading specs)
@D:\ELDER\docs1\CLAUDE_CODE_BUILD_PROMPTS.md (lines 1221-1429 - Prompt 14 implementation)
</execution_context>

<context>
# OpenEnv Task Framework

## Task 1: Tech Stack Recommendation (Easy)
- 5 components: api_framework, database, cache_layer, message_queue, monitoring
- Weight: 0.2 each (total 1.0)
- Fuzzy matching for similar products

## Task 2: Anti-Pattern Detection (Medium)
- Detect: circular_dependency, polyglot_persistence, single_point_of_failure, n_plus_1_query, tight_coupling
- Keyword-based matching

## Task 3: Full Design Integration (Hard)
- Sensibility: 30%
- Decomposition: 20%
- Integration: 40%
- Failure coverage: 10%
</context>

<tasks>

<task type="auto">
  <name>Task 1: Create graders.py with Task 1 (Stack Recommendation)</name>
  <files>app/openenv/graders.py</files>
  <action>
Create `app/openenv/graders.py` with the following structure:

1. **fuzzy_match(a: str, b: str) -> float**:
   - Normalize both strings: lowercase, strip whitespace
   - Exact match: return 1.0
   - Fuzzy match using SequenceMatcher (Levenshtein-like):
     - If similarity >= 0.85: return similarity score
     - Else: return 0.0 (no partial credit for unrelated tech)
   - Handle "none"/"n/a" as equivalent to empty string (1.0 match)
   - Handle "postgres" ~ "postgresql" (0.9+ similarity)

2. **grade_task_1(agent_recommendation: Dict[str, str], ground_truth: Dict[str, str]) -> float**:
   - Components: api_framework, database, cache_layer, message_queue, monitoring
   - For each component: get agent_val and truth_val, apply fuzzy_match
   - Score = sum(weight * similarity) for each component
   - Clamp to [0.0, 1.0]
   - Example ground truth keys: "fastapi", "postgresql", "redis", "rabbitmq", "prometheus"

Include type hints and docstrings. No randomness - all operations deterministic.
  </action>
  <verify>python -c "from app.openenv.graders import grade_task_1, fuzzy_match; assert fuzzy_match('postgresql', 'postgres') > 0.85; assert grade_task_1({'api_framework': 'fastapi', 'database': 'postgresql', 'cache_layer': 'redis', 'message_queue': 'rabbitmq', 'monitoring': 'prometheus'}, {'api_framework': 'fastapi', 'database': 'postgresql', 'cache_layer': 'redis', 'message_queue': 'rabbitmq', 'monitoring': 'prometheus'}) == 1.0"</verify>
  <done>grade_task_1 returns score between 0.0-1.0 based on 5 component matches</done>
</task>

<task type="auto">
  <name>Task 2: Implement Task 2 (Anti-Pattern Detection) grader</name>
  <files>app/openenv/graders.py</files>
  <action>
Add to graders.py:

1. **get_keywords_for_pattern(pattern_name: str) -> List[str]**:
   Return keyword lists for each anti-pattern type:
   
   ```python
   PATTERN_KEYWORDS = {
       "circular_dependency": ["circular", "cycle", "dependency loop", "mutual dependency"],
       "polyglot_persistence_mismatch": ["polyglot", "persistence", "transaction", "acid mismatch", "redis", "mongodb"],
       "single_point_of_failure": ["single point", "bottleneck", "critical path", "all depend on"],
       "n_plus_1_query": ["n+1", "query", "loop within loop", "inefficient"],
       "tight_coupling": ["tight", "coupling", "shared database", "monolith"],
   }
   ```
   
   Return empty list if pattern_name not found.

2. **grade_task_2(agent_findings: List[str], ground_truth_patterns: Dict[str, Dict]) -> float**:
   - agent_findings: List of strings the agent identified (anti-pattern names/descriptions)
   - ground_truth_patterns: Dict mapping pattern_name -> {description, severity, services}
   - For each ground truth pattern:
     - Get keywords via get_keywords_for_pattern(pattern_name)
     - Check if any keyword appears in agent_findings (join as lowercase string)
     - found_count += 1 if any keyword matches
   - Score = found_count / len(ground_truth_patterns)
   - Handle empty ground_truth_patterns: return 0.0

Include comprehensive docstrings. Deterministic - no randomness.
  </action>
  <verify>python -c "from app.openenv.graders import grade_task_2, get_keywords_for_pattern; keywords = get_keywords_for_pattern('circular_dependency'); assert 'circular' in keywords; result = grade_task_2(['Found circular dependency between auth and product'], {'circular_dependency': {'services': ['auth', 'product']}}); assert result == 1.0"</verify>
  <done>grade_task_2 returns score based on % of patterns identified via keyword matching</done>
</task>

<task type="auto">
  <name>Task 3: Implement Task 3 (Full Design Integration) with helpers</name>
  <files>app/openenv/graders.py</files>
  <action>
Add to graders.py:

1. **evaluate_sensibility(architecture: Dict, requirements: Dict) -> float**:
   Score 0.0-1.0 based on:
   - 0.25: Latency requirement met (has caching if latency < 500ms)
   - 0.25: Scale requirement met (horizontal scaling support)
   - 0.25: PII/compliance requirement met (encryption/auth present)
   - 0.25: Monitoring present
   
   Check architecture dict fields: tech_stack, services, features

2. **evaluate_decomposition(services: List[Dict]) -> float**:
   Score based on service count:
   - < 2 services: 0.0 (too simple)
   - 2-3 services: 0.6 (reasonable for small)
   - 4-8 services: 1.0 (ideal range)
   - 9-15 services: 0.8 (a bit much)
   - > 15 services: 0.4 (over-engineered)

3. **evaluate_integration(architecture: Dict) -> float**:
   For each service with dependencies:
   - Check if API contracts defined between dependent services
   - Check if database schemas align for shared data
   - Score = matched pairs / total pairs (default 1.0 if no dependencies)

4. **evaluate_failure_coverage(architecture: Dict) -> float**:
   - If no failure_modes: return 0.0
   - coverage = services_with_failure_modes / total_services
   - Return coverage score

5. **grade_task_3(architecture: Dict, ground_truth: Dict) -> float**:
   Composite: 0.3*sensibility + 0.2*decomposition + 0.4*integration + 0.1*failures
   Clamp final score to [0.0, 1.0]

Include type hints, comprehensive docstrings. All deterministic.
  </action>
  <verify>python -c "
from app.openenv.graders import grade_task_3, evaluate_decomposition, evaluate_sensibility, evaluate_integration, evaluate_failure_coverage

# Test decomposition
assert evaluate_decomposition([{'id': 'a'}, {'id': 'b'}]) == 0.6
assert evaluate_decomposition([{'id': 'a'}, {'id': 'b'}, {'id': 'c'}, {'id': 'd'}]) == 1.0
assert evaluate_decomposition([{'id': str(i)} for i in range(20)]) == 0.4

# Test sensibility
arch = {'tech_stack': {'cache': 'redis', 'encryption': 'AES256'}, 'services': []}
req = {'latency_ms': 100, 'pii': True}
assert evaluate_sensibility(arch, req) > 0.5

# Test composite
result = grade_task_3({'services': [{'id': 'a'}, {'id': 'b'}], 'tech_stack': {}}, {})
assert 0.0 <= result <= 1.0
print('All Task 3 tests pass')
"</verify>
  <done>grade_task_3 returns composite score with 4 weighted sub-evaluations</done>
</task>

<task type="auto">
  <name>Task 4: Create test suite for determinism verification</name>
  <files>app/openenv/test_graders.py</files>
  <action>
Create `app/openenv/test_graders.py` with comprehensive tests:

1. **Test determinism**: Run each grader 3x with same input, assert same output
2. **Test Task 1**:
   - Exact match returns 1.0
   - Partial fuzzy match returns partial credit
   - Complete mismatch returns 0.0
   - Test postgres/postgresql equivalence
   - Test "none" equivalence
3. **Test Task 2**:
   - Found all patterns returns 1.0
   - Found none returns 0.0
   - Partial detection returns proportional score
4. **Test Task 3**:
   - All evaluate_* functions return 0.0-1.0
   - Composite scores weighted correctly
   - Edge cases (empty services, no failure modes)
5. **Test boundary conditions**:
   - Empty inputs
   - Missing keys in dicts
   - All graders return 0.0-1.0 range

Include pytest fixtures. Run with: pytest app/openenv/test_graders.py -v
  </action>
  <verify>pytest app/openenv/test_graders.py -v --tb=short</verify>
  <done>All tests pass, confirming determinism and correctness</done>
</task>

<task type="auto">
  <name>Task 5: Create __init__.py and verify imports</name>
  <files>app/openenv/__init__.py</files>
  <action>
Create `app/openenv/__init__.py`:

```python
"""OpenEnv grading system for Architect Agent evaluation."""

from app.openenv.graders import (
    grade_task_1,
    grade_task_2,
    grade_task_3,
    fuzzy_match,
    get_keywords_for_pattern,
    evaluate_sensibility,
    evaluate_decomposition,
    evaluate_integration,
    evaluate_failure_coverage,
)

__all__ = [
    "grade_task_1",
    "grade_task_2",
    "grade_task_3",
    "fuzzy_match",
    "get_keywords_for_pattern",
    "evaluate_sensibility",
    "evaluate_decomposition",
    "evaluate_integration",
    "evaluate_failure_coverage",
]
```

Verify: python -c "from app.openenv import grade_task_1, grade_task_2, grade_task_3; print('All imports successful')"
  </action>
  <verify>python -c "from app.openenv import *; print('Exports:', __all__)"</verify>
  <done>Module exports all grader functions for easy importing</done>
</task>

</tasks>

<verification>
- All graders return scores in [0.0, 1.0] range
- No randomness (no random module imports)
- Deterministic: same input → same output
- Type hints on all functions
- Docstrings on all functions
</verification>

<success_criteria>
1. `app/openenv/graders.py` exists with all 3 grader functions + helpers
2. `app/openenv/test_graders.py` exists with passing tests
3. `app/openenv/__init__.py` exports all functions
4. All pytest tests pass
5. Graders are 100% deterministic (no randomness)
</success_criteria>

<output>
After completion, create `.planning/phases/00-openenv-graders/00-openenv-graders-SUMMARY.md`
</output>
