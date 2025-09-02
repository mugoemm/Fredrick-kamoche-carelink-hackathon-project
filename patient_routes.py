from flask import Blueprint, request, jsonify
from extensions import db
from models import Patient, User
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

patient_bp = Blueprint('patient_bp', __name__)

@patient_bp.route('/', methods=['GET'])
@jwt_required(optional=True)
def list_patients():
    patients = Patient.query.all()
    out = []
    for p in patients:
        user = User.query.get(p.user_id) if p.user_id else None
        out.append({
            "patient_id": p.patient_id,
            "full_name": user.full_name if user else None,
            "email": user.email if user else None,
            "phone": user.phone if user else None,
            "dob": p.dob.isoformat() if p.dob else None,
            "gender": p.gender,
            "address": p.address,
            "blood_group": p.blood_group
        })
    return jsonify(out), 200

@patient_bp.route('/<int:patient_id>', methods=['GET'])
@jwt_required(optional=True)
def get_patient(patient_id):
    p = Patient.query.get_or_404(patient_id)
    user = User.query.get(p.user_id) if p.user_id else None
    return jsonify({
        "patient_id": p.patient_id,
        "full_name": user.full_name if user else None,
        "email": user.email if user else None,
        "phone": user.phone if user else None,
        "dob": p.dob.isoformat() if p.dob else None,
        "gender": p.gender,
        "address": p.address,
        "blood_group": p.blood_group
    }), 200

@patient_bp.route('/', methods=['POST'])
@jwt_required()
def create_patient():
    data = request.get_json() or {}

    # require minimal fields if creating user
    if not data.get('user_id'):
        for r in ('full_name','email','password'):
            if not data.get(r):
                return jsonify({"error": f"'{r}' required when user_id not provided"}), 400
        if User.query.filter_by(email=data['email']).first():
            return jsonify({"error":"email exists"}), 400
        user = User(full_name=data['full_name'], email=data['email'], role='patient', phone=data.get('phone'))
        user.set_password(data['password'])
        db.session.add(user)
        db.session.flush()
        user_id = user.user_id
    else:
        user_id = data.get('user_id')
        if not User.query.get(user_id):
            return jsonify({"error":"user_id not found"}), 404

    dob = None
    if data.get('dob'):
        try:
            dob = datetime.fromisoformat(data['dob']).date()
        except Exception:
            return jsonify({"error":"dob must be YYYY-MM-DD"}), 400

    patient = Patient(user_id=user_id, dob=dob, gender=data.get('gender'), address=data.get('address'), blood_group=data.get('blood_group'))
    db.session.add(patient)
    db.session.commit()
    return jsonify({"message":"patient created","patient_id":patient.patient_id}), 201
