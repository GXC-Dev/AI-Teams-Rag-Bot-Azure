
param location string
param searchServiceName string
param searchIndexName string
param storageAccountName string
param webAppName string
param keyVaultName string
param openAIAccountName string
@allowed(['gpt-4o-mini','chat-mini','o4-mini'])
param openAIChatDeployment string
@allowed(['text-embedding-3-large','text-embedding-3-small'])
param openAIEmbeddingDeployment string

module search 'modules/search.bicep' = {
  name: 'search'
  params: {
    location: location
    name: searchServiceName
  }
}

module storage 'modules/storage.bicep' = {
  name: 'storage'
  params: {
    location: location
    name: storageAccountName
  }
}

module appsvc 'modules/appsvc.bicep' = {
  name: 'appsvc'
  params: {
    location: location
    name: webAppName
  }
}

module kv 'modules/keyvault.bicep' = {
  name: 'kv'
  params: {
    location: location
    name: keyVaultName
  }
}

module aoai 'modules/aoai.bicep' = {
  name: 'aoai'
  params: {
    location: location
    name: openAIAccountName
    chatDeployment: openAIChatDeployment
    embedDeployment: openAIEmbeddingDeployment
  }
}
