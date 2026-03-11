from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas import UtilisateurIn, LoginLDAP, LoginLocal
from app.models import Utilisateur
from app.security import hash_password, create_access_token, verify_password
from app.services.ldap_auth import auth_ldap
import bcrypt


router = APIRouter(prefix="/auth", tags=["Authentification"])

# -------------------------------------------------------
# Authentification locale (JWT + hashing de mot de passe)
# -------------------------------------------------------

@router.post("/register")
def register_user(user: UtilisateurIn, db: Session = Depends(get_db)):

    # Vérifier si l'utilisateur existe déjà
    existing_user = db.query(Utilisateur).filter(Utilisateur.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email déjà utilisé!")
    
    # Vérifier si le mdp est trop long 
    if len(user.password.encode("utf-8")) > 72:
        raise HTTPException(status_code=400, detail="Mot de passe trop long! (max 72 caractères pour bycrypt)")
    
    # Hash du mot de passe
    try:
        hashed = hash_password(user.password).decode("utf-8")
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

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


# -------------------------------------------------------
# Login LDAP -> JWT
# -------------------------------------------------------
@router.post("/login-ldap")
def login_ldap(payload: LoginLDAP):

    # vérifier l'authentification de l'utilisateur via LDAP
    valid_auth = auth_ldap(payload.username, payload.password)

    if not valid_auth:
        raise HTTPException(status_code=401, detail="Identifiants LDAP invalides...")

    # Si l'authentification LDAP est réussie, on génère un token JWT pour l'utilisateur
    token = create_access_token(data=payload.username)

    return {
        "access_token": token,
        "token_type": "bearer",
        "username": payload.username
    }

# -------------------------------------------------------
# Login Local -> JWT
# -------------------------------------------------------
@router.post("/login") # email + mdp -> token JWT
def login_local(payload: LoginLocal, db: Session = Depends(get_db)):
    user = db.query(Utilisateur).filter(Utilisateur.email == payload.email).first()
    
    # Vérifier si l'utilisateur existe
    if not user:
        raise HTTPException(status_code=401, detail="Email utilisateur incorrecte")

    # Vérifier le mot de passe
    if not verify_password(payload.password, user.password):
        raise HTTPException(status_code=401, detail="Mot de passe invalide")

    # Générer le token JWT
    token = create_access_token(data=payload.email)

    return {
        "access_token": token,
        "token_type": "bearer",
        "email": payload.email
    }


@router.get("/debug-user/{email}")
def debug_user(email: str, db: Session = Depends(get_db)):
    user = db.query(Utilisateur).filter(Utilisateur.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"email": user.email, "password_hash": user.password}

# @router.get("/me") # token JWT -> infos de l'utilisateur connecté

