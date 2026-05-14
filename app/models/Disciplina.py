from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Disciplina(Base):
    __tablename__ = "disciplinas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    codigo = Column(String(20), unique=True, nullable=False)
    descricao = Column(String(500), nullable=True)
    carga_horaria = Column(Integer, nullable=False, default=60)

    turmas = relationship("Turma", back_populates="disciplina")
