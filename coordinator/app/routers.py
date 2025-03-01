from fastapi import APIRouter
from .services.uploads import router as uploads_router

api_router = APIRouter()

api_router.include_router(uploads_router, prefix="/uploads", tags=["uploads"])
