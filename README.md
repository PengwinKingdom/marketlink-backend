# MarketLink – Backend API (Flask + MongoDB)

Este repositorio contiene la API backend de MarketLink, desarrollada con Flask 3, Python 3.10 y conectada a MongoDB 7 mediante PyMongo.
La API permite gestionar usuarios a través de operaciones CRUD y se despliega en contenedores Docker.

---

# Instalación y ejecución con Docker

- Clonar repositorio:
```
git clone
cd marketlink-backend
```

- Configurar variables de entorno:
  
  utiliza .env
  
  
- Ejecutar backend + MongoDB:

```
docker compose up --build
```

- La API estará disponible en:
```
http://localhost:5000
```
