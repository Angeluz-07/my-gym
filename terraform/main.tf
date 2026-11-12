# 1. Configuración de Terraform y Proveedor
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# 2. Grupo de Recursos
resource "azurerm_resource_group" "rg_mygym" {
  name     = "rg-${var.project_name}"
  location = var.location
}

# 3. Log Analytics (Requerido por Container Apps)
resource "azurerm_log_analytics_workspace" "logs" {
  name                = "log-${var.project_name}"
  location            = azurerm_resource_group.rg_mygym.location
  resource_group_name = azurerm_resource_group.rg_mygym.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

# 4. Entorno de Container Apps
resource "azurerm_container_app_environment" "env" {
  name                       = "env-${var.project_name}"
  location                   = azurerm_resource_group.rg_mygym.location
  resource_group_name        = azurerm_resource_group.rg_mygym.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.logs.id
  timeouts {
    delete = "60m" # Le damos hasta 1 hora para evitar el corte por deadline
  }
}

# 5. Aplicación Django en Container App
resource "azurerm_container_app" "api" {
  name                         = "app-${var.project_name}"
  container_app_environment_id = azurerm_container_app_environment.env.id
  resource_group_name          = azurerm_resource_group.rg_mygym.name
  revision_mode                = "Single"

  template {
    container {
      name   = "django-app"
      image  = var.docker_image
      cpu    = 0.25
      memory = "0.5Gi"

      # Inyección de variables de entorno hacia tu contenedor
      env {
        name  = "POSTGRES_URI"
        value = var.database_url # URL de Supabase protegida o pasada por variable
      }

      env {
        name  = "DJANGO_SECRET_KEY"
        value = var.django_secret_key
      }
    }

    min_replicas = 0
    max_replicas = 1
  }

  ingress {
    external_enabled = true
    target_port      = var.container_port
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }
}

# 6. Outputs esenciales
output "app_url" {
  description = "URL pública de tu aplicación Django en Azure Container Apps"
  value       = "https://${azurerm_container_app.api.latest_revision_fqdn}"
}