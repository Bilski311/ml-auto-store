provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "ml-auto-store-rg" {
  name     = "ml-auto-store-rg"
  location = "polandcentral"
}