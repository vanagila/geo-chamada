from sqlalchemy.orm import Session, joinedload
from typing import Optional, List
from app.models.Turma import Turma
from app.models.Usuario import Usuario
from app.schemas.turma import TurmaCreate, TurmaUpdate

class TurmaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, turma_id: int) -> Optional[Turma]:
        return self.db.query(Turma).options(
            joinedload(Turma.disciplina),
            joinedload(Turma.professores),
            joinedload(Turma.alunos)
        ).filter(Turma.id == turma_id).first()

    def get_by_codigo(self, codigo: str) -> Optional[Turma]:
        return self.db.query(Turma).filter(Turma.codigo == codigo).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Turma]:
        return self.db.query(Turma).options(
            joinedload(Turma.disciplina)
        ).offset(skip).limit(limit).all() 

    def get_by_professor(self, professor_id: int, skip: int = 0, limit: int = 100) -> List[Turma]:
        return self.db.query(Turma).join(Turma.professores).filter(
            Usuario.id == professor_id
        ).offset(skip).limit(limit).all()

    def get_by_aluno(self, aluno_id: int, skip: int = 0, limit: int = 100) -> List[Turma]:
        return self.db.query(Turma).join(Turma.alunos).filter(
            Usuario.id == aluno_id
        ).offset(skip).limit(limit).all()

    def save(self, turma: Turma) -> Turma:
        self.db.add(turma)
        self.db.commit()
        self.db.refresh(turma)
        return turma

    def delete(self, turma: Turma) -> bool:
        self.db.delete(turma)
        self.db.commit()
        return True
