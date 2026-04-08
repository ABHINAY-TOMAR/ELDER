import logging
from typing import List, Dict, Set
from collections import deque
from app.models.architecture import Architecture, Service, Phase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImplementationPlanner:
    """
    Groups services into logical implementation phases based on their dependency graph.
    """

    def plan(self, arch: Architecture) -> List[Phase]:
        """
        Create an ordered list of implementation phases.
        """
        logger.info(f"Planning implementation for {arch.project_name}...")
        
        # 1. Build adjacency list and in-degree map
        adj = {s.id: [] for s in arch.services}
        in_degree = {s.id: 0 for s in arch.services}
        
        for s in arch.services:
            for dep in s.dependencies:
                # dep is a service_id that 's' depends on
                if dep in adj:
                    adj[dep].append(s.id)
                    in_degree[s.id] += 1

        # 2. Group into layers (Kahn's algorithm variant)
        phases = []
        phase_num = 1
        
        processed_ids: Set[str] = set()
        
        while len(processed_ids) < len(arch.services):
            # Find all services with 0 in-degree among remaining services
            current_layer = [
                s_id for s_id in in_degree 
                if in_degree[s_id] == 0 and s_id not in processed_ids
            ]
            
            if not current_layer:
                # Circular dependency or missing dependency link
                remaining = [s_id for s_id in in_degree if s_id not in processed_ids]
                logger.error(f"Circular dependency detected among: {remaining}")
                # Fallback: just group everything remaining into a 'Final' phase
                current_layer = remaining

            # Create phase
            name = self._get_phase_name(phase_num)
            phases.append(Phase(
                phase_number=phase_num,
                name=name,
                service_ids=current_layer,
                description=f"Implementation of {', '.join(current_layer)}.",
                dependencies=[phase_num - 1] if phase_num > 1 else []
            ))

            # Update in-degrees for next layer
            for s_id in current_layer:
                processed_ids.add(s_id)
                for neighbor in adj.get(s_id, []):
                    in_degree[neighbor] -= 1
            
            phase_num += 1

        return phases

    def _get_phase_name(self, num: int) -> str:
        names = {
            1: "Foundation & Core Infrastructure",
            2: "Primary Business Logic",
            3: "Secondary Services & Integrations",
            4: "Extended Features & Optimization"
        }
        return names.get(num, f"Expansion Phase {num}")
