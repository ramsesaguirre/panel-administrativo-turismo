from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'tu_super_clave_secreta'

# Configuración básica
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['MAX_IMAGES'] = 5

# Datos de ejemplo (en producción usarías una base de datos)
posts = [
    {
        'id': 1,
        'title': 'Primer post',
        'description': 'Descripción del primer post',
        'category_id': 1,
        'map_url': 'https://goo.gl/maps/ejemplo',
        'images': ['static/uploads/image1.jpg'],
        'created_at': datetime.now()
    }
]

categories = [
    {'id': 1, 'name': 'Playas'},
    {'id': 2, 'name': 'Montañas'}
]

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('posts/index.html', posts=posts)

@app.route('/posts/create', methods=['GET'])
def create_post():
    return render_template('posts/create.html', categories=categories)

@app.route('/posts/store', methods=['POST'])
def store_post():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        category_id = request.form.get('category_id')
        map_url = request.form.get('map_url')
        
        # Validaciones básicas
        if not title or not description:
            flash('Título y descripción son requeridos', 'error')
            return redirect(url_for('create_post'))
        
        # Procesar imágenes
        images = []
        if 'images' in request.files:
            files = request.files.getlist('images')
            for file in files[:app.config['MAX_IMAGES']]:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    images.append(f"static/uploads/{filename}")
        
        # Crear nuevo post
        new_post = {
            'id': len(posts) + 1,
            'title': title,
            'description': description,
            'category_id': int(category_id) if category_id else None,
            'map_url': map_url,
            'images': images,
            'created_at': datetime.now()
        }
        posts.append(new_post)
        
        flash('Publicación creada exitosamente', 'success')
        return redirect(url_for('index'))

@app.route('/posts/edit/<int:post_id>', methods=['GET'])
def edit_post(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    if not post:
        flash('Publicación no encontrada', 'error')
        return redirect(url_for('index'))
    return render_template('posts/edit.html', post=post, categories=categories)

@app.route('/posts/update/<int:post_id>', methods=['POST'])
def update_post(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    if not post:
        flash('Publicación no encontrada', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        post['title'] = request.form['title']
        post['description'] = request.form['description']
        post['category_id'] = request.form.get('category_id')
        post['map_url'] = request.form.get('map_url')
        
        # Procesar imágenes eliminadas
        removed_images = request.form.getlist('removed_images')
        post['images'] = [img for img in post['images'] if img not in removed_images]
        
        # Procesar nuevas imágenes
        if 'new_images' in request.files:
            files = request.files.getlist('new_images')
            for file in files[:app.config['MAX_IMAGES'] - len(post['images'])]:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    post['images'].append(f"static/uploads/{filename}")
        
        flash('Publicación actualizada exitosamente', 'success')
        return redirect(url_for('index'))

# Rutas para categorías
@app.route('/categories')
def list_categories():
    return render_template('categories/index.html', categories=categories)

@app.route('/categories/create', methods=['GET'])
def create_category():
    return render_template('categories/create.html')

@app.route('/categories/store', methods=['POST'])
def store_category():
    name = request.form.get('name')
    if name:
        new_category = {
            'id': len(categories) + 1,
            'name': name,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        categories.append(new_category)
        flash('Categoría creada exitosamente', 'success')
    else:
        flash('Nombre de categoría es requerido', 'error')
    return redirect(url_for('list_categories'))

@app.route('/categories/edit/<int:category_id>', methods=['GET'])
def edit_category(category_id):
    category = next((c for c in categories if c['id'] == category_id), None)
    if not category:
        flash('Categoría no encontrada', 'error')
        return redirect(url_for('list_categories'))
    return render_template('categories/edit.html', category=category)

@app.route('/categories/update/<int:category_id>', methods=['POST'])
def update_category(category_id):
    category = next((c for c in categories if c['id'] == category_id), None)
    if not category:
        flash('Categoría no encontrada', 'error')
        return redirect(url_for('list_categories'))
    
    name = request.form.get('name')
    if name:
        category['name'] = name
        category['updated_at'] = datetime.now()
        flash('Categoría actualizada exitosamente', 'success')
    else:
        flash('Nombre de categoría es requerido', 'error')
    return redirect(url_for('list_categories'))

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
