
import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

load_dotenv()

connection_string_blob = os.getenv("AZURE_STORAGE_CONNECTION_STRING")


# stockage d'image sur le blob
container_name = "images"
file_path = r"C:\Users\jblize\Desktop\image2.webp"
blob_name = "image2.webp"

# connexion
blob_service_client = BlobServiceClient.from_connection_string(connection_string_blob)

# container
container_client = blob_service_client.get_container_client(container_name)

# upload
with open(file_path, "rb") as data:
    container_client.upload_blob(name=blob_name, data=data, overwrite=True)
print("Image envoyée sur Azure Blob Storage")