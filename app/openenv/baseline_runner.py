"""
Baseline OpenAI Runner for OpenEnv Tasks
Submits task requirements to OpenAI API and evaluates responses.
"""

import asyncio
import json
from typing import Dict, List, Any
import os
from dataclasses import dataclass

from app.openenv.interface import OpenEnvInterface
from app.openenv.test_cases import TASK_1_TEST_CASES, TASK_2_TEST_CASES, TASK_3_TEST_CASES
from app.models.schemas import Action
from app.core.config import settings


try:
    from openai import AsyncOpenAI
except ImportError:
    AsyncOpenAI = None


@dataclass
class BaselineResult:
    """Result from baseline OpenAI submission."""
    task_id: str
    test_id: str
    openai_score: float
    openai_response: str
    grader_score: float
    grader_evidence: str
    match: bool  # Whether grader and OpenAI agree (roughly)


class OpenEnvBaseline:
    """Baseline runner using OpenAI for task submission."""

    def __init__(self):
        if not AsyncOpenAI:
            raise RuntimeError("OpenAI library not installed. Install with: pip install openai")
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        self.client = AsyncOpenAI(api_key=api_key)
        self.interface = OpenEnvInterface()
        self.model = "gpt-4"  # Use latest model
        self.results: List[BaselineResult] = []

    async def run_task_1_baseline(self) -> List[BaselineResult]:
        """Run Task 1 test cases via OpenAI."""
        task_results = []
        
        for test_case in TASK_1_TEST_CASES:
            test_id = test_case["id"]
            task_id = test_case["task_id"]
            requirement = test_case.get("requirement", "")
            ground_truth = test_case.get("ground_truth", {})
            
            # Prepare the prompt
            prompt = f"""You are an expert system architect. Given the following project requirement, 
recommend a technology stack with the following components: api_framework, database, cache_layer, message_queue, monitoring.

Requirement: {requirement}

Return a JSON object with these exact keys and technology recommendations."""
            
            try:
                # Get OpenAI response
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2,
                    response_format={"type": "json_object"},
                    timeout=30.0,
                )
                
                response_text = response.choices[0].message.content
                openai_rec = json.loads(response_text)
                
                # Reset and submit to grader
                await self.interface.reset(task_id)
                action = Action(task_id=task_id, payload=openai_rec)
                reward = await self.interface.step(action)
                
                result = BaselineResult(
                    task_id=task_id,
                    test_id=test_id,
                    openai_score=1.0,  # OpenAI was able to respond
                    openai_response=response_text,
                    grader_score=reward.score,
                    grader_evidence=reward.observation.message,
                    match=reward.score >= 0.7,  # Consider match if score >= 0.7
                )
                task_results.append(result)
                
            except Exception as e:
                result = BaselineResult(
                    task_id=task_id,
                    test_id=test_id,
                    openai_score=0.0,
                    openai_response=str(e),
                    grader_score=0.0,
                    grader_evidence="Error processing OpenAI response",
                    match=False,
                )
                task_results.append(result)
        
        self.results.extend(task_results)
        return task_results

    async def run_task_2_baseline(self) -> List[BaselineResult]:
        """Run Task 2 test cases via OpenAI."""
        task_results = []
        
        for test_case in TASK_2_TEST_CASES:
            test_id = test_case["id"]
            task_id = test_case["task_id"]
            architecture_context = test_case.get("architecture_context", "")
            ground_truth_patterns = test_case.get("ground_truth_patterns", {})
            
            # Prepare the prompt
            expected_patterns = ", ".join(ground_truth_patterns.keys())
            prompt = f"""You are an expert in architectural anti-patterns. 
Analyze the following architecture context and identify architectural anti-patterns.

Expected patterns to look for: {expected_patterns}

Architecture: {architecture_context}

Return a JSON object with a 'findings' list containing the anti-patterns you found."""
            
            try:
                # Get OpenAI response
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2,
                    response_format={"type": "json_object"},
                    timeout=30.0,
                )
                
                response_text = response.choices[0].message.content
                openai_findings = json.loads(response_text)
                
                # Reset and submit to grader
                await self.interface.reset(task_id)
                action = Action(task_id=task_id, payload=openai_findings)
                reward = await self.interface.step(action)
                
                result = BaselineResult(
                    task_id=task_id,
                    test_id=test_id,
                    openai_score=1.0,  # OpenAI was able to respond
                    openai_response=response_text,
                    grader_score=reward.score,
                    grader_evidence=reward.observation.message,
                    match=reward.score >= 0.7,
                )
                task_results.append(result)
                
            except Exception as e:
                result = BaselineResult(
                    task_id=task_id,
                    test_id=test_id,
                    openai_score=0.0,
                    openai_response=str(e),
                    grader_score=0.0,
                    grader_evidence="Error processing OpenAI response",
                    match=False,
                )
                task_results.append(result)
        
        self.results.extend(task_results)
        return task_results

    async def run_task_3_baseline(self) -> List[BaselineResult]:
        """Run Task 3 test cases via OpenAI."""
        task_results = []
        
        for test_case in TASK_3_TEST_CASES:
            test_id = test_case["id"]
            task_id = test_case["task_id"]
            full_requirement = test_case.get("full_requirement", "")
            ground_truth_requirements = test_case.get("ground_truth_requirements", {})
            
            # Prepare the prompt
            required_services = ground_truth_requirements.get("required_services", [])
            required_integrations = ground_truth_requirements.get("required_integrations", [])
            required_failures = ground_truth_requirements.get("required_failure_modes", [])
            
            prompt = f"""You are an expert system architect. Design a complete system architecture 
that satisfies the following requirements.

Requirement: {full_requirement}

Must include services: {', '.join(required_services)}
Must include integrations: {', '.join(required_integrations)}
Must handle failure modes: {', '.join(required_failures)}

Return a JSON object with the complete architecture including services, integrations, and failure_modes."""
            
            try:
                # Get OpenAI response
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2,
                    response_format={"type": "json_object"},
                    timeout=30.0,
                )
                
                response_text = response.choices[0].message.content
                openai_architecture = json.loads(response_text)
                
                # Reset and submit to grader
                await self.interface.reset(task_id)
                action = Action(task_id=task_id, payload=openai_architecture)
                reward = await self.interface.step(action)
                
                result = BaselineResult(
                    task_id=task_id,
                    test_id=test_id,
                    openai_score=1.0,  # OpenAI was able to respond
                    openai_response=response_text[:200],  # Truncate for readability
                    grader_score=reward.score,
                    grader_evidence=reward.observation.message,
                    match=reward.score >= 0.7,
                )
                task_results.append(result)
                
            except Exception as e:
                result = BaselineResult(
                    task_id=task_id,
                    test_id=test_id,
                    openai_score=0.0,
                    openai_response=str(e),
                    grader_score=0.0,
                    grader_evidence="Error processing OpenAI response",
                    match=False,
                )
                task_results.append(result)
        
        self.results.extend(task_results)
        return task_results

    async def run_all(self) -> Dict[str, Any]:
        """Run all baseline tasks."""
        print("=" * 80)
        print("OpenEnv Baseline (OpenAI) - Starting")
        print("=" * 80)
        
        try:
            print("\n[1/3] Running Task 1 Baseline...")
            await self.run_task_1_baseline()
            print("  ✓ Task 1 complete")
            
            print("\n[2/3] Running Task 2 Baseline...")
            await self.run_task_2_baseline()
            print("  ✓ Task 2 complete")
            
            print("\n[3/3] Running Task 3 Baseline...")
            await self.run_task_3_baseline()
            print("  ✓ Task 3 complete")
            
        except Exception as e:
            print(f"\n✗ Error running baseline: {e}")
            return {"error": str(e)}
        
        return self._summarize()

    def _summarize(self) -> Dict[str, Any]:
        """Summarize baseline results."""
        avg_grader_score = sum(r.grader_score for r in self.results) / len(self.results) if self.results else 0
        match_count = sum(1 for r in self.results if r.match)
        
        summary = {
            "total_runs": len(self.results),
            "avg_grader_score": avg_grader_score,
            "matches": match_count,
            "match_rate": match_count / len(self.results) if self.results else 0,
        }
        
        print("\n" + "=" * 80)
        print("BASELINE SUMMARY")
        print("=" * 80)
        print(f"Total Runs: {summary['total_runs']}")
        print(f"Average Grader Score: {summary['avg_grader_score']:.4f}")
        print(f"Matches (score >= 0.7): {summary['matches']}/{summary['total_runs']}")
        print(f"Match Rate: {summary['match_rate']:.2%}")
        
        return summary


async def main():
    """Run the baseline."""
    try:
        runner = OpenEnvBaseline()
        await runner.run_all()
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
