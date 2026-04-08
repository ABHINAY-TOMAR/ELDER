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
        "description": "E-commerce platform for 10k users with 2-person team",
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
        "description": "AI agent platform for solo developer",
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
    },
    {
        "id": "test_case_3_microservices_enterprise",
        "task_id": "task_stack_recommendation",
        "description": "Enterprise microservices for 1M users",
        "requirements": {
            "project_name": "Enterprise SaaS Platform",
            "domain": "microservices",
            "team_size": 10,
            "budget_usd": 100000,
            "expected_users": 1000000,
            "latency_requirement_ms": 100,
            "data_sensitivity": "pii",
            "deployment_target": "cloud",
            "timeline_weeks": 52
        },
        "ground_truth": {
            "api_framework": "fastapi",
            "database": "postgresql",
            "cache_layer": "redis",
            "message_queue": "kafka",
            "monitoring": "datadog"
        }
    },
    {
        "id": "test_case_4_data_pipeline",
        "task_id": "task_stack_recommendation",
        "description": "Data pipeline for ETL processing",
        "requirements": {
            "project_name": "Data Pipeline Platform",
            "domain": "data_pipeline",
            "team_size": 3,
            "budget_usd": 15000,
            "expected_users": 100,
            "latency_requirement_ms": 5000,
            "data_sensitivity": "internal",
            "deployment_target": "cloud",
            "timeline_weeks": 16
        },
        "ground_truth": {
            "api_framework": "none",
            "database": "postgresql",
            "cache_layer": "none",
            "message_queue": "kafka",
            "monitoring": "airflow"
        }
    },
    {
        "id": "test_case_5_startup_mvp",
        "task_id": "task_stack_recommendation",
        "description": "Startup MVP with minimal team",
        "requirements": {
            "project_name": "Startup MVP",
            "domain": "microservices",
            "team_size": 2,
            "budget_usd": 3000,
            "expected_users": 5000,
            "latency_requirement_ms": 1000,
            "data_sensitivity": "public",
            "deployment_target": "cloud",
            "timeline_weeks": 8
        },
        "ground_truth": {
            "api_framework": "fastapi",
            "database": "postgresql",
            "cache_layer": "redis",
            "message_queue": "none",
            "monitoring": "prometheus"
        }
    },
    {
        "id": "test_case_6_hipaa_healthcare",
        "task_id": "task_stack_recommendation",
        "description": "Healthcare platform with HIPAA compliance",
        "requirements": {
            "project_name": "Healthcare Platform",
            "domain": "microservices",
            "team_size": 5,
            "budget_usd": 50000,
            "expected_users": 100000,
            "latency_requirement_ms": 500,
            "data_sensitivity": "pii",
            "deployment_target": "on_prem",
            "timeline_weeks": 26
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
        "id": "test_case_7_ai_chatbot",
        "task_id": "task_stack_recommendation",
        "description": "AI chatbot with RAG capabilities",
        "requirements": {
            "project_name": "AI Chatbot Platform",
            "domain": "ai_native",
            "team_size": 2,
            "budget_usd": 8000,
            "expected_users": 50000,
            "latency_requirement_ms": 1000,
            "data_sensitivity": "pii",
            "deployment_target": "cloud",
            "timeline_weeks": 12
        },
        "ground_truth": {
            "api_framework": "fastapi",
            "database": "supabase",
            "cache_layer": "redis",
            "message_queue": "none",
            "monitoring": "prometheus"
        }
    },
    {
        "id": "test_case_8_gaming_backend",
        "task_id": "task_stack_recommendation",
        "description": "Real-time gaming backend",
        "requirements": {
            "project_name": "Gaming Platform",
            "domain": "microservices",
            "team_size": 6,
            "budget_usd": 30000,
            "expected_users": 500000,
            "latency_requirement_ms": 50,
            "data_sensitivity": "pii",
            "deployment_target": "cloud",
            "timeline_weeks": 24
        },
        "ground_truth": {
            "api_framework": "fastapi",
            "database": "postgresql",
            "cache_layer": "redis",
            "message_queue": "kafka",
            "monitoring": "datadog"
        }
    },
    {
        "id": "test_case_9_iot_platform",
        "task_id": "task_stack_recommendation",
        "description": "IoT device management platform",
        "requirements": {
            "project_name": "IoT Platform",
            "domain": "data_pipeline",
            "team_size": 4,
            "budget_usd": 20000,
            "expected_users": 10000,
            "latency_requirement_ms": 200,
            "data_sensitivity": "internal",
            "deployment_target": "hybrid",
            "timeline_weeks": 20
        },
        "ground_truth": {
            "api_framework": "fastapi",
            "database": "postgresql",
            "cache_layer": "redis",
            "message_queue": "kafka",
            "monitoring": "prometheus"
        }
    },
    {
        "id": "test_case_10_e_commerce_marketplace",
        "task_id": "task_stack_recommendation",
        "description": "Multi-vendor e-commerce marketplace",
        "requirements": {
            "project_name": "E-commerce Marketplace",
            "domain": "microservices",
            "team_size": 8,
            "budget_usd": 75000,
            "expected_users": 500000,
            "latency_requirement_ms": 200,
            "data_sensitivity": "pii",
            "deployment_target": "cloud",
            "timeline_weeks": 40
        },
        "ground_truth": {
            "api_framework": "fastapi",
            "database": "postgresql",
            "cache_layer": "redis",
            "message_queue": "kafka",
            "monitoring": "datadog"
        }
    }
]

TASK_2_TEST_CASES: List[Dict[str, Any]] = [
    {
        "id": "test_case_1_circular_spf",
        "task_id": "task_anti_pattern_detection",
        "description": "E-commerce with circular dependency and auth SPOF",
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
        "description": "SaaS monolith with shared database",
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
    },
    {
        "id": "test_case_3_unencrypted_pii",
        "task_id": "task_anti_pattern_detection",
        "description": "Healthcare system with unencrypted PII",
        "system_description": "Healthcare patient management system. Patient records stored in MongoDB without encryption. Auth service uses JWT but tokens not rotated. Database credentials hardcoded in config.",
        "service_map": {
            "auth": [],
            "patient_records": ["auth"],
            "billing": ["auth", "patient_records"],
            "reporting": ["patient_records"]
        },
        "database_choices": {
            "auth": "postgresql",
            "patient_records": "mongodb",
            "billing": "postgresql",
            "reporting": "mongodb"
        },
        "communication_pattern": "rest",
        "scalability_requirements": "10k users",
        "ground_truth_patterns": {
            "unencrypted_pii": {
                "severity": "critical",
                "description": "Patient records stored without encryption in MongoDB",
                "keywords": ["encryption", "gdpr", "hipaa", "pii", "plaintext", "unencrypted"]
            },
            "single_point_of_failure": {
                "severity": "high",
                "description": "Auth service is single point of failure",
                "keywords": ["single point", "spof", "bottleneck", "redundancy"]
            },
            "tight_coupling": {
                "severity": "medium",
                "description": "Reporting tightly coupled to patient_records schema",
                "keywords": ["tight", "coupling", "coupled"]
            }
        }
    },
    {
        "id": "test_case_4_n_plus_1_queries",
        "task_id": "task_anti_pattern_detection",
        "description": "E-commerce with N+1 query problems",
        "system_description": "E-commerce platform. Product listing page loads products, then for each product makes separate API call to get inventory, then for each inventory makes call to get pricing.",
        "service_map": {
            "api_gateway": ["product_service", "inventory_service", "pricing_service"],
            "product_service": [],
            "inventory_service": [],
            "pricing_service": []
        },
        "database_choices": {
            "api_gateway": "none",
            "product_service": "postgresql",
            "inventory_service": "postgresql",
            "pricing_service": "postgresql"
        },
        "communication_pattern": "rest",
        "scalability_requirements": "100k users",
        "ground_truth_patterns": {
            "n_plus_1_query": {
                "severity": "critical",
                "description": "N+1 query pattern: product listing causes cascading API calls",
                "keywords": ["n+1", "query", "inefficient", "loop", "cascading"]
            },
            "tight_coupling": {
                "severity": "high",
                "description": "Services tightly coupled through API gateway",
                "keywords": ["tight", "coupling", "coupled", "gateway"]
            }
        }
    },
    {
        "id": "test_case_5_shared_database",
        "task_id": "task_anti_pattern_detection",
        "description": "Microservices sharing single database",
        "system_description": "Four microservices (users, orders, inventory, billing) all connect to same PostgreSQL database instance. Each service can directly query tables belonging to other services.",
        "service_map": {
            "users": [],
            "orders": [],
            "inventory": [],
            "billing": []
        },
        "database_choices": {
            "users": "postgresql_shared",
            "orders": "postgresql_shared",
            "inventory": "postgresql_shared",
            "billing": "postgresql_shared"
        },
        "communication_pattern": "direct_db",
        "scalability_requirements": "500k users",
        "ground_truth_patterns": {
            "shared_database": {
                "severity": "critical",
                "description": "All services share single database - tight coupling",
                "keywords": ["shared database", "shared schema", "coupling"]
            },
            "single_point_of_failure": {
                "severity": "high",
                "description": "Database is single point of failure for all services",
                "keywords": ["single point", "spof", "bottleneck", "redundancy"]
            }
        }
    },
    {
        "id": "test_case_6_cascade_failure",
        "task_id": "task_anti_pattern_detection",
        "description": "Payment service failure causes cascade",
        "system_description": "E-commerce with payment service that if slow, causes all other services to timeout. No circuit breaker. Retry storm when payment recovers.",
        "service_map": {
            "api_gateway": ["auth", "catalog", "cart", "payment", "order"],
            "auth": [],
            "catalog": [],
            "cart": [],
            "payment": [],
            "order": ["payment"]
        },
        "database_choices": {
            "auth": "postgresql",
            "catalog": "mongodb",
            "cart": "redis",
            "payment": "postgresql",
            "order": "postgresql"
        },
        "communication_pattern": "sync",
        "scalability_requirements": "200k users",
        "ground_truth_patterns": {
            "single_point_of_failure": {
                "severity": "critical",
                "description": "Payment service is synchronous SPOF - slow payment freezes entire system",
                "keywords": ["single point", "spof", "cascade", "timeout", "payment"]
            },
            "circular_dependency": {
                "severity": "medium",
                "description": "API gateway depends on payment, payment depends on order, order depends on API gateway for orchestration",
                "keywords": ["circular", "cycle", "loop", "cascade"]
            }
        }
    },
    {
        "id": "test_case_7_god_object",
        "task_id": "task_anti_pattern_detection",
        "description": "Single service doing too much",
        "system_description": "One 'main' service handles auth, product catalog, inventory, orders, payments, notifications, email, SMS, webhooks, and reporting. 50k lines of code.",
        "service_map": {
            "main_service": ["database"],
            "frontend": ["main_service"]
        },
        "database_choices": {
            "main_service": "postgresql",
            "frontend": "none"
        },
        "communication_pattern": "internal",
        "scalability_requirements": "1M users",
        "ground_truth_patterns": {
            "tight_coupling": {
                "severity": "critical",
                "description": "God object service - single service does everything",
                "keywords": ["tight", "coupling", "monolith", "god object", "single service"]
            },
            "single_point_of_failure": {
                "severity": "high",
                "description": "One service handles everything - complete SPOF",
                "keywords": ["single point", "spof", "bottleneck"]
            }
        }
    },
    {
        "id": "test_case_8_data_consistency",
        "task_id": "task_anti_pattern_detection",
        "description": "Eventual consistency without handling",
        "system_description": "Event-driven architecture using Kafka. Services read from Kafka topics but don't handle out-of-order events. No idempotency. No saga pattern for distributed transactions.",
        "service_map": {
            "order_service": [],
            "inventory_service": [],
            "payment_service": [],
            "notification_service": []
        },
        "database_choices": {
            "order_service": "postgresql",
            "inventory_service": "mongodb",
            "payment_service": "postgresql",
            "notification_service": "redis"
        },
        "communication_pattern": "async",
        "scalability_requirements": "500k users",
        "ground_truth_patterns": {
            "tight_coupling": {
                "severity": "high",
                "description": "Services assume synchronous behavior in async system",
                "keywords": ["tight", "coupling", "async", "consistency"]
            },
            "shared_database": {
                "severity": "medium",
                "description": "Order and payment share customer data without transaction",
                "keywords": ["shared", "coupling", "consistency"]
            }
        }
    },
    {
        "id": "test_case_9_resource_contention",
        "task_id": "task_anti_pattern_detection",
        "description": "Thread pool exhaustion",
        "system_description": "API service with fixed thread pool of 100 threads. Makes synchronous calls to 5 downstream services. One downstream service has 2s latency. All threads blocked waiting.",
        "service_map": {
            "api": ["service_a", "service_b", "service_c", "service_d", "service_e"],
            "service_a": [],
            "service_b": [],
            "service_c": [],
            "service_d": [],
            "service_e": []
        },
        "database_choices": {
            "api": "none",
            "service_a": "postgresql",
            "service_b": "postgresql",
            "service_c": "postgresql",
            "service_d": "postgresql",
            "service_e": "postgresql"
        },
        "communication_pattern": "sync",
        "scalability_requirements": "10k users",
        "ground_truth_patterns": {
            "single_point_of_failure": {
                "severity": "critical",
                "description": "Thread pool exhaustion blocks all requests",
                "keywords": ["thread", "pool", "exhaustion", "blocking", "bottleneck"]
            },
            "tight_coupling": {
                "severity": "high",
                "description": "Synchronous coupling to slow services",
                "keywords": ["tight", "coupling", "sync", "blocking"]
            }
        }
    },
    {
        "id": "test_case_10_missing_caching",
        "task_id": "task_anti_pattern_detection",
        "description": "No caching for hot data",
        "system_description": "Social media platform. User profile, feed, and timeline fetched from database on every request. No caching layer. Database CPU at 100%.",
        "service_map": {
            "api": ["user_service", "feed_service", "timeline_service"],
            "user_service": [],
            "feed_service": [],
            "timeline_service": []
        },
        "database_choices": {
            "api": "none",
            "user_service": "postgresql",
            "feed_service": "postgresql",
            "timeline_service": "postgresql"
        },
        "communication_pattern": "rest",
        "scalability_requirements": "10M users",
        "ground_truth_patterns": {
            "single_point_of_failure": {
                "severity": "critical",
                "description": "No caching causes database overload - SPOF",
                "keywords": ["cache", "bottleneck", "overload", "database"]
            },
            "tight_coupling": {
                "severity": "high",
                "description": "Services tightly coupled to database performance",
                "keywords": ["tight", "coupling", "database", "performance"]
            }
        }
    }
]

TASK_3_TEST_CASES: List[Dict[str, Any]] = [
    {
        "id": "test_case_1_recommendation_engine",
        "task_id": "task_full_design_integration",
        "description": "AI-powered recommendation engine with vector DB",
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
        "description": "SaaS multi-tenant project management platform",
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
    },
    {
        "id": "test_case_3_iot_platform",
        "task_id": "task_full_design_integration",
        "description": "IoT device management with real-time streaming",
        "requirements": {
            "project_name": "IoT Device Management Platform",
            "domain": "data_pipeline",
            "project_description": """
                Build an IoT platform for managing 1M connected devices.
                Requirements:
                - Real-time telemetry ingestion from 1M devices
                - Time-series storage for sensor data
                - Alerting and anomaly detection
                - Device command and control
                - Sub-second latency for critical alerts
            """,
            "constraints": [
                "must use time-series database",
                "edge computing for offline devices",
                "device firmware OTA updates"
            ],
            "expected_services": ["iot_gateway", "telemetry_ingestion", "time_series_db", "alerting_engine", "device_registry", "ota_service"],
            "latency_ms": 100,
            "scale": "1M devices",
            "pii": False
        },
        "ground_truth_requirements": {
            "latency_ms": 100,
            "scale": "1M devices",
            "pii": False,
            "required_services": ["iot_gateway", "telemetry", "time_series", "alerting"],
            "required_integrations": ["device → gateway → telemetry", "alerting → notification"],
            "required_failure_modes": ["gateway_overload", "timeseries_write_failure", "alerting_latency"]
        }
    },
    {
        "id": "test_case_4_healthcare_platform",
        "task_id": "task_full_design_integration",
        "description": "HIPAA-compliant healthcare platform",
        "requirements": {
            "project_name": "Healthcare Telemedicine Platform",
            "domain": "microservices",
            "project_description": """
                Build a telemedicine platform for healthcare providers.
                Requirements:
                - Video consultations with <200ms latency
                - HIPAA-compliant patient data storage
                - Appointment scheduling and reminders
                - E-prescription integration
                - Insurance verification
            """,
            "constraints": [
                "HIPAA compliance mandatory",
                "end-to-end encryption for video",
                "audit logging for all data access"
            ],
            "expected_services": ["video_gateway", "patient_service", "appointment_service", "prescription_service", "insurance_service", "audit_logger"],
            "latency_ms": 200,
            "scale": "100k patients",
            "pii": True
        },
        "ground_truth_requirements": {
            "latency_ms": 200,
            "scale": "100k patients",
            "pii": True,
            "required_services": ["video", "patient", "appointment", "audit"],
            "required_integrations": ["patient → video", "appointment → notification"],
            "required_failure_modes": ["encryption_failure", "audit_log_failure", "video_latency"]
        }
    },
    {
        "id": "test_case_5_fintech_platform",
        "task_id": "task_full_design_integration",
        "description": "Real-time trading platform",
        "requirements": {
            "project_name": "Cryptocurrency Trading Platform",
            "domain": "data_pipeline",
            "project_description": """
                Build a cryptocurrency trading platform.
                Requirements:
                - Real-time order matching <10ms latency
                - Handle 100k TPS order throughput
                - Real-time price streaming to 500k clients
                - PCI-DSS compliance for payment processing
                - Fraud detection and risk management
            """,
            "constraints": [
                "sub-millisecond latency for critical paths",
                "horizontal scaling for peak loads",
                "cold wallet storage for crypto assets"
            ],
            "expected_services": ["order_matcher", "price_streaming", "payment_service", "fraud_detection", "wallet_service", "risk_engine"],
            "latency_ms": 10,
            "scale": "500k users",
            "pii": True
        },
        "ground_truth_requirements": {
            "latency_ms": 10,
            "scale": "500k users",
            "pii": True,
            "required_services": ["order_matcher", "price_stream", "fraud", "wallet"],
            "required_integrations": ["order → matcher → wallet", "fraud → risk"],
            "required_failure_modes": ["matching_latency", "fraud_false_positive", "wallet_security"]
        }
    },
    {
        "id": "test_case_6_gaming_backend",
        "task_id": "task_full_design_integration",
        "description": "Real-time multiplayer gaming backend",
        "requirements": {
            "project_name": "Multiplayer Gaming Platform",
            "domain": "data_pipeline",
            "project_description": """
                Build a real-time multiplayer gaming backend.
                Requirements:
                - Game state synchronization <50ms
                - Matchmaking for 10k concurrent players
                - Leaderboard and player stats
                - In-game purchases and virtual currency
                - Anti-cheat integration
            """,
            "constraints": [
                "UDP-based communication for low latency",
                "state reconciliation for network issues",
                "rate limiting to prevent abuse"
            ],
            "expected_services": ["game_server", "matchmaking_service", "leaderboard_service", "payment_service", "anti_cheat_service", "player_stats_service"],
            "latency_ms": 50,
            "scale": "100k concurrent users",
            "pii": True
        },
        "ground_truth_requirements": {
            "latency_ms": 50,
            "scale": "100k users",
            "pii": True,
            "required_services": ["game_server", "matchmaking", "leaderboard", "anti_cheat"],
            "required_integrations": ["player → game_server → stats", "matchmaking → game_server"],
            "required_failure_modes": ["sync_failure", "matchmaking_timeout", "cheat_detection_latency"]
        }
    },
    {
        "id": "test_case_7_social_media",
        "task_id": "task_full_design_integration",
        "description": "Social media platform with real-time feed",
        "requirements": {
            "project_name": "Social Media Platform",
            "domain": "microservices",
            "project_description": """
                Build a social media platform.
                Requirements:
                - User timeline generation <500ms
                - Real-time notifications for 1M users
                - Media upload and processing (images, videos)
                - Friend/follow relationships
                - Content moderation and reporting
            """,
            "constraints": [
                "content delivery network for media",
                "caching for hot data paths",
                "graceful degradation during peak load"
            ],
            "expected_services": ["user_service", "post_service", "media_service", "notification_service", "timeline_service", "moderation_service"],
            "latency_ms": 500,
            "scale": "10M users",
            "pii": True
        },
        "ground_truth_requirements": {
            "latency_ms": 500,
            "scale": "10M users",
            "pii": True,
            "required_services": ["user", "post", "timeline", "notification", "media"],
            "required_integrations": ["post → timeline", "user → notification"],
            "required_failure_modes": ["timeline_generation_slow", "media_upload_failure", "notification_flood"]
        }
    },
    {
        "id": "test_case_8_edtech_platform",
        "task_id": "task_full_design_integration",
        "description": "Online learning platform with video streaming",
        "requirements": {
            "project_name": "Online Learning Platform",
            "domain": "microservices",
            "project_description": """
                Build an online learning platform.
                Requirements:
                - Video course streaming
                - Interactive quizzes and assessments
                - Progress tracking and certificates
                - Discussion forums
                - Live instructor sessions
            """,
            "constraints": [
                "adaptive bitrate streaming",
                "offline viewing support",
                "quiz anti-cheating measures"
            ],
            "expected_services": ["video_service", "course_service", "quiz_service", "progress_service", "forum_service", "live_session_service"],
            "latency_ms": 2000,
            "scale": "500k learners",
            "pii": False
        },
        "ground_truth_requirements": {
            "latency_ms": 2000,
            "scale": "500k learners",
            "pii": False,
            "required_services": ["video", "course", "quiz", "progress"],
            "required_integrations": ["course → video", "quiz → progress"],
            "required_failure_modes": ["video_buffering", "quiz_submission_failure", "progress_sync_delay"]
        }
    },
    {
        "id": "test_case_9_supply_chain",
        "task_id": "task_full_design_integration",
        "description": "Supply chain visibility platform",
        "requirements": {
            "project_name": "Supply Chain Visibility Platform",
            "domain": "data_pipeline",
            "project_description": """
                Build a supply chain visibility platform.
                Requirements:
                - Real-time shipment tracking
                - IoT sensor data from containers
                - Predictive delivery ETA
                - Supplier collaboration portal
                - Inventory optimization
            """,
            "constraints": [
                "integration with carrier APIs",
                "predictive analytics for delays",
                "audit trail for compliance"
            ],
            "expected_services": ["tracking_service", "iot_ingestion", "prediction_service", "supplier_portal", "inventory_service", "analytics_service"],
            "latency_ms": 5000,
            "scale": "10k shipments/day",
            "pii": False
        },
        "ground_truth_requirements": {
            "latency_ms": 5000,
            "scale": "10k shipments/day",
            "pii": False,
            "required_services": ["tracking", "iot", "prediction", "inventory"],
            "required_integrations": ["shipment → tracking → prediction", "iot → analytics"],
            "required_failure_modes": ["tracking_update_delay", "iot_data_loss", "prediction_inaccuracy"]
        }
    },
    {
        "id": "test_case_10_logistics_platform",
        "task_id": "task_full_design_integration",
        "description": "Last-mile delivery optimization platform",
        "requirements": {
            "project_name": "Last-Mile Delivery Platform",
            "domain": "data_pipeline",
            "project_description": """
                Build a last-mile delivery optimization platform.
                Requirements:
                - Route optimization for 1000 drivers
                - Real-time GPS tracking
                - Customer ETA notifications
                - Proof of delivery capture
                - Driver scheduling and dispatch
            """,
            "constraints": [
                "offline capability for drivers in dead zones",
                "dynamic rerouting for traffic",
                "signature and photo proof of delivery"
            ],
            "expected_services": ["route_optimizer", "driver_app_backend", "customer_notification", "pod_service", "dispatch_service", "geofencing_service"],
            "latency_ms": 500,
            "scale": "1000 drivers",
            "pii": True
        },
        "ground_truth_requirements": {
            "latency_ms": 500,
            "scale": "1000 drivers",
            "pii": True,
            "required_services": ["route", "driver", "customer", "pod"],
            "required_integrations": ["driver → route → customer", "pod → delivery_confirmation"],
            "required_failure_modes": ["route_calculation_slow", "offline_sync_failure", "pod_upload_failure"]
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
