import os
from flask import Flask, send_from_directory, redirect, url_for
from flask_login import LoginManager, current_user
from flask_admin import Admin
from flask_migrate import Migrate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from models import db, User, Scenario, Progress, Screenshot, Certificate, Config
from auth import auth
from views import app as app_blueprint

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

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(app_blueprint, url_prefix='/app')

    # Make login page the homepage
    @app.route('/')
    def home():
        return redirect(url_for('auth.login'))

    @app.route('/docs/<path:filename>')
    def docs_files(filename):
        return send_from_directory(MKDOCS_SITE_DIR, filename)

    @app.route('/docs')
    def docs_redirect():
        return redirect(url_for('home'))

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