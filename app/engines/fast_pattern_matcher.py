class FastPatternMatcher:
    """ Rule-based matching for known architectural patterns avoiding expensive API calls. """
    
    def process_fast_recommendation(self, domain: str, users: int, budget: int) -> dict:
        if domain == "ai_native" and budget < 10000:
            return {
                "tech_stack": {"api": "fastapi", "db": "supabase_pgvector"},
                "rationale": "High AI vector capabilities required at low startup threshold.",
                "risky_decisions": ["rate_limit_handling"]
            }
        
        if domain == "microservices" and users > 100000:
            return {
                "tech_stack": {"api": "go-grpc", "db": "postgresql", "queue": "kafka"},
                "rationale": "Massive user scale justifies complex decoupling.",
                "risky_decisions": ["distributed_tracing", "event_consistency"]
            }
            
        return {
            "tech_stack": {"api": "node-express", "db": "postgresql"},
            "rationale": "Standard reliable baseline for unstructured domains.",
            "risky_decisions": ["schema_evolution"]
        }

fast_matcher = FastPatternMatcher()
