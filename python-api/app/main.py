from fastapi import FastAPI, Depends, HTTPException
from app.routeurs import utilisateurs, formations, modules, sessions, resultats, recommandations, inscriptions, auth
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from app import models, schemas


# -------------------------------------------------------
# DB (qu'on adapte pour SQL Server dans db.py)
# -------------------------------------------------------
CONNECT_STRING = "sqlite:///./dev.db"
engine = create_engine(CONNECT_STRING, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------------------------------------
# APP Swagger + FastAPI
# -------------------------------------------------------
app = FastAPI(title="Base de données: Formation APIs - CRUD complet")

app.include_router(auth.router)

app.include_router(utilisateurs.router)
app.include_router(formations.router)
app.include_router(modules.router)
app.include_router(sessions.router)
app.include_router(resultats.router)
app.include_router(recommandations.router)
app.include_router(inscriptions.router)












# -------------------------------------------------------
# JOINTURES : Posseder (Formation <-> Module)
# -------------------------------------------------------
@app.get("/posseder")
def list_posseder(db: Session = Depends(get_db)):
    return db.query(models.Posseder).all()

@app.post("/posseder", status_code=201)
def create_posseder(payload: schemas.PossederIn, db: Session = Depends(get_db)):
    obj = models.Posseder(**payload.model_dump())
    db.add(obj)
    db.commit()
    return payload

@app.delete("/posseder/{id_module}/{id_formation}", status_code=204)
def delete_posseder(id_module: int, id_formation: int, db: Session = Depends(get_db)):
    obj = db.query(models.Posseder).filter_by(id_module=id_module, id_formation=id_formation).first()
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
    return db.query(models.Suggere).all()

@app.post("/suggere", status_code=201)
def create_suggere(payload: schemas.SuggereIn, db: Session = Depends(get_db)):
    obj = models.Suggere(**payload.model_dump())
    db.add(obj)
    db.commit()
    return payload

@app.delete("/suggere/{id_recommandation}/{id_formation}", status_code=204)
def delete_suggere(id_recommandation: int, id_formation: int, db: Session = Depends(get_db)):
    obj = db.query(models.Suggere).filter_by(id_recommandation=id_recommandation, id_formation=id_formation).first()
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
    return db.query(models.Recommander).all()

@app.post("/recommander", status_code=201)
def create_recommander(payload: schemas.RecommanderIn, db: Session = Depends(get_db)):
    obj = models.Recommander(**payload.model_dump())
    db.add(obj)
    db.commit()
    return payload

@app.delete("/recommander/{id_utilisateur}/{id_recommandation}", status_code=204)
def delete_recommander(id_utilisateur: int, id_recommandation: int, db: Session = Depends(get_db)):
    obj = db.query(models.Recommander).filter_by(id_utilisateur=id_utilisateur, id_recommandation=id_recommandation).first()
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
    return db.query(models.Sinscrire).all()

@app.post("/inscriptions", status_code=201)
def create_inscription(payload: schemas.InscriptionIn, db: Session = Depends(get_db)):
    obj = models.Sinscrire(**payload.model_dump())
    db.add(obj)
    db.commit()
    return payload

@app.delete("/inscriptions/{id_utilisateur}/{id_session}", status_code=204)
def delete_inscription(id_utilisateur: int, id_session: int, db: Session = Depends(get_db)):
    obj = db.query(models.Sinscrire).filter_by(id_utilisateur=id_utilisateur, id_session=id_session).first()
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
    return db.query(models.Obtenir).all()

@app.post("/obtenir", status_code=201)
def create_obtenir(payload: schemas.ObtenirIn, db: Session = Depends(get_db)):
    obj = models.Obtenir(**payload.model_dump())
    db.add(obj)
    db.commit()
    return payload

@app.delete("/obtenir/{id_utilisateur}/{id_resultats}", status_code=204)
def delete_obtenir(id_utilisateur: int, id_resultats: int, db: Session = Depends(get_db)):
    obj = db.query(models.Obtenir).filter_by(id_utilisateur=id_utilisateur, id_resultats=id_resultats).first()
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
    return db.query(models.Passer).all()

@app.post("/passer", status_code=201)
def create_passer(payload: schemas.PasserIn, db: Session = Depends(get_db)):
    obj = models.Passer(**payload.model_dump())
    db.add(obj)
    db.commit()
    return payload

@app.delete("/passer/{id_utilisateur}/{id_resultats}", status_code=204)
def delete_passer(id_utilisateur: int, id_resultats: int, db: Session = Depends(get_db)):
    obj = db.query(models.Passer).filter_by(id_utilisateur=id_utilisateur, id_resultats=id_resultats).first()
    if not obj:
        raise HTTPException(404, "Link not found")
    db.delete(obj)
    db.commit()
    return None