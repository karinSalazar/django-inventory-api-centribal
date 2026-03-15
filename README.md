# Centribal Tech Challenge – Order Management API

![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Django](https://img.shields.io/badge/django-%23092E20.svg?logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

REST API desarrollada para la gestión de **artículos y pedidos**.  
El proyecto implementa una **Arquitectura Hexagonal (Ports & Adapters)** que separa la lógica de negocio de los frameworks y de la infraestructura, permitiendo mayor **mantenibilidad, testabilidad y escalabilidad**.

---

# 📌 Tabla de contenidos

- [Objetivos del desafío](#-objetivos-del-desafío)
- [Stack tecnológico](#-stack-tecnológico)
- [Arquitectura](#-arquitectura)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Instalación y ejecución](#-instalación-y-ejecución)
- [Tests](#-tests)
- [Endpoints de la API](#-endpoints-de-la-api)
- [Colección de Postman](#-colección-de-postman)

---

# 🎯 Objetivos del desafío

Este proyecto implementa:

- Persistencia de **artículos** y **pedidos**
- Cálculo automático de **impuestos (IVA 21%)**
- Separación clara entre **lógica de negocio y frameworks**
- Entorno completamente **contenedorizado con Docker**
- Validaciones de integridad de datos

Ejemplo de validación:

- Se devuelve **HTTP 400** si se intenta crear un pedido con **IDs de artículos inexistentes**.

---

# 🛠 Stack tecnológico

| Tecnología | Uso |
|------------|------|
| Python 3.11 | Lenguaje principal |
| Django 5.1 | Framework backend |
| Django Rest Framework | Construcción de API REST |
| MariaDB 10.6 | Base de datos |
| Docker | Contenerización |
| Docker Compose | Orquestación de servicios |

---

# 🏗 Arquitectura

El proyecto utiliza **Arquitectura Hexagonal (Ports & Adapters)**.

Esto permite desacoplar la lógica de negocio de la infraestructura.

```
              ┌─────────────────────┐
              │    Presentation     │
              │  (DRF Controllers)  │
              └──────────┬──────────┘
                         │
              ┌──────────▼──────────┐
              │     Application     │
              │      Use Cases      │
              └──────────┬──────────┘
                         │
              ┌──────────▼──────────┐
              │       Domain        │
              │  Entities & Logic   │
              └──────────┬──────────┘
                         │
              ┌──────────▼──────────┐
              │    Infrastructure   │
              │  ORM / Repositories │
              └─────────────────────┘
```

### Capas del sistema

**Domain**

- Entidades del negocio
- Cálculo de IVA
- Reglas de negocio

**Application**

- Casos de uso
- Orquestación de operaciones

**Infrastructure**

- Implementación de repositorios
- Persistencia con Django ORM
- Conexión a la base de datos

**Presentation**

- Endpoints REST
- Serializers
- Validación de entrada

---

# 📁 Estructura del proyecto

```
project/
│
├── domain/
│   ├── entities
│   └── services
│
├── application/
│   └── use_cases
│
├── infrastructure/
│   ├── repositories
│   └── models
│
├── presentation/
│   ├── api
│   └── serializers
│
├── postman/
│   └── centribal_api_collection.json
│
├── docker-compose.yml
├── Dockerfile
└── manage.py
```

---

# 🚀 Instalación y ejecución

## 1. Clonar repositorio

```bash
git clone <repository_url>
cd centribal-tech-challenge
```

---

## 2. Crear variables de entorno

```bash
cp .env.example .env
```

---

## 3. Levantar contenedores

```bash
docker-compose up -d --build
```

Esto iniciará:

- API Django
- Base de datos MariaDB

---

## 4. Ejecutar migraciones

```bash
docker-compose exec web python manage.py migrate
```

La API estará disponible en:

```
http://localhost:8000/api/
```

---

# 🧪 Tests

El proyecto incluye:

- **Tests unitarios** para la lógica de negocio
- **Tests de integración** para los endpoints

Ejecutar los tests dentro del entorno Docker:

```bash
docker-compose exec -e DB_USER=root -e DB_PASSWORD=root web python manage.py test
```

---

## Validaciones verificadas

### Cálculo de totales

Ejemplo de cálculo:

```
Precio base: 200
IVA (21%): 42
Total: 242
```

### Integridad de pedidos

El sistema valida que todos los artículos del pedido existan en la base de datos.

En caso contrario se devuelve:

```
HTTP 400 - Bad Request
```

---

# 🌐 Endpoints de la API

## Artículos

### Crear artículo

```
POST /api/articles/
```

Body:

```json
{
  "name": "Laptop",
  "price": 1000
}
```

---

### Listar artículos

```
GET /api/articles/
```

---

## Pedidos

### Crear pedido

```
POST /api/orders/
```

Body:

```json
{
  "items": [1, 2, 3]
}
```

El sistema calcula automáticamente:

- subtotal
- IVA
- total

---

### Listar pedidos

```
GET /api/orders/
```

---

# 📬 Colección de Postman

Se incluye una colección lista para importar.

Ruta:

```
postman/centribal_api_collection.json
```

Permite probar rápidamente:

- creación de artículos
- creación de pedidos
- listado de recursos

---

# 📄 Licencia

Este proyecto fue desarrollado como parte de un **technical challenge**.

Uso libre para fines educativos o de evaluación técnica.
