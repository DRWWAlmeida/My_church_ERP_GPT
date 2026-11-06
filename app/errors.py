from flask import Blueprint, jsonify

from app.core.errors import ValidationError, OperationalError, IntegrityError

errors_bp = Blueprint('errors', __name__)

@errors_bp.app_errorhandler(ValidationError)
def handle_validation_error(e):
    if e.field is None:
        response = {
            "message": e.message,
            "status": "error"
        }
        return jsonify(response), e.status_code
    else:
        response = {
            "message": e.message,
            "data": {e.field: e.value},
            "status": "error"
        }
        return jsonify(response), e.status_code

@errors_bp.app_errorhandler(OperationalError)
def handle_operational_error(e):
    response = {
        "message": e.message,
        "status": "error"
    }
    return jsonify(response), e.status_code

@errors_bp.app_errorhandler(IntegrityError)
def handle_integrity_error(e):
    if e.field is None:
        response = {
            "message": e.message,
            "status": "error"
        }
        return jsonify(response), e.status_code
    else:
        response = {
            "message": e.message,
            "data": {e.field: e.value},
            "status": "error"
        }
        return jsonify(response), e.status_code
