from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Any
from app.core.database import get_db
from app.api.deps import get_current_active_user, verificar_perfil
from app.models.Usuario import Usuario
from app.schemas.chamada import ChamadaCreate, ChamadaResponse
from app.services.chamada_service import ChamadaService

router = APIRouter()

@router.post("/", response_model=ChamadaResponse)
def criar_chamada(
    *, db: Session = Depends(get_db),
    chamada_data: ChamadaCreate,
    current_user: Usuario = Depends(verificar_perfil(["PROFESSOR"]))
) -> Any:
    chamada_service = ChamadaService(db)
    try:
        chamada = chamada_service.abrir_chamada(chamada_data, current_user.id)
        return chamada
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/{chamada_id}/encerrar")
def fechar_chamada(
    *, db: Session = Depends(get_db),
    chamada_id: int,
    current_user: Usuario = Depends(verificar_perfil(["PROFESSOR"]))
) -> Any:
    chamada_service = ChamadaService(db)
    try:
        chamada = chamada_service.encerrar_chamada(chamada_id)
        return {"message": "Chamada encerrada com sucesso"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{chamada_id}/relatorio")
def relatorio_presencas(
    chamada_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(verificar_perfil(["PROFESSOR", "ADMIN"]))
) -> Any:
    chamada_service = ChamadaService(db)
    return chamada_service.relatorio_presencas(chamada_id)
