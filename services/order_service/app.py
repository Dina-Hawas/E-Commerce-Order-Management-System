from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Simple health-check
@app.route("/", methods=["GET"])
def home():
    return "Order Service is running on port 5001!"

# Simple test endpoint
@app.route("/api/orders/test", methods=["GET"])
def test_order():
    return jsonify({"message": "Order service test OK"}), 200

# Endpoint that calls Inventory Service
# @app.route("/api/orders/check-inventory/<int:product_id>", methods=["GET"])
# def check_inventory(product_id):
#     try:
#         # URL of Inventory Service (Member A’s responsibility)
#         inventory_url = f"http://localhost:5002/api/inventory/check/{product_id}"
        
#         resp = requests.get(inventory_url, timeout=5)
#         if resp.status_code == 200:
#             data = resp.json()
#             return jsonify({
#                 "message": "Inventory check successful",
#                 "inventory_response": data
#             }), 200
#         else:
#             return jsonify({
#                 "message": "Inventory service returned error",
#                 "status_code": resp.status_code,
#                 "text": resp.text
#             }), 502

#     except requests.exceptions.RequestException as e:
#         return jsonify({
#             "message": "Failed to reach Inventory Service",
#             "error": str(e)
#         }), 500


if __name__ == "__main__":
    app.run(port=5001, debug=True)
