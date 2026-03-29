from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from app.core.config import settings
from app.core.database import engine, Base
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from app.models.Usuario import Usuario
from app.models.Disciplina import Disciplina
from app.models.Presenca import Presenca
from app.models.Turma import Turma
from app.models.Chamada import Chamada

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware, 
    allow_methods=["*"], 
    allow_headers=["*"], 
    allow_origins=settings.BACKEND_CORS_ORIGINS,)

app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    logger.info("Iniciando GeoChamada")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Banco de dados verificado")
    except Exception as e:
        logger.error(f"Erro ao conectar banco: {e}")

@app.get("/")
def root():
    return {
        "message": "GeoChamada API",
        "status": "online",
        "docs": "/docs"
    }
