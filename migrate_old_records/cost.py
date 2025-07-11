import os
from azure.cosmos import CosmosClient

COSMOS_ENDPOINT = os.environ['COSMOS_ENDPOINT']
COSMOS_KEY = os.environ['COSMOS_KEY']
COSMOS_DB = os.environ.get('COSMOS_DB', 'BillingDB')
COSMOS_CONTAINER = os.environ.get('COSMOS_CONTAINER', 'BillingRecords')

client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
database = client.get_database_client(COSMOS_DB)
container = database.get_container_client(COSMOS_CONTAINER)

def get_old_records(cutoff_date):
    query = f"SELECT * FROM c WHERE c.timestamp < '{cutoff_date.isoformat()}'"
    return list(container.query_items(query, enable_cross_partition_query=True))

def delete_record(record_id):
    container.delete_item(item=record_id, partition_key=record_id)
