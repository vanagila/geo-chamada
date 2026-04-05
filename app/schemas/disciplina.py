from pydantic import BaseModel, Field
from typing import Optional, List

class DisciplinaBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100)
    codigo: str = Field(..., max_length=20)
    descricao: Optional[str] = Field(None, max_length=500)

class DisciplinaCreate(DisciplinaBase):
    pass

class DisciplinaUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None

class DisciplinaResponse(DisciplinaBase):
    id: int
    turmas_count: Optional[int] = 0 

    class Config:
        from_attributes = True
