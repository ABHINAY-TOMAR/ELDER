import structlog
from typing import List
from app.models.schemas import RequirementSpec, StackRecommendation
from app.engines.fast_pattern_matcher import RiskyDecision

logger = structlog.get_logger("architect_agent.risky_decision_detector")

def detect(spec: RequirementSpec, fast_rec: StackRecommendation) -> List[RiskyDecision]:
    """
    Identifies architectural choices that shouldn't be templated.
    These are decisions that need deeper reasoning (LLM extended thinking).
    """
    logger.info("detecting_risky_decisions_start")
    
    risks: List[RiskyDecision] = []
    
    # Text helper
    ft_str = " ".join(spec.key_features + spec.constraints).lower()
    
    # 1. UNUSUAL SCALE
    if spec.expected_users > 10000000 and "scaling" not in ft_str:
        risks.append(RiskyDecision(
            decision_type="scaling",
            reason="Extremely high scale without explicit scaling strategy.",
            impact="high",
            why_needs_deep_thinking="Base architectures will fail at 10M+ without precise horizontal and sharding strategies."
        ))
    if spec.latency_requirement_ms < 100 and "cache" not in ft_str:
        risks.append(RiskyDecision(
            decision_type="performance",
            reason="Sub-100ms latency without explicit caching.",
            impact="high",
            why_needs_deep_thinking="Requires deep caching/CDN/Edge deployment configurations."
        ))
        
    # 2. SECURITY & COMPLIANCE
    if spec.data_sensitivity == "pii" and "gdpr" not in ft_str and "hipaa" not in ft_str:
        risks.append(RiskyDecision(
            decision_type="security",
            reason="PII data handling but missing GDPR/HIPAA compliance notes.",
            impact="critical",
            why_needs_deep_thinking="Need strictly reviewed encryption, isolation, and data retention policies."
        ))
    if "payment" in ft_str and "pci" not in ft_str:
        risks.append(RiskyDecision(
            decision_type="security",
            reason="Payment handling mentioned without PCI compliance strategy.",
            impact="critical",
            why_needs_deep_thinking="Financial data has catastrophic failure modes. Needs isolation."
        ))
        
    # 3. NOVEL DOMAIN COMBINATIONS
    if "ai" in ft_str and "real-time" in ft_str and "streaming" in ft_str:
        risks.append(RiskyDecision(
            decision_type="complexity",
            reason="Real-time AI streaming is extremely non-standard.",
            impact="high",
            why_needs_deep_thinking="Requires low-latency LLM streaming over WebSockets + Vector processing constraints."
        ))
        
    # 4. TECH MISMATCH
    if spec.team_size <= 1 and (spec.budget_usd > 50000 or "kubernetes" in ft_str):
        risks.append(RiskyDecision(
            decision_type="operational",
            reason="Team size of 1 with complex/expensive architecture.",
            impact="medium",
            why_needs_deep_thinking="High risk of ops burden. Should fallback to serverless/managed paths if possible."
        ))
        
    if spec.timeline_weeks < 4 and len(spec.key_features) > 10:
        risks.append(RiskyDecision(
            decision_type="schedule",
            reason="Tight timeline with enormous feature set.",
            impact="medium",
            why_needs_deep_thinking="Needs aggressive MVP scoping / COTS recommendations."
        ))

    logger.info("detecting_risky_decisions_complete", risks_found=len(risks))
    return risks
