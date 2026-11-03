from flask import Blueprint, jsonify, request

from . import get_db

bp = Blueprint('products', __name__)


@bp.get('/')
def home():
    return jsonify(
        {
            'name': 'OpenShift CI/CD Pipeline – Product Catalogue Application',
            'version': '1.0.0',
            'status': 'running',
        }
    )


@bp.get('/health')
def health():
    try:
        database = get_db()
        database.execute('SELECT 1').fetchone()
        db_status = 'connected'
    except Exception:
        db_status = 'disconnected'
    return jsonify({'status': 'ok', 'database': db_status}), 200 if db_status == 'connected' else 503


@bp.get('/api/products')
def list_products():
    rows = get_db().execute(
        'SELECT id, name, description, price, category FROM products ORDER BY id ASC'
    ).fetchall()
    return jsonify(
        [
            {
                'id': row['id'],
                'name': row['name'],
                'description': row['description'],
                'price': float(row['price']),
                'category': row['category'],
            }
            for row in rows
        ]
    )


@bp.get('/api/products/<int:product_id>')
def get_product(product_id):
    row = get_db().execute(
        'SELECT id, name, description, price, category FROM products WHERE id = ?',
        (product_id,),
    ).fetchone()
    if row is None:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify({
        'id': row['id'],
        'name': row['name'],
        'description': row['description'],
        'price': float(row['price']),
        'category': row['category'],
    })


@bp.post('/api/products')
def create_product():
    payload = request.get_json(silent=True) or {}
    if not isinstance(payload, dict):
        return jsonify({'error': 'Request body must be a JSON object'}), 400

    name = payload.get('name')
    description = payload.get('description', '')
    price = payload.get('price')
    category = payload.get('category')

    if not isinstance(name, str) or not name.strip():
        return jsonify({'error': 'Product name is required'}), 400
    if not isinstance(category, str) or not category.strip():
        return jsonify({'error': 'Product category is required'}), 400
    if not isinstance(price, (int, float)) or float(price) <= 0:
        return jsonify({'error': 'Price must be a positive number'}), 400

    database = get_db()
    cursor = database.execute(
        'INSERT INTO products (name, description, price, category) VALUES (?, ?, ?, ?)',
        (name.strip(), description.strip(), float(price), category.strip()),
    )
    database.commit()
    product_id = cursor.lastrowid
    row = database.execute(
        'SELECT id, name, description, price, category FROM products WHERE id = ?',
        (product_id,),
    ).fetchone()
    return jsonify({
        'id': row['id'],
        'name': row['name'],
        'description': row['description'],
        'price': float(row['price']),
        'category': row['category'],
    }), 201


@bp.put('/api/products/<int:product_id>')
def update_product(product_id):
    payload = request.get_json(silent=True) or {}
    if not isinstance(payload, dict):
        return jsonify({'error': 'Request body must be a JSON object'}), 400

    existing = get_db().execute(
        'SELECT id FROM products WHERE id = ?',
        (product_id,),
    ).fetchone()
    if existing is None:
        return jsonify({'error': 'Product not found'}), 404

    name = payload.get('name')
    description = payload.get('description')
    price = payload.get('price')
    category = payload.get('category')

    database = get_db()
    current = database.execute(
        'SELECT name, description, price, category FROM products WHERE id = ?',
        (product_id,),
    ).fetchone()

    updated_name = name.strip() if isinstance(name, str) and name.strip() else current['name']
    updated_description = description.strip() if isinstance(description, str) else current['description']
    updated_category = category.strip() if isinstance(category, str) and category.strip() else current['category']
    updated_price = float(price) if isinstance(price, (int, float)) and float(price) > 0 else float(current['price'])

    if not updated_name or not updated_category:
        return jsonify({'error': 'Product name and category cannot be empty'}), 400

    database.execute(
        'UPDATE products SET name = ?, description = ?, price = ?, category = ? WHERE id = ?',
        (updated_name, updated_description, updated_price, updated_category, product_id),
    )
    database.commit()

    row = database.execute(
        'SELECT id, name, description, price, category FROM products WHERE id = ?',
        (product_id,),
    ).fetchone()
    return jsonify({
        'id': row['id'],
        'name': row['name'],
        'description': row['description'],
        'price': float(row['price']),
        'category': row['category'],
    })


@bp.delete('/api/products/<int:product_id>')
def delete_product(product_id):
    database = get_db()
    row = database.execute('SELECT id FROM products WHERE id = ?', (product_id,)).fetchone()
    if row is None:
        return jsonify({'error': 'Product not found'}), 404
    database.execute('DELETE FROM products WHERE id = ?', (product_id,))
    database.commit()
    return jsonify({'message': 'Product deleted successfully', 'id': product_id})


def register_routes(app):
    app.register_blueprint(bp)
