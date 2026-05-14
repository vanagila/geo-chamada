from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from app.models.Usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate

class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, usuario: Usuario) -> Usuario:
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def get_by_id(self, usuario_id: int) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.id == usuario_id).first()

    def get_by_email(self, email: str) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.email == email).first()

    def get_by_matricula(self, matricula: str) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.matricula == matricula).first()

    def get_by_registro(self, registro: str) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.registro_professor == registro).first()

    def get_by_tipo(self, tipo: str, skip: int = 0, limit: int = 100) -> List[Usuario]:
        return self.db.query(Usuario).filter(Usuario.tipo == tipo).offset(skip).limit(limit).all()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Usuario]:
        return self.db.query(Usuario).offset(skip).limit(limit).all()

    def delete(self, usuario: Usuario) -> bool:
        self.db.delete(usuario)
        self.db.commit()
        return True
