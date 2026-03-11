from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app import models, schemas


router = APIRouter(prefix="/sessions", tags=["Sessions"])
    
# -------------------------------------------------------
# CRUD : Sessions
# -------------------------------------------------------
@router.get("/")
def list_sessions(db: Session = Depends(get_db)):
    return db.query(models.SessionFormation).all()

@router.get("/{id_session}")
def get_session(id_session: int, db: Session = Depends(get_db)):
    obj = db.get(models.SessionFormation, id_session)
    if not obj:
        raise HTTPException(status_code=404, detail="Session non trouvée")
    return obj

@router.post("/")
def create_session(payload: schemas.SessionIn, db: Session = Depends(get_db)):
    obj = models.SessionFormation(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.put("/{id_session}")
def update_session(id_session: int, payload: schemas.SessionIn, db: Session = Depends(get_db)):
    obj = db.get(models.SessionFormation, id_session)
    for k, v in payload.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{id_session}")
def delete_session(id_session: int, db: Session = Depends(get_db)):
    obj = db.get(models.SessionFormation, id_session)
    if not obj:
        raise HTTPException(status_code=404, detail="Session de formation non trouvée")
    db.delete(obj)
    db.commit()
    return {"message": "Session de formationsupprimée avec succès!"}