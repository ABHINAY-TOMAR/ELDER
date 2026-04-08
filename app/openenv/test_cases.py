"""
Test cases with ground truth for OpenEnv evaluation.
Each task has at least 2 hardcoded test cases for reset functionality.
"""

from typing import Dict, List, Any
from app.models.schemas import Architecture, Service, ADR, FailureMode, DataFlow

TASK_1_TEST_CASES: List[Dict[str, Any]] = [
    {
        "id": "test_case_1_microservices_small",
        "task_id": "task_stack_recommendation",
        "requirements": {
            "project_name": "E-commerce Microservices",
            "domain": "microservices",
            "team_size": 2,
            "budget_usd": 5000,
            "expected_users": 10000,
            "latency_requirement_ms": 500,
            "data_sensitivity": "internal",
            "deployment_target": "cloud",
            "timeline_weeks": 12
        },
        "ground_truth": {
            "api_framework": "fastapi",
            "database": "postgresql",
            "cache_layer": "redis",
            "message_queue": "rabbitmq",
            "monitoring": "prometheus"
        }
    },
    {
        "id": "test_case_2_ai_native_startup",
        "task_id": "task_stack_recommendation",
        "requirements": {
            "project_name": "AI Agent Platform",
            "domain": "ai_native",
            "team_size": 1,
            "budget_usd": 2000,
            "expected_users": 1000,
            "latency_requirement_ms": 2000,
            "data_sensitivity": "public",
            "deployment_target": "cloud",
            "timeline_weeks": 8
        },
        "ground_truth": {
            "api_framework": "fastapi",
            "database": "supabase",
            "cache_layer": "none",
            "message_queue": "none",
            "monitoring": "basic"
        }
    }
]

TASK_2_TEST_CASES: List[Dict[str, Any]] = [
    {
        "id": "test_case_1_circular_spf",
        "task_id": "task_anti_pattern_detection",
        "system_description": "E-commerce platform with 5 services: Auth, Product, Recommendation, Cart, Order. Auth depends on Product and Order. Product depends on Recommendation. Recommendation depends on Product. Cart depends on Order. Order depends on Auth.",
        "service_map": {
            "auth": ["product", "order", "cart"],
            "product": ["recommendation"],
            "recommendation": ["product"],
            "cart": ["order"],
            "order": ["auth"]
        },
        "database_choices": {
            "auth": "postgresql",
            "product": "postgresql",
            "recommendation": "mongodb",
            "cart": "redis",
            "order": "postgresql"
        },
        "communication_pattern": "rest",
        "scalability_requirements": "100k users",
        "ground_truth_patterns": {
            "circular_dependency": {
                "severity": "critical",
                "description": "Circular dependency between product and recommendation services creates deployment ordering problem",
                "keywords": ["circular", "cycle", "loop", "product → recommendation", "recommendation → product"]
            },
            "single_point_of_failure": {
                "severity": "high",
                "description": "Auth service is single point of failure - every service depends on it",
                "keywords": ["single point", "spof", "bottleneck", "redundancy", "auth"]
            },
            "polyglot_persistence_issue": {
                "severity": "medium",
                "description": "Cart uses Redis (no ACID) but Order uses PostgreSQL - transactional issues",
                "keywords": ["polyglot", "persistence", "transaction", "acid", "redis"]
            }
        }
    },
    {
        "id": "test_case_2_tight_coupling",
        "task_id": "task_anti_pattern_detection",
        "system_description": "SaaS multi-tenant platform with monolith backend. All tenants share single database instance. Authentication embedded in main service.",
        "service_map": {
            "main_service": ["database"],
            "frontend": ["main_service"]
        },
        "database_choices": {
            "main_service": "postgresql",
            "frontend": "none"
        },
        "communication_pattern": "mixed",
        "scalability_requirements": "50k users",
        "ground_truth_patterns": {
            "tight_coupling": {
                "severity": "high",
                "description": "Monolithic architecture creates tight coupling between all features",
                "keywords": ["tight", "coupling", "monolith", "coupled"]
            },
            "shared_database": {
                "severity": "medium",
                "description": "Shared database creates coupling and potential performance bottlenecks",
                "keywords": ["shared database", "coupling", "bottleneck", "shared"]
            },
            "n_plus_1_query": {
                "severity": "medium",
                "description": "Embedded auth may cause N+1 queries when checking tenant permissions",
                "keywords": ["n+1", "query", "inefficient", "loop"]
            }
        }
    }
]

TASK_3_TEST_CASES: List[Dict[str, Any]] = [
    {
        "id": "test_case_1_recommendation_engine",
        "task_id": "task_full_design_integration",
        "requirements": {
            "project_name": "AI-Powered Recommendation Engine",
            "domain": "ai_native",
            "project_description": """
                Build an AI-powered recommendation engine for e-commerce.
                Requirements:
                - 100,000 users
                - Personalized product recommendations in <500ms
                - Real-time inventory sync
                - Async model retraining daily
                - PII compliance required (user data handling)
            """,
            "constraints": [
                "must use vector database for embeddings",
                "payment processing must be PCI-DSS compliant",
                "async processing for model training"
            ],
            "expected_services": ["api_gateway", "auth_service", "product_service", "recommendation_engine", "vector_db", "payment_service", "job_queue"],
            "latency_ms": 500,
            "scale": "100k users",
            "pii": True
        },
        "ground_truth_requirements": {
            "latency_ms": 500,
            "scale": "100k users",
            "pii": True,
            "required_services": ["api_gateway", "auth", "product", "recommendation", "vector_db"],
            "required_integrations": ["auth → recommendation", "product → recommendation", "recommendation → product"],
            "required_failure_modes": ["vector_db_down", "model_timeout", "auth_failure"]
        }
    },
    {
        "id": "test_case_2_microservices_platform",
        "task_id": "task_full_design_integration",
        "requirements": {
            "project_name": "SaaS Multi-Tenant Platform",
            "domain": "microservices",
            "project_description": """
                Build a SaaS multi-tenant platform for project management.
                Requirements:
                - 50,000 users across 500 tenants
                - Sub-200ms response time
                - Tenant isolation required (data security)
                - Real-time notifications
                - 99.9% uptime SLA
            """,
            "constraints": [
                "tenant isolation mandatory",
                "multi-region deployment",
                "websocket support for notifications"
            ],
            "expected_services": ["api_gateway", "auth_service", "tenant_service", "project_service", "notification_service", "websocket_handler"],
            "latency_ms": 200,
            "scale": "50k users",
            "pii": True
        },
        "ground_truth_requirements": {
            "latency_ms": 200,
            "scale": "50k users",
            "pii": True,
            "required_services": ["api_gateway", "auth", "tenant", "project", "notification"],
            "required_integrations": ["auth → tenant", "tenant → project", "project → notification"],
            "required_failure_modes": ["tenant_isolation_breach", "notification_delay", "api_gateway_spof"]
        }
    }
]

TEST_CASES = {
    "task_stack_recommendation": TASK_1_TEST_CASES,
    "task_anti_pattern_detection": TASK_2_TEST_CASES,
    "task_full_design_integration": TASK_3_TEST_CASES,
}

def get_test_cases_for_task(task_id: str) -> List[Dict[str, Any]]:
    """Get all test cases for a specific task."""
    if task_id == "task_stack_recommendation":
        return TASK_1_TEST_CASES
    elif task_id == "task_anti_pattern_detection":
        return TASK_2_TEST_CASES
    elif task_id == "task_full_design_integration":
        return TASK_3_TEST_CASES
    return []

def get_random_test_case(task_id: str) -> Dict[str, Any]:
    """Get a random test case for a specific task."""
    import random
    test_cases = get_test_cases_for_task(task_id)
    return random.choice(test_cases) if test_cases else {}
