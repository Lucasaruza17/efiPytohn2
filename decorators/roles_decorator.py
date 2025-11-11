from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt

def roles_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims.get("role") not in roles:
                return jsonify({"msg": "Permiso denegado"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper