from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base

class UserType(str, enum.Enum):
    ALUNO = "ALUNO"
    PROFESSOR = "PROFESSOR"
    ADMIN = "ADMIN"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    senha_hash = Column(String(200), nullable=False)
    tipo = Column(Enum(UserType), nullable=False)
    matricula = Column(String(20), unique=True, nullable=True)
    registro_professor = Column(String(20), unique=True, nullable=True)
    ativo = Column(Boolean, default=True)
    data_cadastro = Column(DateTime, default=datetime.utcnow)
    ultimo_acesso = Column(DateTime, nullable=True)

    presencas = relationship("Presenca", back_populates="aluno", foreign_keys="Presenca.aluno_id")
    chamadas_abertas = relationship("Chamada", back_populates="professor")
    faltas_abonadas = relationship("Presenca", back_populates="abonado_por", foreign_keys="Presenca.abonado_por_id")
