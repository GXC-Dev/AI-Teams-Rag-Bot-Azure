
param location string
param name string

resource search 'Microsoft.Search/searchServices@2023-11-01' = {
  name: name
  location: location
  sku: { name: 'basic' }
  properties: {
    replicaCount: 1
    partitionCount: 1
    hostingMode: 'default'
    publicNetworkAccess: 'enabled'
    semanticSearch: { configuration: 'free' }
  }
}

output hostName string = search.properties.hostName
