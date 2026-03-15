# Centribal Backend Test - API de Gestión de Pedidos

Esta es una REST API desarrollada en **Python 3.11** utilizando **Django** y **Django Rest Framework**, diseñada bajo los principios de **Arquitectura Hexagonal** (Puertos y Adaptadores) para asegurar un desacoplamiento total entre la lógica de negocio y la infraestructura.

## 🚀 Requisitos Técnicos
* **Lenguaje:** Python 3.11
* **Framework:** Django 4.2+
* **Arquitectura:** Hexagonal (Dominio, Aplicación, Infraestructura, Presentación)
* **Base de Datos:** MariaDB 10.6
* **Contenedores:** Docker & Docker Compose

---

## 🛠️ Instalación y Ejecución con Docker

Para levantar el entorno de desarrollo (API + Base de datos), sigue estos pasos:

1. **Construir y levantar los contenedores:**
   ```bash
   docker-compose up --build