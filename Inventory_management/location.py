from flask import Blueprint, request, jsonify
from db import get_db_connection

location_bp = Blueprint('location', __name__)

# Create table for locations
def create_location_table():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS locations (
            l_id VARCHAR(10) PRIMARY KEY,
            l_name VARCHAR(255) NOT NULL
        )
    """)
    db.commit()
    db.close()

# Get the next location ID
def get_next_location_id():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT l_id FROM locations ORDER BY l_id DESC LIMIT 1")
    last = cursor.fetchone()
    if last and last[0]:
        # Extract the numeric part of the last location ID and increment it
        next_id = f'L{int(last[0][1:]) + 1:03d}'  # Remove 'L' and increment the number
    else:
        next_id = 'L001'  # If no records, start from L001
    db.close()
    return next_id



# Route for GET and POST
@location_bp.route('/locations', methods=['GET', 'POST'])
def handle_locations():
    db = get_db_connection()
    cursor = db.cursor()

    if request.method == 'GET':
        cursor.execute("SELECT * FROM locations")
        rows = cursor.fetchall()
        db.close()
        return jsonify([{'l_id': row[0], 'l_name': row[1]} for row in rows])

    # POST request (add a new location)
    data = request.get_json()
    l_name = data.get('l_name')
    if not l_name:
        db.close()
        return jsonify({'error': 'Location name is required'}), 400

    l_id = get_next_location_id()
    cursor.execute("INSERT INTO locations (l_id, l_name) VALUES (%s, %s)", (l_id, l_name))
    db.commit()
    db.close()
    return jsonify({'message': 'Location added', 'l_id': l_id}), 201

# Route for PUT (update a location)
@location_bp.route('/locations/<l_id>', methods=['PUT'])
def update_location(l_id):
    db = get_db_connection()
    cursor = db.cursor()
    data = request.get_json()
    l_name = data.get('l_name')
    if not l_name:
        db.close()
        return jsonify({'error': 'Location name is required'}), 400

    cursor.execute("SELECT * FROM locations WHERE l_id = %s", (l_id,))
    if not cursor.fetchone():
        db.close()
        return jsonify({'error': 'Location not found'}), 404

    cursor.execute("UPDATE locations SET l_name = %s WHERE l_id = %s", (l_name, l_id))
    db.commit()
    db.close()
    return jsonify({'message': f'Location {l_id} updated'})
