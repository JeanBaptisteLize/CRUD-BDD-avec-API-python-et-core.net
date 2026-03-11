
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app import models, schemas


router = APIRouter(prefix="/formations", tags=["Formations"])
    
# -------------------------------------------------------
# CRUD : Formations
# -------------------------------------------------------
@router.get("/")
def list_formations(db: Session = Depends(get_db)):
    return db.query(models.Formation).all()

@router.post("/")
def create_formation(payload: schemas.FormationIn, db: Session = Depends(get_db)):
    obj = models.Formation(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/{id_formation}")
def get_formation(id_formation: int, db: Session = Depends(get_db)):
    obj = db.get(models.Formation, id_formation)
    if not obj:
        raise HTTPException(status_code=404, detail="Formation non trouvée")
    return obj

@router.put("/{id_formation}")
def update_formation(id_formation: int, payload: schemas.FormationIn, db: Session = Depends(get_db)):
    obj = db.get(models.Formation, id_formation)
    for k, v in payload.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{id_formation}")
def delete_formation(id_formation: int, db: Session = Depends(get_db)):
    obj = db.get(models.Formation, id_formation)
    if not obj:
        raise HTTPException(status_code=404, detail="Formation non trouvée")
    db.delete(obj)
    db.commit()
    return {"message": "Formation supprimée avec succès!"}