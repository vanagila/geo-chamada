from sqlalchemy.orm import Session
from app.models.Usuario import Usuario

class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, usuario: Usuario) -> Usuario:
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def delete(self, usuario: Usuario) -> Usuario:
        self.db.delete(usuario)
        self.db.commit()
        return true
