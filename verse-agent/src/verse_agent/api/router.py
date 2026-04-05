"""Top-level API router registration."""

from fastapi import APIRouter

from verse_agent.api.v1.endpoints.health import public_router as health_public_router
from verse_agent.api.v1.router import router as v1_router

public_router = APIRouter()
public_router.include_router(health_public_router)

api_router = APIRouter()
api_router.include_router(v1_router)
