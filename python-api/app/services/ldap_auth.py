import os
from dotenv import load_dotenv
from ldap3 import Server, Connection, ALL

# Notre server LDAP nous permet de vérifier l'identité de nos utilisateurs en se connectant à notre annuaire d'entreprise (ISEN)

load_dotenv()

LDAP_SERVER = os.getenv("LDAP_SERVER")
LDAP_DOMAIN = os.getenv("LDAP_DOMAIN")


def auth_ldap(username: str, password: str) -> bool:
    user_principal_name = f"{username}@{LDAP_DOMAIN}"      # Construire le User Principal Name (UPN) pour l'authentification LDAP

    server = Server(LDAP_SERVER, get_info=ALL)      # ALL pour récupérer les informations du serveur LDAP, comme les schémas et les attributs disponibles

    try:
        connect = Connection(
            server,
            user=user_principal_name,
            password=password,
            auto_bind=True
        )
        connect.unbind()
        print("✅ Authentification réussie pour l'utilisateur:", username, "!!!")
        return True
    
    except Exception as error:
        print("⚠️ Erreur d'authentification LDAP:", error)
        return False

if __name__ == "__main__":
    print("Test d'authentification LDAP: ")
    #auth_ldap("patrice.cognet", "S1pln83!")
    auth_ldap("devia", "Ch@t83!")
    #auth_ldap("deviadmin", "CeUnscrt!")