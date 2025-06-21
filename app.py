import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import html
import mimetypes
from werkzeug.security import safe_join
from database.repository import PostRepository, CategoryRepository
from database.models import db_service

# Configuración
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200, content_type='text/html'):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def serve_template(self, template_path, context={}):
        try:
            template_path = safe_join('templates', template_path)
            if not template_path:
                raise ValueError("Invalid template path")
                
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
                for key, value in context.items():
                    content = content.replace(f'{{{{ {key} }}}}', html.escape(str(value)))
                return content
        except (FileNotFoundError, ValueError, PermissionError) as e:
            self.send_error(404, "Template not found")
            return None

    def serve_static_file(self):
        try:
            filepath = safe_join('.', self.path[1:])
            if not filepath or not os.path.exists(filepath) or not os.path.isfile(filepath):
                raise FileNotFoundError
                
            mimetype, _ = mimetypes.guess_type(filepath)
            self._set_headers(200, mimetype or 'application/octet-stream')
            
            with open(filepath, 'rb') as f:
                self.wfile.write(f.read())
        except (FileNotFoundError, ValueError, PermissionError) as e:
            self.send_error(404, "File not found")

    def parse_form_data(self, post_data):
        try:
            params = parse_qs(post_data.decode('utf-8'), keep_blank_values=False)
            return {k: html.escape(v[0]) if len(v) == 1 else [html.escape(i) for i in v] 
                   for k, v in params.items()}
        except Exception as e:
            self.send_error(400, "Invalid form data")
            return {}

    def handle_create_post(self, post_data):
        form_data = self.parse_form_data(post_data)
        
        if not form_data.get('title') or not form_data.get('description'):
            self.send_error(400, "Title and description are required")
            return
            
        try:
            images = []
            if 'images' in form_data:
                if isinstance(form_data['images'], list):
                    for img in form_data['images']:
                        if not img.filename or '.' not in img.filename:
                            raise ValueError("Invalid filename")
                        ext = img.filename.rsplit('.', 1)[1].lower()
                        if ext not in ALLOWED_EXTENSIONS:
                            raise ValueError("Invalid file extension")
                        if len(img.file.read()) > MAX_FILE_SIZE:
                            raise ValueError("File too large")
                        img.file.seek(0)
                        
                        # Guardar archivo
                        filename = f"{uuid.uuid4().hex}.{ext}"
                        filepath = safe_join(UPLOAD_FOLDER, filename)
                        with open(filepath, 'wb') as f:
                            f.write(img.file.read())
                        images.append(filename)
                        
            post = PostRepository.create_post(
                title=form_data['title'],
                description=form_data['description'],
                category_id=int(form_data.get('category_id', 0)) if form_data.get('category_id') else None,
                map_url=form_data.get('map_url', ''),
                images=images
            )
            self._set_headers(303)
            self.send_header('Location', '/')
            self.end_headers()
        except Exception as e:
            self.send_error(400, str(e))

    def do_GET(self):
        if self.path.startswith('/static/'):
            self.serve_static_file()
            return
            
        try:
            if self.path == '/':
                posts = PostRepository.get_all_posts()
                content = self.serve_template('posts/index.html', {'posts': posts})
                if content:
                    self._set_headers()
                    self.wfile.write(content.encode())
            
            # ... (otros endpoints GET)

        except Exception as e:
            self.send_error(500, f"Server Error: {str(e)}")

    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                raise ValueError("Empty request body")
                
            post_data = self.rfile.read(content_length)
            
            if self.path == '/posts/store':
                self.handle_create_post(post_data)
            # ... (otros endpoints POST)
            
        except Exception as e:
            self.send_error(400, str(e))

if __name__ == '__main__':
    db_service.init_db()
    server = HTTPServer(('0.0.0.0', 5000), RequestHandler)
    print("Servidor iniciado en http://0.0.0.0:5000")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print("Servidor detenido")
