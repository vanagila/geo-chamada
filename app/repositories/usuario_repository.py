from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from app.models.Usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate

class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, usuario_data: UsuarioCreate, senha_hash: str) -> Usuario:
        db_usuario = Usuario(
            nome=usuario_data.nome,
            email=usuario_data.email,
            senha_hash=senha_hash,
            tipo=usuario_data.tipo,
            matricula=usuario_data.matricula,
            registro_professor=usuario_data.registro_professor
        )

        self.db.add(db_usuario)
        self.db.commit()
        self.db.refresh(db_usuario)
        return db_usuario

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

    def update(self, usuario_id: int, usuario_data: UsuarioUpdate) -> Optional[Usuario]:
        usuario = self.get_by_id(usuario_id)
        if not usuario:
            return None
        
        update_data = usuario_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(usuario, field):
                setattr(usuario, field, value)

        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def update_ultimo_acesso(self, usuario_id: int) -> Optional[Usuario]:
        usuario = self.get_by_id(usuario_id)
        if usuario:
            usuario.ultimo_acesso = datetime.utcnow()
            self.db.commit()
            self.db.refresh(usuario)
        return usuario

    def activate(self, usuario_id: int) -> Optional[Usuario]:
        usuario = self.get_by_id(usuario_id)
        if usuario:
            usuario.ativo = True
            self.db.commit()
            self.db.refresh(usuario)
        return usuario

    def deactivate(self, usuario_id: int) -> Optional[Usuario]:
        usuario = self.get_by_id(usuario_id)
        if usuario:
            usuario.ativo = False
            self.db.commit()
            self.db.refresh(usuario)
        return usuario

    def delete(self, usuario_id: int) -> bool:
        usuario = self.get_by_id(usuario_id)
        if usuario:
            self.db.delete(usuario)
            self.db.commit()
            return True
        return False
