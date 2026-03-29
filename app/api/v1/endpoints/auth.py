from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Any
from app.core.database import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, Token
from app.services.auth_service import AuthService

router = APIRouter()

@router.post("/register", response_model=UsuarioResponse, status_code=201)
def register(*, db: Session = Depends(get_db), user_data: UsuarioCreate) -> Any:
    auth_service = AuthService(db)
    usuario = auth_service.register_user(user_data)

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar usuário"
        )
        
    return usuario

@router.post("/login", response_model=Token)
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    auth_service = AuthService(db)
    usuario = auth_service.authenticate_user(
        email=form_data.username,
        senha=form_data.password
    )

    token_data = auth_service.generate_token(usuario)
    return {
        "access_token": token_data["access_token"],
        "token_type": token_data["token_type"]
    }
