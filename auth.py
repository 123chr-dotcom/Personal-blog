from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from extensions import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('posts.index'))
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('邮箱或密码错误，请重试')
        return redirect(url_for('auth.login'))
    
    login_user(user, remember=remember)
    return redirect(url_for('posts.index'))

@auth.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('posts.index'))
    return render_template('register.html')

@auth.route('/register', methods=['POST'])
def register_post():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if password != confirm_password:
        flash('两次输入的密码不一致')
        return redirect(url_for('auth.register'))

    user = User.query.filter_by(email=email).first()
    if user:
        flash('该邮箱已被注册')
        return redirect(url_for('auth.register'))

    new_user = User(
        username=username,
        email=email,
        password=generate_password_hash(password, method='pbkdf2:sha256')
    )

    db.session.add(new_user)
    db.session.commit()

    flash('注册成功，请登录')
    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('posts.index'))
