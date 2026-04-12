"""
Comprehensive OpenEnv Test Runner
Validates all test cases across all 3 tasks with detailed reporting.
"""

import asyncio
import json
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime

from app.openenv.interface import OpenEnvInterface
from app.openenv.test_cases import TASK_1_TEST_CASES, TASK_2_TEST_CASES, TASK_3_TEST_CASES
from app.models.schemas import Action
from app.models.architecture import Architecture


@dataclass
class TestResult:
    """Result of a single test execution."""
    test_id: str
    task_id: str
    test_name: str
    passed: bool
    score: float
    error: str | None = None
    evidence: str | None = None


@dataclass
class TaskSummary:
    """Summary of all tests for a task."""
    task_id: str
    task_name: str
    total_tests: int
    passed: int
    failed: int
    avg_score: float
    min_score: float
    max_score: float


class OpenEnvTestRunner:
    """Runs OpenEnv test suite and collects results."""

    def __init__(self):
        self.interface = OpenEnvInterface()
        self.results: List[TestResult] = []
        self.task_map = {
            "task_stack_recommendation": ("Task 1: Tech Stack Recommendation", TASK_1_TEST_CASES),
            "task_anti_pattern_detection": ("Task 2: Anti-Pattern Detection", TASK_2_TEST_CASES),
            "task_full_design_integration": ("Task 3: Full Design Integration", TASK_3_TEST_CASES),
        }

    async def run_task_1(self) -> List[TestResult]:
        """Run all Task 1 (Tech Stack) test cases."""
        task_results = []
        
        for test_case in TASK_1_TEST_CASES:
            test_id = test_case["id"]
            task_id = test_case["task_id"]
            description = test_case["description"]
            ground_truth = test_case.get("ground_truth", {})
            
            try:
                # Reset the environment
                obs = await self.interface.reset(task_id)
                
                # Submit the ground truth as the action
                action = Action(
                    task_id=task_id,
                    payload=ground_truth
                )
                reward = await self.interface.step(action)
                
                # For ground truth submission, we expect high scores
                passed = reward.score >= 0.95
                result = TestResult(
                    test_id=test_id,
                    task_id=task_id,
                    test_name=description,
                    passed=passed,
                    score=reward.score,
                    evidence=reward.observation.message,
                )
                task_results.append(result)
                
            except Exception as e:
                result = TestResult(
                    test_id=test_id,
                    task_id=task_id,
                    test_name=description,
                    passed=False,
                    score=0.0,
                    error=str(e),
                )
                task_results.append(result)
        
        self.results.extend(task_results)
        return task_results

    async def run_task_2(self) -> List[TestResult]:
        """Run all Task 2 (Anti-Pattern) test cases."""
        task_results = []
        
        for test_case in TASK_2_TEST_CASES:
            test_id = test_case["id"]
            task_id = test_case["task_id"]
            description = test_case["description"]
            ground_truth_patterns = test_case.get("ground_truth_patterns", {})
            
            try:
                # Reset the environment
                obs = await self.interface.reset(task_id)
                
                # Extract pattern names from ground truth
                pattern_findings = list(ground_truth_patterns.keys())
                
                # Submit findings
                action = Action(
                    task_id=task_id,
                    payload={"findings": pattern_findings}
                )
                reward = await self.interface.step(action)
                
                # For ground truth submission, we expect high scores
                passed = reward.score >= 0.95
                result = TestResult(
                    test_id=test_id,
                    task_id=task_id,
                    test_name=description,
                    passed=passed,
                    score=reward.score,
                    evidence=reward.observation.message,
                )
                task_results.append(result)
                
            except Exception as e:
                result = TestResult(
                    test_id=test_id,
                    task_id=task_id,
                    test_name=description,
                    passed=False,
                    score=0.0,
                    error=str(e),
                )
                task_results.append(result)
        
        self.results.extend(task_results)
        return task_results

    async def run_task_3(self) -> List[TestResult]:
        """Run all Task 3 (Full Design) test cases."""
        task_results = []
        
        for test_case in TASK_3_TEST_CASES:
            test_id = test_case["id"]
            task_id = test_case["task_id"]
            description = test_case["description"]
            ground_truth_architecture = test_case.get("ground_truth_architecture", {})
            
            try:
                # Reset the environment
                obs = await self.interface.reset(task_id)
                
                # Submit the ground truth architecture
                action = Action(
                    task_id=task_id,
                    payload=ground_truth_architecture
                )
                reward = await self.interface.step(action)
                
                # For ground truth submission, we expect high scores
                passed = reward.score >= 0.95
                result = TestResult(
                    test_id=test_id,
                    task_id=task_id,
                    test_name=description,
                    passed=passed,
                    score=reward.score,
                    evidence=reward.observation.message,
                )
                task_results.append(result)
                
            except Exception as e:
                result = TestResult(
                    test_id=test_id,
                    task_id=task_id,
                    test_name=description,
                    passed=False,
                    score=0.0,
                    error=str(e),
                )
                task_results.append(result)
        
        self.results.extend(task_results)
        return task_results

    async def run_all(self) -> Dict[str, Any]:
        """Run all test suites and return comprehensive report."""
        print("=" * 80)
        print("ELDER OpenEnv Test Runner - Starting Comprehensive Test Suite")
        print(f"Start Time: {datetime.now().isoformat()}")
        print("=" * 80)
        
        # Run all tasks
        print("\n[1/3] Running Task 1: Tech Stack Recommendation...")
        task1_results = await self.run_task_1()
        print(f"  ✓ Completed {len(task1_results)} test cases")
        
        print("\n[2/3] Running Task 2: Anti-Pattern Detection...")
        task2_results = await self.run_task_2()
        print(f"  ✓ Completed {len(task2_results)} test cases")
        
        print("\n[3/3] Running Task 3: Full Design Integration...")
        task3_results = await self.run_task_3()
        print(f"  ✓ Completed {len(task3_results)} test cases")
        
        # Compile summary
        return self._generate_report()

    def _generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_tests": len(self.results),
            "passed": sum(1 for r in self.results if r.passed),
            "failed": sum(1 for r in self.results if not r.passed),
            "avg_score": sum(r.score for r in self.results) / max(len(self.results), 1),
            "tasks": {},
            "details": [asdict(r) for r in self.results],
        }
        
        # Summarize by task
        for task_id in ["task_stack_recommendation", "task_anti_pattern_detection", "task_full_design_integration"]:
            task_results = [r for r in self.results if r.task_id == task_id]
            if task_results:
                task_name, _ = self.task_map[task_id]
                scores = [r.score for r in task_results]
                report["tasks"][task_id] = {
                    "name": task_name,
                    "total": len(task_results),
                    "passed": sum(1 for r in task_results if r.passed),
                    "failed": sum(1 for r in task_results if not r.passed),
                    "avg_score": sum(scores) / len(scores),
                    "min_score": min(scores),
                    "max_score": max(scores),
                }
        
        return report

    def print_summary(self, report: Dict[str, Any]) -> None:
        """Print human-readable test summary."""
        print("\n" + "=" * 80)
        print("TEST EXECUTION SUMMARY")
        print("=" * 80)
        
        print(f"\nTotal Tests: {report['total_tests']}")
        print(f"  ✓ Passed: {report['passed']}")
        print(f"  ✗ Failed: {report['failed']}")
        print(f"  Average Score: {report['avg_score']:.4f}")
        
        print("\n" + "-" * 80)
        print("TASK BREAKDOWN")
        print("-" * 80)
        
        for task_id, task_summary in report["tasks"].items():
            print(f"\n{task_summary['name']}")
            print(f"  Total: {task_summary['total']} | Passed: {task_summary['passed']} | Failed: {task_summary['failed']}")
            print(f"  Score Range: {task_summary['min_score']:.4f} - {task_summary['max_score']:.4f}")
            print(f"  Average: {task_summary['avg_score']:.4f}")
        
        print("\n" + "=" * 80)
        if report['failed'] == 0:
            print("✓ ALL TESTS PASSED")
        else:
            print(f"✗ {report['failed']} TESTS FAILED - Review details above")
        print("=" * 80)


async def main():
    """Run the test suite."""
    runner = OpenEnvTestRunner()
    report = await runner.run_all()
    runner.print_summary(report)
    
    # Return exit code
    return 0 if report['failed'] == 0 else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
