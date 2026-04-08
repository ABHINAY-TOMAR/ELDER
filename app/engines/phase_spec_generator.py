import logging
from typing import List
from app.models.architecture import Architecture, Phase, Service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PhaseSpecGenerator:
    """
    Generates detailed markdown specifications for implementation phases.
    These specs are intended to be consumed by developer agents (e.g., Claude Code).
    """

    def generate_specs(self, arch: Architecture, phases: List[Phase]) -> List[Phase]:
        """
        Populate the spec_markdown field for each phase.
        """
        for phase in phases:
            phase.spec_markdown = self._build_markdown(arch, phase)
        return phases

    def _build_markdown(self, arch: Architecture, phase: Phase) -> str:
        """
        Construct the markdown text for a single phase.
        """
        service_details = []
        for s_id in phase.service_ids:
            # Find service object
            svc = next((s for s in arch.services if s.id == s_id), None)
            if svc:
                endpoints_list = "\n".join([f"  - {e}" for e in svc.endpoints])
                service_details.append(f"""
### Service: {svc.name} (`{svc.id}`)
- **Description**: {svc.description}
- **Stack**: {svc.stack}
- **Endpoints to Implement**:
{endpoints_list or "  - N/A (Internal component)"}
- **Dependencies**: {', '.join(svc.dependencies) or "None"}
""")

        spec = f"""# Phase {phase.phase_number}: {phase.name}

## Overview
{phase.description}

## Architecture Context
- **Project**: {arch.project_name}
- **Domain**: {arch.domain}
- **Global Tech Stack**: {arch.tech_stack}

## Services to Build
{''.join(service_details)}

## Success Criteria
1. All services in this phase are containerized and pass health checks.
2. API contracts defined above are fully implemented and validated.
3. Unit tests achieve > 80% coverage.
4. Services can communicate with their dependencies.

## Instructions for Developer Agent
- Initialize the project structure for each service.
- Follow the defined tech stack strictly.
- Ensure all endpoints match the specifications.
- Provide a README.md for each service with setup instructions.
"""
        return spec.strip()
