import os       # pour accéder aux variables d'environnement du .env
from datetime import datetime, timedelta, timezone
import bcrypt
from jose import JWTError, jwt


# Configuration pour les tokens JWT en utilisant des variables d'environnement du .env
SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_change_me")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES","60"))


def hash_password(password: str):
    try:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    except ValueError:
        raise ValueError("Le mot de passe dépasse 72 bytes, incompatible avec bcrypt.")


def verify_password(password: str, hashed_password: str):
    if len(password.encode("utf-8")) > 72:
        return False
    hashed_password = hashed_password.strip()  # supprime les espaces invisibles
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)


# Création de la clé JWT à partir des données utilisateurs (id,email,password haché)
def create_access_token(data: str|dict):
    if isinstance(data, str):
        to_encode = {"date": data}
    else:
        to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    try:
        return token
    except JWTError as error:
        raise JWTError(f"Erreur lors de la création du token JWT : {error}")


def decode_access_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as error:
        raise JWTError(f"Erreur lors du décodage du token JWT : {error}")

