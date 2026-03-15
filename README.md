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

- El sistema garantiza que no existan pedidos "huérfanos". Se devuelve un **HTTP 400** (Bad Request) con el mensaje específico: {"error": "el artículo con id X no existe."} si se intenta referenciar un ID inexistente.

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
              LADO DE ENTRADA (Driving)              NÚCLEO (Core)             LADO DE SALIDA (Driven)
      
      ┌──────────────────────┐           ┌───────────────────┐          ┌──────────────────────┐
      │     PRESENTATION     │           │    APPLICATION    │          │    INFRASTRUCTURE    │
      │  (Adaptador REST)    │           │   (Casos de Uso)  │          │    (Adaptador DB)    │
      ├──────────────────────┤           ├───────────────────┤          ├──────────────────────┤
      │                      │           │                   │          │                      │
      │  - views.py          │           │  - use_cases.py   │          │  - repositories.py   │
      │  - serializers.py    │ ────────▶ │                   │ ────────▶ │  - models.py (ORM)   │
      │  - urls.py           │           │                   │          │  - migrations/       │
      │                      │           └─────────┬─────────┘          │                      │
      └──────────────────────┘                     │                    └──────────────────────┘
                                                   │
                                         ┌─────────▼─────────┐
                                         │      DOMAIN       │
                                         │ (Reglas de Oro)   │
                                         ├───────────────────┤
                                         │                   │
                                         │  - models.py      │
                                         │    (Entidades)    │
                                         │                   │
                                         └───────────────────┘
```

### Capas del sistema

* **Domain:** Contiene las entidades puras (`Order`, `OrderItem`) y la lógica de cálculo de IVA.
* **Application:** Casos de uso que orquestan las operaciones (ej. `OrderUseCases`).
* **Infrastructure:** Implementación de repositorios con Django ORM y persistencia física.
* **Presentation:** Endpoints REST, Serializers y validación de entrada.

---

# 📁 Estructura del proyecto

```
app/
├── articles/                # Módulo de Gestión de Artículos
│   ├── application/         # Casos de uso (use_cases.py)
│   ├── domain/              # Entidades y lógica pura (models.py)
│   ├── infrastructure/      # Persistencia (models.py, repositories.py, migrations/)
│   └── presentation/        # Entrada/Salida (views.py, serializers.py, urls.py)
│
├── orders/                  # Módulo de Gestión de Pedidos
│   ├── application/         # Casos de uso y lógica de procesamiento
│   ├── domain/              # Lógica de cálculo (IVA 21%, totales)
│   ├── infrastructure/      # Repositorios ORM y migrations/
│   └── presentation/        # API Endpoints y Serializers
│
├── core/                    # Lógica compartida (excepciones y modelos base)
└── tests.py                 # Pruebas unitarias y de integración
│
├── postman/                 # Colección de pruebas para importar
│   └── centribal_api_collection.json
│
├── centribal_project/       # Configuración global de Django
├── docker-compose.yml       # Orquestación de servicios
├── Dockerfile               # Imagen de la aplicación
└── .env.example             # Plantilla de variables de entorno

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
Nota: Se utiliza temporalmente el usuario root para permitir que Django cree la base de datos de pruebas en el contenedor.

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
Se devuelve HTTP 400 con el mensaje {"error": "el artículo con id X no existe."} si se intenta referenciar un artículo inexistente. Esto asegura que no se creen pedidos con datos huérfanos.
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
Request Payload 
{
    "reference": "PROD-001",
    "name": "Monitor Gamer 24 pulgadas",
    "description": "Frecuencia de 144Hz IPS",
    "price_without_tax": 200.0,
    "tax_rate": 21.0
}
Response Payload
{
    "id": 1,
    "reference": "PROD-001",
    "name": "Monitor Gamer 24 pulgadas",
    "description": "Frecuencia de 144Hz IPS",
    "price_without_tax": 200.0,
    "tax_rate": 21.0,
    "created_at": "2026-03-15T02:02:58.267619Z"
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
Request Payload 
[
    {
        "article_id": 1, 
        "quantity": 5
    }
]
Response Payload
  {
    "id": 1,
    "created_at": "2026-03-15T02:03:12.416102Z",
    "items": [
        {
            "reference": "PROD-001",
            "quantity": 5,
            "total_without_tax": 1000.0,
            "total_with_tax": 1210.0
        }
    ],
    "total_price_without_tax": 1000.0,
    "total_price_with_tax": 1210.0
}

Body:
```json
Request Payload 
[
  {
    "article_id": 999,
    "quantity": 1
  }
]
Response Payload
Status: 400 Bad Request
{"error": "el artículo con id 999 no existe."}
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
