# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database_setup import engine, SessionLocal
from database import Base, Material as DBMaterial
from models import Material, MaterialCreate, MaterialUpdate
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

app = FastAPI()
Base.metadata.create_all(bind=engine)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ GET /materials?telegram_post_id=...
@app.get("/materials", response_model=List[Material])
def get_materials(telegram_post_id: Optional[int] = None, db: Session = Depends(get_db)):
    if telegram_post_id:
        return db.query(DBMaterial).filter(DBMaterial.telegram_post_id == telegram_post_id).all()
    return db.query(DBMaterial).all()

@app.post("/materials", response_model=Material)
def create_material(material: MaterialCreate, db: Session = Depends(get_db)):
    db_material = DBMaterial(**material.dict())
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material

@app.patch("/materials/{material_id}", response_model=Material)
def update_material(material_id: int, updates: MaterialUpdate, db: Session = Depends(get_db)):
    db_material = db.query(DBMaterial).filter(DBMaterial.id == material_id).first()
    if not db_material:
        raise HTTPException(status_code=404, detail="Material not found")

    update_data = updates.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_material, key, value)

    db.commit()
    db.refresh(db_material)
    return db_material
