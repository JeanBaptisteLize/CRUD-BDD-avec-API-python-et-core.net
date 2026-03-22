from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app import models, schemas
from app.deps import get_current_user


router = APIRouter(prefix="/resultats", tags=["Résultats"], dependencies=[Depends(get_current_user)])
    
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

@router.post("/", status_code=201)
def create_resultat(payload: schemas.ResultatIn, db: Session = Depends(get_db)):
    obj = models.Resultat(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return {"message": "Résultat créé avec succès!", "resultat": obj}

@router.put("/{id_resultat}")
def update_resultat(id_resultat: int, payload: schemas.ResultatIn, db: Session = Depends(get_db)):
    obj = db.get(models.Resultat, id_resultat)
    if not obj:
        raise HTTPException(status_code=404, detail="Résultat non trouvé")
    for k, v in payload.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return {"message": "Résultat mis à jour avec succès!", "resultat": obj}

@router.delete("/{id_resultat}", status_code=200)
def delete_resultat(id_resultat: int, db: Session = Depends(get_db)):
    obj = db.get(models.Resultat, id_resultat)
    if not obj:
        raise HTTPException(status_code=404, detail="Résultat non trouvé")
    db.delete(obj)
    db.commit()
    return {"message": "Résultat supprimé avec succès!"}