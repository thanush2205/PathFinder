"""API routes initialization"""
from fastapi import APIRouter
from .auth import router as auth_router
from .analytics import router as analytics_router
from .sessions import router as sessions_router
from .complaints import router as complaints_router
from .ai_demo import router as ai_demo_router
from .yolo_detection import router as yolo_router

# Create main API router
api_router = APIRouter(prefix="/api")

# Include all sub-routers
api_router.include_router(auth_router)
api_router.include_router(analytics_router)
api_router.include_router(sessions_router)
api_router.include_router(complaints_router)
api_router.include_router(ai_demo_router)  # AI Demo (no dependencies needed)
api_router.include_router(yolo_router, prefix="/detection", tags=["yolo-detection"])  # YOLO real-time detection

__all__ = ["api_router"]
