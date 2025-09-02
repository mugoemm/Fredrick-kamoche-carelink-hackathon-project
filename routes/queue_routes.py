from flask import Blueprint, request, jsonify
from extensions import db
from models import Queue, Patient, Doctor
from flask_jwt_extended import jwt_required

queue_bp = Blueprint('queue_bp', __name__)

@queue_bp.route('/', methods=['GET'])
@jwt_required(optional=True)
def list_queue():
    q = Queue.query.order_by(Queue.position).all()
    out = [{"queue_id": item.queue_id, "patient_id": item.patient_id, "doctor_id": item.doctor_id, "position": item.position, "status": item.status} for item in q]
    return jsonify(out), 200
