from flask import Blueprint, jsonify, request
from backend.config.database import get_db
from backend.ml.models.models import DisasterHistory
from sqlalchemy.exc import SQLAlchemyError
from flask_cors import CORS


disaster_bp = Blueprint('disaster', __name__, url_prefix='/api/disasters/')

@disaster_bp.route('/', methods=['GET'])
def get_disasters():
    """Fetch all disaster records."""
    try:
        db_session = get_db()
        disasters = db_session.query(DisasterHistory).all()
        return jsonify([disaster.to_dict() for disaster in disasters]), 200
    except SQLAlchemyError as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@disaster_bp.route('/', methods=['POST'])
def add_disaster():
    """Add a new disaster record."""
    try:
        data = request.json
        db = next(get_db())
        new_disaster = DisasterHistory(
            disaster_type=data['disaster_type'],
            location=data['location'],
            date=data['date'],
            description=data.get('description')
        )
        db.add(new_disaster)
        db.commit()
        return jsonify({"status": "success", "message": "Disaster record added successfully"}), 201
    except SQLAlchemyError as e:
        db.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500