import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import html
import mimetypes
from database.repository import PostRepository, CategoryRepository
from database.models import db_service

# Configuración
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class RequestHandler(BaseHTTPRequestHandler):
    def serve_template(self, template_path, context={}):
        try:
            with open(f'templates/{template_path}', 'r', encoding='utf-8') as f:
                content = f.read()
                for key, value in context.items():
                    content = content.replace(f'{{{{ {key} }}}}', str(value))
                return content
        except FileNotFoundError:
            self.send_error(404, "Template not found")
            return None

    def do_GET(self):
        try:
            # Servir archivos estáticos
            if self.path.startswith('/static/'):
                self.serve_static_file()
                return
            
            # Rutas principales
            if self.path == '/':
                posts = PostRepository.get_all_posts()
                content = self.serve_template('posts/index.html', {'posts': posts})
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(content.encode())
                
            elif self.path == '/posts/create':
                categories = CategoryRepository.get_all_categories()
                content = self.serve_template('posts/create.html', {'categories': categories})
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(content.encode())
                
            elif self.path.startswith('/posts/edit/'):
                post_id = int(self.path.split('/')[-1])
                post = PostRepository.get_post_by_id(post_id)
                if not post:
                    self.send_error(404, "Post not found")
                    return
                
                categories = CategoryRepository.get_all_categories()
                content = self.serve_template('posts/edit.html', {
                    'post': post,
                    'categories': categories
                })
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(content.encode())
                
            elif self.path == '/categories':
                categories = CategoryRepository.get_all_categories()
                content = self.serve_template('categories/index.html', {'categories': categories})
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(content.encode())
                
            elif self.path == '/categories/create':
                content = self.serve_template('categories/create.html')
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(content.encode())
                
            elif self.path.startswith('/categories/edit/'):
                category_id = int(self.path.split('/')[-1])
                category = CategoryRepository.get_category_by_id(category_id)
                if not category:
                    self.send_error(404, "Category not found")
                    return
                
                content = self.serve_template('categories/edit.html', {'category': category})
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(content.encode())
                
            else:
                self.send_error(404, "Endpoint not found")
                
        except Exception as e:
            self.send_error(500, f"Server Error: {str(e)}")

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            if self.path == '/posts/store':
                self.handle_create_post(post_data)
            elif self.path.startswith('/posts/update/'):
                post_id = int(self.path.split('/')[-1])
                self.handle_update_post(post_id, post_data)
            elif self.path.startswith('/posts/delete/'):
                post_id = int(self.path.split('/')[-1])
                self.handle_delete_post(post_id)
            elif self.path == '/categories/store':
                self.handle_create_category(post_data)
            elif self.path.startswith('/categories/update/'):
                category_id = int(self.path.split('/')[-1])
                self.handle_update_category(category_id, post_data)
            elif self.path.startswith('/categories/delete/'):
                category_id = int(self.path.split('/')[-1])
                self.handle_delete_category(category_id)
            else:
                self.send_error(404, "Endpoint not found")
                
        except Exception as e:
            self.send_error(500, f"Server Error: {str(e)}")

    def serve_static_file(self):
        try:
            filepath = self.path[1:]  # Remove leading slash
            if not os.path.exists(filepath):
                raise FileNotFoundError
                
            mimetype, _ = mimetypes.guess_type(filepath)
            self.send_response(200)
            self.send_header('Content-type', mimetype or 'application/octet-stream')
            self.end_headers()
            
            with open(filepath, 'rb') as f:
                self.wfile.write(f.read())
        except FileNotFoundError:
            self.send_error(404, "File not found")

    def parse_form_data(self, post_data):
        try:
            params = parse_qs(post_data.decode('utf-8'))
            return {k: v[0] if len(v) == 1 else v for k, v in params.items()}
        except:
            return {}

    def handle_create_post(self, post_data):
        form_data = self.parse_form_data(post_data)
        
        if not form_data.get('title') or not form_data.get('description'):
            self.send_error(400, "Title and description are required")
            return
            
        try:
            post = PostRepository.create_post(
                title=form_data['title'],
                description=form_data['description'],
                category_id=form_data.get('category_id'),
                map_url=form_data.get('map_url'),
                images=[]  # Aquí deberías procesar las imágenes subidas
            )
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
        except Exception as e:
            self.send_error(400, str(e))

    def handle_update_post(self, post_id, post_data):
        form_data = self.parse_form_data(post_data)
        
        try:
            updated_post = PostRepository.update_post(
                post_id=post_id,
                title=form_data.get('title'),
                description=form_data.get('description'),
                category_id=form_data.get('category_id'),
                map_url=form_data.get('map_url')
            )
            if not updated_post:
                self.send_error(404, "Post not found")
                return
                
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
        except Exception as e:
            self.send_error(400, str(e))

    def handle_delete_post(self, post_id):
        try:
            success = PostRepository.delete_post(post_id)
            if not success:
                self.send_error(404, "Post not found")
                return
                
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True}).encode())
        except Exception as e:
            self.send_error(400, str(e))

    def handle_create_category(self, post_data):
        form_data = self.parse_form_data(post_data)
        name = form_data.get('name', '').strip()
        
        if not name:
            self.send_error(400, "Category name is required")
            return
            
        try:
            category = CategoryRepository.create_category(name)
            self.send_response(303)
            self.send_header('Location', '/categories')
            self.end_headers()
        except Exception as e:
            self.send_error(400, str(e))

    def handle_update_category(self, category_id, post_data):
        form_data = self.parse_form_data(post_data)
        name = form_data.get('name', '').strip()
        
        if not name:
            self.send_error(400, "Category name is required")
            return
            
        try:
            category = CategoryRepository.update_category(category_id, name)
            if not category:
                self.send_error(404, "Category not found")
                return
                
            self.send_response(303)
            self.send_header('Location', '/categories')
            self.end_headers()
        except Exception as e:
            self.send_error(400, str(e))

    def handle_delete_category(self, category_id):
        try:
            success = CategoryRepository.delete_category(category_id)
            if not success:
                self.send_error(404, "Category not found")
                return
                
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True}).encode())
        except Exception as e:
            self.send_error(400, str(e))

if __name__ == '__main__':
    # Inicializar la base de datos
    db_service.init_db()
    
    server = HTTPServer(('0.0.0.0', 5000), RequestHandler)
    print("Servidor iniciado en http://0.0.0.0:5000")
    server.serve_forever()
