from flask import Flask, jsonify, request
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Service URLs
USER_SERVICE_URL = "http://user-service:5000"
PRODUCT_SERVICE_URL = "http://product-service:5001"
BLOCKCHAIN_SERVICE_URL = "http://blockchain-service:5002"

@app.route('/')
def home():
    return jsonify({
        "message": "Microservices API Gateway",
        "services": {
            "users": "/users",
            "products": "/products", 
            "blockchain": "/chain"
        }
    })

@app.route('/users', methods=['GET', 'POST'])
def users_proxy():
    if request.method == 'GET':
        response = requests.get(f"{USER_SERVICE_URL}/users")
    else:
        response = requests.post(f"{USER_SERVICE_URL}/users", json=request.get_json())
    return jsonify(response.json()), response.status_code

@app.route('/users/<path:path>', methods=['GET', 'POST'])
def user_path_proxy(path):
    url = f"{USER_SERVICE_URL}/users/{path}"
    if request.method == 'GET':
        response = requests.get(url)
    else:
        response = requests.post(url, json=request.get_json())
    return jsonify(response.json()), response.status_code

@app.route('/products', methods=['GET', 'POST'])
def products_proxy():
    if request.method == 'GET':
        response = requests.get(f"{PRODUCT_SERVICE_URL}/products")
    else:
        response = requests.post(f"{PRODUCT_SERVICE_URL}/products", json=request.get_json())
    return jsonify(response.json()), response.status_code

@app.route('/products/<path:path>', methods=['GET', 'POST'])
def product_path_proxy(path):
    url = f"{PRODUCT_SERVICE_URL}/products/{path}"
    if request.method == 'GET':
        response = requests.get(url)
    else:
        response = requests.post(url, json=request.get_json())
    return jsonify(response.json()), response.status_code

@app.route('/chain', methods=['GET'])
def chain_proxy():
    response = requests.get(f"{BLOCKCHAIN_SERVICE_URL}/chain")
    return jsonify(response.json()), response.status_code

@app.route('/mine', methods=['GET'])
def mine_proxy():
    response = requests.get(f"{BLOCKCHAIN_SERVICE_URL}/mine")
    return jsonify(response.json()), response.status_code

@app.route('/transactions/new', methods=['POST'])
def transactions_proxy():
    response = requests.post(f"{BLOCKCHAIN_SERVICE_URL}/transactions/new", json=request.get_json())
    return jsonify(response.json()), response.status_code

@app.route('/dashboard')
def dashboard():
    # Get data from all services
    users_response = requests.get(f"{USER_SERVICE_URL}/users")
    products_response = requests.get(f"{PRODUCT_SERVICE_URL}/products")
    chain_response = requests.get(f"{BLOCKCHAIN_SERVICE_URL}/chain")
    stats_response = requests.get(f"{BLOCKCHAIN_SERVICE_URL}/stats")
    
    return jsonify({
        "users_count": len(users_response.json()),
        "products_count": len(products_response.json()),
        "blockchain_blocks": stats_response.json().get('total_blocks', 0),
        "blockchain_transactions": stats_response.json().get('total_transactions', 0)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)