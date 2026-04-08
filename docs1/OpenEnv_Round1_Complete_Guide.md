# OpenEnv Round 1: Complete Hackathon Guide

**Submission Window Opens:** March 28, 2026  
**Round 1 Starts:** April 1, 2026  
**Installation Deadline:** Before April 1, 2026

---

## Quick Start Overview

When Round 1 opens, you will **select 1 of 4-5 problem statements** and build an OpenEnv environment around it. Top 3,000 of 20,000 advancing teams will qualify for the next phase.

---

## Table of Contents

1. [Prerequisites & Setup](#prerequisites--setup)
2. [The Task](#the-task)
3. [Key Requirements at a Glance](#key-requirements-at-a-glance)
4. [Detailed Requirements](#detailed-requirements)
5. [Evaluation Criteria](#evaluation-criteria)
6. [How Judging Works](#how-judging-works)
7. [Pre-Submission Checklist](#pre-submission-checklist)
8. [Common Problem Statement Example](#common-problem-statement-example)

---

## Prerequisites & Setup

### Required: Install Before April 1st

All of the following **must be installed and verified working** before submission:

#### Python 3.10+
Check your version:
```bash
python --version
```
Install Python 3.10, 3.11, or 3.12 if needed.

#### Git + GitHub Account
Verify Git is installed:
```bash
git --version
```
You'll need a GitHub or Hugging Face account to push your submission.

#### OpenEnv Framework
Install the core framework:
```bash
pip install openenv-core
```

#### Docker
Verify Docker installation:
```bash
docker --version
```
Your environment **must containerize** with a working Dockerfile.

#### Hugging Face CLI (for HF Space deployment)
Install and login:
```bash
pip install huggingface_hub --ver
huggingface-cli login
```
You'll deploy your environment as a **Hugging Face Space**.

#### Optional but Recommended: Google Colab
Free tier works fine for prep course runs:  
→ https://colab.research.google.com

#### Optional: VS Code
Best Python + Docker support:  
→ Download from https://code.visualstudio.com

---

## The Task

### What You're Building

**A real-world OpenEnv environment that an AI agent can learn from.**

This is **not a game or toy**. It simulates actual tasks humans perform, such as:
- Email triage
- Code review
- Data cleaning
- Scheduling
- Customer support
- Content moderation

### How It Works

1. You define a **concrete objective** the agent must achieve.
2. You implement the full **OpenEnv interface**: `step()`, `reset()`, `state()`.
3. You create **3+ graded tasks** with increasing difficulty (easy → medium → hard).
4. You write a **grader function** that scores agent performance (0.0–1.0).
5. You design a **reward function** that gives partial credit for progress.
6. You write a **baseline inference script** using OpenAI API.
7. You **containerize everything** and deploy to Hugging Face Spaces.

---

## Key Requirements at a Glance

✅ **Real-world task simulation** (not games, not toys)  
✅ **Full OpenEnv spec compliance**: typed Observation, Action, Reward Pydantic models  
✅ **Minimum 3 tasks** with graders scoring 0.0–1.0  
✅ **Meaningful reward function** (tracks progress, penalizes bad behavior)  
✅ **Baseline inference script** (reproducible scores on all 3 tasks)  
✅ **Docker containerization** (must build and run cleanly)  
✅ **Hugging Face Space deployment** (tagged with `openenv`)  
✅ **Clean, documented README** (environment description, setup, usage)  
✅ **openenv.yaml** with metadata  
✅ **`/baseline`, `/grader`, `/tasks` endpoints** that work correctly

---

## Detailed Requirements

### 1. Real-World Task Simulation

**Must simulate a task humans actually do.**

#### ✅ Good Examples:
- **Email triage**: Agent reads emails, categorizes (urgent/normal/spam), marks for action.
- **Code review**: Agent reads PRs, identifies bugs, suggests fixes, scores quality.
- **Data cleaning**: Agent receives messy data, fills gaps, standardizes formats, verifies completeness.
- **Customer support**: Agent reads tickets, responds, routes to specialist if needed.
- **Content moderation**: Agent reviews user posts, decides (approve/flag/remove), logs decisions.
- **Scheduling**: Agent books meetings, avoids conflicts, respects time zones and availability.

#### ❌ Bad Examples (Disqualifying):
- Turn-based games (Chess, Tic-Tac-Toe, GridWorld).
- Toy environments (simple maze, block stacking).
- Purely synthetic or unrealistic tasks.
- Trivial modifications of existing OpenEnv environments.

---

### 2. OpenEnv Spec Compliance

Your environment **must implement the full OpenEnv interface** with typed Pydantic models.

#### Required Endpoints

```python
# openenv.yaml
name: "Your Environment Name"
description: "Clear description of the task"
version: "1.0.0"
tasks:
  - id: "task_easy"
    name: "Easy Task"
    difficulty: "easy"
  - id: "task_medium"
    name: "Medium Task"
    difficulty: "medium"
  - id: "task_hard"
    name: "Hard Task"
    difficulty: "hard"
```

#### Environment Class Structure

```python
from pydantic import BaseModel, Field
from typing import Optional

class Observation(BaseModel):
    """What the agent sees at each step."""
    task_id: str
    episode_state: dict
    # Add your specific observation fields here
    pass

class Action(BaseModel):
    """What the agent can do."""
    action_type: str
    # Add your specific action fields here
    pass

class Reward(BaseModel):
    """Feedback signal."""
    score: float = Field(ge=0.0, le=1.0)  # Must be 0.0–1.0
    info: Optional[str] = None

class YourEnvironment:
    """Your OpenEnv environment."""
    
    def step(self, action: Action) -> tuple[Observation, Reward, bool, dict]:
        """Execute one action.
        
        Returns:
            observation: Current state
            reward: Feedback (0.0–1.0)
            done: Episode finished?
            info: Metadata
        """
        pass
    
    def reset(self, task_id: str) -> Observation:
        """Reset to clean initial state."""
        pass
    
    def state(self) -> dict:
        """Return current environment state."""
        pass
```

#### Validation

Your submission will be checked with:
```bash
openenv validate
```

This verifies:
- ✅ `openenv.yaml` is valid  
- ✅ Pydantic models are typed correctly  
- ✅ `step()`, `reset()`, `state()` exist and work  
- ✅ Endpoints respond correctly

---

### 3. Minimum 3 Tasks with Graders

You must define **at least 3 distinct tasks** with **progressively increasing difficulty**.

#### Task Structure

Each task must have:
- **Clear objective**: What should the agent accomplish?
- **Difficulty**: easy, medium, or hard.
- **Grader function**: Scores agent performance (0.0–1.0).

#### Grading Requirements

Graders **must be deterministic and reproducible**:
- Same agent → same score every time.
- Scores range **0.0–1.0** with meaningful granularity.
- Clear, measurable success criteria.

#### Example Grader

```python
def grade_email_triage_task(agent_decisions, ground_truth):
    """
    Ground truth: list of (email, correct_category)
    Agent decisions: list of (email, predicted_category)
    
    Score = correct / total
    """
    correct = sum(1 for (email, pred), (_, truth) in zip(agent_decisions, ground_truth)
                  if pred == truth)
    return correct / len(ground_truth)
```

**Validation**: Your graders will be run to verify they work and return 0.0–1.0.

---

### 4. Meaningful Reward Function

The reward function **guides learning** by providing feedback at each step, not just at episode end.

#### Requirements

- ✅ Returns **partial progress signals** (not just binary pass/fail).
- ✅ Rewards **incremental progress** toward the goal.
- ✅ Penalizes **clearly undesirable behavior** (e.g., infinite loops, destructive actions).
- ✅ Is **non-sparse** (agent gets feedback most steps).

#### Example: Email Triage

```python
def compute_reward(agent_action, env_state) -> float:
    """
    Partial progress:
    - Correctly classify email: +0.5
    - Partially relevant category: +0.2
    - Wrong category: 0.0
    - Infinite loop detected: -0.3
    
    Return: 0.0–1.0
    """
    score = 0.0
    
    if agent_action.category == env_state.correct_category:
        score += 0.5
    elif agent_action.category in env_state.related_categories:
        score += 0.2
    
    if detect_infinite_loop(agent_action, env_state):
        score -= 0.3
    
    return max(0.0, min(1.0, score))
```

**Avoid**: Rewards that are always the same (static) or always fail → agents can't learn.

---

### 5. Baseline Inference Script

You must provide a **reproducible baseline** that runs an LLM against your environment.

#### Requirements

- Uses **OpenAI API client** (reads `OPENAI_API_KEY` from environment).
- Runs against **all 3 tasks** and produces reproducible scores.
- Outputs **baseline scores** for each task.
- Returns in **0.0–1.0 range**.

#### Script Structure

```bash
# File: inference.py
python inference.py
```

```python
import os
from openai import OpenAI

def run_baseline():
    """Run a standard LLM (e.g., Nemotron 3 Super) against your environment."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Initialize your environment
    env = YourEnvironment()
    
    scores = {}
    for task_id in ["task_easy", "task_medium", "task_hard"]:
        obs = env.reset(task_id)
        total_reward = 0.0
        done = False
        steps = 0
        max_steps = 50
        
        while not done and steps < max_steps:
            # Get action from LLM
            response = client.messages.create(
                model="gpt-4",  # Use a consistent baseline model
                messages=[{
                    "role": "user",
                    "content": f"Given this observation: {obs}\nWhat action should you take?"
                }],
                max_tokens=500
            )
            
            # Parse and execute
            action_text = response.content[0].text
            action = parse_action(action_text)
            obs, reward, done, info = env.step(action)
            total_reward += reward.score
            steps += 1
        
        avg_score = total_reward / steps
        scores[task_id] = avg_score
    
    return scores

if __name__ == "__main__":
    scores = run_baseline()
    print(f"Baseline Scores: {scores}")
```

**Important**: Your baseline script will be **re-run to verify reproducibility**. Scores must not vary wildly.

---

### 6. Docker Containerization

Your environment **must run in Docker**.

#### Dockerfile Requirements

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copy your environment code
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Build must complete without error
RUN python -m openenv validate

# Entry point: your environment should listen on a port
EXPOSE 7860

CMD ["python", "app.py"]
```

#### Requirements

- ✅ **`docker build .`** completes successfully.
- ✅ **`docker run -p 7860:7860 <image>`** starts the environment.
- ✅ Environment **responds on HTTP** (e.g., `http://localhost:7860/step`).
- ✅ No hardcoded paths or secrets.

#### Validation

Before submission, test locally:
```bash
docker build -t my-env .
docker run -p 7860:7860 my-env
# In another terminal:
curl -X POST http://localhost:7860/step -d '{"action": "..."}'
```

---

### 7. Hugging Face Spaces Deployment

Your environment **must deploy to Hugging Face Spaces** with the `openenv` tag.

#### Steps

1. Create a **Hugging Face Space**: https://huggingface.co/spaces
2. Choose **Docker** as the runtime.
3. Push your repo (it auto-builds).
4. Tag with `openenv` tag.
5. Share the Space URL in your submission.

#### Verification

Submission validators will:
- ✅ Ping your Space URL.
- ✅ Verify it responds with HTTP 200.
- ✅ Test `/baseline`, `/grader`, `/tasks` endpoints.

---

### 8. README with Documentation

Your **README must include**:

#### Environment Description
- What real-world task does this simulate?
- Why is it useful for agent evaluation?

#### Motivation
- What gap does this fill in agent research?

#### Action & Observation Spaces
- What can the agent observe?
- What actions can it take?
- Provide example JSON.

#### Task Descriptions
- **Easy**: What makes it easy?
- **Medium**: What's the stepping stone?
- **Hard**: What's the frontier challenge?

#### Expected Difficulty
- How hard should each task be for a baseline LLM?
- Baseline scores (as reference).

#### Setup Instructions
```bash
pip install -r requirements.txt
python app.py
```

#### Usage Example
```bash
curl -X POST http://localhost:7860/reset \
  -H "Content-Type: application/json" \
  -d '{"task_id": "task_easy"}'

curl -X POST http://localhost:7860/step \
  -H "Content-Type: application/json" \
  -d '{"action_type": "classify", "value": "spam"}'
```

#### Baseline Scores
```
Task Easy:   0.75
Task Medium: 0.50
Task Hard:   0.25
```

---

## Evaluation Criteria

Submissions are scored across 5 dimensions:

### 1. Real-World Utility (30%)

**Does the environment model a genuine, practical task?**

| Score | Description |
|-------|-------------|
| 0–5   | Toy/artificial problem with no practical application |
| 6–15  | Valid domain but shallow modeling of the real task |
| 16–25 | Good domain modeling; would be useful for agent evaluation |
| 26–30 | Excellent: fills a real gap; immediate value for RL/agent community |

**Scoring Checklist**:
- ✅ Task is something humans actually do (not a game).
- ✅ Complexity matches real-world version (not oversimplified).
- ✅ Reward design reflects true success metrics.
- ✅ Would real agent researchers use this?

---

### 2. Task & Grader Quality (25%)

**Are your 3 tasks well-designed with clear, measurable graders?**

| Score | Description |
|-------|-------------|
| 0–5   | Graders always return the same score / are not reproducible |
| 6–15  | Graders work but lack clear success criteria |
| 16–20 | Good tasks with clear objectives; graders are reproducible |
| 21–25 | Excellent: thoughtful progression (easy→medium→hard); deterministic graders |

**Scoring Checklist**:
- ✅ 3+ tasks with difficulty range.
- ✅ Graders produce scores 0.0–1.0.
- ✅ Same agent → same score every run (reproducible).
- ✅ Difficulty clearly increases.
- ✅ Hard task genuinely challenges frontier models.

---

### 3. Environment Design (20%)

**Is the environment well-designed and does it produce useful reward signals?**

| Score | Description |
|-------|-------------|
| 0–5   | Poor state management; sparse/misleading rewards |
| 6–12  | Functional but basic environment design |
| 13–16 | Clean state management, sensible action/observation spaces |
| 17–20 | Excellent: rich observations, meaningful reward shaping, good episode boundaries |

**Scoring Checklist**:
- ✅ `reset()` produces clean initial state.
- ✅ Action/observation spaces well-designed and documented.
- ✅ Reward function is non-sparse and guides learning.
- ✅ Episode boundaries make sense (finite, reasonable length).
- ✅ No undefined behavior or crashes.

---

### 4. Code Quality & Spec Compliance (15%)

**Does your code follow OpenEnv spec and best practices?**

| Score | Description |
|-------|-------------|
| 0–3   | `openenv validate` fails or code is messy/undocumented |
| 4–9   | Passes validation; basic code quality |
| 10–12 | Clean, documented code; follows OpenEnv patterns |
| 13–15 | Excellent: production-quality code, comprehensive docstrings, tested |

**Scoring Checklist**:
- ✅ `openenv validate` passes.
- ✅ Docker builds and runs without error.
- ✅ HF Space deploys and responds.
- ✅ Baseline script runs and reproduces.
- ✅ Code is documented, typed, and clean.

---

### 5. Creativity & Novelty (10%)

**Does your environment present a novel problem or approach?**

| Score | Description |
|-------|-------------|
| 0–3   | Derivative; seen before in OpenEnv |
| 4–6   | Reasonable but not particularly novel |
| 7–8   | Interesting angle; fills a gap in the domain space |
| 9–10  | Novel problem domain or clever mechanics; cutting-edge for agent eval |

**Scoring Checklist**:
- ✅ Not a trivial copy of an existing environment.
- ✅ Reward design has interesting properties.
- ✅ Domain is underexplored in agent research.
- ✅ Mechanics are clever or novel.

---

## How Judging Works

Judging happens in **3 phases**:

### Phase 1: Automated Validation ✅

**Pass/fail gates** (all must pass or you're disqualified):

1. **HF Space deploys** → Must respond to HTTP.
2. **OpenEnv spec compliance** → `openenv validate` passes.
3. **Dockerfile builds** → `docker build .` succeeds.
4. **Baseline reproduces** → Baseline script runs without error, returns 0.0–1.0 scores.
5. **3+ tasks with graders** → Enumerated, graders work, scores in 0.0–1.0 range.

#### Disqualification Criteria ❌

Your submission is **automatically disqualified** if:
- ❌ Environment does not deploy or respond.
- ❌ Plagiarized or trivially modified existing environments.
- ❌ Graders always return the same score (static).
- ❌ No baseline inference script.
- ❌ Task is a game (Chess, Grid worlds, turn-based games).

---

### Phase 2: Agentic Evaluation 🤖

**Automated scoring** across 5 dimensions (Real-utility, Task quality, Environment design, Code quality, Creativity).

- Baseline agent (e.g., Nemotron 3 Super) runs against your environment.
- Variance checked: multiple runs should yield similar scores.
- Environments ranked by evaluation criteria scores.

---

### Phase 3: Human Review 👥

**Top submissions** reviewed by Meta and Hugging Face engineers.

- Real-world utility check.
- Creativity assessment.
- Exploit/safety checks (prevent adversarial grading, reward hacking).
- Final ranking for top 3,000 teams.

---

## Pre-Submission Checklist

**All items must be completed before submitting** (submission opens March 28):

### Setup ✅
- [ ] Python 3.10+ installed (`python --version`).
- [ ] OpenEnv core installed (`pip install openenv-core`).
- [ ] Docker installed and working (`docker --version`).
- [ ] Git configured (`git --version`).
- [ ] Hugging Face CLI installed and authenticated (`huggingface-cli login`).

### Code ✅
- [ ] Environment implements `step()`, `reset()`, `state()`.
- [ ] Pydantic models for Observation, Action, Reward defined.
- [ ] Runs locally without errors.
- [ ] `openenv validate` passes.
- [ ] Baseline inference script works (`python inference.py`).

### Tasks & Grading ✅
- [ ] 3+ tasks defined (easy, medium, hard).
- [ ] Each task has a grader that returns 0.0–1.0.
- [ ] Graders are deterministic (run multiple times → same score).
- [ ] Reward function is non-sparse and guides learning.

### Docker ✅
- [ ] `Dockerfile` exists.
- [ ] `docker build .` completes without error.
- [ ] `docker run -p 7860:7860 <image>` starts the environment.
- [ ] Environment listens on port 7860.

### Hugging Face Spaces ✅
- [ ] Space created: https://huggingface.co/spaces
- [ ] Repo pushed to Space (auto-builds).
- [ ] Space tags include `openenv`.
- [ ] Space is publicly accessible.
- [ ] Test endpoints respond: `/step`, `/reset`, `/tasks`, `/baseline`, `/grader`.

### Documentation ✅
- [ ] README explains the task in detail.
- [ ] Motivation section included.
- [ ] Example action/observation JSON provided.
- [ ] Task descriptions (easy, medium, hard) clear.
- [ ] Setup and usage instructions included.
- [ ] Baseline scores documented.

### Meta ✅
- [ ] `openenv.yaml` exists with task metadata.
- [ ] `requirements.txt` lists all dependencies.
- [ ] No hardcoded API keys or secrets in repo.
- [ ] Code is clean and documented.
- [ ] Task is not a game or toy (real-world).
- [ ] Submission window verified (opens March 28).

---

## Common Problem Statement Example

### Example: Email Triage Environment

**Problem Statement**:  
*"Build a mini email-triage environment with clearly defined tasks, automated graders, and reward logic using the OpenEnv framework."*

### Task Breakdown

#### Task 1: Easy - Binary Spam Detection
- **Objective**: Classify emails as SPAM or NOT_SPAM.
- **Dataset**: 20 synthetic emails (10 spam, 10 legitimate).
- **Grader**: Accuracy = correct classifications / 20.
- **Baseline Expected**: ~0.80 (easy task).

#### Task 2: Medium - Multi-Category Routing
- **Objective**: Classify into URGENT, NORMAL, LOW_PRIORITY.
- **Dataset**: 30 emails with ground truth labels.
- **Grader**: F1-score across all 3 classes.
- **Baseline Expected**: ~0.60 (moderate task).

#### Task 3: Hard - Custom Rules + Classification
- **Objective**: Apply custom rules (e.g., "Flag emails from CEO as URGENT") + classify.
- **Dataset**: 40 emails with mixed rule triggers.
- **Grader**: Composite score (accuracy on rules + classification F1).
- **Baseline Expected**: ~0.40 (genuinely hard).

### Reward Function

```python
def compute_reward(agent_action, email, ground_truth):
    """
    - Correct classification: +0.4
    - Partially correct (related class): +0.1
    - Wrong classification: 0.0
    - Detected rule violation: +0.3
    - Infinite loop: -0.2
    """
    reward = 0.0
    
    if agent_action.category == ground_truth.category:
        reward += 0.4
    elif agent_action.category in ground_truth.related_categories:
        reward += 0.1
    
    if agent_action.flag_as_rule_violation == ground_truth.has_rule_violation:
        reward += 0.3
    
    return max(0.0, min(1.0, reward))
```

### Baseline Scores (Reference)

```
Email Triage - Binary Spam:   0.80
Email Triage - Multi-Category: 0.62
Email Triage - Hard (Rules):   0.41
```

### Deployment

```bash
git init
git add .
git commit -m "Initial commit"
git push origin main

# Deploy to HF Space (auto-builds from Dockerfile)
```

---

## Key Takeaways

1. **Real-world tasks only** — No games, no toys.
2. **Full OpenEnv spec** — step(), reset(), state() with typed models.
3. **3+ graded tasks** — Easy→medium→hard with deterministic graders.
4. **Meaningful rewards** — Non-sparse, guides learning, penalizes bad behavior.
5. **Reproducible baseline** — OpenAI API, consistent scores.
6. **Docker containerization** — Must build and run.
7. **HF Spaces deployment** — Public, tagged, responsive.
8. **Excellent documentation** — README, setup, usage examples.
9. **Pass Phase 1 (automated)** — Or you're disqualified.
10. **Phase 2 & 3** — Agentic eval + human review for top submissions.

---

## Useful Resources

- **OpenEnv Docs**: https://github.com/huggingface/openenv
- **Hugging Face Spaces**: https://huggingface.co/spaces
- **OpenEnv GitHub**: https://github.com/DAREDEVIL-AI/openenv
- **Submission Portal**: https://scaler.com (check for contest details)
- **Baseline Scores Reference**: Included in each problem statement

---

**Good luck with your submission! 🚀**
