# fraud_model.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# fake data for training
data = {
    'amount': [50, 200, 5000, 20000, 15000, 120, 75, 30000, 80, 7000],
    'category_encoded': [1, 2, 3, 3, 2, 1, 1, 3, 2, 3],
    'is_fraud': [0, 0, 0, 1, 1, 0, 0, 1, 0, 1]
}

df = pd.DataFrame(data)

# Split X and y
X = df[['amount', 'category_encoded']]
y = df['is_fraud']

# Train model
model = RandomForestClassifier()
model.fit(X, y)

# Save model
joblib.dump(model, 'fraud_model.pkl')

print("Fraud detection model trained and saved!")