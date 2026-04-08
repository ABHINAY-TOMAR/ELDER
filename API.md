# ELDER API Documentation

## Base URL

```
Production: https://api.elder-architecture.com/v1
Development: http://localhost:8000/api/v1
```

## Authentication

All API requests require an API key in the header:

```
Authorization: Bearer YOUR_API_KEY
```

## Endpoints

### Architecture Design

#### POST `/architect`

Generate a system architecture from natural language requirements.

**Request Body:**

```json
{
  "requirement": "Design a real-time chat application supporting 10,000 concurrent users",
  "constraints": {
    "max_latency_ms": 100,
    "availability_target": 0.999,
    "budget_constraint": "medium",
    "compliance_requirements": ["GDPR", "SOC2"]
  },
  "context": {
    "existing_systems": ["legacy monolith", "PostgreSQL 12"],
    "team_expertise": ["Python", "React", "AWS"],
    "preferred_technologies": ["FastAPI", "Redis"]
  },
  "options": {
    "include_failure_modes": true,
    "include_adrs": true,
    "include_mermaid": true,
    "depth": "comprehensive"
  }
}
```

**Response:**

```json
{
  "architecture": {
    "id": "arch_abc123def456",
    "name": "Real-time Chat Platform",
    "components": [
      {
        "id": "comp_001",
        "name": "API Gateway",
        "type": "gateway",
        "technology": "Kong",
        "responsibilities": ["Rate limiting", "Authentication", "Request routing"],
        "scalability": "horizontal",
        "instances": 3
      },
      {
        "id": "comp_002",
        "name": "Chat Service",
        "type": "service",
        "technology": "FastAPI",
        "responsibilities": ["Message handling", "WebSocket management"],
        "scalability": "horizontal",
        "instances": 5
      }
    ],
    "connections": [
      {
        "from": "comp_001",
        "to": "comp_002",
        "protocol": "HTTP/WebSocket",
        "description": "Client requests routed to chat service"
      }
    ],
    "mermaid_diagram": "graph TD\n    A[Client] --> B[API Gateway]..."
  },
  "adrs": [
    {
      "id": "ADR-001",
      "title": "Use WebSocket for Real-time Communication",
      "status": "accepted",
      "context": "Chat requires real-time message delivery",
      "decision": "Implement WebSocket connections via Socket.IO",
      "consequences": ["Increased complexity", "Better user experience"]
    }
  ],
  "failure_modes": [
    {
      "component": "Chat Service",
      "failure_mode": "Service unavailable",
      "probability": "low",
      "impact": "high",
      "mitigation": "Multi-zone deployment with automatic failover"
    }
  ],
  "implementation_phases": [
    {
      "phase": 1,
      "name": "Foundation",
      "duration_weeks": 4,
      "tasks": ["Set up infrastructure", "Deploy API Gateway"]
    }
  ],
  "confidence_score": 0.87,
  "metadata": {
    "processing_time_ms": 2340,
    "tokens_used": 8500,
    "model": "gpt-4-turbo"
  }
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid request
- `422`: Validation error
- `500`: Server error

---

#### POST `/architect/stream`

Stream architecture generation progress (Server-Sent Events).

**Request Body:** Same as `/architect`

**Response (SSE):**

```
event: phase
data: {"phase": "classification", "status": "started"}

event: phase
data: {"phase": "classification", "status": "completed", "result": {...}}

event: phase
data: {"phase": "generation", "status": "started"}

event: result
data: {"architecture": {...}}

event: done
data: {"total_time_ms": 2340}
```

---

### Session Management

#### POST `/session`

Create a new architecture session.

**Request Body:**

```json
{
  "client_id": "user_123",
  "project_name": "Chat Platform v2"
}
```

**Response:**

```json
{
  "session_id": "sess_xyz789",
  "created_at": "2024-01-15T10:30:00Z",
  "expires_at": "2024-01-15T11:30:00Z"
}
```

---

#### GET `/session/{session_id}`

Get session details and history.

**Response:**

```json
{
  "session_id": "sess_xyz789",
  "project_name": "Chat Platform v2",
  "created_at": "2024-01-15T10:30:00Z",
  "architectures": [
    {
      "id": "arch_abc123",
      "created_at": "2024-01-15T10:35:00Z",
      "requirement_summary": "Real-time chat..."
    }
  ],
  "token_usage": {
    "total_tokens": 45000,
    "cost_usd": 1.25
  }
}
```

---

#### DELETE `/session/{session_id}`

Delete a session and all associated data.

**Response:**
```json
{
  "status": "deleted",
  "session_id": "sess_xyz789"
}
```

---

### Knowledge Base

#### GET `/memory/search`

Search previous architecture decisions.

**Query Parameters:**
- `query` (string, required): Search query
- `limit` (integer, optional): Max results (default: 10)
- `threshold` (float, optional): Similarity threshold (default: 0.75)

**Example:**
```
GET /memory/search?query=microservices%20chat&limit=5
```

**Response:**

```json
{
  "results": [
    {
      "id": "mem_001",
      "content": "Architecture for real-time chat using WebSocket...",
      "similarity": 0.89,
      "created_at": "2024-01-10T14:20:00Z"
    }
  ],
  "total_results": 1
}
```

---

#### POST `/memory/store`

Store an architecture in memory.

**Request Body:**

```json
{
  "content": "Designed microservices chat platform with...",
  "category": "chat-application",
  "tags": ["real-time", "websocket", "scalable"],
  "metadata": {
    "component_count": 12,
    "complexity": "high"
  }
}
```

**Response:**

```json
{
  "id": "mem_xyz123",
  "stored_at": "2024-01-15T12:00:00Z"
}
```

---

### Token Usage

#### GET `/usage/summary`

Get token usage summary.

**Query Parameters:**
- `start_date` (string, optional): Start date (ISO format)
- `end_date` (string, optional): End date (ISO format)
- `group_by` (string, optional): `day`, `week`, `month`

**Response:**

```json
{
  "total_tokens": 150000,
  "total_cost_usd": 4.50,
  "breakdown": {
    "prompt_tokens": 120000,
    "completion_tokens": 30000
  },
  "by_period": [
    {"date": "2024-01-15", "tokens": 45000, "cost_usd": 1.35}
  ]
}
```

---

#### GET `/usage/session/{session_id}`

Get token usage for a specific session.

**Response:**

```json
{
  "session_id": "sess_xyz789",
  "total_tokens": 8500,
  "cost_usd": 0.25,
  "requests": [
    {
      "timestamp": "2024-01-15T10:35:00Z",
      "tokens": 4500,
      "operation": "architecture_generation"
    }
  ]
}
```

---

### Health & Status

#### GET `/health`

Health check endpoint.

**Response:**

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "uptime_seconds": 86400,
  "dependencies": {
    "database": "connected",
    "redis": "connected",
    "llm_service": "available"
  }
}
```

---

#### GET `/status`

Detailed system status.

**Response:**

```json
{
  "status": "operational",
  "models": {
    "gpt-4-turbo": {"status": "available", "avg_latency_ms": 450},
    "gpt-3.5-turbo": {"status": "available", "avg_latency_ms": 200}
  },
  "rate_limits": {
    "requests_per_minute": 60,
    "tokens_per_minute": 150000
  }
}
```

---

## OpenEnv Endpoints

### POST `/openenv/reset`

Reset OpenEnv evaluation session.

**Request Body:**

```json
{
  "task_id": "task_1",
  "seed": 42
}
```

**Response:**

```json
{
  "session_id": "oe_sess_123",
  "task": {
    "id": "task_1",
    "description": "Design a basic e-commerce checkout flow"
  }
}
```

---

### POST `/openenv/step`

Submit an answer for evaluation.

**Request Body:**

```json
{
  "session_id": "oe_sess_123",
  "answer": {
    "architecture": {...},
    "reasoning": "I chose microservices because..."
  }
}
```

**Response:**

```json
{
  "reward": 0.85,
  "done": false,
  "info": {
    "score_breakdown": {
      "completeness": 0.9,
      "correctness": 0.8,
      "best_practices": 0.85
    }
  }
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid requirement format",
    "details": [
      {"field": "requirement", "message": "must be at least 10 characters"}
    ]
  }
}
```

**Error Codes:**
- `VALIDATION_ERROR`: Request validation failed
- `AUTHENTICATION_ERROR`: Invalid or missing API key
- `RATE_LIMIT_ERROR`: Rate limit exceeded
- `PROCESSING_ERROR`: Architecture generation failed
- `INTERNAL_ERROR`: Server-side error

---

## Rate Limits

| Plan | Requests/Min | Tokens/Min | Concurrent |
|------|--------------|------------|------------|
| Free | 10 | 50,000 | 2 |
| Pro | 60 | 150,000 | 10 |
| Enterprise | Unlimited | Unlimited | Unlimited |

---

## SDK Examples

### Python

```python
from elder import ELDERClient

client = ELDERClient(api_key="your-api-key")

# Generate architecture
result = client.architect(
    requirement="Design a scalable e-commerce platform",
    constraints={"availability_target": 0.999}
)

print(result.architecture.mermaid_diagram)
```

### JavaScript

```javascript
import { ELDERClient } from '@elder/sdk';

const client = new ELDERClient({ apiKey: 'your-api-key' });

const result = await client.architect({
  requirement: 'Design a scalable e-commerce platform',
  constraints: { availability_target: 0.999 }
});

console.log(result.architecture.mermaidDiagram);
```

---

## Webhooks

Configure webhooks to receive async notifications:

```json
{
  "url": "https://your-server.com/webhook",
  "events": ["architecture.completed", "architecture.failed"],
  "secret": "your-webhook-secret"
}
```

---

## Changelog

### v1.0.0 (2024-01-15)
- Initial release
- Architecture generation endpoint
- Session management
- Knowledge base with vector search
- OpenEnv integration
