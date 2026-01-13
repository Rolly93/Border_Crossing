
from flask_login import login_required , current_user,login_user
from flask import Blueprint, render_template, request, redirect, url_for, flash
import time
from backend.utility.service.auth_service import AuthService

auth_bp = Blueprint('auth_bp', __name__)
auth_service = AuthService()


@auth_bp.route('/', methods=['GET'])
def login():
    logit = True
    return render_template('login.html' , logit=logit)

@auth_bp.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    
    user = auth_service.autenticar(username,password)
    
    if user:
        login_user(user)
        return redirect(url_for('dashboard_bp.dashboard'))
    
    
    return redirect(url_for('auth_bp.login'),logit=logit)

@auth_bp.route('/logout')
@login_required
def logout():
    # Lógica para limpiar sesión
    flash("Has cerrado sesión", "info")
    return redirect(url_for('auth_bp.login'))