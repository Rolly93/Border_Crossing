from backend.db.db import getData
# backend/routes/api.py
from flask import Blueprint, jsonify
from flask_login import login_required , current_user
api_bp = Blueprint('api', __name__)

@api_bp.route('/api/updateShipment/<ref_id>')
@login_required
def get_shipment(ref_id):
    print("Fetching shipment with ref_id:", ref_id)
    
    shipment = next((item for item in getData() if item['trans_ref'] == ref_id), None)
    if shipment:
        return jsonify(shipment)
    return jsonify({"error": "Shipment not found"}), 404