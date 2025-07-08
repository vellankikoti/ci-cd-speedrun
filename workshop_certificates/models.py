from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for workshop participants"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(200), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Relationships
    progress = db.relationship('Progress', backref='user', lazy=True)
    screenshots = db.relationship('Screenshot', backref='user', lazy=True)
    certificates = db.relationship('Certificate', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_total_points(self):
        """Calculate total points from all progress entries"""
        return sum(p.points_earned for p in self.progress)
    
    def get_completed_scenarios(self):
        """Get list of completed scenario IDs"""
        return [p.scenario_id for p in self.progress if p.completed]
    
    def is_certificate_eligible(self):
        """Check if user meets certificate requirements"""
        total_points = self.get_total_points()
        completed_scenarios = len(self.get_completed_scenarios())
        
        # Requirements: 100+ points and at least 8 scenarios completed
        return total_points >= 100 and completed_scenarios >= 8

class Scenario(db.Model):
    """Workshop scenarios/phases"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    phase = db.Column(db.String(50), nullable=False)  # Setup, TestContainers, Docker, Jenkins, Kubernetes
    scenario_number = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    points = db.Column(db.Integer, default=0)
    checkpoint_tag = db.Column(db.String(100), unique=True)  # e.g., "Jenkins, Scenario 1, points=5"
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    progress = db.relationship('Progress', backref='scenario', lazy=True)
    
    def __repr__(self):
        return f'<Scenario {self.phase} {self.scenario_number}: {self.name}>'

class Progress(db.Model):
    """User progress tracking for scenarios"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    scenario_id = db.Column(db.Integer, db.ForeignKey('scenario.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    points_earned = db.Column(db.Integer, default=0)
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def mark_completed(self, points):
        self.completed = True
        self.points_earned = points
        self.completed_at = datetime.utcnow()

class Screenshot(db.Model):
    """Screenshot uploads for proof of completion"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    scenario_id = db.Column(db.Integer, db.ForeignKey('scenario.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    verified = db.Column(db.Boolean, default=False)
    verified_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    verified_at = db.Column(db.DateTime)

class Certificate(db.Model):
    """Generated certificates"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    certificate_number = db.Column(db.String(50), unique=True, nullable=False)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    total_points = db.Column(db.Integer, nullable=False)
    completed_scenarios = db.Column(db.Integer, nullable=False)
    pdf_filename = db.Column(db.String(255))
    
    def generate_certificate_number(self):
        """Generate unique certificate number"""
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        return f"EP-{timestamp}-{self.user_id:04d}"

class Config(db.Model):
    """Event configuration for certificates and branding"""
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(200), default="EuroPython CI/CD Chaos Workshop")
    event_date = db.Column(db.String(100), default="2024")
    event_location = db.Column(db.String(200), default="Prague, Czech Republic")
    certificate_title = db.Column(db.String(200), default="Certificate of Completion")
    certificate_subtitle = db.Column(db.String(200), default="CI/CD Chaos Engineering Workshop")
    certificate_text = db.Column(db.Text, default="This is to certify that {full_name} has successfully completed the EuroPython CI/CD Chaos Workshop, demonstrating proficiency in Docker, Kubernetes, Jenkins, and Testcontainers.")
    logo_filename = db.Column(db.String(255), default="workshop_logo.png")
    logo_size = db.Column(db.Integer, default=120)  # Size in pixels
    primary_color = db.Column(db.String(7), default="#326CE5")  # Docker blue
    secondary_color = db.Column(db.String(7), default="#3263D2")  # Kubernetes blue
    accent_color = db.Column(db.String(7), default="#00ADD8")  # Light blue
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @classmethod
    def get_config(cls):
        """Get or create default configuration"""
        config = cls.query.first()
        if not config:
            config = cls()
            db.session.add(config)
            db.session.commit()
        return config 