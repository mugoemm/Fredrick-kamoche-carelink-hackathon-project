from flask import Blueprint, request, jsonify
from extensions import db
from models import Appointment, Patient, Doctor
from flask_jwt_extended import jwt_required

appointment_bp = Blueprint('appointment_bp', __name__)

@appointment_bp.route('/', methods=['GET'])
@jwt_required(optional=True)
def list_appointments():
    apps = Appointment.query.order_by(Appointment.appointment_time.desc()).all()
    out = []
    for a in apps:
        out.append({
            "appointment_id": a.appointment_id,
            "patient_id": a.patient_id,
            "doctor_id": a.doctor_id,
            "appointment_time": a.appointment_time.isoformat() if a.appointment_time else None,
            "status": a.status
        })
    return jsonify(out), 200

@appointment_bp.route('/', methods=['POST'])
def create_appointment():
    data = request.get_json() or {}
    required = ['patient_id','doctor_id','appointment_time']
    for r in required:
        if r not in data:
            return jsonify({"error": f"'{r}' required"}), 400
    # optional: validate existence
    if not Patient.query.get(data['patient_id']):
        return jsonify({"error":"patient not found"}), 404
    if not Doctor.query.get(data['doctor_id']):
        return jsonify({"error":"doctor not found"}), 404

    from datetime import datetime
    try:
        appt_time = datetime.fromisoformat(data['appointment_time'])
    except Exception:
        return jsonify({"error":"appointment_time must be ISO format"}), 400

    a = Appointment(patient_id=data['patient_id'], doctor_id=data['doctor_id'], appointment_time=appt_time, status=data.get('status','pending'))
    db.session.add(a)
    db.session.commit()
    return jsonify({"message":"appointment created","appointment_id":a.appointment_id}), 201
