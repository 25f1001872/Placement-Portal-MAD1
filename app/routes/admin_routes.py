from flask import Blueprint, redirect, render_template, url_for
from app.models.company import CompanyProfile
from .. import db
from app.models.user import User
admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard')
def admin_dashboard():
    total_companies = User.query.filter_by(role = 'company').count()
    total_students = User.query.filter_by(role = 'student').count()
    pending_approval = CompanyProfile.query.filter_by(approval_status = 'Pending').count()
    companies = CompanyProfile.query.all()
    students = User.query.filter_by(role = 'student').all()
    pending_companies = CompanyProfile.query.filter_by(approval_status = 'Pending').all()
    return render_template('admin/dashboard.html', 
                           total_companies = total_companies, 
                           total_students = total_students, 
                           pending_approval = pending_approval,
                           companies = companies,
                           students = students,
                           pending_companies = pending_companies)



@admin_bp.route('/admin/approve_company/<int:id>')
def approve_company(id):
    company_profile = CompanyProfile.query.get(id)

    if not company_profile:
        return "User not found", 404
    
    company_profile.approval_status = 'Approved'
    db.session.commit()

    return redirect(url_for('admin.admin_dashboard'))

    