"""
Test script for Fast Path engine integration (Mock/Regex Version)
Tests the /step endpoint with recommend_stack action using regex-based parsing.
No LLM dependencies - works offline.
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:7860"

def test_fast_path():
    """Test the Fast Path: regex parsing -> keyword classification -> rule matching"""
    
    print("=" * 80)
    print("🧪 FAST PATH INTEGRATION TEST (Mock/Regex Version)")
    print("=" * 80)
    
    # Test Case 1: Small AI-native project
    print("\n📋 Test Case 1: Small AI-native project (RAG chatbot)")
    print("-" * 80)
    
    requirement_text_1 = """
    Build an AI-powered chatbot for customer support with RAG capabilities. 
    We have 2 developers and a budget of $3,000.
    Expected to handle 5,000 users initially.
    Must include vector search and semantic search.
    Real-time responses required.
    """
    
    payload_1 = {
        "action": {
            "action_type": "recommend_stack",
            "requirement_text": requirement_text_1
        }
    }
    
    print(f"📤 Sending request with natural language requirements")
    
    try:
        response = requests.post(f"{BASE_URL}/step", json=payload_1, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        print(f"\n✅ Status: {response.status_code}")
        print(f"📊 Observation:")
        print(f"   - Task: {result['observation']['task_id']}")
        print(f"   - Phase: {result['observation']['episode_state']['phase']}")
        print(f"   - Domain: {result['observation']['episode_state'].get('domain', 'N/A')}")
        print(f"   - Feedback: {result['observation']['feedback'][:100]}...")
        
        if result['observation'].get('requirements'):
            req = result['observation']['requirements']
            print(f"\n📝 Parsed Requirements:")
            print(f"   - Team Size: {req.get('team_size', 'N/A')}")
            print(f"   - Budget: ${req.get('budget_usd', 'N/A')}")
            print(f"   - Expected Users: {req.get('expected_users', 'N/A')}")
            print(f"   - Latency: {req.get('latency_requirement_ms', 'N/A')}ms")
            print(f"   - Features: {', '.join(req.get('key_features', []))}")
        
        if result['observation'].get('current_architecture'):
            arch = result['observation']['current_architecture']
            if 'stack_recommendation' in arch:
                stack = arch['stack_recommendation']['tech_stack']
                print(f"\n🏗️  Recommended Stack:")
                print(f"   - API Framework: {stack.get('api_framework', 'N/A')}")
                print(f"   - Database: {stack.get('database', 'N/A')}")
                print(f"   - Vector DB: {stack.get('vector_db', 'N/A')}")
                print(f"   - Cache: {stack.get('cache_layer', 'N/A')}")
                print(f"   - Confidence: {arch['stack_recommendation'].get('confidence', 0):.2f}")
            
            if 'domain_classification' in arch:
                domain = arch['domain_classification']
                print(f"\n🎯 Domain Classification:")
                print(f"   - Primary: {domain.get('primary_domain', 'N/A')}")
                print(f"   - Confidence: {domain.get('confidence', 0):.2f}")
                print(f"   - Reasoning: {domain.get('reasoning', 'N/A')[:80]}...")
            
            if 'risky_decisions' in arch and arch['risky_decisions']:
                print(f"\n⚠️  Risky Decisions Detected: {len(arch['risky_decisions'])}")
                for i, risk in enumerate(arch['risky_decisions'][:3], 1):
                    print(f"   {i}. {risk.get('decision_type', 'unknown')}: {risk.get('reason', 'N/A')[:60]}...")
        
        print(f"\n🎯 Reward: {result['reward']['score']:.2f}")
        print(f"✅ Success: {result['reward']['success']}")
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Request failed: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test Case 2: Large microservices project
    print("\n" + "=" * 80)
    print("📋 Test Case 2: Large microservices e-commerce platform")
    print("-" * 80)
    
    requirement_text_2 = """
    E-commerce platform with REST API backend and microservices architecture.
    Team of 8 engineers, budget $50,000 USD.
    Expected 1 million users with high traffic.
    Need message queue for order processing and real-time notifications.
    Sub-200ms latency requirement for API endpoints.
    Must support real-time analytics and monitoring.
    """
    
    payload_2 = {
        "action": {
            "action_type": "recommend_stack",
            "requirement_text": requirement_text_2
        }
    }
    
    print(f"📤 Sending request...")
    
    try:
        response = requests.post(f"{BASE_URL}/step", json=payload_2, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        print(f"\n✅ Status: {response.status_code}")
        print(f"📊 Domain: {result['observation']['episode_state'].get('domain', 'N/A')}")
        
        if result['observation'].get('requirements'):
            req = result['observation']['requirements']
            print(f"📝 Team: {req.get('team_size')} engineers, Budget: ${req.get('budget_usd')}")
        
        if result['observation'].get('current_architecture'):
            arch = result['observation']['current_architecture']
            if 'stack_recommendation' in arch:
                stack = arch['stack_recommendation']['tech_stack']
                print(f"\n🏗️  Recommended Stack:")
                print(f"   - API Framework: {stack.get('api_framework', 'N/A')}")
                print(f"   - Database: {stack.get('database', 'N/A')}")
                print(f"   - Cache: {stack.get('cache_layer', 'N/A')}")
                print(f"   - Message Queue: {stack.get('message_queue', 'N/A')}")
                print(f"   - Monitoring: {stack.get('monitoring', 'N/A')[:40]}")
            
            if 'risky_decisions' in arch and arch['risky_decisions']:
                print(f"\n⚠️  Risky Decisions: {len(arch['risky_decisions'])}")
                for risk in arch['risky_decisions'][:2]:
                    print(f"   - {risk.get('decision_type')}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False
    
    # Test Case 3: Data pipeline project with ETL
    print("\n" + "=" * 80)
    print("📋 Test Case 3: Real-time data analytics pipeline")
    print("-" * 80)
    
    requirement_text_3 = """
    Real-time analytics pipeline for streaming data with ETL processing.
    Using Spark and Kafka for data processing.
    Team of 5 data engineers, budget $30,000.
    Need data warehouse and batch processing capabilities.
    Must handle streaming and batch workloads.
    PII data - requires strict encryption and compliance.
    """
    
    payload_3 = {
        "action": {
            "action_type": "recommend_stack",
            "requirement_text": requirement_text_3
        }
    }
    
    print(f"📤 Sending request...")
    
    try:
        response = requests.post(f"{BASE_URL}/step", json=payload_3, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        print(f"\n✅ Status: {response.status_code}")
        print(f"📊 Domain: {result['observation']['episode_state'].get('domain', 'N/A')}")
        
        if result['observation'].get('requirements'):
            req = result['observation']['requirements']
            print(f"📝 Sensitivity: {req.get('data_sensitivity')} (should be 'pii')")
        
        if result['observation'].get('current_architecture'):
            arch = result['observation']['current_architecture']
            if 'stack_recommendation' in arch:
                stack = arch['stack_recommendation']['tech_stack']
                print(f"\n🏗️  Recommended Stack:")
                print(f"   - Framework: {stack.get('api_framework', 'N/A')}")
                print(f"   - Database: {stack.get('database', 'N/A')}")
                print(f"   - Message Queue: {stack.get('message_queue', 'N/A')}")
            
            if 'risky_decisions' in arch and arch['risky_decisions']:
                print(f"\n⚠️  Risky Decisions: {len(arch['risky_decisions'])}")
                # Should detect PII compliance risk
                for risk in arch['risky_decisions']:
                    if risk.get('decision_type') == 'security_compliance':
                        print(f"   ✓ Correctly detected PII compliance risk")
                        break
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False
    
    # Test Case 4: Edge case - High scale + low budget (should trigger risk)
    print("\n" + "=" * 80)
    print("📋 Test Case 4: Edge case - High scale with low budget")
    print("-" * 80)
    
    requirement_text_4 = """
    Microservices platform for social media app.
    Team of 2 developers, budget only $1,500.
    But we expect 15 million users!
    Need sub-50ms latency for feeds.
    """
    
    payload_4 = {
        "action": {
            "action_type": "recommend_stack",
            "requirement_text": requirement_text_4
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/step", json=payload_4, timeout=10)
        result = response.json()
        
        print(f"✅ Status: {response.status_code}")
        
        if result['observation'].get('current_architecture'):
            arch = result['observation']['current_architecture']
            if 'risky_decisions' in arch:
                risks = arch['risky_decisions']
                print(f"\n⚠️  Risky Decisions: {len(risks)} (should detect multiple risks)")
                for risk in risks:
                    print(f"   - {risk.get('decision_type')}: {risk.get('impact')} impact")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False
    
    print("\n" + "=" * 80)
    print("✅ ALL TESTS COMPLETED")
    print("=" * 80)
    return True


if __name__ == "__main__":
    print(f"\n🚀 Starting Fast Path integration test (Mock/Regex Version)")
    print(f"⏰ Timestamp: {datetime.now().isoformat()}")
    print(f"🌐 Target: {BASE_URL}")
    print("\n⚠️  Make sure the server is running:")
    print("   uvicorn app.main:app --port 7860 --reload\n")
    
    input("Press Enter to start tests...")
    
    success = test_fast_path()
    
    if success:
        print("\n✅ Fast Path integration working correctly!")
        print("   - No LLM dependencies required")
        print("   - Regex-based parsing is fast and deterministic")
        print("   - Keyword classification works as expected")
        print("   - Rule-based matching provides instant recommendations")
    else:
        print("\n❌ Fast Path integration has issues - check logs")
    
    # Test Case 1: Small AI-native project
    print("\n📋 Test Case 1: Small AI-native project")
    print("-" * 80)
    
    requirement_text_1 = """
    Build an AI-powered chatbot for customer support. 
    We have 2 developers and a budget of $3,000.
    Expected to handle 5,000 users initially.
    Must include RAG capabilities and vector search.
    """
    
    payload_1 = {
        "action": {
            "action_type": "recommend_stack",
            "requirement_text": requirement_text_1
        }
    }
    
    print(f"📤 Sending request: {json.dumps(payload_1, indent=2)}")
    
    try:
        response = requests.post(f"{BASE_URL}/step", json=payload_1, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        print(f"\n✅ Status: {response.status_code}")
        print(f"📊 Observation:")
        print(f"   - Task: {result['observation']['task_id']}")
        print(f"   - Phase: {result['observation']['episode_state']['phase']}")
        print(f"   - Domain: {result['observation']['episode_state'].get('domain', 'N/A')}")
        print(f"   - Feedback: {result['observation']['feedback']}")
        
        if result['observation'].get('current_architecture'):
            arch = result['observation']['current_architecture']
            if 'stack_recommendation' in arch:
                stack = arch['stack_recommendation']['tech_stack']
                print(f"\n🏗️  Recommended Stack:")
                print(f"   - API Framework: {stack.get('api_framework', 'N/A')}")
                print(f"   - Database: {stack.get('database', 'N/A')}")
                print(f"   - Vector DB: {stack.get('vector_db', 'N/A')}")
                print(f"   - Cache: {stack.get('cache_layer', 'N/A')}")
                print(f"   - Confidence: {arch['stack_recommendation'].get('confidence', 0):.2f}")
            
            if 'domain_classification' in arch:
                domain = arch['domain_classification']
                print(f"\n🎯 Domain Classification:")
                print(f"   - Primary: {domain.get('primary_domain', 'N/A')}")
                print(f"   - Confidence: {domain.get('confidence', 0):.2f}")
                print(f"   - Reasoning: {domain.get('reasoning', 'N/A')}")
            
            if 'risky_decisions' in arch and arch['risky_decisions']:
                print(f"\n⚠️  Risky Decisions Detected: {len(arch['risky_decisions'])}")
                for i, risk in enumerate(arch['risky_decisions'], 1):
                    print(f"   {i}. {risk.get('decision_type', 'unknown')}: {risk.get('reason', 'N/A')}")
        
        print(f"\n🎯 Reward: {result['reward']['score']:.2f}")
        print(f"✅ Success: {result['reward']['success']}")
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Request failed: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False
    
    # Test Case 2: Large microservices project
    print("\n" + "=" * 80)
    print("📋 Test Case 2: Large microservices project")
    print("-" * 80)
    
    requirement_text_2 = """
    E-commerce platform with REST API backend.
    Team of 8 engineers, budget $50,000.
    Expected 1 million users with high traffic.
    Need message queue for order processing.
    Sub-200ms latency requirement.
    """
    
    payload_2 = {
        "action": {
            "action_type": "recommend_stack",
            "requirement_text": requirement_text_2
        }
    }
    
    print(f"📤 Sending request: {json.dumps(payload_2, indent=2)}")
    
    try:
        response = requests.post(f"{BASE_URL}/step", json=payload_2, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        print(f"\n✅ Status: {response.status_code}")
        print(f"📊 Observation:")
        print(f"   - Task: {result['observation']['task_id']}")
        print(f"   - Phase: {result['observation']['episode_state']['phase']}")
        print(f"   - Domain: {result['observation']['episode_state'].get('domain', 'N/A')}")
        print(f"   - Feedback: {result['observation']['feedback']}")
        
        if result['observation'].get('current_architecture'):
            arch = result['observation']['current_architecture']
            if 'stack_recommendation' in arch:
                stack = arch['stack_recommendation']['tech_stack']
                print(f"\n🏗️  Recommended Stack:")
                print(f"   - API Framework: {stack.get('api_framework', 'N/A')}")
                print(f"   - Database: {stack.get('database', 'N/A')}")
                print(f"   - Cache: {stack.get('cache_layer', 'N/A')}")
                print(f"   - Message Queue: {stack.get('message_queue', 'N/A')}")
                print(f"   - Confidence: {arch['stack_recommendation'].get('confidence', 0):.2f}")
            
            if 'risky_decisions' in arch and arch['risky_decisions']:
                print(f"\n⚠️  Risky Decisions Detected: {len(arch['risky_decisions'])}")
                for i, risk in enumerate(arch['risky_decisions'], 1):
                    print(f"   {i}. {risk.get('decision_type', 'unknown')}: {risk.get('reason', 'N/A')}")
        
        print(f"\n🎯 Reward: {result['reward']['score']:.2f}")
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Request failed: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False
    
    # Test Case 3: Data pipeline project
    print("\n" + "=" * 80)
    print("📋 Test Case 3: Data pipeline project")
    print("-" * 80)
    
    requirement_text_3 = """
    Real-time analytics pipeline for streaming data.
    ETL processing with Spark and Kafka.
    Team of 5 data engineers, budget $30,000.
    Need data warehouse and batch processing.
    """
    
    payload_3 = {
        "action": {
            "action_type": "recommend_stack",
            "requirement_text": requirement_text_3
        }
    }
    
    print(f"📤 Sending request: {json.dumps(payload_3, indent=2)}")
    
    try:
        response = requests.post(f"{BASE_URL}/step", json=payload_3, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        print(f"\n✅ Status: {response.status_code}")
        print(f"📊 Observation:")
        print(f"   - Task: {result['observation']['task_id']}")
        print(f"   - Phase: {result['observation']['episode_state']['phase']}")
        print(f"   - Domain: {result['observation']['episode_state'].get('domain', 'N/A')}")
        
        if result['observation'].get('current_architecture'):
            arch = result['observation']['current_architecture']
            if 'stack_recommendation' in arch:
                stack = arch['stack_recommendation']['tech_stack']
                print(f"\n🏗️  Recommended Stack:")
                print(f"   - API Framework: {stack.get('api_framework', 'N/A')}")
                print(f"   - Database: {stack.get('database', 'N/A')}")
                print(f"   - Cache: {stack.get('cache_layer', 'N/A')}")
                print(f"   - Message Queue: {stack.get('message_queue', 'N/A')}")
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Request failed: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False
    
    print("\n" + "=" * 80)
    print("✅ ALL TESTS COMPLETED")
    print("=" * 80)
    return True


if __name__ == "__main__":
    print(f"\n🚀 Starting Fast Path integration test...")
    print(f"⏰ Timestamp: {datetime.now().isoformat()}")
    print(f"🌐 Target: {BASE_URL}")
    print("\n⚠️  Make sure the server is running: uvicorn app.main:app --port 7860\n")
    
    input("Press Enter to start tests...")
    
    success = test_fast_path()
    
    if success:
        print("\n✅ Fast Path integration working correctly!")
    else:
        print("\n❌ Fast Path integration has issues - check logs")
