from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from .config import settings

pwd_context = CryptContext(schemas=["bcrypt"], deprecated="auto")

class Security:
    @staticmethod
    def verificar_senha(senha_simples: str, senha_hashed: str) -> bool:
        return pwd_context.verify(senha_simples, senha_hashed)

    @staticmethod
    def get_senha_hash(senha: str) -> bool:
        return pwd_context.hash(senha)

    @staticmethod
    def criar_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutos=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    @staticmethod
    def decode_token(token: str):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return payload
        except JWTError:
            return None
