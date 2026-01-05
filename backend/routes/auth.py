from flask import Blueprint, render_template, request, redirect, url_for, flash

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/', methods=['GET'])
def login():
    return render_template('login.html')

@auth_bp.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    
    return redirect(url_for('dashboard_bp.dashboard'))
    #else:
    #    flash("Usuario o contraseña incorrectos", "danger")
    #    return redirect(url_for('auth_bp.login'))

@auth_bp.route('/logout')
def logout():
    # Lógica para limpiar sesión
    flash("Has cerrado sesión", "info")
    return redirect(url_for('auth_bp.login'))