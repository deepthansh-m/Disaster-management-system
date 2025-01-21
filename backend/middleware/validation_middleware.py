from flask import request, jsonify

def validate_json(func):
    """Middleware to validate JSON payloads."""
    def wrapper(*args, **kwargs):
        if not request.is_json:
            return jsonify({"status": "error", "message": "Invalid or missing JSON"}), 400
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper
