from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Any
from app.core.database import get_db
from app.api.deps import get_current_active_user, verificar_perfil
from app.models.Usuario import Usuario
from app.schemas.chamada import ChamadaCreate, ChamadaResponse, RelatorioChamadaResponse
from app.services.chamada_service import ChamadaService

router = APIRouter()

@router.post("/", response_model=ChamadaResponse)
def criar_chamada(
    *, db: Session = Depends(get_db),
    chamada_data: ChamadaCreate,
    current_user: Usuario = Depends(verificar_perfil(["PROFESSOR"]))
) -> Any:
    service = ChamadaService(db)
    return service.abrir_chamada(chamada_data, current_user.id)

@router.post("/{chamada_id}/encerrar", response_model=ChamadaResponse)
def encerrar_chamada(
    *, db: Session = Depends(get_db),
    chamada_id: int,
    current_user: Usuario = Depends(verificar_perfil(["PROFESSOR"]))
) -> Any:
    service = ChamadaService(db)
    return service.encerrar_chamada(chamada_id, current_user.id)

@router.get("/{chamada_id}/relatorio", response_model=RelatorioChamadaResponse)
def relatorio_presencas(
    *, chamada_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(verificar_perfil(["PROFESSOR", "ADMIN"]))
) -> Any:
    service = ChamadaService(db)
    return service.relatorio_chamada(chamada_id)

@router.get("/{chamada_id}", response_model=ChamadaResponse)
def get_chamada(
    *, db: Session = Depends(get_db),
    chamada_id: int,
    current_user: Usuario = Depends(verificar_perfil(["PROFESSOR", "ADMIN"]))
) -> Any:
    service = ChamadaService(db)
    return service.get_by_id(chamada_id)

@router.get("/turma/{turma_id}", response_model=List[ChamadaResponse])
def get_by_turma(
    *, db: Session = Depends(get_db),
    turma_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: Usuario = Depends(verificar_perfil(["PROFESSOR", "ADMIN"]))
) -> Any:
    service = ChamadaService(db)
    return service.get_by_turma(turma_id, skip, limit)

@router.get("/professor/{professor_id}", response_model=List[ChamadaResponse])
def get_by_professor(
    *, db: Session = Depends(get_db),
    professor_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: Usuario = Depends(verificar_perfil(["PROFESSOR", "ADMIN"]))
) -> Any:
    service = ChamadaService(db)
    return service.get_by_professor(professor_id, skip, limit)
