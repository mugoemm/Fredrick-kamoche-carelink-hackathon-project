from flask import Blueprint, request, jsonify
from extensions import db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/', methods=['GET'])
def list_users():
    users = User.query.all()
    out = [{"user_id": u.user_id, "full_name": u.full_name, "email": u.email, "role": u.role, "phone": u.phone} for u in users]
    return jsonify(out), 200

@user_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json() or {}
    required = ['full_name', 'email', 'password', 'role']
    for r in required:
        if r not in data:
            return jsonify({"error": f"'{r}' required"}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already exists"}), 400

    user = User(full_name=data['full_name'], email=data['email'], role=data['role'], phone=data.get('phone'))
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message":"user created", "user_id": user.user_id}), 201

@user_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json() or {}
    email = data.get('email'); password = data.get('password')
    if not email or not password:
        return jsonify({"error":"email & password required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error":"invalid credentials"}), 401

    token = create_access_token(identity={"user_id": user.user_id, "role": user.role})
    return jsonify({"access_token": token, "user": {"user_id": user.user_id, "full_name": user.full_name, "role": user.role}}), 200

@user_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    identity = get_jwt_identity()
    uid = identity.get('user_id')
    user = User.query.get(uid)
    if not user:
        return jsonify({"error":"not found"}), 404
    return jsonify({"user_id": user.user_id, "full_name": user.full_name, "email": user.email, "role": user.role}), 200
