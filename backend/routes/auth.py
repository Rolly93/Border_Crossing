from backend.model.models import users_db
from flask_login import login_required , current_user,login_user
from flask import Blueprint, render_template, request, redirect, url_for, flash
import time
auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/', methods=['GET'])
def login():
    logit = True
    return render_template('login.html' , logit=logit)

@auth_bp.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    logit = None
    if username =='admid' and password == '1234':

        logit = True
        user = users_db.get('1')
        login_user(user)
        #flash("Has iniciado sesión", "success")
        time.sleep(2)
    
        return redirect(url_for('dashboard_bp.dashboard'))
    
    else:
        # 4. Si fallan las credenciales, mandamos un error y recargamos el login
        flash("Usuario o contraseña incorrectos", "danger")
        return redirect(url_for('auth_bp.login'),logit=logit)

@auth_bp.route('/logout')
@login_required
def logout():
    # Lógica para limpiar sesión
    flash("Has cerrado sesión", "info")
    return redirect(url_for('auth_bp.login'))