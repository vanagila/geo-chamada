from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException, status
from app.repositories.turma_repository import TurmaRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.disciplina_repository import DisciplinaRepository
from app.schemas.turma import TurmaCreate, TurmaUpdate, TurmaMessage
from app.schemas.msg import Msg
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
        nova_turma = Turma(
            codigo=turma_data.codigo,
            disciplina_id=turma_data.disciplina_id,
            semestre=turma_data.semestre,
            ano=turma_data.ano,
            horario=turma_data.horario,
            data_inicio=turma_data.data_inicio,
            data_fim=turma_data.data_fim
        )

        turma_salva = self.repository.save(nova_turma)
        turma_salva.disciplina = disciplina
        return turma_salva

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

    def update_turma(self, turma_id: int, turma_data: TurmaUpdate) -> TurmaMessage:
        turma = self.repository.get_by_id(turma_id)
        if not turma:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Turma não encontrada"
            )
        update_data = turma_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(turma, field, value)

        turma_atualizada = self.repository.save(turma)
        return TurmaMessage(
            message="Turma atualizada com sucesso",
            turma=turma_atualizada
        )

    def delete_turma(self, turma_id: int) -> Msg:
        turma = self.repository.get_by_id(turma_id)
        if not turma:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Turma não encontrada"
        )
        self.repository.delete(turma)
        return Msg(
            message="Turma deletada com sucesso"
        )

    def add_professor_turma(self, turma_id: int, professor_id: int) -> TurmaMessage:
        turma = self.repository.get_by_id(turma_id)
        professor = self.usuario_repo.get_by_id(professor_id)

        if not professor or professor.tipo.value != "PROFESSOR":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Professor não encontrado"
            )

        if professor not in turma.professores:
            turma.professores.append(professor)
            self.repository.save(turma)

        return TurmaMessage(
            message="Professor adicionado com sucesso",
            turma=turma
        )

    def remove_professor_turma(self, turma_id: int, professor_id: int) -> TurmaMessage:
        turma = self.repository.get_by_id(turma_id)
        professor = self.usuario_repo.get_by_id(professor_id)

        if not professor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Professor não encontrado"
            )

        if professor in turma.professores:
            turma.professores.remove(professor)
            self.repository.save(turma)

        return TurmaMessage(
            message="Professor removido com sucesso",
            turma=turma
        )

    def add_aluno_turma(self, turma_id: int, aluno_id: int) -> TurmaMessage:
        turma = self.repository.get_by_id(turma_id)
        aluno = self.usuario_repo.get_by_id(aluno_id)

        if not aluno or aluno.tipo.value != "ALUNO":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aluno não encontrado"
            )

        if aluno not in turma.alunos:
            turma.alunos.append(aluno)
            self.repository.save(turma)

        return TurmaMessage(
            message="Aluno adicionado com sucesso",
            turma=turma
        )

    def remove_aluno_turma(self, turma_id: int, aluno_id: int) -> TurmaMessage:
        turma = self.repository.get_by_id(turma_id)
        aluno = self.usuario_repo.get_by_id(aluno_id)

        if not aluno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aluno não encontrado"
            )

        if aluno in turma.alunos:
            turma.alunos.remove(aluno)
            self.repository.save(turma)

        return TurmaMessage(
            message="Aluno removido com sucesso",
            turma=turma
        )
