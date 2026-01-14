
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
    
    
    return redirect(url_for('auth_bp.login'))

@auth_bp.route('/usuarios' , methods=['GET', 'POST'])
@login_required
def registrar_empleado():
    if not current_user.admit:
        # logica para manejo de usuarios 
        flash("No tienes permisos para acceder a esta sección","danger")
        return redirect(url_for('dashboard_bp.dashboard'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')
        es_admin = True if request.form.get('es_admin')  else False

        exito = auth_service.crear_usuario(nombre,email,password , es_admin)

        if exito:
            flash(f"Usuario: {nombre}  creado con exito","success")
            return redirect(url_for('dashboard_bp.dashboard'))
    return render_template('registrar_empleado.html')


@auth_bp.route('/setup/<token>', methods =['GET','POST'])
def setup_inicial(token):
    if not auth_service.es_token_valido(token):
        flash("El enlace de configuracion es invalido o ha expirado","danger")
        return redirect(url_for('auth_bp.login'))
    
    if request.method == 'POST':
        nombre= request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if auth_service.crear_usuario(nombre,email,password,es_admin=True):
            flash("Usuario creado con exito","success")
            return redirect(url_for('auth_bp.login'))
    
    return render_template('setup.html', token=token)


@auth_bp.route('/logout')
@login_required
def logout():
    # Lógica para limpiar sesión
    flash("Has cerrado sesión", "info")
    return redirect(url_for('auth_bp.login'))