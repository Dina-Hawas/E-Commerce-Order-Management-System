from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error
from db_config import DB_CONFIG
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# ---------------------------
#  DATABASE CONNECTION
# ---------------------------
def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print("DB connection error:", e)
        return None

@app.route('/')
def home():
    return "Inventory Service (Phase 2) is running!"

# ---------------------------
#  GET INVENTORY DETAILS
# ---------------------------
@app.route('/api/inventory/check/<int:product_id>', methods=['GET'])
def check_inventory(product_id):
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT id, product_name, quantity_available, unit_price
            FROM inventory 
            WHERE id = %s
        """
        cursor.execute(query, (product_id,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row:
            return jsonify({
                "product_id": row["id"],
                "product_name": row["product_name"],
                "unit_price": row["unit_price"],
                "quantity_available": row["quantity_available"]
            })
        else:
            return jsonify({"error": "Product not found"}), 404

    except Error as e:
        return jsonify({"error": f"MySQL Error: {str(e)}"}), 500


# ---------------------------
#  UPDATE INVENTORY (PUT)
# ---------------------------
@app.route('/api/inventory/update/<int:product_id>', methods=['PUT'])
def update_inventory(product_id):
    try:
        data = request.get_json()

        # Validate JSON body
        if not data or "quantity_available" not in data:
            return jsonify({"error": "quantity_available is required"}), 400

        qty = data["quantity_available"]
        if not isinstance(qty, int) or qty < 0:
            return jsonify({"error": "quantity_available must be a positive integer"}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()

        query = """
            UPDATE inventory 
            SET quantity_available = %s
            WHERE id = %s
        """
        cursor.execute(query, (qty, product_id))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "status": "updated",
            "product_id": product_id,
            "quantity_available": qty
        }), 200

    except Error as e:
        return jsonify({"error": f"MySQL Error: {str(e)}"}), 500

# -------------------------------
# GET ALL PRODUCTS
# -------------------------------
@app.route('/api/inventory/all', methods=['GET'])
def get_all_inventory():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT id,
                   product_name,
                   quantity_available,
                   unit_price
            FROM inventory
        """
        cursor.execute(query)
        products = cursor.fetchall()

        return jsonify(products), 200

    except Exception as e:
        return jsonify({
            "error": "Failed to fetch inventory",
            "details": str(e)
        }), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# ---------------------------
#  ENDPOINT FOR ORDER SERVICE
# ---------------------------
@app.route('/api/inventory/validate', methods=['POST'])
def validate_multiple_products():
    """
    This is used when Order Service wants to check multiple products at once
    Example request:
    {
        "items": [
            {"product_id": 1, "quantity": 2},
            {"product_id": 3, "quantity": 1}
        ]
    }
    """
    try:
        data = request.get_json()
        items = data.get("items", [])

        if not items:
            return jsonify({"error": "items list is required"}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor(dictionary=True)

        results = []
        for item in items:
            query = """
                SELECT id, product_name, quantity_available, unit_price
                FROM inventory
                WHERE id = %s
            """
            cursor.execute(query, (item["product_id"],))
            row = cursor.fetchone()

            if not row:
                results.append({
                    "product_id": item["product_id"],
                    "status": "not_found"
                })
            else:
                if row["quantity_available"] >= item["quantity"]:
                    results.append({
                        "product_id": row["id"],
                        "status": "ok",
                        "product_name": row["product_name"],
                        "unit_price": row["unit_price"],
                        "quantity_available": row["quantity_available"]
                    })
                else:
                    results.append({
                        "product_id": row["id"],
                        "status": "out_of_stock",
                        "available": row["quantity_available"]
                    })

        cursor.close()
        conn.close()
        return jsonify(results), 200

    except Error as e:
        return jsonify({"error": f"MySQL Error: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(port=5002, debug=True)
