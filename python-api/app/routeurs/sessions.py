from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app import models, schemas
from app.deps import get_current_user


router = APIRouter(prefix="/sessions", tags=["Sessions"], dependencies=[Depends(get_current_user)])
    
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

@router.post("/", status_code=201)
def create_session(payload: schemas.SessionIn, db: Session = Depends(get_db)):
    obj = models.SessionFormation(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return {"message": "Session créée avec succès!", "session": obj}

@router.put("/{id_session}")
def update_session(id_session: int, payload: schemas.SessionIn, db: Session = Depends(get_db)):
    obj = db.get(models.SessionFormation, id_session)
    if not obj:
        raise HTTPException(status_code=404, detail="Session non trouvée")
    for k, v in payload.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return {"message": "Session mise à jour avec succès!", "session": obj}

@router.delete("/{id_session}", status_code=200)
def delete_session(id_session: int, db: Session = Depends(get_db)):
    obj = db.get(models.SessionFormation, id_session)
    if not obj:
        raise HTTPException(status_code=404, detail="Session de formation non trouvée")
    db.delete(obj)
    db.commit()
    return {"message": "Session de formation supprimée avec succès!"}