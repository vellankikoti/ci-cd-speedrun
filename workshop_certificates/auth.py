from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from models import db, User

class DummyForm:
    def hidden_tag(self):
        return ''
    username = password = email = full_name = confirm = confirm_password = lambda self, *a, **k: ''
    remember = lambda self, *a, **k: ''

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('app.dashboard'))
    form = DummyForm()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user, remember=True)
            flash('Successfully logged in!', 'success')
            return redirect(url_for('app.dashboard'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('auth/login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('app.dashboard'))
    form = DummyForm()
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        full_name = request.form.get('full_name')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        # Validation
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('auth/register.html', form=form)
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('auth/register.html', form=form)
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('auth/register.html', form=form)
        if len(password) < 6:
            flash('Password must be at least 6 characters', 'error')
            return render_template('auth/register.html', form=form)
        # Create user
        user = User(
            username=username,
            email=email,
            full_name=full_name
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login')) 