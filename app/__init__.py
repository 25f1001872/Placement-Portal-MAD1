from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        from . import models
        db.create_all()

        from app.models.user import User
        from werkzeug.security import generate_password_hash

        existing_admin = User.query.filter_by(role = "admin").first()

        if not existing_admin:
            admin = User(
                name="Admin",
                email="admin@gmail.com",
                password_hash=generate_password_hash("admin@2005"),
                role="admin"
            )
            db.session.add(admin)
            db.session.commit()

    return app

