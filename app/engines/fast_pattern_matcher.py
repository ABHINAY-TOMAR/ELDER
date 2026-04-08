"""
Fast Pattern Matcher Engine - Rule-Based Version
Recommends tech stacks using hardcoded rules based on domain, team size, and budget.
No LLM dependencies - instant recommendations.
"""

from typing import Dict, List, Tuple
from pydantic import BaseModel
import logging

from app.models.schemas import RequirementSpec, StackRecommendation, Recommendation

logger = logging.getLogger("architect_agent.fast_pattern_matcher")


class RiskyDecision(BaseModel):
    decision_type: str
    reason: str
    impact: str
    why_needs_deep_thinking: str


class Rule(BaseModel):
    id: str
    domain: str
    max_team_size: int
    max_budget: int
    recommendation: Recommendation
    confidence: float
    priority: int


# ============================================================================
# HARDCODED RULE DATABASE
# ============================================================================

RULES_DB = [
    # MICROSERVICES RULES
    Rule(
        id="ms_small_team",
        domain="microservices",
        max_team_size=3,
        max_budget=10000,
        recommendation=Recommendation(
            api_framework="FastAPI",
            database="PostgreSQL",
            cache_layer="Redis",
            message_queue="",
            monitoring="Basic logging"
        ),
        confidence=0.95,
        priority=10
    ),
    Rule(
        id="ms_medium_team",
        domain="microservices",
        max_team_size=10,
        max_budget=50000,
        recommendation=Recommendation(
            api_framework="FastAPI",
            database="PostgreSQL",
            cache_layer="Redis",
            message_queue="RabbitMQ",
            monitoring="Prometheus + Grafana"
        ),
        confidence=0.90,
        priority=8
    ),
    Rule(
        id="ms_large_team",
        domain="microservices",
        max_team_size=999,
        max_budget=999999,
        recommendation=Recommendation(
            api_framework="Go (gRPC)",
            database="PostgreSQL (sharded)",
            cache_layer="Redis Cluster",
            message_queue="Kafka",
            monitoring="Datadog"
        ),
        confidence=0.85,
        priority=5
    ),
    
    # AI_NATIVE RULES
    Rule(
        id="ai_small_budget",
        domain="ai_native",
        max_team_size=3,
        max_budget=5000,
        recommendation=Recommendation(
            api_framework="FastAPI",
            database="Supabase",
            cache_layer="",
            vector_db="pgvector",
            monitoring="Basic logging"
        ),
        confidence=0.95,
        priority=10
    ),
    Rule(
        id="ai_medium_team",
        domain="ai_native",
        max_team_size=10,
        max_budget=50000,
        recommendation=Recommendation(
            api_framework="FastAPI",
            database="PostgreSQL",
            cache_layer="Redis",
            vector_db="Pinecone",
            message_queue="Celery",
            monitoring="Prometheus"
        ),
        confidence=0.90,
        priority=8
    ),
    Rule(
        id="ai_large_production",
        domain="ai_native",
        max_team_size=999,
        max_budget=999999,
        recommendation=Recommendation(
            api_framework="FastAPI",
            database="PostgreSQL",
            cache_layer="Redis",
            vector_db="Milvus",
            message_queue="Kafka",
            monitoring="Datadog + LLM observability"
        ),
        confidence=0.85,
        priority=5
    ),
    
    # DATA_PIPELINE RULES
    Rule(
        id="dp_batch_simple",
        domain="data_pipeline",
        max_team_size=5,
        max_budget=20000,
        recommendation=Recommendation(
            api_framework="Python scripts + Cron",
            database="PostgreSQL",
            cache_layer="",
            message_queue="",
            monitoring="Basic logging"
        ),
        confidence=0.90,
        priority=10
    ),
    Rule(
        id="dp_streaming_medium",
        domain="data_pipeline",
        max_team_size=15,
        max_budget=100000,
        recommendation=Recommendation(
            api_framework="Airflow",
            database="Snowflake",
            cache_layer="Spark (in-memory)",
            message_queue="Kafka",
            monitoring="Prometheus + Grafana"
        ),
        confidence=0.85,
        priority=8
    ),
    Rule(
        id="dp_enterprise",
        domain="data_pipeline",
        max_team_size=999,
        max_budget=999999,
        recommendation=Recommendation(
            api_framework="Airflow + dbt",
            database="Snowflake + Delta Lake",
            cache_layer="Spark",
            message_queue="Kafka + Flink",
            monitoring="Datadog + data quality monitoring"
        ),
        confidence=0.80,
        priority=5
    ),
]


class FastPatternMatcher:
    """
    Matches requirements to tech stack rules.
    Returns instant recommendations based on domain, team size, and budget.
    """
    
    def __init__(self):
        self.rules = RULES_DB
    
    def match(self, spec: RequirementSpec, domain: str) -> Tuple[StackRecommendation, List[RiskyDecision]]:
        """
        Match requirements to best rule and detect risky decisions.
        
        Args:
            spec: Parsed requirements
            domain: Classified domain
            
        Returns:
            Tuple of (StackRecommendation, List[RiskyDecision])
        """
        logger.info(f"Matching pattern for {domain} domain (team={spec.team_size}, budget=${spec.budget_usd})")
        
        # Find matching rules
        scored_rules = self._evaluate_rules(spec, domain)
        
        if not scored_rules:
            # Fallback to a safe default
            best_rule = self._get_fallback_rule(domain)
        else:
            best_rule = scored_rules[0][0]
        
        # Create recommendation
        recommendation = StackRecommendation(
            tech_stack=best_rule.recommendation,
            confidence=best_rule.confidence
        )
        
        # Detect risky decisions
        risky_decisions = self._detect_risky_decisions(spec, best_rule.recommendation)
        
        logger.info(f"Matched rule: {best_rule.id} (confidence={best_rule.confidence}, risks={len(risky_decisions)})")
        
        return recommendation, risky_decisions
    
    def _evaluate_rules(self, spec: RequirementSpec, domain: str) -> List[Tuple[Rule, float]]:
        """
        Evaluate all rules for given domain and return scored matches.
        
        Returns list of (Rule, score) tuples sorted by score descending.
        """
        scored_rules = []
        
        for rule in self.rules:
            if rule.domain != domain:
                continue
            
            # Check if requirements fit within rule constraints
            if spec.team_size <= rule.max_team_size and spec.budget_usd <= rule.max_budget:
                # Score based on confidence and priority
                score = rule.confidence * float(rule.priority)
                scored_rules.append((rule, score))
        
        # Sort by score descending
        scored_rules.sort(key=lambda x: x[1], reverse=True)
        return scored_rules
    
    def _get_fallback_rule(self, domain: str) -> Rule:
        """Get a safe fallback rule for domain"""
        fallbacks = {
            "microservices": "ms_small_team",
            "ai_native": "ai_small_budget",
            "data_pipeline": "dp_batch_simple"
        }
        
        fallback_id = fallbacks.get(domain, "ms_small_team")
        
        for rule in self.rules:
            if rule.id == fallback_id:
                return rule
        
        return self.rules[0]  # Ultimate fallback
    
    def _detect_risky_decisions(self, spec: RequirementSpec, rec: Recommendation) -> List[RiskyDecision]:
        """
        Detect risky decisions that need deep thinking.
        
        Returns list of decisions flagged for extended reasoning.
        """
        risks = []
        
        # Risk 1: Extreme scale
        if spec.expected_users > 10000000:
            risks.append(RiskyDecision(
                decision_type="scaling",
                reason=f"Extremely high user count ({spec.expected_users:,}) exceeds standard templates",
                impact="high",
                why_needs_deep_thinking="Need to determine sharding strategy, CDN requirements, and multi-region deployment"
            ))
        
        # Risk 2: PII data handling
        if spec.data_sensitivity == "pii":
            risks.append(RiskyDecision(
                decision_type="security_compliance",
                reason="Handling PII data requires strict compliance measures",
                impact="high",
                why_needs_deep_thinking="Need to verify encryption, access controls, audit logging, and regulatory compliance (GDPR, HIPAA, etc.)"
            ))
        
        # Risk 3: Ultra-low latency
        if spec.latency_requirement_ms < 100:
            risks.append(RiskyDecision(
                decision_type="performance",
                reason=f"Sub-100ms latency ({spec.latency_requirement_ms}ms) is extremely demanding",
                impact="high",
                why_needs_deep_thinking="Need to evaluate CDN, edge computing, in-memory caching, and data locality strategies"
            ))
        
        # Risk 4: Large team coordination
        if spec.team_size > 20:
            risks.append(RiskyDecision(
                decision_type="team_coordination",
                reason=f"Large team ({spec.team_size} engineers) requires careful service boundaries",
                impact="medium",
                why_needs_deep_thinking="Need to define clear service ownership, API contracts, and communication patterns"
            ))
        
        # Risk 5: Budget constraints with high requirements
        if spec.budget_usd < 20000 and spec.expected_users > 1000000:
            risks.append(RiskyDecision(
                decision_type="cost_optimization",
                reason=f"Low budget (${spec.budget_usd}) for high user count ({spec.expected_users:,})",
                impact="high",
                why_needs_deep_thinking="Need to identify cost-effective alternatives and optimize infrastructure spending"
            ))
        
        return risks


# Module-level function for backward compatibility
def match(spec: RequirementSpec, domain: str) -> Tuple[StackRecommendation, List[RiskyDecision]]:
    """Match pattern (non-async version)"""
    matcher = FastPatternMatcher()
    return matcher.match(spec, domain)
