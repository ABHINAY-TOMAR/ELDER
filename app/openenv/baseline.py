"""
Baseline agent implementation for OpenEnv evaluation.

This module provides a simple rule-based baseline that demonstrates
acceptable performance for each of the three tasks:
1. Stack recommendation
2. Anti-pattern detection
3. Full design integration

The baseline uses simple heuristics and pattern matching to generate
reasonable but not optimal solutions.
"""

import re
from typing import Dict, Any, List, Optional
from app.models.schemas import Architecture, Service, ADR, FailureMode


class BaselineAgent:
    """Simple rule-based baseline agent for architecture tasks."""

    def __init__(self):
        self.domain_rules = {
            "microservices": {
                "api_framework": "fastapi",
                "database": "postgresql",
                "cache_layer": "redis",
                "message_queue": "rabbitmq",
                "monitoring": "prometheus"
            },
            "ai_native": {
                "api_framework": "fastapi",
                "database": "supabase",
                "cache_layer": "redis",
                "message_queue": "none",
                "monitoring": "prometheus"
            },
            "data_pipeline": {
                "api_framework": "none",
                "database": "postgresql",
                "cache_layer": "none",
                "message_queue": "kafka",
                "monitoring": "airflow"
            }
        }

        self.budget_thresholds = {
            "low": 5000,
            "medium": 25000,
            "high": 100000
        }

        self.user_scale_rules = {
            "small": (0, 10000),
            "medium": (10000, 100000),
            "large": (100000, 1000000),
            "massive": (1000000, float("inf"))
        }

    def select_stack(self, requirements: Dict[str, Any]) -> Dict[str, str]:
        """Select tech stack based on requirements."""
        domain = requirements.get("domain", "microservices")
        budget = requirements.get("budget_usd", 10000)
        users = requirements.get("expected_users", 1000)
        latency = requirements.get("latency_requirement_ms", 1000)
        pii = requirements.get("data_sensitivity") == "pii"

        stack = self.domain_rules.get(domain, self.domain_rules["microservices"]).copy()

        if budget > 50000 or users > 100000:
            stack["monitoring"] = "datadog"
            stack["message_queue"] = "kafka"
        elif budget < 3000:
            stack["cache_layer"] = "none"
            stack["message_queue"] = "none"

        if latency < 100:
            stack["cache_layer"] = "redis"

        if pii:
            stack["database"] = "postgresql"

        return stack

    def get_scale_category(self, users: int) -> str:
        """Get scale category based on user count."""
        for category, (low, high) in self.user_scale_rules.items():
            if low <= users < high:
                return category
        return "medium"

    def run_stack_recommendation(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Task 1: Recommend technology stack."""
        stack = self.select_stack(requirements)

        return {
            "api_framework": stack["api_framework"],
            "database": stack["database"],
            "cache_layer": stack["cache_layer"],
            "message_queue": stack["message_queue"],
            "monitoring": stack["monitoring"],
            "reasoning": f"Selected based on {requirements.get('domain', 'microservices')} domain and {requirements.get('expected_users', 1000)} users"
        }

    def detect_patterns(self, service_map: Dict[str, List[str]], database_choices: Dict[str, str], communication_pattern: str) -> Dict[str, Any]:
        """Detect architectural anti-patterns."""
        patterns_found = {}

        services = set(service_map.keys())
        for service, deps in service_map.items():
            services.update(deps)

        dep_graph = {s: [] for s in services}
        for service, deps in service_map.items():
            dep_graph[service] = deps

        def has_cycle(node, visited, rec_stack):
            visited.add(node)
            rec_stack.add(node)
            for neighbor in dep_graph.get(node, []):
                if neighbor not in visited:
                    if has_cycle(neighbor, visited, rec_stack):
                        return True
                elif neighbor in rec_stack:
                    return True
            rec_stack.remove(node)
            return False

        visited = set()
        for service in services:
            if service not in visited:
                if has_cycle(service, visited, set()):
                    patterns_found["circular_dependency"] = {
                        "severity": "critical",
                        "description": "Circular dependency detected in service graph",
                        "services": list(services)
                    }
                    break

        auth_dependencies = []
        for service, deps in service_map.items():
            if "auth" in deps or (service == "auth" and any(d for d in deps)):
                auth_dependencies.append(service)

        if len(auth_dependencies) > 3 and len(services) > 3:
            patterns_found["single_point_of_failure"] = {
                "severity": "high",
                "description": "Auth service has many dependencies - potential SPOF",
                "services": auth_dependencies
            }

        db_types = set(database_choices.values())
        if len(db_types) > 2 and "postgresql_shared" in db_types:
            patterns_found["shared_database"] = {
                "severity": "critical",
                "description": "Multiple services sharing same database instance",
                "database_type": "postgresql_shared"
            }
        elif len(db_types) > 3:
            patterns_found["polyglot_persistence_issue"] = {
                "severity": "medium",
                "description": "Multiple database types may cause consistency issues",
                "database_types": list(db_types)
            }

        if communication_pattern == "sync" and len(services) > 4:
            patterns_found["tight_coupling"] = {
                "severity": "high",
                "description": "Synchronous communication creates tight coupling",
                "communication": communication_pattern
            }

        return patterns_found

    def run_anti_pattern_detection(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """Task 2: Detect architectural anti-patterns."""
        service_map = test_case.get("service_map", {})
        database_choices = test_case.get("database_choices", {})
        communication_pattern = test_case.get("communication_pattern", "rest")

        patterns = self.detect_patterns(service_map, database_choices, communication_pattern)

        return {
            "patterns_detected": patterns,
            "severity_summary": {
                "critical": len([p for p in patterns.values() if p.get("severity") == "critical"]),
                "high": len([p for p in patterns.values() if p.get("severity") == "high"]),
                "medium": len([p for p in patterns.values() if p.get("severity") == "medium"])
            }
        }

    def generate_services(self, requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate service list based on requirements."""
        domain = requirements.get("domain", "microservices")
        services = []

        services.append({
            "name": "api_gateway",
            "type": "gateway",
            "technology": "Kong",
            "responsibilities": ["routing", "rate_limiting", "authentication"]
        })

        services.append({
            "name": "auth_service",
            "type": "service",
            "technology": "FastAPI",
            "responsibilities": ["authentication", "authorization", "user_management"]
        })

        if domain == "microservices":
            services.append({
                "name": "product_service",
                "type": "service",
                "technology": "FastAPI",
                "responsibilities": ["product_catalog", "search"]
            })

        if domain == "data_pipeline":
            services.append({
                "name": "ingestion_service",
                "type": "service",
                "technology": "Python",
                "responsibilities": ["data_ingestion", "validation"]
            })

        services.append({
            "name": "database",
            "type": "database",
            "technology": "PostgreSQL",
            "responsibilities": ["data_storage"]
        })

        return services

    def generate_failure_modes(self, services: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate failure modes for services."""
        failure_modes = []

        failure_modes.append({
            "component": "api_gateway",
            "failure_mode": "gateway_unavailable",
            "probability": "low",
            "impact": "critical",
            "mitigation": "multi-region_deployment"
        })

        failure_modes.append({
            "component": "auth_service",
            "failure_mode": "auth_service_down",
            "probability": "low",
            "impact": "high",
            "mitigation": "auth_caching"
        })

        failure_modes.append({
            "component": "database",
            "failure_mode": "database_connection_failure",
            "probability": "low",
            "impact": "critical",
            "mitigation": "connection_pooling"
        })

        return failure_modes

    def run_full_design(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Task 3: Generate full architecture design."""
        services = self.generate_services(requirements)

        connections = []
        for i, service in enumerate(services):
            if service["type"] == "gateway":
                for j, other in enumerate(services):
                    if other["type"] == "service":
                        connections.append({
                            "from": service["name"],
                            "to": other["name"],
                            "protocol": "HTTP/REST"
                        })

        failure_modes = self.generate_failure_modes(services)

        adrs = [
            {
                "id": "ADR-001",
                "title": "Use Microservices Architecture",
                "status": "accepted",
                "context": "Requirements indicate need for scalability",
                "decision": "Implement microservices pattern",
                "consequences": ["Increased complexity", "Better scalability"]
            }
        ]

        mermaid_diagram = "graph TD\n"
        for service in services:
            mermaid_diagram += f'    {service["name"].upper()}[{service["name"]}]\n'
        for conn in connections:
            mermaid_diagram += f'    {conn["from"].upper()} --> {conn["to"].upper()}\n'

        return {
            "architecture": {
                "id": "baseline_arch",
                "name": requirements.get("project_name", "Project"),
                "components": services,
                "connections": connections,
                "mermaid_diagram": mermaid_diagram
            },
            "adrs": adrs,
            "failure_modes": failure_modes,
            "confidence_score": 0.65
        }


def create_baseline_agent() -> BaselineAgent:
    """Factory function to create baseline agent."""
    return BaselineAgent()


def run_baseline(task_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Run baseline agent for given task and input."""
    agent = create_baseline_agent()

    if task_id == "task_stack_recommendation":
        return agent.run_stack_recommendation(input_data.get("requirements", {}))
    elif task_id == "task_anti_pattern_detection":
        return agent.run_anti_pattern_detection(input_data)
    elif task_id == "task_full_design_integration":
        return agent.run_full_design(input_data.get("requirements", {}))
    else:
        return {"error": f"Unknown task: {task_id}"}


if __name__ == "__main__":
    print("Baseline Agent for ELDER")
    print("=" * 50)

    agent = create_baseline_agent()

    test_requirements = {
        "domain": "microservices",
        "team_size": 5,
        "budget_usd": 50000,
        "expected_users": 100000,
        "latency_requirement_ms": 100,
        "data_sensitivity": "pii"
    }

    print("\nTask 1 - Stack Recommendation:")
    stack_result = agent.run_stack_recommendation(test_requirements)
    print(f"  Recommended Stack: {stack_result}")

    print("\nTask 3 - Full Design:")
    design_result = agent.run_full_design(test_requirements)
    print(f"  Services: {len(design_result['architecture']['components'])}")
    print(f"  Failure Modes: {len(design_result['failure_modes'])}")
