
import os, re, io
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.storage.blob import BlobServiceClient
from pypdf import PdfReader

SEARCH_ENDPOINT = os.environ["SEARCH_ENDPOINT"]
SEARCH_INDEX_NAME = os.environ["SEARCH_INDEX_NAME"]
SEARCH_ADMIN_KEY = os.environ["SEARCH_ADMIN_KEY"]
ST_CONN = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
DOCS_CONTAINER = os.getenv("DOCS_CONTAINER","manuals")

def list_blobs():
    bs = BlobServiceClient.from_connection_string(ST_CONN)
    cont = bs.get_container_client(DOCS_CONTAINER)
    return [b.name for b in cont.list_blobs() if b.name.lower().endswith(".pdf")]

def get_pdf_bytes(name):
    bs = BlobServiceClient.from_connection_string(ST_CONN)
    cont = bs.get_container_client(DOCS_CONTAINER)
    return cont.download_blob(name).readall()

def chunk_pages(pdf_bytes, source_name):
    reader = PdfReader(io.BytesIO(pdf_bytes))
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            yield {
              "id": f"{source_name}#p{i+1}",
              "content": text[:32000],
              "source": source_name,
              "page": i+1
            }

def upload_docs(docs):
    client = SearchClient(SEARCH_ENDPOINT, SEARCH_INDEX_NAME, AzureKeyCredential(SEARCH_ADMIN_KEY))
    batch = list(docs)
    for i in range(0, len(batch), 1000):
        client.upload_documents(documents=batch[i:i+1000])

if __name__ == "__main__":
    names = list_blobs()
    all_docs = []
    for n in names:
        pdfb = get_pdf_bytes(n)
        all_docs.extend(list(chunk_pages(pdfb, n)))
    upload_docs(all_docs)
    print(f"Indexed {len(all_docs)} chunks from {len(names)} PDFs.")
