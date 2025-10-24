from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

products = [
    {"id": 101, "name": "Laptop", "price": 999.99, "category": "Electronics", "stock": 10},
    {"id": 102, "name": "Mobile", "price": 499.99, "category": "Electronics", "stock": 25},
    {"id": 103, "name": "Headphones", "price": 149.99, "category": "Electronics", "stock": 50},
    {"id": 104, "name": "Desk", "price": 199.99, "category": "Furniture", "stock": 15}
]

@app.route('/products', methods=['GET'])
def get_products():
    category = request.args.get('category')
    if category:
        filtered_products = [p for p in products if p['category'].lower() == category.lower()]
        return jsonify(filtered_products)
    return jsonify(products)

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    new_product = {
        "id": len(products) + 101,
        "name": data.get('name'),
        "price": data.get('price'),
        "category": data.get('category'),
        "stock": data.get('stock', 0)
    }
    products.append(new_product)
    return jsonify(new_product), 201

@app.route('/products/<int:product_id>/purchase', methods=['POST'])
def purchase_product(product_id):
    data = request.get_json()
    user_id = data.get('user_id')
    quantity = data.get('quantity', 1)
    
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    if product['stock'] < quantity:
        return jsonify({"error": "Insufficient stock"}), 400
    
    # Get user info (in real app, this would be a service call)
    total_price = product['price'] * quantity
    product['stock'] -= quantity
    
    # Record transaction on blockchain
    transaction_data = {
        "sender": f"user_{user_id}",
        "recipient": "store",
        "amount": total_price
    }
    try:
        requests.post('http://blockchain-service:5002/transactions/new', 
                     json=transaction_data, timeout=2)
    except:
        pass
    
    return jsonify({
        "message": "Purchase successful",
        "product": product['name'],
        "quantity": quantity,
        "total_price": total_price,
        "transaction": transaction_data
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)