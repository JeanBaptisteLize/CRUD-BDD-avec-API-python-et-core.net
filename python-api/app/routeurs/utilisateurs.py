from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app import models, schemas
from app.deps import get_current_user

router = APIRouter(prefix="/utilisateurs", tags=["Utilisateurs"])

# -------------------------------------------------------
# CRUD : Utilisateurs
# -------------------------------------------------------
@router.get("/")
def list_utilisateurs(db: Session = Depends(get_db)):
    return db.query(models.Utilisateur).all()

@router.post("/")
def create_utilisateur(payload: schemas.UtilisateurIn, db: Session = Depends(get_db)):
    created_user = models.Utilisateur(**payload.model_dump())
    db.add(created_user)
    db.commit()
    db.refresh(created_user)
    return created_user

@router.get("/{id_utilisateur}")
def get_utilisateur(id_utilisateur: int, db: Session = Depends(get_db)):
    user = db.get(models.Utilisateur, id_utilisateur)   # recupere l'utilisateur par son id (PK)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user

@router.put("/{id_utilisateur}")
def update_utilisateur(id_utilisateur: int, payload: schemas.UtilisateurIn, db: Session = Depends(get_db)):
    user = db.get(models.Utilisateur, id_utilisateur)
    for k, v in payload.model_dump().items():
        setattr(user, k, v)
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{id_utilisateur}", status_code=204)
def delete_utilisateur(id_utilisateur: int, db: Session = Depends(get_db)):
    user = db.get(models.Utilisateur, id_utilisateur)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    db.delete(user)
    db.commit()
    return {"message": "Utilisateur supprimé avec succès!"}

