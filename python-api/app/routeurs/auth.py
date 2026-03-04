from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas import UtilisateurIn
from app.models import Utilisateur
from app.security import hash_password, verify_password, create_access_token


router = APIRouter(prefix="/auth", tags=["Authentification"])

# -------------------------------------------------------
# Authentification (JWT + hashing de mot de passe)
# -------------------------------------------------------

@router.post("/register")  # email + mdp -> hash du mdp en DB
def register_user(user: UtilisateurIn, db: Session = Depends(get_db)):

    # Vérifier si l'utilisateur existe déjà
    existing_user = db.query(Utilisateur).filter(Utilisateur.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email déjà utilisé!")
    
    # Vérifier si le mdp est trop long
    if len(user.password) > 128:
        raise HTTPException(status_code=400, detail="Mot de passe trop long! (max 128 caractères)")
    
    # Hash du mot de passe
    hashed = hash_password(user.password)

    # Création du nouvel utilisateur avec le hash du mot de passe
    new_user = Utilisateur(
        nom=user.nom,
        prenom=user.prenom,
        email=user.email,
        password=hashed
    )

    # Ajout du nouvel utilisateur à la base de données
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



# @router.post("/login") # email + mdp -> token JWT

# @router.get("/me") # token JWT -> infos de l'utilisateur connecté
