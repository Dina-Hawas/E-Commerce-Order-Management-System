from flask import Flask, request, jsonify
import mysql.connector
import mysql
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# ---------

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="enas1234",
    database="ecommerce_system"
)
cursor = db.cursor(dictionary=True)
@app.route("/", methods=["GET"])
def home():
    return "Notify Service is running on port 5005!"

@app.route("/api/notify/test", methods=["GET"])
def test_order():
    return jsonify({"message": "Order service test OK"}), 200

# main endpointss
@app.route("/api/notifications/send", methods=["POST"])
def send_notification():
    data = request.get_json()
    order_id = data.get("order_id")
    customer_id = data.get("customer_id")

    if not order_id or not customer_id:
        return jsonify({"error": "Missing parameters"}), 400

    # ---- Get customer ----
    customer_res = requests.get(
        f"http://localhost:5004/api/customers/{customer_id}"
    )
    if customer_res.status_code != 200:
        return jsonify({"error": "Customer not found"}), 404

    customer_data = customer_res.json()

    # ---- Get order ----
    order_res = requests.get(
        f"http://localhost:5001/api/orders/{order_id}"
    )
    if order_res.status_code != 200:
        return jsonify({"error": "Order not found"}), 404

    order_data = order_res.json()

    # ---- Handle MULTIPLE products ----
    product_lines = []

    for item in order_data["products"]:
        product_id = item["product_id"]
        ordered_qty = item["quantity"]

        inventory_res = requests.get(
            f"http://localhost:5002/api/inventory/check/{product_id}"
        )

        if inventory_res.status_code != 200:
            available_qty = "Unknown"
        else:
            available_qty = inventory_res.json().get("quantity_available")

        product_lines.append(
            f"Product {product_id}: ordered {ordered_qty}, available {available_qty}"
        )

    # ---- Build notification message ----
    message = (
        f"Order #{order_id} confirmed\n"
        f"Customer: {customer_data['name']}\n"
        f"Email: {customer_data['email']}\n"
        f"Products:\n" +
        "\n".join(product_lines)
    )

    # ---- Store notification ----
    cursor.execute(
        "INSERT INTO notification_log (customer_id, message) VALUES (%s, %s)",
        (customer_id, message)
    )
    db.commit()

    # ---- Return response ----
    return jsonify({
        "status": "sent",
        "message": message,
        "products_count": len(product_lines)
    }), 200

if __name__ == "__main__":
    app.run(port=5005, debug=True)
