from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app import models, schemas


router = APIRouter(prefix="/inscriptions", tags=["Inscriptions"])
    
# -------------------------------------------------------
# CRUD : Inscriptions
# -------------------------------------------------------
@router.get("/")
def list_inscriptions(db: Session = Depends(get_db)):
    return db.query(models.Inscription).all()

@router.get("/{id_inscription}")
def get_inscription(id_inscription: int, db: Session = Depends(get_db)):
    obj = db.get(models.Inscription, id_inscription)
    if not obj:
        raise HTTPException(status_code=404, detail="Inscription non trouvée")
    return obj

@router.post("/")
def create_inscription(payload: schemas.InscriptionIn, db: Session = Depends(get_db)):
    obj = models.Inscription(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.put("/{id_inscription}")
def update_inscription(id_inscription: int, payload: schemas.InscriptionIn, db: Session = Depends(get_db)):
    obj = db.get(models.Inscription, id_inscription)
    for k, v in payload.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{id_inscription}")
def delete_inscription(id_inscription: int, db: Session = Depends(get_db)):
    obj = db.get(models.Inscription, id_inscription)
    if not obj:
        raise HTTPException(status_code=404, detail="Inscription non trouvée")
    db.delete(obj)
    db.commit()
    return {"message": "Inscription supprimée avec succès!"}