from backend.db.db import getData
from flask_login import login_required , current_user

from flask import Blueprint, render_template , request , redirect ,url_for
dashboard_bp = Blueprint('dashboard_bp', __name__)




@dashboard_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    # Obtenemos los datos de la base de datos
    data = getData()
    print(data.__len__( ))
    return render_template('dashboard.html', shipment=data)