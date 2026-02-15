from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from models import User

def role_required(required_role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get('role')
            
            if user_role != required_role:
                return jsonify({'error': f'Access denied. {required_role.capitalize()} role required'}), 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def get_current_user():
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    return User.query.get(user_id)
