from fastapi import APIRouter
from app.api.v1.endpoints import auth, usuarios

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["autenticação"])
api_router.include_router(usuarios.router, prefix="/usuarios", tags=["usuários"])
