"""
Domain Classifier Engine - Keyword Matching Version
Classifies projects into domains using keyword matching.
No LLM dependencies - fast and deterministic.
"""

from typing import List
from pydantic import BaseModel
import logging

from app.models.schemas import RequirementSpec

logger = logging.getLogger("architect_agent.domain_classifier")


class DomainClassification(BaseModel):
    primary_domain: str
    secondary_domains: List[str]
    confidence: float
    reasoning: str


class DomainClassifier:
    """
    Classifies projects into domains using keyword matching.
    Three domains: microservices, ai_native, data_pipeline
    """
    
    def __init__(self):
        # Domain keywords
        self.domain_keywords = {
            "ai_native": [
                "ai", "agent", "agentic", "llm", "ml", "machine learning",
                "rag", "vector", "embedding", "semantic search",
                "model", "inference", "training", "neural", "gpt", "claude"
            ],
            "microservices": [
                "microservice", "rest", "api", "grpc", "service mesh",
                "kubernetes", "k8s", "docker", "container",
                "gateway", "load balancer", "service discovery",
                "crud", "web", "backend", "frontend", "saas"
            ],
            "data_pipeline": [
                "etl", "pipeline", "streaming", "batch", "data warehouse",
                "analytics", "spark", "airflow", "kafka", "flink",
                "data lake", "warehouse", "dbt", "transform",
                "ingestion", "orchestration"
            ]
        }
    
    def classify(self, spec: RequirementSpec) -> DomainClassification:
        """
        Classify project domain based on RequirementSpec.
        
        Args:
            spec: Parsed requirements
            
        Returns:
            DomainClassification with primary domain and confidence
        """
        logger.info(f"Classifying domain for {len(spec.key_features)} features")
        
        # Text to scan (from key features and constraints)
        text_to_scan = " ".join(spec.key_features + spec.constraints).lower()
        
        # Score each domain
        scores = {
            "ai_native": 0.0,
            "microservices": 0.0,
            "data_pipeline": 0.0
        }
        
        # Count keyword matches
        for domain, keywords in self.domain_keywords.items():
            for keyword in keywords:
                if keyword in text_to_scan:
                    scores[domain] += 1.0
        
        # Apply feature-based boosts
        if "AI" in spec.key_features or "RAG" in spec.key_features:
            scores["ai_native"] += 3.0
        
        if "api" in spec.key_features:
            scores["microservices"] += 2.0
        
        if "ETL" in spec.key_features or "streaming" in spec.key_features:
            scores["data_pipeline"] += 3.0
        
        # Determine primary domain
        max_score = max(scores.values())
        
        if max_score == 0:
            # No clear signals - default to microservices
            primary_domain = "microservices"
            confidence = 0.5
            reasoning = "No strong domain signals detected. Defaulting to microservices as general-purpose domain."
        else:
            primary_domain = max(scores, key=lambda k: scores[k])
            # Normalize confidence (0.6 to 1.0 range)
            confidence = min(0.6 + (max_score / 10.0), 1.0)
            
            matched_keywords = [
                kw for kw in self.domain_keywords[primary_domain]
                if kw in text_to_scan
            ]
            reasoning = f"Detected {primary_domain} domain. Matched keywords: {', '.join(matched_keywords[:5])}"
        
        # Determine secondary domains
        secondary_domains = [
            domain for domain, score in scores.items()
            if domain != primary_domain and score > 0
        ]
        
        classification = DomainClassification(
            primary_domain=primary_domain,
            secondary_domains=secondary_domains,
            confidence=confidence,
            reasoning=reasoning
        )
        
        logger.info(f"Classified as {primary_domain} (confidence: {confidence:.2f})")
        return classification


# Module-level function for backward compatibility
def classify(spec: RequirementSpec) -> DomainClassification:
    """Classify domain (non-async version)"""
    classifier = DomainClassifier()
    return classifier.classify(spec)
