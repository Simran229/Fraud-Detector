from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from .config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Load configuration from Config class

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from .routes import main_bp
    app.register_blueprint(main_bp, url_prefix='/api')  # Ensure blueprint is registered with a URL prefix

    @app.route('/')
    def root():
        return 'Welcome to the Personal Finance App', 200

    return app