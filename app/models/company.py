from .. import db
from datetime import datetime
class CompanyProfile(db.Model):
    __tablename__ = "company_profiles"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique = True, nullable = False)
    company_name = db.Column(db.String(100), nullable=False)
    company_description = db.Column(db.String(500), nullable = False)
    approval_status = db.Column(db.String(20), default = "Pending")
    is_blacklisted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


