import os       # pour accéder aux variables d'environnement du .env
from datetime import datetime, timedelta, timezone

from passlib import context
from jose import JWTError, jwt


# Configuration pour les tokens JWT en utilisant des variables d'environnement du .env
SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_change_me")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES","60"))

# Configuration pour le hachage des mots de passe (bycrypt)
pwd_hash = context.CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_hash.verify(password, hashed_password)


# Création de la clé JWT à partir des données utilisateurs (id,email,password haché)
def create_access_token(data):
    try:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})

        token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return token
    except JWTError as err:
        raise JWTError(f"Erreur lors de la création du token JWT : {err}")


def decode_access_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded
    except JWTError as err:
        raise JWTError(f"Erreur lors du décodage du token JWT : {err}")

