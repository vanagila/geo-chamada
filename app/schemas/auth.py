from pydantic import BaseModel
from typing import Optional
from app.schemas.usuario import UserType

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None
    tipo: Optional[UserType] = None
