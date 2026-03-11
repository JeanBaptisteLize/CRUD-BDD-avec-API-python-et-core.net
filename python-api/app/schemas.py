from typing import Optional
from pydantic import BaseModel, EmailStr

# -------------------------------------------------------
# SCHEMAS (Pydantic) si on met autre chose que le modele ça fait une erreur de validation (ex: email pas bon)
# -------------------------------------------------------

# Schema pour l'authentification LDAP

class LoginLDAP(BaseModel):
    username: str
    password: str

class LoginLocal(BaseModel):
    email: str
    password: str

#########################################################

class UtilisateurIn(BaseModel):
    nom: str
    prenom: str
    email: EmailStr
    password: str  # on reçoit le mot de passe en clair, on le hashera avant de le stocker en DB

class FormationIn(BaseModel):
    titre: str
    description: str
    duree: Optional[str] = None

class ModuleIn(BaseModel):
    titre: str
    contenu: str
    duree: Optional[str] = None

class SessionIn(BaseModel):
    id_formation: int
    date_debut: str
    date_fin: str
    lieu: str
    capacite: int
    mode: Optional[int] = None  # 0/1

class ResultatIn(BaseModel):
    id_module: int
    note: Optional[int] = None
    reussite: Optional[int] = None
    date_passage: str
    tentative: Optional[int] = None

class RecommendationIn(BaseModel):
    date: str
    score_pertinence: int
    motif: Optional[str] = None

class InscriptionIn(BaseModel):
    id_utilisateur: int
    id_session: int
    date_inscription: str

# Jointures
class PossederIn(BaseModel):
    id_module: int
    id_formation: int

class SuggereIn(BaseModel):
    id_recommandation: int
    id_formation: int

class RecommanderIn(BaseModel):
    id_utilisateur: int
    id_recommandation: int

class ObtenirIn(BaseModel):
    id_utilisateur: int
    id_resultats: int

class PasserIn(BaseModel):
    id_utilisateur: int
    id_resultats: int
