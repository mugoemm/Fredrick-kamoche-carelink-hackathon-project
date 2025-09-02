from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'doctor','patient','admin'
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Patient(db.Model):
    __tablename__ = "patients"
    patient_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), unique=True)
    dob = db.Column(db.Date)
    gender = db.Column(db.String(10))
    address = db.Column(db.Text)
    blood_group = db.Column(db.String(5))

class Doctor(db.Model):
    __tablename__ = "doctors"
    doctor_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), unique=True)
    specialization = db.Column(db.String(100))
    experience_years = db.Column(db.Integer)
    license_no = db.Column(db.String(50), unique=True)

class Appointment(db.Model):
    __tablename__ = "appointments"
    appointment_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.doctor_id'))
    appointment_time = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='pending')

class MedicalRecord(db.Model):
    __tablename__ = "medical_records"
    record_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.doctor_id'))
    diagnosis = db.Column(db.Text)
    prescribed_drugs = db.Column(db.Text)
    tests_ordered = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Queue(db.Model):
    __tablename__ = "queue"
    queue_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.doctor_id'))
    position = db.Column(db.Integer)
    status = db.Column(db.String(20), default='waiting')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Billing(db.Model):
    __tablename__ = "billing"
    bill_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'))
    amount = db.Column(db.Numeric(10,2))
    status = db.Column(db.String(20), default='unpaid')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
