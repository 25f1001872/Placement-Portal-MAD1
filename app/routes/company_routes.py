from flask import Blueprint, render_template

company_bp = Blueprint('company', __name__)

@company_bp.route('/company/dashboard')
def company_dashboard():
    return render_template('company/dashboard.html')

