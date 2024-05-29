variable "tag" {
  type        = string
  description = "tag all resources created."
}

variable "resource_group_name" {
  type        = string
  description = "resource group name"
}

variable "location" {
  type        = string
  description = "location to deploying the resources"
}

# lake
variable "lake_account_name" {
  type        = string
  description = "storage account name for the storage that will be used as a data lake"
}

variable "lake_container_name" {
  type        = string
  description = "name for lake storage container"
}

variable "lake_container_access_type" {
  type        = string
  description = "access type for lake container"
}

variable "app_name" {
  type        = string
  description = "name given to a newly registered app"
}

variable "databricks_workspace_name" {
  type        = string
  description = "name given to the created databricks workspace"
}

variable "databricks_managed_resource_group_name" {
  type        = string
  description = "name of the resource group holding the resources for the databricks workspace compute."
}