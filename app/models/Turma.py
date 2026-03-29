from sqlalchemy import Column, Integer, String, ForeignKey, Table, Date, Time
from sqlalchemy.orm import relationship
from app.core.database import Base

turma_professor = Table(
    "turma_professor",
    Base.metadata,
    Column("turma_id", Integer, ForeignKey("turmas.id")),
    Column("professor_id", Integer, ForeignKey("usuarios.id"))
)

turma_aluno = Table(
    "turma_aluno",
    Base.metadata,
    Column("turma_id", Integer, ForeignKey("turmas.id")),
    Column("aluno_id", Integer, ForeignKey("usuarios.id"))
)

class Turma(Base):
    __tablename__ = "turmas"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(20), unique=True, nullable=False)
    disciplina_id = Column(Integer, ForeignKey("disciplinas.id"))
    semestre = Column(String(6), nullable=False)
    ano = Column(Integer, nullable=False)
    horario = Column(Time, nullable=False)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date, nullable=False)

    disciplina = relationship("Disciplina", back_populates="turmas")
    professores = relationship("Usuario", secondary=turma_professor)
    alunos = relationship("Usuario", secondary=turma_aluno)
    chamadas = relationship("Chamada", back_populates="turma")
