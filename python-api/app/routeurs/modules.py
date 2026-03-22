from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app import models, schemas
from app.deps import get_current_user


router = APIRouter(prefix="/modules", tags=["Modules"], dependencies=[Depends(get_current_user)])
    
# -------------------------------------------------------
# CRUD : Modules
# -------------------------------------------------------
@router.get("/")
def list_modules(db: Session = Depends(get_db)):
    return db.query(models.ModuleFormation).all()

@router.get("/{id_module}")
def get_module(id_module: int, db: Session = Depends(get_db)):
    obj = db.get(models.ModuleFormation, id_module)
    if not obj:
        raise HTTPException(status_code=404, detail="Module non trouvé")
    return obj

@router.post("/", status_code=201)
def create_module(payload: schemas.ModuleIn, db: Session = Depends(get_db)):
    obj = models.ModuleFormation(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return {"message": "Module créé avec succès!", "module": obj}

@router.put("/{id_module}")
def update_module(id_module: int, payload: schemas.ModuleIn, db: Session = Depends(get_db)):
    obj = db.get(models.ModuleFormation, id_module)
    if not obj:
        raise HTTPException(status_code=404, detail="Module non trouvé")
    for k, v in payload.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return {"message": "Module mis à jour avec succès!", "module": obj}

@router.delete("/{id_module}", status_code=200)
def delete_module(id_module: int, db: Session = Depends(get_db)):
    obj = db.get(models.ModuleFormation, id_module)
    if not obj:
        raise HTTPException(status_code=404, detail="Module non trouvé")
    db.delete(obj)
    db.commit()
    return {"message": "Module supprimé avec succès!"}