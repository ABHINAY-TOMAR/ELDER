---
description: architect-agent-workflow
---

# Architect Agent Workflow

The Architect Agent operates at the system design layer, receiving natural language requirements and translating them into robust, production-ready system architectures.

## The User's Perspective

From the user's point of view, interacting with the system is seamless and conversational:

1. **Input Requirements**: The user provides business constraints and product needs in plain text. Examples:
   - "I need a recommendation engine for e-commerce with 100k users. Keep latency under 500ms."
   - "Build an MVP for a two-sided marketplace. We have a team of 4, mostly familiar with JavaScript, with a budget of $5k a month."
2. **Instant Feedback**: The system immediately gives a high-level recommendation (the "Fast Path"), suggesting core tech boundaries such as frameworks, data stores, and potential pitfalls.
3. **Deep Deep Dive**: For complex problems or conflicting constraints (e.g., highly stringent latencies coupled with low budgets), you'll see a loading indicator while the Agent "thinks deeply" (the "Slow Path").
4. **Final Deliverable**: The platform renders an interactive, phase-by-phase architectural map, showcasing dependencies, databases, messaging layers, failovers, and concrete task assignments ready to be federated to coding agents (via the Model Context Protocol - MCP).

## Behind the Scenes

Under the hood, the system is a decentralized 12-engine orchestrator designed similarly to how an elite software architect approaches a problem:

1. **Parser & Classifier**: Extracts entities (budget, scale, domain constraints). Determines if this is a microservice, a data pipeline, or an AI-native stack.
2. **Memory & pgvector Search**: Cross-references against 30+ pre-seeded battle-tested architectures and previously stored project decisions to avoid reinventing the wheel.
3. **Hybrid Reasoner & Token Tracker**:
   - Uses **Fastcode** logic to route straightforward decisions to fast, inexpensive models.
   - Routes highly risky or complex scaling hurdles to extensive deep-thinking models (supporting OpenAI, Nvidia, and OpenRouter for maximum model flexibility).
   - Real-time token tracking guards against budget overruns ensuring predictable API costs.
4. **Phase Generation**: Generates explicit Architecture Decision Records (ADRs) and chunks the workload into topological phases (auth -> core -> features) based on `autoMate` scheduling logic.
5. **Database**: Everything is persisted in **Supabase** (remote), establishing a long-term architectural memory.

## Real-World Value

Software engineering fails mostly at the design phase. Junior level coding agents will happily write thousands of lines of code building a monolith when a microservices approach was needed, or an SQL database when vector storage was required. 

This workflow positions the Architect Agent perfectly as "The Manager" -> deciding **what** needs to be built and **how** it should connect, so that downstream coding agents actually write code that scales, functions efficiently, and solves the user's *real* problem.
