import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import pymssql
from dotenv import load_dotenv

from azure.storage.blob import BlobServiceClient

load_dotenv()

# Configuration de la connexion à SQL Server avec notre fichier environnement
DB_HOST = os.getenv("DB_HOST", "localhost/10.0.1.4")
DB_PORT = int(os.getenv("DB_PORT", "1433"))
DB_USER = os.getenv("DB_USER", "sa")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Str0ng!Passw0rd123/monmdpssecert")
DB_NAME = os.getenv("DB_NAME", "FormationDB")

# pymssql est necessaire pour la connexion à SQL server
CONNECT_STRING = (
    f"mssql+pymssql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


# creation du moteur SQLAlchemy et de la session de base de données
engine = create_engine(CONNECT_STRING, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

with engine.connect() as conn:
    print("DB:", conn.execute(text("SELECT DB_NAME()")).scalar())


# Base pour les modèles SQLAlchemy (models.py)
class Base(DeclarativeBase):
    pass


# Fournir une session propre pour chaque requête API
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


'''
L’objectif de ce fichier :

🔹 Configurer la connexion à SQL Server
🔹 Créer un moteur SQLAlchemy
🔹 Créer une session de base de données
🔹 Fournir une session propre pour chaque requête API
'''