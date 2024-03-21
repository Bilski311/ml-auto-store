provider "azurerm" {
  features {}
}

terraform {
  backend "azurerm" {
    resource_group_name   =  "terraform-rg"
    storage_account_name  =  "terraformstate321"
    container_name        =  "terraform-state-container"
    key                   =  "terraform.tfstate"
  }
}

resource "azurerm_resource_group" "ml_auto_store_rg" {
  name     = "ml-auto-store-rg"
  location = "polandcentral"
}

resource "azurerm_storage_account" "storage_account" {
  name                     = "autostore321"
  resource_group_name      = azurerm_resource_group.ml_auto_store_rg.name
  location                 = azurerm_resource_group.ml_auto_store_rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "storage_container" {
  name                  = "ml-auto-store-container"
  storage_account_name  = azurerm_storage_account.storage_account.name
  container_access_type = "private"
}

resource "azurerm_machine_learning_workspace" "ml_auto_store_workspace" {
  name                    = "ml-auto-store-workspace"
  location                = azurerm_resource_group.ml_auto_store_rg.location
  resource_group_name     = azurerm_resource_group.ml_auto_store_rg.name
  storage_account_id      = azurerm_storage_account.storage_account.id
  application_insights_id = azurerm_application_insights.app_insights.id
  key_vault_id            = azurerm_key_vault.key_vault.id

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_key_vault" "key_vault" {
  name                = "autoStoreKv"
  location            = azurerm_resource_group.ml_auto_store_rg.location
  resource_group_name = azurerm_resource_group.ml_auto_store_rg.name
  tenant_id           = var.tenant_id
  sku_name            = "standard"
}

resource "azurerm_log_analytics_workspace" "log_analytics_workspace" {
  name                = "autoStoreAnalyticsWorkspace"
  location            = azurerm_resource_group.ml_auto_store_rg.location
  resource_group_name = azurerm_resource_group.ml_auto_store_rg.name
  sku                 = "PerGB2018"
}

resource "azurerm_application_insights" "app_insights" {
  name                = "autoStoreAppInsights"
  location            = azurerm_resource_group.ml_auto_store_rg.location
  resource_group_name = azurerm_resource_group.ml_auto_store_rg.name
  workspace_id        = azurerm_log_analytics_workspace.log_analytics_workspace.id
  application_type    = "web"
}