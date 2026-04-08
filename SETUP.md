# ELDER Local Development Setup

This guide covers setting up ELDER for local development.

## Prerequisites

### Required Software

| Software | Version | Notes |
|----------|---------|-------|
| Python | 3.10+ | Required for backend |
| Node.js | 18+ | Required for frontend |
| Docker | 24+ | For containerized services |
| Docker Compose | 2.0+ | Service orchestration |
| Git | 2.0+ | Version control |

### Optional (for local without Docker)

- PostgreSQL 15+ with pgvector extension
- Redis 7+
- OpenAI API key (or Azure OpenAI)

## Quick Start (Recommended)

### 1. Clone and Setup

```bash
git clone https://github.com/yourusername/elder.git
cd elder
```

### 2. Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Required
OPENAI_API_KEY=sk-your-api-key-here

# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/elder
REDIS_URL=redis://localhost:6379

# Application
LOG_LEVEL=INFO
ENVIRONMENT=development
SECRET_KEY=your-secret-key-here

# Optional
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### 3. Start Services

Using Docker Compose (recommended):

```bash
docker-compose up -d
```

This starts:
- PostgreSQL with pgvector (port 5432)
- Redis (port 6379)
- Backend API (port 8000)
- Frontend (port 3000)

Verify services:
```bash
docker-compose ps
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Manual Setup (Without Docker)

### Database Setup

#### PostgreSQL with pgvector

```bash
# Install PostgreSQL
# macOS
brew install postgresql@15
brew services start postgresql@15

# Ubuntu
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql

# Install pgvector extension
psql -U postgres -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

Create database:
```bash
psql -U postgres
CREATE DATABASE elder;
\c elder
CREATE EXTENSION vector;
\q
```

#### Redis

```bash
# macOS
brew install redis
brew services start redis

# Ubuntu
sudo apt install redis-server
sudo systemctl start redis
```

### Backend Setup

```bash
cd app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Seed reference data
python -m scripts.seed_data

# Start development server
uvicorn main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## Database Schema

### Memory Table (with pgvector)

```sql
CREATE TABLE memory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    embedding VECTOR(1536),
    category VARCHAR(100),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX ON memory USING ivfflat (embedding vector_cosine_ops);
```

### Token Usage Table

```sql
CREATE TABLE token_usage (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id VARCHAR(100),
    operation VARCHAR(100),
    model VARCHAR(50),
    prompt_tokens INTEGER,
    completion_tokens INTEGER,
    total_tokens INTEGER,
    cost_usd DECIMAL(10, 6),
    created_at TIMESTAMP DEFAULT NOW()
);
```

## Running Tests

### Backend Tests

```bash
cd app

# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=. --cov-report=html

# Specific test file
pytest tests/test_engines.py -v

# With verbose output
pytest tests/ -vv --tb=long
```

### Frontend Tests

```bash
cd frontend

# Run tests
npm test

# Watch mode
npm test -- --watch

# Coverage
npm test -- --coverage
```

### Integration Tests

```bash
# Start test environment
docker-compose -f docker-compose.test.yml up -d

# Run integration tests
pytest tests/integration/ -v

# Cleanup
docker-compose -f docker-compose.test.yml down
```

## Code Quality

### Linting

```bash
# Python
cd app
ruff check .
ruff format .

# Type checking
mypy .

# Frontend
cd frontend
npm run lint
npm run typecheck
```

### Pre-commit Hooks

Install pre-commit:
```bash
pip install pre-commit
pre-commit install
```

Run manually:
```bash
pre-commit run --all-files
```

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

Follow the coding standards:
- Python: Follow PEP 8, use type hints
- TypeScript: Strict mode enabled
- Commits: Use conventional commits

### 3. Test Changes

```bash
# Backend
pytest tests/ -v

# Frontend
cd frontend && npm test

# Both
npm run test:all
```

### 4. Submit Changes

```bash
git add .
git commit -m "feat: add new feature"
git push origin feature/your-feature-name
```

## Debugging

### Backend Debugging

Enable debug mode:
```bash
export LOG_LEVEL=DEBUG
uvicorn main:app --reload
```

Use Python debugger:
```python
import pdb; pdb.set_trace()
```

### Frontend Debugging

React DevTools:
- Install browser extension
- Access component inspector

Verbose logging:
```bash
npm run dev:verbose
```

### Database Debugging

Connect to database:
```bash
psql $DATABASE_URL
```

View recent queries:
```sql
SELECT * FROM token_usage ORDER BY created_at DESC LIMIT 10;
```

Check memory embeddings:
```sql
SELECT id, category, created_at FROM memory ORDER BY created_at DESC LIMIT 10;
```

## Troubleshooting

### Common Issues

#### Port Already in Use

```bash
# Find process using port
lsof -i :8000  # macOS
netstat -tlnp | grep 8000  # Linux

# Kill process
kill -9 <PID>
```

#### Database Connection Error

```bash
# Check PostgreSQL is running
pg_isready -h localhost -p 5432

# Test connection
psql $DATABASE_URL -c "SELECT 1;"
```

#### pgvector Not Installed

```bash
psql -U postgres -d elder -c "CREATE EXTENSION vector;"
```

#### Redis Connection Error

```bash
# Check Redis is running
redis-cli ping

# Should return: PONG
```

#### Node Modules Issues

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Reset Development Environment

```bash
# Stop all containers
docker-compose down

# Remove volumes (WARNING: deletes data)
docker-compose down -v

# Rebuild and restart
docker-compose up -d --build
```

## Performance Tuning

### Database Connection Pooling

Edit `app/core/config.py`:
```python
DATABASE_POOL_SIZE = 20
DATABASE_MAX_OVERFLOW = 10
```

### Redis Caching

Enable caching for frequently accessed data:
```python
# In your route
@router.get("/architect/{id}")
@cache(ttl=300)  # Cache for 5 minutes
async def get_architecture(id: str):
    ...
```

### LLM Rate Limiting

Configure rate limits in `config.yaml`:
```yaml
rate_limits:
  requests_per_minute: 30
  tokens_per_minute: 100000
```

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | - | OpenAI API key |
| `DATABASE_URL` | Yes | - | PostgreSQL connection string |
| `REDIS_URL` | No | `redis://localhost:6379` | Redis connection string |
| `LOG_LEVEL` | No | `INFO` | Logging level |
| `ENVIRONMENT` | No | `development` | Environment name |
| `SECRET_KEY` | Yes | - | JWT signing secret |
| `CORS_ORIGINS` | No | `*` | Allowed CORS origins |
| `MAX_TOKENS_PER_REQUEST` | No | `4000` | Token limit per request |

## Additional Resources

- [API Documentation](./API.md)
- [Architecture Overview](./README.md)
- [Contributing Guide](./CONTRIBUTING.md)
- [Example Projects](./examples/)
