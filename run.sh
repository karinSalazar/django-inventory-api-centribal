#!/bin/bash

# Colores para la terminal
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}1. Levantando contenedores...${NC}"
docker-compose up -d

echo -e "${GREEN}2. Ejecutando migraciones...${NC}"
docker-compose exec web python manage.py makemigrations articles orders
docker-compose exec web python manage.py migrate

echo -e "${GREEN}3. Ejecutando tests unitarios...${NC}"
docker-compose exec web python manage.py test app.orders

echo -e "${GREEN}¡Todo listo! La API está corriendo en http://localhost:8000${NC}"