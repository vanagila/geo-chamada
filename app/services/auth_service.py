from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
from app.repositories.auth_repository import AuthRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.usuario import UsuarioCreate
from app.schemas.auth import Token
from app.models.Usuario import Usuario
from app.core.security import Security

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = AuthRepository(db)
        self.usuario_repo = UsuarioRepository(db)

    def criar_usuario(self, user_data: UsuarioCreate) -> Usuario:
        if self.usuario_repo.get_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado"
            )

        if user_data.tipo == "ALUNO" and not user_data.matricula:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Aluno deve ter matrícula"
            )

        if user_data.tipo == "PROFESSOR" and not user_data.registro_professor:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Professor deve ter registro"
            )

        senha_hash = Security.get_senha_hash(user_data.senha)
        novo_usuario = Usuario(
            nome=user_data.nome,
            email=user_data.email,
            senha_hash=senha_hash,
            tipo=user_data.tipo,
            matricula=user_data.matricula,
            registro_professor=user_data.registro_professor
        )
        return self.repository.save(novo_usuario)

    def authenticate_usuario(self, email: str, senha: str) -> Usuario:
        usuario = self.usuario_repo.get_by_email(email)

        if not usuario or not Security.verificar_senha(senha, usuario.senha_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos"
            )

        if not usuario.ativo:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuário inativo"
            )

        usuario.ultimo_acesso = datetime.utcnow()
        self.usuario_repo.save(usuario)
        return usuario

    def generate_token(self, usuario: Usuario) -> Token:
        access_token = Security.criar_access_token(
            data={
                "sub": str(usuario.id),
                "email": usuario.email,
                "tipo": usuario.tipo.value
            }
        )
        return Token(
            access_token=access_token, token_type="bearer"
        )
