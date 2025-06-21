============================================
SISTEMA DE BLOG - MANUAL DE INSTALACIÓN Y USO
============================================

1. REQUISITOS DEL SISTEMA
-------------------------
- Docker 20.10+ y Docker Compose 1.29+
- Opcional: Node.js v16+ y Python 3.8+ para desarrollo local

2. INSTALACIÓN CON DOCKER (RECOMENDADO)
---------------------------------------
1. Clonar el repositorio
2. Navegar al directorio del proyecto:
   cd /ruta/al/proyecto
3. Construir y ejecutar contenedores:
   docker-compose up --build
4. Acceder en:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - PostgreSQL: localhost:5432

3. MODO DESARROLLO LOCAL
------------------------
3.1 Configurar entorno:
   npm install
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

3.2 Ejecutar:
   # Terminal 1 (backend):
   python app.py
   # Terminal 2 (frontend):
   npm run start

4. COMANDOS ÚTILES DOCKER
-------------------------
- Reiniciar servicios: docker-compose restart
- Ver logs: docker-compose logs -f
- Detener contenedores: docker-compose down
- Limpiar volúmenes: docker-compose down -v

5. ESTRUCTURA DE ARCHIVOS
-------------------------
/
├── docker-compose.yaml  # Configuración multi-contenedor
├── Dockerfile           # Configuración imagen principal
├── nginx.conf          # Configuración proxy inverso
├── app.py              # Servidor principal
├── static/
│   ├── css/
│   │   ├── bootstrap.min.css
│   │   ├── bootstrap-icons.css
│   │   └── styles.css
│   └── js/
│       ├── bootstrap.bundle.min.js
│       ├── sweetalert2.min.js
│       └── main.js
└── templates/
    └── base.html
└── (resto de estructura...)

6. SOLUCIÓN DE PROBLEMAS
------------------------
6.1 Problemas comunes Docker:
- "Port already in use": 
  Detener otros servicios usando los puertos 3000/5000/5432
- "Build failed":
  Ejecutar: docker-compose build --no-cache
- Problemas de permisos:
  sudo chown -R $USER:$USER .

7. LICENCIA
-----------
Este proyecto está bajo licencia MIT.

Última actualización: {fecha}
