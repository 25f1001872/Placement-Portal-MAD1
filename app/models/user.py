from .. import db # .. to avoid circular imports
from datetime import datetime
from werkzeug.security import generate_password_hash

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key = True, autoincrement = True)
    name = db.Column(db.String(75), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique = True)
    password_hash = db.Column(db.String(255), nullable = False)
    role = db.Column(db.String(20), nullable = False)
    is_active = db.Column(db.Boolean, default = True)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    