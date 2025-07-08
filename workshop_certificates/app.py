import os
from flask import Flask, send_from_directory, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_migrate import Migrate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
admin = Admin(name='Workshop Admin', template_mode='bootstrap4')

MKDOCS_SITE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../site'))


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

    # Import models after db initialization
    from models import User, Scenario, Progress, Screenshot, Certificate, Config

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from auth import auth
    from views import app as app_blueprint
    
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(app_blueprint, url_prefix='/app')

    # URL Structure for abc.vellanki.in:
    # 
    # Main Documentation (MkDocs):
    # - https://abc.vellanki.in/                    -> Workshop homepage
    # - https://abc.vellanki.in/docs/              -> Workshop documentation
    # - https://abc.vellanki.in/docs/phases/       -> Workshop phases
    # - https://abc.vellanki.in/docs/jenkins/      -> Jenkins scenarios
    # 
    # Interactive App (Flask):
    # - https://abc.vellanki.in/app/               -> User dashboard
    # - https://abc.vellanki.in/app/upload         -> Screenshot upload
    # - https://abc.vellanki.in/app/progress       -> Progress tracking
    # - https://abc.vellanki.in/app/certificate    -> Certificate download
    # 
    # Admin Panel:
    # - https://abc.vellanki.in/admin/             -> Admin dashboard
    # - https://abc.vellanki.in/admin/config       -> Event configuration
    # - https://abc.vellanki.in/admin/users        -> User management

    # Serve MkDocs static site for documentation
    @app.route('/')
    def docs_index():
        """Serve the main workshop homepage"""
        return send_from_directory(MKDOCS_SITE_DIR, 'index.html')

    @app.route('/docs/<path:filename>')
    def docs_files(filename):
        """Serve all MkDocs static files (CSS, JS, images, etc.)"""
        return send_from_directory(MKDOCS_SITE_DIR, filename)

    @app.route('/docs')
    def docs_redirect():
        """Redirect /docs to homepage"""
        return redirect(url_for('docs_index'))

    # Create database tables
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database tables created successfully")
            
            # Create default configuration if it doesn't exist
            try:
                if not Config.query.first():
                    default_config = Config()
                    db.session.add(default_config)
                    db.session.commit()
                    print("✅ Default configuration created")
            except Exception as e:
                # If there's an error, just continue - the database might not be ready yet
                print(f"Warning: Could not create default config: {e}")
                pass
        except Exception as e:
            print(f"Warning: Could not create database tables: {e}")
            # Continue anyway - the app should still work
            pass

    return app

# For gunicorn deployment - create app instance
app = create_app()

if __name__ == '__main__':
    # Use environment variable for debug mode
    debug_mode = os.getenv('FLASK_ENV') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=int(os.getenv('PORT', 5000))) 