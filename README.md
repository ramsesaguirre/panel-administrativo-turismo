```markdown
# 🚀 Panel Administrativo de Turismo - Docker Edition

## 1. Requisitos del Sistema
### 🛠️ Tecnologías necesarias
- Docker 20.10+
- Docker Compose 2.0+
- (Opcional) Make para comandos simplificados

## 2. Instalación con Docker (Recomendado)
### 🐳 Pasos iniciales
```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-repositorio/panel-turismo.git
cd panel-turismo

# 2. Construir y ejecutar los contenedores
docker-compose up --build

# 3. Acceder a la aplicación:
http://localhost:5000
```

## 3. Configuración del Entorno
### 🔧 Variables de entorno (.env)
Crea un archivo `.env` en la raíz del proyecto con:
```ini
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=tusuperclavesecreta
DATABASE_URL=postgresql://postgres:example@db:5432/blogdb
UPLOAD_FOLDER=/app/static/uploads
```

## 4. Comandos Útiles
### 🐋 Docker Compose
```bash
# Iniciar servicios (modo desarrollo)
docker-compose up

# Reconstruir imágenes y reiniciar
docker-compose up --build

# Detener servicios
docker-compose down

# Eliminar todo (contenedores + volúmenes)
docker-compose down -v

# Ver logs en tiempo real
docker-compose logs -f web

# Ejecutar comandos dentro del contenedor web
docker-compose exec web flask shell
```

### 🛠️ Comandos Make (opcional)
Si tienes Make instalado, puedes usar estos alias:

```bash
make up      # Iniciar servicios
make down    # Detener servicios
make rebuild # Reconstruir y reiniciar
make logs    # Ver logs
make shell   # Acceder a shell interactiva
```

## 5. Estructura de Servicios
```
Servicio    Puerto      Descripción
-------     ------      -----------
web         5000        Aplicación Flask (desarrollo)
db          5432        PostgreSQL database
```

## 6. Características del Entorno Docker
- ✅ Hot-reloading para desarrollo
- ✅ Base de datos PostgreSQL persistente
- ✅ Volumen para uploads de imágenes
- ✅ Health checks automáticos
- ✅ Variables de entorno configurables

## 7. Solución de Problemas Comunes
### 🔍 Problemas de conexión a la base de datos
```bash
# Verificar estado de la DB
docker-compose exec db pg_isready

# Reintentar conexión
docker-compose restart web
```

### 🐛 Debugging
```bash
# Acceder a los logs
docker-compose logs -f web

# Inspeccionar la DB
docker-compose exec db psql -U postgres -d blogdb
```

## 8. Despliegue en Producción
Para producción, considera:
1. Usar `gunicorn` en lugar de `flask run`
2. Configurar `FLASK_ENV=production`
3. Implementar migraciones de base de datos
4. Configurar un proxy inverso (Nginx)

📌 **Nota**: Esta configuración es solo para desarrollo. No usar en producción sin las debidas modificaciones de seguridad.

## 9. Licencia
📄 MIT License - Copyright (c) 2023 [Tu Nombre]
```
