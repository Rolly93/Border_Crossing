from flask_login import login_required , current_user
from flask import Blueprint, render_template , request , redirect ,url_for , flash

employee_bp = Blueprint('employee_bp', __name__)

EMPLOYEE_DATA = [
    {
    "id": "1",
    "nombre": "Rolando Rios",
    "email": "testsadmit@example.com",
    "rol": "Administrador"
    },
    {
        "id":"2",
        "nombre":"Juan pablo",
        "email": "null",
        "rol": "CSR"
    } ,
    {
        "id":'3',
        "nombre":"Rosendo",
        "email": "null",
        "rol": "Operador"
    }
]

@employee_bp.route('/employee', methods=["GET"])
@login_required
def employee():
    return render_template('employee.html' , employee=EMPLOYEE_DATA)
    