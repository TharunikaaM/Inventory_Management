from flask import Flask, Blueprint, request, jsonify
from db import get_db_connection

product_bp = Blueprint('product', __name__)

# 1. Create product table
def create_product_table():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            p_id VARCHAR(10) PRIMARY KEY,
            p_name VARCHAR(255) NOT NULL
        )
    """)
    db.commit()
    db.close()

# 2. Get next product ID
def get_next_product_id():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT p_id FROM products ORDER BY p_id DESC LIMIT 1")
    last = cursor.fetchone()
    if last:
        last_num = int(last[0][1:])  # strip 'P' and convert to int
        next_id = f'P{last_num + 1:03d}'
    else:
        next_id = 'P001'
    db.close()
    return next_id

# 3. Handle GET and POST for products
@product_bp.route('/', methods=['GET', 'POST'])
def handle_products():
    db = get_db_connection()
    cursor = db.cursor()
    
    if request.method == 'GET':
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        db.close()
        return jsonify([{'p_id': row[0], 'p_name': row[1]} for row in products])
    
    elif request.method == 'POST':
        data = request.get_json()
        p_name = data.get('p_name')
        if not p_name:
            db.close()
            return jsonify({'error': 'Product name is required'}), 400

        p_id = get_next_product_id()
        cursor.execute("INSERT INTO products (p_id, p_name) VALUES (%s, %s)", (p_id, p_name))
        db.commit()
        db.close()
        return jsonify({'message': 'Product added', 'p_id': p_id})

# 4. Handle PUT to update a product
@product_bp.route('/<p_id>', methods=['PUT'])
def update_product(p_id):
    db = get_db_connection()
    cursor = db.cursor()
    data = request.get_json()
    p_name = data.get('p_name')
    if not p_name:
        db.close()
        return jsonify({'error': 'Product name is required'}), 400

    cursor.execute("SELECT * FROM products WHERE p_id = %s", (p_id,))
    if not cursor.fetchone():
        db.close()
        return jsonify({'error': 'Product not found'}), 404

    cursor.execute("UPDATE products SET p_name = %s WHERE p_id = %s", (p_name, p_id))
    db.commit()
    db.close()
    return jsonify({'message': f'Product {p_id} updated'})
