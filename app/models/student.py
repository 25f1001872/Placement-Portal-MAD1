from .. import db
from datetime import datetime

class StudentProfile(db.Model):
    __tablename__ = "student_profiles"
    id = db.Column(db.Integer, primary_key = True)
    student_name = db.Column(db.String(100), db.ForeignKey('users.name'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique = True, nullable = False)
    education = db.Column(db.String(200))
    skills = db.Column(db.String(300))
    resume_path = db.Column(db.String(300))
    is_blacklisted = db.Column(db.Boolean, default = False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
