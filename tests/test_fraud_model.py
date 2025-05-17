import pytest
import numpy as np
from app.fraud_model import train_model, predict_fraud

def test_model_training():
    """Test that the model can be trained successfully"""
    model, scaler = train_model()
    assert model is not None
    assert scaler is not None

def test_prediction():
    """Test that the model can make predictions"""
    # Create a sample transaction
    sample_transaction = np.random.rand(1, 30)  # 30 features
    
    # Get prediction
    prediction = predict_fraud(sample_transaction)
    
    # Check prediction format
    assert isinstance(prediction, (int, float))
    assert prediction in [0, 1]  # Binary classification

def test_model_metrics():
    """Test that model metrics are within expected ranges"""
    model, _ = train_model()
    
    # Get model metrics
    metrics = model.get_metrics()
    
    # Check metric ranges
    assert 0 <= metrics['precision'] <= 1
    assert 0 <= metrics['recall'] <= 1
    assert 0 <= metrics['f1_score'] <= 1
    assert 0 <= metrics['auc_roc'] <= 1

def test_feature_importance():
    """Test that feature importance is calculated correctly"""
    model, _ = train_model()
    
    # Get feature importance
    importance = model.get_feature_importance()
    
    # Check importance format
    assert isinstance(importance, dict)
    assert len(importance) > 0
    assert all(0 <= v <= 1 for v in importance.values()) 