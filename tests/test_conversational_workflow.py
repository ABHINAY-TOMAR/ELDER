import os
from app.engines.interaction_engine import interaction_engine
from app.engines.export_engine import export_engine

def test_interaction_engine():
    print("--- Testing Interaction Engine ---")
    current_state = {}
    prompt = "I want to build an e-commerce website."
    
    # Simulate a conversational flow
    for _ in range(4): # Limit looping just in case
        result = interaction_engine.analyze_requirements(prompt, current_state)
        print(f"Status: {result.get('status')}")
        if result.get("status") == "complete":
            break
            
        print(f"Missing Field: {result.get('field')}")
        print(f"Prompt output: {result.get('prompt')}")
        
        # Simulate user providing an answer for the missing field
        current_state[result["field"]] = "mock_value"

def test_export_engine():
    print("--- Testing Export Engine ---")
    mock_arch_data = {
        "domain": "Marketplace",
        "tech_stack": "Python FastAPI + PostgreSQL",
        "scale": "Medium ($10k/month)",
        "details": "This architecture utilizes FastAPI for backend high-concurrency requests, matching users with merchants. Data is stored in high performance PostgreSQL instances. A cache layer is used with Redis."
    }
    
    try:
        pdf_path = export_engine.generate_prd_pdf(mock_arch_data)
        print(f"Generated PRD PDF at: {pdf_path}")
        assert os.path.exists(pdf_path)
    except Exception as e:
         print(f"PDF ERROR: {e}")
         
    try:
        pptx_path = export_engine.generate_architecture_slides(mock_arch_data)
        print(f"Generated Slide Deck at: {pptx_path}")
        assert os.path.exists(pptx_path)
    except Exception as e:
        print(f"PPTX ERROR: {e}")

if __name__ == "__main__":
    test_interaction_engine()
    test_export_engine()
    print("All tests completed successfully.")
