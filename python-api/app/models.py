from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    SmallInteger,
    PrimaryKeyConstraint
)
from app.db import Base


# -------------------------------------------------------
# MODELS (SQLAlchemy) : correspondance avec les tables de la DB 
# -------------------------------------------------------


class Utilisateur(Base):
    __tablename__ = "utilisateurs"
    __table_args__ = {"schema": "dbo"}  # ✅ important si table dbo.utilisateurs

    id_utilisateur = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)  # on stocke le hash du mot de passe


class Formation(Base):
    __tablename__ = "formations"

    id_formation = Column(Integer, primary_key=True, index=True)
    titre = Column(String, nullable=False)
    description = Column(String, nullable=False)
    duree = Column(String, nullable=True)


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
    __tablename__ = "recommandations"

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
