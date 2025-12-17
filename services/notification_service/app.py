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

    customer_res = requests.get(f"http://localhost:5004/api/customers/{customer_id}")
    customer_data = customer_res.json()

    order_res =requests.get(f"http://localhost:5001/api/orders/{order_id}")
    order_data = order_res.json()
    product_id = order_data['products'][0]['product_id']
    inventory_res = requests.get(f"http://localhost:5002/api/inventory/check/{product_id}")
    inventory_data = inventory_res.json()

    message = (
        f"Order #{order_id} confirmed for customer {customer_data['name']}.\n"
        f"Email: {customer_data['email']}\n"
        f"Stock Status: {inventory_data}"
    )

    print("TO:", customer_data["email"])
    print("MESSAGE:", message)
    print("=====================================\n")

    cursor.execute(
        "INSERT INTO notification_log (customer_id, message) VALUES (%s, %s)",
        (customer_id, message)
    )
    db.commit()

    return jsonify({
        "status": "sent",
        "message": message
    })

if __name__ == "__main__":
    app.run(port=5005, debug=True)
