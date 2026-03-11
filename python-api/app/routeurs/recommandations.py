from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app import models, schemas


router = APIRouter(prefix="/recommandations", tags=["Recommandations"])
    
# -------------------------------------------------------
# CRUD : Recommandations
# -------------------------------------------------------
@router.get("/")
def list_recommandations(db: Session = Depends(get_db)):
    return db.query(models.Recommendation).all()

@router.get("/{id_recommandation}")
def get_recommandation(id_recommandation: int, db: Session = Depends(get_db)):
    obj = db.get(models.Recommendation, id_recommandation)
    if not obj:
        raise HTTPException(status_code=404, detail="Recommandation non trouvée")
    return obj

@router.post("/")
def create_recommandation(payload: schemas.RecommendationIn, db: Session = Depends(get_db)):
    obj = models.Recommendation(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.put("/{id_recommandation}")
def update_recommandation(id_recommandation: int, payload: schemas.RecommendationIn, db: Session = Depends(get_db)):
    obj = db.get(models.Recommendation, id_recommandation)
    if not obj:
        raise HTTPException(status_code=404, detail="Recommandation non trouvée")
    for k, v in payload.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{id_recommandation}")
def delete_recommandation(id_recommandation: int, db: Session = Depends(get_db)):
    obj = db.get(models.Recommendation, id_recommandation)
    if not obj:
        raise HTTPException(status_code=404, detail="Recommandation non trouvée")
    db.delete(obj)
    db.commit() 
    return {"message": "Recommandation supprimée avec succès!"}