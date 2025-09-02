from flask import Blueprint, request, jsonify
from extensions import db
from models import Billing, Patient
from flask_jwt_extended import jwt_required
import time

billing_bp = Blueprint('billing_bp', __name__)

@billing_bp.route('/', methods=['GET'])
@jwt_required(optional=True)
def list_bills():
    bills = Billing.query.order_by(Billing.created_at.desc()).all()
    out = [{"bill_id": b.bill_id, "patient_id": b.patient_id, "amount": float(b.amount), "status": b.status} for b in bills]
    return jsonify(out), 200

@billing_bp.route('/', methods=['POST'])
@jwt_required()
def create_bill():
    data = request.get_json() or {}
    if 'patient_id' not in data or 'amount' not in data:
        return jsonify({"error":"patient_id and amount required"}), 400
    if not Patient.query.get(data['patient_id']):
        return jsonify({"error":"patient not found"}), 404
    bill = Billing(patient_id=data['patient_id'], amount=data['amount'], status=data.get('status','unpaid'))
    db.session.add(bill)
    db.session.commit()
    return jsonify({"message":"bill created","bill_id": bill.bill_id}), 201

@billing_bp.route('/<int:bill_id>/pay', methods=['POST'])
@jwt_required()
def pay_bill(bill_id):
    bill = Billing.query.get_or_404(bill_id)
    bill.status = 'paid'
    db.session.commit()
    return jsonify({"message":"bill marked as paid","bill_id": bill.bill_id}), 200

@billing_bp.route('/process-payment', methods=['POST'])
def process_payment():
    data = request.get_json()
    required_fields = ['patient_id', 'amount', 'phone_number']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    return jsonify({
        'message': 'Payment simulation successful',
        'payment_id': f"sim_{int(time.time())}",
        'status': 'completed',
        'amount': data['amount'],
        'patient_id': data['patient_id']
    }), 200
