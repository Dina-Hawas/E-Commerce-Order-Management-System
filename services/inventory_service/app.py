from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error
from db_config import DB_CONFIG

app = Flask(__name__)

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print("DB connection error:", e)
        return None

@app.route('/')
def home():
    return "Inventory Service is running!"

@app.route('/api/inventory/check/<int:product_id>', methods=['GET'])
def check_inventory(product_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "DB connection failed"}), 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, product_name, quantity_available, unit_price FROM inventory WHERE id = %s", (product_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        return jsonify(row)
    return jsonify({"error": "product not found"}), 404

@app.route('/api/inventory/update/<int:product_id>', methods=['POST'])
def update_inventory(product_id):
    data = request.get_json()
    qty = data.get("quantity_available")
    if qty is None:
        return jsonify({"error": "quantity_available required"}), 400
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "DB connection failed"}), 500
    cursor = conn.cursor()
    cursor.execute("UPDATE inventory SET quantity_available = %s WHERE id = %s", (qty, product_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"status": "updated", "product_id": product_id, "quantity_available": qty})

if __name__ == '__main__':
    app.run(port=5002, debug=True)
