import logging
from typing import List, Literal, Dict, Any, Tuple
from pydantic import BaseModel, Field
from app.models.requirement_spec import RequirementSpec

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DomainClassification(BaseModel):
    """
    Result of the domain classification process.
    """
    primary_domain: Literal["microservices", "ai_native", "data_pipeline"]
    secondary_domains: List[str] = Field(default_factory=list)
    confidence: float = Field(..., ge=0.0, le=1.0)
    reasoning: str

class DomainClassifier:
    """
    Fast, rule-based classifier that categorizes requirements into architectural domains.
    """

    SIGNALS = {
        "microservices": [
            "api", "rest", "grpc", "microservice", "service oriented", "crud", 
            "scalability", "kubernetes", "docker", "traditional saas", "web app",
            "dashboard", "multi-tenant"
        ],
        "ai_native": [
            "agent", "agentic", "orchestration", "llm", "rag", "autonomous", 
            "vector db", "embedding", "reasoning", "multimodal", "inference",
            "openai", "anthropic", "memory system", "langchain", "crewai"
        ],
        "data_pipeline": [
            "etl", "pipeline", "streaming", "batch", "analytics", "warehouse", 
            "bigquery", "snowflake", "spark", "kafka", "airflow", "transformation",
            "aggregation", "data lake", "delta lake"
        ]
    }

    def classify(self, spec: RequirementSpec) -> DomainClassification:
        """
        Classify a RequirementSpec based on features, constraints, and keywords.
        """
        # 1. Combine all relevant text fields to search for signals
        text_to_analyze = (
            f"{spec.project_name} "
            f"{' '.join(spec.extracted_features)} "
            f"{' '.join(spec.constraints)} "
        ).lower()

        # 2. Score each domain
        scores = {
            "microservices": 0.0,
            "ai_native": 0.0,
            "data_pipeline": 0.0
        }

        # Weighting
        # Direct domain mention in spec (from parser) is a strong hint but we re-verify
        if spec.domain in scores:
            scores[spec.domain] += 2.0

        for domain, keywords in self.SIGNALS.items():
            for keyword in keywords:
                if keyword in text_to_analyze:
                    # Give higher weight to some very specific keywords
                    if domain == "ai_native" and keyword in ["agent", "rag", "autonomous"]:
                        scores[domain] += 1.5
                    elif domain == "data_pipeline" and keyword in ["etl", "pipeline", "batch"]:
                        scores[domain] += 1.5
                    else:
                        scores[domain] += 1.0

        # 3. Rank domains
        sorted_domains = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        primary_domain, primary_score = sorted_domains[0]
        
        # 4. Determine secondary domains (any domain with score > threshold)
        secondary = [d for d, s in sorted_domains[1:] if s > 1.0]

        # 5. Calculate confidence (normalized score)
        total_score = sum(scores.values())
        confidence = primary_score / total_score if total_score > 0 else 0.5
        
        # Clamp confidence for realism
        confidence = min(0.95, max(0.5, confidence))

        # 6. Generate reasoning
        reasons = []
        if primary_score > 0:
            reasons.append(f"Identified strong signals for {primary_domain} in requirements.")
        if secondary:
            reasons.append(f"Detected overlap with {', '.join(secondary)} domain(s).")
        if total_score == 0:
            reasons.append("No specific domain signals found; defaulting to microservices.")

        return DomainClassification(
            primary_domain=primary_domain, # type: ignore
            secondary_domains=secondary,
            confidence=confidence,
            reasoning=" ".join(reasons)
        )
