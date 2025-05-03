import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///finance.db'
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable track modifications warning
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback_jwt_secret_key")
    
    JWT_VERIFY_SUB = False  