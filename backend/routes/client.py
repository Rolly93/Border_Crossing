from flask_login import login_required , current_user
from flask import Blueprint, render_template , request,redirect , url_for , flash

client_bp = Blueprint('client_bp', __name__)

clientedata = [{
    "compania":'expeditors',
    'host': 'example@sftp.com',
    'port' : '22',
    'password' : 'testingpassword',
    'ruta': 'test/route/out/path/here',
    'filesender':'si'
}]


@client_bp.route('/client_dash', methods=["GET"])
@login_required
def client_dash():


    #if isadmit:
    return render_template('client.html' , cliente=clientedata)
    #else:
    #    return redirect(url_for('auth_bp.login'))

@client_bp.route('/cliente<int:user_id>', methods=['POST'])
@login_required
def alta_cliente():
    pass

