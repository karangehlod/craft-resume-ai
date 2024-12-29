provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}

data "azurerm_client_config" "current" {}

resource "azurerm_resource_group" "rg" {
  name     = "craft-resume-ai-rg"
  location = var.location
}

resource "azurerm_storage_account" "storage" {
  name                     = "craftresumeaistorage"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "container" {
  name                  = "resumes"
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = "private"
}

resource "azurerm_cognitive_account" "cognitive" {
  name                = "craftresumeaicognitive"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  kind                = "CognitiveServices"
  sku_name            = "S0"
}

resource "azurerm_key_vault" "kv" {
  name                = "craftresumeaikv"
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.location
  sku_name            = "standard"
  tenant_id           = data.azurerm_client_config.current.tenant_id

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id

    secret_permissions = [
      "Get", "List", "Set", "Delete"
    ]
  }
}

resource "azurerm_key_vault_secret" "openai_key" {
  name         = "AzureOpenAIKey"
  value        = "your-openai-key"  // Replace with actual key
  key_vault_id = azurerm_key_vault.kv.id
}

resource "azurerm_key_vault_secret" "openai_endpoint" {
  name         = "AzureOpenAIEndpoint"
  value        = "your-openai-endpoint"  // Replace with actual endpoint
  key_vault_id = azurerm_key_vault.kv.id
}

resource "azurerm_key_vault_secret" "openai_deployment" {
  name         = "AzureOpenAIDeployment"
  value        = "gpt4o-mini"  // or "gpt4o" based on your preference
  key_vault_id = azurerm_key_vault.kv.id
}

resource "azurerm_key_vault_secret" "openai_version" {
  name         = "AzureOpenAIVersion"
  value        = var.openai_api_version
  key_vault_id = azurerm_key_vault.kv.id
}