"""Versioned API router."""

from fastapi import APIRouter

from verse_agent.api.v1.endpoints.health import router as health_router

router = APIRouter()
router.include_router(health_router)
