import os
from flask import Flask, send_from_directory, redirect, url_for, jsonify
from flask_login import LoginManager, current_user
from flask_admin import Admin
from flask_migrate import Migrate
from dotenv import load_dotenv
import time
import psutil

# Load environment variables
load_dotenv()

from models import db, User, Scenario, Progress, Screenshot, Certificate, Config
from auth import auth
from views import app as app_blueprint

login_manager = LoginManager()
migrate = Migrate()
admin = Admin(name='Workshop Admin', template_mode='bootstrap4')

MKDOCS_SITE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'site'))

# Global variable to track start time for uptime calculation
START_TIME = time.time()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')
    # Handle database URL (Render provides DATABASE_URL, but we need to handle it properly)
    database_url = os.getenv('DATABASE_URL', 'sqlite:///workshop.db')
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB upload limit

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    admin.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(app_blueprint, url_prefix='/app')

    # Make docs the homepage
    @app.route('/')
    def home():
        return send_from_directory(MKDOCS_SITE_DIR, 'index.html')

    # Health check endpoint for Docker and monitoring
    @app.route('/health')
    def health():
        try:
            # Check database connectivity
            db.session.execute(db.text('SELECT 1'))
            db_status = 'healthy'
        except Exception as e:
            db_status = f'unhealthy: {str(e)}'
        
        # Calculate uptime
        uptime_seconds = time.time() - START_TIME
        uptime_hours = uptime_seconds / 3600
        
        # Get system info
        memory_info = psutil.virtual_memory()
        cpu_percent = psutil.cpu_percent(interval=1)
        
        return jsonify({
            'status': 'healthy' if db_status == 'healthy' else 'unhealthy',
            'timestamp': time.time(),
            'uptime_hours': round(uptime_hours, 2),
            'version': '1.0.0',
            'database': db_status,
            'system': {
                'memory_usage_percent': round(memory_info.percent, 2),
                'cpu_usage_percent': round(cpu_percent, 2),
                'memory_available_mb': round(memory_info.available / 1024 / 1024, 2)
            }
        })

    @app.route('/docs/<path:filename>')
    def docs_files(filename):
        return send_from_directory(MKDOCS_SITE_DIR, filename)

    @app.route('/docs')
    def docs_index():
        return send_from_directory(MKDOCS_SITE_DIR, 'index.html')

    # Create database tables and default config
    with app.app_context():
        try:
            db.create_all()
            if not Config.query.first():
                default_config = Config()
                db.session.add(default_config)
                db.session.commit()
        except Exception as e:
            print(f"Warning: Could not create database tables or default config: {e}")
            pass

    return app

app = create_app()

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_ENV') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=int(os.getenv('PORT', 5000))) 