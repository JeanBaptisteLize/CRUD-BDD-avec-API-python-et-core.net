from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app import models, schemas
from app.deps import get_current_user


router = APIRouter(prefix="/inscriptions", tags=["Inscriptions"], dependencies=[Depends(get_current_user)])
    
# -------------------------------------------------------
# CRUD : Inscriptions
# -------------------------------------------------------
@router.get("/")
def list_inscriptions(db: Session = Depends(get_db)):
    return db.query(models.Sinscrire).all()

@router.get("/{id_inscription}")
def get_inscription(id_inscription: int, db: Session = Depends(get_db)):
    obj = db.get(models.Sinscrire, id_inscription)
    if not obj:
        raise HTTPException(status_code=404, detail="Inscription non trouvée")
    return obj

@router.post("/", status_code=201)
def create_inscription(payload: schemas.InscriptionIn, db: Session = Depends(get_db)):
    obj = models.Sinscrire(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return {"message": "Inscription créée avec succès!", "inscription": obj}

@router.put("/{id_inscription}")
def update_inscription(id_inscription: int, payload: schemas.InscriptionIn, db: Session = Depends(get_db)):
    obj = db.get(models.Sinscrire, id_inscription)
    if not obj:
        raise HTTPException(status_code=404, detail="Inscription non trouvée")
    for k, v in payload.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return {"message": "Inscription mise à jour avec succès!", "inscription": obj}

@router.delete("/{id_inscription}", status_code=200)
def delete_inscription(id_inscription: int, db: Session = Depends(get_db)):
    obj = db.get(models.Sinscrire, id_inscription)
    if not obj:
        raise HTTPException(status_code=404, detail="Inscription non trouvée")
    db.delete(obj)
    db.commit()
    return {"message": "Inscription supprimée avec succès!"}