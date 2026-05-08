from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Any
from datetime import datetime
from app.core.database import get_db
from app.api.deps import get_current_active_user, verificar_perfil
from app.models.Usuario import Usuario
from app.schemas.presenca import PresencaResponse, PresencaCreate, AbonoRequest, HistoricoAlunoDisciplinaResponse
from app.services.presenca_service import PresencaService

router = APIRouter()

@router.post("/registrar", response_model=PresencaResponse)
def registrar_presenca(
    *, db: Session = Depends(get_db),
    presenca_data: PresencaCreate,
    current_user: Usuario = Depends(verificar_perfil(["ALUNO"]))
) -> Any:
    service = PresencaService(db)
    presenca, dentro = service.marcar_presenca(
        current_user.id,
        presenca_data
    )
    return {
        "id": presenca.id,
        "aluno_id": presenca.aluno_id,
        "chamada_id": presenca.chamada_id,
        "distancia_calculada": presenca.distancia_calculada,
        "data_registro": presenca.data_registro,
        "status": presenca.status,
        "dentro_raio": dentro
    }

@router.post("/abonar")
def abonar_falta(
    *, db: Session = Depends(get_db),
    abonar_data: AbonoRequest,
    current_user: Usuario = Depends(verificar_perfil(["PROFESSOR"]))
) -> Any:
    service = PresencaService(db)
    return service.abonar_ausencia(
        current_user.id,
        abonar_data.presenca_id,
        abonar_data.motivo
    )

@router.get("/historico_aluno", response_model=List[PresencaResponse])
def get_historico_aluno(
    *, db: Session = Depends(get_db),
    current_user: Usuario = Depends(verificar_perfil(["ALUNO"]))
) -> Any:
    service = PresencaService(db)
    return service.historico_aluno(current_user.id)

@router.get("/historico/disciplina/{disciplina_id}", response_model=HistoricoAlunoDisciplinaResponse)
def get_historico_aluno_disciplina(
    *, db: Session = Depends(get_db),
    disciplina_id: int,
    current_user: Usuario = Depends(verificar_perfil(["ALUNO"]))
) -> Any:
    service = PresencaService(db)
    return service.historico_aluno_disciplina(current_user.id, disciplina_id)

@router.get("/turma/{turma_id}", response_model=List[PresencaResponse])
def get_presencas_turma(
    *, db: Session = Depends(get_db),
    turma_id: int,
    data_inicio: datetime = Query(None),
    data_fim: datetime = Query(None),
    current_user: Usuario = Depends(verificar_perfil(["PROFESSOR", "ADMIN"]))
):
    service = PresencaService(db)
    return service.get_presencas_turma(turma_id, data_inicio, data_fim)

@router.get("/chamada/{chamada_id}", response_model=List[PresencaResponse])
def get_presencas_chamada(
    *, db: Session = Depends(get_db),
    chamada_id: int,
    current_user: Usuario = Depends(verificar_perfil(["PROFESSOR", "ADMIN"]))
):
    service = PresencaService(db)
    return service.presencas_chamada(chamada_id)
