```markdown
# 📝 Sistema de Blog - Manual de Instalación y Uso

## 1. Requisitos del Sistema
### 🛠️ Tecnologías necesarias
- Docker 20.10+ y Docker Compose 1.29+
- Node.js v16+ (requerido)
- Python 3.8+ (requerido)
- PostgreSQL 13+ (para desarrollo local)

## 2. Instalación con Docker (Recomendado)
### 🐳 Pasos de despliegue
```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-repositorio/blog-system.git

# 2. Navegar al directorio del proyecto
cd blog-system

# 3. Construir y ejecutar contenedores
docker-compose up --build

# 4. Acceder a:
- Frontend: http://localhost:3000
- API: http://localhost:5000
- Adminer (DB GUI): http://localhost:8080
```

## 3. Configuración de Entorno
### 🔧 Variables de entorno (.env)
```ini
DEBUG=True
DATABASE_URL=postgresql://postgres:example@db:5432/blogdb
SECRET_KEY=tusuperclavesecreta
UPLOAD_FOLDER=static/uploads
ALLOWED_EXTENSIONS=png,jpg,jpeg,gif
```

## 4. Estructura del Proyecto
```
blog-system/
├── docker-compose.yaml       # Configuración de servicios
├── Dockerfile                # Configuración de la imagen principal
├── nginx.conf               # Configuración de Nginx
├── app.py                   # Servidor principal (Python)
├── src/
│   ├── main.js              # Punto de entrada frontend
│   └── styles/              # Estilos SCSS
├── static/
│   ├── css/                 # CSS compilado
│   └── js/                  # JavaScript
├── templates/               # Plantillas HTML
│   ├── base.html            # Layout principal
│   └── ...                  # Otras plantillas
├── database/                # Modelos y repositorios
├── package.json             # Dependencias frontend
└── requirements.txt         # Dependencias backend
```

## 5. Comandos Útiles
### 🐋 Docker
```bash
# Reconstruir imágenes
docker-compose build

# Ver logs en tiempo real
docker-compose logs -f

# Eliminar todo (contenedores + volúmenes)
docker-compose down -v
```

### 🛠️ Desarrollo
```bash
# Instalar dependencias
npm install && pip install -r requirements.txt

# Ejecutar servidor de desarrollo
npm run dev  # Frontend
python app.py  # Backend
```

## 6. Características Principales
- ✅ Autenticación de usuarios
- ✅ CRUD de publicaciones
- ✅ Gestión de categorías
- ✅ Subida de imágenes
- ✅ Integración con Google Maps
- ✅ Diseño responsive con Bootstrap 5

## 7. Solución de Problemas
### 🔍 Errores comunes
- **"Port already in use"**  
  `sudo lsof -i :3000 && kill -9 <PID>`
- **"Database connection failed"**  
  Verificar DATABASE_URL en .env
- **"Module not found"**  
  Reinstalar dependencias: `npm install && pip install -r requirements.txt`

## 8. Licencia
📄 MIT License - Copyright (c) 2023 [Tu Nombre]

Última actualización: `2023-11-15`
```
