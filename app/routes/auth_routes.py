from flask import Blueprint, render_template, redirect, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from app.models.student import StudentProfile
from app.models.company import CompanyProfile
from .. import db
from app.models.user import User
from werkzeug.utils import secure_filename
import os


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    return render_template('home.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user  = User.query.filter_by(email = email).first()
        if user:
            company = CompanyProfile.query.filter_by(user_id = user.id).first()
        if user and check_password_hash(user.password_hash, password):
            
            session['user_id'] = user.id
            session['email'] = user.email
            session['role'] = user.role

            if user.role == 'admin':
                return redirect(url_for('admin.admin_dashboard'))
            
            elif user.role == 'company':
                if company.approval_status == 'Pending':
                    return render_template('login.html', error = 'Your account approval is pending by admin.')
                return redirect(url_for('company.company_dashboard'))
            
            elif user.role == 'student':
                return redirect(url_for('student.student_dashboard'))
        
        else:
            return render_template('login.html', error = 'Invalid Credentials')
            

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.home'))

@auth_bp.route('/register/student', methods=['GET', 'POST'])
def register_student():
    if request.method == 'GET':
        return render_template('register_student.html')

    elif request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        education = request.form.get('education')
        skills = request.form.get('skills')

        resume = request.files.get('resume')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template('register_student.html', error='User already registered.')
        
        else:
            new_user = User(name = name, email = email, password_hash = generate_password_hash(password), role = 'student')
            db.session.add(new_user)
            db.session.commit()
            new_student_profile = StudentProfile(user_id = new_user.id, student_name = name, education = education, skills = skills, resume_path = '')
            db.session.add(new_student_profile)
            db.session.commit()

            if resume:
                new_filename = f"student_{new_student_profile.id}_resume.pdf"
                upload_folder = os.path.join('app', 'static', 'uploads', 'resumes')
                os.makedirs(upload_folder, exist_ok=True)
                file_path = os.path.join(upload_folder, new_filename)
                resume.save(file_path)
                new_student_profile.resume_path = f"uploads/resumes/{new_filename}"
                db.session.commit()

            return render_template('login.html', message = 'Registration successful. Please login.')

@auth_bp.route('/register/company', methods  = ['GET', 'POST'])
def register_company():
    if request.method == 'GET':
        return render_template('register_company.html')
    
    elif request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        company_description = request.form.get('company_description')

        existing_user = User.query.filter_by(email = email).first()
            

        if existing_user:
            return render_template('register_company.html', error = 'User already exists.')  

        else:
            new_user = User(name = name, email = email, password_hash = generate_password_hash(password), role = 'company')
            db.session.add(new_user)
            db.session.commit()
            new_company_profile = CompanyProfile(user_id = new_user.id, company_name = name, company_description = company_description, approval_status = 'Pending')
            db.session.add(new_company_profile)
            db.session.commit()
            company = CompanyProfile.query.filter_by(user_id = new_user.id).first()
            if company.approval_status == 'Pending':
                return render_template('login.html', message = 'Registered Succesfully, Pending approval at admin.')
            elif company.approval_status == 'Rejected':
                return render_template('register_company.html', message = 'Your registration was rejected by admin.')
            return render_template('login.html', message = 'Registration successful. Please login.') 