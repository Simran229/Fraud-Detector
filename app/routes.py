from flask import Blueprint, request, jsonify
from . import db
from .models import User, Transaction
from .fraud_detection import detect_fraud
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
import joblib
import numpy as np
import pandas as pd
import os

main_bp = Blueprint('main', __name__, url_prefix='/api')

# Load the machine learning model
fraud_model_path = os.path.join(os.path.dirname(__file__), 'fraud_model.pkl')
fraud_model = joblib.load(fraud_model_path)

@main_bp.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to the Personal Finance App API'}), 200

@main_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400
    # Hash the password before storing
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@main_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if user and check_password_hash(user.password, data['password']):  # In production, use hashed passwords
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401

def encode_category(category):
    encoding = {
        'Groceries': 1, 'Rent': 2, 'Utilities': 3, 'Entertainment': 4,
        'Transportation': 5, 'Healthcare': 6, 'Insurance': 7}
    return encoding.get(category, 0)  # Default to 0 if category not found

# Add transaction
@main_bp.route('/transactions', methods=['POST'])
@jwt_required()
def add_transaction():
    data = request.get_json()
    user_id = get_jwt_identity()  # Extract user id from JWT token

    amount = data.get('amount')
    category = data.get('category')
    category_encoded = encode_category(category)
    # features = np.array([[amount, category_encoded]])
    features = pd.DataFrame([[amount, category_encoded]], columns=['amount', 'category_encoded'])

    # prediction = fraud_model.predict(features)[0]
    fraud_score = fraud_model.predict_proba(features)[0][1]

    if fraud_score > 0.7:
        fraud_alert = Transaction(amount=amount, category=category,
                                description=data.get('description', ''), user_id=user_id, is_fraud=True)
        db.session.add(fraud_alert)
        db.session.commit()
        return jsonify({'message': 'Transaction flagged as fraudulent', 'fraud_score': fraud_score}), 400

    # if prediction == 1:
        # return jsonify({'message': 'Transaction flagged as fraudulent'}), 400
    
    # new_transaction = Transaction(amount=amount, category=category,
    #                             description=data.get('description', ''), user_id=user_id)
    # db.session.add(new_transaction)
    # db.session.commit()

    return jsonify({'message': 'Transaction added successfully', 'fraud_score': fraud_score}), 201
    # data = request.get_json()
    # user_id = get_jwt_identity() #extract user id from JWT token

    # if not data.get('amount') or not data.get('category'):
    #     return jsonify({'message': 'Amount and category are required'}), 400
    
    # new_transaction = Transaction(amount=data['amount'], category=data['category'],
    #                               description=data.get('description', ''), user_id=user_id)
    # # Check for fraud
    # if detect_fraud(new_transaction):
    #     new_transaction.is_fraud = True
    #     db.session.add(new_transaction)
    #     db.session.commit()
    #     return jsonify({'message': 'Transaction added but detected as fraudulent'}), 400
    
    # db.session.add(new_transaction)
    # db.session.commit()

    # return jsonify({'message': 'Transaction added successfully'}), 201

# Get transactions
@main_bp.route('/transactions', methods=['GET'])
@jwt_required()
def get_transactions():
    user_id = get_jwt_identity()
    transactions = Transaction.query.filter_by(user_id=user_id).all()
    transactions_list = [{'amount': t.amount, 'category': t.category,
                     'description': t.description, 'date': t.date} for t in transactions]
    return jsonify({'transactions': transactions_list}), 200

@main_bp.route('fraud-alerts', methods=['GET'])
@jwt_required()
def fraud_alerts():
    user_id = get_jwt_identity()
    flagged_transactions = Transaction.query.filter_by(user_id=user_id, is_fraud=True).all()
    fraud_list = [{'amount': t.amount, 'category': t.category,
                     'description': t.description, 'date': t.date} for t in flagged_transactions]
    return jsonify({'fraud_alerts': fraud_list}), 200

@main_bp.route('/debug/delete-user/<username>', methods=['DELETE'])
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': f'User {username} deleted successfully'}), 200
    return jsonify({'message': f'User {username} not found'}), 404

@main_bp.route('/debug/users', methods=['GET'])
def list_users():
    users = User.query.all()
    users_list = [{'id': u.id, 'username': u.username} for u in users]
    return jsonify({'users': users_list}), 200