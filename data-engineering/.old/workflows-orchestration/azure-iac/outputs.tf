# are needed to be passed to the .env file, so they're readable by
# the docker-compose.yml execution.
# so they're able to be passed to the mage container via environment variables

output "storage_account_name" {
  value = azurerm_storage_account.lake_account.name
}

output "client_id" {
  value     = azuread_application.app.application_id
  sensitive = true
}

output "client_secret" {
  value     = azuread_application_password.passkey.value
  sensitive = true
}