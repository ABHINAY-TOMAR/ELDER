from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import HTTPException
import os
from app.api.routes import router
from app.core.config import settings
from app.models.schemas import Action, Observation, OpenEnvState, Reward
from app.openenv.interface import OpenEnvInterface

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Backend for the Architect Agent - translates NL requirements to system architectures."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

# OpenEnv Interface instance (module-level for external access)
openenv_interface = OpenEnvInterface()


async def reset(task_id: str) -> Observation:
    """OpenEnv reset() function - module-level export."""
    return await openenv_interface.reset(task_id)


async def step(action: Action) -> Reward:
    """OpenEnv step() function - module-level export."""
    return await openenv_interface.step(action)


def state() -> OpenEnvState:
    """OpenEnv state() function - module-level export."""
    return openenv_interface.state()


# Export at module level for OpenEnv compliance
__all__ = ["app", "reset", "step", "state", "openenv_interface"]


@app.post("/openenv/reset", response_model=Observation)
async def openenv_reset(task_id: str) -> Observation:
    try:
        return await reset(task_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/openenv/step", response_model=Reward)
async def openenv_step(action: Action) -> Reward:
    try:
        return await step(action)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/openenv/state", response_model=OpenEnvState)
async def openenv_state() -> OpenEnvState:
    return state()

@app.get("/health")
async def health_check():
    return {"status": "healthy", "project": settings.PROJECT_NAME}

# Serve frontend static files
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

