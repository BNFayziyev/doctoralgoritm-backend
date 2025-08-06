# database.py
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.types import JSON
from database_setup import Base

class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    categories = Column(JSON)
    file_url = Column(String)
    preview_url = Column(String, nullable=True)
    telegram_post_id = Column(Integer, nullable=True, index=True)  # ✅ YANGI USTUN
