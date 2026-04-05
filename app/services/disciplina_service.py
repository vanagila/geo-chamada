from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException, status
from app.repositories.disciplina_repository import DisciplinaRepository
from app.schemas.disciplina import DisciplinaCreate, DisciplinaUpdate
from app.models.Disciplina import Disciplina

class DisciplinaService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = DisciplinaRepository(db)

    def create_disciplina(self, disciplina_data: DisciplinaCreate) -> Disciplina:
        if self.repository.get_by_codigo(disciplina_data.codigo):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Código de disciplina já cadastrado"
            )
        return self.repository.create(disciplina_data)

    def get_all_disciplinas(self, skip: int = 0, limit: int = 100) -> List[Disciplina]:
        return self.repository.get_all(skip, limit)

    def get_disciplina_by_id(self, disciplina_id: int) -> Disciplina:
        disciplina = self.repository.get_by_id(disciplina_id)
        if not disciplina:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Disciplina não encontrada"
            )
        return disciplina

    def get_disciplina_by_codigo(self, codigo: str) -> Disciplina:
        disciplina = self.repository.get_by_codigo(codigo)
        if not disciplina:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Disciplina não encontrada"
            )
        return disciplina

    def update_disciplina(self, disciplina_id: int, disciplina_data: DisciplinaUpdate) -> dict:
        disciplina = self.repository.get_by_id(disciplina_id)
        if not disciplina:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Disciplina não encontrada"
            )
        return {
            "message": "Disciplina atualizada com sucesso",
            "disciplina": disciplina
        }

    def delete_disciplina(self, disciplina_id: int) -> dict:
        if self.repository.delete(disciplina_id):
            return {"message": "Disciplina deletada com sucesso"}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Disciplina não encontrada"
        )
