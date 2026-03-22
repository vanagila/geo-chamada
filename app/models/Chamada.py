from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float, Enum
from sqlalchemy.orm import relationship
from geoalchemy2 import Geography
from datetime import datetime
import enum
from app.core.database import Base

class ChamadaStatus(str, enum.Enum):
    ABERTA = "ABERTA"
    ENCERRADA = "ENCERRADA"

class Chamada(Base):
    __tablename__ = "chamadas"

    id = Column(Integer, primary_key=True, index=True)
    turma_id = Column(Integer, ForeignKey("turmas.id"))
    professor_id = Column(Integer, ForeignKey("usuarios.id"))
    coordenadas_professor = Column(Geography(geometry_type="POINT", srid=4326))
    raio = Column(Float, nullable=False)
    data_abertura = Column(DateTime, default=datetime.utcnow)
    data_encerramento = Column(DateTime, nullable=True)
    status = Column(Enum(ChamadaStatus), default=ChamadaStatus.ABERTA)

    turma = relationship("Turma", back_populates="chamadas")
    professor = relationship("Usuario", back_populates="chamadas_abertas")
    presencas = relationship("Presenca", back_populates="chamadas")
