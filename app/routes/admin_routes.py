from flask import Blueprint, redirect, render_template, request, url_for
from app.models import application
from app.models.company import CompanyProfile
from .. import db
from app.models.user import User
from app.models.student import StudentProfile
from app.models.placement_drive import PlacementDrive
from app.models.application import Application
admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard')
def admin_dashboard():
    total_companies = User.query.filter_by(role = 'company').count()
    total_students = User.query.filter_by(role = 'student').count()
    pending_approval = CompanyProfile.query.filter_by(approval_status = 'Pending').count()
    companies = CompanyProfile.query.filter_by(approval_status = 'Approved').all()
    students = StudentProfile.query.all()
    pending_companies = CompanyProfile.query.filter_by(approval_status = 'Pending').all()
    drives = PlacementDrive.query.filter_by(status = 'Active').all()
    student_applications = (Application.query.join(PlacementDrive).filter(PlacementDrive.status == "Active").all())

    return render_template('admin/dashboard.html', 
                           total_companies = total_companies, 
                           total_students = total_students, 
                           pending_approval = pending_approval,
                           companies = companies,
                           students = students,
                           pending_companies = pending_companies,
                           drives = drives,
                           student_applications = student_applications)

@admin_bp.route('/admin/search', methods = ['GET'])
def search():
    id = request.args.get('id')
    user = User.query.filter_by(id=id).first()

    if not user:
        return "User not found", 404

    if user.role == 'company':
        company = CompanyProfile.query.filter_by(user_id=user.id).first()
        if company:
            return redirect(url_for('admin.company_profile', id=company.id))

    elif user.role == 'student':
        student = StudentProfile.query.filter_by(user_id=user.id).first()
        if student:
            return redirect(url_for('admin.student_profile', id=student.id))

    return "Profile not found", 404

@admin_bp.route('/admin/approve_company/<int:id>', methods = ['POST'])
def approve_company(id):
    company_profile = CompanyProfile.query.get(id)

    if not company_profile:
        return "User not found", 404
    
    company_profile.approval_status = 'Approved'
    db.session.commit()

    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/company_profile/<int:id>')
def company_profile(id):
    company_profile = CompanyProfile.query.get(id)
    if not company_profile:
        return "Company not found", 404
    
    return render_template('admin/company_profile.html', company_profile = company_profile)

@admin_bp.route('/admin/blacklist_company/<int:id>', methods = ['POST'])
def blacklist_company(id):
    company_profile = CompanyProfile.query.get(id)

    if not company_profile:
        return "Company not found", 404
    
    company_profile.is_blacklisted = True
    db.session.commit()

    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/blacklist_student/<int:id>', methods = ['POST'])
def blacklist_student(id):
    student = StudentProfile.query.get(id)

    if not student:
        return "User not found", 404
    
    student.is_blacklisted = True
    db.session.commit()

    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/student_profile/<int:id>')
def student_profile(id):

    student = StudentProfile.query.get(id)
    if not student:
        return "User not found", 404

    application = Application.query.filter_by(student_id=id).all()
    
    return render_template('admin/student_profile.html', student = student, application = application)

@admin_bp.route('/admin/drive_details/<int:id>')
def drive_details(id):
    drive = PlacementDrive.query.get(id)
    if not drive:
        return "Drive not Found", 404
    return render_template('admin/drive_details.html', drive = drive)

@admin_bp.route('/admin/drive_status/<int:drive_id>', methods = ['POST'])
def drive_status(drive_id):
    drive = PlacementDrive.query.get(drive_id)

    if not drive:
        return "Drive not Found", 404
    
    drive.status = 'Closed'
    db.session.commit()

    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/student_applications/<int:id>')
def student_applications(id):
    student_applications = Application.query.filter_by(student_id=id).all()
    return render_template('admin/student_applications.html', applications = student_applications)