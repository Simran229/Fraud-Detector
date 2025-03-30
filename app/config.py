import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///finance.db'  # Replace with your actual database URI
    # SECRET_KEY = 'your_secret_key'  # For session/cookie encryption
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable track modifications warning
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback_jwt_secret_key")
    # JWT_SECRET_KEY = 'jwt_secret_key'  # For JWT token encryption (if using JWT)
    JWT_VERIFY_SUB = False  # Allow 'sub' claim not to be present in JWT