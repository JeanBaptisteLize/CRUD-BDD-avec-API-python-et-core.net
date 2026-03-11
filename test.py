import pymssql
import os
from dotenv import load_dotenv

print("pymssql installé")
load_dotenv()


conn = pymssql.connect(
    server=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    port=os.getenv("DB_PORT")
)

cursor = conn.cursor()

cursor.execute("SELECT TOP 5 TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.TABLES")

print(cursor.fetchall())

print("Connexion réussie :")


conn.close()