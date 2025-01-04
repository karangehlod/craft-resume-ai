output "storage_account_name" {
  value = azurerm_storage_account.storage.name
}

output "storage_account_key" {
  value = azurerm_storage_account.storage.primary_access_key
  sensitive = true
}

output "storage_container_name" {
  value = azurerm_storage_container.container.name
}

output "cognitive_account_key" {
  value = azurerm_cognitive_account.cognitive.primary_access_key
  sensitive = true
}

output "cognitive_account_endpoint" {
  value = azurerm_cognitive_account.cognitive.endpoint
}

output "openai_account_key" {
  value = azurerm_key_vault_secret.openai_key.value
  sensitive = true
}

output "openai_account_endpoint" {
  value = azurerm_key_vault_secret.openai_endpoint.value
  sensitive = true
}

output "openai_deployment_name" {
  value = azurerm_key_vault_secret.openai_deployment.value
  sensitive = true
}

output "openai_model" {
  value = var.openai_model
}

output "openai_api_version" {
  value = var.openai_api_version
}

output "key_vault_uri" {
  value = azurerm_key_vault.kv.vault_uri
}