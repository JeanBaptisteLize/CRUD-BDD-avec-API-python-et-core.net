from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app import models, schemas


router = APIRouter(prefix="/modules", tags=["Modules"])
    
# -------------------------------------------------------
# CRUD : Modules
# -------------------------------------------------------
@router.get("/")
def list_modules(db: Session = Depends(get_db)):
    return db.query(models.Module).all()

@router.get("/{id_module}")
def get_module(id_module: int, db: Session = Depends(get_db)):
    obj = db.get(models.Module, id_module)
    if not obj:
        raise HTTPException(status_code=404, detail="Module non trouvé")
    return obj

@router.post("/")
def create_module(payload: schemas.ModuleIn, db: Session = Depends(get_db)):
    obj = models.Module(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.put("/{id_module}")
def update_module(id_module: int, payload: schemas.ModuleIn, db: Session = Depends(get_db)):
    obj = db.get(models.Module, id_module)
    for k, v in payload.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{id_module}")
def delete_module(id_module: int, db: Session = Depends(get_db)):
    obj = db.get(models.Module, id_module)
    if not obj:
        raise HTTPException(status_code=404, detail="Module non trouvé")
    db.delete(obj)
    db.commit()
    return {"message": "Module supprimé avec succès!"}