
import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

endpoint = os.environ["SEARCH_ENDPOINT"]
index_name = os.environ["SEARCH_INDEX_NAME"]
key = os.environ["SEARCH_ADMIN_KEY"]

_client = SearchClient(endpoint=endpoint, index_name=index_name, credential=AzureKeyCredential(key))

def retrieve(query, top=5):
    results = _client.search(search_text=query, top=top, query_type="semantic", semantic_configuration_name="default")
    docs = []
    for r in results:
        docs.append({"id": r["id"], "content": r["content"], "source": r.get("source","")})
    return docs
