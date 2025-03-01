from fastapi import APIRouter
from app.services.password_cracker.router import router as password_cracker_router

api_router = APIRouter()

api_router.include_router(password_cracker_router, prefix="/crack", tags=["crack"])
