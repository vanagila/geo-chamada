from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException, status
from app.repositories.disciplina_repository import DisciplinaRepository
from app.schemas.disciplina import DisciplinaCreate, DisciplinaUpdate, DisciplinaMessage
from app.schemas.msg import Msg
from app.models.Disciplina import Disciplina

class DisciplinaService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = DisciplinaRepository(db)

    def _attach_count(self, disciplina: Disciplina) -> Disciplina:
        count = self.repository.count_turmas(disciplina.id)
        disciplina.turmas_count = count
        return disciplina

    def create_disciplina(self, disciplina: DisciplinaCreate) -> Disciplina:
        if self.repository.get_by_codigo(disciplina.codigo):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Código de disciplina já cadastrado"
            )

        nova_disciplina = Disciplina(
            nome=disciplina.nome,
            codigo=disciplina.codigo,
            descricao=disciplina.descricao
        )

        disciplina_salva = self.repository.save(nova_disciplina)
        disciplina_salva.turmas_count = 0
        return disciplina_salva

    def get_all_disciplinas(self, skip: int = 0, limit: int = 100) -> List[Disciplina]:
        disciplinas = self.repository.get_all(skip, limit)
        for d in disciplinas:
            self._attach_count(d)
        return disciplinas 

    def get_disciplina_by_id(self, disciplina_id: int) -> Disciplina:
        disciplina = self.repository.get_by_id(disciplina_id)
        if not disciplina:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Disciplina não encontrada"
            )
        return self._attach_count(disciplina)

    def get_disciplina_by_codigo(self, codigo: str) -> Disciplina:
        disciplina = self.repository.get_by_codigo(codigo)
        if not disciplina:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Disciplina não encontrada"
            )
        return self._attach_count(disciplina)

    def update_disciplina(self, disciplina_id: int, disciplina_data: DisciplinaUpdate) -> DisciplinaMessage:
        disciplina = self.repository.get_by_id(disciplina_id)
        if not disciplina:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Disciplina não encontrada"
            )

        update_data = disciplina_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(disciplina, field, value)

        disciplina_atualizada = self.repository.save(disciplina)
        self._attach_count(disciplina_atualizada)

        return DisciplinaMessage(
            message="Disciplina atualizada com sucesso",
            disciplina=disciplina_atualizada
        )

    def delete_disciplina(self, disciplina_id: int) -> dict:
        disciplina = self.repository.get_by_id(disciplina_id)
        if not disciplina:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Disciplina não encontrada"
            )

        if self.repository.count_turmas(disciplina_id) > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não é possível deletar esta disciplina, pois existem turmas vinculadas a ela"
            )

        self.repository.delete(disciplina)
        return Msg(
            message="Disciplina deletada com sucesso"
        )
