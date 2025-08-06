from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Material
from database import get_db_connection, init_db
import json

app = FastAPI()

origins = ["*"]  # Frontend uchun CORS ochiq
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/materials")
def get_materials():
    conn = get_db_connection()
    materials = conn.execute("SELECT * FROM materials").fetchall()
    conn.close()

    return [
        {
            "id": row["id"],
            "title": row["title"],
            "description": row["description"],
            "categories": json.loads(row["categories"]),
            "file_url": row["file_url"],
            "preview_url": row["preview_url"]
        }
        for row in materials
    ]

@app.post("/materials")
def add_material(material: Material):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO materials (title, description, categories, file_url, preview_url)
        VALUES (?, ?, ?, ?, ?)
    """, (
        material.title,
        material.description,
        json.dumps(material.categories),
        material.file_url,
        material.preview_url
    ))
    conn.commit()
    conn.close()
    return {"message": "Material added successfully"}

