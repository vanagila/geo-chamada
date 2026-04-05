from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any
from app.core.database import get_db
from app.api.deps import get_current_active_user, verificar_perfil
from app.models.Usuario import Usuario
from app.schemas.disciplina import DisciplinaCreate, DisciplinaUpdate, DisciplinaResponse, DisciplinaMessage
from app.schemas.msg import Msg
from app.services.disciplina_service import DisciplinaService

router = APIRouter()

@router.post("/", response_model=DisciplinaResponse)
def criar_disciplina(
    *, db: Session = Depends(get_db),
    disciplina_data: DisciplinaCreate,
    current_user: Usuario = Depends(verificar_perfil(["ADMIN"]))
) -> Any:
    service = DisciplinaService(db)
    disciplina = service.create_disciplina(disciplina_data)
    return disciplina

@router.get("/", response_model=List[DisciplinaResponse])
def listar_disciplinas(
    *, db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user),
    skip: int = 0, limit: int = 100
) -> Any:
    service = DisciplinaService(db)
    disciplinas = service.get_all_disciplinas(skip, limit)
    return disciplinas

@router.get("/{disciplina_id}", response_model=DisciplinaResponse)
def listar_disciplina(
    *, db: Session = Depends(get_db),
    disciplina_id: int,
    current_user: Usuario = Depends(get_current_active_user)
) -> Any:
    service = DisciplinaService(db)
    disciplina = service.get_disciplina_by_id(disciplina_id)
    return disciplina

@router.get("/codigo/{codigo}", response_model=DisciplinaResponse)
def disciplina_por_codigo(
    *, db: Session = Depends(get_db),
    codigo: str,
    current_user: Usuario = Depends(get_current_active_user)
) -> Any:
    service = DisciplinaService(db)
    disciplina = service.get_disciplina_by_codigo(codigo)
    return disciplina

@router.put("/{disciplina_id}", response_model=DisciplinaMessage)
def atualizar_disciplina(
    *, db: Session = Depends(get_db),
    disciplina_id: int,
    disciplina_data: DisciplinaUpdate,
    current_user: Usuario = Depends(verificar_perfil(["ADMIN"]))
) -> Any:
    service = DisciplinaService(db)
    disciplina = service.update_disciplina(disciplina_id, disciplina_data)
    return disciplina

@router.delete("{disciplina_id}", response_model=Msg)
def deletar_disciplina(
    *, db: Session = Depends(get_db),
    disciplina_id: int,
    current_user: Usuario = Depends(verificar_perfil(["ADMIN"]))
) -> Any:
    service = DisciplinaService(db)
    return service.deletar_disciplina(disciplina_id)
