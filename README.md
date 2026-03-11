# Realisation du CRUD sur BDD Formation, sur API Python et Core.Net


---

# Objectif du projet

Ce projet implémente un système de surveillance vidéo capable de :

- Crée la base de donnée SQLServer à partir de la BDD issu de notre MPD draw.io
- Avec docker créer 3 contenaires ( sqlserver, python-api, dotnet-api)
- Realiser les endpoints (Crate, Read, Update, Delete) pour chaque tables (prio Utilisateur)

---

## Initialisation

On va travailler sur 2 terminaux, l'un va lancer notre docker pour activer les conteneurs, l'autre lancera notre API

### I - FastAPI (Python) : Lancement de Unvicorn (sur Powershell)

1) Creation d'un environnement virtuel et initialisation:

```bash
cd ./python-api/

py -m venv venv

venv/Scripts/activate

pip install -r requirements.txt
```

2) Lancement du serveur uvicorn:

```bash
uvicorn app.main:app --reload
```

Maintenant pour accéder à notre Swagger apres le lancement du serveur:

```bash
http://127.0.0.1:8000
```

---

### II - .NET Core (C#) :

Pour .NET Core on n'a pas installer ses dépendances sur notre environnement de travail.
A la place, pour son installation, on fait tout via Docker dans notre Dockerfile de notre dossier dotnet-api

Dans la partie suivante, lorsque l'on aura effectué notre docker compose qui chargera tous nos conteneurs, on lancera notre Swagger via:

```bash
http://localhost:5000/swagger
```

---

### II - .NET Core (C#) :

2) Docker : lancement des 3 conteners (sur Bash)

Ouvrir docker desktop afin  de bien visualiser l'activation des conteneurs
On effectuer la première ligne de commande si nos conteneurs dockers n'ont pas encore été crées

```bash
docker compose down
docker compose build --no-cache python-api

docker compose up --build
```

3) créer le .env à la racine de notre projet

```python
## Si souhaite communiquer avec une DB sur une VM depuis une auter VM
# DB_HOST="10.0.1.4"
# DB_USER="sa"
# DB_PASSWORD=""
# DB_NAME="FormationDB"
# DB_PORT=1433
# AZURE_STORAGE_CONNECTION_STRING=""

SECRET_KEY="dev_secret_change_me"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES="10"

# Pour local
DB_HOST="localhost"
DB_USER="sa"
DB_PASSWORD="Str0ng!Passw0rd123" # le même utilisé dans docker-compose.yml
DB_NAME="FormationDB"
DB_PORT=1433

# Requete LDAP
LDAP_SERVER=192.168.170.10
LDAP_DOMAIN=isen.fr
```
