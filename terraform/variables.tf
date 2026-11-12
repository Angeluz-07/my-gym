variable "project_name" {
  description = "Nombre base para los recursos"
  type        = string
}

variable "location" {
  description = "Región de Azure donde se desplegarán los recursos"
  type        = string
}

variable "docker_image" {
  description = "Imagen de Docker para la API"
  type        = string
}

variable "container_port" {
  description = "Puerto en el que escucha la aplicación"
  type        = number
  default     = 8000
}

variable "django_secret_key" {
  description = "django secret key"
  type        = string
}


variable "database_url" {
  description = "database uri"
  type        = string
}
