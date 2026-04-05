from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any
from app.core.database import get_db
from app.api.deps import get_current_active_user, verificar_perfil
from app.models.Usuario import Usuario
from app.schemas.turma import TurmaCreate, TurmaUpdate, TurmaResponse, TurmaMessage
from app.services.turma_service import TurmaService

router = APIRouter()

@router.post("/", response_model=TurmaResponse)
def criar_turma(
    *, db: Session = Depends(get_db),
    turma_data: TurmaCreate,
    current_user: Usuario = Depends(verificar_perfil(["ADMIN"]))
) -> Any:
    service = TurmaService(db)
    turma = service.create_turma(turma_data)
    return turma

@router.get("/", response_model=List[TurmaResponse])
def listar_turmas(
    *, db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user),
    skip: int = 0, limit: int = 0
) -> Any:
    service = TurmaService(db)
    turmas = service.get_all_turmas(skip, limit)
    return turmas

@router.get("/{turma_id}", response_model=TurmaResponse)
def listar_turma(
    *, db: Session = Depends(get_db),
    turma_id: int,
    current_user: Usuario = Depends(get_current_active_user)
) -> Any:
    service = TurmaService(db)
    turma = service.get_turma_by_id(turma_id)
    return turma

@router.get("/codigo/{codigo}", response_model=TurmaResponse)
def turma_por_codigo(
    *, db: Session = Depends(get_db),
    codigo: str,
    current_user: Usuario = Depends(get_current_active_user)
) -> Any:
    service = TurmaService(db)
    turma = service.get_turma_by_codigo(codigo)
    return turma

@router.get("/professor/{professor_id}", response_model=List[TurmaResponse])
def turmas_por_professor(
    *, db: Session = Depends(get_db),
    professor_id: int,
    current_user: Usuario = Depends(get_current_active_user),
    skip: int = 0, limit: int = 0
) -> Any:
    service = TurmaService(db)
    turmas = service.get_turmas_by_professor(professor_id, skip, limit)
    return turmas

@router.get("/aluno/{aluno_id}", response_model=List[TurmaResponse])
def turmas_por_aluno(
    *, db: Session = Depends(get_db),
    aluno_id: int,
    current_user: Usuario = Depends(get_current_active_user),
    skip: int = 0, limit: int = 0
) -> Any:
    service = TurmaService(db)
    turmas = service.get_turmas_by_aluno(aluno_id, skip, limit)
    return turmas

@router.put("/{turma_id}", response_model=TurmaMessage)
def atualizar_turma(
    *, db: Session = Depends(get_db),
    turma_id: int,
    turma_data: TurmaUpdate,
    current_user: Usuario = Depends(verificar_perfil(["ADMIN"]))
) -> Any:
    service = TurmaService(db)
    turma = service.update_turma(turma_id, turma_data)
    return turma

@router.delete("/{turma_id}", response_model=TurmaMessage)
def deletar_turma(
    *, db: Session = Depends(get_db),
    turma_id: int,
    current_user: Usuario = Depends(verificar_perfil(["ADMIN"]))
) -> Any:
    service = TurmaService(db)
    return service.deletar_turma(turma_id)

@router.post("/{turma_id}/professores/{professor_id}", response_model=TurmaMessage)
def adicionar_professor_turma(
    *, db: Session = Depends(get_db),
    turma_id: int,
    professor_id: int,
    current_user: Usuario = Depends(verificar_perfil(["ADMIN"]))
) -> Any:
    service = TurmaService(db)
    turma = service.add_professor_turma(turma_id, professor_id)
    return turma

@router.delete("/{turma_id}/professores/{professor_id}", response_model=TurmaMessage)
def remover_professor_turma(
    *, db: Session = Depends(get_db),
    turma_id: int,
    professor_id: int,
    current_user: Usuario = Depends(verificar_perfil(["ADMIN"]))
) -> Any:
    service = TurmaService(db)
    turma = service.remove_professor_turma(turma_id, professor_id)
    return turma

@router.post("/{turma_id}/alunos/{aluno_id}", response_model=TurmaMessage)
def adicionar_aluno_turma(
    *, db: Session = Depends(get_db),
    turma_id: int,
    aluno_id: int,
    current_user: Usuario = Depends(verificar_perfil(["ADMIN"]))
) -> Any:
    service = TurmaService(db)
    turma = service.add_aluno_turma(turma_id, aluno_id)
    return turma

@router.delete("/{turma_id}/alunos/{aluno_id}", response_model=TurmaMessage)
def remover_aluno_turma(
    *, db: Session = Depends(get_db),
    turma_id: int,
    aluno_id: int,
    current_user: Usuario = Depends(verificar_perfil(["ADMIN"]))
) -> Any:
    service = TurmaService(db)
    turma = service.remove_aluno_turma(turma_id, aluno_id)
    return turma
