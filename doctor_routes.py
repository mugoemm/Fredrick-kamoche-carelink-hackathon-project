from flask import Blueprint, request, jsonify
from extensions import db
from models import Doctor, User
from flask_jwt_extended import jwt_required

doctor_bp = Blueprint('doctor_bp', __name__)

@doctor_bp.route('/', methods=['GET'])
def list_doctors():
    docs = Doctor.query.all()
    out = []
    for d in docs:
        user = User.query.get(d.user_id) if d.user_id else None
        out.append({
            "doctor_id": d.doctor_id,
            "full_name": user.full_name if user else None,
            "email": user.email if user else None,
            "specialization": d.specialization,
            "experience_years": d.experience_years,
            "license_no": d.license_no
        })
    return jsonify(out), 200

@doctor_bp.route('/', methods=['POST'])
@jwt_required()
def add_doctor():
    data = request.get_json() or {}
    # Expect user_id existing or create via users route
    if not data.get('user_id'):
        return jsonify({"error":"user_id required"}), 400
    if not User.query.get(data['user_id']):
        return jsonify({"error":"user_id not found"}), 404
    doc = Doctor(user_id=data['user_id'], specialization=data.get('specialization'), experience_years=data.get('experience_years'), license_no=data.get('license_no'))
    db.session.add(doc)
    db.session.commit()
    return jsonify({"message":"doctor added","doctor_id":doc.doctor_id}), 201
