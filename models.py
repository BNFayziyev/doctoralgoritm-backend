from pydantic import BaseModel
from typing import List, Optional

class Material(BaseModel):
    title: str
    description: str
    categories: List[str]
    file_url: str
    preview_url: Optional[str] = None

