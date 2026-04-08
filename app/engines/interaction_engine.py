class InteractionEngine:
    """ 
    Evaluates the user's prompt against required architectural fields 
    and generates Multiple-Choice Questions (MCQ) to gather missing context.
    """
    
    def analyze_requirements(self, prompt: str, current_state: dict) -> dict:
        """
        Takes the prompt and the current state to figure out what's missing.
        It progresses sequentially until all major fields are filled.
        Returns a question object with multiple choice options if incomplete.
        """
        required_fields = ["project_type", "tech_stack", "scale_budget"]
        missing_fields = [f for f in required_fields if current_state.get(f) is None]
            
        if not missing_fields:
            return {"status": "complete", "message": "All requirements gathered. Ready for architecture generation."}
            
        next_missing = missing_fields[0]
        
        question_schema = {
            "project_type": {
                "question": "What best describes the domain of the architecture you want to build?",
                "options": [
                    {"id": "ai_native", "label": "AI-Native App (Agents, RAG, LLMs)", "recommended": True},
                    {"id": "ecommerce", "label": "E-Commerce / Marketplace", "recommended": True},
                    {"id": "data_pipeline", "label": "High-throughput Data Pipeline", "recommended": True},
                    {"id": "other", "label": "Other (Please type below)", "recommended": False}
                ]
            },
            "tech_stack": {
                "question": "Which backend ecosystem does your team prefer or require?",
                "options": [
                    {"id": "python-fastapi", "label": "Python (FastAPI + PostgreSQL)", "recommended": True},
                    {"id": "node-express", "label": "Node.js (Express/Nest + Document DB)", "recommended": True},
                    {"id": "go-grpc", "label": "Go (gRPC + Core DB) for max performance", "recommended": True},
                    {"id": "other", "label": "Other (Please specify)", "recommended": False}
                ]
            },
            "scale_budget": {
                 "question": "What is the expected scale or monthly infrastructure budget?",
                 "options": [
                    {"id": "low", "label": "< $500 / month (Startup MVP)", "recommended": True},
                    {"id": "medium", "label": "$1k - $5k / month (Growth)", "recommended": True},
                    {"id": "high", "label": "> $10k / month (Enterprise Scale)", "recommended": False},
                    {"id": "other", "label": "Other (Please specify)", "recommended": False}
                 ]
            }
        }
        
        return {
            "status": "incomplete",
            "field": next_missing,
            "prompt": question_schema.get(next_missing)
        }

interaction_engine = InteractionEngine()
