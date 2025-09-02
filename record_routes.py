from flask import Blueprint, request, jsonify
from extensions import db
from models import MedicalRecord, Patient, Doctor
from flask_jwt_extended import jwt_required

record_bp = Blueprint('record_bp', __name__)

@record_bp.route('/', methods=['GET'])
@jwt_required(optional=True)
def list_records():
    recs = MedicalRecord.query.order_by(MedicalRecord.created_at.desc()).all()
    out = []
    for r in recs:
        out.append({
            "record_id": r.record_id,
            "patient_id": r.patient_id,
            "doctor_id": r.doctor_id,
            "diagnosis": r.diagnosis,
            "prescribed_drugs": r.prescribed_drugs,
            "tests_ordered": r.tests_ordered,
            "created_at": r.created_at.isoformat()
        })
    return jsonify(out), 200

@record_bp.route('/', methods=['POST'])
@jwt_required()
def add_record():
    data = request.get_json() or {}
    required = ['patient_id','doctor_id','diagnosis']
    for r in required:
        if r not in data:
            return jsonify({"error": f"'{r}' required"}), 400
    if not Patient.query.get(data['patient_id']) or not Doctor.query.get(data['doctor_id']):
        return jsonify({"error":"patient or doctor not found"}), 404
    rec = MedicalRecord(patient_id=data['patient_id'], doctor_id=data['doctor_id'], diagnosis=data['diagnosis'], prescribed_drugs=data.get('prescribed_drugs'), tests_ordered=data.get('tests_ordered'))
    db.session.add(rec)
    db.session.commit()
    return jsonify({"message":"medical record added","record_id":rec.record_id}), 201
