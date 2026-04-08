import logging
from typing import List, Dict, Any, Literal
from app.models.architecture import Architecture, Service, FailureMode

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FailureModeMapper:
    """
    Identifies common and specific failure modes for each service in the architecture.
    """

    def map_failures(self, arch: Architecture) -> List[FailureMode]:
        """
        Produce a list of FailureMode objects for all services.
        """
        all_failures = []
        for service in arch.services:
            failures = self._get_failures_for_service(service, arch.domain)
            all_failures.extend(failures)
        return all_failures

    def _get_failures_for_service(self, service: Service, domain: str) -> List[FailureMode]:
        """
        Identify top 3 failure modes based on service type and domain.
        """
        failures = []

        # 1. Generic availability failure (common to almost all)
        failures.append(FailureMode(
            service_id=service.id,
            mode="Service Availability Loss",
            probability="low",
            impact="Critical - Service unresponsive",
            detection="Heartbeat/Health check timeout (>5s)",
            mitigation="Auto-restart via orchestrator (K8s), multi-zone replicas"
        ))

        # 2. Domain-specific failures
        if domain == "microservices":
            failures.append(FailureMode(
                service_id=service.id,
                mode="Database Connection Timeout",
                probability="medium",
                impact="High - Data operations fail",
                detection="Exception: Connection pool exhausted",
                mitigation="Connection pooling, query timeout, read-replicas"
            ))
            failures.append(FailureMode(
                service_id=service.id,
                mode="API Latency Spike",
                probability="medium",
                impact="Medium - Degraded user experience",
                detection="P99 Latency > 2s",
                mitigation="Caching, circuit breakers, autoscaling"
            ))

        elif domain == "ai_native":
            failures.append(FailureMode(
                service_id=service.id,
                mode="Model Hallucination",
                probability="medium",
                impact="High - Incorrect/Unsafe response",
                detection="Confidence score < 0.7 or validation check failed",
                mitigation="RAG consistency check, human-in-the-loop, retry with temp=0"
            ))
            failures.append(FailureMode(
                service_id=service.id,
                mode="Vector DB Search Failure",
                probability="low",
                impact="High - Context loss for agents",
                detection="Query returns zero results or connection error",
                mitigation="Fallback to generic prompt, vector index redundancy"
            ))

        elif domain == "data_pipeline":
            failures.append(FailureMode(
                service_id=service.id,
                mode="Data Schema Mismatch",
                probability="medium",
                impact="High - Pipeline halts or corrupts data",
                detection="Schema validation error at ingestion",
                mitigation="DLQ (Dead Letter Queue), schema evolution enforcement"
            ))
            failures.append(FailureMode(
                service_id=service.id,
                mode="Storage Quota Exceeded",
                probability="low",
                impact="Critical - Data loss",
                detection="Write error: Insufficient space",
                mitigation="Old data archival to S3, proactive alerting at 80% usage"
            ))

        return failures[:3] # Ensure exactly top 3
