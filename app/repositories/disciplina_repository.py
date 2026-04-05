from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.Disciplina import Disciplina
from app.schemas.disciplina import DisciplinaCreate, DisciplinaUpdate

class DisciplinaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, disciplina_data: DisciplinaCreate) -> Disciplina:
        db_disciplina = Disciplina(
            nome=disciplina_data.nome,
            codigo=disciplina_data.codigo,
            descricao=disciplina_data.descricao
        )

        self.db.add(db_disciplina)
        self.db.commit()
        self.db.refresh(db_disciplina)
        return db_disciplina

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Disciplina]:
        return self.db.query(Disciplina).offset(skip).limit(limit).all()

    def get_by_id(self, disciplina_id: int) -> Optional[Disciplina]:
        return self.db.query(Disciplina).filter(Disciplina.id == disciplina_id).first()

    def get_by_codigo(self, codigo: str) -> Optional[Disciplina]:
        return self.db.query(Disciplina).filter(Disciplina.codigo == codigo).first()

    def update(self, disciplina_id: int, disciplina_data: DisciplinaUpdate) -> Optional[Disciplina]:
        disciplina = self.get_by_id(disciplina_id)
        if disciplina:
            update_data = disciplina_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                if hasattr(disciplina, field):
                    setattr(disciplina, field, value)
            self.db.commit()
            self.db.refresh(disciplina)
            return disciplina

    def delete(self, disciplina_id: int) -> bool:
        disciplina = self.get_by_id(disciplina_id)
        if disciplina:
            self.db.delete(disciplina)
            self.db.commit()
            return True
        return False

    def count_turmas(self, disciplina_id: int) -> int:
        try:
            count = self.db.query(Turma).filter(
            Turma.disciplina_id == disciplina_id).count()
            return count
        except Exception as e:
            print(f"Erro ao contar turmas: {e}")
            return 0
