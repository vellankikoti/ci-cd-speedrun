from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_file
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from models import db, User, Scenario, Progress, Screenshot, Certificate, Config
from certificate_generator import generate_certificate_pdf

app = Blueprint('app', __name__)

def allowed_file(filename):
    """Check if uploaded file is allowed"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard with progress tracking"""
    # Get user's progress
    user_progress = Progress.query.filter_by(user_id=current_user.id).all()
    completed_scenarios = [p.scenario_id for p in user_progress if p.completed]
    total_points = current_user.get_total_points()
    
    # Get all scenarios grouped by phase
    scenarios = Scenario.query.filter_by(is_active=True).order_by(Scenario.phase, Scenario.scenario_number).all()
    phases = {}
    for scenario in scenarios:
        if scenario.phase not in phases:
            phases[scenario.phase] = []
        phases[scenario.phase].append(scenario)
    
    # Calculate progress percentages
    total_scenarios = len(scenarios)
    completed_count = len(completed_scenarios)
    progress_percentage = (completed_count / total_scenarios * 100) if total_scenarios > 0 else 0
    
    # Check certificate eligibility
    is_eligible = current_user.is_certificate_eligible()
    
    return render_template('app/dashboard.html',
                         phases=phases,
                         user_progress=user_progress,
                         total_points=total_points,
                         completed_count=completed_count,
                         total_scenarios=total_scenarios,
                         progress_percentage=progress_percentage,
                         is_eligible=is_eligible)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """Screenshot upload interface"""
    if request.method == 'POST':
        if 'screenshot' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['screenshot']
        scenario_id = request.form.get('scenario_id')
        
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if not scenario_id:
            flash('Please select a scenario', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            # Secure filename and save
            filename = secure_filename(file.filename)
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            new_filename = f"{current_user.id}_{scenario_id}_{timestamp}_{filename}"
            
            # Ensure upload directory exists
            upload_dir = current_app.config['UPLOAD_FOLDER']
            os.makedirs(upload_dir, exist_ok=True)
            
            file_path = os.path.join(upload_dir, new_filename)
            file.save(file_path)
            
            # Create screenshot record
            screenshot = Screenshot(
                user_id=current_user.id,
                scenario_id=scenario_id,
                filename=new_filename,
                original_filename=filename,
                file_size=os.path.getsize(file_path)
            )
            
            db.session.add(screenshot)
            db.session.commit()
            
            flash('Screenshot uploaded successfully!', 'success')
            return redirect(url_for('app.dashboard'))
        else:
            flash('Invalid file type. Please upload an image.', 'error')
    
    # Get scenarios for dropdown
    scenarios = Scenario.query.filter_by(is_active=True).order_by(Scenario.phase, Scenario.scenario_number).all()
    return render_template('app/upload.html', scenarios=scenarios)

@app.route('/progress')
@login_required
def progress():
    """Detailed progress tracking"""
    user_progress = Progress.query.filter_by(user_id=current_user.id).all()
    scenarios = Scenario.query.filter_by(is_active=True).order_by(Scenario.phase, Scenario.scenario_number).all()
    
    # Create progress map
    progress_map = {p.scenario_id: p for p in user_progress}
    
    return render_template('app/progress.html',
                         scenarios=scenarios,
                         progress_map=progress_map,
                         total_points=current_user.get_total_points())

@app.route('/certificate')
@login_required
def certificate():
    """Certificate download page"""
    # Check if user is eligible
    if not current_user.is_certificate_eligible():
        flash('You need 100+ points and 8+ completed scenarios to earn a certificate.', 'warning')
        return redirect(url_for('app.dashboard'))
    
    # Check if certificate already exists
    existing_cert = Certificate.query.filter_by(user_id=current_user.id).first()
    
    if not existing_cert:
        # Generate new certificate
        total_points = current_user.get_total_points()
        completed_scenarios = len(current_user.get_completed_scenarios())
        
        cert = Certificate(
            user_id=current_user.id,
            certificate_number=Certificate().generate_certificate_number(),
            total_points=total_points,
            completed_scenarios=completed_scenarios
        )
        
        db.session.add(cert)
        db.session.commit()
        
        # Generate PDF
        pdf_filename = generate_certificate_pdf(cert)
        cert.pdf_filename = pdf_filename
        db.session.commit()
        
        existing_cert = cert
    
    return render_template('app/certificate.html', certificate=existing_cert)

@app.route('/download-certificate/<int:cert_id>')
@login_required
def download_certificate(cert_id):
    """Download certificate PDF"""
    cert = Certificate.query.get_or_404(cert_id)
    
    # Ensure user can only download their own certificate
    if cert.user_id != current_user.id:
        flash('Access denied', 'error')
        return redirect(url_for('app.dashboard'))
    
    if not cert.pdf_filename:
        flash('Certificate PDF not found', 'error')
        return redirect(url_for('app.certificate'))
    
    pdf_path = os.path.join(current_app.config['UPLOAD_FOLDER'], cert.pdf_filename)
    
    if not os.path.exists(pdf_path):
        flash('Certificate file not found', 'error')
        return redirect(url_for('app.certificate'))
    
    return send_file(pdf_path, as_attachment=True, download_name=f"certificate_{cert.certificate_number}.pdf")

@app.route('/profile')
@login_required
def profile():
    """User profile page"""
    return render_template('app/profile.html') 