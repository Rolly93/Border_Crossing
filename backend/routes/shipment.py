from backend.db.db import insertData, updateData , getData
from backend.exception.exceptions import ShipmentValidationError
from backend.utility.xml_export import eventcreador
from flask import Blueprint, jsonify, request, redirect, url_for, flash
from backend.utility.shipment_logic import format_for_display , validate_client_shipment


# Create the Blueprint
shipment_bp = Blueprint('shipment_bp', __name__)

@shipment_bp.route('/newshipment', methods=['POST'])
def new_shipment():
    shipment_details = request.form.to_dict()
    
    try:
        shipment_details = validate_client_shipment(shipment_details)
      
        insertData(shipment_details)
        flash("¡Embarque guardado exitosamente!", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    return redirect(url_for('dashboard_bp.dashboard'))


# backend/routes/shipment.py
from flask import jsonify


@shipment_bp.route('/shipmentupdate', methods=['POST'])
def updateShipment():

    changes = request.get_json()
    

    try:
        
        format_for_display(changes)
        updateData(changes)

        eventcreador(changes)
        flash("¡Cambios aplicados!", "success")
        return jsonify({"status": "success", 
                        "action": "redirect",
                        "url": url_for('dashboard_bp.dashboard')}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500