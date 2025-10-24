from flask import Flask, jsonify, request
import requests
import json

app = Flask(__name__)

# In-memory database for demo
users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com", "balance": 100},
    {"id": 2, "name": "Bob", "email": "bob@example.com", "balance": 150}
]

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = {
        "id": len(users) + 1,
        "name": data.get('name'),
        "email": data.get('email'),
        "balance": data.get('balance', 0)
    }
    users.append(new_user)
    
    # Record transaction on blockchain
    transaction_data = {
        "sender": "system",
        "recipient": new_user['name'],
        "amount": new_user['balance']
    }
    try:
        requests.post('http://blockchain-service:5002/transactions/new', 
                     json=transaction_data, timeout=2)
    except:
        pass  # Blockchain might be unavailable
    
    return jsonify(new_user), 201

@app.route('/users/<int:user_id>/transfer', methods=['POST'])
def transfer_balance(user_id):
    data = request.get_json()
    recipient_id = data.get('recipient_id')
    amount = data.get('amount')
    
    sender = next((u for u in users if u['id'] == user_id), None)
    recipient = next((u for u in users if u['id'] == recipient_id), None)
    
    if not sender or not recipient:
        return jsonify({"error": "User not found"}), 404
    
    if sender['balance'] < amount:
        return jsonify({"error": "Insufficient balance"}), 400
    
    sender['balance'] -= amount
    recipient['balance'] += amount
    
    # Record transaction on blockchain
    transaction_data = {
        "sender": sender['name'],
        "recipient": recipient['name'],
        "amount": amount
    }
    try:
        requests.post('http://blockchain-service:5002/transactions/new', 
                     json=transaction_data, timeout=2)
    except:
        pass
    
    return jsonify({
        "message": "Transfer successful",
        "transaction": transaction_data
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
