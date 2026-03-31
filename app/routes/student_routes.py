from flask import Blueprint, flash, redirect, render_template, session, url_for
from app.models.company import CompanyProfile
from app.models.placement_drive import PlacementDrive
from app.models.application import Application
from app.models.student import StudentProfile
from .. import db
student_bp = Blueprint('student', __name__)


@student_bp.route('/student/dashboard')
def student_dashboard():
    student_profile = StudentProfile.query.filter_by(user_id=session['user_id']).first()
    student_id = student_profile.id
    student_name = student_profile.student_name
    company_profile = CompanyProfile.query.filter_by(approval_status = 'Approved', is_blacklisted = False).all()
    applied_drives = Application.query.filter_by(student_id = student_id).all()
    return render_template('student/dashboard.html' , company_profile = company_profile, applied_drives = applied_drives, student_name = student_name, student_profile = student_profile)

@student_bp.route('/student/company_profiles/<int:company_id>')
def company_profile(company_id):
    company_profile = CompanyProfile.query.get(company_id)
    drive_info = PlacementDrive.query.filter_by(company_id = company_id).all()
    return render_template('student/company_profile.html', company_profile = company_profile, drive_info = drive_info)

@student_bp.route('/student/applications_history')
def applications_history():
    student_profile = StudentProfile.query.filter_by(user_id=session['user_id']).first()
    student_id = student_profile.id    
    applications = Application.query.filter_by(student_id = student_id).all()

    return render_template('student/applications_history.html', applications = applications, Remark = "None", student_profile = student_profile, student_id = student_id)

@student_bp.route('/student/drive_details/<int:drive_id>')
def drive_details(drive_id):
    drive_info = PlacementDrive.query.get(drive_id)
    return render_template('student/drive_details.html', drive = drive_info)

@student_bp.route('/student/drive_details/<int:drive_id>/apply' , methods = ['POST'])
def apply(drive_id):
    student_profile = StudentProfile.query.filter_by(user_id=session['user_id']).first()
    student_id = student_profile.id
    existing_application = Application.query.filter_by(
    student_id=student_id,
    drive_id=drive_id
    ).first()

    if existing_application:
       flash("You have already applied to this drive!", "warning")
       return redirect(url_for('student.student_dashboard', drive_id=drive_id))
    new_application = Application(student_id = student_id, student_name = student_profile.student_name, drive_id = drive_id,)
    db.session.add(new_application)
    db.session.commit()
    return redirect(url_for('student.student_dashboard'))