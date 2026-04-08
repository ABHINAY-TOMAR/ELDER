"""
ELDER Architect Agent — API Routes
Serves the frontend session lifecycle and connects to the backend engines.
"""
import uuid
import logging
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.engines.fast_pattern_matcher import fast_matcher
from app.engines.interaction_engine import interaction_engine
from app.engines.export_engine import export_engine

logger = logging.getLogger(__name__)

router = APIRouter()

# ─── In-memory session store (MVP: single user) ─── #
_sessions: dict[str, dict] = {}


# ─── Request models ─── #

class StartSessionInput(BaseModel):
    requirement: str

class StepSessionInput(BaseModel):
    session_id: str
    action: str

class ChatInput(BaseModel):
    prompt: str
    current_state: dict = {}

class ExportInput(BaseModel):
    requirement: Optional[str] = "N/A"
    domain: Optional[str] = "Unknown"
    tech_stack: Optional[str] = "Unknown"
    scale: Optional[str] = "Unknown"
    created_at: Optional[str] = None
    components: Optional[list] = []
    adrs: Optional[list] = []
    failure_modes: Optional[list] = []
    phases: Optional[list] = []
    details: Optional[str] = ""


# ─── Helpers ─── #

def _build_mermaid(components: list[dict], connections: list[dict]) -> str:
    """Generate a mermaid graph string from components and connections."""
    if not components:
        return "graph TD\n  A[No Components]"
    diagram = "graph TD\n"
    for comp in components:
        node_id = comp["name"].replace(" ", "_").replace("-", "_")
        ctype = comp.get("type", "service")
        if ctype == "database":
            shape = f"[({comp['name']})]"
        elif ctype == "gateway":
            shape = f"[{comp['name']}]"
        elif ctype == "queue":
            shape = f">{comp['name']}]"
        else:
            shape = f"([{comp['name']}])"
        diagram += f"  {node_id}{shape}\n"
    for conn in connections:
        from_id = conn["from"].replace(" ", "_").replace("-", "_")
        to_id = conn["to"].replace(" ", "_").replace("-", "_")
        protocol = conn.get("protocol", "HTTP")
        diagram += f"  {from_id} -->|{protocol}| {to_id}\n"
    return diagram


def _generate_architecture(requirement: str) -> dict:
    """
    Use the fast pattern matcher + heuristics to produce a complete
    SessionState from a single requirement string.
    """
    session_id = uuid.uuid4().hex[:16]
    now = datetime.now(timezone.utc).isoformat()

    # Detect domain
    req_lower = requirement.lower()
    if any(kw in req_lower for kw in ["ai", "llm", "agent", "ml", "rag"]):
        domain = "ai_native"
    elif any(kw in req_lower for kw in ["ecommerce", "shop", "payment", "store", "inventory"]):
        domain = "ecommerce"
    elif any(kw in req_lower for kw in ["chat", "realtime", "real-time", "websocket", "messaging"]):
        domain = "realtime"
    elif any(kw in req_lower for kw in ["video", "stream", "media"]):
        domain = "media_streaming"
    elif any(kw in req_lower for kw in ["game", "bgmi", "gaming"]):
        domain = "gaming"
    else:
        domain = "microservices"

    # Get recommendation from rule engine
    rec = fast_matcher.process_fast_recommendation(
        domain=domain, users=10000, budget=5000
    )
    tech = rec.get("tech_stack", {})

    # Build component graph based on domain
    components = [
        {
            "name": "API Gateway",
            "type": "gateway",
            "description": "Entry point for all client requests",
            "technology": "Nginx / Kong",
            "responsibilities": ["Request routing", "Rate limiting", "Auth"],
        },
        {
            "name": f"{domain.replace('_', ' ').title()} Service",
            "type": "service",
            "description": f"Core business logic for {domain}",
            "technology": tech.get("api", "fastapi"),
            "responsibilities": ["Business logic", "Data validation", "Event publishing"],
        },
        {
            "name": "Auth Service",
            "type": "service",
            "description": "Authentication and authorization",
            "technology": "FastAPI / Supabase Auth",
            "responsibilities": ["JWT/OAuth", "Session management", "RBAC"],
        },
        {
            "name": "Primary Database",
            "type": "database",
            "description": "Main persistent data store",
            "technology": tech.get("db", "postgresql"),
            "responsibilities": ["Data persistence", "ACID transactions"],
        },
        {
            "name": "Cache Layer",
            "type": "cache",
            "description": "In-memory caching for hot data",
            "technology": "Redis",
            "responsibilities": ["Session cache", "Rate limiting", "Pub/Sub"],
        },
    ]

    # Add domain-specific components
    if domain == "realtime":
        components.append({
            "name": "WebSocket Server",
            "type": "service",
            "description": "Real-time bidirectional communication",
            "technology": "Socket.IO / FastAPI WebSockets",
            "responsibilities": ["Connection management", "Message broadcasting", "Presence detection"],
        })

    if domain in ("media_streaming", "gaming"):
        components.append({
            "name": "CDN / Media Service",
            "type": "service",
            "description": "Content delivery and media processing",
            "technology": "CloudFront / FFmpeg",
            "responsibilities": ["Asset delivery", "Transcoding", "Edge caching"],
        })

    if tech.get("queue"):
        components.append({
            "name": "Message Queue",
            "type": "queue",
            "description": "Asynchronous event processing",
            "technology": tech["queue"],
            "responsibilities": ["Event streaming", "Decoupling", "Replay"],
        })

    # Build connections
    connections = [
        {"from": "API Gateway", "to": f"{domain.replace('_', ' ').title()} Service", "protocol": "REST"},
        {"from": "API Gateway", "to": "Auth Service", "protocol": "REST"},
        {"from": f"{domain.replace('_', ' ').title()} Service", "to": "Primary Database", "protocol": "SQL"},
        {"from": f"{domain.replace('_', ' ').title()} Service", "to": "Cache Layer", "protocol": "Redis"},
        {"from": "Auth Service", "to": "Primary Database", "protocol": "SQL"},
    ]

    if tech.get("queue"):
        connections.append({
            "from": f"{domain.replace('_', ' ').title()} Service",
            "to": "Message Queue",
            "protocol": tech["queue"].upper(),
        })

    # Generate ADRs
    adrs = [
        {
            "id": f"adr-{uuid.uuid4().hex[:6]}",
            "title": f"Use {tech.get('api', 'FastAPI')} as primary API framework",
            "decision": f"Selected {tech.get('api', 'FastAPI')} based on domain requirements and team expertise.",
            "rationale": rec.get("rationale", "Standard reliable baseline."),
            "consequences": ["Requires team familiarity", "Lock-in to ecosystem"],
            "status": "accepted",
        },
        {
            "id": f"adr-{uuid.uuid4().hex[:6]}",
            "title": f"Use {tech.get('db', 'PostgreSQL')} for primary data storage",
            "decision": f"Chose {tech.get('db', 'PostgreSQL')} for its reliability and feature set.",
            "rationale": "Strong ACID compliance, rich ecosystem, proven at scale.",
            "consequences": ["Vertical scaling limits", "Schema migration overhead"],
            "status": "accepted",
        },
        {
            "id": f"adr-{uuid.uuid4().hex[:6]}",
            "title": "Adopt API Gateway pattern for request routing",
            "decision": "Centralized gateway for auth, rate-limiting, and routing.",
            "rationale": "Simplifies client integration and enforces security at the edge.",
            "consequences": ["Single point of failure", "Added latency hop"],
            "status": "proposed",
        },
    ]

    # Generate failure modes from risky decisions
    failure_modes = []
    for risk in rec.get("risky_decisions", []):
        failure_modes.append({
            "component": risk.replace("_", " ").title(),
            "failure_type": "Design Risk",
            "probability": "medium",
            "impact": "high",
            "mitigation": f"Implement monitoring and graceful degradation for {risk.replace('_', ' ')}.",
        })
    failure_modes.extend([
        {
            "component": "Primary Database",
            "failure_type": "Connection Pool Exhaustion",
            "probability": "medium",
            "impact": "critical",
            "mitigation": "Use PgBouncer connection pooling, set max connections, implement circuit breaker.",
        },
        {
            "component": "Cache Layer",
            "failure_type": "Cache Stampede",
            "probability": "low",
            "impact": "high",
            "mitigation": "Implement cache warming, staggered TTLs, and probabilistic early expiration.",
        },
    ])

    # Generate phases
    phases = [
        {
            "id": f"phase-{uuid.uuid4().hex[:6]}",
            "name": "Foundation & Infrastructure",
            "status": "in_progress",
            "tasks": [
                {"id": f"task-{uuid.uuid4().hex[:6]}", "title": "Set up CI/CD pipeline", "description": "Configure GitHub Actions for automated testing and deployment", "status": "completed", "dependencies": []},
                {"id": f"task-{uuid.uuid4().hex[:6]}", "title": "Provision cloud infrastructure", "description": "Set up compute, networking, and managed services", "status": "in_progress", "dependencies": []},
                {"id": f"task-{uuid.uuid4().hex[:6]}", "title": "Configure monitoring stack", "description": "Deploy Prometheus, Grafana, and alerting", "status": "pending", "dependencies": []},
            ],
        },
        {
            "id": f"phase-{uuid.uuid4().hex[:6]}",
            "name": "Core Services Development",
            "status": "pending",
            "tasks": [
                {"id": f"task-{uuid.uuid4().hex[:6]}", "title": "Implement API Gateway", "description": "Set up routing, rate limiting, and auth middleware", "status": "pending", "dependencies": []},
                {"id": f"task-{uuid.uuid4().hex[:6]}", "title": "Build core business service", "description": f"Implement {domain} business logic and data models", "status": "pending", "dependencies": []},
                {"id": f"task-{uuid.uuid4().hex[:6]}", "title": "Set up database schema", "description": "Design and migrate initial database schema", "status": "pending", "dependencies": []},
            ],
        },
        {
            "id": f"phase-{uuid.uuid4().hex[:6]}",
            "name": "Testing & Launch",
            "status": "pending",
            "tasks": [
                {"id": f"task-{uuid.uuid4().hex[:6]}", "title": "Integration testing", "description": "End-to-end tests across all services", "status": "pending", "dependencies": []},
                {"id": f"task-{uuid.uuid4().hex[:6]}", "title": "Load testing", "description": "Stress test with expected traffic patterns", "status": "pending", "dependencies": []},
                {"id": f"task-{uuid.uuid4().hex[:6]}", "title": "Production deployment", "description": "Blue-green deploy to production environment", "status": "pending", "dependencies": []},
            ],
        },
    ]

    # Agent dispatches
    dispatches = [
        {"id": f"agent-{uuid.uuid4().hex[:6]}", "agent_name": "Pattern Analyzer", "task": "Evaluate architectural patterns", "status": "completed", "result": rec.get("rationale", "Analysis complete.")},
        {"id": f"agent-{uuid.uuid4().hex[:6]}", "agent_name": "Risk Assessor", "task": "Identify failure modes and risks", "status": "completed", "result": f"Found {len(failure_modes)} potential failure modes."},
        {"id": f"agent-{uuid.uuid4().hex[:6]}", "agent_name": "Cost Estimator", "task": "Estimate infrastructure costs", "status": "running"},
    ]

    # Default state if we want to bypass interaction or after interaction is complete
    mermaid_diagram = _build_mermaid(components, connections)

    session_state = {
        "id": session_id,
        "requirement": {
            "text": requirement,
            "domain": domain,
            "constraints": [],
            "stakeholders": [],
        },
        "domain": domain,
        "components": components,
        "connections": connections,
        "adrs": adrs,
        "failure_modes": failure_modes,
        "phases": phases,
        "dispatches": dispatches,
        "memory": [],
        "tokens": {
            "total": 1250,
            "input": 800,
            "output": 450,
            "cost": 0.0042,
        },
        "mermaid_diagram": mermaid_diagram,
        "pending_interaction": None,
        "created_at": now,
        "updated_at": now,
    }

    # CHECK FOR MISSING REQUIREMENTS
    # If the requirement is very short, we force an interaction
    if len(requirement) < 50:
        analysis = interaction_engine.analyze_requirements(requirement, {})
        if analysis["status"] == "incomplete":
            session_state["pending_interaction"] = {
                "field": analysis["field"],
                "question": analysis["prompt"]["question"],
                "options": analysis["prompt"]["options"]
            }

    _sessions[session_id] = session_state
    return session_state


# ─── Session Lifecycle Routes (Frontend facing) ─── #

@router.post("/start")
async def start_session(req: StartSessionInput):
    """Creates a new architecture session from a requirement prompt."""
    try:
        logger.info(f"Starting session for: {req.requirement[:80]}...")
        session = _generate_architecture(req.requirement)
        return session
    except Exception as e:
        logger.error(f"Failed to start session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/step")
async def step_session(req: StepSessionInput):
    """Processes a follow-up action on an existing session."""
    session = _sessions.get(req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    action = req.action
    session["updated_at"] = datetime.now(timezone.utc).isoformat()

    # 1. Handle Interaction Choices
    field = session.get("pending_interaction", {}).get("field")
    if field and not action.startswith(("approve_adr:", "toggle_task:")):
        session["requirement"][field] = action
        current_reqs = {k: v for k, v in session["requirement"].items() if k in ["project_type", "tech_stack", "scale_budget"]}
        analysis = interaction_engine.analyze_requirements(session["requirement"]["text"], current_reqs)
        
        if analysis["status"] == "incomplete":
            session["pending_interaction"] = {
                "field": analysis["field"],
                "question": analysis["prompt"]["question"],
                "options": analysis["prompt"]["options"]
            }
        else:
            session["pending_interaction"] = None
        return session

    # 2. Handle ADR Approval
    if action.startswith("approve_adr:"):
        adr_id = action.split(":")[1]
        for adr in session.get("adrs", []):
            if adr["id"] == adr_id:
                adr["status"] = "accepted"
                break
        return session

    # 3. Handle Task Toggling
    if action.startswith("toggle_task:"):
        task_id = action.split(":")[1]
        for phase in session.get("phases", []):
            for task in phase.get("tasks", []):
                if task["id"] == task_id:
                    # Cycle status: pending -> in_progress -> completed -> pending
                    current = task["status"]
                    if current == "pending":
                        task["status"] = "in_progress"
                    elif current == "in_progress":
                        task["status"] = "completed"
                    else:
                        task["status"] = "pending"
                    
                    # AUTO-UDPATE PHASE STATUS
                    tasks = phase.get("tasks", [])
                    completed_count = sum(1 for t in tasks if t["status"] == "completed")
                    in_progress_count = sum(1 for t in tasks if t["status"] == "in_progress")
                    
                    if completed_count == len(tasks):
                        phase["status"] = "completed"
                    elif in_progress_count > 0 or completed_count > 0:
                        phase["status"] = "in_progress"
                    else:
                        phase["status"] = "pending"
                    break
        return session
            
    return session


@router.get("/session")
async def get_session():
    """Returns the most recent session, or 404 if none exist."""
    if not _sessions:
        raise HTTPException(status_code=404, detail="No active session")
    latest_id = list(_sessions.keys())[-1]
    return _sessions[latest_id]


@router.post("/reset")
async def reset_session():
    """Clears all sessions."""
    _sessions.clear()
    return {"status": "ok", "message": "All sessions cleared."}


# ─── Requirement Interaction Routes ─── #

@router.post("/chat/analyze")
async def chat_analyze(req: ChatInput):
    """
    Evaluates the user's prompt and current session state
    to decide which requirements are missing.
    """
    result = interaction_engine.analyze_requirements(req.prompt, req.current_state)
    return result


# ─── Export Routes ─── #

@router.post("/export/docs")
async def export_docs(req: ExportInput):
    """Exports a comprehensive PDF containing PRD, TRD, and DRD."""
    filepath = export_engine.generate_prd_pdf(req.dict())
    if filepath:
        return FileResponse(filepath, media_type="application/pdf", filename="architecture_docs.pdf")
    raise HTTPException(status_code=500, detail="Failed to create documentation")


@router.post("/export/slides")
async def export_slides(req: ExportInput):
    """Generates a .pptx Presentation Deck."""
    filepath = export_engine.generate_architecture_slides(req.dict())
    if filepath:
        return FileResponse(
            filepath,
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            filename="architecture_deck.pptx",
        )
    raise HTTPException(status_code=500, detail="Failed to create slide deck")


# ─── Design Routes (Pattern Matcher) ─── #

class RequirementInput(BaseModel):
    project_name: str
    domain: str
    expected_users: int
    budget_usd: int
    latency_requirement_ms: int
    constraints: list[str]


@router.post("/design/fast")
async def get_fast_design(req: RequirementInput):
    recommendation = fast_matcher.process_fast_recommendation(
        domain=req.domain, users=req.expected_users, budget=req.budget_usd
    )
    return {"status": "success", "recommendation": recommendation}
