# 🏛️ ARCHITECT AGENT — Complete System Overview

**A high-level guide to understanding how the entire system works, how users interact with it, and what happens behind the scenes.**

---

## 🎯 What Users See vs. What Happens Behind the Scenes

### User Perspective: Simple Three-Step Process

From a user's viewpoint, the Architect Agent is remarkably simple to use. You visit the website, describe your project in natural language, and receive a complete architectural blueprint including service diagrams, technology recommendations, failure analysis, and an implementation roadmap. The entire process takes seconds to minutes depending on complexity.

Behind that simple interface lies a sophisticated system with twelve specialized engines that work together to produce thoughtful, well-reasoned architectures.

---

## 📊 The Complete System Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER SUBMITS PROJECT                      │
│          "Build e-commerce platform, 5 engineers, $5k/mo"      │
└──────────────────────────┬──────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│              1. REQUIREMENTS PARSER (0.1 seconds)               │
│  Converts natural language → structured RequirementSpec        │
│  Extracts: team_size=5, budget=5000, expected_users=100000    │
│  Output: RequirementSpec object with all fields                │
└──────────────────────────┬──────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│          2. DOMAIN CLASSIFIER (0.05 seconds)                    │
│  Determines primary domain: Microservices                       │
│  Recognizes: e-commerce = transactional, service-oriented      │
│  Output: domain="microservices", confidence=0.95               │
└──────────────────────────┬──────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│       3. PATTERN RETRIEVER (0.3 seconds)                        │
│  Search pgvector for similar past architectures               │
│  Query: "e-commerce team:5 scale:100k budget:5k"              │
│  Found: 3 similar projects from past designs                   │
│  Output: Reference architectures to learn from                 │
└──────────────────────────┬──────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│      4. FAST PATTERN MATCHER (0.2 seconds)                      │
│  Apply 20+ rules: IF domain="microservices" AND                 │
│                      team=5 AND budget=5k                       │
│                  THEN use FastAPI, PostgreSQL, Redis            │
│  Output: StackRecommendation with 5 tech choices              │
│  Latency: <1 second total so far                              │
└──────────────────────────┬──────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│   5. RISKY DECISION DETECTOR (0.2 seconds)                      │
│  Analyzes: PCI compliance? No. Unusual scale? No.              │
│  Real-time requirement? No. Sensitive data? No.                │
│  → Result: 0 risky decisions requiring deep thinking           │
│  Fast path sufficient; skip extended thinking                 │
│  Output: RiskyDecision[] (empty in this case)                 │
└──────────────────────────┬──────────────────────────────────────┘
                           ↓
                    [USER SEES FAST RESULTS]
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│              ARCHITECTURE GENERATOR (1-2 seconds)                │
│  Combines: fast recommendation + no risky decisions            │
│  Generates:                                                     │
│    - Service map: 5 services (API Gateway, Auth, Product,      │
│                   Cart, Orders)                                │
│    - Technology stack with rationale                           │
│    - Data flows between services                               │
│    - 5-7 Architecture Decision Records                         │
│  Output: Complete Architecture object                          │
└──────────────────────────┬──────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│          FAILURE MODE MAPPER (0.5 seconds)                      │
│  For each service, identify 3 failure scenarios:               │
│    Auth Service: DB unavailable, token validation fails        │
│    Product: Catalog corruption, search timeout                 │
│    Cart: Redis loss, session expiry                            │
│  For each failure: detection strategy, mitigation, monitoring  │
│  Output: FailureMode[] for all services                        │
└──────────────────────────┬──────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│      IMPLEMENTATION PLANNER (0.3 seconds)                       │
│  Build dependency graph of services                            │
│  Topological sort → phases                                     │
│    Phase 1: API Gateway, Auth (no dependencies)               │
│    Phase 2: Product Service (depends on API Gateway)          │
│    Phase 3: Cart Service (depends on Product)                 │
│    Phase 4: Orders (depends on Auth, Cart, Products)          │
│  Identify parallelization: Phase 1 and 2 can overlap          │
│  Estimate effort: 2 weeks Phase 1, 1 week Phase 2, etc.       │
│  Output: Phase[] with ordering and timing                     │
└──────────────────────────┬──────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│           VECTOR EMBEDDER (0.1 seconds)                         │
│  Embed complete architecture for future retrieval             │
│  Store in pgvector: embedding + architecture + metadata       │
│  Add tags: domain:microservices, scale:100k, budget:5k        │
│  Output: Architecture stored and searchable                    │
└──────────────────────────┬──────────────────────────────────────┘
                           ↓
         [USER SEES COMPLETE ARCHITECTURE WITH DIAGRAM,
          DECISIONS, FAILURE MODES, IMPLEMENTATION PLAN]
```

This entire flow takes three to five seconds when no deep thinking is required.

### When Deep Thinking Is Required

If the risky decision detector identifies complex decisions (PCI compliance, unusual scale, sensitive data, novel domain combinations), the system invokes Claude Sonnet 4 with extended thinking.

```
            [RISKY DECISIONS DETECTED]
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│    HYBRID REASONER + EXTENDED THINKING (10-30 seconds)         │
│  For each risky decision:                                       │
│    1. Generate 3-5 alternative approaches                      │
│    2. Evaluate each with Sonnet 4 extended thinking            │
│    3. Consider: trade-offs, failure modes, team skills         │
│    4. Synthesize best approach + reasoning                     │
│  Example: If PCI compliance required, reasoning might show:     │
│    - Fast path: Stripe payment in product service             │
│    - Deep thinking: Isolated payment service recommended       │
│    - Reason: Reduced attack surface, simplified compliance     │
│  Output: Refined recommendations with detailed reasoning       │
└──────────────────────────┬──────────────────────────────────────┘
                           ↓
    [SYSTEM MERGES FAST + DEEP RECOMMENDATIONS]
                           ↓
    [REGENERATES ARCHITECTURE WITH REFINED DESIGN]
                           ↓
    [USER SEES FINAL, DEEPLY-REASONED ARCHITECTURE]
```

When deep thinking is involved, total time is 15-45 seconds depending on decision complexity.

---

## 🎮 User Workflow: From Requirement to Implementation

### Phase 1: Project Submission (1 minute)

The user visits the Architect Agent website and clicks "Create New Project." They enter a project name, optionally select the primary domain, and write a natural language description of what they want to build. The description can be brief (one paragraph) or comprehensive (multiple pages). More detail produces better results.

The user clicks "Design Architecture" to submit their requirements.

### Phase 2: View Fast Results (2-5 seconds)

The system immediately displays initial recommendations. The interface shows a service diagram, the recommended technology stack, and preliminary failure modes. This is the output of fast pattern matching and provides an instant sense of direction.

The user reviews these results and can see at a glance whether the recommendations align with their thinking. If they expected four services but the system recommended seven, they can note that discrepancy. If the recommended technology choices match their team's experience, that is a good sign.

### Phase 3: Review Deep Thinking Results (15-45 seconds, if applicable)

If risky decisions were detected, the system shows a progress indicator: "Reasoning about complex decisions." After this completes, the interface updates with refined recommendations. The user sees how deep thinking adjusted the architecture. Perhaps the fast path recommended a straightforward service structure, but deep thinking added an isolated payment service or separate data governance layer.

### Phase 4: Explore the Architecture (5-15 minutes)

The user spends time understanding the proposed design. They click on services to read descriptions. They click on connections to understand communication protocols. They read Architecture Decision Records to understand why specific choices were made.

Most importantly, they read the failure modes. For each service, the system identified the three ways it could fail, how to detect failures, and how to mitigate them. This transforms architectural decisions from academic exercises into operational systems the team can run and monitor.

### Phase 5: Review Implementation Plan (5 minutes)

The user switches to the Phases tab and reviews the implementation roadmap. They see which services should be built in what order, which phases can proceed in parallel, and estimated effort for each phase. If their timeline is tight, they can see which phases are on the critical path.

### Phase 6: Export and Share (2-3 minutes)

The user exports the architecture. They might download the diagram as an image for presentations, export the complete specification as Markdown for documentation, or generate a shareable link so team members can review the design.

### Phase 7: Discuss with Team (variable)

The user shares the architecture with their engineering team. They discuss whether the recommendations align with team expertise, organizational constraints, and project goals. They may adjust the architecture slightly based on team feedback, which regenerates the design with changes.

### Phase 8: Dispatch to Agents or Teams (variable)

Once the team approves the architecture, the user exports the implementation specifications for each phase. They either assign phases to team members or dispatch phase specifications to AI agents like Claude Code, providing full context about service boundaries, API contracts, and integration points.

The system tracks phase completion and validates that generated code matches the architectural specifications.

---

## 🔍 Behind the Scenes: How Each Component Works

### The Requirements Parser

The Requirements Parser reads natural language and extracts structured information. It identifies team size, budget, expected user scale, latency requirements, compliance needs, and specific features. It does this by sending the user's text to Claude API and asking the model to extract and structure the information into a RequirementSpec object.

For example, if a user writes "We need GDPR compliance because we are handling European customer data," the parser extracts data_sensitivity="pii" and regulatory_requirements=["GDPR"]. If a user writes "We need responses within 100 milliseconds," the parser extracts latency_requirement_ms=100.

The parser is fast because it uses a small model and simple prompts, not extended thinking.

### The Domain Classifier

The Domain Classifier determines whether a project is primarily microservices-oriented, AI-native, or data-pipeline-oriented. It looks for keywords: "agent" or "orchestration" or "agentic workflow" suggests AI-native. "ETL" or "pipeline" or "streaming" suggests data-pipeline. "REST API" or "microservice" suggests microservices.

If multiple domains are detected, the classifier ranks them by confidence and returns the primary domain plus secondary domains.

### The Pattern Retriever

The Pattern Retriever uses pgvector to search past architectures. It embeds the user's requirement description and searches the vector database for similar past projects. It returns the top five similar architectures with similarity scores.

This allows the system to learn from past decisions. If another team built a similar recommendation system, their technology choices, mistakes, and lessons are immediately available.

### The Fast Pattern Matcher

The Fast Pattern Matcher applies hundreds of if-then rules. Rules are organized by domain and encode accumulated knowledge about technology selection. For example:

```
Rule: IF domain == "microservices" 
      AND team_size <= 5 
      AND expected_users <= 100000
      AND latency_ms >= 500
      THEN api_framework = "FastAPI" OR "Express"
           database = "PostgreSQL"
           cache = "Redis"
           message_queue = "none"
           monitoring = "Prometheus"
```

Rules vary from simple (one condition, one conclusion) to complex (multiple conditions, conditional conclusions). The rule engine scores each rule based on how many conditions match and returns the best-matching rule.

This approach is fast because it requires no API calls, just in-memory rule evaluation. It provides instant results while accounting for many factors.

### The Risky Decision Detector

The Risky Decision Detector identifies decisions too complex for rules. It checks for conditions like:

If expected_users > 10M AND no scaling_strategy mentioned → risky decision  
If data_sensitivity == "PII" AND no security_strategy mentioned → risky decision  
If latency_ms < 100 AND no caching_strategy mentioned → risky decision

When risky decisions are detected, they are flagged for deeper reasoning.

### The Hybrid Reasoner

The Hybrid Reasoner has two paths. The fast path immediately returns the fast pattern matcher results if no risky decisions exist. The deep path, triggered by risky decisions, invokes Claude Sonnet 4 with extended thinking.

For each risky decision, the Hybrid Reasoner generates multiple hypotheses (alternative approaches), evaluates each with deep reasoning, and synthesizes the best approach. The reasoning considers trade-offs, failure modes, team expertise requirements, and long-term maintenance burden.

This hybrid approach balances speed (most projects require no deep thinking) with quality (complex decisions receive careful analysis).

### The Architecture Generator

The Architecture Generator converts recommendations into a complete specification. It generates:

A service map showing services and their dependencies. This is the core architectural diagram. Each service has responsibilities, technologies, scalability strategy, and dependencies listed.

A list of Architecture Decision Records, each explaining a major decision: what was chosen, why alternatives were rejected, what assumptions were made, and what implications exist.

Data flows showing how information moves between services: are calls synchronous REST or asynchronous message queues? What data format is used?

Technology stack recommendations with rationale explaining why each technology was chosen.

Estimated effort in weeks, derived from service count, complexity, and team experience level.

### The Failure Mode Mapper

The Failure Mode Mapper identifies three failure scenarios for each service. For example, an authentication service might fail due to database unavailability, due to token validation becoming computationally expensive, or due to the external identity provider becoming unavailable.

For each failure, the mapper specifies:

The probability (high, medium, low) based on typical patterns for this failure in this type of service. Database failures are common in high-scale systems, so they are marked high probability. A specific external API failure is lower probability.

The severity (critical, high, medium, low) based on how much damage the failure causes. Authentication failures are critical because they prevent all user access.

A detection strategy explaining how to know the failure occurred. For database unavailability, this is a connection timeout. For token validation slowness, this is response time exceeding a threshold.

A mitigation strategy explaining how to prevent or recover from the failure. Database failover, read replicas, or caching might mitigate database failures. Timeout limits or degradation modes might mitigate validation slowness.

### The Implementation Planner

The Implementation Planner builds a dependency graph of services. If Service A calls Service B, then B must be built before A (or A must be built to call a stub version of B).

The planner performs a topological sort of the graph, grouping independent services into phases. Services with no dependencies form Phase 1. Services depending only on Phase 1 services form Phase 2. And so on.

The planner also identifies opportunities for parallelization. All services in a phase can theoretically be built in parallel because they do not depend on each other.

For each phase, the planner estimates effort based on service count, complexity, and team experience. These estimates inform timeline planning.

### The Coherence Checker

After agents or teams complete phases, the Coherence Checker validates that services integrate correctly. It extracts API specifications from generated code, compares them against the architecture specification, and flags mismatches.

For example, if the architecture specifies that Service A calls Service B's endpoint `/products?query=...` but the generated Service B provides `/products/search?q=...`, the coherence checker flags the mismatch before integration is attempted.

### The Token Tracker

The Token Tracker monitors Claude API usage throughout the design process. When the Hybrid Reasoner calls Claude Sonnet 4, the tracker counts prompt tokens and completion tokens and calculates costs.

This allows users to understand how much the design cost and whether they are within budget. It also provides data on typical costs for different project types and complexities.

---

## 💾 Data Flow and Storage

### What Gets Stored

When a user submits a project and receives an architecture, the system stores:

The original requirement description in the projects table  
The parsed RequirementSpec with extracted fields  
The complete Architecture object including services, ADRs, failure modes, phases  
An embedding of the architecture for semantic search  
Metadata tags describing domain, scale, technology, team size  

All of this is stored in Supabase PostgreSQL with pgvector indexing.

### How Storage Enables Learning

By storing architectures, the system builds a corpus of designs that future users can learn from. When a new user with a similar project arrives, the pattern retriever finds past designs, surface lessons learned, and provides templates to adapt.

This corpus also allows the system to analyze trends. Which technologies are most commonly recommended for which domains? How does team size affect architecture decomposition? What failure modes are most common?

### Privacy and Access Control

All stored architectures are private to the user who created them unless explicitly shared. Users can generate shareable links with read-only or read-write permissions for team members.

Aggregated data (technology trends, typical effort estimates) may be shared anonymously in reports, but specific project architectures remain private.

---

## 🎯 Key Design Principles

The Architect Agent is designed around three core principles.

### Speed First, Depth When Necessary

The system defaults to fast, instant recommendations that work for typical projects. Only when the system detects complexity does it engage expensive deep thinking. This balance provides instant gratification for simple projects while carefully handling complex cases.

### Explainability Over Black Boxes

Every recommendation includes reasoning explaining why it was chosen. Architecture Decision Records show alternatives that were rejected and why. Failure mode analysis shows how the system thought about risk. This transparency allows users to understand and validate recommendations.

### Production-Ready Output

The system generates not rough sketches but production-ready specifications. Phase descriptions include API contracts in OpenAPI format, database schemas, configuration requirements, and success criteria. Teams can begin implementation immediately using these specifications.

---

## 📈 How the System Improves

The system continuously improves through three mechanisms.

### User Feedback

After users implement architectures, they can rate how well the design worked. Were effort estimates accurate? Did failure modes match reality? Did the technology stack suit the team? This feedback refines future recommendations.

### Pattern Accumulation

As more users submit projects and architectures are stored, the pattern database grows. The Pattern Retriever finds increasingly specific matches, providing better templates for new projects.

### Reasoning Improvement

Over time, improvements to Claude models (Sonnet 5, Opus, etc.) naturally improve the quality of hybrid reasoning when complex decisions require deep thinking.

---

## 🚀 Getting Started as a User

If you are new to the Architect Agent, begin with the tutorial project. The system guides you through describing a sample project and explains how to interpret the generated architecture.

Then create your actual project. Be specific in your description. Include constraints, team experience level, timeline, and specific requirements. The more context you provide, the better the recommendations.

Review the fast results and wait for deep reasoning if risky decisions were detected. Explore the architecture interactively, reading decision records and understanding the reasoning. Discuss with your team and adjust if necessary.

Export the implementation plan and begin building. Use phase specifications as your implementation guide.

The Architect Agent is designed to save weeks of architectural work, improve design quality, and provide a solid foundation for your team's implementation. It is most effective when used collaboratively—the system provides thoughtful recommendations, and your team applies organizational knowledge and expertise to refine and execute those recommendations.
