#!/usr/bin/env python3
"""
Quick validation script for OpenEnv implementation
Tests that all core components are working correctly
"""

import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all modules can be imported"""
    print("🔍 Testing imports...")
    try:
        from app.models import (
            Observation, Action, Reward,
            Task1Requirements, StackRecommendation,
            Task2Input, AntiPattern,
            Task3Input, ArchitectureDesign,
            StepRequest, StepResponse,
            ResetRequest, StateResponse,
            TasksResponse, TaskDefinition,
            GraderRequest, GraderResponse,
            BaselineResponse
        )
        print("  ✅ All models imported successfully")
        return True
    except ImportError as e:
        print(f"  ❌ Import failed: {e}")
        return False

def test_pydantic_models():
    """Test that Pydantic models validate correctly"""
    print("\n🔍 Testing Pydantic models...")
    try:
        from app.models import Action, Observation, Reward
        from datetime import datetime
        
        # Test Action model
        action = Action(
            action_type="recommend_stack",
            stack_recommendation={
                "api_framework": "fastapi",
                "database": "postgresql",
                "cache_layer": "redis",
                "message_queue": "rabbitmq",
                "monitoring": "prometheus"
            },
            reasoning="Test recommendation"
        )
        print(f"  ✅ Action model validated: {action.action_type}")
        
        # Test Observation model
        observation = Observation(
            task_id="task_stack_recommendation",
            episode_state={"step": 1, "phase": "test"},
            available_actions=["recommend_stack"],
            timestamp=datetime.now()
        )
        print(f"  ✅ Observation model validated: {observation.task_id}")
        
        # Test Reward model
        reward = Reward(
            score=0.85,
            info="Test reward",
            success=True
        )
        print(f"  ✅ Reward model validated: score={reward.score}")
        
        # Test that invalid data is rejected
        try:
            invalid_reward = Reward(score=1.5)  # Should fail (> 1.0)
            print("  ❌ Validation should have failed for score > 1.0")
            return False
        except Exception:
            print("  ✅ Validation correctly rejected score > 1.0")
        
        return True
    except Exception as e:
        print(f"  ❌ Model validation failed: {e}")
        return False

def test_app_creation():
    """Test that FastAPI app can be created"""
    print("\n🔍 Testing FastAPI app creation...")
    try:
        from app.main import app
        print(f"  ✅ FastAPI app created: {app.title}")
        print(f"  ✅ Version: {app.version}")
        return True
    except Exception as e:
        print(f"  ❌ App creation failed: {e}")
        return False

def test_openenv_yaml():
    """Test that openenv.yaml exists and is valid"""
    print("\n🔍 Testing openenv.yaml...")
    try:
        import yaml
        yaml_file = Path(__file__).parent / "openenv.yaml"
        
        if not yaml_file.exists():
            print(f"  ❌ openenv.yaml not found at {yaml_file}")
            return False
        
        with open(yaml_file) as f:
            config = yaml.safe_load(f)
        
        required_fields = ['name', 'description', 'version', 'domains', 'tasks']
        for field in required_fields:
            if field not in config:
                print(f"  ❌ Missing required field: {field}")
                return False
        
        print(f"  ✅ openenv.yaml valid")
        print(f"     Name: {config['name']}")
        print(f"     Version: {config['version']}")
        print(f"     Tasks: {len(config['tasks'])}")
        
        return True
    except Exception as e:
        print(f"  ❌ YAML validation failed: {e}")
        return False

def test_dockerfile():
    """Test that Dockerfile exists"""
    print("\n🔍 Testing Dockerfile...")
    try:
        dockerfile = Path(__file__).parent / "Dockerfile"
        
        if not dockerfile.exists():
            print(f"  ❌ Dockerfile not found")
            return False
        
        content = dockerfile.read_text()
        
        # Check for required elements
        checks = [
            ("FROM python", "Base image"),
            ("EXPOSE 7860", "Port exposure"),
            ("CMD", "Start command"),
            ("uvicorn", "Uvicorn command")
        ]
        
        for check, description in checks:
            if check in content:
                print(f"  ✅ {description} found")
            else:
                print(f"  ❌ {description} missing")
                return False
        
        return True
    except Exception as e:
        print(f"  ❌ Dockerfile check failed: {e}")
        return False

def main():
    """Run all validation tests"""
    print("=" * 70)
    print("🏛️  ARCHITECT AGENT - OpenEnv Foundation Validation")
    print("=" * 70)
    
    tests = [
        ("Imports", test_imports),
        ("Pydantic Models", test_pydantic_models),
        ("FastAPI App", test_app_creation),
        ("OpenEnv YAML", test_openenv_yaml),
        ("Dockerfile", test_dockerfile),
    ]
    
    results = {}
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"\n❌ Test '{name}' crashed: {e}")
            results[name] = False
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 VALIDATION SUMMARY")
    print("=" * 70)
    
    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status:12} {name}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n🎉 All validation tests passed!")
        print("✅ Foundation is ready for implementation")
        return 0
    else:
        print("\n⚠️  Some tests failed - review errors above")
        return 1

if __name__ == "__main__":
    sys.exit(main())
