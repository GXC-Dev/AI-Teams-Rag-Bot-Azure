<# ================================
 Teams RAG Bot – Deploy Script
 Author: Gaurish (AI-102)
 Version: v1.0
================================ #>

param(
  [string]$SubscriptionId = "<PUT-YOURS>",
  [string]$Location = "australiaeast",
  [string]$Env = "dev",
  [bool]$UseExistingResources = $false,

  # If using existing, fill these; otherwise ignored.
  [string]$ResourceGroup = "rg-rag-bot",
  [string]$SearchServiceName = "ai-search-xyz",
  [string]$SearchIndexName = "kb-index",
  [string]$StorageAccountName = "stkbxyz",
  [string]$WebAppName = "app-rag-bot-xyz",
  [string]$KeyVaultName = "kv-rag-bot-xyz",
  [string]$OpenAIAccountName = "aoai-xyz",
  [string]$OpenAIChatDeployment = "gpt-4o-mini",
  [string]$OpenAIEmbeddingDeployment = "text-embedding-3-large"
)

$ErrorActionPreference = "Stop"

Write-Host ">>> Login & set subscription"
az account show 1>$null 2>$null; if ($LASTEXITCODE -ne 0) { az login | Out-Null }
az account set --subscription $SubscriptionId

if (-not $UseExistingResources) {
  $ResourceGroup       = "rg-rag-bot-$Env"
  $SearchServiceName   = "srch$($Env)$(Get-Random)"
  $SearchIndexName     = "kb-index"
  $StorageAccountName  = "st$($Env)$(Get-Random)"
  $WebAppName          = "app-rag-bot-$Env-$(Get-Random)"
  $KeyVaultName        = "kv-rag-bot-$Env-$(Get-Random)"
  $OpenAIAccountName   = "aoai-$Env-$(Get-Random)"

  Write-Host ">>> Creating resource group and deploying Bicep..."
  az group create -n $ResourceGroup -l $Location | Out-Null

  az deployment group create `
    -g $ResourceGroup `
    -f ./deploy/main.bicep `
    -p location=$Location `
       searchServiceName=$SearchServiceName `
       searchIndexName=$SearchIndexName `
       storageAccountName=$StorageAccountName `
       webAppName=$WebAppName `
       keyVaultName=$KeyVaultName `
       openAIAccountName=$OpenAIAccountName `
       openAIChatDeployment=$OpenAIChatDeployment `
       openAIEmbeddingDeployment=$OpenAIEmbeddingDeployment | Out-Null
}

Write-Host ">>> Fetching connection details"
$SEARCH_ENDPOINT = az search service show -g $ResourceGroup -n $SearchServiceName --query "hostName" -o tsv
$SEARCH_ENDPOINT = "https://$SEARCH_ENDPOINT"
$SEARCH_ADMIN_KEY = az search admin-key show -g $ResourceGroup -n $SearchServiceName --query "primaryKey" -o tsv
$ST_CONN = az storage account show-connection-string -g $ResourceGroup -n $StorageAccountName --query connectionString -o tsv
$AOAI_ENDPOINT = az cognitiveservices account show -g $ResourceGroup -n $OpenAIAccountName --query "properties.endpoint" -o tsv
$AOAI_KEY = az cognitiveservices account keys list -g $ResourceGroup -n $OpenAIAccountName --query "key1" -o tsv

Write-Host ">>> Configure App Settings on Web App"
az webapp config appsettings set -g $ResourceGroup -n $WebAppName --settings `
  SEARCH_ENDPOINT="$SEARCH_ENDPOINT" `
  SEARCH_ADMIN_KEY="$SEARCH_ADMIN_KEY" `
  SEARCH_INDEX_NAME="$SearchIndexName" `
  AZURE_STORAGE_CONNECTION_STRING="$ST_CONN" `
  AOAI_ENDPOINT="$AOAI_ENDPOINT" `
  AOAI_KEY="$AOAI_KEY" `
  AOAI_CHAT_DEPLOYMENT="$OpenAIChatDeployment" `
  AOAI_EMBED_DEPLOYMENT="$OpenAIEmbeddingDeployment" `
  RAG_STRICT_MODE="true" `
  MAX_TOKENS="1200" `
  TEMPERATURE="0" `
  RAG_API_URL="https://$($WebAppName).azurewebsites.net/api/chat" | Out-Null

Write-Host ">>> Package & deploy API (zip)"
$root = (Get-Item -Path ".").FullName
$apiZip = Join-Path $root "api.zip"
if (Test-Path $apiZip) { Remove-Item $apiZip -Force }
Compress-Archive -Path ./src/api/* -DestinationPath $apiZip
az webapp deployment source config-zip -g $ResourceGroup -n $WebAppName --src $apiZip | Out-Null

Write-Host "`n✅ Done. Web App URL:" (az webapp show -g $ResourceGroup -n $WebAppName --query "defaultHostName" -o tsv)
Write-Host "Next: upload PDFs to the 'manuals' container and run src/ingest/ingest.py, then connect the bot to Teams."
