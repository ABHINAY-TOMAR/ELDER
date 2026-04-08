import logging
from typing import List, Dict, Any, Literal
from app.models.requirement_spec import RequirementSpec
from app.engines.fast_pattern_matcher import StackRecommendation, RiskyDecision

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RiskyDecisionDetector:
    """
    Identifies architectural choices that shouldn't be templated.
    These are decisions that need deeper reasoning (Claude Sonnet 4 extended thinking).
    """

    def detect(self, spec: RequirementSpec, fast_rec: StackRecommendation) -> List[RiskyDecision]:
        """
        Analyze requirements and the proposed fast-path stack for potential risks.
        """
        risky_decisions = []

        # --- 1. Unusual Scale ---
        if spec.expected_users > 1_000_000:
            risky_decisions.append(RiskyDecision(
                decision_type="scaling",
                reason=f"Massive scale requirement ({spec.expected_users} users) detected.",
                impact="high",
                why_needs_deep_thinking="Standard PostgreSQL/Redis templates may hit limits; requires evaluation of sharding, global distribution, or Spanner-like DBs."
            ))
        
        if spec.latency_requirement_ms < 50:
            risky_decisions.append(RiskyDecision(
                decision_type="performance",
                reason=f"Extreme latency requirement ({spec.latency_requirement_ms}ms) detected.",
                impact="high",
                why_needs_deep_thinking="Requires evaluating Edge computing, specialized network protocols, or C++/Rust core services."
            ))

        # --- 2. Security & Compliance ---
        if spec.data_sensitivity == "regulated" or spec.data_sensitivity == "pii":
            risks_found = []
            if "compliance" not in " ".join(spec.constraints).lower():
                risks_found.append("No explicit compliance strategy mentioned for sensitive data.")
            if "encryption" not in " ".join(spec.constraints).lower():
                risks_found.append("No encryption requirements specified.")
            
            if risks_found:
                risky_decisions.append(RiskyDecision(
                    decision_type="security",
                    reason=" ".join(risks_found),
                    impact="high",
                    why_needs_deep_thinking="Sensitive data handling must be architected with clear encryption, audit, and retention policies."
                ))

        # --- 3. Technology Mismatch / Constraints ---
        # If constraints explicitly conflict with fast recommendation
        for constraint in spec.constraints:
            constraint_lower = constraint.lower()
            if "must use" in constraint_lower:
                for category, tech in fast_rec.tech_stack.items():
                    # If user says "must use MongoDB" but we recommend PostgreSQL
                    if "mongodb" in constraint_lower and "postgresql" in tech.lower():
                        risky_decisions.append(RiskyDecision(
                            decision_type="database",
                            reason=f"Constraint '{constraint}' conflicts with recommended {tech}.",
                            impact="medium",
                            why_needs_deep_thinking="Requires analyzing if the forced database can actually support the requirements (transactions vs scale)."
                        ))
                        break

        # --- 4. Complexity vs Team ---
        if spec.team_size == 1 and len(spec.extracted_features) > 8:
            risky_decisions.append(RiskyDecision(
                decision_type="complexity",
                reason=f"High complexity ({len(spec.extracted_features)} features) for a solo engineer.",
                impact="medium",
                why_needs_deep_thinking="Requires aggressive prioritization or serverless/managed-only stack to ensure project viability."
            ))

        # --- 5. Novel Domain Combinations ---
        if spec.domain == "ai_native" and "streaming" in " ".join(spec.extracted_features).lower():
             risky_decisions.append(RiskyDecision(
                decision_type="real-time-ai",
                reason="AI Agent logic combined with real-time streaming data.",
                impact="high",
                why_needs_deep_thinking="Requires careful orchestration to avoid inference latency blocking the data stream."
            ))

        logger.info(f"Detected {len(risky_decisions)} risky decisions for project {spec.project_name}.")
        return risky_decisions
