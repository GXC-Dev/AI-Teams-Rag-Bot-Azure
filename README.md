
# Teams RAG Bot on Azure
Production-grade Teams chatbot that answers from your manuals/policies using **Azure OpenAI** + **Azure AI Search**. Designed for **consistent, citation-backed answers** every time.

## Features
- RAG over your PDFs (Blob → Azure AI Search)
- Microsoft Teams integration (Bot Framework)
- Strict policy-grounded responses + **Sources:** line
- One-click deploy (scratch or existing Azure)
- Repeatable smoke/eval tests

## Quick Start
1. `az login`
2. Edit `deploy/deploy.ps1` header (choose `$UseExistingResources` true/false).
3. Run: `pwsh ./deploy/deploy.ps1`
4. Upload PDFs to the `manuals` container; then:
   ```bash
   pip install -r src/ingest/requirements.txt
   python src/ingest/ingest.py
   ```
5. Create Azure Bot (if not auto), set messaging endpoint to `https://<webapp>/api/messages`.
6. Add Teams channel, install to your team.

## Local Dev (API)
```bash
cd src/api
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

## Environment Variables
See `.env.example` or configure App Settings on the Web App.

## Repo Layout
- `deploy/` – bicep + deploy script
- `src/api` – FastAPI RAG service
- `src/bot` – Teams bot (forwards to RAG API)
- `src/ingest` – Index builder for Azure AI Search
- `tests/` – smoke & eval templates

## License
MIT
