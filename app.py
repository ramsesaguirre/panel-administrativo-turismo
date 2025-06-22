from flask import Flask, send_from_directory
import os

app = Flask(__name__, static_folder=None)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Servir archivos estáticos de Vite
@app.route('/assets/<path:filename>')
def serve_vite_assets(filename):
    return send_from_directory('dist/assets', filename)

# Catch-all route para SPA
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_spa(path):
    if path and os.path.exists(os.path.join('dist', path)):
        return send_from_directory('dist', path)
    return send_from_directory('dist', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
