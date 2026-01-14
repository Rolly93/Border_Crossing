
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


@auth_bp.route('/register/<token>', methods =['GET','POST'])
def register(token):
    #valodar el otken (podria ser un codigo que se guarde en la DB con tiempo de expiracion)
    if not auth_service.calidar_token_registro(token):
        flash("El enlace de registro es invalido o ha expirado","danger")
        return redirect(url_for('auth_bp.login'))
    
    if request.method == 'POST':

        #metodo para crear el primer usuario admin
        email = request.form.get('email')
        password = request.form.get('password')
        
        exito =auth_service.crear_usuario_inicial(email,password,token)
        if exito:
            flash("Cuenta configurada con exito . Ta puedes iniciar sesion","success")
            return redirect(url_for('auth_bp.login'))
    return render_template('register.html', token=token)


@auth_bp.route('/logout')
@login_required
def logout():
    # Lógica para limpiar sesión
    flash("Has cerrado sesión", "info")
    return redirect(url_for('auth_bp.login'))