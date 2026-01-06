from backend.model.models import users_db
from flask_login import login_required , current_user,login_user
from flask import Blueprint, render_template, request, redirect, url_for, flash
auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/', methods=['GET'])
def login():
    return render_template('login.html')

@auth_bp.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username =='admid' and password == '1234':


        user = users_db.get('1')
        login_user(user)
        flash("Has iniciado sesión", "success")
        return redirect(url_for('dashboard_bp.dashboard'))
    
    else:
        # 4. Si fallan las credenciales, mandamos un error y recargamos el login
        flash("Usuario o contraseña incorrectos", "danger")
        return redirect(url_for('auth_bp.login'))

@auth_bp.route('/logout')
@login_required
def logout():
    # Lógica para limpiar sesión
    flash("Has cerrado sesión", "info")
    return redirect(url_for('auth_bp.login'))