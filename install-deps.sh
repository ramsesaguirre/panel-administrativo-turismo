#!/bin/bash
echo "Instalando dependencias JavaScript..."
npm install --save \
  sweetalert2@latest \
  leaflet@latest \
  moment@latest \
  bootstrap@latest \
  vite@latest

echo "Instalando dependencias de desarrollo..."
npm install --save-dev @types/leaflet@latest

echo "Dependencias instaladas correctamente"
