from .. import db
from datetime import datetime

class Placement(db.Model):
    __tablename__ = "placements"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student_profiles.id"), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey("placement_drives.id"), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("company_profiles.id"), nullable=False)
    package = db.Column(db.String(50))
    placement_date = db.Column(db.Date, default=datetime.utcnow)
