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

1) FastAPI (Python) : Lancement de Unvicorn (sur Powershell)

Creation d'un environnement virtuel et initialisation:

```python
cd ./python-api/

py -m venv venv

venv/Scripts/activate

pip install -r requirements.txt
```

Lancement du server uvicorn:

```python
uvicorn app.main:app --reload
```

2) Docker : lancement des 3 conteners (sur Bash)

Ouvrir docker desktop afin  de bien visualiser l'activation des conteneurs

```python
docker compose build --no-cache python-api

docker compose up --build
```


