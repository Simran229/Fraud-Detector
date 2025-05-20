# Fraud Detection System

A machine learning-based fraud detection system designed to identify suspicious financial transactions. This project demonstrates the implementation of a production-ready fraud detection system using modern technologies and best practices.

## Features

- Real-time fraud score computation for transactions
- Preprocessed dataset generation and synthetic fraud data support
- Trained machine learning model with auto-retraining pipeline
- REST API for logging transactions and querying predictions
- Comprehensive model evaluation and monitoring
- Database integration for transaction history
- JWT-based authentication for API security

## Tech Stack

- **Backend**: Python 3.10+, Flask 3.1.0
- **Machine Learning**: scikit-learn 1.6.1, pandas 2.2.3, NumPy 2.2.4
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/simran229/fraud-detection.git
cd fraud-detection
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database:
```bash
flask db upgrade
```

5. Download the dataset:
- Visit [Kaggle Credit Card Fraud Dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)
- Download and place `creditcard.csv` in the `data` directory

## Usage

1. Train the model:
```bash
python app/fraud_model.py
```

2. Start the API server:
```bash
flask run
```

3. Access the API documentation at `http://localhost:5000/api/docs`

## Project Structure

```
fraud-detection/
├── app/
│   ├── __init__.py
│   ├── fraud_model.py      # ML model implementation
│   ├── api/                # API endpoints
│   ├── models/             # Database models
│   └── utils/              # Utility functions
├── data/                   # Dataset directory
├── migrations/             # Database migrations
├── tests/                  # Test suite
├── .env.example           # Environment variables template
├── .gitignore
├── README.md
└── requirements.txt
```

## API Endpoints

- `POST /api/transactions`: Submit a new transaction for fraud detection
- `GET /api/transactions`: Retrieve transaction history
- `GET /api/model/status`: Check model status and metrics
- `POST /api/model/retrain`: Trigger model retraining

## Model Performance

The current model achieves:
- Precision: 88%
- Recall: 75%
- F1-Score: 81%
- AUC-ROC: 0.98

## Acknowledgments
- Credit Card Fraud Dataset from Kaggle

## Dataset Setup

This project uses the "Credit Card Fraud Detection" dataset from Kaggle. To set up the dataset:

1. Download the dataset from [Kaggle](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)
2. Create a `data` directory in the project root if it doesn't exist
3. Place the downloaded `creditcard.csv` file in the `data` directory

The dataset is not included in this repository due to its size (143.84 MB). This is intentional as it's a best practice to not include large datasets in version control.