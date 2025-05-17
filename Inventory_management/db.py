import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="Tharunikaa",           # Your MySQL username
        password="Tharunikaa@0112",  # Your MySQL password
        database="new_inventory"     # Your database name
    )
