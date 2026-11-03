import os
import sqlite3

from flask import Flask, g

DATABASE_PATH = os.environ.get('DATABASE_PATH', os.path.join('/tmp', 'product_catalog.db'))


def get_db():
    if 'db' not in g:
        connection = sqlite3.connect(DATABASE_PATH)
        connection.row_factory = sqlite3.Row
        g.db = connection
    return g.db


def init_db():
    database = get_db()
    database.execute(
        '''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            category TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    database.execute('SELECT COUNT(*) FROM products').fetchone()

    if database.execute('SELECT COUNT(*) FROM products').fetchone()[0] == 0:
        products = [
            ('Laptop Pro 14', 'Thin ultraportable business laptop', 1299.99, 'Electronics'),
            ('CloudSync Backpack', 'Water-resistant travel backpack', 79.0, 'Accessories'),
            ('Developer Keyboard', 'Mechanical keyboard for coding', 149.5, 'Accessories'),
        ]
        database.executemany(
            'INSERT INTO products (name, description, price, category) VALUES (?, ?, ?, ?)',
            products,
        )
    database.commit()


app = Flask(__name__)
app.config['DATABASE_PATH'] = DATABASE_PATH

from .routes import register_routes  # noqa: E402

register_routes(app)


@app.teardown_appcontext
def close_db(exception):
    database = g.pop('db', None)
    if database is not None:
        database.close()


with app.app_context():
    init_db()
