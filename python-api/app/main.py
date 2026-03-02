from datetime import date
from typing import Optional, List

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import (
    Column, Integer, String, ForeignKey, SmallInteger,
    PrimaryKeyConstraint, create_engine
)
from sqlalchemy.orm import declarative_base, sessionmaker, Session




# -------------------------------------------------------
# DB (à adapter à ta connexion SQL Server)
# -------------------------------------------------------
DATABASE_URL = "sqlite:///./dev.db"  # <-- remplace par ton SQL Server
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------------------------------------
# MODELS (SQLAlchemy)
# -------------------------------------------------------

class Utilisateur(Base):
    __tablename__ = "utilisateurs"
    id_utilisateur = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    email = Column(String, nullable=False)  # unique conseillé (à mettre côté DB)

class Formation(Base):
    __tablename__ = "formations"
    id_formation = Column(Integer, primary_key=True, index=True)
    titre = Column(String, nullable=False)
    description = Column(String, nullable=False)
    duree = Column(String, nullable=True)  # ton schéma indique char

class ModuleFormation(Base):
    __tablename__ = "modules_de_formations"
    id_module = Column(Integer, primary_key=True, index=True)
    titre = Column(String, nullable=False)
    contenu = Column(String, nullable=False)
    duree = Column(String, nullable=True)

class SessionFormation(Base):
    __tablename__ = "session_de_formations"
    id_session = Column(Integer, primary_key=True, index=True)
    id_formation = Column(Integer, ForeignKey("formations.id_formation"), nullable=False)
    date_debut = Column(String, nullable=False)
    date_fin = Column(String, nullable=False)
    lieu = Column(String, nullable=False)
    capacite = Column(Integer, nullable=False)
    mode = Column(SmallInteger, nullable=True)  # tinyint (0/1)

class Resultat(Base):
    __tablename__ = "resultats"
    id_resultats = Column(Integer, primary_key=True, index=True)
    id_module = Column(Integer, ForeignKey("modules_de_formations.id_module"), nullable=False)
    note = Column(Integer, nullable=True)
    reussite = Column(SmallInteger, nullable=True)  # tinyint (0/1)
    date_passage = Column(String, nullable=False)
    tentative = Column(SmallInteger, nullable=True)

class Recommendation(Base):
    __tablename__ = "recommendations"
    id_recommandation = Column(Integer, primary_key=True, index=True)
    date = Column(String, nullable=False)
    score_pertinence = Column(Integer, nullable=False)
    motif = Column(String, nullable=True)

# ----- Tables de jointure (PK composite) -----

class Posseder(Base):
    __tablename__ = "posseder"
    id_module = Column(Integer, ForeignKey("modules_de_formations.id_module"), nullable=False)
    id_formation = Column(Integer, ForeignKey("formations.id_formation"), nullable=False)
    __table_args__ = (PrimaryKeyConstraint("id_module", "id_formation"),)

class Suggere(Base):
    __tablename__ = "suggere"
    id_recommandation = Column(Integer, ForeignKey("recommendations.id_recommandation"), nullable=False)
    id_formation = Column(Integer, ForeignKey("formations.id_formation"), nullable=False)
    __table_args__ = (PrimaryKeyConstraint("id_recommandation", "id_formation"),)

class Recommander(Base):
    __tablename__ = "recommander"
    id_utilisateur = Column(Integer, ForeignKey("utilisateurs.id_utilisateur"), nullable=False)
    id_recommandation = Column(Integer, ForeignKey("recommendations.id_recommandation"), nullable=False)
    __table_args__ = (PrimaryKeyConstraint("id_utilisateur", "id_recommandation"),)

class Sinscrire(Base):
    __tablename__ = "sinscrire"
    id_utilisateur = Column(Integer, ForeignKey("utilisateurs.id_utilisateur"), nullable=False)
    id_session = Column(Integer, ForeignKey("session_de_formations.id_session"), nullable=False)
    date_inscription = Column(String, nullable=False)
    __table_args__ = (PrimaryKeyConstraint("id_utilisateur", "id_session"),)

class Obtenir(Base):
    __tablename__ = "obtenir"
    id_utilisateur = Column(Integer, ForeignKey("utilisateurs.id_utilisateur"), nullable=False)
    id_resultats = Column(Integer, ForeignKey("resultats.id_resultats"), nullable=False)
    __table_args__ = (PrimaryKeyConstraint("id_utilisateur", "id_resultats"),)

class Passer(Base):
    __tablename__ = "passer"
    id_utilisateur = Column(Integer, ForeignKey("utilisateurs.id_utilisateur"), nullable=False)
    id_resultats = Column(Integer, ForeignKey("resultats.id_resultats"), nullable=False)
    __table_args__ = (PrimaryKeyConstraint("id_utilisateur", "id_resultats"),)

# -------------------------------------------------------
# SCHEMAS (Pydantic) si on met autre chose que le modele ça fait une erreur de validation (ex: email pas bon)
# -------------------------------------------------------

class UtilisateurIn(BaseModel):
    nom: str
    prenom: str
    email: EmailStr

class UtilisateurOut(UtilisateurIn):
    id_utilisateur: int
    class Config:
        from_attributes = True

class FormationIn(BaseModel):
    titre: str
    description: str
    duree: Optional[str] = None

class FormationOut(FormationIn):
    id_formation: int
    class Config:
        from_attributes = True

class ModuleIn(BaseModel):
    titre: str
    contenu: str
    duree: Optional[str] = None

class ModuleOut(ModuleIn):
    id_module: int
    class Config:
        from_attributes = True

class SessionIn(BaseModel):
    id_formation: int
    date_debut: str
    date_fin: str
    lieu: str
    capacite: int
    mode: Optional[int] = None  # 0/1

class SessionOut(SessionIn):
    id_session: int
    class Config:
        from_attributes = True

class ResultatIn(BaseModel):
    id_module: int
    note: Optional[int] = None
    reussite: Optional[int] = None
    date_passage: str
    tentative: Optional[int] = None

class ResultatOut(ResultatIn):
    id_resultats: int
    class Config:
        from_attributes = True

class RecommendationIn(BaseModel):
    date: str
    score_pertinence: int
    motif: Optional[str] = None

class RecommendationOut(RecommendationIn):
    id_recommandation: int
    class Config:
        from_attributes = True

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

class SinscrireIn(BaseModel):
    id_utilisateur: int
    id_session: int
    date_inscription: str

class ObtenirIn(BaseModel):
    id_utilisateur: int
    id_resultats: int

class PasserIn(BaseModel):
    id_utilisateur: int
    id_resultats: int

# -------------------------------------------------------
# APP
# -------------------------------------------------------
app = FastAPI(title="Base de données: Formation APIs - CRUD complet")

# Base.metadata.create_all(bind=engine)

# -------------------------------------------------------
# Helpers 
# -------------------------------------------------------
def get_or_404(db: Session, model, pk_name: str, pk_value: int):
    obj = db.get(model, pk_value)
    if not obj:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    return obj



# -------------------------------------------------------
# CRUD : Utilisateurs
# -------------------------------------------------------
@app.get("/utilisateurs", response_model=List[UtilisateurOut])
def list_utilisateurs(db: Session = Depends(get_db)):
    return db.query(Utilisateur).all()

@app.get("/utilisateurs/{id_utilisateur}", response_model=UtilisateurOut)
def get_utilisateur(id_utilisateur: int, db: Session = Depends(get_db)):
    return get_or_404(db, Utilisateur, "id_utilisateur", id_utilisateur)

@app.post("/utilisateurs", response_model=UtilisateurOut, status_code=201)
def create_utilisateur(payload: UtilisateurIn, db: Session = Depends(get_db)):
    obj = Utilisateur(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.put("/utilisateurs/{id_utilisateur}", response_model=UtilisateurOut)
def update_utilisateur(id_utilisateur: int, payload: UtilisateurIn, db: Session = Depends(get_db)):
    obj = get_or_404(db, Utilisateur, "id_utilisateur", id_utilisateur)
    for k, v in payload.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@app.delete("/utilisateurs/{id_utilisateur}", status_code=204)
def delete_utilisateur(id_utilisateur: int, db: Session = Depends(get_db)):
    obj = get_or_404(db, Utilisateur, "id_utilisateur", id_utilisateur)
    db.delete(obj)
    db.commit()
    return None

# -------------------------------------------------------
# CRUD : Formations
# -------------------------------------------------------
@app.get("/formations", response_model=List[FormationOut])
def list_formations(db: Session = Depends(get_db)):
    return db.query(Formation).all()

@app.get("/formations/{id_formation}", response_model=FormationOut)
def get_formation(id_formation: int, db: Session = Depends(get_db)):
    return get_or_404(db, Formation, "id_formation", id_formation)

@app.post("/formations", response_model=FormationOut, status_code=201)
def create_formation(payload: FormationIn, db: Session = Depends(get_db)):
    obj = Formation(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.put("/formations/{id_formation}", response_model=FormationOut)
def update_formation(id_formation: int, payload: FormationIn, db: Session = Depends(get_db)):
    obj = get_or_404(db, Formation, "id_formation", id_formation)
    for k, v in payload.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@app.delete("/formations/{id_formation}", status_code=204)
def delete_formation(id_formation: int, db: Session = Depends(get_db)):
    obj = get_or_404(db, Formation, "id_formation", id_formation)
    db.delete(obj)
    db.commit()
    return None

# -------------------------------------------------------
# CRUD : Modules
# -------------------------------------------------------
@app.get("/modules", response_model=List[ModuleOut])
def list_modules(db: Session = Depends(get_db)):
    return db.query(ModuleFormation).all()

@app.get("/modules/{id_module}", response_model=ModuleOut)
def get_module(id_module: int, db: Session = Depends(get_db)):
    return get_or_404(db, ModuleFormation, "id_module", id_module)

@app.post("/modules", response_model=ModuleOut, status_code=201)
def create_module(payload: ModuleIn, db: Session = Depends(get_db)):
    obj = ModuleFormation(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.put("/modules/{id_module}", response_model=ModuleOut)
def update_module(id_module: int, payload: ModuleIn, db: Session = Depends(get_db)):
    obj = get_or_404(db, ModuleFormation, "id_module", id_module)
    for k, v in payload.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@app.delete("/modules/{id_module}", status_code=204)
def delete_module(id_module: int, db: Session = Depends(get_db)):
    obj = get_or_404(db, ModuleFormation, "id_module", id_module)
    db.delete(obj)
    db.commit()
    return None

# -------------------------------------------------------
# CRUD : Sessions
# -------------------------------------------------------
@app.get("/sessions", response_model=List[SessionOut])
def list_sessions(db: Session = Depends(get_db)):
    return db.query(SessionFormation).all()

@app.get("/sessions/{id_session}", response_model=SessionOut)
def get_session(id_session: int, db: Session = Depends(get_db)):
    return get_or_404(db, SessionFormation, "id_session", id_session)

@app.post("/sessions", response_model=SessionOut, status_code=201)
def create_session(payload: SessionIn, db: Session = Depends(get_db)):
    obj = SessionFormation(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.put("/sessions/{id_session}", response_model=SessionOut)
def update_session(id_session: int, payload: SessionIn, db: Session = Depends(get_db)):
    obj = get_or_404(db, SessionFormation, "id_session", id_session)
    for k, v in payload.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@app.delete("/sessions/{id_session}", status_code=204)
def delete_session(id_session: int, db: Session = Depends(get_db)):
    obj = get_or_404(db, SessionFormation, "id_session", id_session)
    db.delete(obj)
    db.commit()
    return None

# -------------------------------------------------------
# CRUD : Résultats
# -------------------------------------------------------
@app.get("/resultats", response_model=List[ResultatOut])
def list_resultats(db: Session = Depends(get_db)):
    return db.query(Resultat).all()

@app.get("/resultats/{id_resultats}", response_model=ResultatOut)
def get_resultat(id_resultats: int, db: Session = Depends(get_db)):
    return get_or_404(db, Resultat, "id_resultats", id_resultats)

@app.post("/resultats", response_model=ResultatOut, status_code=201)
def create_resultat(payload: ResultatIn, db: Session = Depends(get_db)):
    obj = Resultat(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.put("/resultats/{id_resultats}", response_model=ResultatOut)
def update_resultat(id_resultats: int, payload: ResultatIn, db: Session = Depends(get_db)):
    obj = get_or_404(db, Resultat, "id_resultats", id_resultats)
    for k, v in payload.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@app.delete("/resultats/{id_resultats}", status_code=204)
def delete_resultat(id_resultats: int, db: Session = Depends(get_db)):
    obj = get_or_404(db, Resultat, "id_resultats", id_resultats)
    db.delete(obj)
    db.commit()
    return None

# -------------------------------------------------------
# CRUD : Recommendations
# -------------------------------------------------------
@app.get("/recommendations", response_model=List[RecommendationOut])
def list_recos(db: Session = Depends(get_db)):
    return db.query(Recommendation).all()

@app.get("/recommendations/{id_recommandation}", response_model=RecommendationOut)
def get_reco(id_recommandation: int, db: Session = Depends(get_db)):
    return get_or_404(db, Recommendation, "id_recommandation", id_recommandation)

@app.post("/recommendations", response_model=RecommendationOut, status_code=201)
def create_reco(payload: RecommendationIn, db: Session = Depends(get_db)):
    obj = Recommendation(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.put("/recommendations/{id_recommandation}", response_model=RecommendationOut)
def update_reco(id_recommandation: int, payload: RecommendationIn, db: Session = Depends(get_db)):
    obj = get_or_404(db, Recommendation, "id_recommandation", id_recommandation)
    for k, v in payload.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@app.delete("/recommendations/{id_recommandation}", status_code=204)
def delete_reco(id_recommandation: int, db: Session = Depends(get_db)):
    obj = get_or_404(db, Recommendation, "id_recommandation", id_recommandation)
    db.delete(obj)
    db.commit()
    return None

# -------------------------------------------------------
# JOINTURES : Posseder (Formation <-> Module)
# -------------------------------------------------------
@app.get("/posseder")
def list_posseder(db: Session = Depends(get_db)):
    return db.query(Posseder).all()

@app.post("/posseder", status_code=201)
def create_posseder(payload: PossederIn, db: Session = Depends(get_db)):
    obj = Posseder(**payload.model_dump())
    db.add(obj)
    db.commit()
    return payload

@app.delete("/posseder/{id_module}/{id_formation}", status_code=204)
def delete_posseder(id_module: int, id_formation: int, db: Session = Depends(get_db)):
    obj = db.query(Posseder).filter_by(id_module=id_module, id_formation=id_formation).first()
    if not obj:
        raise HTTPException(404, "Link not found")
    db.delete(obj)
    db.commit()
    return None

# -------------------------------------------------------
# JOINTURES : Suggere (Reco <-> Formation)
# -------------------------------------------------------
@app.get("/suggere")
def list_suggere(db: Session = Depends(get_db)):
    return db.query(Suggere).all()

@app.post("/suggere", status_code=201)
def create_suggere(payload: SuggereIn, db: Session = Depends(get_db)):
    obj = Suggere(**payload.model_dump())
    db.add(obj)
    db.commit()
    return payload

@app.delete("/suggere/{id_recommandation}/{id_formation}", status_code=204)
def delete_suggere(id_recommandation: int, id_formation: int, db: Session = Depends(get_db)):
    obj = db.query(Suggere).filter_by(id_recommandation=id_recommandation, id_formation=id_formation).first()
    if not obj:
        raise HTTPException(404, "Link not found")
    db.delete(obj)
    db.commit()
    return None

# -------------------------------------------------------
# JOINTURES : Recommander (User <-> Reco)
# -------------------------------------------------------
@app.get("/recommander")
def list_recommander(db: Session = Depends(get_db)):
    return db.query(Recommander).all()

@app.post("/recommander", status_code=201)
def create_recommander(payload: RecommanderIn, db: Session = Depends(get_db)):
    obj = Recommander(**payload.model_dump())
    db.add(obj)
    db.commit()
    return payload

@app.delete("/recommander/{id_utilisateur}/{id_recommandation}", status_code=204)
def delete_recommander(id_utilisateur: int, id_recommandation: int, db: Session = Depends(get_db)):
    obj = db.query(Recommander).filter_by(id_utilisateur=id_utilisateur, id_recommandation=id_recommandation).first()
    if not obj:
        raise HTTPException(404, "Link not found")
    db.delete(obj)
    db.commit()
    return None

# -------------------------------------------------------
# JOINTURES : Sinscrire (User <-> Session)
# -------------------------------------------------------
@app.get("/inscriptions")
def list_inscriptions(db: Session = Depends(get_db)):
    return db.query(Sinscrire).all()

@app.post("/inscriptions", status_code=201)
def create_inscription(payload: SinscrireIn, db: Session = Depends(get_db)):
    obj = Sinscrire(**payload.model_dump())
    db.add(obj)
    db.commit()
    return payload

@app.delete("/inscriptions/{id_utilisateur}/{id_session}", status_code=204)
def delete_inscription(id_utilisateur: int, id_session: int, db: Session = Depends(get_db)):
    obj = db.query(Sinscrire).filter_by(id_utilisateur=id_utilisateur, id_session=id_session).first()
    if not obj:
        raise HTTPException(404, "Link not found")
    db.delete(obj)
    db.commit()
    return None

# -------------------------------------------------------
# JOINTURES : Obtenir (User <-> Resultats)
# -------------------------------------------------------
@app.get("/obtenir")
def list_obtenir(db: Session = Depends(get_db)):
    return db.query(Obtenir).all()

@app.post("/obtenir", status_code=201)
def create_obtenir(payload: ObtenirIn, db: Session = Depends(get_db)):
    obj = Obtenir(**payload.model_dump())
    db.add(obj)
    db.commit()
    return payload

@app.delete("/obtenir/{id_utilisateur}/{id_resultats}", status_code=204)
def delete_obtenir(id_utilisateur: int, id_resultats: int, db: Session = Depends(get_db)):
    obj = db.query(Obtenir).filter_by(id_utilisateur=id_utilisateur, id_resultats=id_resultats).first()
    if not obj:
        raise HTTPException(404, "Link not found")
    db.delete(obj)
    db.commit()
    return None

# -------------------------------------------------------
# JOINTURES : Passer (User <-> Resultats)
# -------------------------------------------------------
@app.get("/passer")
def list_passer(db: Session = Depends(get_db)):
    return db.query(Passer).all()

@app.post("/passer", status_code=201)
def create_passer(payload: PasserIn, db: Session = Depends(get_db)):
    obj = Passer(**payload.model_dump())
    db.add(obj)
    db.commit()
    return payload

@app.delete("/passer/{id_utilisateur}/{id_resultats}", status_code=204)
def delete_passer(id_utilisateur: int, id_resultats: int, db: Session = Depends(get_db)):
    obj = db.query(Passer).filter_by(id_utilisateur=id_utilisateur, id_resultats=id_resultats).first()
    if not obj:
        raise HTTPException(404, "Link not found")
    db.delete(obj)
    db.commit()
    return None