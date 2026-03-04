from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app import models, schemas


router = APIRouter(prefix="/resultats", tags=["Résultats"])
    
# -------------------------------------------------------
# CRUD : Résultats
# -------------------------------------------------------
@router.get("/")
def list_resultats(db: Session = Depends(get_db)):
    return db.query(models.Resultat).all()

@router.get("/{id_resultat}")
def get_resultat(id_resultat: int, db: Session = Depends(get_db)):
    obj = db.get(models.Resultat, id_resultat)
    if not obj:
        raise HTTPException(status_code=404, detail="Résultat non trouvé")
    return obj

@router.post("/")
def create_resultat(payload: schemas.ResultatIn, db: Session = Depends(get_db)):
    obj = models.Resultat(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.put("/{id_resultat}")
def update_resultat(id_resultat: int, payload: schemas.ResultatIn, db: Session = Depends(get_db)):
    obj = db.get(models.Resultat, id_resultat)
    for k, v in payload.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{id_resultat}")
def delete_resultat(id_resultat: int, db: Session = Depends(get_db)):
    obj = db.get(models.Resultat, id_resultat)
    if not obj:
        raise HTTPException(status_code=404, detail="Résultat non trouvé")
    db.delete(obj)
    db.commit()
    return {"message": "Résultat supprimé avec succès!"}