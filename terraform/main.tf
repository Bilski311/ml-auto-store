provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "ml_auto_store_rg" {
  name     = "ml-auto-store-rg"
  location = "polandcentral"
}

resource "azurerm_storage_account" "storage_account" {
  name                     = "autostore"
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

  identity {
    type = "SystemAssigned"
  }
}