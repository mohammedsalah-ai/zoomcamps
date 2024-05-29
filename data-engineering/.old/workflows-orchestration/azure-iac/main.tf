terraform {
  required_providers {
    azuread = {
      source  = "hashicorp/azuread"
      version = "~> 2.15.0"
    }

    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.43.0"
    }
  }
}

provider "azuread" {}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "resources" {
  name     = var.resource_group_name
  location = var.location

  tags = {
    name = var.tag
  }
}

# lake
resource "azurerm_storage_account" "lake_account" {
  name                     = var.lake_account_name
  resource_group_name      = azurerm_resource_group.resources.name
  location                 = azurerm_resource_group.resources.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "lake_container" {
  name                  = var.lake_container_name
  container_access_type = var.lake_container_access_type
  storage_account_name  = azurerm_storage_account.lake_account.name
}

# app registration for mage
resource "azuread_application" "app" {
  display_name = var.app_name
}

resource "azuread_service_principal" "app" {
  application_id = azuread_application.app.application_id
}

resource "azuread_application_password" "passkey" {
  application_object_id = azuread_application.app.object_id
}

resource "azurerm_role_assignment" "lake_blob_contributor" {
  scope                = azurerm_storage_account.lake_account.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azuread_service_principal.app.id
}

# databricks
resource "azurerm_databricks_workspace" "databricks_workspace" {
  name                        = var.databricks_workspace_name
  resource_group_name         = azurerm_resource_group.resources.name
  location                    = azurerm_resource_group.resources.location
  sku                         = "premium"
  managed_resource_group_name = var.databricks_managed_resource_group_name
}
