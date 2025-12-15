
from flask import Flask, jsonify, request
import requests
from db_config import get_db_connection
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# ---------
@app.route("/")
def home():
    return "Customer Service is running!"


@app.route('/api/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
    customer = cursor.fetchone()

    conn.close()

    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    return jsonify(customer), 200



# @app.route('/api/customers/<int:customer_id>/orders', methods=['GET'])
# def get_customer_orders(customer_id):

#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
#     customer = cursor.fetchone()
#     conn.close()

#     if not customer:
#         return jsonify({"error": "Customer not found"}), 404


#     try:
#         response = requests.get(f"http://localhost:5001/api/orders/{customer_id}")
#     except:
#         return jsonify({"error": "Order Service unavailable"}), 503

#     if response.status_code != 200:
#         return jsonify({"error": "Order Service error"}), 500

#     orders = response.json()

 
#     return jsonify({
#         "customer": {
#             "customer_id": customer["id"],
#             "name": customer["name"],
#             "email": customer["email"]
#         },
#         "orders": orders
#     }), 200



@app.route('/api/customers/<int:customer_id>/loyalty', methods=['PUT'])
def update_loyalty(customer_id):
    body = request.get_json()

    if not body or "points" not in body:
        return jsonify({"error": "Missing 'points' field"}), 400

    new_points = body["points"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)


    cursor.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
    customer = cursor.fetchone()

    if not customer:
        conn.close()
        return jsonify({"error": "Customer not found"}), 404

    update_query = """
        UPDATE customers 
        SET loyalty_points = loyalty_points + %s 
        WHERE id = %s
    """
    cursor.execute(update_query, (new_points, customer_id))
    conn.commit()
    conn.close()

    return jsonify({
        "message": "Loyalty points updated successfully",
        "customer_id": customer_id,
        "added_points": new_points
    }), 200


if __name__ == "__main__":
    app.run(port=5004, debug=True)
