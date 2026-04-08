# 🏛️ ARCHITECT AGENT — User Guide & Workflow Documentation

**Purpose:** This guide explains how the Architect Agent works, how to use it, and what to expect at each stage of the architectural design process.

---

## 📌 What Is the Architect Agent?

The Architect Agent is an artificial intelligence system designed to help you design production-ready system architectures without requiring deep expertise in distributed systems, technology selection, or failure mode analysis. Instead of spending weeks researching which technologies to use and how to structure your application, you describe what you want to build, and the Architect Agent produces a complete, production-ready architectural blueprint.

The system operates at the architectural layer, which sits above individual coding tasks. While tools like Claude Code, Cursor, and Copilot help you write code faster, the Architect Agent helps you design the right system before any code is written. It thinks like a senior architect: it considers trade-offs, identifies risks, proposes solutions, and hands off an implementation plan to your engineering team.

---

## 🎯 Core Value Proposition

The Architect Agent saves you time and prevents costly architectural mistakes through four key functions.

**First, it recommends the optimal technology stack for your specific constraints.** Rather than presenting a generic recommendation, the system learns from your unique situation—your team size, budget, timeline, expected user scale, and specific requirements. It searches a database of past architectural decisions to find similar projects and learn from what worked. It then uses artificial intelligence reasoning to adapt those lessons to your specific context.

**Second, it generates a complete system design.** The output is not just a list of technologies, but a fully specified architecture including service boundaries, data flows, database schemas, and communication protocols. This specification is detailed enough for experienced engineers to begin implementation immediately.

**Third, it identifies failure modes and proposes mitigation strategies.** For each major component, the system identifies the three most likely ways it could fail and recommends detection and mitigation strategies. This transforms architectural decisions from academic exercises into practical, operational designs.

**Fourth, it creates an implementation roadmap.** The system breaks your architecture into phases, determines the correct order to build them (respecting dependencies), identifies opportunities for parallelization, and generates specifications ready to hand to engineering teams or AI coding agents.

---

## 🔄 How the System Works: The Complete Flow

The Architect Agent operates through a three-stage process: intelligent pattern matching, deep reasoning on complex decisions, and architectural generation.

### Stage 1: Fast Pattern Matching (Seconds)

When you submit your project requirements, the system begins with rapid pattern matching. It parses your natural language description to extract key facts: team size, budget, expected user scale, latency requirements, and specific features you need to build.

The system then uses rule-based matching against a database of proven technology patterns. If your project is a small team building an AI recommendation system with less than five thousand users and a modest budget, the system recognizes this pattern instantly and recommends appropriate technologies: FastAPI for the backend API, PostgreSQL for the primary database, Redis for caching, and pgvector for vector embeddings. This recommendation takes less than one second.

The system simultaneously searches a database of past architectures for similar projects. Using semantic search powered by vector embeddings, it finds designs that solved comparable problems. If another team built a similar recommendation system six months ago, the system retrieves their architectural decisions, the technologies they chose, and the lessons they documented.

### Stage 2: Risk Identification

Next, the system identifies which architectural decisions are too important or unusual to rely on templated recommendations. For example, if your project involves handling payment information and requires regulatory compliance, the security architecture needs careful thought rather than a standard pattern. Similarly, if you need sub-hundred-millisecond latency for a million-user system, the scaling strategy requires deep consideration.

The system flags these risky decisions for deeper analysis. Typical projects have zero to three risky decisions requiring additional thought. A project handling sensitive data with unusual performance requirements might have five or six.

### Stage 3: Deep Reasoning (Minutes)

For each risky decision, the system invokes Claude Sonnet 4, Anthropic's most capable reasoning model, using extended thinking mode. This allows the model to reason through trade-offs, failure modes, and hidden assumptions for up to eight thousand tokens of internal reasoning.

For example, if your project requires handling personally identifiable information with GDPR compliance while also needing real-time personalization, the system might reason through multiple approaches: storing all sensitive data in a separate encrypted service, implementing a data masking layer, using differential privacy techniques, or separating data flows for sensitive versus non-sensitive information. The reasoning process considers the operational complexity of each approach, the training requirements for your team, and the performance implications.

This deep thinking produces refined recommendations that often differ from the fast path. Where the fast pattern matcher might recommend a straightforward architecture, the deep reasoner might propose additional layers of indirection, redundancy, or separation of concerns specifically tailored to your constraints.

### Stage 4: Architecture Generation

With fast recommendations and deep thinking results merged together, the system generates a complete architecture specification. This specification includes a service map showing how components interact, Architecture Decision Records explaining why specific choices were made, data flow diagrams showing how information moves through the system, and estimated effort requirements.

---

## 💻 User Interface Walkthrough

The Architect Agent presents a clean, three-panel interface designed for efficient use by technical teams.

### The Input Panel

The input panel occupies the top of the interface and contains a large text area where you describe your project in natural language. You might write something like: "We are building an e-commerce platform for a fast-growing fashion brand. Our team is five engineers. We need to support one hundred thousand users at launch and grow to one million within two years. Real-time inventory synchronization across multiple warehouses is critical. We need personalized product recommendations powered by machine learning models that retrain daily. We have a monthly technology budget of fifteen thousand dollars. Our team is comfortable with Python and JavaScript. We need the system to be deployed on AWS. We need PCI compliance for payment handling."

The system accepts any length of text from one paragraph to several pages. More details lead to more accurate recommendations, but even brief descriptions produce useful results.

Below the text area, a submit button labeled "Design Architecture" initiates the process. Once clicked, the interface shows a progress indicator explaining which stage is currently running: "Parsing requirements," "Searching similar architectures," "Matching patterns," or "Reasoning about risky decisions."

### The Architecture Diagram Panel

The center panel displays the generated architecture as an interactive diagram. Services appear as boxes colored by their primary technology. Connection lines show dependencies, with different line styles indicating different communication patterns: solid lines for synchronous REST calls, dashed lines for asynchronous message queue communication.

Clicking any service opens a details panel showing its responsibilities, the technology it uses, what other services it depends on, and what services depend on it. Hovering over connections shows the communication protocol and data format. The diagram supports standard pan and zoom operations, and you can export it as an image for presentations or documentation.

Below the diagram, tabs allow you to switch between the service map view and alternative views like a data flow diagram, a critical path visualization showing dependencies, or a technology dependency map.

### The Decision Panel

The right side of the interface displays architectural decisions. The Decisions tab shows all Architecture Decision Records, organized by importance. Each record displays what was chosen, what alternatives were considered and rejected, and the reasoning behind the choice. The Risks tab shows identified failure modes for each service, with severity indicators and proposed mitigations. The Phases tab displays the implementation plan, showing which services should be built in which order, estimated effort per phase, and which phases can proceed in parallel.

---

## 🚀 Step-by-Step User Workflow

### Step 1: Describe Your Project

Begin by clicking the "New Project" button in the top-left corner. Enter a project name and select the primary domain your project addresses: microservices and APIs, AI-native systems with agents and orchestration, or data pipelines and batch processing. While the system automatically detects domains from your description, pre-selecting helps.

Then write a description of what you want to build. Include your constraints: team size, budget, timeline, expected scale, latency requirements, compliance needs, and specific features. The more specific you are, the better. Instead of writing "we need real-time data," write "we need data synchronized across three geographic regions with maximum five-second latency." Instead of "our team is experienced," write "we have three senior backend engineers comfortable with Python and Go, two frontend engineers, and one DevOps engineer."

### Step 2: Review the Fast Recommendation

Within one to two seconds, the system displays an initial recommendation. This shows the recommended technology stack with brief explanations for each choice. You see the service map with the proposed architecture decomposition. You see a preliminary list of identified risks.

At this point, you can review the recommendation and decide if it makes sense for your context. If the system recommended PostgreSQL but your organization standardizes on MySQL, you can note that preference. If the recommended service count seems too high or too low, you can note that feedback.

### Step 3: Review Deep Reasoning Results (If Applicable)

If the system identified risky decisions, after thirty seconds to two minutes it completes deep reasoning and updates the interface with refined recommendations. You see what assumptions the reasoning process made, what alternatives it considered, and how it adjusted the architecture based on deeper analysis.

For example, if you specified PCI compliance requirements, you might see that the fast path recommended a straightforward service architecture, but deep reasoning added a separate, isolated payment service with its own database and stricter access controls. The reasoning explains that this isolation reduces the attack surface and simplifies compliance audits.

### Step 4: Explore the Generated Architecture

Once the architecture is complete, you can explore it interactively. Click on services to understand their responsibilities. Click on connections to see data formats and protocols. Switch between diagram views to see different aspects of the design.

Read the Architecture Decision Records to understand the reasoning behind the design. These records explain not just what was chosen, but why alternatives were rejected. This helps you understand trade-offs and confidently discuss the design with your team.

Review the failure modes. For each service, the system identifies the three most likely failure scenarios, their severity, how you would detect them, and how you would mitigate them. This transforms abstract architectural decisions into concrete operational concerns.

### Step 5: Review the Implementation Plan

Switch to the Phases tab to see the implementation roadmap. The system shows which services depend on which, which can be built in parallel, and estimated effort for each phase. Phase One typically includes foundational infrastructure and critical services. Subsequent phases build out additional features and advanced capabilities.

The specification for each phase includes everything an engineering team needs to begin: detailed service descriptions, API contracts in OpenAPI format, database schemas, environment variable requirements, error handling specifications, and success criteria.

### Step 6: Generate Implementation Specifications

Click "Generate Implementation Plan" to produce detailed specifications ready to hand to engineers. The system generates a Markdown document for each phase with complete, actionable specifications. These documents include example API requests and responses, database migration scripts, configuration requirements, and integration points with other services.

### Step 7: Dispatch to Engineering Teams

If you are using AI coding agents or teams of engineers, you can dispatch phase specifications to them through the interface. Click "Assign Phase," select the phase, and either assign it to a team member or dispatch it to an AI agent like Claude Code with full context about the architecture, dependencies, and specifications.

The system tracks the progress of each phase and validates that the generated code matches the architectural specifications. If an agent completes a service that does not meet the API contract specified in the architecture, the system flags the discrepancy before integration attempts.

---

## 📋 Example Workflows by Domain

To illustrate how the system works in practice, consider three projects representing the three domains the Architect Agent supports.

### Example 1: Microservices Architecture (E-Commerce Platform)

A startup with a five-person engineering team wants to build an e-commerce platform. They submit this description:

"We are building an e-commerce platform for a fashion brand. We need a product catalog system, shopping cart, order management, payment processing with Stripe integration, and customer accounts with authentication. We expect one thousand users at launch, growing to fifty thousand within six months and five hundred thousand within two years. Orders need to be processed within one second. Our team has three backend engineers skilled in Python and Node.js, one frontend engineer, and one DevOps engineer. Our monthly technology budget is five thousand dollars. We need to deploy on AWS."

The system responds with the following recommendation within seconds. It proposes a service-oriented architecture with separate services for authentication, product catalog, shopping cart, orders, and payments. It recommends PostgreSQL for transactional consistency on orders and payments, Redis for session caching and cart operations, and Amazon S3 for product images and assets.

When deep reasoning engages, it notices that payment processing requires PCI compliance and that the startup mentioned Stripe integration. The reasoning process recommends isolating the payment service into a separately secured service that never handles raw credit card data, instead tokenizing cards through Stripe immediately. It also considers the growth trajectory and recommends designing the product catalog service to scale horizontally, with database read replicas for the product information needed frequently but with less frequent writes.

The architecture diagram shows five services arranged vertically: the API gateway at the top handling all external requests, the authentication service handling login and session management, the product catalog service handling product data, the cart service managing shopping carts, and the order and payment services at the bottom handling transactional operations. All services except payment can scale horizontally. The payment service runs as a single, highly available instance with failover.

Failure modes identified for the cart service include potential loss of shopping carts if Redis fails without persistence, lag in inventory synchronization if the product catalog service becomes overloaded, and payment failures if the Stripe API becomes temporarily unavailable. The system recommends Redis persistence to handle the first issue, database read replicas for the second, and local retry queues for the third.

The implementation plan shows four phases. Phase One establishes the API gateway, authentication service, and basic product catalog. Phase Two adds shopping cart and inventory management. Phase Three implements order processing. Phase Four integrates payment processing and adds advanced features like recommendations and admin dashboards.

### Example 2: AI-Native System (Multi-Agent Orchestration)

A research team wants to build an AI-native system that orchestrates multiple specialized agents to research topics and synthesize findings. They describe their project as follows:

"We are building an AI research orchestration platform. The system needs to coordinate multiple specialized AI agents: a research agent that investigates topics, a synthesis agent that combines findings, a critique agent that evaluates conclusions for bias and validity, and a refinement agent that iterates on results. Each agent uses Claude Sonnet 4. The system needs to handle ten concurrent research projects, with each project taking ten to thirty minutes to complete. We need results with high quality and low hallucination rates. Our team is two engineers experienced with Python. We have no specific budget constraints but want to minimize API costs. We plan to deploy on Heroku."

The system recognizes this as an AI-native system and recommends a different architecture than a traditional microservices platform. It proposes a central orchestration service that manages agent workflows, a vector database for storing research results and preventing duplicate research, a task queue for managing agent work, and a memory system that allows agents to reference previous findings.

Deep reasoning improves upon this foundation by considering the iterative nature of the research process. The reasoning suggests implementing a structured workflow engine that can run agents in parallel when possible, in sequence when one agent depends on another's output, and with conditional branching based on intermediate results. It recommends storing agent execution traces for debugging and analysis, and implements a feedback loop where the critique agent can request re-research if it identifies problems in findings.

The architecture shows the orchestration service at the center, coordinating work for the research, synthesis, critique, and refinement agents. Results are stored in a vector database, allowing semantic search for past research. Task queues manage the work distribution. Memory systems track agent reasoning and previous conclusions.

Failure modes for this architecture include hallucinations by individual agents, infinite loops if critique repeatedly rejects results, cost overruns from excessive API calls, and memory/context limits if projects involve extensive research. The system recommends validation gates after each agent to check for hallucinations, a maximum iteration count for the refinement loop, token budgeting and cost monitoring, and context summarization to keep memory within limits.

The implementation plan shows three phases. Phase One builds the orchestration engine and basic agent integration. Phase Two adds the memory system and duplicate detection. Phase Three implements advanced features like parallel agent execution and feedback loops.

### Example 3: Data Pipeline Architecture (Analytics Platform)

A mid-sized company wants to build a data platform for analytics. They describe it as follows:

"We ingest data from ten different source systems including Salesforce, customer databases, web analytics, and payment systems. Data arrives in real time from some sources and daily batches from others. We need to transform this data into a unified customer data platform, remove personally identifiable information for certain analyses, aggregate metrics for dashboards, and feed results into machine learning models. We have a data engineering team of four people skilled in Python and SQL. We need to handle petabytes of data annually. We are deploying on AWS. Data retention and governance are critical, and some data is sensitive."

The system recognizes this as a data pipeline domain and recommends an architecture centered on a data orchestration tool like Apache Airflow, data processing engines like Apache Spark for transformations, and a data warehouse like Snowflake or Redshift for analytics. It recommends separate systems for real-time ingestion using Kafka and batch processing using Airflow.

Deep reasoning considers the sensitive data requirement and recommends adding a data governance layer that tracks personally identifiable information, enforces data access controls, and ensures compliance with regulations. It also considers the multi-source nature of the ingestion and recommends implementing schema validation and data quality checks early in the pipeline to catch problems from source systems before they propagate downstream.

The architecture shows a source system layer ingesting data through both batch and streaming mechanisms. Raw data lands in a data lake. Transformation jobs in Airflow process the data, remove personally identifiable information as appropriate, and load results into a data warehouse. Analytics jobs run on the warehouse to produce reports and feed machine learning models. All operations are audited and versioned for compliance.

Failure modes include data quality issues from upstream sources, schema mismatches, personally identifiable information leakage during transformations, and pipeline failures that delay data availability. The system recommends data validation, schema evolution management, column-level encryption for sensitive data, and monitoring with automated alerting.

The implementation plan shows four phases. Phase One implements batch ingestion and basic transformations. Phase Two adds real-time streaming. Phase Three implements data governance and personally identifiable information handling. Phase Four adds advanced analytics and machine learning integration.

---

## 🎨 Interface Features and Navigation

### Search and History

The left sidebar shows your project history. Previous architectures are listed with creation dates and domain classifications. You can search your history by project name, domain, or key technologies used. Clicking any past architecture loads it, allowing you to review previous designs or use them as starting points for new projects.

### Diagram Customization

The diagram supports several visualization options. You can color services by technology type, by team responsibility, by scalability strategy, or by failure severity. Different colorings highlight different aspects of the design. You can also customize the diagram layout, choosing between hierarchical layouts that show dependencies clearly, circular layouts that show peer relationships, or force-directed layouts that cluster tightly related services.

### Export and Sharing

The architecture can be exported in multiple formats. You can download the diagram as a PNG or SVG image for presentations. You can export the complete architecture specification as a Markdown document or as a JSON file. You can generate a shareable link that allows team members to review the architecture without creating accounts, with optional read-only or read-write permissions.

### Comparing Alternatives

If you want to explore how different technology choices would affect the architecture, you can fork the current design and make changes. The system will regenerate the architecture with your changes and show you the differences. This allows you to explore alternatives like "what if we used MongoDB instead of PostgreSQL" or "what if we reduced the team to three engineers" and see how the architecture adjusts.

### Integration with External Tools

The architecture specifications can be integrated with project management tools. You can export phases as Jira epics and stories. You can generate GitHub issue templates from phase specifications. You can feed the implementation plan into team wikis or documentation systems.

---

## 📊 Reading the Output: Key Components

Understanding the output produced by the Architect Agent is essential to using it effectively.

### Service Descriptions

Each service in the architecture includes a structured description. The name identifies the service clearly, such as "Authentication Service" or "Product Recommendation Engine." The purpose explains what the service does and why it exists as a separate service. The technology specifies which programming language, framework, and libraries the service uses. The scalability strategy explains how it handles growth: whether it scales horizontally by adding replicas, whether it has built-in sharding, or whether it is a single-instance service with failover.

Dependencies list what other services this service calls, what data sources it queries, and what external APIs it consumes. The API section specifies what endpoints the service exposes, what request parameters they accept, and what response they return. The data storage section describes databases, caches, or file systems the service uses exclusively.

### Architecture Decision Records

Architecture Decision Records follow a standard format that includes the decision title, the context that made the decision necessary, the alternatives considered, the chosen solution, the consequences of the choice, and any assumptions made. For example, an ADR might read as follows:

"Decision: Use PostgreSQL for order storage instead of MongoDB. Context: Orders require strong transactional consistency because payment processing and inventory updates must succeed or fail together. Alternatives: MongoDB offers flexible schemas and scales horizontally more easily, and DynamoDB offers fully managed operations. Decision: PostgreSQL's ACID transactions and mature transaction support outweigh MongoDB's flexibility benefits for this use case. Consequences: PostgreSQL requires schema management and careful capacity planning for writes at scale. We will need read replicas for scaling read queries. Assumptions: Our order modification patterns are primarily transactional appends rather than frequent updates of existing orders."

### Failure Mode Analysis

For each service, the system identifies failure modes with severity levels ranging from low to critical. A typical failure mode entry reads as follows:

"Service: Product Catalog. Failure Mode: Database connection failures. Severity: High. Probability: Medium (databases occasionally require maintenance). Detection: Application layer detects when connections cannot be established and returns 503 Service Unavailable. Mitigation: Connection pooling with retry logic. Database read replicas for read scalability. Monitoring: Alert if error rate exceeds 1 percent over five minutes. Recovery: Automatic failover to read replicas. Manual failover to standby instance if primary fails."

### Implementation Phase Specifications

Phase specifications are detailed documents that teams or AI agents can use to begin development immediately. Each phase includes a summary of what gets built, the services included, integration points with previous phases, API contracts in full OpenAPI specification format, database schema with migrations, configuration requirements, error handling specifications, and testing requirements.

---

## 🔧 Customization and Feedback

The system learns and improves based on your feedback. After you or your team implements an architecture, you can rate how well it worked. Were the estimated effort hours accurate? Did failure modes match actual problems encountered? Did the proposed technologies suit your team's experience level? This feedback refines future recommendations for you and other users.

You can also provide feedback on individual recommendations. If you disagree with a suggested technology choice, you can explain why, and the system uses this information to adjust future suggestions. If a recommended service boundary does not match your team's work structure, you can suggest an alternative, and the system notes this for future designs.

---

## 📱 Mobile and Command-Line Access

While the primary interface is a web application, you can also use the Architect Agent through a command-line tool or API. The command line supports workflows like creating a new architecture from a requirements file, exporting specifications, or validating an existing architecture against architectural constraints.

The API allows integration with other tools. You can submit requirements to the API and receive the complete architecture as JSON. This allows programmatic use cases like automatically designing architectures for large numbers of projects or integrating architecture design into deployment automation.

---

## ⚠️ Limitations and Best Practices

The Architect Agent is a powerful tool, but it has limitations that you should understand.

The system makes recommendations based on typical constraints and requirements. If your use case is highly unusual—a specialized gaming engine, a medical device firmware, or a quantum computing simulation—the recommendations may be less applicable. The system works best for typical application categories: web services, mobile backends, data platforms, and AI orchestration.

The system cannot fully understand implicit organizational constraints. If your company has standardized on specific technologies, has unique security requirements, or operates in a regulated industry with specialized compliance needs, you should review recommendations carefully and adjust them based on these constraints before implementation.

The system generates architectures for new systems. If you are refactoring an existing system, the recommendations may not account for constraints from legacy code, database migrations, or gradual rollout requirements. The system can assist in refactoring scenarios, but the context and constraints are different.

The effort estimates are based on typical team capabilities. If your team has significantly more or less experience than assumed, actual effort may differ substantially. Use effort estimates as a starting point and refine them based on your team's actual velocity.

Finally, the system produces architectural designs, not detailed implementation plans. Architecture provides the blueprint, but teams must still make numerous detailed implementation decisions. The architecture specifies that you need a caching layer, but the detailed configuration of cache invalidation strategies, cache key design, and fallback behaviors remains for the implementation team.

---

## 🎓 Learning Resources

To get the most from the Architect Agent, consider reading background material on system design. The system recommends designs but does not teach the reasoning behind them. Reading Designing Data-Intensive Applications by Martin Kleppmann provides deep knowledge of distributed systems concepts that help you understand and validate architectural recommendations. The system also links to relevant documentation for each technology recommendation, allowing you to learn more about tools you may be unfamiliar with.

As you use the system repeatedly, you develop intuition for when recommendations are appropriate and when you need to adjust them. Over time, reviewing the reasoning behind recommendations builds your own architectural thinking.

---

## 📞 Support and Community

The Architect Agent includes integrated documentation explaining every recommendation. You can hover over any service, connection, or decision record to read a detailed explanation of why it was chosen.

A community forum allows users to discuss recommendations, share implementations, and learn from each other's experiences. You can see how other teams in your domain approached similar problems and what challenges they encountered.

The system includes examples for each domain showing typical architectures for common scenarios. These examples serve as templates and learning resources.

---

## 🚀 Getting Started

To get started with the Architect Agent, create an account and begin with a tutorial project. The system guides you through describing a sample project and walks you through understanding the generated architecture. Once you complete the tutorial, you can create your actual project and begin designing.

Begin with a clear, detailed project description. Include your constraints explicitly. The more context you provide, the better the recommendations. Submit your description and review the fast pattern matching results. Then wait for deep reasoning to complete if the system identifies risky decisions.

Explore the generated architecture interactively, reading the decision records and understanding the reasoning. Discuss the architecture with your team, noting any concerns or constraints you want to address. Make adjustments if necessary, forking the design to explore alternatives.

Once you have a design your team is confident in, export the implementation plan and begin assigning work to team members or AI agents. Use the phase specifications as the specification for implementation.

The Architect Agent is designed to save you weeks of architectural work while producing more thorough, better-reasoned designs than you could produce manually. It is most powerful when used as a collaborative tool—the system provides recommendations and reasoning, and your team applies organizational knowledge and expertise to refine and implement those recommendations.
