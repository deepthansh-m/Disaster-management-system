# backend/middleware/error_handler.py
from flask import jsonify

def handle_error(error):
    """Global error handler for the application"""
    response = {
        "error": str(error),
        "status": "error"
    }
    return jsonify(response), 500