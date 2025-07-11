import os
import json
from azure.storage.blob import BlobServiceClient

BLOB_CONN_STR = os.environ['AZURE_BLOB_CONNECTION']
BLOB_CONTAINER = os.environ.get('BLOB_CONTAINER', 'billing')

blob_service = BlobServiceClient.from_connection_string(BLOB_CONN_STR)
container = blob_service.get_container_client(BLOB_CONTAINER)

def save_to_blob(record):
    record_id = record['id']
    date_part = record['timestamp'][:10]  # "yyyy-MM-dd"
    blob_path = f"{date_part}/{record_id}.json"
    blob_client = container.get_blob_client(blob_path)
    blob_client.upload_blob(json.dumps(record), overwrite=True)

def read_from_blob(record_id, timestamp):
    date_part = timestamp[:10]
    blob_path = f"{date_part}/{record_id}.json"
    blob_client = container.get_blob_client(blob_path)
    try:
        data = blob_client.download_blob().readall()
        return json.loads(data)
    except Exception:
        return None
