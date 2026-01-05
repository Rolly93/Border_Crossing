from backend.db.db import getData
from flask import Blueprint, render_template

dashboard_bp = Blueprint('dashboard_bp', __name__)

@dashboard_bp.route('/dashboard', methods=['GET'])
def dashboard():
    # Obtenemos los datos de la base de datos
    data = getData()
  
    return render_template('dashboard.html', shipment=data)