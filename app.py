from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from cryptography.fernet import Fernet
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    # Initialize extensions
    db.init_app(app)
    with app.app_context():
        from models import Image
        db.create_all()

    # Encryption key
    app.fernet = Fernet(app.config['SECRET_KEY'])

    # Register routes
    from routes import init_routes
    init_routes(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
