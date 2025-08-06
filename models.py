# models.py
from pydantic import BaseModel
from typing import List, Optional

class MaterialBase(BaseModel):
    title: str
    description: str
    categories: List[str]
    file_url: str
    preview_url: Optional[str] = None
    telegram_post_id: Optional[int] = None  # ✅ YANGI MAYDON

class MaterialCreate(MaterialBase):
    pass

class MaterialUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    categories: Optional[List[str]] = None
    file_url: Optional[str] = None
    preview_url: Optional[str] = None
    telegram_post_id: Optional[int] = None  # ✅ PATCH uchun ham

class Material(MaterialBase):
    id: int

    class Config:
        orm_mode = True
