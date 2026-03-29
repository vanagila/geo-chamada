from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError
from typing import List, Optional
from app.core.database import get_db
from app.core.security import Security
from app.models.Usuario import Usuario
from app.schemas.usuario import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> Usuario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = Security.decode_token(token)
    if payload is None:
        raise credentials_exception

    try:
        subject = payload.get("sub")
        if subject is None:
            raise credentials_exception
        user_id = int(subject)
    except (ValueError, TypeError):
        raise credentials_exception

    user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user

async def get_current_active_user(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    if not current_user.ativo:
        raise HTTPException(
            status_code=400,
            detail="Usuário inativo"
        )
    return current_user

def verificar_perfil(perfis_permitidos: List[str]):
    async def role_checker(current_user: Usuario = Depends(get_current_user)):
        if current_user.tipo.value.upper() not in [p.upper() for p in perfis_permitidos]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operação permitida apenas para {','.join(perfis_permitidos)}"
            )
        return current_user
    return role_checker

async def get_current_user_optional(
        db: Session = Depends(get_db),
        token: Optional[str] = Depends(oauth2_scheme)
) -> Optional[Usuario]:
    if  not token:
        return None

    try:
        payload = Security.decode_token(token)
        if payload:
            subject = payload.get("sub")
            if subject:
                user_id = int(subject)
                return db.query(Usuario).filter(Usuario.id == user_id).first()
    except (ValueError, TypeError):
        raise credentials_exception

    return None
