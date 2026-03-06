
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions

load_dotenv()

connection_string_blob = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

# stockage d'image sur le blob
storage_account = "storagecursedimages"
container_name = "images"
file_path = r"C:\Users\jblize\Desktop\image3.jpg"
blob_name = "image3.jpg"

# connexion
blob_service_client = BlobServiceClient.from_connection_string(connection_string_blob)

# container
container_client = blob_service_client.get_container_client(container_name)

# upload
with open(file_path, "rb") as data:
    container_client.upload_blob(name=blob_name, data=data, overwrite=True)
print("Image envoyée sur Azure Blob Storage")

account_name = blob_service_client.account_name
account_key = blob_service_client.credential.account_key

# génération du SAS token
sas_token = generate_blob_sas(
    account_name=account_name,
    container_name=container_name,
    blob_name=blob_name,
    account_key=account_key,
    permission=BlobSasPermissions(read=True),
    expiry=datetime.utcnow() + timedelta(minutes=2)
)

url = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"

print("Le lien URL temporaire et sécurisé du blob : ",url)