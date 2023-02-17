from fastapi import APIRouter
from .stat.routes import router as stat_routes

router = APIRouter(prefix="/api/v1")

router.include_router(stat_routes)
