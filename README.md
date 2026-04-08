# ELDER - Extracted Legacy Empowered Development Reasoning

An AI-powered system architecture design agent that transforms natural language requirements into production-ready architectural blueprints.

## Overview

ELDER (Extracted Legacy Empowered Development Reasoning) is an intelligent agent system that designs comprehensive, production-ready system architectures from natural language descriptions. It employs a multi-phase reasoning approach with specialized engines for classification, validation, generation, and research.

## Features

- **Natural Language Input**: Describe your system requirements in plain English
- **Multi-Phase Reasoning**: Decomposes the architecture process into 6 distinct phases
- **Component Analysis**: Identifies services, data stores, and their relationships
- **Technology Research**: Validates technology choices against current ecosystem
- **Architecture Decision Records (ADRs)**: Documents significant decisions with rationale
- **Failure Mode Analysis**: Identifies potential failure points and mitigations
- **Visual Diagrams**: Generates Mermaid.js architecture diagrams
- **OpenEnv Compatible**: Ready for automated grading and benchmarking

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (React)                         │
│  RequirementInput │ ArchitectureViewer │ ADRPanel │ PhaseBoard  │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Backend (FastAPI)                          │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────┐   │
│  │   REST API  │  │ OpenEnv API  │  │   Core Services     │   │
│  └─────────────┘  └──────────────┘  └─────────────────────┘   │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │              Engine Modules (14 specialized)            │    │
│  │  Domain │ Coherence │ LLM │ MCP │ Tech │ Deep │ Arch  │    │
│  │  Reason │ Selector │ Dispatch │ Memory │ TokenTrack   │    │
│  └────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Database (Supabase/Postgres)                 │
│              memory table (pgvector) │ token_usage              │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL with pgvector extension
- OpenAI API key (or compatible)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/elder.git
cd elder
```

2. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

3. **Start with Docker Compose**
```bash
docker-compose up -d
```

4. **Or run locally**

Backend:
```bash
cd app
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

### API Usage

#### Generate Architecture

```bash
curl -X POST http://localhost:8000/api/v1/architect \
  -H "Content-Type: application/json" \
  -d '{
    "requirement": "Design a real-time chat application supporting 10,000 concurrent users",
    "constraints": {
      "max_latency_ms": 100,
      "availability_target": 0.999
    }
  }'
```

#### Response Format

```json
{
  "architecture": {
    "id": "arch_abc123",
    "components": [...],
    "connections": [...],
    "mermaid_diagram": "graph TD\n    A[Client] --> B[API Gateway]..."
  },
  "adrs": [...],
  "failure_modes": [...],
  "confidence_score": 0.87
}
```

## Development

### Running Tests

```bash
# Backend tests
pytest app/tests/ -v

# Frontend tests
cd frontend && npm test

# All tests with coverage
pytest app/tests/ --cov=app --cov-report=html
```

### Code Quality

```bash
# Linting
ruff check app/

# Formatting
black app/
eslint frontend/src/

# Type checking
mypy app/
```

## Project Structure

```
elder/
├── app/                      # Backend application
│   ├── main.py              # FastAPI application
│   ├── core/                # Core services
│   │   ├── memory.py        # Architect memory with pgvector
│   │   └── token_tracker.py # Token usage tracking
│   ├── engines/             # Specialized engine modules
│   │   ├── domain_classifier.py
│   │   ├── coherence_checker.py
│   │   ├── architecture_generator.py
│   │   ├── deep_thinker.py
│   │   ├── tech_research.py
│   │   └── ...
│   ├── models/              # Pydantic schemas
│   ├── openenv/             # OpenEnv grading system
│   │   ├── graders.py       # Evaluation functions
│   │   └── test_cases.py    # Test case definitions
│   └── tests/               # Backend tests
├── frontend/                # React frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── lib/            # Utilities
│   │   └── styles/         # CSS
│   └── ...
├── supabase/                # Database migrations
│   └── migrations/
├── docker-compose.yml       # Local development
├── .github/workflows/       # CI/CD pipelines
└── docs/                    # Additional documentation
```

## Engine Modules

| Engine | Purpose |
|--------|---------|
| `domain_classifier` | Classifies requirements into domains (e-commerce, fintech, etc.) |
| `coherence_checker` | Validates architectural coherence and identifies conflicts |
| `llm_client` | Manages LLM interactions with retry logic |
| `mcp_dispatcher` | Orchestrates multi-component processing |
| `model_selector` | Selects optimal LLM model per task |
| `tech_research` | Researches technology stack options |
| `deep_thinker` | Performs deep analysis and pattern matching |
| `architecture_generator` | Generates component and connection specifications |
| `implementation_planner` | Creates phased implementation roadmap |

## OpenEnv Integration

ELDER is designed to work with the OpenEnv grading environment:

```python
from openenv.graders import grade_task_1, grade_task_2, grade_task_3
from openenv.test_cases import TEST_CASES

# Grade a submission
result = grade_task_1(submission, reference_answer)
print(f"Score: {result['score']}")
```

### Test Tasks

1. **Task 1**: Basic architecture design (10 test cases)
2. **Task 2**: Multi-service architectures (10 test cases)
3. **Task 3**: Complex distributed systems (10 test cases)

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `REDIS_URL` | Redis connection string | redis://localhost:6379 |
| `LOG_LEVEL` | Logging level | INFO |
| `MAX_TOKENS_PER_REQUEST` | Token limit per request | 4000 |

### Configuration File

```yaml
# config.yaml
engines:
  model_selector:
    default_model: gpt-4-turbo
    fallback_model: gpt-3.5-turbo
  
  mcp_dispatcher:
    default_timeout: 30
    max_retries: 3
  
  coherence_checker:
    strict_mode: false
    confidence_threshold: 0.7

database:
  pool_size: 10
  max_overflow: 20
  
vector_search:
  similarity_threshold: 0.75
  max_results: 10
```

## Deployment

### Docker

```bash
# Build images
docker-compose build

# Deploy
docker-compose up -d
```

### Kubernetes

```bash
kubectl apply -f k8s/
```

### HuggingFace Spaces

See [DEPLOY_HF.md](./DEPLOY_HF.md) for deployment instructions.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- Built with FastAPI, React, and Tailwind CSS
- Powered by OpenAI GPT-4
- Database by Supabase (PostgreSQL + pgvector)
- Containerized with Docker

## Support

- Open an issue on GitHub
- Read the [documentation](./docs/)
- Join our community Discord

---

**ELDER** - Building the future, one architecture at a time.
