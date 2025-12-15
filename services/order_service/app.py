from flask import Flask, jsonify, request
import requests
import uuid
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# ---------
orders_db = {}  # In-memory DB

INVENTORY_VALIDATE_URL = "http://localhost:5002/api/inventory/validate"
PRICING_URL = "http://localhost:5003/api/pricing/calculate"
CUSTOMER_URL = "http://localhost:5004/api/customers"


@app.route("/", methods=["GET"])
def home():
    return "Order Service is running on port 5001!"


# ----------------------------------
# CREATE ORDER
# ----------------------------------
@app.route("/api/orders/create", methods=["POST"])
def create_order():
    try:
        data = request.get_json()

        # ---- Input validation ----
        customer_id = data["customer_id"]
        products = data["products"]

        if not products or not isinstance(products, list):
            return jsonify({"error": "Products list is required"}), 400

        # ---- Validate customer ----
        customer_resp = requests.get(f"{CUSTOMER_URL}/{customer_id}")
        if customer_resp.status_code != 200:
            return jsonify({"error": "Invalid customer"}), 400

        # ---- Validate inventory (bulk check) ----
        inventory_resp = requests.post(
            INVENTORY_VALIDATE_URL,
            json={"items": products}
        )

        if inventory_resp.status_code != 200:
            return jsonify({"error": "Inventory service failed"}), 500

        inventory_results = inventory_resp.json()

        for item in inventory_results:
            if item["status"] != "ok":
                return jsonify({
                    "error": f"Product {item['product_id']} not available"
                }), 400

        # ---- Pricing calculation ----
        pricing_resp = requests.post(
            PRICING_URL,
            json={"products": products}
        )

        if pricing_resp.status_code != 200:
            return jsonify({"error": "Pricing service failed"}), 500

        pricing_data = pricing_resp.json()

        # ---- Create order ----
        order_id = str(uuid.uuid4())
        order = {
            "order_id": order_id,
            "customer_id": customer_id,
            "products": products,
            "pricing": pricing_data,
            "status": "CONFIRMED",
            "timestamp": datetime.now().isoformat()
        }

        orders_db[order_id] = order

        return jsonify(order), 201

    except KeyError as e:
        return jsonify({"error": f"Missing field {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ----------------------------------
# GET ORDER BY ID
# ----------------------------------
@app.route("/api/orders/<order_id>", methods=["GET"])
def get_order(order_id):
    order = orders_db.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(order), 200


# ----------------------------------
# GET ORDERS BY CUSTOMER (FOR CUSTOMER SERVICE)
# ----------------------------------
@app.route("/api/orders", methods=["GET"])
def get_orders_by_customer():
    customer_id = request.args.get("customer_id")
    if not customer_id:
        return jsonify({"error": "customer_id is required"}), 400

    result = [
        o for o in orders_db.values()
        if str(o["customer_id"]) == customer_id
    ]

    return jsonify(result), 200


if __name__ == "__main__":
    app.run(port=5001, debug=True)
