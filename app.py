# app.py
from flask import Flask, jsonify
from config import Config
from extensions import init_extensions, db
from models import *  # Import all models so SQLAlchemy knows them

# Import blueprints
from routes.auth_routes import auth_bp
from routes.appointment_routes import appointment_bp
from routes.billing_routes import billing_bp
from routes.patient_routes import patient_bp
from routes.doctor_routes import doctor_bp
from routes.queue_routes import queue_bp
from routes.record_routes import record_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init extensions (db, jwt, cors)
    init_extensions(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(appointment_bp)
    app.register_blueprint(billing_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(queue_bp)
    app.register_blueprint(record_bp)

    # Health check route
    @app.route("/")
    def index():
        return jsonify({
            "status": "active",
            "message": "CareLink API is running",
            "version": "1.0.0"
        })

    return app


app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # auto-create tables
    app.run(debug=True)
