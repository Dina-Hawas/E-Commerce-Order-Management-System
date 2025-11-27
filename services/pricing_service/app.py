from flask import Flask, request, jsonify

from mysql.connector import Error
import requests

from db_config import get_db_connection

app = Flask(__name__)



@app.route('/')
def home():
    return "Pricing Service is running!", 200



def get_bulk_discount(product_id, quantity):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT discount_percentage 
        FROM pricing_rules
        WHERE product_id = %s AND min_quantity <= %s
        ORDER BY min_quantity DESC
        LIMIT 1
    """

    cursor.execute(query, (product_id, quantity))
    rule = cursor.fetchone()

    conn.close()

    if rule:
        return float(rule["discount_percentage"])
    return 0.0



def get_tax_rate():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT rate FROM tax_rates")
    row = cursor.fetchone()

    conn.close()

    return float(row["rate"]) if row else 0.0



@app.route("/api/pricing/calculate", methods=["POST"])
def calculate_price():

    data = request.get_json()

    if not data or "products" not in data:
        return jsonify({"error": "Invalid input"}), 400

    products = data["products"]
    itemized = []
    subtotal = 0

    for item in products:
        product_id = item["product_id"]
        quantity = item["quantity"]


        response = requests.get(f"http://localhost:5002/api/inventory/check/{product_id}")

        if response.status_code != 200:
            return jsonify({"error": f"Inventory Service failed for product {product_id}"}), 500

        product_data = response.json()  
        unit_price = float(product_data["unit_price"])
        product_name= product_data["product_name"]
        discount_percentage = get_bulk_discount(product_id, quantity)
        discount_amount = (discount_percentage / 100) * unit_price * quantity
        item_total = (unit_price * quantity) - discount_amount
        subtotal += item_total

        itemized.append({
            "product_id": product_id,
            "produc_name": product_name,
            "quantity": quantity,
            "unit_price": unit_price,
            "discount_percentage": discount_percentage,
            "discount_amount": discount_amount,
            "total_after_discount": item_total
        })


    tax_rate = get_tax_rate()
    tax_amount = subtotal * (tax_rate / 100)
    grand_total = subtotal + tax_amount


    return jsonify({
        "items": itemized,
        "subtotal": subtotal,
        "tax_rate": tax_rate,
        "tax_amount": tax_amount,
        "grand_total": grand_total
    }), 200


if __name__ == '__main__':
    app.run(port=5003, debug=True)