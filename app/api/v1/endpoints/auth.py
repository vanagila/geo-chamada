from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Any
from app.core.database import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.schemas.auth import Token
from app.services.auth_service import AuthService

router = APIRouter()

@router.post("/register", response_model=UsuarioResponse)
def register(*, db: Session = Depends(get_db), user_data: UsuarioCreate) -> UsuarioResponse:
    service = AuthService(db)
    return service.criar_usuario(user_data)

@router.post("/login", response_model=Token)
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    service = AuthService(db)
    usuario = service.authenticate_usuario(
        email=form_data.username,
        senha=form_data.password
    )
    return service.generate_token(usuario)
