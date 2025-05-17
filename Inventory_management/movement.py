from flask import Blueprint, request, jsonify
from db import get_db_connection

movement_bp = Blueprint('movement', __name__)

def create_product_movements_table():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_movements (
            movement_id VARCHAR(10) PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            from_location VARCHAR(10),
            to_location VARCHAR(10),
            product_id VARCHAR(10),
            qty INT,
            FOREIGN KEY (from_location) REFERENCES locations(l_id) ON DELETE SET NULL,
            FOREIGN KEY (to_location) REFERENCES locations(l_id) ON DELETE SET NULL,
            FOREIGN KEY (product_id) REFERENCES products(p_id) ON DELETE CASCADE
        )
    """)
    db.commit()
    db.close()



# Get next movement ID
def get_next_movement_id():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT movement_id FROM product_movements ORDER BY movement_id DESC LIMIT 1")
    last = cursor.fetchone()

    if last and last[0] is not None:
        next_id = int(last[0]) + 1
    else:
        next_id = 1

    db.close()
    return next_id

# Handle GET for product movements
@movement_bp.route('/movements', methods=['GET'])
def get_product_movements():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        SELECT pm.movement_id, pm.timestamp, l_from.location_name AS from_location, 
               l_to.location_name AS to_location, p.p_name AS product_name, pm.qty
        FROM product_movements pm
        JOIN locations l_from ON pm.from_location = l_from.location_id
        JOIN locations l_to ON pm.to_location = l_to.location_id
        JOIN products p ON pm.product_id = p.p_id
    """)
    movements = cursor.fetchall()
    db.close()

    # Debug log to check what's being fetched
    print("Fetched Movements:", movements)

    return jsonify([{
        'movement_id': row[0],
        'timestamp': row[1],
        'from_location': row[2],
        'to_location': row[3],
        'product_name': row[4],
        'qty': row[5]
    } for row in movements])

# Handle POST to add a product movement
@movement_bp.route('/movements', methods=['POST'])
def add_product_movement():
    data = request.get_json()
    from_location_name = data.get('from_location')
    to_location_name = data.get('to_location')
    product_name = data.get('product_name')
    qty = data.get('qty')

    if not from_location_name or not to_location_name or not product_name or not qty:
        return jsonify({'error': 'All fields (from_location, to_location, product_name, qty) are required'}), 400

    # Get location IDs
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT location_id FROM locations WHERE location_name = %s", (from_location_name,))
    from_location = cursor.fetchone()
    if not from_location:
        db.close()
        return jsonify({'error': f'From location "{from_location_name}" not found'}), 404
    from_location_id = from_location[0]

    cursor.execute("SELECT location_id FROM locations WHERE location_name = %s", (to_location_name,))
    to_location = cursor.fetchone()
    if not to_location:
        db.close()
        return jsonify({'error': f'To location "{to_location_name}" not found'}), 404
    to_location_id = to_location[0]

    # Get product ID
    cursor.execute("SELECT p_id FROM products WHERE p_name = %s", (product_name,))
    product = cursor.fetchone()
    if not product:
        db.close()
        return jsonify({'error': f'Product "{product_name}" not found'}), 404
    product_id = product[0]

    # Insert movement
    movement_id = get_next_movement_id()  # Get the next movement ID
    cursor.execute("""
        INSERT INTO product_movements (movement_id, from_location, to_location, product_id, qty)
        VALUES (%s, %s, %s, %s, %s)
    """, (movement_id, from_location_id, to_location_id, product_id, qty))
    db.commit()
    db.close()
    return jsonify({'message': 'Product movement added'})
