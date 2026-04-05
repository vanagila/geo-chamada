from sqlalchemy.orm import Session, joinedload
from typing import Optional, List
from app.models.Turma import Turma
from app.models.Usuario import Usuario
from app.schemas.turma import TurmaCreate, TurmaUpdate

class TurmaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, turma_data: TurmaCreate) -> Turma:
        db_turma = Turma(
            codigo=turma_data.codigo,
            disciplina_id=turma_data.disciplina_id,
            semestre=turma_data.semestre,
            ano=turma_data.ano,
            horario=turma_data.horario,
            data_inicio=turma_data.data_inicio,
            data_fim=turma_data.data_fim
        )

        self.db.add(db_turma)
        self.db.commit()
        self.db.refresh(db_turma)
        return db_turma

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Turma]:
        return self.db.query(Turma).options(
            joinedload(Turma.disciplina)
        ).offset(skip).limit(limit).all()

    def get_by_id(self, turma_id: int) -> Optional[Turma]:
        return self.db.query(Turma).options(
            joinedload(Turma.disciplina),
            joinedload(Turma.professores),
            joinedload(Turma.alunos)
        ).filter(Turma.id == turma_id).first()

    def get_by_codigo(self, codigo: str) -> Optional[Turma]:
        return self.db.query(Turma).filter(Turma.codigo = codigo).first()

    def get_by_professor(self, professor_id: int, skip: int = 0, limit: int = 100) -> List[Turma]:
        return self.db.query(Turma).join(Turma.professores).filter(
            Usuario.id == professor_id
        ).offset(skip).limit(limit).all()

    def get_by_aluno(self, aluno_id: int, skip: int = 0, limit: int = 100) -> List[Turma]:
        return self.db.query(Turma).join(Turma.alunos).filter(
            Usuario.id == aluno_id
        ).offset(skip).limit(limit).all()

    def update(self, turma_id: int, turma_data: TurmaUpdate) -> Optional[Turma]:
        turma = self.get_by_id(turma_id)
        if turma:
            update_data = turma_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                if hasattr(turma, field):
                    setattr(turma, field, value)
            self.db.commit()
            self.db.refresh(turma)
            return turma

    def delete(self, turma_id: int) -> bool:
        turma = self.get_by_id(turma_id)
        if turma:
            self.db.delete(turma)
            self.db.commit()
            return True
        return False

    def add_professor(self, turma_id: int, professor_id: int) -> Optional[Turma]:
        turma = self.get_by_id(turma_id)
        professor = self.db.query(Usuario).filter(
            Usuario.id == professor_id,
            Usuario.tipo == "PROFESSOR").first()

        if not turma or not professor:
            return None

        if professor not in turma.professores:
            turma.professores.append(professor)
            self.db.commit()
            self.db.refresh(turma)
        return turma

    def remove_professor(self, turma_id: int, professor_id: int) -> Optional[Turma]:
        turma = self.get_by_id(turma_id)
        professor = self.db.query(Usuario).filter(
            Usuario.id == professor_id).first()

        if not turma or not professor:
            return None

        if professor in turma.professores:
            turma.professores.remove(professor)
            self.db.commit()
            self.db.refresh(turma)
        return turma

    def add_aluno(self, turma_id: int, aluno_id: int) -> Optional[Turma]:
        turma = self.get_by_id(turma_id)
        aluno = self.db.query(Usuario).filter(
            Usuario.id == aluno_id,
            Usuario.tipo == "ALUNO").first()

        if not turma or not aluno:
            return None

        if aluno not in turma.alunos:
            turma.alunos.append(aluno)
            self.db.commit()
            self.db.refresh(turma)
        return turma

    def remove_professor(self, turma_id: int, aluno_id: int) -> Optional[Turma]:
        turma = self.get_by_id(turma_id)
        aluno = self.db.query(Usuario).filter(
            Usuario.id == aluno_id).first()

        if not turma or not aluno:
            return None

        if aluno in turma.alunos:
            turma.alunos.remove(aluno)
            self.db.commit()
            self.db.refresh(turma)
        return turma
