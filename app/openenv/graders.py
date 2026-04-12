from typing import Any, Dict, List

from app.models.architecture import Architecture


EPSILON = 1e-6


def _strict_unit_interval(score: float) -> float:
    return min(1.0 - EPSILON, max(EPSILON, float(score)))


def _normalize_text(value: Any) -> str:
    return str(value or "").strip().lower()


def fuzzy_match(candidate: str, expected: str) -> float:
    candidate_norm = _normalize_text(candidate)
    expected_norm = _normalize_text(expected)
    if not candidate_norm or not expected_norm:
        return 0.0
    if candidate_norm == expected_norm:
        return 1.0
    if candidate_norm in expected_norm or expected_norm in candidate_norm:
        return 0.7

    synonyms = [
        {"postgres", "postgresql", "pg"},
        {"redis", "memcached"},
        {"rabbitmq", "amqp"},
        {"kafka", "confluent"},
        {"fastapi", "flask", "django", "starlette"},
        {"prometheus", "grafana", "datadog"},
    ]
    for group in synonyms:
        if candidate_norm in group and expected_norm in group:
            return 0.8
    return 0.0


class OpenEnvGraders:
    """Deterministic OpenEnv graders with partial-credit scoring."""

    def grade_tech_stack(self, agent_rec: Dict[str, str], ground_truth: Dict[str, str]) -> float:
        aliases = {
            "cache": "cache_layer",
            "cache_layer": "cache_layer",
            "api": "api_framework",
            "monitor": "monitoring",
        }
        canonical_agent: Dict[str, str] = {}
        for key, value in (agent_rec or {}).items():
            canonical_agent[aliases.get(key, key)] = value

        keys = ["api_framework", "database", "cache_layer", "message_queue", "monitoring"]
        component_scores = [
            fuzzy_match(canonical_agent.get(key, ""), ground_truth.get(key, ""))
            for key in keys
        ]
        raw = sum(component_scores) / len(keys)
        return _strict_unit_interval(raw)

    def grade_anti_patterns(self, agent_findings: List[str], ground_truth_patterns: Dict[str, Dict[str, Any]]) -> float:
        if not ground_truth_patterns:
            return _strict_unit_interval(0.5)

        findings_blob = _normalize_text(" ".join(agent_findings or []))
        if not findings_blob:
            return _strict_unit_interval(0.0)

        found = 0
        for pattern_name, pattern_info in ground_truth_patterns.items():
            default_keywords = [_normalize_text(pattern_name).replace("_", " ")]
            keywords = [_normalize_text(k) for k in (pattern_info.get("keywords") or default_keywords)]
            if any(keyword and keyword in findings_blob for keyword in keywords):
                found += 1

        raw = found / max(len(ground_truth_patterns), 1)
        return _strict_unit_interval(raw)

    def grade_full_design(self, arch: Architecture, ground_truth_reqs: Dict[str, Any]) -> float:
        required_services = [_normalize_text(s) for s in ground_truth_reqs.get("required_services", [])]
        required_integrations = [_normalize_text(i) for i in ground_truth_reqs.get("required_integrations", [])]
        required_failures = [_normalize_text(f) for f in ground_truth_reqs.get("required_failure_modes", [])]

        service_names = [_normalize_text(s.name) for s in arch.services]
        failure_modes = [_normalize_text(f.mode) for f in arch.failure_modes]

        required_service_hits = 0
        for token in required_services:
            if any(token in candidate for candidate in service_names):
                required_service_hits += 1
        service_coverage = required_service_hits / max(len(required_services), 1)

        integration_hits = 0
        for integration in required_integrations:
            parts = [p.strip() for p in integration.split("→") if p.strip()]
            if len(parts) < 2:
                continue
            src, dst = parts[0], parts[-1]
            if any(src in s for s in service_names) and any(dst in s for s in service_names):
                integration_hits += 1
        integration_coverage = integration_hits / max(len(required_integrations), 1)

        failure_hits = 0
        for token in required_failures:
            if any(token in failure for failure in failure_modes):
                failure_hits += 1
        failure_coverage = failure_hits / max(len(required_failures), 1)

        size_score = 1.0 if 3 <= len(arch.services) <= 12 else 0.5

        raw = (
            (service_coverage * 0.45)
            + (integration_coverage * 0.30)
            + (failure_coverage * 0.20)
            + (size_score * 0.05)
        )
        return _strict_unit_interval(raw)
