from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from geoalchemy2 import Geography
from datetime import datetime
import enum
from app.core.database import Base

class PresencaStatus(str, enum.Enum):
    PRESENTE = "PRESENTE"
    AUSENTE = "AUSENTE"
    ABONADA = "ABONADA"

class Presenca(Base):
    __tablename__ = "presencas"
    __table_args__ = (
        UniqueConstraint("aluno_id", "chamada_id", name="unique_aluno_chamada"),
    )

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("usuarios.id"))
    chamada_id = Column(Integer, ForeignKey("chamadas.id"))
    coordenadas_aluno = Column(Geography(geometry_type="POINT", srid=4326))
    distancia_calculada = Column(Float)
    data_registro = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(PresencaStatus), default=PresencaStatus.AUSENTE)
    abonado_por_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    data_abono = Column(DateTime, nullable=True)
    motivo_abono = Column(String(200), nullable=True)

    aluno = relationship("Usuario", back_populates="presencas", foreign_keys=[aluno_id])
    chamada = relationship("Chamada", back_populates="presencas")
    abonado_por = relationship("Usuario", back_populates="chamadas_abonadas", foreign_keys=[abonado_por_id])
