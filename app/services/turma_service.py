from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException, status
from app.repositories.turma_repository import TurmaRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.disciplina_repository import DisciplinaRepository
from app.schemas.turma import TurmaCreate, TurmaUpdate
from app.models.Turma import Turma

class TurmaService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = TurmaRepository(db)
        self.usuario_repo = UsuarioRepository(db)
        self.disciplina_repo = DisciplinaRepository(db)

    def create_turma(self, turma_data: TurmaCreate) -> Turma:
        disciplina = self.disciplina_repo.get_by_id(turma_data.disciplina_id)
        if not disciplina:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Disciplina não encontrada"
            )

        if self.repository.get_by_codigo(turma_data.codigo):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Código de turma já cadastrado"
            )
        nova_turma = self.repository.create(turma_data)
        nova_turma.disciplina = disciplina
        return nova_turma

    def get_all_turmas(self, skip: int = 0, limit: int = 100) -> List[Turma]:
        return self.repository.get_all(skip, limit)

    def get_turma_by_id(self, turma_id: int) -> Turma:
        turma = self.repository.get_by_id(turma_id)
        if not turma:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Turma não encontrada"
            )
        return turma

    def get_turma_by_codigo(self, codigo: str) -> Turma:
        turma = self.repository.get_by_codigo(codigo)
        if not turma:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Turma não encontrada"
            )
        return turma

    def get_turmas_by_professor(self, professor_id: int, skip: int = 0, limit: int = 100) -> List[Turma]:
        professor = self.usuario_repo.get_by_id(professor_id)
        if not professor or professor.tipo.value != "PROFESSOR":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Professor não encontrado"
            )
        return self.repository.get_by_professor(professor_id, skip, limit)

    def get_turmas_by_aluno(self, aluno_id: int, skip: int = 0, limit: int = 100) -> List[Turma]:
        aluno = self.usuario_repo.get_by_id(aluno_id)
        if not aluno or aluno.tipo.value != "ALUNO":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aluno não encontrado"
            )
        return self.repository.get_by_aluno(aluno_id, skip, limit)

    def update_turma(self, turma_id: int, turma_data: TurmaUpdate) -> dict:
        turma = self.repository.update(turma_id, turma_data)
        if not turma:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Turma não encontrada"
            )
        return {
            "message": "Turma atualizada com sucesso",
            "turma": turma
        }

    def delete_turma(self, turma_id: int) -> dict:
        if self.repository.delete(turma_id):
            return {"message": "Turma deletada com sucesso"}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Turma não encontrada"
        )

    def add_professor_turma(self, turma_id: int, professor_id: int) -> dict:
        turma = self.repository.add_professor(turma_id, professor_id)
        if not turma:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Turma ou professor não encontrado"
        )
        return {
            "message": "Professor adicionado com sucesso",
            "turma": turma
        }

    def remove_professor_turma(self, turma_id: int, professor_id: int) -> dict:
        turma = self.repository.remove_professor(turma_id, professor_id)
        if not turma:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Turma ou professor não encontrado"
        )
        return {
            "message": "Professor removido com sucesso",
            "turma": turma
        }

    def add_aluno_turma(self, turma_id: int, aluno_id: int) -> dict:
        turma = self.repository.add_aluno(turma_id, aluno_id)
        if not turma:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Turma ou aluno não encontrado"
        )
        return {
            "message": "Aluno adicionado com sucesso",
            "turma": turma
        }

    def remove_aluno_turma(self, turma_id: int, aluno_id: int) -> dict:
        turma = self.repository.remove_aluno(turma_id, aluno_id)
        if not turma:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Turma ou aluno não encontrado"
        )
        return {
            "message": "Professor removido com sucesso",
            "turma": turma
        }
