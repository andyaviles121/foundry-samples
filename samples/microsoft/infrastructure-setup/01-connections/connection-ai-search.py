from azure.identity import DefaultAzureCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient

sub_id = '{SUBSCRIPTION_ID}'
rgp = '{RESOURCE_GROUP_NAME}'
account_name = '{ACCOUNT_NAME}'
project_name = '{PROJECT_NAME}'
location = '{LOCATION}'
aisearch_account_name = '{AIS_ACCOUNT_NAME}'
aisearch_connection_name = 'myaisearchconnection'

# Provide the API key here or call it from a vault directly
api_key = "{API_KEY}"

# Client
client = CognitiveServicesManagementClient(
    credential=DefaultAzureCredential(), 
    subscription_id=sub_id,
    api_version="2025-04-01-preview"
)

# Create AI Search Account Connection
client.account_connections.create(
    resource_group_name=rgp,
    account_name=account_name,
    connection_name=aisearch_connection_name,
    connection={
        "properties": {
            "authType": "ApiKey",
            "category": "CognitiveSearch",
            "isSharedToAll": True,
            "target": "https://{}.search.windows.net/".format(aisearch_account_name),
            "credentials": {
                "key": api_key
            },
            "metadata": {
                "ApiType": "Azure",
                "resourceId": "/subscriptions/{}/resourceGroups/{}/providers/Microsoft.Search/searchServices/{}".format(sub_id, rgp, aisearch_account_name),
                "location": location
            } 
        }
    }
)
