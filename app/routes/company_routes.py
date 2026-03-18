from flask import Blueprint, redirect, render_template, request, url_for, session

from app.models.application import Application
from .. import db
from app.models.student import StudentProfile
from app.models.company import CompanyProfile
from app.models.placement_drive import PlacementDrive

company_bp = Blueprint('company', __name__)

@company_bp.route('/company/dashboard')
def company_dashboard():
    company_profile = CompanyProfile.query.filter_by(user_id = session['user_id']).first()
    company_id = company_profile.id
    upcoming_drives = PlacementDrive.query.filter_by(company_id = company_id, status = 'Active').all()
    closed_drives = PlacementDrive.query.filter_by(company_id = company_id, status = 'Closed').all()
    return render_template('company/dashboard.html', company_id = company_id, upcoming_drives = upcoming_drives, closed_drives = closed_drives)

@company_bp.route('/company/drive_applications/<int:drive_id>')
def drive_applications(drive_id):

    company_profile = CompanyProfile.query.filter_by(user_id = session['user_id']).first()
    drive = PlacementDrive.query.get(drive_id)
    if drive.company_id != company_profile.id:
         return "unauthorised access", 403
    
    student_applications = Application.query.filter_by(drive_id = drive_id).all()
    return render_template('company/drive_applications.html', student_applications = student_applications)

@company_bp.route('/company/student_application/<int:application_id>')
def student_application(application_id):

    company_profile = CompanyProfile.query.filter_by(user_id = session['user_id']).first()
    student_application = Application.query.get(application_id)  
    drive = PlacementDrive.query.get(student_application.drive_id)  
    if drive.company_id != company_profile.id:
        return "unauthorised access", 403

    student = StudentProfile.query.get(student_application.student_id)
    return render_template('company/student_application.html', student_application = student_application, student = student, drive = drive)

@company_bp.route('/company/student_application/<int:application_id>/update_status', methods = ['POST'])
def update_student_application_status(application_id):
        student_application = Application.query.get(application_id)
        new_status = request.form.get('status')
        if new_status not in ['Waiting', 'Shortlisted', 'Rejected']:
             return "Invalid status", 400

        student_application.status = new_status
        db.session.commit()

        return redirect(url_for('company.drive_applications', drive_id = student_application.drive_id))

@company_bp.route('/company/drive_status/<int:drive_id>', methods = ['POST'])
def drive_status(drive_id):
    placement_drive = PlacementDrive.query.get(drive_id)
    placement_drive.status = 'Closed'
    db.session.commit()
    return redirect(url_for('company.company_dashboard'))

@company_bp.route('/company/create_drive', methods = ['GET', 'POST'])
def create_drive():
    if request.method == 'GET':
        return render_template('company/create_drive.html')
    
    elif request.method == 'POST':
        company_profile = CompanyProfile.query.filter_by(user_id = session['user_id']).first()
        company_id = company_profile.id
        company_name = company_profile.company_name
        job_title = request.form.get('job_title')
        job_description = request.form.get('job_description')
        Eligibility_criteria = request.form.get('eligibility_criteria')
        Application_deadline = request.form.get('application_deadline')

        new_drive = PlacementDrive(company_id = company_id, company_name = company_name,job_title = job_title, job_description = job_description, eligibility = Eligibility_criteria, deadline = Application_deadline)
        db.session.add(new_drive)
        db.session.commit()

        
        return redirect(url_for('company.company_dashboard'))
    
