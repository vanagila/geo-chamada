from sqlalchemy.orm import Session
from typing import Optional, List
from fastapi import HTTPException, status
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse, UsuarioMessage
from app.schemas.msg import Msg
from app.models.Usuario import Usuario

class UsuarioService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = UsuarioRepository(db)

    def get_by_id(self, usuario_id: int) -> Usuario:
        usuario = self.repository.get_by_id(usuario_id)
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

    def get_by_matricula(self, matricula: str) -> Usuario:
        aluno = self.repository.get_by_matricula(matricula)
        if not aluno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aluno não encontrado"
            )
        return aluno

    def get_by_registro(self, registro: str) -> Usuario:
        professor = self.repository.get_by_registro(registro)
        if not professor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Professor não encontrado"
            )
        return professor

    def update_usuario(self, usuario_id: int, usuario_data: UsuarioUpdate) -> UsuarioMessage:
        usuario = self.repository.get_by_id(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        update_data = usuario_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(usuario, field, value)

        usuario_salvo = self.repository.save(usuario)
        return UsuarioMessage(
            message="Usuário atualizado com sucesso",
            usuario=usuario_salvo
        )

    def activate_usuario(self, usuario_id: int) -> UsuarioMessage:
        usuario = self.repository.get_by_id(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        usuario.ativo = True
        usuario_salvo = self.repository.save(usuario)
        return UsuarioMessage(
            message="Usuário ativado com sucesso",
            usuario=usuario_salvo
        )

    def deactivate_usuario(self, usuario_id: int) -> UsuarioMessage:
        usuario = self.repository.get_by_id(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        usuario.ativo = False
        usuario_salvo = self.repository.save(usuario)
        return UsuarioMessage(
            message="Usuário desativado com sucesso",
            usuario=usuario_salvo
        )

    def delete_usuario(self, usuario_id: int) -> Msg:
        usuario = self.repository.get_by_id(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        self.repository.delete(usuario)
        return Msg(message="Usuário deletado com sucesso")

    def verificar_permissao(self, usuario: Usuario, recurso: str, acao: str) -> bool:
        if usuario.tipo.value == "ADMIN":
            return True
        if usuario.tipo.value == "PROFESSOR":
            if recurso == "turma": return True
            if recurso == "chamada" and acao in ["abrir", "encerrar", "visualizar"]: return True
        if usuario.tipo.value == "ALUNO":
            if recurso == "presenca" and acao == "visualizar": return True
            if recurso == "chamada" and acao == "registrar": return True
        return False
