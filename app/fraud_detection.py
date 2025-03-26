from datetime import datetime, timedelta
from .models import Transaction, db

def detect_fraud(transaction):
    # return true if fraud is detected, false otherwise

    fraud = False

    # rule based approach
    # large amount transactions
    if transaction.amount > 5000:
        fraud = True

    # mulitple transactions in a short time
    recent_transactions = Transaction.query.filter(Transaction.user_id == transaction.user_id, Transaction.date >= datetime.now() - timedelta(minutes=1)).count()
    if recent_transactions > 5:
        fraud = True

    # unusual spending category
    usual_categories = ["Gambling", "Luxury", "High-Risk Investment"]
    if transaction.category in usual_categories:
        fraud = True
    
    # fraud detection machine learning model
    # model = load_model()
    # if model.predict(transaction):
    #     fraud = True
    return fraud

    