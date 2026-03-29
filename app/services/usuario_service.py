from sqlalchemy.orm import Session
from typing import Optional, List
from fastapi import HTTPException, status
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from app.models.Usuario import Usuario

class UsuarioService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = UsuarioRepository(db)

    def get_user_by_id(self, usuario_id: int) -> Usuario:
        usuario = self.repository.get_by_id(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        return usuario

    def get_user_by_email(self, email: str) -> Usuario:
        usuario = self.repository.get_by_email(email)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        return usuario

    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[Usuario]:
        return self.repository.get_all(skip, limit)

    def get_by_type(self, tipo: str, skip: int = 0, limit: int = 100) -> List[Usuario]:
        return self.repository.get_by_tipo(tipo, skip, limit)

    def update_user(self, usuario_id: int, usuario_data: UsuarioUpdate) -> dict:
        usuario = self.repository.update(usuario_id, usuario_data)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        return {
            "message": "Usuário atualizado com sucesso",
            "usuario": usuario
        }

    def activate_user(self, usuario_id: int) -> dict:
        usuario = self.repository.activate(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        return {
            "message": "Usuário ativado com sucesso",
            "usuario": usuario
        }

    def deactivate_user(self, usuario_id: int) -> dict:
        usuario = self.repository.deactivate(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        return {
            "message": "Usuário desativado com sucesso",
            "usuario": usuario
        }
    
    def delete_user(self, usuario_id: int) -> dict:
        if self.repository.delete(usuario_id):
            return {"message": "Usuário deletado com sucesso"}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    def verificar_permissao(self, usuario: Usuario, recurso: str, acao: str) -> bool:
        if usuario.tipo.value == "ADMIN":
            return True

        if usuario.tipo.value == "PROFESSOR":
            if recurso == "turma":
                return True
            if recurso == "chamada" and acao in ["abrir", "encerrar", "visualizar"]:
                return True
        
        if usuario.tipo.value == "ALUNO":
            if recurso == "presenca" and acao == "visualizar":
                return True
            if recurso == "chamada" and acao == "registrar":
                return True
        
        return False

    def format_user_response(self, usuario: Usuario) -> UsuarioResponse:
        return UsuarioResponse(
            id=usuario.id,
            nome=usuario.nome,
            email=usuario.email,
            tipo=usuario.tipo,
            matricula=usuario.matricula,
            registro_professor=usuario.registro_professor,
            ativo=usuario.ativo,
            data_cadastro=usuario.data_cadastro,
            ultimo_acesso=usuario.ultimo_acesso
        )
