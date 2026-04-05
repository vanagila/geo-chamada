from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Any, Optional
from app.core.database import get_db
from app.models.Usuario import Usuario, UserType
from app.schemas.usuario import UsuarioResponse, UsuarioUpdate, UsuarioMessage
from app.schemas.msg import Msg
from app.services.usuario_service import UsuarioService
from app.api.deps import get_current_active_user, verificar_perfil

router = APIRouter()

@router.get("/me", response_model=UsuarioResponse)
def get_me(current_user: Usuario = Depends(get_current_active_user)) -> Any:
    return current_user

@router.put("/me", response_model=UsuarioMessage)
def update_me(
    *, db: Session = Depends(get_db), usuario_data: UsuarioUpdate,
    current_user: Usuario = Depends(get_current_active_user)
) -> Any:
    service = UsuarioService(db)
    usuario = service.update_user(current_user.id, usuario_data)
    return usuario

@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios(*, db: Session = Depends(get_db),
                    tipo: Optional[UserType] = None, 
                    skip: int = 0, limit: int = 100,
                    current_user: Usuario = Depends(verificar_perfil(["ADMIN"]))
) -> Any:
    service = UsuarioService(db)
    if tipo:
        usuarios = service.get_by_type(tipo.value, skip, limit)
    else:
        usuarios = service.get_all_users(skip, limit)

    return usuarios

@router.get("/{usuario_id}", response_model=UsuarioResponse)
def get_usuario(*, db: Session = Depends(get_db), usuario_id: int,
                current_user: Usuario = Depends(verificar_perfil(["ADMIN"]))
) -> Any:
    service = UsuarioService(db)
    usuario = service.get_user_by_id(usuario_id)
    return usuario

@router.put("/{usuario_id}", response_model=UsuarioMessage)
def update_usuario(
    *, db: Session = Depends(get_db),
    usuario_id: int, usuario_data: UsuarioUpdate,
    current_user: Usuario = Depends(verificar_perfil(["ADMIN"]))
) -> Any:
    service = UsuarioService(db)
    usuario = service.update_user(usuario_id, usuario_data)
    return usuario

@router.post("/{usuario_id}/activate", response_model=UsuarioMessage)
def activate_usuario(*, db: Session = Depends(get_db), usuario_id: int,
                     current_user: Usuario = Depends(verificar_perfil(["ADMIN"]))
) -> Any:
    service = UsuarioService(db)
    usuario = service.activate_user(usuario_id)
    return usuario

@router.post("/{usuario_id}/deactivate", response_model=UsuarioMessage)
def deactivate_usuario(*, db: Session = Depends(get_db), usuario_id: int,
                       current_user: Usuario = Depends(verificar_perfil(["ADMIN"]))
) -> Any:
    service = UsuarioService(db)
    usuario = service.deactivate_user(usuario_id)
    return usuario

@router.delete("/{usuario_id}", response_model=Msg)
def delete_usuario(*, db: Session = Depends(get_db), usuario_id: int,
                   current_user: Usuario = Depends(verificar_perfil(["ADMIN"]))
) -> Any:
    service = UsuarioService(db)
    return service.delete_user(usuario_id)
