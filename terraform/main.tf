provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "ml-auto-store-rg" {
  name     = "ml-auto-store-rg"
  location = "polandcentral"
}

resource "azurerm_storage_account" "storage_account" {
  name                     = "ml-auto-store-storage-account"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "storage_container" {
  name                  = "ml-auto-store-container"
  storage_account_name  = azurerm_storage_account.storage_account.name
  container_access_type = "private"
}