from app import create_app
from extensions import db
from models import User, Doctor, Patient
app = create_app()

with app.app_context():
    # Admin
    if not User.query.filter_by(email='admin@example.com').first():
        admin = User(full_name='Admin User', email='admin@example.com', role='admin', phone='0700000000')
        admin.set_password('Admin#123')
        db.session.add(admin)

    # Doctor
    if not User.query.filter_by(email='jane.mwangi@example.com').first():
        duser = User(full_name='Dr. Jane Mwangi', email='jane.mwangi@example.com', role='doctor', phone='0712345678')
        duser.set_password('Doctor#123')
        db.session.add(duser)
        db.session.flush()
        doctor = Doctor(user_id=duser.user_id, specialization='General Medicine', experience_years=8, license_no='DOC1001')
        db.session.add(doctor)

    # Patient
    if not User.query.filter_by(email='john.kamau@example.com').first():
        puser = User(full_name='John Kamau', email='john.kamau@example.com', role='patient', phone='0734567890')
        puser.set_password('Patient#123')
        db.session.add(puser)
        db.session.flush()
        patient = Patient(user_id=puser.user_id, dob='1990-05-12', gender='male', address='123 Meru Street', blood_group='O+')
        db.session.add(patient)

    db.session.commit()
    print("Seeded sample users/doctors/patients")
