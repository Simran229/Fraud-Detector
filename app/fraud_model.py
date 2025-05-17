# fraud_model.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score, learning_curve
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
import matplotlib.pyplot as plt
import joblib
import os

# Load the dataset
try:
    df = pd.read_csv('data/creditcard.csv')
    print(f"Dataset loaded successfully! Shape: {df.shape}")
except FileNotFoundError:
    print("Dataset not found. Please ensure 'creditcard.csv' is in the 'data' directory.")
    exit(1)

# Use 20% of data for faster training while maintaining good representation
df_sample = df.sample(frac=0.2, random_state=42)
print(f"Using sample of {len(df_sample)} transactions for training")

# Add some feature engineering
df_sample['amount_log'] = np.log1p(df_sample['Amount'])  # Log transform of amount
df_sample['hour'] = df_sample['Time'] // 3600  # Extract hour from timestamp

# Split features and target
feature_columns = [col for col in df_sample.columns if col not in ['Class', 'Time', 'Amount']]
X = df_sample[feature_columns]
y = df_sample['Class']

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Simplified parameter grid for faster training
param_grid = {
    'n_estimators': [100],
    'max_depth': [10],
    'min_samples_split': [2],
    'class_weight': ['balanced']
}

# Initialize model
model = RandomForestClassifier(random_state=42)

# Perform grid search with fewer cross-validation folds
grid_search = GridSearchCV(
    estimator=model,
    param_grid=param_grid,
    cv=3,  # Reduced to 3 folds
    scoring='f1',
    n_jobs=-1
)

print("Training model...")
# Fit the model
grid_search.fit(X_train_scaled, y_train)

# Get best model
best_model = grid_search.best_estimator_

# Make predictions
y_pred = best_model.predict(X_test_scaled)
y_pred_proba = best_model.predict_proba(X_test_scaled)[:, 1]  # Probability of fraud

# Print model performance
print("\nModel Performance:")
print("\nBest Parameters:", grid_search.best_params_)
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Calculate and print feature importance
feature_importance = pd.DataFrame({
    'feature': feature_columns,
    'importance': best_model.feature_importances_
})
feature_importance = feature_importance.sort_values('importance', ascending=False)
print("\nTop 10 Most Important Features:")
print(feature_importance.head(10))

# Calculate ROC curve and AUC
fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
roc_auc = auc(fpr, tpr)

# Plot ROC curve
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc="lower right")
plt.savefig('roc_curve.png')
plt.close()

# Plot learning curves to check for overfitting
train_sizes, train_scores, test_scores = learning_curve(
    best_model, X_train_scaled, y_train, cv=3, n_jobs=-1,
    train_sizes=np.linspace(0.1, 1.0, 10),
    scoring='f1'
)

train_mean = np.mean(train_scores, axis=1)
train_std = np.std(train_scores, axis=1)
test_mean = np.mean(test_scores, axis=1)
test_std = np.std(test_scores, axis=1)

plt.figure(figsize=(10, 6))
plt.plot(train_sizes, train_mean, label='Training score')
plt.plot(train_sizes, test_mean, label='Cross-validation score')
plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.1)
plt.fill_between(train_sizes, test_mean - test_std, test_mean + test_std, alpha=0.1)
plt.xlabel('Training Examples')
plt.ylabel('F1 Score')
plt.title('Learning Curves')
plt.legend(loc='best')
plt.grid(True)
plt.savefig('learning_curves.png')
plt.close()

# Print cross-validation scores
cv_scores = cross_val_score(best_model, X_train_scaled, y_train, cv=3, scoring='f1')
print("\nCross-validation scores:", cv_scores)
print("Average CV score:", cv_scores.mean())
print("CV score std:", cv_scores.std())

# Save model and scaler
joblib.dump(best_model, 'fraud_model.pkl')
joblib.dump(scaler, 'fraud_scaler.pkl')

print("\nFraud detection model trained and saved!")
print("ROC curve plot saved as 'roc_curve.png'")
print("Learning curves plot saved as 'learning_curves.png'")